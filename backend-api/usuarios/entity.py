from sqlalchemy import Column, Integer, String
from database.database import Base


class UsuarioEntity(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer)
    email = Column(String, unique=True, index=True)
