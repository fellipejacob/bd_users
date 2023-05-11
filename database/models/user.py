from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria uma conexão com o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./dados.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', cpf='{self.cpf}')>"
