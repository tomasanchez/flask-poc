import abc

from sqlalchemy import ColumnExpressionArgument, delete, inspect, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from src.poc.adapters.mappers import base_to_dict
from src.poc.model.book import Book


class BookRepository(abc.ABC):

    @abc.abstractmethod
    def save(self, book: Book, **kwargs):
        """
        Inserts or updates a book in persistent unit

        Args:
            book: entity to be persisted
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, **kwargs) -> Book | None:
        """
        Looks for a book matching a criteria

        Args:
            **kwargs: criteria to be matched

        Returns:
            Either a book or nothing, if no element satisfies given criteria
        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, **kwargs) -> list[Book]:
        """
        Obtains all records

        Returns:
            A collection of books
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args):
        """
        Removes books with matching criteria from persistent unit
        """
        raise NotImplementedError


class SqlAlchemyBookRepository(BookRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, book: Book, **kwargs):
        book_dict = base_to_dict(book, include_nones=kwargs.get("nullables", False))

        stmt = (
            insert(Book)
            .values(**book_dict)
            .on_conflict_do_update(
                # retrieve all primary keys as index
                index_elements=[pk.name for pk in inspect(Book).primary_key],
                set_=book_dict,
            )
        )

        self._session.execute(stmt)

    def find_by(self, **kwargs) -> Book | None:
        return (
            self._session.execute(select(Book).filter_by(**kwargs))
            .scalars()
            .one_or_none()
        )

    def find_all(self, **kwargs) -> list[Book]:
        return list(self._session.execute(select(Book)).scalars().all())

    def delete(self, *args: ColumnExpressionArgument[bool]) -> int:
        return self._session.execute(delete(Book).where(*args)).rowcount
