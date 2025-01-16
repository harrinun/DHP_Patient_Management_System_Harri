import re  # For validating input formats using regular expressions
from datetime import datetime as dt  # Alias datetime class as dt for better readability

# Initialize patient records and unique ID counter
patient_records = []  # List to store all patient records
next_id = 1  # Auto-incrementing ID for patients


def calculate_age(date_of_birth):
    """
    Calculates a person's age given their date of birth.
    """
    birth_date = dt.strptime(date_of_birth, "%d-%m-%Y")  # Convert the date string into a datetime object
    today = dt.today()  # Get current date
    # Subtract birth year from current year and adjust if the birthday hasn't occurred yet this year
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def validate_date_of_birth(date_of_birth):
    """
    Validates the date of birth format and ensures it's a valid date.
    """
    try:
        # Match the format 'dd-mm-yyyy'
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_of_birth):
            return False
        # Split the date string into day, month, and year and convert them to integers
        day, month, year = map(int, date_of_birth.split('-'))
        dt(year, month, day)  # Create datetime object and raises ValueError if the date is invalid
        return True
    except ValueError:
        return False


def validate_phone_number(phone_number):
    """
    Validates the phone number format.
    """
    return bool(re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number))


def add_patient():
    """
    Adds a new patient to the patient records.
    """
    global next_id  # Reference the global ID counter
    print("\n--- Add New Patient ---")

    # Input and validate patient details
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()

    while True:
        date_of_birth = input("Enter Date of Birth (dd-mm-yyyy): ").strip()
        if validate_date_of_birth(date_of_birth):
            break
        print("Invalid date format. Please enter a valid date (dd-mm-yyyy).")

    while True:
        phone_number = input("Enter Phone Number (024-000-0000): ").strip()
        if validate_phone_number(phone_number):
            break
        print("Invalid phone number format. Please use 024-000-0000.")

    hometown = input("Enter Hometown: ").strip()
    house_number = input("Enter House Number: ").strip()

    # Calculate age and create patient record
    age = calculate_age(date_of_birth)
    patient = {
        "id": next_id,
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "age": age,
        "hometown": hometown,
        "house_number": house_number,
        "phone_number": phone_number,
    }
    patient_records.append(patient)  # Add patient to the patient records
    next_id += 1  # Increment ID for the next patient
    print("Patient added successfully!")


def get_all_patients():
    """
    Displays all patient records in a readable format.
    """
    print("\n--- Patient Records ---")
    if not patient_records: # Checks if there are no patient records.
        print("No patient records found.")
        return
    for patient in patient_records:
        print(f"ID: {patient['id']}, Name: {patient['first_name']} {patient['last_name']}, "
              f"Age: {patient['age']}, Hometown: {patient['hometown']}, Phone: {patient['phone_number']}")


def search_patient_by_id(patient_id):
    """
    Searches and displays a patient record by their ID.
    """
    print("\n--- Search Patient ---")
    for patient in patient_records:
        if patient['id'] == patient_id:
            print(f"ID: {patient['id']}, Name: {patient['first_name']} {patient['last_name']}, "
                  f"Age: {patient['age']}, Hometown: {patient['hometown']}, Phone: {patient['phone_number']}")
            return
    print("Patient not found.")


def update_patient_by_id(patient_id):
    """
    Updates a patient's record by their ID.
    """
    print("\n--- Update Patient ---")
    for patient in patient_records:
        if patient['id'] == patient_id:
            print(f"Updating record for {patient['first_name']} {patient['last_name']} (ID: {patient['id']})")
            patient['first_name'] = input("Update First Name or (leave blank to keep current name): ") or patient['first_name']
            patient['last_name'] = input("Update Last Name or (leave blank to keep current name): ") or patient['last_name']
            while True:
                new_date_of_birth = input("Update new Date of Birth (dd-mm-yyyy, or leave blank to keep current): ").strip()
                if not new_date_of_birth or validate_date_of_birth(new_date_of_birth):
                    break
                print("Invalid date format. Please enter a valid date (dd-mm-yyyy).")
            if new_date_of_birth:
                patient['date_of_birth'] = new_date_of_birth
                patient['age'] = calculate_age(new_date_of_birth)
            patient['hometown'] = input("Update Hometown or (leave blank to keep current): ") or patient['hometown']
            patient['house_number'] = input("Update House Number or (leave blank to keep current): ") or patient['house_number']
            print("Patient record updated successfully!")
            return
    print("Patient not found.")


def delete_patient_by_id(patient_id):
    """
    Deletes a patient's record by their ID.
    """
    print("\n--- Delete Patient ---")
    for patient in patient_records:
        if patient['id'] == patient_id:
            patient_records.remove(patient)
            print(f"Patient with ID {patient_id} has been deleted.")
            return
        print("Patient not found.")


def main():
    """
    Provides a menu-based interface for the user.
    """
    while True:
        print("\n--- Patient Management System ---\n==================================")
        print("1. Add New Patient")
        print("2. Get All Patients")
        print("3. Search Patient by ID")
        print("4. Update Patient by ID")
        print("5. Delete Patient by ID")
        print("6. Exit")

        choice = input("Select a number above to perform the corresponding task (1-6): ").strip()
        if choice == "1":
            add_patient()
        elif choice == "2":
            get_all_patients()
        elif choice == "3":
            patient_id = int(input("Enter Patient ID to Search: ").strip())
            search_patient_by_id(patient_id)
        elif choice == "4":
            patient_id = int(input("Enter Patient ID to Update: ").strip())
            update_patient_by_id(patient_id)
        elif choice == "5":
            patient_id = int(input("Enter Patient ID to Delete: ").strip())
            delete_patient_by_id(patient_id)
        elif choice == "6":
            print("Closing the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()

