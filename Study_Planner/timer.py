import tkinter as tk
from tkinter import messagebox

class PomodoroTimer:
    def __init__(self, root, update_callback):
        self.root = root
        self.update_callback = update_callback
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60  # 5 minutes in seconds
        self.timer_running = False
        self.is_break = False
        self.remaining_time = 0

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.is_break = False
            self.remaining_time = self.work_duration
            self._countdown()

    def _countdown(self):
        if self.timer_running:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.update_callback(minutes * 60 + seconds)

            if self.remaining_time > 0:
                self.remaining_time -= 1
                # Schedule the next countdown call after 1 second
                self.root.after(1000, self._countdown)
            else:
                # When countdown ends, toggle work/break state
                self.is_break = not self.is_break
                if self.is_break:
                    messagebox.showinfo("Break Time", "Take a 5-minute break!")
                    self.remaining_time = self.break_duration
                else:
                    messagebox.showinfo("Back to Work", "Break over! Start working.")
                    self.remaining_time = self.work_duration
                self._countdown()  # Start the next session countdown

    def stop_timer(self):
        self.timer_running = False
        # Reset the display to initial work or break duration
        self.update_callback(self.work_duration if not self.is_break else self.break_duration)
