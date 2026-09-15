from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from app.db.session import Base

class RegulationChunk(Base):
    __tablename__ = "regulation_chunks"

    id = Column(Integer, primary_key=True, index=True)
    regulation_name = Column(String, index=True, nullable=False)
    article_number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(3072))  