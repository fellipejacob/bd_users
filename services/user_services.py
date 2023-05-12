from sqlalchemy.orm import Session
from database.models.user import User
import hashlib


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserServices:
    def __init__(self):
        pass

    # Função de banco de dados para buscar o usuário por ID
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # Função de banco de dados para buscar o usuário por CPF
    @staticmethod
    def get_user_by_cpf(db: Session, cpf: str):
        return db.query(User).filter(User.cpf == cpf).first()

    # Função de banco de dados para criar o usuário
    @staticmethod
    def create_user(db: Session, name: str, cpf: str, password: str):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db_user = User(name=name, cpf=cpf, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"user": db_user.name, "user_cpf": db_user.cpf}

    # Função de banco de dados para atualizar o usuário
    @staticmethod
    def update_user_by_cpf(db: Session, cpf: str, name: str = None,
                           password: str = None):
        db_user = db.query(User).filter(User.cpf == cpf).first()
        if db_user:
            if name is not None:
                db_user.name = name
            if password is not None:
                hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
        return {"user": db_user.name, "user_cpf": db_user.cpf, "password": db_user.password}

    # Função de banco de dados para remover o usuário
    @staticmethod
    def remove_user(db: Session, user: User):
        db.delete(user)
        db.commit()


user_services = UserServices()
