from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROGRAMS = {
    "computer science": {
        "name": "B.Tech Computer Science",
        "eligibility": "12th with PCM, minimum 60%",
        "documents": [
            "10th Marksheet",
            "12th Marksheet",
            "Entrance Exam Score",
            "ID Proof",
            "Photos"
        ],
        "deadline": "30 June"
    },
    "mba": {
        "name": "MBA",
        "eligibility": "Bachelor's degree with minimum 50%",
        "documents": [
            "Graduation Marksheet",
            "CAT/MAT Score",
            "Statement of Purpose",
            "Resume"
        ],
        "deadline": "15 July"
    }
}

UNIVERSITIES = [
    {
        "name": "Tech University",
        "min_percentage": 60,
        "programs": ["Computer Science", "IT", "AI"],
        "deadline": "30 June 2026",
        "mode": "Online Application"
    },
    {
        "name": "Global Business School",
        "min_percentage": 55,
        "programs": ["MBA", "BBA"],
        "deadline": "15 July 2026",
        "mode": "Entrance + Interview"
    },
    {
        "name": "National Engineering College",
        "min_percentage": 65,
        "programs": ["Mechanical", "Civil", "Computer Science"],
        "deadline": "10 June 2026",
        "mode": "Entrance Exam"
    }
]
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()

    if "program" in msg:
        return {
            "type": "program_list",
            "programs": list(PROGRAMS.keys())
        }

    if "university" in msg or "universities" in msg:
        return {
            "type": "universities",
            "data": UNIVERSITIES
        }

    if "eligibility" in msg:
        return {
            "type": "eligibility_form"
        }

    for key, program in PROGRAMS.items():
        if key in msg:
            return {
                "type": "program",
                "data": program
            }

    return {
        "type": "text",
        "message": "Try asking about programs, universities, or eligibility."
    }


from typing import List

class EligibilityRequest(BaseModel):
    percentage: int

@app.post("/eligibility-check")
def eligibility_check(req: EligibilityRequest):
    eligible = []
    not_eligible = []

    for uni in UNIVERSITIES:
        if req.percentage >= uni["min_percentage"]:
            eligible.append(uni)
        else:
            not_eligible.append(uni)

    return {
        "eligible": eligible,
        "not_eligible": not_eligible
    }

