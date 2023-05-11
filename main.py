import uvicorn
from routes.routes import users, app
from database.models.user import Base, engine

routes = [users]
for route in routes:
    route.apply()

# Iniciar o servidor
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=7000)
