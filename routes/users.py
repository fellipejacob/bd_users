from services.user_services import user_services
from database.models.repository import get_db
from database.models.user import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from configs.core import app


# Cria uma instância da aplicação FastAPI
class Users:
    def __int__(self):
        pass

    @staticmethod
    def apply():
        @app.get("/users", tags=["Users"])
        def read_root(db: Session = Depends(get_db)):
            db_users = db.query(User).all()
            return db_users

        # Create
        @app.post("/users/", tags=["CRUD"])
        def create_new_user(name: str,
                            cpf: str,
                            password: str,
                            db: Session = Depends(get_db)):
            """Create a new user using your document:"""
            db_user = user_services.get_user_by_cpf(db, cpf=cpf)
            if db_user:
                raise HTTPException(status_code=400,
                                    detail="User already registered")
            return user_services.create_user(db=db, name=name, cpf=cpf, password=password)

        # Read
        @app.get("/users/{user_id}", tags=["CRUD"])
        def read_user(cpf: str, db: Session = Depends(get_db)):
            """How may I look up your record? Please enter your document."""
            user = user_services.get_user_by_cpf(db, cpf=cpf)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user

        # Update
        # First, search by document, and then the update, if possible
        @app.put("/users/{user_cpf}", tags=["CRUD"])
        def update_user(user_cpf: str, name: str = None, password: str = None,
                        db: Session = Depends(get_db)):
            db_user = user_services.update_user_by_cpf(db, cpf=user_cpf, name=name, password=password)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user

        # Delete
        @app.delete("/users/{user_id}", tags=["CRUD"])
        def delete_user(cpf: str,
                        db: Session = Depends(get_db)):
            """Please enter the registered document number you wish to delete."""
            db_user = user_services.get_user_by_cpf(db, cpf=cpf)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            user_services.remove_user(db=db, user=db_user)
            return {"message": "User deleted"}


users = Users()
