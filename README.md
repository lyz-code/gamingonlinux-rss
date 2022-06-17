# GamingOnLinux RSS

[![Actions Status](https://github.com/lyz-code/gamingonlinux-rss/workflows/Tests/badge.svg)](https://github.com/lyz-code/gamingonlinux-rss/actions)
[![Actions Status](https://github.com/lyz-code/gamingonlinux-rss/workflows/Build/badge.svg)](https://github.com/lyz-code/gamingonlinux-rss/actions)
[![Coverage Status](https://coveralls.io/repos/github/lyz-code/gamingonlinux-rss/badge.svg?branch=main)](https://coveralls.io/github/lyz-code/gamingonlinux-rss?branch=main)

Full article RSS of the GamingOnLinux website.

Some months ago, GamingOnLinux decided to reduce the quality of their public RSS
so that users support them to get the good RSS feed. It's important to support
the content creators, so if you can, [please
do](https://www.gamingonlinux.com/support-us/), if you are not able to do so,
you can use [this alternate
RSS](https://raw.githubusercontent.com/lyz-code/gamingonlinux-rss/main/rss.xml) created with this
program.

Features:

* Create entries with images.
* Change youtube videos to [indivious](https://invidious.io/A) ones.

## Installing

```bash
pip install gamingonlinux-rss
```

## Usage

```bash
$: gaminonlinux --help

Usage: gamingonlinux [OPTIONS] RSS_PATH RSS_URL

Options:
  --version                   Show the version and exit.
  -n, --max-articles INTEGER
  -v, --verbose
  --help                      Show this message and exit.

$: gaminonlinux rss.xml https://lyz-code.github.io/gamingonlinux-rss/rss.xml
```

## Contributing

For guidance on setting up a development environment, and how to make
a contribution to *gamingonlinux-rss*, see [Contributing to
gamingonlinux-rss](https://lyz-code.github.io/gamingonlinux-rss/contributing).

## License

GPLv3
