from pydantic import BaseModel, Field
from typing import List

class GanhoItem(BaseModel):
    type: str = Field(..., min_length=1, max_length=50, example="CLT")
    valor: float = Field(..., gt=0, example=1500.00)

class GanhosUpsertRequest(BaseModel):
    ganhos: List[GanhoItem]

class GanhosResponse(BaseModel):
    ganhos: List[GanhoItem]

class MensagemResponse(BaseModel):
    message: str