"""Application factory untuk Task Manager API."""
from flask import Flask

from .config import Config
from .routes import create_blueprint
from .storage import TaskStorage


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    storage = TaskStorage(max_tasks=app.config["MAX_TASKS"])
    app.register_blueprint(create_blueprint(storage))
    return app
