from fastapi import APIRouter, Depends, HTTPException
from app.models import QueryRequest, QueryResponse, ErrorResponse
from app.document_utils import download_file, extract_text, chunk_text
from app.embedding_utils import EmbeddingStore
from app.llm_utils import answer_question
from app.auth import verify_token
from app.config import EMBEDDING_MODEL

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/hackrx/run", response_model=QueryResponse, responses={401: {"model": ErrorResponse}})
async def run_query(
    request: QueryRequest,
    _: None = Depends(verify_token)
):
    # Step 1: Download and extract text
    try:
        file_path = await download_file(request.documents)
        raw_text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not process document: {str(e)}")
    # Step 2: Chunk and embed
    chunks = chunk_text(raw_text)
    emb_store = EmbeddingStore(EMBEDDING_MODEL)
    emb_store.fit(chunks)
    # Step 3: For each question, retrieve & answer
    answers = []
    for q in request.questions:
        top_chunks, _ = emb_store.search(q, k=3)
        context = "\n---\n".join(top_chunks)
        try:
            answer = await answer_question(context, q)
        except Exception as exc:
            answer = f"Error calling LLM: {exc}"
        answers.append(answer)
    return QueryResponse(answers=answers)
