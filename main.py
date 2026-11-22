from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agents.manager import ManagerAgent
from agents.reviewer import QAAgent
from core.state import get_student_state, update_genome_score

app = FastAPI(title="YUGORA Simulation Engine", description="API Backend")
manager = ManagerAgent()
qa_reviewer = QAAgent()


class ChatRequest(BaseModel):
    student_id: str
    user_message: str


class CodeSubmission(BaseModel):
    student_id: str
    code: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serves the frontend UI."""
    with open("index.html", "r", encoding="utf-8") as file:  # <-- Added encoding here
        return file.read()

@app.post("/chat/manager")
async def chat_with_manager(request: ChatRequest):
    try:
        student = get_student_state(request.student_id)
        response = manager.chat_with_developer(
            user_message=request.user_message,
            chat_history=student.chat_history
        )
        student.chat_history.append({"role": "user", "content": request.user_message})
        student.chat_history.append({"role": "manager", "content": response})

        return {"role": "manager", "message": response, "current_score": student.skill_genome_score}
    except Exception as e:
        print(f"!!! CRASH REPORT !!! -> {e}")  # Added debug line
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit_code")
async def submit_code(request: CodeSubmission):
    try:
        student = get_student_state(request.student_id)
        review_feedback = qa_reviewer.review_code(request.code)

        if review_feedback.strip().upper().startswith("PASS"):
            update_genome_score(request.student_id, 10)
            status = "Success"
        else:
            status = "Failed"

        return {
            "qa_status": status,
            "feedback": review_feedback,
            "new_genome_score": student.skill_genome_score
        }
    except Exception as e:
        print(f"!!! CRASH REPORT !!! -> {e}")  # Added debug line
        raise HTTPException(status_code=500, detail=str(e))