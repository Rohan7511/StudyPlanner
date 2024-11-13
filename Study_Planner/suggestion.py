def suggest_tasks(tasks):
    # Simple suggestion based on priority
    return sorted(tasks, key=lambda x: x.priority) 