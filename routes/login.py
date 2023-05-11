from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from services.login_services import verify_password
from database.models.repository import get_db
from services.user_services import user_services
from configs.core import app


class Login:
    def __init__(self):
        pass

    @staticmethod
    def apply():
        @app.post("/login")
        def user_login(cpf: str, password: str, db: Session = Depends(get_db)):
            user = user_services.get_user_by_cpf(db, cpf=cpf)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid CPF or password")
            if not verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="Invalid CPF or password")
            return {"cpf": user.cpf, "name": user.name}


login = Login()
