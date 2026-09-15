from google import genai
from app.core.config import settings

# Inicializa o cliente oficial do Google GenAI
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
    )
    return response.embeddings[0].values

def generate_rag_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt,
    )
    return response.text