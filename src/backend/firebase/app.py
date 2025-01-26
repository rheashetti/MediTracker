import firebase
from datetime import datetime
import ast
from firebase_admin import firestore
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = firebase.db

@app.route("/")
def hello():
    return jsonify({"greeting": "Welcome to MediTracker!"})


"""
Checks if the user password matches the password in the database. If it doesn't exist in the
database, it creates one.
"""
@app.route("/login", methods=['POST'])
##TODO##
def login():
    data = request.get_json()
    patient_name = data.get("patient_name")
    password_attempt = data.get("password_attempt")
    try:
        login_data = db.collection(patient_name).document("login").get()
        password = login_data.to_dict().values()[0]
        if password == password_attempt:
            return jsonify({"attempt": "Log in successful!"})
        else:
            return jsonify({"attempt": "Wrong password."})
        
    except:
        db.collection(patient_name).document("login").set({"password": password_attempt})



"""--------------------------------ADD FUNCTIONS---------------------------------------"""


"""
Gets user name, email, birthday and adds it to Firebase.
"""
@app.route("/add/profile", methods=['POST'])
def create_profile():
    print("hello!")
    data = request.get_json()
    print(data)
    patient_name = data.get("patient_name")
    email = data.get("patient_email")
    birthday = data.get("birthday")
    profile = {"email": email, "birthday": birthday}
    db.collection(patient_name).document("profile").set(profile)
    return jsonify({"patient_name": patient_name,
                    "patient_email": email,
                    "birthday": birthday})

"""
Gets user name, doctor's email, doctor's name, doctor's phone and adds it to Firebase.
"""
@app.route("/add/doctor", methods=['POST'])
def add_doctor_info():
    data = request.get_json()
    patient_name = data.get("patient_name")
    doctor_name = data.get("doctor_name")
    email = data.get("doctor_email")
    phone = data.get("doctor_phone")
    doctor = {"name": doctor_name, "email": email, "phone": phone}
    db.collection(patient_name).document("doctor").set(doctor)
    return jsonify({"doctor_name": doctor_name,
                    "doctor_email": email,
                    "doctor_phone": phone})

"""
Gets user name, medicine name, how often medicine is taken, and dosage of medicine
and adds it to Firebase.
"""
@app.route("/add/medicine", methods=['POST'])
def add_medication():
    data = request.get_json()
    print(data)
    patient_name = data.get("patient_name")
    med_name  = data.get("med_name")
    #schedule is a string of a dictorary
    #schedule = {days: [], time: []}
    dosage = data.get("dosage")
    schedule = data.get("schedule")
    medicine = {med_name: [dosage, schedule]}
    db.collection(patient_name).document("medicine").set(medicine)
    return jsonify({"med_name": med_name,
                    "schedule": schedule,
                    "dosage": dosage})



"""--------------------------DELETE FUNCTION-------------------------------"""


###TODO###
@app.route("/delete", methods=['DELETE'])
def delete_info():
    data = request.get_json()
    patient_name = data.get("patient_name")
    coll = data.get("coll")
    field = data.get("field")

    #does not allow deletion of password
    if coll == "login":
        return jsonify({field: "We delete send this information."})

    data_ref = db.collection(patient_name).document(coll)
    data_ref.update({field: None})

    return jsonify({field: f"Deleted {field} successfully."})



"""--------------------------------GET FUNCTIONS----------------------------------"""



@app.route("/get/info", methods=['GET'])
def get_info():
    data = request.get_json()
    patient_name = data.get("patient_name")
    coll = data.get("coll")
    field = data.get("field")

    #does not allow retrieval of password
    if coll == "login":
        return jsonify({field: "We cannot send this information."})

    data = db.collection(patient_name).document(coll).get()
    result = data.to_dict()[field]

    return jsonify({field: result})

@app.route("/get/schedule", methods=['GET'])
def retrieve_schedule():
    data = request.get_json()
    name = data.get("patient_name")

    # initialize all necessary data structures and variables
    schedule = {}
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    year = datetime.now().year
    month = datetime.now().month
    curr_date = datetime.now().day
    curr_day = datetime.now().weekday()
    db = firebase.db

    # pull information about all the medicines from the database
    medicine_dict = db.collection(name).document("medicine").get().to_dict()

    # sort all of the information into a dictionary with dates as the keys which are linked to a list of dictionaries that have information about what medicine to take and when
    for key, value in medicine_dict.items():
        counter = 0
        # converts all of the days for each medicine into indexes from 0-6 representing monday-sunday respectively
        day_idxs = [weekdays.index(day) for day in ast.literal_eval(value[1])['days']]
        # all of the times that are linked to each medicine in list form
        time = ast.literal_eval(value[1])['time'].split(',')
        for idx in day_idxs:
            # calculates the number of days away so it can be used for final date calculations
            if idx < curr_day:
                days_until = 7 - curr_day + idx
            else:
                days_until = idx - curr_day

            # adds the medicine and time to take it to the schedule
            if (year + "-" + month + "-" + curr_date + days_until) in schedule.keys:
                schedule[year + "-" + month + "-" + curr_date + days_until] += {'title':key, 'description': time[counter]}
            else:
                schedule[year + "-" + month + "-" + curr_date + days_until] = [{'title':key, 'description': time[counter]}]
            counter += 1
    return jsonify(schedule)


if __name__ == "__main__":
    app.run(debug=True)
    # hello()
    # add_doctor_info()
#   name = "Sonic"
#   create_profile(name, "sonic@hedgehog.com", "1/2/03")
#   add_doctor_info(name, "eggman", "eggman@bot.com", "123-456-7890")
#   add_medication(name, "ibuprofen", "12 hours", "1 pill")

#   name2 = "Stephen"
#   create_profile(name2, "srzacari@uci.edu", "01/10/2003")