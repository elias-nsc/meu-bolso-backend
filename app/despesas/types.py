from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DespesaCreateSchema(BaseModel):
    descricao: str = Field(..., max_length=200)
    categoria: str
    tipo_gasto: str = Field(..., pattern='^(fixo|variavel)$')
    forma_pagamento: str = Field(..., pattern='^(credito|debito|dinheiro|pix)$')
    valor_total: float = Field(..., gt=0)
    total_parcelas: int = Field(..., ge=1, le=12)
    valor_parcela: float = Field(..., gt=0)
    data_primeira_parcela: datetime
    dia_vencimento: int = Field(..., ge=1, le=31)

class DespesaResponseSchema(BaseModel):
    id: str
    user_id: str
    descricao: str
    categoria: str
    tipo_gasto: str
    forma_pagamento: str
    valor_total: float
    total_parcelas: int
    valor_parcela: float
    data_primeira_parcela: datetime
    dia_vencimento: int
    criado_em: datetime

class DespesaDeleteResponse(BaseModel):
    message: str