import os

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from . import models, schemas, auth
from .database import engine, get_db
from .ai_service import (
    generate_interview_question,
    evaluate_answer,
    generate_question_with_rag
)
from .rag_service import question_rag, seed_sample_questions

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Interview Prep AI",
    description="An AI-powered interview preparation platform.",
    version="1.0.0"
)

# Rate limiting (protects the OpenAI-backed endpoints and login from abuse)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS: restrict to known frontend origin(s), configurable via env var
_frontend_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:8501")
allowed_origins = [origin.strip() for origin in _frontend_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Root & Health Endpoints
# ============================================

@app.get("/")
def root():
    """Root endpoint - verify API is running"""
    return {
        "message": "Interview AI API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint, verifies DB connection"""
    try:
        # Simple query to check DB connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# ============================================
# Auth Endpoints
# ============================================

@app.post("/api/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Sign up a new user"""
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=auth.hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/api/auth/login", response_model=schemas.TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Verify username + password and issue a JWT access token"""
    user = db.query(models.User).filter(models.User.username == credentials.username).first()

    if not user or not auth.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = auth.create_access_token(user_id=user.id, username=user.username)
    return schemas.TokenResponse(access_token=token, user=user)

@app.get("/api/users/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    """Get the currently authenticated user"""
    return current_user

# ============================================
# Interview Question Endpoints
# ============================================

@app.post('/api/questions', response_model=schemas.QuestionResponse, status_code=201)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Create new interview question"""
    db_question = models.InterviewQuestion(**question.dict())

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question

@app.get('/api/questions', response_model=List[schemas.QuestionResponse])
def list_questions(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List questions with optional filters"""
    query = db.query(models.InterviewQuestion)

    if topic:
        query = query.filter(models.InterviewQuestion.topic == topic)
    if difficulty:
        query = query.filter(models.InterviewQuestion.difficulty == difficulty)

    questions = query.offset(skip).limit(limit).all()
    return questions

@app.get('/api/questions/{question_id}', response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get question by ID"""
    question = db.query(models.InterviewQuestion).filter(
        models.InterviewQuestion.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

# ============================================
# Interview Session Endpoints
# ============================================

@app.post('/api/sessions', response_model=schemas.SessionResponse, status_code=201)
def create_session(
    session: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Create new interview session for the authenticated user"""
    db_session = models.InterviewSession(
        user_id=current_user.id,
        topic=session.topic,
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session

@app.get('/api/sessions/{session_id}', response_model=schemas.SessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get session by ID (only the owner may view it)"""
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session")

    return session

@app.get('/api/users/{user_id}/sessions', response_model=List[schemas.SessionResponse])
def get_user_sessions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get all sessions for a specific user (only the user themselves)"""
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these sessions")

    sessions = db.query(models.InterviewSession).filter(
        models.InterviewSession.user_id == user_id
    ).all()

    return sessions

# ============================================
# AI-Powered Endpoints
# ============================================

@app.post("/api/ai/generate-question")
@limiter.limit("15/minute")
def ai_generate_question(
    request: Request,
    topic: str,
    difficulty: str = "medium",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Generate an interview question using AI

    Args:
        topic: Topic of the question (e.g., "Python", "JavaScript")
        difficulty: Difficulty level ("easy", "medium", "hard")
    """
    try:
        # Generate question using AI
        result = generate_interview_question(topic, difficulty)

        # Save to database
        db_question = models.InterviewQuestion(
            topic=result["topic"],
            difficulty=result["difficulty"],
            question_text=result["question_text"],
            model_answer=result["model_answer"],
        )

        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        return {
            "success": True,
            "question_id": db_question.id,
            "question": result["question_text"],
            "model_answer": result["model_answer"],
            "topic": topic,
            "difficulty": difficulty
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/evaluate-answer")
@limiter.limit("15/minute")
def ai_evaluate_answer(
    request: Request,
    question_id: int,
    user_answer: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Evaluate the authenticated user's answer using AI"""
    try:
        # Get question from database
        question = db.query(models.InterviewQuestion).filter(
            models.InterviewQuestion.id == question_id
        ).first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Evaluate using AI
        evaluation = evaluate_answer(question.question_text, user_answer)

        # Create session record
        session = models.InterviewSession(
            user_id=current_user.id,
            topic=question.topic,
            difficulty=question.difficulty,
            question_id=question_id,
            user_answer=user_answer,
            ai_evaluation=evaluation["feedback"],
            score=evaluation["score"],
            completed=True
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        # Save detailed feedback
        for strength in evaluation["strengths"]:
            feedback = models.Feedback(
                user_id=current_user.id,
                session_id=session.id,
                feedback_type="strength",
                feedback_text=strength
            )
            db.add(feedback)

        for weakness in evaluation["weaknesses"]:
            feedback = models.Feedback(
                user_id=current_user.id,
                session_id=session.id,
                feedback_type="weakness",
                feedback_text=weakness
            )
            db.add(feedback)

        for suggestion in evaluation["suggestions"]:
            feedback = models.Feedback(
                user_id=current_user.id,
                session_id=session.id,
                feedback_type="suggestion",
                feedback_text=suggestion
            )
            db.add(feedback)

        db.commit()

        return {
            "success": True,
            "session_id": session.id,
            "score": evaluation["score"],
            "feedback": evaluation["feedback"],
            "strengths": evaluation["strengths"],
            "weaknesses": evaluation["weaknesses"],
            "suggestions": evaluation["suggestions"],
            "model_answer": question.model_answer or ""
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/feedback")
def get_session_feedback(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get detailed feedback for a session (only the owner may view it)"""
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this feedback")

    feedback = db.query(models.Feedback).filter(
        models.Feedback.session_id == session_id
    ).all()

    # Organize by type
    strengths = [f.feedback_text for f in feedback if f.feedback_type == "strength"]
    weaknesses = [f.feedback_text for f in feedback if f.feedback_type == "weakness"]
    suggestions = [f.feedback_text for f in feedback if f.feedback_type == "suggestion"]

    return {
        "session_id": session_id,
        "score": session.score,
        "overall_feedback": session.ai_evaluation,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "question": session.question_id,
        "user_answer": session.user_answer
    }

# ============================================
# RAG Endpoints
# ============================================

@app.post("/api/rag/seed")
def seed_question_bank(current_user: models.User = Depends(auth.get_current_user)):
    """
    Seed vector store with sample questions
    (Run this once to populate question bank)
    """
    try:
        seed_sample_questions()
        count = question_rag.count_questions()
        return {
            "success": True,
            "message": "Question bank seeded successfully",
            "total_questions": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag/add-question")
def add_question_to_rag(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Add a question from database to RAG vector store"""
    question = db.query(models.InterviewQuestion).filter(
        models.InterviewQuestion.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Add to RAG
    question_rag.add_questions([{
        "id": question.id,
        "topic": question.topic,
        "difficulty": question.difficulty,
        "question_text": question.question_text,
        "model_answer": question.model_answer or ""
    }])

    return {
        "success": True,
        "message": f"Question {question_id} added to RAG",
        "question": question.question_text
    }

@app.get("/api/rag/search")
def search_question_bank(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 5
):
    """Search question bank using RAG"""
    results = question_rag.search_questions(
        query=query,
        topic=topic,
        difficulty=difficulty,
        k=limit
    )

    return {
        "success": True,
        "count": len(results),
        "questions": results
    }

@app.post("/api/ai/generate-question-rag")
@limiter.limit("15/minute")
def ai_generate_question_rag(
    request: Request,
    topic: str,
    difficulty: str = "medium",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Generate question using RAG (retrieves from question bank first)
    Falls back to AI generation if no match found
    """
    try:
        # Use RAG to find or generate question
        result = generate_question_with_rag(topic, difficulty)

        # If it was AI-generated (not from bank), save it
        if result.get("source") == "ai_generated":
            db_question = models.InterviewQuestion(
                topic=result["topic"],
                difficulty=result["difficulty"],
                question_text=result["question_text"],
                model_answer=result["model_answer"]
            )

            db.add(db_question)
            db.commit()
            db.refresh(db_question)

            # Add to RAG for future use
            question_rag.add_questions([{
                "id": db_question.id,
                "topic": db_question.topic,
                "difficulty": db_question.difficulty,
                "question_text": db_question.question_text,
                "model_answer": db_question.model_answer
            }])

            result["question_id"] = db_question.id

        return {
            "success": True,
            "question": result["question_text"],
            "model_answer": result["model_answer"],
            "topic": topic,
            "difficulty": difficulty,
            "source": result.get("source", "unknown")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rag/stats")
def get_rag_stats():
    """Get statistics about question bank"""
    count = question_rag.count_questions()
    return {
        "total_questions": count,
        "vectorstore_path": "./chroma_db"
    }

# ============================================
# Run the app
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
