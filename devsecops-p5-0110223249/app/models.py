"""Model data Task."""
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    done: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at,
        }
