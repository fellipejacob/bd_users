from sqlalchemy import Integer, Column, String
from database.models.repository import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', cpf='{self.cpf}')>"
