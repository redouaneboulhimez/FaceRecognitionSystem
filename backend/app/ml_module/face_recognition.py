"""
Face Recognition Service
Utilise MTCNN pour la détection et FaceNet pour l'embedding
"""
import os
import numpy as np
import cv2
from PIL import Image
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import faiss
import pickle
from pathlib import Path
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Employee, EmployeePhoto

class FaceRecognitionService:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialiser MTCNN pour la détection
        self.mtcnn = MTCNN(
            image_size=160,
            margin=0,
            min_face_size=20,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=False,
            device=self.device
        )
        
        # Initialiser FaceNet pour l'embedding
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        
        # Initialiser FAISS index
        self.index_path = Path(settings.MODELS_DIR) / "faiss_index.index"
        self.metadata_path = Path(settings.MODELS_DIR) / "faiss_metadata.pkl"
        os.makedirs(settings.MODELS_DIR, exist_ok=True)
        
        self.index = None
        self.metadata = {}  # {index_id: employee_id}
        self.load_index()
    
    def detect_face(self, image_path: str) -> Optional[np.ndarray]:
        """
        Détecter et aligner un visage dans une image
        """
        try:
            img = Image.open(image_path).convert('RGB')
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Détecter le visage avec MTCNN
            boxes, probs = self.mtcnn.detect(img, landmarks=False)
            
            if boxes is None or len(boxes) == 0:
                return None
            
            # Prendre le visage avec la plus haute probabilité
            best_idx = np.argmax(probs)
            box = boxes[best_idx]
            
            # Extraire et aligner le visage
            face = self.mtcnn.extract(img, [box], save_path=None)
            
            if face is None or len(face) == 0:
                return None
            
            return face[0]
        
        except Exception as e:
            print(f"Error detecting face: {e}")
            return None
    
    def get_embedding(self, image_path: str) -> Optional[np.ndarray]:
        """
        Extraire l'embedding facial d'une image
        """
        face = self.detect_face(image_path)
        if face is None:
            return None
        
        try:
            # Normaliser l'image
            face_tensor = torch.FloatTensor(face).unsqueeze(0).to(self.device)
            face_tensor = (face_tensor - 127.5) / 128.0
            
            # Générer l'embedding
            with torch.no_grad():
                embedding = self.resnet(face_tensor)
            
            # Normaliser l'embedding
            embedding = embedding.cpu().numpy()
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding[0]
        
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def load_index(self):
        """
        Charger l'index FAISS depuis le disque
        """
        if self.index_path.exists() and self.metadata_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
            except Exception as e:
                print(f"Error loading index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """
        Créer un nouvel index FAISS vide
        """
        # Créer un index L2 (distance euclidienne)
        dimension = settings.EMBEDDING_SIZE
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = {}
    
    def save_index(self):
        """
        Sauvegarder l'index FAISS sur le disque
        """
        try:
            faiss.write_index(self.index, str(self.index_path))
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def add_to_index(self, employee_id: int, embedding: np.ndarray):
        """
        Ajouter un embedding à l'index FAISS
        """
        if self.index is None:
            self._create_new_index()
        
        # Ajouter l'embedding à l'index
        index_id = self.index.ntotal
        embedding = embedding.reshape(1, -1).astype('float32')
        self.index.add(embedding)
        
        # Sauvegarder le mapping
        self.metadata[index_id] = employee_id
        self.save_index()
    
    def search_in_index(self, embedding: np.ndarray, k: int = 1) -> Optional[Dict]:
        """
        Rechercher le visage le plus proche dans l'index
        """
        if self.index is None or self.index.ntotal == 0:
            return None
        
        embedding = embedding.reshape(1, -1).astype('float32')
        distances, indices = self.index.search(embedding, k)
        
        if len(indices[0]) == 0:
            return None
        
        idx = indices[0][0]
        distance = float(distances[0][0])
        employee_id = self.metadata.get(idx)
        
        return {
            'employee_id': employee_id,
            'distance': distance,
            'index': idx
        }
    
    def rebuild_index(self, db: Session):
        """
        Reconstruire l'index FAISS à partir de la base de données
        """
        self._create_new_index()
        
        # Récupérer tous les employés actifs
        employees = db.query(Employee).filter(Employee.is_active == True).all()
        
        for employee in employees:
            # Récupérer les photos de l'employé
            photos = db.query(EmployeePhoto).filter(
                EmployeePhoto.employee_id == employee.id
            ).all()
            
            for photo in photos:
                if os.path.exists(photo.photo_path):
                    embedding = self.get_embedding(photo.photo_path)
                    if embedding is not None:
                        self.add_to_index(employee.id, embedding)
        
        self.save_index()

