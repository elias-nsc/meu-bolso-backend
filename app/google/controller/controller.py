import httpx
from urllib.parse import urlencode
from fastapi import HTTPException, status
from app.models.models import User
from app.user.controller.controller import create_access_token
from app.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_google_auth_url() -> str:
    """Monta a URL de redirecionamento para o Google com encoding correto."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> dict:
    """Troca o code retornado pelo Google por access_token + id_token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Falha ao trocar o code: {response.text}",
        )
    return response.json()


async def get_google_user_info(access_token: str) -> dict:
    """Busca os dados do usuário no Google (nome, email, foto, sub)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Falha ao buscar dados do usuário no Google: {response.text}",
        )
    return response.json()


async def google_login_or_register(code: str) -> dict:
    token_data = await exchange_code_for_token(code)
    access_token_google = token_data.get("access_token")

    user_info = await get_google_user_info(access_token_google)

    google_id = user_info.get("sub")
    email = user_info.get("email")
    nome = user_info.get("name", email)
    foto_url = user_info.get("picture", "")

    if not email or not google_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível obter e-mail do Google.",
        )

    user = User.objects(email=email).first()

    if user:
        if not user.google_id:
            user.google_id = google_id
            user.foto_url = foto_url
            user.save()
    else:
        user = User(
            nome=nome,
            email=email,
            google_id=google_id,
            foto_url=foto_url,
        )
        user.save()

    # Gera token JWT incluindo o user_id
    jwt_token = create_access_token({
        "sub": email,
        "user_id": str(user.id)          # <-- ID do usuário salvo em cookie
    })

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
    }