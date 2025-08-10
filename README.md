# hackathon_llm_backend

# Hackathon LLM Backend

**Features:**
- LLM-powered document question answering (PDF/DOCX)
- Semantic retrieval (SentenceTransformers + FAISS)
- GPT-4 answers, citing policy/contract wording
- Bearer token authentication

## Quick start

1. `pip install -r requirements.txt`
2. Copy `.env.template` to `.env` and set `OPENAI_API_KEY`.
3. `uvicorn app.main:app --reload`
4. Test `/docs` or `/hackrx/run` endpoint.
