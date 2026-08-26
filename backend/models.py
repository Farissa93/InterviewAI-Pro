from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

try:
    from .database import Base
except ImportError:  # support script execution
    from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Bcrypt hash, never the plain password. See auth.hash_password / verify_password.
    password_hash = Column(String(255), nullable=False)

    sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")

class InterviewQuestion(Base):
    #stores interview questions
    __tablename__ = "interview_questions"
    id = Column(Integer, primary_key=True, index=True)
    topic=Column(String(100), index=True) #e.g., arrays, strings, dynamic programming
    difficulty = Column(String(20))#easy, medium, hard
    question_text = Column(Text, nullable=False)
    model_answer = Column(Text)  # Ideal answer or explanation
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship("InterviewSession", back_populates="question")

class InterviewSession(Base):
    #stores user interview practice sessions
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic=Column(String(100))
    difficulty = Column(String(20))
    question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=True, index=True)
    user_answer=Column(Text)  # User's combined answers
    ai_evaluation=Column(Text)  # AI's feedback on user's answers
    score = Column(Float)  # Score out of 10
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")
    question = relationship("InterviewQuestion", back_populates="sessions")
    feedback = relationship("Feedback", back_populates="session", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False, index=True)
    score = Column(Float)  # e.g., rating out of 10
    feedback_type=Column(String(50))  # e.g., strength, weakness, suggestion
    feedback_text = Column(Text)  # Optional user comments
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="feedback")
    session = relationship("InterviewSession", back_populates="feedback")