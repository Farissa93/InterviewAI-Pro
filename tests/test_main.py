"""
Core backend tests: signup/login, auth enforcement, session ownership,
and the AI endpoints (with the actual OpenAI calls mocked out).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend import models
from backend.database import get_db
from backend.main import app

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def fresh_database():
    models.Base.metadata.create_all(bind=test_engine)
    yield
    models.Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


def signup(client, username="alice", email="alice@example.com", password="hunter22"):
    return client.post(
        "/api/users",
        json={"username": username, "email": email, "password": password},
    )


def login(client, username="alice", password="hunter22"):
    return client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )


def auth_header(client, **kwargs):
    token = login(client, **kwargs).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_signup_hashes_password_not_stored_plaintext(client):
    response = signup(client)
    assert response.status_code == 201
    body = response.json()
    assert "password" not in body
    assert "password_hash" not in body

    db = TestingSessionLocal()
    user = db.query(models.User).filter(models.User.username == "alice").first()
    db.close()
    assert user.password_hash != "hunter22"
    assert user.password_hash.startswith("$2b$")  # bcrypt hash prefix


def test_signup_duplicate_username_rejected(client):
    signup(client)
    response = signup(client, email="different@example.com")
    assert response.status_code == 400


def test_login_success_returns_token(client):
    signup(client)
    response = login(client)
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["user"]["username"] == "alice"


def test_login_wrong_password_rejected(client):
    signup(client)
    response = login(client, password="wrong-password")
    assert response.status_code == 401


def test_login_nonexistent_user_rejected(client):
    response = login(client, username="ghost", password="whatever")
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/api/users/me")
    assert response.status_code == 401  # no bearer credentials supplied


def test_me_with_valid_token(client):
    signup(client)
    headers = auth_header(client)
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_me_with_garbage_token_rejected(client):
    response = client.get("/api/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_create_session_requires_auth(client):
    response = client.post("/api/sessions", json={"user_id": 1, "topic": "Python"})
    assert response.status_code == 401


def test_user_cannot_view_another_users_sessions(client):
    signup(client, username="alice", email="alice@example.com")
    signup(client, username="bob", email="bob@example.com")

    alice_headers = auth_header(client, username="alice")
    alice_id = client.get("/api/users/me", headers=alice_headers).json()["id"]

    bob_headers = auth_header(client, username="bob")

    response = client.get(f"/api/users/{alice_id}/sessions", headers=bob_headers)
    assert response.status_code == 403


def test_user_cannot_view_another_users_session_detail(client):
    signup(client, username="alice", email="alice@example.com")
    signup(client, username="bob", email="bob@example.com")

    alice_headers = auth_header(client, username="alice")
    session_resp = client.post(
        "/api/sessions", json={"user_id": 0, "topic": "Python"}, headers=alice_headers
    )
    assert session_resp.status_code == 201
    session_id = session_resp.json()["id"]

    bob_headers = auth_header(client, username="bob")
    response = client.get(f"/api/sessions/{session_id}", headers=bob_headers)
    assert response.status_code == 403


def test_generate_question_uses_ai_service_and_requires_auth(client, monkeypatch):
    def fake_generate(topic, difficulty):
        return {
            "question_text": f"What is {topic}?",
            "model_answer": "A fake answer.",
            "topic": topic,
            "difficulty": difficulty,
        }

    monkeypatch.setattr("backend.main.generate_interview_question", fake_generate)

    unauthenticated = client.post(
        "/api/ai/generate-question", params={"topic": "Python", "difficulty": "easy"}
    )
    assert unauthenticated.status_code == 401

    signup(client)
    headers = auth_header(client)
    response = client.post(
        "/api/ai/generate-question",
        params={"topic": "Python", "difficulty": "easy"},
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What is Python?"
    assert body["question_id"]


def test_evaluate_answer_creates_session_owned_by_caller(client, monkeypatch):
    def fake_evaluate(question, user_answer):
        return {
            "score": 8.5,
            "feedback": "Solid answer.",
            "strengths": ["Clear explanation"],
            "weaknesses": ["Missing an example"],
            "suggestions": ["Add a code sample"],
        }

    monkeypatch.setattr("backend.main.evaluate_answer", fake_evaluate)

    signup(client)
    headers = auth_header(client)

    db = TestingSessionLocal()
    question = models.InterviewQuestion(
        topic="Python", difficulty="easy", question_text="What is a list?", model_answer="..."
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    question_id = question.id
    db.close()

    response = client.post(
        "/api/ai/evaluate-answer",
        params={"question_id": question_id, "user_answer": "It's an ordered collection."},
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 8.5
    assert body["strengths"] == ["Clear explanation"]

    db = TestingSessionLocal()
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == body["session_id"]
    ).first()
    me = client.get("/api/users/me", headers=headers).json()
    assert session.user_id == me["id"]
    db.close()
