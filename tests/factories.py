"""Define the program factories."""

from typing import Any

from pydantic_factories import ModelFactory

from gamingonlinux_rss import model


class CustomFactory(ModelFactory[Any]):
    """Tweak the ModelFactory to add our custom mocks."""

    @classmethod
    def get_mock_value(cls, field_type: Any) -> Any:
        """Add our custom mock value."""
        if str(field_type) == "<class 'datetime.datetime'>":
            return cls._get_faker().date_time_between()

        return super().get_mock_value(field_type)


class ArticleFactory(CustomFactory):
    """Define the Article factory."""

    __model__ = model.Article
