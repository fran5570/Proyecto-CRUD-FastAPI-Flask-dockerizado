from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)


API_URL = os.getenv("BACKEND_URL", "http://backend:8000") + "/usuarios"

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/usuarios")
def ver_usuarios():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        usuarios = response.json()
        return render_template("usuarios.html", usuarios=usuarios, mostrar_usuarios=True)
    except Exception as e:
        return f"Error al obtener usuarios: {e}"

@app.route("/consultar-id")
def mostrar_formulario_id():
    return render_template("usuarios.html", mostrar_formulario_id=True)

@app.route("/consultar")
def consultar_usuario():
    usuario_id = request.args.get("usuario_id")
    if not usuario_id:
        return render_template("usuarios.html", error_consulta="Debe ingresar un ID")
    
    try:
        response = requests.get(f"{API_URL}/{usuario_id}")
        data = response.json()
        if "error" in data:
            return render_template("usuarios.html", error_consulta=data["error"])
        return render_template("usuarios.html", usuario_consultado=data)
    except Exception as e:
        return render_template("usuarios.html", error_consulta=f"Error de conexión: {e}")

@app.route('/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        data = {
            "nombre": request.form['nombre'],
            "edad": int(request.form['edad']),
            "email": request.form['email']
        }
        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            return redirect('/usuarios')
        except Exception as e:
            return f"Error al crear usuario: {e}"
    return render_template('crear.html')

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    try:
        response = requests.delete(f"{API_URL}/{id}")
        if response.status_code == 200:
            return redirect('/usuarios')
        else:
            return f"Error al eliminar usuario ({response.status_code})"
    except Exception as e:
        return f"Error al eliminar usuario: {e}"

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        data = {
            "nombre": request.form["nombre"],
            "edad": int(request.form["edad"]),
            "email": request.form["email"]
        }
        try:
            response = requests.put(f"{API_URL}/{id}", json=data)
            response.raise_for_status()
            return redirect("/usuarios")
        except Exception as e:
            return f"Error al actualizar usuario: {e}"

    try:
        response = requests.get(f"{API_URL}/{id}")
        if response.status_code == 200:
            usuario = response.json()
            return render_template("editar.html", usuario=usuario)
        else:
            return f"Error: Usuario no encontrado ({response.status_code})"
    except Exception as e:
        return f"Error al obtener usuario: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
