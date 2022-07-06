"""Define the data models of the program."""

from datetime import datetime
from email import utils
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field


class Article(BaseModel):
    """Define the model of an article."""

    url: AnyHttpUrl
    title: str
    summary: str
    content: Optional[str] = None
    author: str
    image: Optional[AnyHttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    published_at: datetime

    @property
    def published_at_rfc2822(self) -> str:
        """Create an RFC2822 compliant date.

        https://www.rssboard.org/rss-validator/docs/error/InvalidRFC2822Date.html
        """
        return utils.format_datetime(self.published_at)
