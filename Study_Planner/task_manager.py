import csv
import os
from datetime import datetime

CSV_FILE = 'data/tasks.csv'

def init_task_db():
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'due_date', 'priority', 'subject', 'completed'])

def add_task(task):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task.name, task.due_date.strftime('%Y-%m-%d'), task.priority, task.subject, task.completed])

def get_tasks():
    tasks = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                tasks.append(Task(row[0], row[1], row[2], row[3]))
    return tasks

def delete_task_from_csv(task_name):
    tasks = get_tasks()
    valid_tasks = [task for task in tasks if task.name != task_name]

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'due_date', 'priority', 'subject', 'completed'])  # Write header
        for task in valid_tasks:
            writer.writerow([task.name, task.due_date.strftime('%Y-%m-%d'), task.priority, task.subject, task.completed])

class Task:
    def __init__(self, name, due_date, priority, subject):
        self.name = name
        self.due_date = self.parse_due_date(due_date) 
        self.priority = priority
        self.subject = subject
        self.completed = False

    def parse_due_date(self, due_date):
        formats = ['%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y']  
        for fmt in formats:
            try:
                return datetime.strptime(due_date, fmt).date()
            except ValueError:
                continue  
        raise ValueError(f"Date format for '{due_date}' is not recognized.")  

    def mark_completed(self):
        self.completed = True
