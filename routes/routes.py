from bd_users.database.models.repository import create_user, get_user_by_cpf, get_db, update_user_db, remove_user
from bd_users.database.models.user import User
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session


# Cria uma instância da aplicação FastAPI
app = FastAPI()


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
        raise HTTPException(status_code=400, detail="User already registered")
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


# Delete
@app.delete("/users/{user_id}")
def delete_user(cpf: str, db: Session = Depends(get_db)):
    db_user = get_user_by_cpf(db, cpf=cpf)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    remove_user(db=db, user=db_user)
    return {"message": "User deleted"}
