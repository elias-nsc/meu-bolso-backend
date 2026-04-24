from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.user.views.views import router as user_router
from app.google.views.views import router as google_router
from app.despesas.views import router as despesas_router   
from app.ganhos.views import router as ganhos_router
from app.models.models import init_db

tags_metadata = [
    {"name": "User", "description": "Cadastro e autenticação de usuários."},
    {"name": "Google OAuth2", "description": "Login e cadastro via conta Google."},
    {"name": "Despesas", "description": "Gerenciamento de despesas do usuário."},
    {"name": "Ganhos", "description": "Gerenciamento de ganhos/salários do usuário."},
]

app = FastAPI(
    title="meu-bolso-backend",
    description="Seu resumo financeiro",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(user_router)
app.include_router(google_router)
app.include_router(despesas_router)  
app.include_router(ganhos_router)