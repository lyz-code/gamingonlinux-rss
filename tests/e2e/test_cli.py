"""Test the command line interface."""

import re
from datetime import datetime

import feedparser
import pytest
from click.testing import CliRunner
from dateutil import parser, tz
from py._path.local import LocalPath

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


def test_corrects_one_file(runner: CliRunner, tmpdir: LocalPath) -> None:
    """Correct the source code of a file."""
    # ignore: call to untyped join method, they don't have type hints
    rss_file = str(tmpdir.join("rss.xml"))  # type: ignore
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
    for attribute in ["title", "author", "description", "link", "published"]:
        assert getattr(feed.entries[0], attribute) is not None
