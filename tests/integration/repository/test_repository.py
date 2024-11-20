from sqlalchemy import select, text
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from src.poc.adapters.repositories import SqlAlchemyBookRepository
from src.poc.model.book import Book


class TestRepository:

    @staticmethod
    def _insert_book(session: Session, title: str, id: int | None = None) -> int:
        """
        Adds a book to the persistent unit

        Args:
            session: sqlalchemy session
            title: book title

        Returns:
            the inserted id
        """
        result = (
            session.execute(
                insert(Book)
                .returning(Book.id)
                .values(
                    id=id,
                    title=title,
                )
            )
            .scalars()
            .one_or_none()
        )

        session.commit()

        return result or -1

    def test_saves_book(self, session: Session):
        """
        GIVEN a book
        AND a repository
        WHEN repository save is called
        THEN it is stored in persistence unit
        """
        # GIVEN
        book = Book(title="Test Book")

        # AND
        repository = SqlAlchemyBookRepository(session=session)

        # WHEN
        repository.save(book)
        session.commit()

        # THEN
        result: tuple[int, str, ...] | None = session.execute(
            text("SELECT id, title FROM books"),
        ).one_or_none()

        assert result is not None
        assert result[0] is not None
        assert result[1] == book.title

    def test_finds_all_books(self, session: Session):
        """
        GIVEN a repository
        AND some inserted records
        WHEN repository finds all is called
        THEN all records are retrieved
        """
        # GIVEN
        repository = SqlAlchemyBookRepository(session=session)

        # AND
        one_book_id = self._insert_book(session, "Finds test")
        another_book_id = self._insert_book(session, "Another test")

        # WHEN
        results = repository.find_all()

        # THEN
        assert one_book_id, another_book_id in [book.id for book in results]

    def test_find_by_id(self, session: Session):
        """
        GIVEN a book repository
        AND an existent book saved
        WHEN repository find by is called with that book id
        THEN book is retrieved
        """
        # GIVEN
        repository = SqlAlchemyBookRepository(session=session)
        # AND
        book_id = self._insert_book(session, title="A find by test")

        # WHEN
        result = repository.find_by(id=book_id)

        # THEN
        assert result is not None
        assert result.id == book_id
        assert result.title == "A find by test"

    def test_delete(self, session: Session):
        """
        GIVEN a book repository
        AND an existent book saved
        WHEN repository delete is called with that book id
        THEN book is removed from database
        """
        # GIVEN
        repository = SqlAlchemyBookRepository(session=session)

        # AND
        book_id = self._insert_book(session, "A delete test")

        # WHEN
        affected_records = repository.delete(book_id == Book.id)
        session.commit()

        # THEN
        assert affected_records == 1
        result = session.execute(
            select(Book).where(book_id == Book.id)
        ).scalar_one_or_none()
        assert result is None
