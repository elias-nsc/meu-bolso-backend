from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CadastroSchema(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, example="Maria Silva")
    email: EmailStr = Field(..., example="maria@exemplo.com")
    senha: str = Field(..., min_length=6, example="senhaSegura123")

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="maria@exemplo.com")
    senha: str = Field(..., example="senhaSegura123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    mensagem: str | None = None

class UserResponse(BaseModel):
    id: str
    nome: str
    email: str
    foto_url: Optional[str] = None
    google_id: Optional[str] = None
    criado_em: datetime