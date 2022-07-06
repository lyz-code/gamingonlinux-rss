"""Script to test the validity of the created rss feed."""

import sys
from datetime import datetime
from email.utils import parsedate_to_datetime

import feedparser

feed = feedparser.parse(sys.argv[1])

assert len(feed.entries) >= 1

for article in feed.entries:
    for attribute in ["title", "author", "description", "link"]:
        assert getattr(article, attribute) is not None

    # Assert that the date are compliant with RFC2822
    # https://www.rssboard.org/rss-validator/docs/error/InvalidRFC2822Date.html
    assert isinstance(parsedate_to_datetime(article.published), datetime)
