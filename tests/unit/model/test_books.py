import uuid

from src.poc.model.book import Book


class TestBooks:

    def test_book_has_id(self):
        """
        GIVEN a title
        AND a name
        AND a year
        AND a genre name
        WHEN structure is instantiated
        THEN a book is created with an autogenerated id
        """
        # GIVEN, AND, AND, AND
        title, name, year, genre = "The Lord of The Rings", "Tolkien", 1960, "Fantasy"

        # WHEN
        book = Book(title=title, author=name, published_year=year, genre=genre)

        # THEN
        assert book.id is not None
        assert isinstance(book.id, uuid.UUID)
        assert title == book.title
        assert name == book.author
        assert year == book.published_year
        assert genre == book.genre