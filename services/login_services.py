import hashlib
import jwt
from datetime import datetime, timedelta
from jwt import decode, PyJWTError
from fastapi import HTTPException


class AuthService:
    def __init__(self):
        self.SECRET_KEY = "mysecretkey"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 1

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifica se a senha informada corresponde à senha armazenada no banco de dados"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password

    # Gerar o token JWT
    def get_token(self, user_id: int):
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data = {"user_id": user_id, "exp": datetime.utcnow() + access_token_expires}
        access_token = jwt.encode(payload=access_token_data, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return access_token

    def verify_token(self, token: str):
        try:
            decoded_token = decode(token, key=self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = decoded_token.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except Exception as er:
            print(er)
            raise HTTPException(status_code=401, detail="Invalid token")


auth_service = AuthService()
