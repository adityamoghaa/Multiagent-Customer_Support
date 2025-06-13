from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    category = Column(String, default="unclassified")
    status = Column(String, default="open")
    response = Column(String, default="")
    agent = Column(String, default="")
    sentiment = Column(String, default="")
    language = Column(String, default="en")
    suggestion = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)