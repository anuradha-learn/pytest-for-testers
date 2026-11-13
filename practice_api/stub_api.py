"""NexaDesk Lite: the practice API for the pytest for Testers course.

NexaDesk is the internal IT and HR service desk for Nexa Group employees.
This small version runs on your own computer and keeps its data in memory.

What it offers:
- Tickets: list, get, create and delete service desk tickets
- Assistant: a fake AI that answers common employee questions.
  It gives the same facts in different words each time, like a real AI.
- Reset: puts the starting tickets back, so every test can start fresh

No AI model and no API key are used.

Start it from the project folder:
    uvicorn practice_api.stub_api:app --reload

Then open:
    http://127.0.0.1:8000/app    the NexaDesk web page
    http://127.0.0.1:8000/docs   the API docs, to explore every endpoint
"""

import copy
import random
from pathlib import Path
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="NexaDesk Lite",
    description="Practice API: Nexa Group IT and HR service desk. See REQUIREMENTS.md for the rules.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Business rules
# ---------------------------------------------------------------------------

RESPONSE_TIME_HOURS = {
    "P1": 4,   # urgent: 4 hours
    "P2": 24,  # high: 1 day
    "P3": 72,  # normal: 3 days
}

TITLE_MIN_LENGTH = 5
TITLE_MAX_LENGTH = 100

# ---------------------------------------------------------------------------
# Starting data
# ---------------------------------------------------------------------------

SEED_TICKETS = [
    {"id": 1, "title": "Cannot connect to VPN", "category": "IT", "priority": "P1"},
    {"id": 2, "title": "Laptop battery drains quickly", "category": "IT", "priority": "P3"},
    {"id": 3, "title": "Update my bank details for salary", "category": "HR", "priority": "P2"},
    {"id": 4, "title": "Request for a second monitor", "category": "IT", "priority": "P3"},
    {"id": 5, "title": "Question about leave balance", "category": "HR", "priority": "P3"},
]

tickets: list[dict] = []
next_id = 1


def _load_seed_data() -> None:
    """Put the starting tickets back and restart ids after the last one."""
    global tickets, next_id
    tickets = []
    for seed in copy.deepcopy(SEED_TICKETS):
        seed["status"] = "open"
        seed["response_time_hours"] = RESPONSE_TIME_HOURS[seed["priority"]]
        tickets.append(seed)
    next_id = len(SEED_TICKETS) + 1


_load_seed_data()

# ---------------------------------------------------------------------------
# Request and response shapes
# ---------------------------------------------------------------------------


class TicketIn(BaseModel):
    title: str
    category: Literal["IT", "HR"]
    priority: Literal["P1", "P2", "P3"] = "P3"

    @field_validator("title")
    @classmethod
    def check_title_length(cls, title: str) -> str:
        title = title.strip()
        if not (TITLE_MIN_LENGTH <= len(title) < TITLE_MAX_LENGTH):
            raise ValueError(
                f"title must be {TITLE_MIN_LENGTH} to {TITLE_MAX_LENGTH} characters"
            )
        return title


class Ticket(BaseModel):
    id: int
    title: str
    category: str
    priority: str
    status: str
    response_time_hours: int


class Question(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def check_not_empty(cls, question: str) -> str:
        if not question.strip():
            raise ValueError("question must not be empty")
        return question


class Answer(BaseModel):
    topic: str
    answer: str


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@app.get("/")
def health():
    """Check that NexaDesk Lite is running."""
    return {"name": "NexaDesk Lite", "status": "ok"}


@app.get("/app", include_in_schema=False)
def web_page():
    """The NexaDesk web page. It calls the same API your tests use."""
    return FileResponse(Path(__file__).parent / "nexadesk.html")


# ---------------------------------------------------------------------------
# Tickets
# ---------------------------------------------------------------------------


@app.get("/tickets", response_model=list[Ticket])
def list_tickets(category: Optional[str] = None, priority: Optional[str] = None):
    """List tickets. Optional filters: ?category=IT or HR, ?priority=P1, P2 or P3."""
    result = tickets
    if category:
        result = [t for t in result if t["category"] == category]
    if priority:
        result = [t for t in result if t["priority"] == priority]
    return result


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    """Get one ticket. Returns 404 if it does not exist."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")


@app.post("/tickets", response_model=Ticket, status_code=201)
def create_ticket(ticket_in: TicketIn):
    """Create a ticket. Returns 201, or 422 if the data breaks a rule."""
    global next_id
    ticket = {
        "id": next_id,
        "title": ticket_in.title,
        "category": ticket_in.category,
        "priority": ticket_in.priority,
        "status": "open",
        "response_time_hours": RESPONSE_TIME_HOURS[ticket_in.priority],
    }
    tickets.append(ticket)
    next_id += 1
    return ticket


@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    """Delete a ticket. Returns 204, or 404 if it does not exist."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            tickets.remove(ticket)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Ticket not found")


@app.post("/reset")
def reset():
    """Put the starting tickets back. Use this before each test."""
    _load_seed_data()
    return {"status": "reset", "tickets": len(tickets)}


# ---------------------------------------------------------------------------
# Assistant (fake AI)
# ---------------------------------------------------------------------------

# Each topic: the words that trigger it, and several ways to say the same facts.
ASSISTANT_TOPICS = {
    "password_reset": {
        "keywords": ["password", "reset", "locked", "log in", "login", "sign in"],
        "answers": [
            "You can reset your password yourself on the IT portal. The new password works within 15 minutes.",
            "Go to the IT portal and choose 'Forgot password'. Your new password is active within 15 minutes.",
            "Password resets are self-service: use the IT portal, and allow up to 15 minutes for the change.",
        ],
    },
    "annual_leave": {
        "keywords": ["leave", "holiday", "vacation", "time off", "day off"],
        "answers": [
            "Full-time employees get 30 days of annual leave per year. Book it in the HR portal.",
            "Your annual leave allowance is 30 days a year. Please request it through the HR portal.",
            "Each year you have 30 days of annual leave. Submit leave requests in the HR portal.",
        ],
    },
    "new_laptop": {
        "keywords": ["laptop", "computer", "new device", "hardware"],
        "answers": [
            "To get a new laptop, raise an IT ticket. Laptops are delivered within 5 working days.",
            "Please raise an IT ticket for a new laptop. Delivery takes up to 5 working days.",
            "New laptops are requested with an IT ticket and usually arrive within 5 working days.",
        ],
    },
    "response_times": {
        "keywords": ["urgent", "priority", "how fast", "how long", "response time"],
        "answers": [
            "Response times depend on priority: P1 within 4 hours, P2 within 1 day, P3 within 3 days.",
            "We respond to P1 tickets within 4 hours, P2 tickets within 1 day and P3 tickets within 3 days.",
            "For urgent P1 tickets expect a reply within 4 hours. P2 takes up to 1 day and P3 up to 3 days.",
        ],
    },
}

FALLBACK_ANSWERS = [
    "I'm not sure about that one. Please raise a ticket and the service desk team will help.",
    "I don't have an answer for that yet. Please raise a ticket so a colleague can help you.",
    "That's outside what I can answer. Please raise a ticket with IT or HR.",
]


@app.post("/assistant/ask", response_model=Answer)
def ask_assistant(question: Question):
    """Ask the NexaDesk assistant a question. The wording changes each time."""
    text = question.question.lower()
    for topic, details in ASSISTANT_TOPICS.items():
        if any(keyword in text for keyword in details["keywords"]):
            return {"topic": topic, "answer": random.choice(details["answers"])}
    return {"topic": "unknown", "answer": random.choice(FALLBACK_ANSWERS)}