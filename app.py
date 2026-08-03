import tempfile
import streamlit as st
import time
import hashlib

from Backend.interview import generate_questions
from Backend.loader import load_resume
from Backend.chunker import chunk_text
from Backend.embeddings import create_embeddings
from Backend.vectorstore import VectorStore
from Backend.retriever import retrieve
from Backend.llm import ask_llm
from Backend.analyzer import analyze_resume
from streamlit_pdf_viewer import pdf_viewer
from Backend.job_match import calculate_match
from Backend.evaluation import evaluate_answer

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="Resume AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ---------------- Load CSS ---------------- #

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
# ---------------- Session State ---------------- #
# ---------------- Session State ---------------- #

defaults = {
    "vector_store": None,
    "chunks": None,
    "resume_hash": None,
    "answer": "",
    "context": "",
    "chat_history": [],
    "stats": {},
    "resume_analysis": {},
    "pdf_bytes": None,
    "match_result": None,
    "resume_text": "",
    "interview_questions": [],
    "selected_question": "",
    "evaluation": ""
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

#------------Hero----------#
st.markdown("""
<div class="hero">
<h1>🤖 Resume AI Assistant</h1>
<p>Upload your resume and ask AI anything about it.</p>
</div>
""", unsafe_allow_html=True)
#------Upload Resume Card---------#
st.markdown("""
<div class="card">
    <h2>📄 Upload Resume</h2>
    <p>Upload your resume in PDF format.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["pdf"],
    label_visibility="collapsed"
)

if uploaded_file is not None:

    # Read file once
    file_bytes = uploaded_file.getvalue()

    # Create unique hash for the file
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Process only if it's a different resume
    if st.session_state.resume_hash != file_hash:

        with st.spinner("Processing resume..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                pdf_path = tmp.name

            resume = load_resume(pdf_path)
            st.session_state.resume_text = resume
            resume_analysis = analyze_resume(resume)

            st.session_state.resume_analysis = resume_analysis
            

            chunks = chunk_text(resume)
            

            if len(chunks) == 0:
                st.error("Couldn't extract any sections from the resume.")
                st.stop()

            embeddings = create_embeddings(chunks)

            if len(embeddings) == 0:
                st.error("Failed to generate embeddings.")
                st.stop()

            vector_store = VectorStore(embeddings.shape[1])
            vector_store.add_embeddings(embeddings)

            st.session_state.vector_store = vector_store
            st.session_state.chunks = chunks
            st.session_state.resume_hash = file_hash
            st.session_state.pdf_bytes = file_bytes

            st.session_state.stats = {
                "Chunks": len(chunks),
                "Embedding": "MiniLM-L6-v2",
                "Vector Store": "FAISS",
                "LLM": "Gemini Flash"
            }

        st.success("✅ Resume processed successfully!")
#---------Ask AI Card------#
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 💬 Ask AI")

question = st.text_input(
    "",
    placeholder="Ask anything about this resume..."
)

ask = st.button(
    "🚀 Ask AI",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)
#-------------AI Response Card--------#
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## ✨ AI Response")

if st.session_state.answer:

    st.success(st.session_state.answer)

    with st.expander("📚 Retrieved Context"):
        st.write(st.session_state.context)

else:

    st.info("Upload a resume and ask a question to begin.")

st.markdown("</div>", unsafe_allow_html=True)
if st.session_state.resume_analysis:

    st.markdown("## 📊 Resume Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Skills", st.session_state.resume_analysis["Skills"])

    with col2:
        st.metric("Projects", st.session_state.resume_analysis["Projects"])

    with col3:
        st.metric("Experience", st.session_state.resume_analysis["Experience"])

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Education", st.session_state.resume_analysis["Education"])

    with col5:
        st.metric("Certificates", st.session_state.resume_analysis["Certificates"])

    st.markdown("### 🛠 Detected Skills")

    st.write(", ".join(st.session_state.resume_analysis["Detected Skills"]))
if st.session_state.pdf_bytes:
    
    st.markdown("## 📄 Resume Preview")

    pdf_viewer(
        st.session_state.pdf_bytes,
        width=900,
        height=700
    )
#-------------Job Description UI--------#
st.markdown("---")
st.markdown("## 🎯 Resume Match Score")

job_description = st.text_area(
    "Paste the Job Description",
    height=180,
    placeholder="Paste the job description here..."
)

analyze_match = st.button(
    "📊 Analyze Match",
    use_container_width=True
)
if analyze_match:

    if not st.session_state.resume_text:
        st.warning("Please upload a resume first.")

    elif not job_description.strip():
        st.warning("Please paste a job description.")

    else:

        result = calculate_match(
            st.session_state.resume_text,
            job_description
        )

        st.session_state.match_result = result
if st.session_state.match_result:

    result = st.session_state.match_result

    st.markdown("## 📊 Match Analysis")

    st.metric(
        "Overall Match Score",
        f"{result['score']}%"
    )

    st.progress(result["score"] / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Semantic Similarity",
            f"{result['semantic']}%"
        )

    with col2:
        st.metric(
            "Skill Match",
            f"{result['skill_score']}%"
        )

    st.markdown("### ✅ Matching Skills")

    if result["matched"]:
        st.success(", ".join(result["matched"]))
    else:
        st.warning("No matching skills found.")

    st.markdown("### ❌ Missing Skills")

    if result["missing"]:
        st.error(", ".join(result["missing"]))
    else:
        st.success("No missing skills. Great match!")

    st.markdown("### 💡 Recommendation")

    if result["score"] >= 85:
        st.success(
            "Excellent match! The resume aligns very well with the job description."
        )
    elif result["score"] >= 70:
        st.info(
            "Good match. A few additional skills could strengthen the application."
        )
    else:
        st.warning(
            "The resume could be improved by adding more relevant skills and experience."
        )
#-------------Resume Match Score-------------#
st.markdown("---")
st.markdown("## 🎤 AI Interview Preparation")

generate = st.button(
    "Generate Interview Questions",
    use_container_width=True
)
if generate:

    if not st.session_state.resume_text:

        st.warning("Upload a resume first.")

    elif not job_description.strip():

        st.warning("Paste a Job Description first.")

    else:

        with st.spinner("Generating Interview Questions..."):

            questions = generate_questions(
                st.session_state.resume_text,
                job_description
            )

            st.session_state.interview_questions = questions
if st.session_state.interview_questions:

    st.markdown("## 🎯 Interview Questions")

    st.markdown(st.session_state.interview_questions)
#---------Add evaluation--------#
st.markdown("## ✍️ Answer the Selected Question")

answer = st.text_area(
    "Your Answer",
    height=180,
)

evaluate = st.button(
    "Evaluate Answer",
    use_container_width=True,
)

if evaluate:

    if answer.strip() == "":
        st.warning("Please write an answer.")

    else:

        with st.spinner("Evaluating..."):

            feedback = evaluate_answer(
                question=st.session_state.selected_question,
                answer=answer,
                job_description=job_description,
            )

            st.session_state.evaluation = feedback

if st.session_state.evaluation:

    st.markdown("## 🤖 AI Feedback")

    st.markdown(st.session_state.evaluation)
    # ---------- Individual Scores ----------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Semantic Similarity",
            f"{result['semantic']}%"
        )

    with col2:
        st.metric(
            "Skill Match",
            f"{result['skill_score']}%"
        )

    # ---------- Matching Skills ----------

    st.markdown("### ✅ Matching Skills")

    if result["matched"]:

        st.success(", ".join(result["matched"]))

    else:

        st.warning("No matching skills found.")

    # ---------- Missing Skills ----------

    st.markdown("### ❌ Missing Skills")

    if result["missing"]:

        st.error(", ".join(result["missing"]))

    else:

        st.success("No missing skills. Great match!")

    # ---------- Recommendation ----------

    st.markdown("### 💡 Recommendation")

    if result["score"] >= 85:

        st.success(
            "Excellent match! The resume aligns very well with the job description."
        )

    elif result["score"] >= 70:

        st.info(
            "Good match. A few additional skills could strengthen the application."
        )

    else:

        st.warning(
            "The resume could be improved by adding more relevant skills and experience."
        )
# ---------------- Chat History ---------------- #

if st.session_state.chat_history:

    st.markdown("## 💬 Chat History")

    for chat in reversed(st.session_state.chat_history):

        st.markdown(
            f"""
<div class="chat-question">
<b>👤 You</b><br>
{chat['question']}
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="chat-answer">
<b>🤖 AI</b><br>
{chat['answer']}
</div>
""",
            unsafe_allow_html=True
        )
#----------Professional Sidebar------#
with st.sidebar:

    st.markdown("""
    <div class="logo-area">
        <h2>🤖 Resume AI</h2>
        <p>Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📄 Resume")

    if uploaded_file:
        st.success("Resume uploaded")
        st.caption(uploaded_file.name)
    else:
        st.info("No resume uploaded")

    

    st.divider()

    st.markdown("### ⚙ AI Configuration")
    st.divider()

    st.markdown("### 📊 Resume Statistics")

    if st.session_state.stats:

        for key, value in st.session_state.stats.items():
            st.write(f"**{key}:** {value}")

    else:

        st.info("Upload a resume")


    st.markdown("""
    🤖 Gemini

    🔍 all-MiniLM-L6-v2

    🗄 FAISS
    """)

    st.divider()

    st.markdown("""
    <div class="developer-card">
        <h4>👨‍💻 Built by</h4>
        <h3>Md Juned Eqbal</h3>
        <p>AI Engineer | Backend Developer</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
   
        st.session_state.answer = ""
        st.session_state.context = ""
        st.session_state.chat_history = []

        st.session_state.vector_store = None
        st.session_state.chunks = None
        st.session_state.resume_hash = None
        st.session_state.resume_text = ""
        st.session_state.resume_analysis = {}
        st.session_state.stats = {}
        st.session_state.pdf_bytes = None

        st.session_state.match_result = None
        st.session_state.interview_questions = ""

        st.rerun()

# ---------------- Ask AI Pipeline ---------------- #

if ask:

    # No resume uploaded
    if st.session_state.vector_store is None:
        st.warning("Please upload a resume first.")

    # Empty question
    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 Thinking..."):

            start = time.time()

            # Retrieve relevant resume chunks
            retrieved_chunks = retrieve(
                question,
                st.session_state.vector_store,
                st.session_state.chunks
    )

            context = "\n\n".join(retrieved_chunks)

            # Generate answer
            answer = ask_llm(context, question)

            end = time.time()

            processing_time = round(end - start, 2)

            st.session_state.stats["Processing Time"] = f"{processing_time} sec"

            st.session_state.answer = answer
            st.session_state.context = context

            st.session_state.chat_history.append({
                "question": question,
                "answer": answer
                
    })
            st.rerun()