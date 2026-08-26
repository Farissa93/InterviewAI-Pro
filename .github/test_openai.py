import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env file
load_dotenv()

# Check if key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
    exit()

print("✅ API Key loaded successfully!")


# Test API call
try:
    llm = ChatOpenAI(model="gpt-3.5-turbo")  # Using cheaper model for test
    response = llm.invoke("Say 'Hello, API is working!' in one sentence.")
    print(f"\n✅ API Call Successful!")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"\n❌ API Call Failed: {e}")