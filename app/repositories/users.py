from uuid import uuid4
from typing import List, Optional
from firebase_admin.firestore import SERVER_TIMESTAMP
from app.schemas.users import UserCreate, UserUpdate
from google.cloud.firestore_v1.base_query import FieldFilter

class UserRepository:
    def __init__(self, db):
        self.collection = db.collection("users")

    def create(self, user: UserCreate) -> dict:
        user_id = str(uuid4())
        user_data = user.model_dump()
        user_data.update({"id": user_id, "created_at": SERVER_TIMESTAMP})
        self.collection.document(user_id).set(user_data)
        return user_data

    def get_by_id(self, user_id: str) -> Optional[dict]:
        doc = self.collection.document(user_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def get_by_email(self, email: str) -> Optional[dict]:
        docs = self.collection.where(filter=FieldFilter("email", "==", email)).stream()
        for doc in docs:
            return doc.to_dict()
        return None

    def get_all(self) -> List[dict]:
        docs = self.collection.stream()
        return [doc.to_dict() for doc in docs]

    def update(self, user_id: str, user: UserUpdate) -> Optional[dict]:
        doc_ref = self.collection.document(user_id)
        if not doc_ref.get().exists:
            return None
        
        data = user if isinstance(user, dict) else user.model_dump(exclude_unset=True)
        data["updated_at"] = SERVER_TIMESTAMP
        doc_ref.update(data)
        return doc_ref.get().to_dict()
    
    def delete(self, user_id: str) -> bool:
        doc_ref = self.collection.document(user_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False
