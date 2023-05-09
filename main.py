import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from models import get_user_by_email

# Cria uma conexão com o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./dados.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Cria uma instância da aplicação FastAPI
app = FastAPI()


# Funções de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rotas
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/users/")
async def create_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, name=name, email=email, password=password)


# Iniciar o servidor
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
