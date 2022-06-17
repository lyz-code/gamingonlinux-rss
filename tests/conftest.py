"""Store the classes and fixtures used throughout the tests."""

from typing import Generator

import freezegun
import pytest
from freezegun.api import FrozenDateTimeFactory


@pytest.fixture(name="page_url", scope="session")
def page_url_() -> str:
    """Return the url of the first page of the site."""
    return "https://gamingonlinux.com/home/page=1/"


@pytest.fixture(name="page_html", scope="session")
def page_html_() -> str:
    """Return the content of the first page of gamingonlinux.com."""
    with open("tests/assets/page_1.html", "r", encoding="UTF8") as file_descriptor:
        return file_descriptor.read()


@pytest.fixture(name="article_html", scope="session")
def article_html_() -> str:
    """Return the content of an article."""
    with open("tests/assets/article.html", "r", encoding="UTF8") as file_descriptor:
        return file_descriptor.read()


@pytest.fixture(name="article_url", scope="session")
def article_url_() -> str:
    """Return the url of an article"""
    return (
        "https://www.gamingonlinux.com/2019/04/"
        "king-arthurs-gold-the-2d-multiplayer-castle-siege-game-is-now-free-to-play/"
    )


@pytest.fixture(autouse=True)
def frozen_time() -> Generator[FrozenDateTimeFactory, None, None]:
    """Freeze all tests time"""
    with freezegun.freeze_time() as freeze:
        yield freeze
