from fastapi import FastAPI
from usuarios.routes import router
from database.cnx import engine
from database.database import Base


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(router)




