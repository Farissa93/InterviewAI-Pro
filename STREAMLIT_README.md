# Interview Prep AI - Streamlit Frontend

A beautiful, user-friendly Streamlit frontend for the Interview Prep AI chatbot.

## Features

✨ **User Authentication**
- Sign up with username, email, and password
- Easy login system with user selection

🎯 **AI-Powered Interview Practice**
- Generate interview questions on any topic
- Choose difficulty level (easy, medium, hard)
- Submit answers and get instant AI evaluation
- View model answers for reference

📊 **Detailed Feedback**
- Get scored out of 10
- Receive strengths, weaknesses, and suggestions
- Overall feedback from AI

📈 **Session History**
- View all past interview sessions
- Filter by topic and difficulty
- Track your progress over time
- Review detailed feedback for each session

## Prerequisites

1. Python 3.8 or higher
2. Backend API running on `http://localhost:8000` (FastAPI server)

## Installation

1. Install Streamlit dependencies:
```bash
pip install -r streamlit_requirements.txt
```

Or install manually:
```bash
pip install streamlit requests
```

## Running the App

### Step 1: Start the Backend API

First, make sure your FastAPI backend is running:

```bash
cd backend
uvicorn main:app --reload
```

The API should be accessible at `http://localhost:8000`

### Step 2: Start the Streamlit App

In a new terminal, from the project root directory:

```bash
streamlit run streamlit_app.py
```

The Streamlit app will automatically open in your browser at `http://localhost:8501`

## Usage Guide

### 1. Sign Up / Login
- On the home page, either sign up with a new account or login with an existing one
- For testing, you can create a dummy account

### 2. Practice Interviews
- Click "Practice Interview" from the sidebar or home page
- Enter a topic (e.g., "Python", "JavaScript", "Data Structures", "System Design")
- Select difficulty level
- Click "Generate Question"
- Write your answer in the text area
- Submit to get instant AI evaluation

### 3. View Results
- After submitting, you'll see:
  - Your score out of 10
  - Strengths in your answer
  - Areas to improve
  - Suggestions for better answers
  - Overall feedback

### 4. Review Sessions
- Click "My Sessions" to see all past interview sessions
- Filter by topic and difficulty
- Review detailed feedback for each session
- Track your progress over time

## Configuration

If your backend API is running on a different host/port, update the `API_BASE_URL` in `streamlit_app.py`:

```python
API_BASE_URL = "http://localhost:8000"  # Change this to your API URL
```

## Troubleshooting

### Connection Refused Error
- Make sure the backend API is running
- Verify the API is accessible at `http://localhost:8000`
- Check if the port 8000 is not blocked by firewall

### No Questions Generating
- Ensure your OpenAI API key is set in the backend `.env` file
- Check backend logs for errors
- Verify the AI service is properly configured

### Sessions Not Showing
- Make sure you're logged in with the correct user
- Complete at least one interview session
- Check that the database is properly configured

## Features Overview

### Home Dashboard
- Quick access to all features
- Recent sessions preview
- Clean, modern interface

### Practice Interview
- Dynamic question generation
- Real-time answer submission
- Instant AI evaluation
- Model answer viewing

### Session History
- Complete session tracking
- Detailed feedback review
- Performance statistics
- Filter and search capabilities

## Tips for Best Experience

1. **Be Specific with Topics**: Use specific topics like "Python Decorators" or "Binary Search Trees" for more targeted questions

2. **Write Detailed Answers**: The more comprehensive your answer, the better feedback you'll receive

3. **Review Feedback**: Take time to read through the strengths, weaknesses, and suggestions

4. **Practice Regularly**: Track your progress by reviewing your session history

5. **Try Different Difficulties**: Start with easy and progress to hard as you improve

## Technology Stack

- **Frontend**: Streamlit (Python)
- **HTTP Client**: Requests library
- **Backend**: FastAPI
- **AI**: OpenAI GPT-3.5 with LangChain

## Support

For issues or questions:
1. Check the backend logs
2. Verify all dependencies are installed
3. Ensure the database is properly set up
4. Check the API health endpoint: `http://localhost:8000/health`

## Future Enhancements

- [ ] Progress tracking dashboard
- [ ] Question difficulty adaptation
- [ ] Timed interview mode
- [ ] Mock interview sessions
- [ ] Peer comparison analytics
- [ ] Export session reports
- [ ] Voice answer input
- [ ] Multi-user collaboration

---

**Happy Practicing! 🎯**
