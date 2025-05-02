from fastapi import APIRouter
from fastapi import HTTPException
from .dto import Usuario
from . import service

router = APIRouter()

# Obtener todos los usuarios
@router.get("/usuarios")
def obtener_usuarios():
    return service.obtener_usuarios()

# Obtener un usuario por su ID
@router.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = service.obtener_usuario(usuario_id)
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")    

# Crear un nuevo usuario
@router.post("/usuarios")
def crear_usuario(usuario: Usuario):
    nuevo_usuario = service.crear_usuario(usuario)
    return nuevo_usuario

# Actualizar un usuario existente
@router.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario):
    usuario_actualizado = service.actualizar_usuario(usuario_id, usuario)
    if usuario_actualizado:
        return usuario_actualizado
    return {"error": "Usuario no encontrado"}

# Eliminar un usuario
@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    resultado = service.eliminar_usuario(usuario_id)
    if resultado:
        return {"mensaje": f"Usuario {usuario_id} eliminado correctamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

