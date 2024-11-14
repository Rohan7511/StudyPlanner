import tkinter as tk
from tkinter import messagebox, simpledialog, Frame, Label
from db_handler import add_subject, get_subjects, delete_subject
from task_manager import add_task, get_tasks, Task
from timer import PomodoroTimer
from notes_manager import NotesManager
from countdown import exam_countdown
from tkcalendar import Calendar
import datetime
import threading
import os
import subprocess
from ttkthemes import ThemedStyle

class StudyPlannerApp:
    def __init__(self, root, notes_manager):
        self.root = root
        self.root.title("Personalized Study Planner")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        # Load background image
        self.bg_image = tk.PhotoImage(file=r"C:\Users\arobl\PycharmProjects\Study_Planner\bg.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.notes_manager = notes_manager

        # Create a base directory for study resources
        self.base_dir = "study_resources"
        os.makedirs(self.base_dir, exist_ok=True)

        # Initialize Pomodoro Timer
        self.pomodoro_timer = PomodoroTimer(root, self.update_timer_display)

        self.create_widgets()
        
    def create_widgets(self):
        # Navigation frame
        nav_frame = Frame(self.root, width=200, bg='darkgrey')
        nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Display frame for dynamic content
        self.display_frame = Frame(self.root, bg='black')
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Navigation buttons
        tk.Button(nav_frame, text="Add Subject", command=lambda: self.show_frame("add_subject")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="Add Task", command=lambda: self.show_frame("add_task")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="Start Pomodoro Timer", command=lambda: self.show_frame("start_timer")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="Delete Subject", command=lambda: self.show_frame("delete_subject")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="Exam Countdown", command=lambda: self.show_frame("exam_countdown")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="View Tasks", command=lambda: self.show_frame("view_tasks")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="View Subjects", command=lambda: self.show_frame("view_subjects")).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(nav_frame, text="Exit", command=self.root.quit).pack(fill=tk.X, padx=5, pady=5)

        # Frames for different functionalities
        self.frames = {
            "add_subject": self.create_add_subject_frame(),
            "add_task": self.create_add_task_frame(),
            "start_timer": self.create_start_timer_frame(),
            "delete_subject": self.create_delete_subject_frame(),
            "exam_countdown": self.create_exam_countdown_frame(),
            "view_tasks": self.create_view_tasks_frame(),
            "view_subjects": self.create_view_subjects_frame(),
        }

        self.show_frame("add_subject")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
            
        if frame_name not in self.frames:
            if frame_name == "view_subjects":
                self.frames[frame_name] = self.create_view_subjects_frame()
    
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)

    def create_add_subject_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="Add Subject", bg='black', fg='darkgrey').pack(pady=10)
        tk.Label(frame, text="Subject Name:", bg='black', fg='darkgrey').pack(pady=5)
        self.subject_name_entry = tk.Entry(frame)
        self.subject_name_entry.pack(pady=5)
        tk.Label(frame, text="Hours per Week:", bg='black', fg='darkgrey').pack(pady=5)
        self.hours_per_week_entry = tk.Entry(frame)
        self.hours_per_week_entry.pack(pady=5)
        tk.Label(frame, text="Difficulty (Easy, Medium, Hard):", bg='black', fg='darkgrey').pack(pady=5)
        self.difficulty_entry = tk.Entry(frame)
        self.difficulty_entry.pack(pady=5)
        tk.Button(frame, text="Add Subject", command=self.add_subject).pack(pady=5)
        return frame

    def create_add_task_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="Add Task", bg='black', fg='darkgrey').pack(pady=10)
        tk.Label(frame, text="Task Name:", bg='black', fg='darkgrey').pack(pady=5)
        self.task_name_entry = tk.Entry(frame)
        self.task_name_entry.pack(pady=5)
        tk.Label(frame, text="Due Date:", bg='black', fg='darkgrey').pack(pady=5)
        self.task_due_date_entry = Calendar(frame, selectmode='day')
        self.task_due_date_entry.pack(pady=5)
        tk.Label(frame, text="Priority (High, Medium, Low):", bg='black', fg='darkgrey').pack(pady=5)
        self.task_priority_entry = tk.Entry(frame)
        self.task_priority_entry.pack(pady=5)
        tk.Label(frame, text="Subject:", bg='black', fg='darkgrey').pack(pady=5)
        self.task_subject_entry = tk.Entry(frame)
        self.task_subject_entry.pack(pady=5)
        tk.Button(frame, text="Add Task", command=self.add_task).pack(pady=5)
        return frame

    def create_start_timer_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="Start Pomodoro Timer", bg='black', fg='darkgrey').pack(pady=10)
        self.timer_label = Label(frame, text="00:00", font=("Helvetica", 24), bg='black', fg='darkgrey')
        self.timer_label.pack(pady=20)
        tk.Button(frame, text="Start Timer", command=self.pomodoro_timer.start_timer).pack(pady=5)
        tk.Button(frame, text="Stop Timer", command=self.stop_timer).pack(pady=5)
        return frame

    def create_delete_subject_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="Delete Subject", bg='black', fg='darkgrey').pack(pady=10)
        tk.Button(frame, text="Delete Subject", command=self.delete_subject).pack(pady=5)
        return frame

    def create_exam_countdown_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="Exam Countdown", bg='black', fg='darkgrey').pack(pady=10)
        tk.Button(frame, text="Check Countdown", command=self.exam_countdown).pack(pady=5)
        return frame

    def create_view_tasks_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="View Tasks", bg='black', fg='darkgrey').pack(pady=10)
        
        tasks = get_tasks()
        if tasks:
            for task in tasks:
                task_label = tk.Label(frame, text=f"Task: {task.name}, Due: {task.due_date}, Priority: {task.priority}", bg='black', fg='darkgrey')
                task_label.pack(pady=5)
        else:
            tk.Label(frame, text="No tasks found.", bg='black', fg='darkgrey').pack(pady=5)

        return frame

    def create_view_subjects_frame(self):
        frame = Frame(self.display_frame, bg='black')
        tk.Label(frame, text="View Subjects", bg='black', fg='darkgrey').pack(pady=10)

        for widget in frame.winfo_children():
            widget.destroy()

        subjects = get_subjects()
        print("Subjects retrieved:", subjects)
        if subjects:
            for subject in subjects:
                subject_label = tk.Label(frame, text=f"Subject: {subject[1]}, Hours/Week: {subject[2]}, Difficulty: {subject[3]}", bg='black', fg='darkgrey')
                subject_label.pack(pady=5)
                tk.Button(frame, text="View Notes", command=lambda s=subject[1]: self.open_notes_folder(s)).pack(pady=5)
        else:
            tk.Label(frame, text="No subjects found.", bg='black', fg='darkgrey').pack(pady=5)

        return frame

    
    def open_notes_folder(self, subject_name):
        notes_folder_path = os.path.join(self.base_dir, subject_name)

        if os.path.exists(notes_folder_path):
            if os.name == 'nt':
                os.startfile(notes_folder_path)
            elif os.name == 'posix':
                subprocess.call(['open', notes_folder_path])
        else:
            messagebox.showwarning("Folder Not Found", f"No notes folder found for {subject_name}.")

    def add_subject(self):
        subject_name = self.subject_name_entry.get()
        hours_per_week = self.hours_per_week_entry.get()
        difficulty = self.difficulty_entry.get()
    
        if subject_name and hours_per_week and difficulty:
            add_subject(subject_name, int(hours_per_week), difficulty)
        
            subject_folder = os.path.join(self.base_dir, subject_name)
            os.makedirs(subject_folder, exist_ok=True)
        
            messagebox.showinfo("Success", f"Added {subject_name} successfully!")
        
            self.frames["view_subjects"] = self.create_view_subjects_frame()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def add_task(self):
        task_name = self.task_name_entry.get()
        due_date = self.task_due_date_entry.get_date()
        priority = self.task_priority_entry.get()
        subject = self.task_subject_entry.get()
    
        if task_name and priority and subject:
            task = Task(task_name, due_date, priority, subject)
            add_task(task)
            messagebox.showinfo("Success", f"Added task: {task_name}")
        
            self.frames["view_tasks"] = self.create_view_tasks_frame()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.remaining_time = 10
            self.update_timer_display(self.remaining_time)
            self.run_timer()

    def run_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_display(self.remaining_time)
            self.root.after(1000, self.run_timer)
        else:
            self.timer_running = False
            self.timer_label.config(text="Break over! Back to work!")

    def stop_timer(self):
        self.pomodoro_timer.stop_timer()
        self.timer_label.config(text="00:00")
                
    def update_timer_display(self, remaining):
        minutes, seconds = divmod(remaining, 60)
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

    def delete_subject(self):
        subjects = get_subjects()
        subject_names = [subject[1] for subject in subjects]
    
        subject_name = simpledialog.askstring("Input", "Select subject to delete:", initialvalue=subject_names[0])
    
        subject_id = next((subject[0] for subject in subjects if subject[1] == subject_name), None)
    
        if subject_id:
            delete_subject(subject_id)
            messagebox.showinfo("Success", f"Deleted {subject_name} successfully.")
        
            self.frames["view_subjects"] = self.create_view_subjects_frame()
        else:
            messagebox.showwarning("Error", "Subject not found.")


    def exam_countdown(self):
        exam_date_str = simpledialog.askstring("Input", "Enter exam date (YYYY-MM-DD):")
        exam_date = datetime.datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        days_left = exam_countdown(exam_date)
        messagebox.showinfo("Countdown", f"Days until exam: {days_left}")
        


if __name__ == "__main__":
    root = tk.Tk()
    style = ThemedStyle(root)
    style.set_theme("black")
    notes_manager = NotesManager()
    app = StudyPlannerApp(root, notes_manager)
    root.mainloop()
