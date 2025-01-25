import firebase_admin
from firebase_admin import firestore, credentials
import json

with open('../../firebase.json', 'r') as file:
    FIREBASE_JSON = json.load(file)
cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")