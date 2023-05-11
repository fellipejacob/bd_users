import uvicorn
from bd_users.routes.routes import app
from bd_users.database.models.user import Base, engine


# Iniciar o servidor
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
