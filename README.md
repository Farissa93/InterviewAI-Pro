# 🎯 Interview Prep AI

An AI-powered interview preparation platform that helps you practice technical interviews with intelligent question generation and detailed feedback.

## ✨ Features

- **AI-Generated Questions**: Get customized interview questions on any technical topic
- **Instant Evaluation**: Receive detailed AI-powered feedback on your answers
- **Score & Analytics**: Track your performance with scores and improvement suggestions
- **Session History**: Review all your past practice sessions
- **User Authentication**: Secure login and signup system
- **Beautiful UI**: Clean, modern Streamlit interface

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **LangChain**: Framework for LLM applications
- **OpenAI GPT-3.5**: AI model for question generation and evaluation
- **ChromaDB**: Vector database for RAG (Retrieval Augmented Generation)

### Frontend
- **Streamlit**: Python-based web application framework
- **Requests**: HTTP library for API calls

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
cd "Interview prep chatbot"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate it:
- **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
- **Windows (CMD)**: `venv\Scripts\activate.bat`
- **macOS/Linux**: `source venv/bin/activate`

### 3. Install Dependencies

```bash
# Backend dependencies
pip install fastapi uvicorn sqlalchemy python-dotenv langchain langchain-openai langchain-chroma chromadb

# Streamlit dependencies
pip install streamlit requests
```

Or install from requirements files (if available):
```bash
pip install -r requirements.txt
pip install -r streamlit_requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./interview_prep.db
```

### 5. Start the Application

#### Option A: Use Startup Scripts (Recommended)

**PowerShell:**
```bash
.\start.ps1
```

**Command Prompt:**
```bash
start.bat
```

#### Option B: Manual Start

**Terminal 1 - Backend (run from the project root, not from `backend/`):**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
streamlit run streamlit_app.py
```

### 6. Access the Application

- **Streamlit UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage Guide

### Sign Up / Login
1. Open the Streamlit app at http://localhost:8501
2. Create a new account or login with existing credentials

### Practice Interviews
1. Click "Practice Interview" from the sidebar
2. Enter a topic (e.g., "Python", "Data Structures", "System Design")
3. Select difficulty level (easy, medium, hard)
4. Click "Generate Question"
5. Write your answer in the text area
6. Submit to get AI evaluation

### View Feedback
After submitting your answer, you'll receive:
- **Score**: Numerical rating out of 10
- **Strengths**: What you did well
- **Weaknesses**: Areas needing improvement
- **Suggestions**: Specific recommendations
- **Overall Feedback**: Comprehensive evaluation

### Review Sessions
1. Click "My Sessions" to view history
2. Filter by topic and difficulty
3. Review detailed feedback for each session
4. Track your progress over time

## 🗂️ Project Structure

```
Interview prep chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & endpoints
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai_service.py        # AI question generation & evaluation
│   └── rag_service.py       # RAG implementation
├── chroma_db/               # Vector database storage
├── streamlit_app.py         # Streamlit frontend
├── start.ps1                # PowerShell startup script
├── start.bat                # Batch startup script
├── streamlit_requirements.txt
└── README.md
```

## 🔌 API Endpoints

### Health & Root
- `GET /` - Root endpoint
- `GET /health` - Health check

### Users
- `POST /api/users` - Create user
- `GET /api/users` - List users
- `GET /api/users/{user_id}` - Get user by ID

### Questions
- `POST /api/questions` - Create question
- `GET /api/questions` - List questions (with filters)
- `GET /api/questions/{question_id}` - Get question by ID

### Sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions/{session_id}` - Get session
- `GET /api/users/{user_id}/sessions` - Get user's sessions
- `GET /api/sessions/{session_id}/feedback` - Get session feedback

### AI Features
- `POST /api/ai/generate-question` - Generate interview question
- `POST /api/ai/evaluate-answer` - Evaluate user's answer
- `POST /api/rag/seed` - Seed question bank with samples
- `POST /api/rag/generate-question` - Generate question using RAG

## 🔧 Configuration

### Backend API URL
If running the backend on a different host/port, update `streamlit_app.py`:
```python
API_BASE_URL = "http://localhost:8000"  # Change as needed
```

### Database
The application uses SQLite by default. To use a different database, update the `DATABASE_URL` in your `.env` file.

### AI Model
To use a different OpenAI model, modify `ai_service.py`:
```python
llm = ChatOpenAI(
    model="gpt-4",  # Change model here
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)
```

## 🐛 Troubleshooting

### Backend not starting
- Verify all dependencies are installed
- Check that port 8000 is not in use
- Ensure `.env` file exists with valid OpenAI API key

### Streamlit connection errors
- Confirm backend is running at http://localhost:8000
- Check API health endpoint: http://localhost:8000/health
- Verify no firewall blocking connections

### Database errors
- Delete the SQLite database file and restart to recreate tables
- Check database permissions

### AI generation errors
- Verify OpenAI API key is valid and has credits
- Check backend logs for detailed error messages
- Ensure internet connection is stable

## 🚧 Future Enhancements

- [ ] Timed interview mode
- [ ] Mock interview sessions with multiple questions
- [ ] Voice input/output for answers
- [ ] Progress tracking dashboard with charts
- [ ] Adaptive difficulty based on performance
- [ ] Multi-language support
- [ ] Export session reports as PDF
- [ ] Collaborative practice sessions
- [ ] Question difficulty auto-adjustment
- [ ] Integration with LeetCode/HackerRank

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for LLM framework
- Streamlit for the amazing UI framework
- FastAPI for the high-performance backend

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check backend logs for error details
4. Ensure all prerequisites are met

---

**Built with ❤️ for aspiring developers**

*Happy interviewing! 🎯*
