# RAG-Based Complaint Chatbot 🤖

A modular chatbot built with:

- Gemini 2.0 (Google Generative AI)
- FastAPI backend (complaint register/check)
- Streamlit UI
- LangChain-powered RAG with PDF

## 🚀 Run Instructions

### 0. Install `uv` (if not already installed)

```bash
pip install uv
```

### 1. Install dependencies

```bash
git clone https://github.com/Sunilktu/rag_complaint_chatbot.git
cd rag_complaint_chatbot

# (Recommended) Create a virtual environment using uv
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Create a `.env` file and add your Gemini API key
```

```bash
echo GOOGLE_API_KEY="Your Gemini API key" > .env
```

### 2. Start the FastAPI backend

```bash
uv run api/main.py
```

This command will automatically install all dependencies from `pyproject.toml` and start the application at [http://localhost:8000](http://localhost:8000).

### 3. Start the Streamlit frontend

```bash
uv run streamlit run ui/ui_app.py
```

This will launch the Streamlit UI for interacting with the chatbot.