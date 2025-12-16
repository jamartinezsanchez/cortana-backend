from fastapi import HTTPException, Header
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    token = authorization.replace("Bearer ", "")

    user_response = supabase.auth.get_user(token)

    if user_response.error:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    return user_response.data.user
