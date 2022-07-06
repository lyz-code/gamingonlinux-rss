"""Tests the service layer."""

import pytest
from requests_mock.mocker import Mocker

from gamingonlinux_rss import exceptions, services
from gamingonlinux_rss.model import Article


class TestGetArticles:
    """Test the fetch of articles."""

    @pytest.mark.slow()
    def test_retries_if_fails(
        self, requests_mock: Mocker, page_url: str, page_html: str
    ) -> None:
        """
        Given: that the web fails, 3 times and then it works
        When: using get_articles
        Then: an article is returned
        """
        requests_mock.get(
            page_url,
            [
                {"status_code": 404},
                {"status_code": 404},
                {"status_code": 404},
                {"text": page_html, "status_code": 200},
            ],
        )

        result = next(services.get_articles())

        assert isinstance(result, Article)

    @pytest.mark.slow()
    def test_doesnt_retry_endless(self, page_url: str, requests_mock: Mocker) -> None:
        """
        Given: that the web fails endlessly
        When: using get_articles until it fails
        Then: an exception is returned
        """
        requests_mock.get(page_url, status_code=404)

        with pytest.raises(
            exceptions.FetchError, match=f"Error fetching {page_url}, is the site up?"
        ):
            next(services.get_articles())

    def test_handles_wrong_html(self, page_url: str, requests_mock: Mocker) -> None:
        """
        Given: that the web returns an html without articles
        When: using get_articles
        Then: an exception is returned
        """
        requests_mock.get(page_url, text="no articles here")

        with pytest.raises(
            exceptions.ParseError,
            match=f"The content of {page_url} returned no articles.",
        ):
            next(services.get_articles())

    def test_handles_spaces_in_image_url(
        self, page_url: str, requests_mock: Mocker
    ) -> None:
        """
        Given: that the web returns an html with an article that has a space in the url
        When: using get_articles
        Then: the image link is transformed so it doesn't raise a ValidationError
        """
        with open(
            "tests/assets/homepage-with-space-in-article-image-url.html",
            "r",
            encoding="UTF8",
        ) as file_descriptor:
            requests_mock.get(page_url, text=file_descriptor.read())

        result = next(services.get_articles())

        assert str(result.image) == (
            "https://www.gamingonlinux.com/uploads/tagline_gallery/"
            "deck%20verified.jpg"
        )


class TestGetArticleContent:
    """Test the fetch of the article content."""

    def test_handles_wrong_html(self, article_url: str, requests_mock: Mocker) -> None:
        """
        Given: that the web returns an html without article content
        When: using get_article_content
        Then: an exception is returned
        """
        requests_mock.get(article_url, text="no articles here")

        with pytest.raises(
            exceptions.ParseError,
            match=f"The content of {article_url} returned no article content.",
        ):
            services.get_article_content(article_url)
