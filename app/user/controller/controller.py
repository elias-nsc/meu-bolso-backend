from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt
from passlib.context import CryptContext

from app.models.models import User
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES

# ── Configuração de senha ────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Configuração do esquema Bearer ───────────────────────────────────────────
bearer_scheme = HTTPBearer()


# ── Helpers de senha ─────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ── Geração e decodificação de token (INCLUINDO user_id) ─────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRATION_MINUTES))
    payload.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Dependência reutilizável: get_current_user ────────────────────────────────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> User:
    payload = decode_access_token(credentials.credentials)
    email: str = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return user


# ── Cadastro (inclui user_id no token) ───────────────────────────────────────
def cadastrar_usuario(nome: str, email: str, senha: str) -> dict:
    if User.objects(email=email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    user = User(
        nome=nome,
        email=email,
        senha_hash=hash_password(senha),
    )
    user.save()

    token = create_access_token({
        "sub": email,
        "user_id": str(user.id)          # <-- ID do usuário salvo em cookie
    })
    return {
        "mensagem": "Usuário cadastrado com sucesso.",
        "access_token": token,
        "token_type": "bearer",
    }


# ── Login (inclui user_id no token) ──────────────────────────────────────────
def login_usuario(email: str, senha: str) -> dict:
    user = User.objects(email=email).first()
    if not user or not verify_password(senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    token = create_access_token({
        "sub": email,
        "user_id": str(user.id)          # <-- ID do usuário salvo em cookie
    })
    return {
        "access_token": token,
        "token_type": "bearer",
    }

def get_usuario_por_id(user_id: str, current_user: User) -> dict:
    """
    Retorna os dados do usuário desde que o usuário autenticado seja o mesmo.
    """
    # Converte o ID do usuário atual (ObjectId) para string e compara
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar dados de outro usuário."
        )

    # Busca o usuário novamente (opcional, mas seguro)
    user = User.objects(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    # Retorna os dados públicos (sem senha_hash)
    return {
        "id": str(user.id),
        "nome": user.nome,
        "email": user.email,
        "foto_url": user.foto_url if hasattr(user, 'foto_url') else None,
        "google_id": user.google_id if hasattr(user, 'google_id') else None,
        "criado_em": user.criado_em,
    }