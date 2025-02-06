import re
import csv
import json
from datetime import datetime

# Global variables
PATIENTS = []  # Temporary list to store patients during runtime
PATIENT_ID_COUNTER = 1  # Auto-incrementing patient ID
STORAGE_TYPE = None  # Will be set to 'csv' or 'json' based on user choice

# Function to validate date of birth format and validity
def validate_date_of_birth(dob):
    # Regex to match dd-mm-yyyy format
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", dob):
        return False, "Invalid date format. Use dd-mm-yyyy."

    try:
        # Parse the date using datetime.strptime
        date_obj = datetime.strptime(dob, "%d-%m-%Y")
        return True, "Valid date."
    except ValueError:
        return False, "Invalid date. Please check the day, month, and year."

# Function to validate phone number format
def validate_phone_number(phone):
    if re.match(r"^\d{3}-\d{3}-\d{4}$", phone):
        return True, "Valid phone number."
    else:
        return False, "Invalid phone number format. Use 024-000-0000."

# Function to calculate age from date of birth
def calculate_age(dob):
    day, month, year = map(int, dob.split('-'))
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

# Function to add a new patient
def add_patient():
    global PATIENT_ID_COUNTER

    print("\nAdd New Patient")

    # First Name
    first_name = input("First Name: ").strip()
    if not first_name:
        print("First Name cannot be empty.")
        return

    # Last Name
    last_name = input("Last Name: ").strip()
    if not last_name:
        print("Last Name cannot be empty.")
        return

    # Date of Birth
    while True:
        date_of_birth = input("Date of Birth (dd-mm-yyyy): ").strip()
        is_valid_dob, dob_message = validate_date_of_birth(date_of_birth)
        if is_valid_dob:
            break
        else:
            print(dob_message)

    # Hometown
    hometown = input("Hometown: ").strip()
    if not hometown:
        print("Hometown cannot be empty.")
        return

    # House Number
    house_number = input("House Number: ").strip()
    if not house_number:
        print("House Number cannot be empty.")
        return

    # Phone Number
    while True:
        phone_number = input("Phone Number (024-000-0000): ").strip()
        is_valid_phone, phone_message = validate_phone_number(phone_number)
        if is_valid_phone:
            break
        else:
            print(phone_message)

    # Calculate age
    age = calculate_age(date_of_birth)

    # Create patient dictionary
    patient = {
        "id": PATIENT_ID_COUNTER,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "age": age,
        "hometown": hometown,
        "house_number": house_number,
        "phone_number": phone_number,
    }

    # Add patient to the list
    PATIENTS.append(patient)
    PATIENT_ID_COUNTER += 1

    # Save to file
    save_patients_to_file()
    print("Patient added successfully!")

