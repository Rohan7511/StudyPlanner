import time
import threading

class Reminder:
    def __init__(self, message, delay):
        self.message = message
        self.delay = delay

    def start_reminder(self):
        threading.Thread(target=self._remind).start()

    def _remind(self):
        time.sleep(self.delay)
        print(f"Reminder: {self.message}") 