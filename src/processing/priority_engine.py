def score_priority(task_details: dict) -> int:
    """
    Scores a task's priority based on keywords and the presence of a deadline.
    Higher score = higher priority.
    """
    score = 0
    task_text = task_details['task'].lower()
    
    # Keyword-based scoring
    high_priority_keywords = [
        "urgent", "asap", "immediate", "critical", "report", "finalize", "deadline"
    ]
    medium_priority_keywords = [
        "review", "feedback", "prepare", "submit", "task", "discuss"
    ]
    low_priority_keywords = ["reminder", "update", "notes", "sync", "lunch"]
    
    if any(keyword in task_text for keyword in high_priority_keywords):
        score += 10
    if any(keyword in task_text for keyword in medium_priority_keywords):
        score += 5
    if any(keyword in task_text for keyword in low_priority_keywords):
        score -= 2
        
    # Deadline-based scoring
    if task_details['deadlines']:
        score += 8
        
    return score