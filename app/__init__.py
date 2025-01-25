from flask import Flask
from app.db import init_db
from app.models import close_db
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.json.sort_keys = False

    # Initialize the database
    with app.app_context():
        init_db()

    # Register the routes
    from app.routes import register_routes
    register_routes(app)

    app.teardown_appcontext(close_db)

    return app