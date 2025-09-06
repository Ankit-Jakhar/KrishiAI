AI-powered Agriculture Expert Assistant

KrishiAI is a Retrieval-Augmented Generation (RAG) based application designed to assist farmers, researchers, and agri-experts with accurate agricultural knowledge. It combines the power of FastAPI, Streamlit, LLMs, and vector databases to answer user queries.

🚀 Features

Streamlit Frontend – Simple, user-friendly interface for asking questions

FastAPI Backend – High-performance API serving AI responses

RAG Pipeline – Retrieve domain-specific knowledge from ChromaDB and generate answers with an LLM

Embeddings – Uses HuggingFace models for semantic search

Generative AI – Provides natural, human-like responses

CI/CD Ready – GitHub Actions workflow included for automated testing & deployment

Docker Support – Easy containerized deployment

🛠️ Tech Stack

Python 3.11+

FastAPI
 – Backend framework

Streamlit
 – Frontend UI

LangChain
 – Orchestration of RAG pipeline

ChromaDB
 – Vector database for embeddings

HuggingFace Transformers
 – Embedding model + LLM integration

GitHub Actions – CI/CD
Docker – Containerization
Deployment - AWS EC2 Server

📂 Project Structure
KrishiAI/
│── main.py                 # FastAPI backend
│── app.py                  # Streamlit frontend
│── requirements.txt        # Python dependencies
│── .gitignore              # Ignored files (e.g., .env, venv)
│── .env                    # API keys & secrets (not pushed to GitHub)
│── src/
│   ├── retriever/
│   │    └── retriever.py   # RAG retriever logic
│   └── models/
│        └── schemas.py     # Pydantic models for API requests/responses
│── tests/                  # (optional) Unit tests
