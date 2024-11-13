class HabitTracker:
    def __init__(self):
        self.habits = {}

    def add_habit(self, habit):
        self.habits[habit] = 0  # Initialize streak to 0

    def mark_habit(self, habit):
        if habit in self.habits:
            self.habits[habit] += 1  # Increment streak 