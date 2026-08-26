import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)