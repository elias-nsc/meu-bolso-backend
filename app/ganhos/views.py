from fastapi import APIRouter, Depends
from app.ganhos.controller import upsert_ganhos, deletar_ganho_por_tipo, deletar_todos_ganhos, listar_ganhos
from app.ganhos.types import GanhosUpsertRequest, GanhosResponse, MensagemResponse
from app.user.controller.controller import get_current_user
from app.models.models import User

router = APIRouter(prefix="/ganhos", tags=["Ganhos"])

@router.put("/", response_model=GanhosResponse, summary="Adicionar ou atualizar ganhos")
def upsert_ganhos_endpoint(
    payload: GanhosUpsertRequest,
    current_user: User = Depends(get_current_user)
):
    """Recebe uma lista de ganhos (type + valor). Se o type já existe, atualiza; senão, adiciona."""
    ganhos_dicts = [item.dict() for item in payload.ganhos]
    novos_ganhos = upsert_ganhos(str(current_user.id), ganhos_dicts)
    return {"ganhos": novos_ganhos}

@router.delete("/{tipo}", response_model=GanhosResponse, summary="Remover um tipo de ganho")
def remover_ganho_por_tipo(
    tipo: str,
    current_user: User = Depends(get_current_user)
):
    """Remove um ganho específico pelo seu type."""
    ganhos_restantes = deletar_ganho_por_tipo(str(current_user.id), tipo)
    return {"ganhos": ganhos_restantes}

@router.delete("/", response_model=MensagemResponse, summary="Remover todos os ganhos")
def remover_todos_ganhos(current_user: User = Depends(get_current_user)):
    """Remove todos os ganhos do usuário."""
    deletar_todos_ganhos(str(current_user.id))
    return {"message": "Todos os ganhos foram removidos"}

@router.get("/", response_model=GanhosResponse, summary="Listar ganhos do usuário")
def listar_ganhos_endpoint(current_user: User = Depends(get_current_user)):
    ganhos = listar_ganhos(str(current_user.id))
    return {"ganhos": ganhos}