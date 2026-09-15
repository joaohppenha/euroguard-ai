from sqlalchemy import text
from app.db.session import engine, Base
from app.models.user import User
from app.models.regulation import RegulationChunk

def init_db():
    with engine.connect() as connection:
        # Ativa a extensão de vetores no PostgreSQL
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()
    
    # Cria as tabelas mapeadas
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados e extensão pgvector inicializados com sucesso!")

if __name__ == "__main__":
    init_db()