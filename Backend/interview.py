from langchain_core.prompts import ChatPromptTemplate
from Backend.llm import llm

# Create the prompt once
prompt = ChatPromptTemplate.from_template("""
You are a senior software engineering interviewer.

Generate exactly 10 interview questions.

Requirements:

- Return ONLY the questions.
- One question per line.
- No numbering.
- No markdown.
- No bullets.
- No explanations.

Resume:
{resume}

Job Description:
{job_description}
""")
# Create the chain only once
chain = prompt | llm


def extract_text(content):
    """Extract clean text from Gemini response."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        answer = ""

        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    answer += block.get("text", "")

            elif hasattr(block, "text"):
                answer += block.text

        return answer.strip()

    return str(content)


def generate_questions(resume, job_description):
    """Generate interview questions using Gemini."""

    try:
        # Validate inputs
        if not resume or not resume.strip():
            return "❌ Resume is empty."

        if not job_description or not job_description.strip():
            return "❌ Job description is empty."

        # Limit input size
        resume = resume[:2500]
        job_description = job_description[:1500]

        print("=" * 60)
        print("Generating Interview Questions")
        print(f"Resume length: {len(resume)}")
        print(f"Job Description length: {len(job_description)}")
        print("=" * 60)

        payload = {
            "resume": resume,
            "job_description": job_description,
        }

        print("Sending request to Gemini...")

        response = chain.invoke(payload)

        print("✅ Gemini responded successfully.")
        print("Response type:", type(response))
        print("Content type:", type(response.content))

        text = extract_text(response.content)

        questions = [
            q.strip()
            for q in text.split("\n")
            if q.strip()
]

        return questions

    except Exception as e:
        print("=" * 60)
        print("Interview generation failed")
        print(type(e).__name__)
        print(str(e))
        print("=" * 60)

        return f"❌ Error generating interview questions.\n\n{str(e)}"