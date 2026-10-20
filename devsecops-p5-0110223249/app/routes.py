"""Endpoint REST API Task Manager."""
from flask import Blueprint, current_app, jsonify, request

from .storage import StorageFullError
from .validators import parse_bool_param, validate_task_payload


def create_blueprint(storage):
    bp = Blueprint("tasks", __name__)

    def _limits():
        cfg = current_app.config
        return cfg["MAX_TITLE_LENGTH"], cfg["MAX_DESCRIPTION_LENGTH"]

    @bp.get("/")
    def index():
        return jsonify(
            {
                "app": "Task Manager API",
                "version": "1.0.0",
                "endpoints": ["/health", "/tasks", "/tasks/stats"],
            }
        )

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @bp.get("/tasks")
    def list_tasks():
        done = parse_bool_param(request.args.get("done"))
        return jsonify([t.to_dict() for t in storage.list(done=done)])

    @bp.get("/tasks/stats")
    def task_stats():
        return jsonify(storage.stats())

    @bp.post("/tasks")
    def create_task():
        max_title, max_desc = _limits()
        cleaned, errors = validate_task_payload(
            request.get_json(silent=True), max_title, max_desc
        )
        if errors:
            return jsonify({"errors": errors}), 400
        try:
            task = storage.add(cleaned["title"], cleaned.get("description", ""))
        except StorageFullError as exc:
            return jsonify({"errors": [str(exc)]}), 507
        return jsonify(task.to_dict()), 201

    @bp.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = storage.get(task_id)
        if task is None:
            return jsonify({"errors": ["Task tidak ditemukan"]}), 404
        return jsonify(task.to_dict())

    @bp.put("/tasks/<int:task_id>")
    def update_task(task_id):
        max_title, max_desc = _limits()
        cleaned, errors = validate_task_payload(
            request.get_json(silent=True), max_title, max_desc, partial=True
        )
        if errors:
            return jsonify({"errors": errors}), 400
        task = storage.update(task_id, **cleaned)
        if task is None:
            return jsonify({"errors": ["Task tidak ditemukan"]}), 404
        return jsonify(task.to_dict())

    @bp.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        if not storage.delete(task_id):
            return jsonify({"errors": ["Task tidak ditemukan"]}), 404
        return "", 204

    return bp
