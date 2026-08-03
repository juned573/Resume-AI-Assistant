from langchain_core.prompts import ChatPromptTemplate
from Backend.llm import llm

prompt = ChatPromptTemplate.from_template("""
You are a senior technical interviewer.

Evaluate the candidate's interview answer.

Interview Question:
{question}

Candidate Answer:
{answer}

Job Description:
{job_description}

Return ONLY Markdown in the following format.

# Score
Score: X/10

# Strengths
- Point 1
- Point 2

# Weaknesses
- Point 1
- Point 2

# Ideal Answer
Provide a concise professional answer.

# Interview Tips
- Tip 1
- Tip 2
""")

chain = prompt | llm


def extract_text(content):
    """Extract text from Gemini response."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text = ""

        for block in content:

            if isinstance(block, dict):
                if block.get("type") == "text":
                    text += block.get("text", "")

            elif hasattr(block, "text"):
                text += block.text

        return text.strip()

    return str(content)


def evaluate_answer(question, answer, job_description):
    """Evaluate the user's interview answer."""

    try:

        response = chain.invoke(
            {
                "question": question,
                "answer": answer,
                "job_description": job_description[:1500],
            }
        )

        return extract_text(response.content)

    except Exception as e:
        print("Evaluation Error:", e)
        return f"❌ Error evaluating answer.\n\n{str(e)}"