from dmiparser.dmiparser import DmiParser, format_output
from sys import exit, stderr, stdin
from argparse import ArgumentParser

__version__ = "7.2"
__all__ = ["DmiParser", "format_output", "main"]


def main() -> None:
    parser = ArgumentParser(
        description="Read dmidecode output from stdin and print as text",
        epilog="example: sudo dmidecode | dmiparser -f json -p",
    )
    parser.add_argument(
        "-f", "--format", default="json", choices=["json", "jsonc", "yaml", "xml"], help="output format (default: json)"
    )
    parser.add_argument("-p", "--pretty", action="store_true", help="human-friendly pretty output")
    args = parser.parse_args()

    try:
        dmiparser = DmiParser(stdin.read(), pretty=args.pretty, format=args.format)
        print(str(dmiparser))
    except ValueError as e:
        print(str(e), file=stderr)
        exit(1)