# Function to save patients to file (CSV or JSON)
def save_patients_to_file():
    global STORAGE_TYPE
    if STORAGE_TYPE == "csv":
        with open("patients.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=PATIENTS[0].keys())
            writer.writeheader()
            writer.writerows(PATIENTS)
    elif STORAGE_TYPE == "json":
        with open("patients.json", mode="w") as file:
            json.dump(PATIENTS, file, indent=4)

# Function to load patients from file (CSV or JSON)
def load_patients_from_file():
    global PATIENTS, PATIENT_ID_COUNTER, STORAGE_TYPE

    try:
        if STORAGE_TYPE == "csv":
            with open("patients.csv", mode="r") as file:
                reader = csv.DictReader(file)
                PATIENTS = list(reader)
                # Convert IDs back to integers
                for patient in PATIENTS:
                    patient["id"] = int(patient["id"])
        elif STORAGE_TYPE == "json":
            with open("patients.json", mode="r") as file:
                PATIENTS = json.load(file)
                # Convert IDs back to integers
                for patient in PATIENTS:
                    patient["id"] = int(patient["id"])

        # Update the patient ID counter
        if PATIENTS:
            PATIENT_ID_COUNTER = max(patient["id"] for patient in PATIENTS) + 1
    except FileNotFoundError:
        PATIENTS = []

# Function to display all patients
def get_all_patients():
    load_patients_from_file()
    if not PATIENTS:
        print("No patients found.")
        return

    print("\nAll Patients:")
    for patient in PATIENTS:
        print(f"ID: {patient['id']}, Name: {patient['first_name']} {patient['last_name']}, "
              f"DOB: {patient['date_of_birth']}, Age: {patient['age']}, "
              f"Hometown: {patient['hometown']}, House Number: {patient['house_number']}, "
              f"Phone: {patient['phone_number']}")

# Function to search for a patient by ID
def search_patient_by_id():
    load_patients_from_file()
    if not PATIENTS:
        print("No patients found.")
        return

    try:
        patient_id = int(input("Enter patient ID: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric ID.")
        return

    for patient in PATIENTS:
        if patient["id"] == patient_id:
            print("\nPatient Found:")
            print(f"ID: {patient['id']}, Name: {patient['first_name']} {patient['last_name']}, "
                  f"DOB: {patient['date_of_birth']}, Age: {patient['age']}, "
                  f"Hometown: {patient['hometown']}, House Number: {patient['house_number']}, "
                  f"Phone: {patient['phone_number']}")
            return
    print(f"No patient found with ID {patient_id}.")

# Function to update a patient by ID
def update_patient_by_id():
    load_patients_from_file()
    if not PATIENTS:
        print("No patients found.")
        return

    try:
        patient_id = int(input("Enter patient ID: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric ID.")
        return

    for patient in PATIENTS:
        if patient["id"] == patient_id:
            print("\nUpdate Patient:")
            print("Leave the field blank to keep the current value.")
            first_name = input(f"First Name ({patient['first_name']}): ").strip() or patient['first_name']
            last_name = input(f"Last Name ({patient['last_name']}): ").strip() or patient['last_name']
            date_of_birth = input(f"Date of Birth ({patient['date_of_birth']}): ").strip() or patient['date_of_birth']
            hometown = input(f"Hometown ({patient['hometown']}): ").strip() or patient['hometown']
            house_number = input(f"House Number ({patient['house_number']}): ").strip() or patient['house_number']
            phone_number = input(f"Phone Number ({patient['phone_number']}): ").strip() or patient['phone_number']

            # Validate date of birth
            is_valid_dob, dob_message = validate_date_of_birth(date_of_birth)
            if not is_valid_dob:
                print(dob_message)
                return

            # Validate phone number
            is_valid_phone, phone_message = validate_phone_number(phone_number)
            if not is_valid_phone:
                print(phone_message)
                return

            # Update patient details
            patient["first_name"] = first_name
            patient["last_name"] = last_name
            patient["date_of_birth"] = date_of_birth
            patient["age"] = calculate_age(date_of_birth)
            patient["hometown"] = hometown
            patient["house_number"] = house_number
            patient["phone_number"] = phone_number

            # Save to file
            save_patients_to_file()
            print("Patient updated successfully!")
            return
    print(f"No patient found with ID {patient_id}.")

# Function to delete a patient by ID
def delete_patient_by_id():
    load_patients_from_file()
    if not PATIENTS:
        print("No patients found.")
        return

    try:
        patient_id = int(input("Enter patient ID: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric ID.")
        return

    for patient in PATIENTS:
        if patient["id"] == patient_id:
            PATIENTS.remove(patient)
            save_patients_to_file()
            print(f"Patient with ID {patient_id} deleted successfully!")
            return
    print(f"No patient found with ID {patient_id}.")

# Main function
def main():
    global STORAGE_TYPE

    print("Welcome to the DHP Patient Management System!")
    print("Choose storage type:")
    print("1. CSV")
    print("2. JSON")

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == "1":
            STORAGE_TYPE = "csv"
            break
        elif choice == "2":
            STORAGE_TYPE = "json"
            break
        else:
            print("Invalid choice. Please enter 1 for CSV or 2 for JSON.")

    load_patients_from_file()

    while True:
        print("\nMenu:")
        print("1. Add New Patient")
        print("2. Get All Patients")
        print("3. Search Patient by ID")
        print("4. Update Patient by ID")
        print("5. Delete Patient by ID")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            get_all_patients()
        elif choice == "3":
            search_patient_by_id()
        elif choice == "4":
            update_patient_by_id()
        elif choice == "5":
            delete_patient_by_id()
        elif choice == "6":
            print("Goodbye")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()