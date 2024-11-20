from src.poc.adapters import mappers
from src.poc.model.book import Book


class TestMappers:

    def test_base_maps_to_dict(self):
        """
        GIVEN a book
        WHEN mapper is called
        THEN dictionary has all its values
        """

        # GIVEN
        book = Book(
            title="A mapper test", author="Tom", published_year=2024, genre="TestCase"
        )

        # WHEN
        mapped_dict = mappers.base_to_dict(book)

        # THEN
        assert book.id == mapped_dict.get("id")
        assert book.author == mapped_dict.get("author")
        assert book.title == mapped_dict.get("title")
        assert book.published_year == mapped_dict.get("published_year")
        assert book.genre == mapped_dict.get("genre")

    def test_base_maps_to_dict_exclude_nones(self):
        """
        GIVEN a book
        AND a flag to exclude nones
        WHEN mapper is called
        THEN dictionary has all its values
        """

        # GIVEN
        book = Book(title="A mapper test")

        # AND
        flag = False

        # WHEN
        mapped_dict = mappers.base_to_dict(base=book, include_nones=flag)

        # THEN
        assert book.id == mapped_dict.get("id")
        assert book.title == mapped_dict.get("title")

        keys = mapped_dict.keys()
        assert "author" not in keys
        assert "published_year" not in keys
        assert "genre" not in keys
