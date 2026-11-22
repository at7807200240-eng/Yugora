from pydantic import BaseModel
from typing import List, Dict

class StudentState(BaseModel):
    student_id: str
    current_task: str = "Write a function to extract titles from URLs."
    tasks_completed: int = 0
    skill_genome_score: int = 0
    chat_history: List[Dict[str, str]] = []

fake_database = {}

def get_student_state(student_id: str) -> StudentState:
    if student_id not in fake_database:
        fake_database[student_id] = StudentState(student_id=student_id)
    return fake_database[student_id]

def update_genome_score(student_id: str, points: int):
    state = get_student_state(student_id)
    state.skill_genome_score += points
    return state.skill_genome_score