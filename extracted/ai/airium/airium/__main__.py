#!/usr/bin/env python

import argparse
import os
import sys
from typing import Optional, cast

try:
    from airium import __version__, from_html_to_airium
except ImportError:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(this_dir))
    from airium import __version__, from_html_to_airium


def entry_main(*args: str) -> None:
    opts = parse_options(args or sys.argv[1:])

    try:
        code = make_airium_code(opts.input_html)
        if code is not None:
            print(code)

    except Exception as e:
        msg = f" Translation failed.\n {type(e).__name__}: {e}"
        sys.stderr.write(msg + "\n")
        sys.exit(msg)


def make_airium_code(input_arg: str) -> Optional[str]:
    html = get_html_as_string(input_arg)
    if html is None:
        sys.stderr.write(f"\nUnable to get HTML from: {input_arg}\n\n")
        sys.exit(31)

    return cast(Optional[str], from_html_to_airium(html))


def _get_html_from_local_file(file_path: str) -> Optional[str]:
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "rt") as file:
        return file.read()


def _get_html_from_uri(uri: str) -> Optional[str]:
    try:
        import requests
    except ImportError as error:
        sys.stderr.write("\nPlease install `requests` package in order to fetch html files from web.\n")
        sys.stderr.write(f"{type(error).__name__}: {error}\n")
        return None

    try:
        response = requests.get(uri, auth=("user", "pass"))
    except IOError as error:
        sys.stderr.write(f"{type(error).__name__}: {error}\n")
        return None

    return _get_html_from_response(response, uri)


def _get_html_from_response(response, uri: str) -> Optional[str]:
    if response.status_code != 200:
        return None

    content_type = response.headers["content-type"]
    if "text/html" in content_type:
        return str(response.text)

    sys.stderr.write(f"Bad content type returned from {uri}: {content_type}.")
    return None


def get_html_as_string(input_arg: str) -> Optional[str]:
    for method in (_get_html_from_local_file, _get_html_from_uri):
        try:
            html = method(input_arg)
        except (
            ValueError,
            TypeError,
            KeyError,
            IOError,
            AttributeError,
            TimeoutError,
            AssertionError,
        ):
            continue
        if html is not None:
            return html

    return None


def get_html_as_strnig(input_arg: str) -> Optional[str]:
    """Keep backward compatibility with the misspelled function"""
    return get_html_as_string(input_arg)


def parse_options(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "airium",
        description="Parse input files and generate output based on options given.",
    )

    parser.add_argument(
        "input_html",
        metavar="URI_PATH",
        nargs="?",
        help="Local HTML file path or an URI",
    )

    parser.add_argument("-v", "--version", action="version", version=f"airium {__version__}")

    return parser.parse_args(args)


if __name__ == "__main__":  # pragma: no cover
    entry_main()
