"""
Book Model
"""
import dataclasses
import uuid


@dataclasses.dataclass(frozen=True)
class Book:
    title: str
    author: str | None = None
    genre: str | None = None
    published_year: int | None = None
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
