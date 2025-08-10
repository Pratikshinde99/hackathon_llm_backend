import openai
from app.config import OPENAI_API_KEY, LLM_MODEL

openai.api_key = OPENAI_API_KEY

async def answer_question(context: str, question: str) -> str:
    prompt = (f"Context: {context}\n\n"
              f"Question: {question}\n"
              "Answer in full, listing any relevant conditions, exclusions, and details. "
              "Cite wording as needed. If not found, state not present in document.")
    # Use OpenAI completion API (async will require httpx or similar if you want async here)
    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful document analysis assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=500,
    )
    return response['choices'][0]['message']['content'].strip()
