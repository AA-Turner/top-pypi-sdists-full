"""Entry point for markdown-it-reporter."""
import argparse
import sys
import os

from mir._impl import html_report

SCRIPT_DESCRIPTION = """
Convert a markdown document into a HTML page using markdown-it.
"""


def main(argv=None):
    """Entry point for script to convert Markdown report into HTML."""
    if argv is None:
        argv = sys.argv[1:]

    args = _parser().parse_args(argv)

    markdown_path = args.input_path
    html_path = args.output_path or (markdown_path + ".html")

    with open(markdown_path, "r") as f:
        markdown = f.read()

    html_contents = html_report(markdown, args.title)

    with open(html_path, "w") as f:
        f.write(html_contents)


def _parser():
    parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTION)
    parser.add_argument('input_path', metavar='INPUT', type=str,
                        help='input markdown path (.md)')
    parser.add_argument('output_path', metavar='OUTPUT', type=str, nargs="?",
                        help='output HTML path (.html)')
    parser.add_argument('--title', type=str, default=None,
                        help='title of document')
    return parser


__all__ = (
    'main',
)
