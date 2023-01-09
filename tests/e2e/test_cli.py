"""Test the command line interface."""

import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

import feedparser
import pytest
from click.testing import CliRunner
from dateutil import parser, tz

from gamingonlinux_rss.entrypoints.cli import cli
from gamingonlinux_rss.version import __version__


@pytest.fixture(name="runner")
def fixture_runner() -> CliRunner:
    """Configure the Click cli test runner."""
    return CliRunner(mix_stderr=False)


def test_version(runner: CliRunner) -> None:
    """Prints program version when called with --version."""
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert re.search(
        rf" *gamingonlinux_rss: {__version__}\n *Python: .*\n *Platform: .*",
        result.stdout,
    )


def test_corrects_one_file(runner: CliRunner, tmp_path: Path) -> None:
    """Correct the source code of a file."""
    rss_file = str(tmp_path / "rss.xml")
    rss_url = "https://gamingonlinuxrss.com/rss.xml"
    now = datetime.now(tz=tz.tzlocal())

    result = runner.invoke(cli, [rss_file, rss_url, "-n", "1"])

    assert result.exit_code == 0
    feed = feedparser.parse(rss_file)
    # Channel attributes
    assert feed.feed.title == "GamingOnLinux Latest Articles"
    assert feed.feed.description == "The latest articles from GamingOnLinux"
    assert feed.feed.link == "https://www.gamingonlinux.com/"
    assert feed.feed.links[1].href == rss_url
    assert parser.parse(feed.feed.published).date() == now.date()
    assert (
        feed.feed.image.href
        == "https://www.gamingonlinux.com/templates/default/images/favicons/favicon.ico"
    )
    # Entry attributes
    assert len(feed.entries) == 1
    article = feed.entries[0]
    for attribute in ["title", "author", "description", "link"]:
        assert getattr(article, attribute) is not None
    # Assert that the date are compliant with RFC2822
    # https://www.rssboard.org/rss-validator/docs/error/InvalidRFC2822Date.html
    assert isinstance(parsedate_to_datetime(article.published), datetime)
