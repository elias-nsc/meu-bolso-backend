from fastapi import HTTPException, status
from bson import ObjectId
from app.models.models import Despesa, User
from app.user.controller.controller import get_current_user 

def criar_despesa(despesa_data: dict, user_id: str) -> dict:
    """Cria uma nova despesa associada ao user_id"""
    despesa = Despesa(
        user_id=ObjectId(user_id),
        **despesa_data
    )
    despesa.save()
    return {
        "id": str(despesa.id),
        "user_id": str(despesa.user_id),
        "descricao": despesa.descricao,
        "categoria": despesa.categoria,
        "tipo_gasto": despesa.tipo_gasto,
        "forma_pagamento": despesa.forma_pagamento,
        "valor_total": despesa.valor_total,
        "total_parcelas": despesa.total_parcelas,
        "valor_parcela": despesa.valor_parcela,
        "data_primeira_parcela": despesa.data_primeira_parcela,
        "dia_vencimento": despesa.dia_vencimento,
        "criado_em": despesa.criado_em,
    }

def listar_despesas(user_id: str) -> list:
    """Retorna todas as despesas do usuário"""
    despesas = Despesa.objects(user_id=ObjectId(user_id)).order_by('-criado_em')
    return [
        {
            "id": str(d.id),
            "user_id": str(d.user_id),
            "descricao": d.descricao,
            "categoria": d.categoria,
            "tipo_gasto": d.tipo_gasto,
            "forma_pagamento": d.forma_pagamento,
            "valor_total": d.valor_total,
            "total_parcelas": d.total_parcelas,
            "valor_parcela": d.valor_parcela,
            "data_primeira_parcela": d.data_primeira_parcela,
            "dia_vencimento": d.dia_vencimento,
            "criado_em": d.criado_em,
        }
        for d in despesas
    ]

def deletar_despesa(despesa_id: str, user_id: str) -> None:
    """Deleta uma despesa somente se pertencer ao usuário"""
    try:
        despesa = Despesa.objects(id=ObjectId(despesa_id), user_id=ObjectId(user_id)).first()
        if not despesa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Despesa não encontrada ou não pertence ao usuário."
            )
        despesa.delete()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de despesa inválido."
        )