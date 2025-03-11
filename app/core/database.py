import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import configs

cred = credentials.Certificate(configs.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {"projectId": configs.FIREBASE_PROJECT})
db = firestore.client()
