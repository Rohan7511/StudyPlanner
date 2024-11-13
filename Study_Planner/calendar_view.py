import tkinter as tk
from tkcalendar import Calendar

class CalendarView:
    def __init__(self, root):
        self.root = root
        self.calendar = Calendar(root, selectmode='day')
        self.calendar.pack(pady=20)

    def get_selected_date(self):
        return self.calendar.get_date() 