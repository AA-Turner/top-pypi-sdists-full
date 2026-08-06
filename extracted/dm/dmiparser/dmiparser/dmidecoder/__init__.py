from dmiparser.dmidecoder.dmidecoder import DmiDecoder
from argparse import ArgumentParser
from subprocess import CalledProcessError
from sys import exit, stderr

__all__ = ["DmiDecoder", "main"]


def main() -> None:
    parser = ArgumentParser(
        description="Run dmidecode and print the output as text",
        epilog='example: sudo env "PATH=$PATH" dmidecoder -f json -p',
    )
    parser.add_argument(
        "-f", "--format", default="json", choices=["json", "jsonc", "yaml", "xml"], help="output format (default: json)"
    )
    parser.add_argument("-p", "--pretty", action="store_true", help="human-friendly pretty output")
    parser.add_argument(
        "-a", "--arguments", nargs=1, type=str, required=False, help="arguments passed to dmidecode command"
    )
    args = parser.parse_args()

    try:
        dmidecoder = DmiDecoder(
            args.arguments[0] if isinstance(args.arguments, list) and len(args.arguments) > 0 else None,
            pretty=args.pretty,
            format=args.format,
        )
    except CalledProcessError as e:
        if e.output:
            print(e.output, end="")
        exit(e.returncode)
    except ValueError as e:
        print(str(e), file=stderr)
        exit(1)

    print(dmidecoder.text)
