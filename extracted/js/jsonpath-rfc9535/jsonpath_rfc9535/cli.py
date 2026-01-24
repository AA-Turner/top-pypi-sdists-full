"""JSONPath command line interface."""

import argparse
import json
import sys

import jsonpath_rfc9535 as jsonpath
from jsonpath_rfc9535.__about__ import __version__
from jsonpath_rfc9535.exceptions import JSONPathIndexError
from jsonpath_rfc9535.exceptions import JSONPathSyntaxError
from jsonpath_rfc9535.exceptions import JSONPathTypeError

INDENT = 2

_EPILOG = """\
Example usage:
  Find values in source.json matching a JSONPath expression, output to result.json.
  $ jsonpath-rfc9535 -q "$.foo['bar'][?@.baz > 1]" -f source.json -o result.json
"""


class DescriptionHelpFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
):
    """Raw epilog formatter with defaults."""


def setup_parser() -> argparse.ArgumentParser:  # noqa: D103
    parser = argparse.ArgumentParser(
        prog="jsonpath-rfc9535",
        formatter_class=DescriptionHelpFormatter,
        description=(
            "Find values in a JSON document given an RFC 9535 JSONPath expression."
        ),
        epilog=_EPILOG,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"jsonpath-rfc9535, version {__version__}",
        help="Show the version and exit.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show stack traces.",
    )

    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Add indents and newlines to output JSON.",
    )

    parser.set_defaults(func=handle_path_command)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-q",
        "--query",
        help="JSONPath expression as a string.",
    )

    group.add_argument(
        "-r",
        "--query-file",
        type=argparse.FileType(mode="r"),
        help="Text file containing a JSONPath expression.",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=argparse.FileType(mode="rb"),
        default=sys.stdin,
        help=(
            "File to read the target JSON document from. "
            "Defaults to reading from the standard input stream."
        ),
    )

    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType(mode="w"),
        default=sys.stdout,
        help=(
            "File to write resulting objects to, as a JSON array. "
            "Defaults to the standard output stream."
        ),
    )

    return parser


def handle_path_command(args: argparse.Namespace) -> None:  # noqa: PLR0912, D103
    if args.query is not None:
        query = args.query
    else:
        query = args.query_file.read().strip()

    try:
        path = jsonpath.JSONPathEnvironment().compile(query)
    except JSONPathSyntaxError as err:
        if args.debug:
            raise
        sys.stderr.write(f"syntax error: {err}\n")
        sys.exit(1)
    except JSONPathTypeError as err:
        if args.debug:
            raise
        sys.stderr.write(f"type error: {err}\n")
        sys.exit(1)
    except JSONPathIndexError as err:
        if args.debug:
            raise
        sys.stderr.write(f"index error: {err}\n")
        sys.exit(1)

    try:
        data = json.load(args.file)
        values = path.find(data).values()
    except json.JSONDecodeError as err:
        if args.debug:
            raise
        sys.stderr.write(f"target document json decode error: {err}\n")
        sys.exit(1)
    except JSONPathTypeError as err:
        # Type errors are currently only occurring are compile-time.
        if args.debug:
            raise
        sys.stderr.write(f"type error: {err}\n")
        sys.exit(1)

    indent = INDENT if args.pretty else None
    json.dump(values, args.output, indent=indent)


def main() -> None:
    """CLI argument parser entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
