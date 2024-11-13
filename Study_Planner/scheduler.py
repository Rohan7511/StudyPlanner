import csv
import random


def generate_schedule(subjects):
    # Create a weekly schedule dictionary with each day initialized as an empty list
    weekly_schedule = {day: [] for day in
                       ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    # Define weights for difficulty levels
    difficulty_weights = {'easy': 1, 'medium': 1.5, 'hard': 2}

    # Calculate and distribute hours across the week
    for subject in subjects:
        name, hours_per_week, difficulty = subject[1], int(subject[2]), subject[3].lower()  # Extract data
        weight = difficulty_weights.get(difficulty, 1)

        # Adjusted total hours based on difficulty
        adjusted_hours = hours_per_week * weight

        # Calculate hours per day and assign them to random days, capping at 7 days
        days_needed = min(7, max(1, int(adjusted_hours // 1.5)))  # Max of 7 days to avoid the error
        days = random.sample(list(weekly_schedule.keys()), days_needed)

        hours_per_day = adjusted_hours / days_needed
        for day in days:
            weekly_schedule[day].append((name, hours_per_day))

    schedule_output = []
    for day, tasks in weekly_schedule.items():
        if tasks:
            schedule_output.append(f"{day}:")
            for task in tasks:
                subject_name, hours = task
                schedule_output.append(f"  - {subject_name}: {hours:.2f} hours")
            schedule_output.append("")  # Add a blank line for spacing

    return schedule_output  # Return the schedule as a list of strings



