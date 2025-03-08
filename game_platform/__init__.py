from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from game_platform.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from game_platform.routes.auth import auth_bp
    from game_platform.routes.items import items_bp
    from game_platform.routes.tasks import tasks_bp
    from game_platform.routes.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(transactions_bp)

    return app
