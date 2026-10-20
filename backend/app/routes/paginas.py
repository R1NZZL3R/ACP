import os
from flask import Blueprint, abort, send_from_directory

FRONTEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend"))

paginas_bp = Blueprint("paginas", __name__)

# ruta pública -> archivo html
RUTAS = {
    "": "index.html",
    "caracteristicas": "caracteristicas.html",
    "como-funciona": "como-funciona.html",
    "tecnologias": "tecnologias.html",
    "documentacion": "documentacion.html",
    "acerca-de": "acerca-de.html",
    "contacto": "contacto.html",
    "login": "login.html",
    "privacidad": "privacidad.html",
    "terminos": "terminos.html",
}


@paginas_bp.route("/", defaults={"ruta": ""})
@paginas_bp.route("/<path:ruta>")
def pagina(ruta):
    ruta = ruta.strip("/")
    if ruta in RUTAS:
        return send_from_directory(FRONTEND, RUTAS[ruta])
    # css, js, assets
    if ruta.split("/")[0] in ("css", "js", "assets"):
        return send_from_directory(FRONTEND, ruta)
    abort(404)
