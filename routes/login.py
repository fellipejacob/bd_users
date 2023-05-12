from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from services.login_services import auth_service
from database.models.repository import get_db
from services.user_services import user_services
from configs.core import app


class Login:
    def __init__(self):
        pass

    @staticmethod
    def apply():
        @app.post("/login", tags=["Login"])
        def user_login(cpf: str, password: str, db: Session = Depends(get_db)):
            user = user_services.get_user_by_cpf(db, cpf=cpf)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid CPF or password")
            if not auth_service.verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="Invalid CPF or password")
            token = auth_service.get_token(user_id=user.id)
            return {"token": token}

        @app.post("/verify_token", tags=["Verify Token"])
        def read_users_token(user_id: int = Depends(auth_service.verify_token)):
            """
            Retorna as informações do usuário logado
            """
            return {"user_id": user_id}


login = Login()
