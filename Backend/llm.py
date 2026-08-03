import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Load .env
load_dotenv()

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",      # More stable than gemini-flash-latest
    google_api_key=api_key,
    temperature=0.3,
    timeout=120,                   # Wait up to 2 minutes
    max_retries=3,
)

# Prompt template for Resume Q&A
prompt = ChatPromptTemplate.from_template("""
You are an AI Resume Assistant.

Answer ONLY using the information provided in the resume context.

If the answer is not present in the context, reply exactly:

I couldn't find that information in the resume.

Resume Context:
{context}

Question:
{question}
""")


def extract_text(content):
    """Extract clean text from Gemini response."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        answer = ""

        for block in content:

            # Gemini dictionary block
            if isinstance(block, dict):
                if block.get("type") == "text":
                    answer += block.get("text", "")

            # LangChain object block
            elif hasattr(block, "text"):
                answer += block.text

        return answer.strip()

    return str(content)


def ask_llm(context, question):
    """Ask Gemini questions about the resume."""

    try:

        chain = prompt | llm

        response = chain.invoke(
            {
                "context": context[:4000],   # Limit context
                "question": question,
            }
        )

        return extract_text(response.content)

    except Exception as e:
        print("LLM Error:", e)
        return f"Error: {str(e)}"