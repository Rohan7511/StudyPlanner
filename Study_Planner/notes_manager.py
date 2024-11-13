class NotesManager:
    def __init__(self):
        self.notes = {}

    def add_note(self, subject, note):
        if subject not in self.notes:
            self.notes[subject] = []
        self.notes[subject].append(note)

    def get_notes(self, subject):
        return self.notes.get(subject, []) 