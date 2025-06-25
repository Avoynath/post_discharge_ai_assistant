import json

# Load patient data from JSON file
def load_patient_data(filepath="data/dummy_patient_data.json"):
    with open(filepath, "r") as f:
        return json.load(f)

# Find a patient by name (case-insensitive)
def find_patient_by_name(name, patient_data):
    matches = [p for p in patient_data if p["patient_name"].lower() == name.lower()]
    if not matches:
        return None, "Patient not found."
    if len(matches) > 1:
        return None, "Multiple patients found with that name."
    return matches[0], None
