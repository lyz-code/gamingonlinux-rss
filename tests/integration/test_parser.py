"""Test the parser against the website."""

from gamingonlinux_rss import services


def test_parser_extracts_articles() -> None:
    """
    Given: That gamingonlinux.com is up
    When: get_articles is called a number so small that with the first page of results
        is enough
    Then: An Article are returned.
    """
    result = services.get_articles()

    for article in result:
        assert article.url is not None
        assert article.title is not None
        assert article.content is None
        assert article.summary is not None
        assert article.author is not None
        assert article.published_at is not None
        break


def test_parser_extracts_articles_of_two_pages() -> None:
    """
    Given: That gamingonlinux.com is up
    When: get_articles is called a number of times that requires the second page of
        results to be loaded
    Then: 30 Articles are returned.
    """
    result = services.get_articles()

    for number, article in enumerate(result):
        assert article.url is not None
        assert article.title is not None
        assert article.content is None
        assert article.summary is not None
        assert article.author is not None
        assert article.published_at is not None
        if number == 30:
            break


def test_extracts_article_content(article_url: str) -> None:
    """
    Given: That the endpoint of an article works.
    When: get_article is called.
    Then: the content of the article is returned and tweaked:
        * The video link is changed to an indivious instance
    """
    result = services.get_article_content(article_url)

    assert result is not None
    assert "With some silly physics " in result
    assert "https://yewtu.be/embed/FvaT01outXs" in result
