import re
from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import conexion

formularios_bp = Blueprint("formularios", __name__, url_prefix="/api")
CORREO = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def datos():
    return request.get_json(silent=True) or {}


def error(mensaje, codigo=400):
    return jsonify(ok=False, error=mensaje), codigo


@formularios_bp.post("/contacto")
def contacto():
    d = datos()
    nombre, correo = str(d.get("nombre", "")).strip(), str(d.get("correo", "")).strip()
    asunto, mensaje = str(d.get("asunto", "")).strip(), str(d.get("mensaje", "")).strip()
    if not nombre or not asunto or not CORREO.match(correo) or len(mensaje) < 10:
        return error("Revisa los campos del formulario.")
    with conexion(current_app) as con:
        con.execute(
            "INSERT INTO mensajes (nombre, correo, asunto, mensaje) VALUES (?,?,?,?)",
            (nombre, correo, asunto, mensaje),
        )
    return jsonify(ok=True)


@formularios_bp.post("/registro")
def registro():
    d = datos()
    nombre, correo = str(d.get("nombre", "")).strip(), str(d.get("correo", "")).strip().lower()
    clave = str(d.get("clave", ""))
    if not nombre or not CORREO.match(correo) or not clave:
        return error("Completa todos los campos.")
    try:
        with conexion(current_app) as con:
            con.execute(
                "INSERT INTO usuarios (nombre, correo, clave_hash) VALUES (?,?,?)",
                (nombre, correo, generate_password_hash(clave)),
            )
    except Exception:
        return error("Ese correo ya está registrado.", 409)
    return jsonify(ok=True)


@formularios_bp.post("/login")
def login():
    d = datos()
    usuario, clave = str(d.get("usuario", "")).strip().lower(), str(d.get("clave", ""))
    with conexion(current_app) as con:
        fila = con.execute(
            "SELECT * FROM usuarios WHERE correo = ? OR lower(nombre) = ?", (usuario, usuario)
        ).fetchone()
    if not fila or not check_password_hash(fila["clave_hash"], clave):
        return error("Usuario o contraseña incorrectos.", 401)
    session["usuario_id"] = fila["id"]
    return jsonify(ok=True, nombre=fila["nombre"])
