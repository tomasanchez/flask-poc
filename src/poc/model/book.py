"""
Book Model
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.poc.model import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, default=0)
    title: Mapped[str] = mapped_column(nullable=False, default=None)
    author: Mapped[str | None] = mapped_column(String(35), nullable=True, default=None)
    genre: Mapped[str | None] = mapped_column(nullable=True, default=None)
    published_year: Mapped[int | None] = mapped_column(nullable=True, default=None)
