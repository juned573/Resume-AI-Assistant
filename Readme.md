# 🤖 Resume AI Assistant

An AI-powered Resume Analysis and Interview Preparation platform built using **Streamlit**, **LangChain**, **Google Gemini**, **Sentence Transformers**, and **FAISS**.

The application enables users to upload a resume, ask questions about it using Retrieval-Augmented Generation (RAG), analyze resume quality, compare resumes with job descriptions, generate interview questions, and evaluate interview answers.

---

## 🚀 Features

### 📄 Resume Upload & Processing
- Upload resumes in PDF format
- Extracts text using PDF parsing
- Automatically processes and indexes resume content

### 🔍 AI Resume Q&A (RAG)
- Ask natural language questions about the uploaded resume
- Retrieves the most relevant resume sections using FAISS
- Uses Google Gemini to generate context-aware responses

### 📊 Resume Insights
Automatically analyzes the resume and displays:
- Skills count
- Projects count
- Experience count
- Education count
- Certifications count
- Detected technical skills

### 🎯 Resume Match Score
Compare a resume with any Job Description and receive:
- Overall Match Score
- Semantic Similarity Score
- Skill Match Score
- Matching Skills
- Missing Skills
- AI-based Recommendation

### 🎤 AI Interview Question Generator
Generates interview questions based on:
- Resume
- Job Description

Questions include:
- 5 Technical Questions
- 3 HR / Behavioral Questions
- 2 Project-based Questions

### ✅ AI Interview Answer Evaluation
Evaluates candidate responses by providing:
- Score (Out of 10)
- Strengths
- Weaknesses
- Ideal Answer
- Interview Tips

### 🐳 Docker Support
- Dockerized application
- Docker Compose support
- Environment variables managed securely using `.env`

---

# 🏗️ Project Architecture

```
                    User Uploads Resume
                             │
                             ▼
                    PDF Text Extraction
                             │
                             ▼
                      Text Chunking
                             │
                             ▼
             Sentence Transformer Embeddings
                             │
                             ▼
                     FAISS Vector Store
                             │
                             ▼
                     Similarity Search
                             │
                             ▼
                  Retrieved Resume Context
                             │
                             ▼
                   Google Gemini (LLM)
                             │
                             ▼
                    AI Generated Response
```

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI / LLM
- Google Gemini Flash
- LangChain

## Embedding Model
- all-MiniLM-L6-v2
- Sentence Transformers

## Vector Database
- FAISS

## PDF Processing
- PyPDF

## Machine Learning
- Scikit-learn

## Deployment
- Docker
- Docker Compose

---

# 📂 Project Structure

```
Resume-AI-Assistant
│
├── Backend
│   ├── analyzer.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── evaluation.py
│   ├── interview.py
│   ├── job_match.py
│   ├── llm.py
│   ├── loader.py
│   ├── retriever.py
│   └── vectorstore.py
│
├── assets
│   ├── logo.png
│   └── style.css
│
├── uploaded_resumes
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .dockerignore
└── README.md
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/juned573/Resume-AI-Assistant.git

cd Resume-AI-Assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# 🐳 Docker

## Build Docker Image

```bash
docker build -t resume-ai-assistant .
```

## Run Container

```bash
docker run --env-file .env -p 8501:8501 resume-ai-assistant
```

---

# 🐳 Docker Compose

Start the application

```bash
docker compose up
```

Rebuild after code changes

```bash
docker compose up --build
```

Stop the application

```bash
docker compose down
```

# 🔮 Future Improvements

- Multi-resume comparison
- Resume improvement suggestions
- ATS compatibility checker
- Voice-based interview simulation
- Chat history export
- Authentication and user accounts
- Cloud deployment (AWS/Azure/GCP)
- CI/CD pipeline using GitHub Actions

---

# 👨‍💻 Author

**Md Juned Eqbal**

AI/ML Engineer | Python Developer | Backend Developer

GitHub:
https://github.com/juned573

LinkedIn:
https://www.linkedin.com/in/md-juned-eqbal-2bb85023a/

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.