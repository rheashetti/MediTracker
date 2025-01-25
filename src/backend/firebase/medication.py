import google.generativeai as genai
import firebase
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GENAI_KEY")

def generate(medicine_list, additional):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Can you see if {additional} has any serious negative interactions with these medicines: {medicine_list}. Only  list the medicines and issues, there is no need for an introduction or summary.")
    return response.text

def get_medication(name):
    db = firebase.db
    # patient_name = request.args.get("patient_name")
    # patient_name = "Sonic"
    patient_data = db.collection(name).document("medicine").get()
    medicine_list = patient_data.to_dict().keys()
    return medicine_list

def check_medication_incompatibilities(patient_name, new):
    # Get the medication list for a specific patient
    medicine_list = get_medication(patient_name)
    # Check for incompatibilities
    incompatibilities = generate(medicine_list, new)
    return incompatibilities


if __name__ == "__main__":
    print(check_medication_incompatibilities('Sonic', 'valproate'))
    # print(generate(["lidocaine", 'ibuprofen', 'tylenol', 'cyclizine']))