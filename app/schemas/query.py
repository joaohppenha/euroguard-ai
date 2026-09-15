from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(
        ..., 
        min_length=3,
        description="The query regarding GDPR or EU AI Act regulations.",
        json_schema_extra={"example": "What are the requirements for high-risk AI data governance?"}
    )

class QueryResponse(BaseModel):
    query: str
    response: str