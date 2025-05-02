from database.cnx import SessionLocal
from .entity import UsuarioEntity
from .dto import Usuario

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los usuarios de la base de datos
def obtener_usuarios():
    db = SessionLocal()
    usuarios = db.query(UsuarioEntity).all()
    db.close()
    return usuarios

# Obtener un solo usuario por su ID
def obtener_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(UsuarioEntity).filter(UsuarioEntity.id == usuario_id).first()
    db.close()
    return usuario

# Crear un nuevo usuario
def crear_usuario(usuario: Usuario):
    db = SessionLocal()
    nuevo_usuario = UsuarioEntity(
        nombre=usuario.nombre,
        edad=usuario.edad,
        email=usuario.email
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # Para traer el nuevo ID
    db.close()
    return nuevo_usuario

# Actualizar un usuario existente
def actualizar_usuario(usuario_id: int, usuario_actualizado: Usuario):
    db = SessionLocal()
    usuario = db.query(UsuarioEntity).filter(UsuarioEntity.id == usuario_id).first()
    if usuario:
        usuario.nombre = usuario_actualizado.nombre
        usuario.edad = usuario_actualizado.edad
        usuario.email = usuario_actualizado.email
        db.commit()
        db.refresh(usuario)
        db.close()
        return usuario
    db.close()
    return None

# Eliminar un usuario
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(UsuarioEntity).filter(UsuarioEntity.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        db.close()
        return {"mensaje": f"Usuario con id {usuario_id} eliminado correctamente."}
    db.close()
    return None

