from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', cpf='{self.cpf}')>"


# Funções de CRUD
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_cpf(db: Session, cpf: str):
    return db.query(User).filter(User.cpf == cpf).first()


def create_user(db: Session, name: str, cpf: str, password: str):
    db_user = User(name=name, cpf=cpf, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
