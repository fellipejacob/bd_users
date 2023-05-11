from sqlalchemy.orm import Session
from database.models.user import User


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
        db_user = User(name=name, cpf=cpf, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    # Função de banco de dados para atualizar o usuário
    @staticmethod
    def update_user_by_cpf(db: Session, cpf: str, name: str = None,
                           password: str = None):
        db_user = db.query(User).filter(User.cpf == cpf).first()
        if db_user:
            if name is not None:
                db_user.name = name
            if password is not None:
                db_user.password = password
            db.commit()
            db.refresh(db_user)
        return db_user

    # Função de banco de dados para remover o usuário
    @staticmethod
    def remove_user(db: Session, user: User):
        db.delete(user)
        db.commit()


user_services = UserServices()
