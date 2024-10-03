from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configurações do Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/barbearia_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização do banco de dados e migrações
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rotas (importadas de outro arquivo)
    from app import routes
    app.register_blueprint(routes.bp)

    return app
