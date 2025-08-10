from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(
    title="Hackathon LLM Backend",
    version="1.0.0",
    description="LLM-powered document Q&A backend"
)

# Enable CORS for testing/demo usage:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, tighten this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
