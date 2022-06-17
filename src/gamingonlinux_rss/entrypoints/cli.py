"""Command line interface definition."""

import click

from .. import services, version
from . import load_logger


@click.command()
@click.version_option(version="", message=version.version_info())
@click.argument("rss_path")
@click.argument("rss_url")
@click.option("-n", "--max-articles", type=int, default=100)
@click.option("-v", "--verbose", is_flag=True)
def cli(rss_path: str, rss_url: str, verbose: bool, max_articles: int) -> None:
    """Command line interface main click entrypoint."""
    load_logger(verbose)
    services.create_rss(rss_path=rss_path, rss_url=rss_url, max_articles=max_articles)


if __name__ == "__main__":  # pragma: no cover
    # E1120: As the arguments are passed through the function decorators instead of
    # during the function call, pylint get's confused.
    cli()  # noqa: E1120
