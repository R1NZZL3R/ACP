from flask import Flask

def create_app():
    app = Flask(__name__)

    # Blueprints / rutas se registran aca a medida que se van creando
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    return app
