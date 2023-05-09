import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from models import get_user_by_email, create_user, get_user, User

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
# Create
@app.post("/users/")
def create_new_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, name=name, email=email, password=password)


# Read
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user_db(db=db, user=db_user, name=name, email=email, password=password)
    return jsonable_encoder(updated_user)


def update_user_db(db: Session, user: User, name: str, email: str, password: str):
    user.name = name
    user.email = email
    user.password = password
    db.commit()
    db.refresh(user)
    return user


# Delete
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    remove_user(db=db, user=db_user)
    return {"message": "User deleted"}


# Função de banco de dados para remover o usuário
def remove_user(db: Session, user: User):
    db.delete(user)
    db.commit()


# Iniciar o servidor
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
