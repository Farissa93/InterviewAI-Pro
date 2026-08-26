from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from .rag_service import question_rag

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,# lower=more deterministic, higher=more creative
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)


class GeneratedQuestion(BaseModel):
    """A single interview question with a model answer."""
    question_text: str = Field(description="The interview question")
    model_answer: str = Field(description="A detailed, ideal answer to the question")


class AnswerEvaluation(BaseModel):
    """Evaluation of a candidate's answer to an interview question."""
    score: float = Field(description="Score from 0 to 10", ge=0, le=10)
    feedback: str = Field(description="2-3 sentences of overall feedback")
    strengths: list[str] = Field(description="What the answer did well")
    weaknesses: list[str] = Field(description="What the answer is missing or gets wrong")
    suggestions: list[str] = Field(description="Specific, actionable improvements")


question_llm = llm.with_structured_output(GeneratedQuestion)
evaluation_llm = llm.with_structured_output(AnswerEvaluation)


def generate_interview_question(topic: str, difficulty: str) -> dict:
    """Args:
    topic: e.g., "Python", "JavaScript", "System Design"
    difficulty: "easy", "medium", or "hard"

    Returns:
    dict with question_text and model_answer
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert technical interviewer. Generate one high quality interview question.",
            ),
            ("user", "Generate a {difficulty} question about {topic}."),
        ]
    )

    chain = prompt | question_llm

    try:
        result: GeneratedQuestion = chain.invoke({"topic": topic, "difficulty": difficulty})

        return {
            "question_text": result.question_text,
            "model_answer": result.model_answer,
            "topic": topic,
            "difficulty": difficulty,
        }
    except Exception as e:
        raise Exception(f"Error generating question: {str(e)}")


def evaluate_answer(question: str, user_answer: str) -> dict:
    """
    Evaluate user's interview answer using AI

    Args:
        question: The interview question
        user_answer: User's answer

    Returns:
        dict with score, feedback, strengths, weaknesses
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert technical interviewer evaluating a candidate's answer.
Score strictly on relevance and correctness relative to the question, using the
full 0-10 range instead of clustering scores near the middle:

- 0-1: Off-topic, blank, gibberish, or an answer that does not address the
  question's subject matter at all (e.g. "banana" or random text for a
  technical question).
- 2-3: On-topic but almost entirely wrong or missing the key concept, showing
  little real understanding.
- 4-5: Partially correct; captures some relevant ideas but has significant
  gaps, errors, or vagueness.
- 6-7: Mostly correct and relevant with minor gaps or imprecision.
- 8-10: Accurate, complete, and well-explained.

Judge relevance first: if the answer does not actually engage with the
question being asked, it must score in the 0-1 range regardless of length or
confidence.""",
            ),
            (
                "user",
                """Question: {question}
         User's Answer: {user_answer}
         Evaluate the answer.""",
            ),
        ]
    )
    chain = prompt | evaluation_llm

    try:
        result: AnswerEvaluation = chain.invoke({"question": question, "user_answer": user_answer})

        return {
            "score": result.score,
            "feedback": result.feedback,
            "strengths": result.strengths,
            "weaknesses": result.weaknesses,
            "suggestions": result.suggestions,
        }
    except Exception as e:
        raise Exception(f"AI evaluation failed: {str(e)}")


def quick_test():
    print("Testing AI service...\n")
    print("1. Generating question...")
    result = generate_interview_question("Python", "easy")
    print(f"Question: {result['question_text'][:100]}...")

    print("\n2. Evaluating answer...")
    eval_result = evaluate_answer(
        "What is a list in Python?",
        "A list is a data structure in Python that can hold an ordered collection of items. "
        "It is mutable, meaning you can change its contents after creation. Lists are defined "
        "using square brackets, e.g., my_list = [1, 2, 3]. You can perform various operations "
        "on lists, such as adding, removing, and slicing elements.",
    )
    print(f"Score: {eval_result['score']}/10")
    print(f"Feedback: {eval_result['feedback'][:100]}...")

def generate_question_with_rag(topic: str, difficulty: str) -> dict:
    """
    Generate question using RAG (retrieve from question bank)
    Falls back to AI generation if no matching questions found
    
    Args:
        topic: Topic area
        difficulty: easy/medium/hard
    
    Returns:
        dict with question details
    """
    # Try to find matching question in vector store
    results = question_rag.search_questions(
        topic=topic,
        difficulty=difficulty,
        k=1  # Get best match
    )
    
    if results:
        # Found a match in question bank!
        question = results[0]
        return {
            "question_text": question["question_text"],
            "model_answer": question["model_answer"],
            "topic": topic,
            "difficulty": difficulty,
            "source": "question_bank"  # Came from RAG
        }
    else:
        # No match found, generate with AI
        print(f"No questions found for {topic}/{difficulty}, generating with AI...")
        result = generate_interview_question(topic, difficulty)
        result["source"] = "ai_generated"
        return result


if __name__ == "__main__":
    quick_test()