import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://elias_nogueira:@mazonas2026@meu-bolso.crzok4j.mongodb.net/")

JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "TROQUE_POR_UM_SEGREDO_FORTE")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI","http://localhost:8000/auth/google/callback")