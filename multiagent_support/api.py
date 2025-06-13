from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from .models import Ticket
from .classifier import classify_ticket
from .agents import get_agent
from .sentiment import analyze_sentiment
from .translate import detect, translate_text
from .proactive import suggest_next_action
from .voice import speech_to_text, text_to_speech
import shutil
import os

app = FastAPI(title="Multi-Agent Support System API")

class TicketRequest(BaseModel):
    body: str
    language: str = "auto"
    want_voice: bool = False

class TicketResponse(BaseModel):
    id: int
    body: str
    category: str
    status: str
    response: str
    agent: str
    sentiment: str
    language: str
    suggestion: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/ticket", response_model=TicketResponse)
def create_ticket(req: TicketRequest, db: Session = Depends(get_db)):
    lang = detect(req.body) if req.language == "auto" else req.language
    body_en = translate_text(req.body, src_lang=lang, tgt_lang="en") if lang != "en" else req.body

    category = classify_ticket(body_en)
    sentiment = analyze_sentiment(body_en)
    suggestion = suggest_next_action(body_en)
    agent = get_agent(category)
    agent_response_en = agent.respond(body_en)
    agent_response = translate_text(agent_response_en, src_lang="en", tgt_lang=lang) if lang != "en" else agent_response_en

    status = "resolved" if category != "escalation" else "escalated"
    ticket = Ticket(
        body=req.body,
        category=category,
        status=status,
        response=agent_response,
        agent=agent.name,
        sentiment=sentiment,
        language=lang,
        suggestion=suggestion
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    if req.want_voice:
        filename = f"ticket_{ticket.id}_response.mp3"
        text_to_speech(agent_response, lang=lang, filename=filename, play_audio=False)

    return TicketResponse(
        id=ticket.id,
        body=ticket.body,
        category=ticket.category,
        status=ticket.status,
        response=ticket.response,
        agent=ticket.agent,
        sentiment=ticket.sentiment,
        language=ticket.language,
        suggestion=ticket.suggestion
    )

@app.get("/ticket/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse(
        id=ticket.id,
        body=ticket.body,
        category=ticket.category,
        status=ticket.status,
        response=ticket.response,
        agent=ticket.agent,
        sentiment=ticket.sentiment,
        language=ticket.language,
        suggestion=ticket.suggestion
    )

@app.post("/ticket/audio", response_model=TicketResponse)
async def create_ticket_from_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_filename = "temp_audio.wav"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        text = speech_to_text(temp_filename)
    finally:
        os.remove(temp_filename)
    req = TicketRequest(body=text, language="auto", want_voice=False)
    return create_ticket(req, db)