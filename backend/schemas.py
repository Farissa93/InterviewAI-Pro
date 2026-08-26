from pydantic import BaseModel

try:
    from pydantic import EmailStr
    import email_validator  # type: ignore
except ImportError:  # fallback when email-validator extra is missing
    EmailStr = str  # type: ignore
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Allows SQLAlchemy model -> Pydantic

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
##interview question schemas
class QuestionBase(BaseModel):
    model_config = {"protected_namespaces": ()}

    topic: str
    difficulty: str
    question_text: str
    model_answer: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
##interview session schemas
class SessionBase(BaseModel):
    user_id: int
    topic: str
    difficulty: Optional[str] = None

class SessionCreate(SessionBase):
    user_id:int

class SessionResponse(SessionBase):
    id: int
    user_id: int
    question_id: Optional[int]
    user_answer: Optional[str]
    ai_evaluation: Optional[str]
    score: Optional[float]
    created_at: datetime
    completed: bool

    class Config:
        from_attributes = True
#request/response schemas(API speciifc)

class InterviewStartRequest(BaseModel):
    #req to start an interview
    topic: str
    difficulty: str
class InterviewAnswerRequest(BaseModel):
    #user's answer
    session_id: int
    answer: str
class InterviewFeedbackRequest(BaseModel):
    #user feedback on session
    score: float  # 0-10
    feedback: str
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]



