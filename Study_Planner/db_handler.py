import csv
import os

CSV_FILE = 'data/study_planner.csv'

def init_db():
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)

    # Create the CSV file if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'hours_per_week', 'difficulty'])  # Write header

def add_subject(name, hours_per_week, difficulty):
    # Read existing subjects
    subjects = get_subjects()
    subject_id = len(subjects) + 1  # Assign a new ID

    # Write the new subject to the CSV file
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([subject_id, name, hours_per_week, difficulty])

def get_subjects():
    subjects = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            subjects = [row for row in reader]
    return subjects

def delete_subject(subject_id):
    subjects = get_subjects()
    subjects = [subject for subject in subjects if subject[0] != str(subject_id)]  # Filter out the subject

    # Write the updated subjects back to the CSV file
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'hours_per_week', 'difficulty'])  # Write header
        writer.writerows(subjects)  # Write remaining subjects

def log_progress(subject_id, hours_studied):
    # This function can be expanded to log progress in a separate CSV file if needed
    pass
