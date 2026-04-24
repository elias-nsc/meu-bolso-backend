from mongoengine import Document, StringField, DateTimeField, FloatField, IntField, ObjectIdField, ListField, DictField, connect
from datetime import datetime
from app.config import MONGO_URI


def init_db():
    connect(host=MONGO_URI)


class User(Document):
    nome = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    senha_hash = StringField()
    google_id = StringField(unique=True, sparse=True)
    foto_url = StringField()
    ganhos = ListField(DictField())
    criado_em = DateTimeField(default=datetime.utcnow)
 
    meta = {
        "collection": "users",
        "indexes": ["email", "google_id"]
    }
 

class Despesa(Document):
    user_id = ObjectIdField(required=True)
    descricao = StringField(required=True, max_length=200)
    categoria = StringField(required=True)
    tipo_gasto = StringField(required=True, choices=('fixo', 'variavel'))
    forma_pagamento = StringField(required=True, choices=('credito', 'debito', 'dinheiro', 'pix'))
    valor_total = FloatField(required=True, min_value=0.01)
    total_parcelas = IntField(required=True, min_value=1, max_value=12)
    valor_parcela = FloatField(required=True, min_value=0.01)
    data_primeira_parcela = DateTimeField(required=True)
    dia_vencimento = IntField(required=True, min_value=1, max_value=31)
    criado_em = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'despesas',
        'indexes': ['user_id', 'categoria', 'tipo_gasto']
    }

    def __repr__(self):
        return f"<Despesa {self.descricao}>"