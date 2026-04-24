from fastapi import HTTPException, status
from bson import ObjectId
from app.models.models import User
from typing import List, Dict

def upsert_ganhos(user_id: str, ganhos_items: List[Dict]) -> List[Dict]:
    user = User.objects(id=ObjectId(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    ganhos_atual = list(user.ganhos) if user.ganhos else []
    
    for novo in ganhos_items:
        tipo = novo.get("type")
        valor = novo.get("valor")
        encontrado = False
        for i, item in enumerate(ganhos_atual):
            if item.get("type") == tipo:
                ganhos_atual[i]["valor"] = valor
                encontrado = True
                break
        if not encontrado:
            ganhos_atual.append({"type": tipo, "valor": valor})
    
    user.ganhos = ganhos_atual
    user.save()
    return ganhos_atual

def deletar_ganho_por_tipo(user_id: str, tipo: str) -> List[Dict]:
    user = User.objects(id=ObjectId(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    ganhos_atual = list(user.ganhos) if user.ganhos else []
    novos_ganhos = [item for item in ganhos_atual if item.get("type") != tipo]
    
    if len(novos_ganhos) == len(ganhos_atual):
        raise HTTPException(status_code=404, detail=f"Tipo '{tipo}' não encontrado")
    
    user.ganhos = novos_ganhos
    user.save()
    return novos_ganhos

def deletar_todos_ganhos(user_id: str) -> None:
    user = User.objects(id=ObjectId(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.ganhos = []
    user.save()

def listar_ganhos(user_id: str) -> List[Dict]:
    user = User.objects(id=ObjectId(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return list(user.ganhos) if user.ganhos else []