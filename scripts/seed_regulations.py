from app.db.session import SessionLocal
from app.models.regulation import RegulationChunk
from app.services.llm import generate_embedding

SAMPLE_REGULATIONS = [
    {
        "regulation_name": "GDPR",
        "article_number": "Article 6(1)(a)",
        "title": "Lawfulness of processing - Consent",
        "content": "Processing shall be lawful only if the data subject has given consent to the processing of his or her personal data for one or more specific purposes."
    },
    {
        "regulation_name": "GDPR",
        "article_number": "Article 17",
        "title": "Right to erasure ('right to be forgotten')",
        "content": "The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay."
    },
    {
        "regulation_name": "EU_AI_ACT",
        "article_number": "Article 5",
        "title": "Prohibited AI Practices",
        "content": "The placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques or real-time remote biometric identification in publicly accessible spaces for law enforcement is prohibited."
    },
    {
        "regulation_name": "EU_AI_ACT",
        "article_number": "Article 10",
        "title": "Data and data governance",
        "content": "High-risk AI systems which make use of techniques involving the training of models with data shall be developed on the basis of training, validation and testing data sets that meet high quality criteria."
    }
]

def seed_data():
    db = SessionLocal()
    try:
        print("🌱 Gerando embeddings e populando o banco de dados...")
        for item in SAMPLE_REGULATIONS:
            text_to_embed = f"{item['regulation_name']} {item['article_number']} - {item['title']}: {item['content']}"
            embedding = generate_embedding(text_to_embed)
            
            chunk = RegulationChunk(
                regulation_name=item["regulation_name"],
                article_number=item["article_number"],
                title=item["title"],
                content=item["content"],
                embedding=embedding
            )
            db.add(chunk)
        db.commit()
        print("✅ Dados de regulação (GDPR + EU AI Act) populados com sucesso!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()