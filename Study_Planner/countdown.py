import datetime

def exam_countdown(exam_date):
    today = datetime.date.today()
    delta = exam_date - today
    return delta.days 