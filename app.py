# Importamos todas las librerías que necesitamos para nuestro backend
from flask import Flask, jsonify, request
from flask_cors import (
    CORS,
)  # Para permitir que el frontend se conecte desde otro puerto
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
)  # Para crear sesiones y modelos
from passlib.hash import bcrypt  # Para encriptar contraseñas de forma segura
import os, re  # os para variables de entorno, re para validar emails

# --- Configuración de Base de Datos ----------------------------------------------------

# Aquí obtenemos la URL de conexión a PostgreSQL desde las variables de entorno
# Si no existe, usamos una por defecto para desarrollo local
URL_BD = os.getenv(
    "URL_BD", "postgresql+psycopg2://dev:devpass@localhost:5432/bd_registro"
)

# Creamos el "motor" que se conecta a la base de datos
# echo=True hace que veamos todas las consultas SQL en la consola (útil para aprender)
motor = create_engine(URL_BD, echo=True)

# Creamos una "fábrica" de sesiones para interactuar con la BD
SesionLocal = sessionmaker(bind=motor)


# Esta es la clase base para todos nuestros modelos de datos
class Base(DeclarativeBase):
    pass


# Definimos nuestro modelo Usuario - esto se convierte en una tabla
class Usuario(Base):
    __tablename__ = "usuarios"  # Nombre de la tabla en PostgreSQL
    id = Column(Integer, primary_key=True)  # ID único que se auto-incrementa
    nombre = Column(String(120), nullable=False)  # Nombre del usuario, obligatorio
    correo = Column(String(120), unique=True, index=True)
    contrasena_hash = Column(String(255))


# Esto crea automáticamente la tabla si no existe
Base.metadata.create_all(motor)

app = Flask(__name__)

# CORS permite que nuestro frontend (React en puerto 3000) se conecte a nuestro backend
# Sin esto, el navegador bloquearía las peticiones por seguridad
CORS(app, origins=["http://localhost:3000"])

# Expresión regular para validar que un email tenga formato válido
# Busca: algo@algo.algo (versión simplificada pero funcional)
REGEX_CORREO = re.compile(r"[^@]+@[^@]+\.[^@]+")


# Ruta para crear un nuevo usuario (POST /usuarios)
@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    # Obtenemos los datos JSON que envía el frontend
    datos = request.get_json() or {}
    # Extraemos y limpiamos los datos
    nombre = datos.get("nombre", "").strip()
    correo = datos.get("correo", "").strip()
    contrasena = datos.get("contrasena", "")

    # Validaciones básicas antes de guardar en la BD

    # Verificamos que todos los campos estén presentes
    if not (nombre and correo and contrasena):
        return jsonify({"detalle": "Faltan campos"}), 400
    if not REGEX_CORREO.match(correo):
        return jsonify({"detalle": "Correo inválido"}), 400
    # La contraseña debe tener al menos 6 caracteres
    if len(contrasena) < 6:
        return jsonify({"detalle": "Contraseña muy corta"}), 400

    # Usamos 'with' para manejar la sesión de BD automáticamente
    with SesionLocal() as bd:
        # Verificamos si ya existe un usuario con ese email
        if bd.query(Usuario).filter_by(correo=correo).first():
            return jsonify({"detalle": "Correo ya registrado"}), 400
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contrasena_hash=bcrypt.hash(contrasena),  # Aquí encriptamos la contraseña
        )
        # Guardamos en la base de datos
        bd.add(usuario)  # Añadimos a la sesión
        bd.commit()  # Confirmamos los cambios
        bd.refresh(usuario)  # Obtenemos el ID generado automáticamente
        # Devolvemos los datos del usuario creado, sin la contraseña
        return (
            jsonify(
                {"id": usuario.id, "nombre": usuario.nombre, "correo": usuario.correo}
            ),
            201,  # Código HTTP 201 significa "creado exitosamente"
        )


# Ruta para obtener todos los usuarios (GET /usuarios)
@app.get("/usuarios")
def listar_usuarios():
    with SesionLocal() as bd:
        # Obtenemos todos los usuarios de la base de datos
        usuarios = bd.query(Usuario).all()

        # Convertimos cada usuario a diccionario (sin contraseñas)
        # Esta es una "list comprehension" - forma compacta de crear listas
        return jsonify(
            [{"id": u.id, "nombre": u.nombre, "correo": u.correo} for u in usuarios]
        )


# Esta línea hace que el servidor solo se ejecute si corremos este archivo directamente
if __name__ == "__main__":
    # Iniciamos el servidor Flask
    # host="0.0.0.0" permite conexiones desde cualquier IP
    # port=5000 es el puerto donde escucha nuestro backend
    # debug=True reinicia automáticamente cuando cambiamos código
    app.run(host="0.0.0.0", port=5000, debug=True)
