import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.google.controller.controller import (
    get_google_auth_url,
    google_login_or_register,
)

router = APIRouter(prefix="/auth", tags=["Google OAuth2"])

# Guarda codes já processados para evitar dupla requisição
_used_codes: set = set()


@router.get("/google", summary="Iniciar login com Google")
def login_google():
    """
    Redireciona o usuário para a tela de login do Google.
    Teste abrindo diretamente no navegador: http://localhost:8000/auth/google
    """
    url = get_google_auth_url()
    return RedirectResponse(url=url)


@router.get("/google/callback", summary="Callback do Google OAuth2")
async def google_callback(code: str):
    if code in _used_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código já utilizado."
        )

    _used_codes.add(code)
    try:
        result = await google_login_or_register(code=code)
        token = result["access_token"]

        # ✅ Lê a URL do frontend da variável de ambiente
        # No túnel, defina: FRONTEND_URL=https://0d3okc.instatunnel.my
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        redirect_url = f"{frontend_url}/auth/google/callback?token={token}"
        return RedirectResponse(url=redirect_url)

    except Exception:
        _used_codes.discard(code)
        raise