import os
import tempfile
import httpx
import mimetypes
from PyPDF2 import PdfReader
from docx import Document

async def download_file(url: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        suffix = mimetypes.guess_extension(resp.headers.get("content-type", ""))
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix or ".bin") as tmp:
            tmp.write(resp.content)
            return tmp.name

def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        return "\n".join(p.extract_text() for p in reader.pages if p.extract_text())

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file extension.")

def chunk_text(text: str, chunk_size=500, overlap=100):
    """Chunk text into overlapping segments for embedding search."""
    sentences = text.split('. ')
    chunks, current = [], []
    length = 0
    for sentence in sentences:
        toks = len(sentence.split())
        if length + toks > chunk_size:
            chunks.append('. '.join(current).strip())
            current = current[-overlap//10:] if overlap < len(current) else []
            length = sum(len(s.split()) for s in current)
        current.append(sentence)
        length += toks
    if current:
        chunks.append('. '.join(current).strip())
    return [c for c in chunks if c]
