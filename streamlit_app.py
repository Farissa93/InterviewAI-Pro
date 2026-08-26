import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="InterviewAI Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles - Force all text to be visible */
    *, *::before, *::after {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Don't override Streamlit's Material icon ligature font, or icons render as literal text */
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #13131f 50%, #0d1421 100%);
    }
    
    /* Force ALL text to be white/light by default */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #e2e8f0 !important;
    }
    
    /* Hide Streamlit branding, but keep the sidebar expand/collapse control usable */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stHeader"] {background: transparent;}
    .stDeployButton {display: none;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121c 0%, #1a1a2e 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }

    /* Keep the sidebar always open - it kept getting accidentally collapsed with no way back */
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 244px !important;
        max-width: 244px !important;
        margin-left: 0px !important;
        transform: none !important;
        visibility: visible !important;
    }
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(99, 102, 241, 0.15) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
    }

    /* Small round icon-only back button */
    .st-key-back_to_dashboard_container .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
        width: 2.25rem !important;
        height: 2.25rem !important;
        min-width: 2.25rem !important;
        padding: 0 !important;
        border-radius: 50% !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    .st-key-back_to_dashboard_container .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px rgba(168, 85, 247, 0.55) !important;
    }
    
    /* Main Header */
    .hero-header {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        margin-bottom: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a1a1aa !important;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(20, 20, 35, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.1);
        padding: 1.75rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.25);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.1);
    }
    
    .feature-card {
        background: linear-gradient(145deg, rgba(20, 20, 35, 0.95) 0%, rgba(30, 30, 50, 0.95) 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(99, 102, 241, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        color: #ffffff !important;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        color: #a1a1aa !important;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Question Box */
    .question-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .question-label {
        color: #c084fc !important;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    .question-text {
        color: #ffffff !important;
        font-size: 1.25rem;
        font-weight: 500;
        line-height: 1.7;
    }
    
    /* Score Display */
    .score-container {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 800;
        color: #4ade80 !important;
        white-space: nowrap;
    }
    
    .score-label {
        color: #a1a1aa !important;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Feedback Sections */
    .feedback-section {
        background: rgba(20, 20, 35, 0.6);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        height: 100%;
    }
    
    .feedback-header {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .strength-header { color: #4ade80 !important; }
    .weakness-header { color: #fbbf24 !important; }
    .suggestion-header { color: #818cf8 !important; }
    
    .feedback-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        color: #e2e8f0 !important;
        font-size: 0.9rem;
        border-left: 3px solid;
    }
    
    .strength-item { border-left-color: #4ade80; background: rgba(34, 197, 94, 0.05); }
    .weakness-item { border-left-color: #fbbf24; background: rgba(251, 191, 36, 0.05); }
    .suggestion-item { border-left-color: #818cf8; background: rgba(129, 140, 248, 0.05); }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(145deg, rgba(20, 20, 35, 0.95) 0%, rgba(30, 30, 50, 0.95) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(99, 102, 241, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stat-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #ffffff !important;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #a1a1aa !important;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* Auth Page */
    .auth-container {
        background: rgba(20, 20, 35, 0.8);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.1);
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }
    
    .auth-title {
        color: #ffffff !important;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Custom Buttons - Main */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button:disabled {
        background: rgba(99, 102, 241, 0.3) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(20, 20, 35, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #6b7280 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(20, 20, 35, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    [data-baseweb="select"] > div {
        background: rgba(20, 20, 35, 0.8) !important;
        border-color: rgba(99, 102, 241, 0.2) !important;
    }
    
    [data-baseweb="popover"] {
        background: #1a1a2e !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    [data-baseweb="menu"] {
        background: #1a1a2e !important;
    }
    
    [data-baseweb="menu"] li {
        color: #e2e8f0 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 35, 0.8) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 15, 25, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a1a1aa !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }
    
    /* Alerts - Make them visible */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    [data-baseweb="notification"] {
        background: rgba(20, 20, 35, 0.95) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border-left: 4px solid #4ade80 !important;
    }
    
    .stSuccess p {
        color: #4ade80 !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border-left: 4px solid #fbbf24 !important;
    }
    
    .stWarning p {
        color: #fbbf24 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #f87171 !important;
    }
    
    .stError p {
        color: #f87171 !important;
    }
    
    .stInfo {
        background: rgba(99, 102, 241, 0.1) !important;
        border-left: 4px solid #818cf8 !important;
    }
    
    .stInfo p {
        color: #a5b4fc !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(99, 102, 241, 0.15) !important;
        margin: 2rem 0 !important;
    }
    
    /* Sections */
    .section-header {
        color: #ffffff !important;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    }
    
    /* User Welcome */
    .user-welcome {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 1rem;
    }
    
    .user-name {
        color: #c084fc !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* Session Card */
    .session-card {
        background: rgba(20, 20, 35, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .session-card:hover {
        background: rgba(30, 30, 50, 0.8);
        border-color: rgba(99, 102, 241, 0.25);
        transform: translateX(4px);
    }
    
    /* Pill badges */
    .pill {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .pill-easy { background: rgba(34, 197, 94, 0.15); color: #4ade80 !important; border: 1px solid rgba(34, 197, 94, 0.3); }
    .pill-medium { background: rgba(251, 191, 36, 0.15); color: #fbbf24 !important; border: 1px solid rgba(251, 191, 36, 0.3); }
    .pill-hard { background: rgba(239, 68, 68, 0.15); color: #f87171 !important; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    /* Markdown text inside st.markdown */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #e2e8f0 !important;
    }
    
    /* Code blocks */
    code {
        background: rgba(99, 102, 241, 0.15) !important;
        color: #c084fc !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 4px !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 25, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }
    
    /* Link styling */
    a {
        color: #818cf8 !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: #a5b4fc !important;
        text-decoration: underline !important;
    }
    
    /* Table styling */
    table {
        background: rgba(20, 20, 35, 0.6) !important;
        border-radius: 8px !important;
    }
    
    th {
        background: rgba(99, 102, 241, 0.1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    td {
        color: #e2e8f0 !important;
        border-color: rgba(99, 102, 241, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'token' not in st.session_state:
    st.session_state.token = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'question_id' not in st.session_state:
    st.session_state.question_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Helper functions for API calls
def create_user(username, email, password):
    """Create a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/users",
            json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 201:
            return True, response.json()
        else:
            detail = response.json().get('detail', 'Unknown error')
            if isinstance(detail, list):
                # FastAPI/Pydantic validation errors
                messages = []
                for err in detail:
                    field = err.get('loc', [])[-1] if err.get('loc') else ''
                    if field == 'email':
                        messages.append("Please enter a valid email address (e.g. name@example.com).")
                    else:
                        messages.append(err.get('msg', 'Invalid input'))
                detail = " ".join(dict.fromkeys(messages))
            return False, detail
    except Exception as e:
        return False, str(e)

def auth_headers():
    """Bearer token header for authenticated requests"""
    return {"Authorization": f"Bearer {st.session_state.token}"}

def login_user(username, password):
    """Log in and store the JWT access token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('detail', 'Invalid username or password')
    except Exception as e:
        return False, str(e)

def generate_question(topic, difficulty):
    """Generate an interview question"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/ai/generate-question",
            params={"topic": topic, "difficulty": difficulty},
            headers=auth_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('detail', 'Failed to generate question')
    except Exception as e:
        return False, str(e)

def submit_answer(question_id, user_answer):
    """Submit answer for evaluation (evaluated as the logged-in user)"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/ai/evaluate-answer",
            params={
                "question_id": question_id,
                "user_answer": user_answer
            },
            headers=auth_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('detail', 'Failed to evaluate answer')
    except Exception as e:
        return False, str(e)

def get_user_sessions(user_id):
    """Get all sessions for the logged-in user"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/users/{user_id}/sessions",
            headers=auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_session_feedback(session_id):
    """Get detailed feedback for a session"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/sessions/{session_id}/feedback",
            headers=auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Sidebar navigation
def render_sidebar():
    with st.sidebar:
        if st.session_state.get('user_id') and st.session_state.get('page_history'):
            with st.container(key="back_to_dashboard_container"):
                if st.button("←", key="sidebar_back_to_dashboard"):
                    prev_page = st.session_state.page_history.pop()
                    st.session_state.page = prev_page
                    st.session_state.last_page = prev_page
                    st.rerun()

        # Logo and Brand
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <span style='font-size: 2.5rem;'>💼</span>
            <h1 style='font-size: 1.5rem; font-weight: 700; 
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin: 0.5rem 0 0 0;'>InterviewAI Pro</h1>
            <p style='color: #64748b; font-size: 0.8rem; margin-top: 0.25rem;'>
                Ace Your Next Interview
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 1rem 0;'>", unsafe_allow_html=True)
        
        if st.session_state.user_id:
            # User info card
            st.markdown(f"""
            <div class='user-welcome'>
                <span style='font-size: 0.8rem; color: #94a3b8;'>Welcome back</span><br>
                <span class='user-name'>👤 {st.session_state.username}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
            
            # Navigation buttons with icons
            if st.button("🏠  Dashboard", use_container_width=True, key="nav_home"):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("🎯  Practice Now", use_container_width=True, key="nav_practice"):
                st.session_state.page = 'practice'
                st.rerun()
            
            if st.button("📊  My Sessions", use_container_width=True, key="nav_sessions"):
                st.session_state.page = 'sessions'
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Bottom section
            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 2rem 0 1rem 0;'>", unsafe_allow_html=True)
            
            if st.button("🚪  Sign Out", use_container_width=True, key="nav_logout"):
                st.session_state.user_id = None
                st.session_state.username = None
                st.session_state.token = None
                st.session_state.page = 'home'
                st.rerun()
                
            # Footer
            st.markdown("""
            <div style='margin-top: 2rem;'>
                <p style='color: #475569; font-size: 0.7rem; text-align: center;'>
                    Powered by OpenAI GPT-3.5<br>
                    © 2024 InterviewAI Pro
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 2rem 1rem;'>
                <p style='color: #94a3b8; font-size: 0.9rem;'>
                    Sign in to start practicing<br>your interview skills
                </p>
            </div>
            """, unsafe_allow_html=True)

# Authentication page
def render_auth_page():
    # Show a one-time popup after a successful signup (persists across the rerun)
    if st.session_state.get('signup_success_username'):
        st.toast(f"Account created for {st.session_state.signup_success_username}! Please sign in.", icon="✅")
        st.balloons()
        del st.session_state['signup_success_username']

    # Hero Section
    st.markdown("""
    <div class='hero-header'>
        <div class='hero-title'>InterviewAI Pro</div>
        <div class='hero-subtitle'>
            Master your technical interviews with AI-powered practice sessions
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Row - single grid so all three cards stretch to equal height
    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; align-items: stretch;'>
        <div class='feature-card'>
            <span class='feature-icon'>🤖</span>
            <div class='feature-title'>AI-Generated Questions</div>
            <div class='feature-desc'>Get customized interview questions tailored to your chosen topic and difficulty level</div>
        </div>
        <div class='feature-card'>
            <span class='feature-icon'>⚡</span>
            <div class='feature-title'>Instant Feedback</div>
            <div class='feature-desc'>Receive detailed AI-powered evaluation with strengths, weaknesses, and suggestions</div>
        </div>
        <div class='feature-card'>
            <span class='feature-icon'>📈</span>
            <div class='feature-title'>Track Progress</div>
            <div class='feature-desc'>Monitor your improvement over time with comprehensive session history</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Auth Forms
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='auth-container'>
            <div class='auth-title'>🔐 Sign In</div>
        </div>
        """, unsafe_allow_html=True)
        
        login_username = st.text_input("Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Sign In", use_container_width=True, type="primary", key="login_btn"):
            if login_username and password:
                success, result = login_user(login_username, password)
                if success:
                    st.session_state.token = result['access_token']
                    st.session_state.user_id = result['user']['id']
                    st.session_state.username = result['user']['username']
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("⚠️ Please enter your username and password")
    
    with col2:
        st.markdown("""
        <div class='auth-container'>
            <div class='auth-title'>✨ Create Account</div>
        </div>
        """, unsafe_allow_html=True)
        
        new_username = st.text_input("Username", key="signup_user", placeholder="Choose a username")
        new_email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
        new_password = st.text_input("Password", type="password", key="signup_pass", placeholder="Create a strong password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🎉 Create Account", use_container_width=True, type="primary", key="signup_btn"):
            if new_username and new_email and new_password:
                success, result = create_user(new_username, new_email, new_password)
                if success:
                    st.session_state.signup_success_username = new_username
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
            else:
                st.warning("⚠️ Please fill in all fields")

# Home page
def render_home_page():
    # Welcome header
    st.markdown(f"""
    <div class='hero-header' style='padding: 2rem;'>
        <div style='font-size: 1rem; color: #94a3b8; margin-bottom: 0.5rem;'>Welcome back</div>
        <div style='font-size: 2rem; font-weight: 700; color: #ffffff;'>{st.session_state.username} 👋</div>
        <div style='font-size: 1rem; color: #94a3b8; margin-top: 0.5rem;'>Ready to ace your next interview?</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    sessions = get_user_sessions(st.session_state.user_id)
    completed_sessions = [s for s in sessions if s.get('completed', False)]
    avg_score = sum(s.get('score', 0) for s in completed_sessions) / len(completed_sessions) if completed_sessions else 0
    topics = list(set(s['topic'] for s in sessions)) if sessions else []
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value' style='color: #6366f1;'>{len(sessions)}</div>
            <div class='stat-label'>Total Sessions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value' style='color: #22c55e;'>{len(completed_sessions)}</div>
            <div class='stat-label'>Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value' style='color: #a855f7;'>{avg_score:.1f}</div>
            <div class='stat-label'>Avg Score /10</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value' style='color: #f59e0b;'>{len(topics)}</div>
            <div class='stat-label'>Topics</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Cards
    st.markdown("<div class='section-header'>🚀 Quick Actions</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(145deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%); border: 1px solid rgba(99, 102, 241, 0.2);'>
            <span class='feature-icon'>🎯</span>
            <div class='feature-title'>Start Practice</div>
            <div class='feature-desc'>Begin a new interview practice session with AI-generated questions</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Practice →", use_container_width=True, key="home_start_practice"):
            st.session_state.page = 'practice'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(145deg, rgba(168, 85, 247, 0.15) 0%, rgba(168, 85, 247, 0.05) 100%); border: 1px solid rgba(168, 85, 247, 0.2);'>
            <span class='feature-icon'>📊</span>
            <div class='feature-title'>View History</div>
            <div class='feature-desc'>Review your past sessions and track your improvement over time</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Sessions →", use_container_width=True, key="home_view_sessions"):
            st.session_state.page = 'sessions'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='background: linear-gradient(145deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%); border: 1px solid rgba(34, 197, 94, 0.2);'>
            <span class='feature-icon'>💡</span>
            <div class='feature-title'>Quick Tips</div>
            <div class='feature-desc'>Practice regularly, focus on weak areas, and review feedback carefully</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Coming Soon", use_container_width=True, disabled=True, key="home_tips")
    
    # Recent Sessions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📋 Recent Sessions</div>", unsafe_allow_html=True)
    
    if sessions:
        recent_sessions = sessions[-5:][::-1]
        for session in recent_sessions:
            difficulty = session.get('difficulty', 'medium')
            pill_class = f"pill-{difficulty}"
            score = session.get('score', 'N/A')
            score_color = '#22c55e' if isinstance(score, (int, float)) and score >= 7 else '#f59e0b' if isinstance(score, (int, float)) and score >= 5 else '#ef4444'
            
            st.markdown(f"""
            <div class='session-card' style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='color: #ffffff; font-weight: 600;'>{session['topic']}</span>
                    <span class='pill {pill_class}' style='margin-left: 0.75rem;'>{difficulty}</span>
                </div>
                <div style='text-align: right;'>
                    <span style='color: {score_color}; font-weight: 700; font-size: 1.25rem;'>{score}/10</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);'>
            <span style='font-size: 3rem;'>📝</span>
            <p style='color: #94a3b8; margin-top: 1rem;'>No sessions yet. Start practicing to see your history!</p>
        </div>
        """, unsafe_allow_html=True)

# Practice page
def render_practice_page():
    st.markdown("""
    <div class='hero-header' style='padding: 1.5rem 2rem;'>
        <div style='font-size: 1.75rem; font-weight: 700; color: #ffffff;'>🎯 Practice Interview</div>
        <div style='font-size: 1rem; color: #94a3b8; margin-top: 0.25rem;'>Generate questions and test your knowledge</div>
    </div>
    """, unsafe_allow_html=True)

    # Step 1: Generate Question
    if not st.session_state.current_question:
        st.markdown("<div class='section-header'>📝 Configure Your Question</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card'>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "🏷️ Topic",
                placeholder="e.g., Python, React, System Design, SQL...",
                help="Enter the technical topic you want to practice"
            )
        
        with col2:
            difficulty = st.selectbox(
                "📊 Difficulty Level",
                ["easy", "medium", "hard"],
                index=1,
                format_func=lambda x: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[x]
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ Generate Question", use_container_width=True, type="primary"):
                if topic:
                    with st.spinner("🤖 AI is crafting your question..."):
                        success, result = generate_question(topic, difficulty)
                        if success:
                            st.session_state.current_question = result['question']
                            st.session_state.question_id = result['question_id']
                            st.session_state.model_answer = result.get('model_answer', '')
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
                else:
                    st.warning("⚠️ Please enter a topic first")
        
        # Tips section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card' style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);'>
            <div style='font-size: 1rem; font-weight: 600; color: #a855f7; margin-bottom: 1rem;'>💡 Pro Tips</div>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                <div style='color: #94a3b8; font-size: 0.9rem;'>
                    <span style='color: #22c55e;'>✓</span> Be specific with your topic
                </div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>
                    <span style='color: #22c55e;'>✓</span> Start with medium difficulty
                </div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>
                    <span style='color: #22c55e;'>✓</span> Practice daily for best results
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Step 2: Display Question and Answer Input
    else:
        # Question Display
        st.markdown(f"""
        <div class='question-container'>
            <div class='question-label'>Interview Question</div>
            <div class='question-text'>{st.session_state.current_question}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer Input
        st.markdown("<div class='section-header'>✍️ Your Answer</div>", unsafe_allow_html=True)
        
        user_answer = st.text_area(
            "Write your response below",
            height=200,
            placeholder="Take your time to write a comprehensive answer. Consider structure, examples, and clarity...",
            help="Write a detailed answer. The AI will evaluate your response.",
            label_visibility="collapsed"
        )
        
        # Character count
        char_count = len(user_answer)
        st.markdown(f"""
        <div style='text-align: right; color: {"#22c55e" if char_count > 100 else "#f59e0b"}; font-size: 0.8rem;'>
            {char_count} characters
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Submit Answer", use_container_width=True, type="primary"):
                if user_answer.strip():
                    with st.spinner("🔍 AI is evaluating your answer..."):
                        success, result = submit_answer(
                            st.session_state.question_id,
                            user_answer
                        )
                        if success:
                            st.session_state.evaluation_result = result
                            st.session_state.current_question = None
                            st.session_state.question_id = None
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {result}")
                else:
                    st.warning("⚠️ Please write an answer before submitting")
        
        with col2:
            if st.button("🔄 New Question", use_container_width=True):
                st.session_state.current_question = None
                st.session_state.question_id = None
                st.rerun()
        
        with col3:
            with st.expander("View Model Answer", icon="💡", key=f"model_answer_expander_{st.session_state.question_id}"):
                if st.session_state.model_answer:
                    st.markdown(f"""
                    <div style='background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 8px; color: #e0e0e0;'>
                        {st.session_state.model_answer}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Model answer not available")
    
    # Step 3: Display Evaluation Results
    if 'evaluation_result' in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        result = st.session_state.evaluation_result
        
        # Score display
        score = result['score']
        score_color = '#22c55e' if score >= 7 else '#f59e0b' if score >= 5 else '#ef4444'
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown(f"""
            <div class='score-container' style='border-color: {score_color}40;'>
                <div style='color: #94a3b8; font-size: 1rem; margin-bottom: 0.5rem;'>Your Score</div>
                <div class='score-value' style='background: linear-gradient(135deg, {score_color} 0%, {score_color}cc 100%); -webkit-background-clip: text;'>{score}/10</div>
                <div style='color: #94a3b8; margin-top: 0.5rem; font-size: 0.9rem;'>
                    {'🌟 Excellent!' if score >= 8 else '👍 Good job!' if score >= 6 else '💪 Keep practicing!'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feedback sections
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='feedback-section'>
                <div class='feedback-header strength-header'>✅ Strengths</div>
            """, unsafe_allow_html=True)
            if result.get('strengths'):
                for strength in result['strengths']:
                    st.markdown(f"<div class='feedback-item strength-item'>{strength}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #64748b; font-size: 0.9rem;'>No specific strengths noted</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='feedback-section'>
                <div class='feedback-header weakness-header'>⚠️ Areas to Improve</div>
            """, unsafe_allow_html=True)
            if result.get('weaknesses'):
                for weakness in result['weaknesses']:
                    st.markdown(f"<div class='feedback-item weakness-item'>{weakness}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #64748b; font-size: 0.9rem;'>No major issues found</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='feedback-section'>
                <div class='feedback-header suggestion-header'>💡 Suggestions</div>
            """, unsafe_allow_html=True)
            if result.get('suggestions'):
                for suggestion in result['suggestions']:
                    st.markdown(f"<div class='feedback-item suggestion-item'>{suggestion}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #64748b; font-size: 0.9rem;'>No additional suggestions</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Overall feedback
        if result.get('feedback'):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size: 1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.75rem;'>📝 Overall Feedback</div>
                <div style='color: #94a3b8; line-height: 1.7;'>{result['feedback']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Correct / model answer, so the user can learn from mistakes
        model_answer = result.get('model_answer') or st.session_state.get('model_answer')
        if model_answer:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size: 1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.75rem;'>✅ Correct Answer</div>
                <div style='color: #94a3b8; line-height: 1.7;'>{model_answer}</div>
            </div>
            """, unsafe_allow_html=True)

        # Action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Practice Another Question", use_container_width=True, type="primary"):
                del st.session_state.evaluation_result
                st.rerun()
        with col2:
            if st.button("📊 View All Sessions", use_container_width=True):
                del st.session_state.evaluation_result
                st.session_state.page = 'sessions'
                st.rerun()

# Sessions page
def render_sessions_page():
    st.markdown("""
    <div class='hero-header' style='padding: 1.5rem 2rem;'>
        <div style='font-size: 1.75rem; font-weight: 700; color: #ffffff;'>📊 Session History</div>
        <div style='font-size: 1rem; color: #94a3b8; margin-top: 0.25rem;'>Track your progress and review past interviews</div>
    </div>
    """, unsafe_allow_html=True)

    sessions = get_user_sessions(st.session_state.user_id)
    
    if not sessions:
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; background: rgba(255,255,255,0.02); border-radius: 20px; border: 1px dashed rgba(255,255,255,0.1);'>
            <span style='font-size: 4rem;'>📝</span>
            <h3 style='color: #ffffff; margin-top: 1.5rem;'>No Sessions Yet</h3>
            <p style='color: #94a3b8; margin-top: 0.5rem;'>Start practicing to build your interview history</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎯 Start Your First Practice", use_container_width=True, type="primary"):
                st.session_state.page = 'practice'
                st.rerun()
        return
    
    # Statistics Cards
    completed_sessions = [s for s in sessions if s.get('completed', False)]
    avg_score = sum(s.get('score', 0) for s in completed_sessions) / len(completed_sessions) if completed_sessions else 0
    topics = list(set(s['topic'] for s in sessions))
    
    # Best and worst topics
    topic_scores = {}
    for s in completed_sessions:
        topic = s['topic']
        if topic not in topic_scores:
            topic_scores[topic] = []
        topic_scores[topic].append(s.get('score', 0))
    
    topic_avgs = {t: sum(scores)/len(scores) for t, scores in topic_scores.items()}
    best_topic = max(topic_avgs.items(), key=lambda x: x[1])[0] if topic_avgs else "N/A"
    
    st.markdown(f"""
    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; align-items: stretch;'>
        <div class='stat-card'>
            <div class='stat-value' style='color: #6366f1;'>{len(sessions)}</div>
            <div class='stat-label'>Total Sessions</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value' style='color: #22c55e;'>{avg_score:.1f}</div>
            <div class='stat-label'>Average Score</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value' style='color: #a855f7;'>{len(topics)}</div>
            <div class='stat-label'>Topics Covered</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value' style='color: #f59e0b; font-size: 1.2rem;'>{best_topic[:12]}...</div>
            <div class='stat-label'>Best Topic</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filters
    st.markdown("<div class='section-header'>🔍 Filter Sessions</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        filter_topics = ["All Topics"] + sorted(set(s['topic'] for s in sessions))
        selected_topic = st.selectbox("Topic", filter_topics, label_visibility="collapsed", key="sessions_filter_topic")

    with col2:
        filter_difficulties = ["All Difficulties", "🟢 Easy", "🟡 Medium", "🔴 Hard"]
        selected_difficulty = st.selectbox("Difficulty", filter_difficulties, label_visibility="collapsed", key="sessions_filter_difficulty")

    with col3:
        sort_order = st.selectbox("Sort", ["Newest", "Oldest", "Highest Score", "Lowest Score"], label_visibility="collapsed", key="sessions_filter_sort")
    
    # Filter and sort sessions
    filtered_sessions = sessions.copy()
    
    if selected_topic != "All Topics":
        filtered_sessions = [s for s in filtered_sessions if s['topic'] == selected_topic]
    
    if selected_difficulty != "All Difficulties":
        diff_map = {"🟢 Easy": "easy", "🟡 Medium": "medium", "🔴 Hard": "hard"}
        filtered_sessions = [s for s in filtered_sessions if s.get('difficulty') == diff_map.get(selected_difficulty)]
    
    # Sort
    if sort_order == "Newest":
        filtered_sessions = filtered_sessions[::-1]
    elif sort_order == "Oldest":
        pass  # Already in order
    elif sort_order == "Highest Score":
        filtered_sessions = sorted(filtered_sessions, key=lambda x: x.get('score', 0), reverse=True)
    elif sort_order == "Lowest Score":
        filtered_sessions = sorted(filtered_sessions, key=lambda x: x.get('score', 0))
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-header'>📋 Sessions ({len(filtered_sessions)})</div>", unsafe_allow_html=True)
    
    # Session cards
    for session in filtered_sessions:
        difficulty = session.get('difficulty', 'medium')
        pill_class = f"pill-{difficulty}"
        score = session.get('score', 'N/A')
        score_color = '#22c55e' if isinstance(score, (int, float)) and score >= 7 else '#f59e0b' if isinstance(score, (int, float)) and score >= 5 else '#ef4444'
        
        safe_topic = str(session['topic']).replace('_', '\\_').replace('*', '\\*')
        score_display = f"{score}/10" if isinstance(score, (int, float)) else str(score)
        with st.expander(f"{safe_topic}  |  Score: {score_display}", icon="📝", key=f"session_expander_{session['id']}"):
            feedback_data = get_session_feedback(session['id'])
            
            if feedback_data:
                # Header row
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <span class='pill {pill_class}'>{difficulty}</span>
                        <span style='color: #64748b; margin-left: 1rem; font-size: 0.85rem;'>Session #{session['id']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style='text-align: right;'>
                        <span style='color: {score_color}; font-weight: 700; font-size: 1.5rem;'>{score}/10</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Your answer
                st.markdown("""
                <div style='font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;'>Your Answer</div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px; color: #e0e0e0; font-size: 0.9rem; line-height: 1.6; border-left: 3px solid #6366f1;'>
                    {feedback_data.get('user_answer', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Feedback columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #22c55e; margin-bottom: 0.5rem;'>✅ Strengths</div>", unsafe_allow_html=True)
                    for strength in feedback_data.get('strengths', []):
                        st.markdown(f"<div class='feedback-item strength-item'>{strength}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #f59e0b; margin-bottom: 0.5rem;'>⚠️ Weaknesses</div>", unsafe_allow_html=True)
                    for weakness in feedback_data.get('weaknesses', []):
                        st.markdown(f"<div class='feedback-item weakness-item'>{weakness}</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("<div style='font-size: 0.9rem; font-weight: 600; color: #6366f1; margin-bottom: 0.5rem;'>💡 Suggestions</div>", unsafe_allow_html=True)
                    for suggestion in feedback_data.get('suggestions', []):
                        st.markdown(f"<div class='feedback-item suggestion-item'>{suggestion}</div>", unsafe_allow_html=True)
                
                if feedback_data.get('overall_feedback'):
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style='background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 8px; border: 1px solid rgba(99, 102, 241, 0.2);'>
                        <div style='font-size: 0.9rem; font-weight: 600; color: #a855f7; margin-bottom: 0.5rem;'>📝 Overall Feedback</div>
                        <div style='color: #e0e0e0; font-size: 0.9rem; line-height: 1.6;'>{feedback_data['overall_feedback']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Detailed feedback not available for this session")

# Main app logic
def main():
    if 'page_history' not in st.session_state:
        st.session_state.page_history = []
    if 'last_page' not in st.session_state:
        st.session_state.last_page = st.session_state.page
    if st.session_state.page != st.session_state.last_page:
        st.session_state.page_history.append(st.session_state.last_page)
        st.session_state.last_page = st.session_state.page

    render_sidebar()
    
    if not st.session_state.user_id:
        render_auth_page()
    else:
        if st.session_state.page == 'home':
            render_home_page()
        elif st.session_state.page == 'practice':
            render_practice_page()
        elif st.session_state.page == 'sessions':
            render_sessions_page()

if __name__ == "__main__":
    main()
