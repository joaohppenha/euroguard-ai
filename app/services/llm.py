from google import genai
from google.genai.errors import APIError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from app.core.config import settings

# Initialize official Google GenAI SDK client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_embedding(text: str) -> list[float]:
    """Generates text vector embeddings using Gemini Embedding model."""
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
    )
    return response.embeddings[0].values

@retry(
    retry=retry_if_exception_type(APIError),
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    reraise=True
)
def generate_rag_response(prompt: str) -> str:
    """Generates completion text response using Gemini 3.6 Flash with automated retries."""
    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt,
    )
    return response.text