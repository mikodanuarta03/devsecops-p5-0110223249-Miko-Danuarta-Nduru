"""Penyimpanan task di memori (in-memory)."""
from .models import Task


class StorageFullError(Exception):
    """Dilempar ketika jumlah task melebihi batas."""


class TaskStorage:
    def __init__(self, max_tasks=1000):
        self._tasks = {}
        self._next_id = 1
        self._max_tasks = max_tasks

    def add(self, title, description=""):
        if len(self._tasks) >= self._max_tasks:
            raise StorageFullError("Batas jumlah task tercapai")
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id):
        return self._tasks.get(task_id)

    def list(self, done=None):
        tasks = list(self._tasks.values())
        if done is not None:
            tasks = [t for t in tasks if t.done == done]
        return tasks

    def update(self, task_id, **fields):
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key, value in fields.items():
            setattr(task, key, value)
        return task

    def delete(self, task_id):
        return self._tasks.pop(task_id, None) is not None

    def stats(self):
        total = len(self._tasks)
        done = sum(1 for t in self._tasks.values() if t.done)
        return {"total": total, "done": done, "pending": total - done}
