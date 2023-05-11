import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from models import create_user, get_user_by_cpf

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
# Default Route
@app.get("/users")
def read_root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# Create
@app.post("/users/")
def create_new_user(name: str, cpf: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db, cpf=cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, name=name, cpf=cpf, password=password)


# Read
@app.get("/users/{user_id}")
def read_user(cpf: str, db: Session = Depends(get_db)):
    user = get_user_by_cpf(db, cpf=cpf)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update
@app.put("/users/{user_id}")
def update_user(name: str, cpf: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db, cpf=cpf)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user_db(db=db, user=db_user, name=name, cpf=cpf, password=password)
    return jsonable_encoder(updated_user)


def update_user_db(db: Session, user: User, name: str, cpf: str, password: str):
    user.name = name
    user.cpf = cpf
    user.password = password
    db.commit()
    db.refresh(user)
    return user


# Delete
@app.delete("/users/{user_id}")
def delete_user(cpf: str, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db, cpf=cpf)
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
