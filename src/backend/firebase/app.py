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


@app.route("/login")
def login():
    patient_name = request.args.get("patient_name")
    password_attempt = request.args.get("password")
    login_data = db.collection(patient_name).document("login").get()

    if login_data.exists:
        password = login_data.to_dict().keys()
        if password == password_attempt:
            return jsonify({"attempt": "Log in successful!"})
        else:
            return jsonify({"attempt": "Wrong password."})
    else:
        db.collection(patient_name).document("login").set(password_attempt)


"""
Gets user name, email, birthday and adds it to Firebase.
"""
@app.route("/addprof")
def create_profile():
    patient_name = request.args.get("patient_name")
    email = request.args.get("patient_email")
    birthday = request.args.get("birthday")
    profile = {"email": email, "birthday": birthday}
    db.collection(patient_name).document("profile").set(profile)
    return jsonify({"patient_name": patient_name,
                    "patient_email": email,
                    "birthday": birthday})
    # return f"Patient name is {patient_name}. Email is {email}. Birthday is {birthday}."

"""
Gets user name, doctor's email, doctor's name, doctor's phone and adds it to Firebase.
"""
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


"""
Gets user name, medicine name, how often medicine is taken, and dosage of medicine
and adds it to Firebase.
"""
@app.route("/addmed")
def add_medication():
    patient_name = request.args.get("patient_name")
    med_name  = request.args.get("med_name")
    #schedule is a string of a dictorary
    #schedule = {days: [], time: []}
    schedule = request.args.get("schedule")
    dosage = request.args.get("dosage")
    medicine = {"name": med_name, "frequency": schedule, "dosage": dosage}
    db.collection(patient_name).document("medicine").set(medicine)
    return jsonify({"med_name": med_name,
                    "schedule": schedule,
                    "dosage": dosage})


# @app.route("/delete")
# def delete_doctor_info():
#     pass

@app.route("/get")
def get_medication():#
    patient_name = request.args.get("patient_name")
    coll = request.args.get("coll")
    field = request.args.get("field")

    return db.collection(patient_name).document(coll).get()

if __name__ == "__main__":
#     hello()
    add_doctor_info()
#   name = "Sonic"
#   create_profile(name, "sonic@hedgehog.com", "1/2/03")
#   add_doctor_info(name, "eggman", "eggman@bot.com", "123-456-7890")
#   add_medication(name, "ibuprofen", "12 hours", "1 pill")

#   name2 = "Stephen"
#   create_profile(name2, "srzacari@uci.edu", "01/10/2003")