from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria uma conexão com o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./dados.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
