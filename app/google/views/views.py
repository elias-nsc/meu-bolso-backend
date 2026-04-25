import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.google.controller.controller import (
    get_google_auth_url,
    google_login_or_register,
)

router = APIRouter(prefix="/auth", tags=["Google OAuth2"])


@router.get("/google", summary="Iniciar login com Google")
def login_google():
    url = get_google_auth_url()
    return RedirectResponse(url=url)


@router.get("/google/callback", summary="Callback do Google OAuth2")
async def google_callback(code: str):
    try:
        result = await google_login_or_register(code=code)
        token   = result["access_token"]
        user_id = result["user_id"]
        nome    = result["nome"]

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        redirect_url = (
            f"{frontend_url}/auth/google/callback"
            f"?token={token}&user_id={user_id}&nome={nome}"
        )
        return RedirectResponse(url=redirect_url)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no callback do Google: {str(e)}",
        )