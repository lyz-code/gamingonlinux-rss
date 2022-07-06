"""Define all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import logging
import typing
import urllib.parse
from datetime import datetime
from typing import Generator, List

import requests
from bs4 import BeautifulSoup, Tag
from dateutil import parser
from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import AnyHttpUrl
from tenacity import RetryError, retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential

from .exceptions import FetchError, ParseError
from .model import Article

log = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=5, min=1, max=300))
def get(url: str) -> BeautifulSoup:
    """Request an url and parse it."""
    log.debug(f"Fetching page {url}")
    request = requests.get(url)
    if request.status_code != 200:
        raise FetchError(f"{url} returned an {request.status_code} code")
    return BeautifulSoup(request.text, "html.parser")


def _normalize_url(url: str) -> AnyHttpUrl:
    """Encode url to make it compatible with AnyHttpUrl."""
    return typing.cast(
        AnyHttpUrl,
        urllib.parse.quote(url, ":/"),
    )


def get_articles(
    base_url: str = "https://gamingonlinux.com",
) -> Generator[Article, None, None]:
    """Return the articles of the GamingOnLinux website."""
    log.debug("Getting articles")
    page = 1
    while True:
        url = f"{base_url}/home/page={page}/"

        try:
            soup = get(url)
        except RetryError as error:
            raise FetchError(f"Error fetching {url}, is the site up?") from error

        articles_data = soup.find("div", class_="articles")
        if not isinstance(articles_data, Tag):
            raise ParseError(f"The content of {url} returned no articles.")

        for article_data in articles_data.find_all("div", class_="article"):
            yield Article(
                url=_normalize_url(article_data.find(class_="title").a["href"]),
                title=article_data.find(class_="title").string,
                summary=article_data.find(class_="p-summary").string,
                author=article_data.find(class_="p-author").string,
                image=_normalize_url(article_data.img["src"]),
                tags=[
                    tag.string
                    for tag in article_data.find(class_="tags").find_all("li")
                ],
                published_at=parser.parse(article_data.find("time")["datetime"]),
            )

        page += 1


def get_article_content(
    url: str, indivious: str = "https://yewtu.be", iframe: bool = False
) -> str:
    """Get the article content.

    If iframe is true, it will add an iframe instead of a link to open it in a new
    tab. The problem is that iframes are not yet supported by Feeder or Wallabag, so
    it's left as an image.
    """
    soup = get(url)

    content = soup.find(class_="e-content")
    if not isinstance(content, Tag):
        raise ParseError(f"The content of {url} returned no article content.")

    # Substitute the youtube video with an indivious one
    for video in soup.find_all(class_="hidden_video_content"):
        video_data = video.find(class_="accept_video")
        video_url = f'{indivious}/embed/{video_data["data-video-id"]}'
        if iframe:
            new_video = soup.new_tag(
                "iframe",
                src=video_url,
                width="640",
                height="360",
                frameborder="0",
                allowfullscreen="true",
            )
        else:
            new_video = soup.new_tag(
                "a",
                href=video_url,
                target="_blank",
            )
            new_video.string = "See video"

        video.clear()
        video.append(new_video)

    return str(content)


def create_rss(rss_path: str, rss_url: str, max_articles: int = 100) -> None:
    """Create the RSS feed with the articles."""
    # Build the articles
    log.info("Fetching the site data")
    articles: List[Article] = []
    for id_, article in enumerate(get_articles()):
        log.debug(f"Fetching article {str(id_)} of {str(max_articles)}")
        article.content = get_article_content(article.url)
        articles.append(article)
        if id_ == max_articles - 1:
            break

    # Create the feed
    env = Environment(
        loader=PackageLoader("gamingonlinux_rss", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("rss.xml.j2")

    feed_content = template.render(
        rss_url=rss_url, published_at=datetime.now(), articles=articles
    )

    with open(rss_path, "+w", encoding="utf-8") as rss_file:
        rss_file.write(feed_content)
