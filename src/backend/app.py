import firebase_admin
from firebase_admin import firestore, credentials
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# load_dotenv()
# PRIVATE_KEY_ID = str(os.getenv("PRIVATE_KEY_ID")) 
# PRIVATE_KEY = str(os.getenv("PRIVATE_KEY"))
# CLIENT_EMAIL = str(os.getenv("CLIENT_EMAIL"))
# CLIENT_ID = str(os.getenv("CLIENT_ID"))
# # print(type(CLIENT_ID))

# FIREBASE_JSON = {
#     "type": "service_account",
#     "project_id": "meditracker-5bf7d",
#     "private_key_id": PRIVATE_KEY_ID,
#     "private_key": PRIVATE_KEY,
#     "client_email": CLIENT_EMAIL,
#     "client_id": CLIENT_ID,
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40meditracker-5bf7d.iam.gserviceaccount.com",
#     "universe_domain": "googleapis.com"
#   }
with open('../firebase.json', 'r') as file:
    FIREBASE_JSON = json.load(file)

cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("users")

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    print("hello!")
    return "We received" + str(request.args.get("var"))

@app.route("/addprofile")
def create_profile():
    patient_name = request.args.get("patient_name")
    email = request.args.get("patient_email")
    birthday = request.args.get("birthday")
    profile = {"email": email, "birthday": birthday}
    db.collection(patient_name).document("profile").set(profile)
    return f"Profile information received.\nName is {patient_name}.\nEmail is {email}.\nBirthday is {birthday}."

@app.route("/adddoctor")
def add_doctor_info():
    patient_name = request.args.get("patient_name")
    doctor_name = request.args.get("doctor_name")
    email = request.args.get("doctor_email")
    phone = request.args.get("doctor_phone")
    doctor = {"name": doctor_name, "email": email, "phone": phone}
    db.collection(patient_name).document("doctor").set(doctor)
    return f"Doctor information received.\nName is {doctor_name}.\nEmail is {email}.\nPhone is {phone}."

@app.route("/addmed")
def add_medication(patient_name, medicine, frequency, dosage):
    patient_name = request.args.get("patient_name")
    med_name  = request.args.get("med_name")
    freqeuncy = request.args.get("frequency")
    dosage = request.args.get("dosage")
    medicine = {"name": med_name, "frequency": frequency, "dosage": dosage}
    db.collection(patient_name).document("medicine").set(medicine)
    return f"Medication information received.\nName is {med_name}.\nFrequency is {freqeuncy}.\Dosage is {dosage}."


# @app.route("/delete")
# def delete_doctor_info():
#     pass

# @app.route("/get")
# def get_medication():
#     pass

if __name__ == "__main__":
#     hello()
    add_doctor_info()
#   name = "Sonic"
#   create_profile(name, "sonic@hedgehog.com", "1/2/03")
#   add_doctor_info(name, "eggman", "eggman@bot.com", "123-456-7890")
#   add_medication(name, "ibuprofen", "12 hours", "1 pill")

#   name2 = "Stephen"
#   create_profile(name2, "srzacari@uci.edu", "01/10/2003")