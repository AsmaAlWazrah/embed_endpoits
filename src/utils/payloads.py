from pydantic import  BaseModel

class EmbeddingPayload(BaseModel):
    text: str
    model: str
    method: str  # 'average' or 'sbert'

    class Config:
        extra = "forbid"
