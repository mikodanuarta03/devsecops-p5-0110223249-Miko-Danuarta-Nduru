import pytest

from app import create_app
from app.storage import StorageFullError, TaskStorage
from app.validators import parse_bool_param, validate_task_payload


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["app"] == "Task Manager API"


def test_create_and_get_task(client):
    res = client.post("/tasks", json={"title": "Belajar DevSecOps"})
    assert res.status_code == 201
    task_id = res.get_json()["id"]

    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Belajar DevSecOps"


def test_create_task_invalid(client):
    res = client.post("/tasks", json={"title": ""})
    assert res.status_code == 400
    assert "errors" in res.get_json()


def test_update_task(client):
    client.post("/tasks", json={"title": "Tugas P5"})
    res = client.put("/tasks/1", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_delete_task(client):
    client.post("/tasks", json={"title": "Hapus aku"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404


def test_filter_and_stats(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    client.put("/tasks/1", json={"done": True})

    done_list = client.get("/tasks?done=true").get_json()
    assert len(done_list) == 1
    assert client.get("/tasks/stats").get_json() == {
        "total": 2,
        "done": 1,
        "pending": 1,
    }


def test_validator_rejects_long_title():
    _, errors = validate_task_payload({"title": "x" * 101}, 100, 500)
    assert errors


def test_parse_bool_param():
    assert parse_bool_param("TRUE") is True
    assert parse_bool_param("false") is False
    assert parse_bool_param("abc") is None
    assert parse_bool_param(None) is None


def test_storage_limit():
    storage = TaskStorage(max_tasks=1)
    storage.add("satu")
    with pytest.raises(StorageFullError):
        storage.add("dua")
