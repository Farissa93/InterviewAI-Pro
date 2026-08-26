"""
RAG Service Module
Handles question retrieval using ChromaDB vector database
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from chromadb.config import Settings
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Initialize embeddings (converts text to numbers)
embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)
# Vector store (where we store question embeddings)
CHROMA_PATH = "./chroma_db"
CHROMA_SETTINGS = Settings(anonymized_telemetry=False)
logging.getLogger("chromadb.telemetry.product.posthog").disabled = True

class QuestionRAG:

    """
    Manages question bank with semantic search
    """
    def __init__(self):
        # Initialize Chroma vector store
        self.vectorstore=None
        self.load_vetorstore()
    def load_vetorstore(self):
        """load existing vectorstore or create new one if not exists
        """
        try:
            self.vectorstore=Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=embeddings,
                client_settings=CHROMA_SETTINGS
            )
            print(f"Loaded existing vector store from {CHROMA_PATH}")
        except Exception as e:
            # Create new if doesn't exist
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=embeddings,
                client_settings=CHROMA_SETTINGS
            )
            print(f"Created new vector store at {CHROMA_PATH}")

    def add_questions(self, questions: list):
        """
        Add questions to vector store
        
        Args:
            questions: List of dicts with keys:
                - question_text
                - topic
                - difficulty
                - model_answer (optional)
                - id (optional)
        """
        documents = []
        
        for q in questions:
            # Create searchable text (question + topic + difficulty)
            text = f"Topic: {q['topic']}\nDifficulty: {q['difficulty']}\nQuestion: {q['question_text']}"
            
            # Create metadata
            metadata = {
                "topic": q['topic'],
                "difficulty": q['difficulty'],
                "question_text": q['question_text'],
                "model_answer": q.get('model_answer', ''),
                "question_id": q.get('id', 0)
            }
            
            # Create document
            doc = Document(
                page_content=text,
                metadata=metadata
            )
            documents.append(doc)
        
        # Add to vector store
        if documents:
            self.vectorstore.add_documents(documents)
            print(f"Added {len(documents)} questions to vector store")
    
    def search_questions(
        self,
        query: str = None,
        topic: str = None,
        difficulty: str = None,
        k: int = 5
    ):
        """
        Search for relevant questions
        
        Args:
            query: Natural language query (optional)
            topic: Filter by topic
            difficulty: Filter by difficulty
            k: Number of results to return
        
        Returns:
            List of matching questions
        """
        # Normalize casing to match stored data
        if topic:
            topic = topic.title()  # "python" -> "Python"
        if difficulty:
            difficulty = difficulty.lower()  # "Easy" -> "easy"

        # Build search query
        if query:
            search_text = query
        else:
            # If no query, build from filters
            parts = []
            if topic:
                parts.append(f"Topic: {topic}")
            if difficulty:
                parts.append(f"Difficulty: {difficulty}")
            search_text = " ".join(parts) if parts else "interview question"
        
        # Build filter (ChromaDB requires $and for multiple conditions)
        filters = []
        if topic:
            filters.append({"topic": topic})
        if difficulty:
            filters.append({"difficulty": difficulty})

        if len(filters) > 1:
            filter_dict = {"$and": filters}
        elif len(filters) == 1:
            filter_dict = filters[0]
        else:
            filter_dict = None

        # Search
        if filter_dict:
            results = self.vectorstore.similarity_search(
                search_text,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search(
                search_text,
                k=k
            )
        
        # Format results
        questions = []
        for doc in results:
            questions.append({
                "question_text": doc.metadata["question_text"],
                "topic": doc.metadata["topic"],
                "difficulty": doc.metadata["difficulty"],
                "model_answer": doc.metadata.get("model_answer", ""),
                "question_id": doc.metadata.get("question_id", 0)
            })
        
        return questions
    
    def get_similar_questions(self, question_text: str, k: int = 3):
        """
        Find questions similar to given question
        (Useful to avoid asking same question twice)
        """
        results = self.vectorstore.similarity_search(
            question_text,
            k=k
        )
        
        return [{
            "question_text": doc.metadata["question_text"],
            "topic": doc.metadata["topic"],
            "difficulty": doc.metadata["difficulty"],
            "question_id": doc.metadata.get("question_id", 0)
        } for doc in results]
    
    def count_questions(self):
        """Get total number of questions in vector store"""
        try:
            # This is a workaround since Chroma doesn't have direct count
            all_docs = self.vectorstore.get()
            return len(all_docs['ids']) if all_docs else 0
        except:
            return 0


# Global instance
question_rag = QuestionRAG()


def seed_sample_questions():
    """
    Add sample questions to vector store (for testing)
    """
    sample_questions = [
        {
            "topic": "Python",
            "difficulty": "easy",
            "question_text": "What is the difference between a list and a tuple in Python?",
            "model_answer": "Lists are mutable (can be changed), tuples are immutable (cannot be changed after creation)."
        },
        {
            "topic": "Python",
            "difficulty": "medium",
            "question_text": "Explain how Python's decorator pattern works.",
            "model_answer": "Decorators are functions that modify the behavior of other functions. They use the @ syntax."
        },
        {
            "topic": "Python",
            "difficulty": "hard",
            "question_text": "Explain the Global Interpreter Lock (GIL) and its implications.",
            "model_answer": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously."
        },
        {
            "topic": "JavaScript",
            "difficulty": "easy",
            "question_text": "What is the difference between let, const, and var?",
            "model_answer": "var is function-scoped, let and const are block-scoped. const cannot be reassigned."
        },
        {
            "topic": "JavaScript",
            "difficulty": "medium",
            "question_text": "Explain closures in JavaScript.",
            "model_answer": "A closure is a function that has access to variables in its outer (enclosing) function's scope chain."
        },
        {
            "topic": "System Design",
            "difficulty": "hard",
            "question_text": "How would you design a URL shortener like bit.ly?",
            "model_answer": "Key components: hash function for short URLs, database for mappings, caching layer, load balancer for scalability."
        },
        {
            "topic": "Algorithms",
            "difficulty": "medium",
            "question_text": "Explain the difference between BFS and DFS.",
            "model_answer": "BFS explores level by level (uses queue), DFS explores depth-first (uses stack or recursion)."
        },
    ]
    
    question_rag.add_questions(sample_questions)
    print(f"Seeded {len(sample_questions)} sample questions")


if __name__ == "__main__":
    print("Testing RAG Service...\n")
    
    # Seed sample questions
    seed_sample_questions()
    
    # Test search
    print("\n1. Searching for Python questions:")
    results = question_rag.search_questions(topic="Python", k=3)
    for i, q in enumerate(results, 1):
        print(f"{i}. [{q['difficulty']}] {q['question_text']}")
    
    print("\n2. Searching for 'decorator' related questions:")
    results = question_rag.search_questions(query="decorator pattern", k=2)
    for i, q in enumerate(results, 1):
        print(f"{i}. {q['question_text']}")
    
    print(f"\n3. Total questions in database: {question_rag.count_questions()}")