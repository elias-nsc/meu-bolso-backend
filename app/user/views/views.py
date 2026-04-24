from fastapi import APIRouter, Body, Depends, Path
from app.user.controller.controller import cadastrar_usuario, login_usuario, get_usuario_por_id, get_current_user
from app.user.types import CadastroSchema, LoginSchema, TokenResponse, UserResponse
from app.models.models import User

router = APIRouter(prefix="/user", tags=["User"])

@router.post( "/cadastro", response_model=TokenResponse, status_code=201, summary="Cadastrar novo usuário")
def cadastro(body: CadastroSchema = Body(...)):
    return cadastrar_usuario(nome=body.nome, email=body.email, senha=body.senha)

@router.post("/login", response_model=TokenResponse, summary="Autenticar usuário")
def login(body: LoginSchema = Body(...)):
    return login_usuario(email=body.email, senha=body.senha)

@router.get("/{user_id}", response_model=UserResponse, summary="Obter dados do próprio usuário")
def get_user(
    user_id: str = Path(..., description="ID do usuário a ser consultado"),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna os dados do usuário correspondente ao ID.
    Apenas o próprio usuário pode acessar seus dados.
    """
    return get_usuario_por_id(user_id, current_user)