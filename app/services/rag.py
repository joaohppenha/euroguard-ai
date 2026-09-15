from sqlalchemy.orm import Session
from app.models.regulation import RegulationChunk
from app.services.llm import generate_embedding, generate_rag_response

def search_similar_chunks(db: Session, query: str, top_k: int = 3):
    query_embedding = generate_embedding(query)
    
    chunks = (
        db.query(RegulationChunk)
        .order_by(RegulationChunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )
    return chunks

def answer_regulation_query(db: Session, query: str) -> str:
    context_chunks = search_similar_chunks(db, query)
    
    context_text = "\n\n".join([
        f"[{c.regulation_name} - Article {c.article_number}] {c.title}: {c.content}"
        for c in context_chunks
    ])
    
    prompt = f"""
You are an expert on European regulations (GDPR and EU AI Act).
Answer the user's question using strictly the context provided below.
If the answer cannot be found in the context, state clearly that the information is not available in the retrieved regulatory text.

Context:
{context_text}

Question: {query}
"""
    return generate_rag_response(prompt)