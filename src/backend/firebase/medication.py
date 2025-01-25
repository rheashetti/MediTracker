import google.generativeai as genai
import firebase
from Flask import request

gemini_key = 'AIzaSyDkE81Ak7eGmrzcahcxeXWBaF9YiFqwn94'

def generate(medicine_list):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Are there any incompatabilties with any of these medicines: {medicine_list}")
    return response.text

def get_medication():
    db = firebase.db
    patient_name = request.args.get("patient_name")
    patient_data = db.collection(patient_name).document("medicine").get("name")
    medicine_list = patient_data.get("name", [])
    return medicine_list

def check_medication_incompatibilities():
    # Get the medication list for a specific patient
    medicine_list = get_medication()
    # Check for incompatibilities
    incompatibilities = generate(medicine_list)
    return incompatibilities
