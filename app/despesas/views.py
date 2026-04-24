from fastapi import APIRouter, Depends, HTTPException, status
from app.despesas.controller import criar_despesa, listar_despesas, deletar_despesa
from app.despesas.types import DespesaCreateSchema, DespesaResponseSchema, DespesaDeleteResponse
from app.user.controller.controller import get_current_user
from app.models.models import User

router = APIRouter(prefix="/despesas", tags=["Despesas"])

@router.post("/", response_model=DespesaResponseSchema, status_code=status.HTTP_201_CREATED)
def adicionar_despesa(
    despesa: DespesaCreateSchema,
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova despesa para o usuário autenticado"""
    user_id = str(current_user.id)
    nova_despesa = criar_despesa(despesa.dict(), user_id)
    return nova_despesa

@router.get("/", response_model=list[DespesaResponseSchema])
def obter_despesas(current_user: User = Depends(get_current_user)):
    """Retorna todas as despesas do usuário autenticado"""
    user_id = str(current_user.id)
    return listar_despesas(user_id)

@router.delete("/{despesa_id}", response_model=DespesaDeleteResponse)
def remover_despesa(
    despesa_id: str,
    current_user: User = Depends(get_current_user)
):
    """Deleta uma despesa específica do usuário autenticado"""
    user_id = str(current_user.id)
    deletar_despesa(despesa_id, user_id)
    return {"message": "Despesa removida com sucesso"}