"""Define the data models of the program."""

from datetime import datetime
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
