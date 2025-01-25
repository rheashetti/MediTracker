import firebase
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = firebase.db

@app.route("/")
def hello():
    print("hello!")
    return "We received" + str(request.args.get("var"))

@app.route("/addprof")
def create_profile(db):
    patient_name = request.args.get("patient_name")
    email = request.args.get("patient_email")
    birthday = request.args.get("birthday")
    profile = {"email": email, "birthday": birthday}
    db.collection(patient_name).document("profile").set(profile)
    return jsonify({"patient_name": patient_name,
                    "patient_email": email,
                    "birthday": birthday})

@app.route("/adddoc")
def add_doctor_info():
    patient_name = request.args.get("patient_name")
    doctor_name = request.args.get("doctor_name")
    email = request.args.get("doctor_email")
    phone = request.args.get("doctor_phone")
    doctor = {"name": doctor_name, "email": email, "phone": phone}
    db.collection(patient_name).document("doctor").set(doctor)
    return jsonify({"doctor_name": doctor_name,
                    "doctor_email": email,
                    "doctor_phone": phone})


@app.route("/addmed")
def add_medication():
    patient_name = request.args.get("patient_name")
    med_name  = request.args.get("med_name")
    frequency = request.args.get("frequency")
    dosage = request.args.get("dosage")
    medicine = {"name": med_name, "frequency": frequency, "dosage": dosage}
    db.collection(patient_name).document("medicine").set(medicine)
    return jsonify({"med_name": med_name,
                    "frequency": frequency,
                    "dosage": dosage})


# @app.route("/delete")
# def delete_doctor_info():
#     pass

@app.route("/get")
def get_medication():
    patient_name = request.args.get("patient_name")
    coll = request.args.get("coll")
    field = request.args.get("field")

    return db.collection(patient_name).document(coll).get(field)

if __name__ == "__main__":
#     hello()
    add_doctor_info()
#   name = "Sonic"
#   create_profile(name, "sonic@hedgehog.com", "1/2/03")
#   add_doctor_info(name, "eggman", "eggman@bot.com", "123-456-7890")
#   add_medication(name, "ibuprofen", "12 hours", "1 pill")

#   name2 = "Stephen"
#   create_profile(name2, "srzacari@uci.edu", "01/10/2003")