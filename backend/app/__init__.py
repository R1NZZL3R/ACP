import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambiar-en-env")
    app.config["DB_PATH"] = os.environ.get(
        "DB_PATH", os.path.join(os.path.dirname(__file__), "..", "acp.db")
    )

    from app.db import iniciar_db
    iniciar_db(app)

    from app.routes.paginas import paginas_bp
    from app.routes.formularios import formularios_bp
    app.register_blueprint(paginas_bp)
    app.register_blueprint(formularios_bp)

    return app
