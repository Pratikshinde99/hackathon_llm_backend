from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    documents: str  # url to PDF or DOCX
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

class ErrorResponse(BaseModel):
    detail: str
