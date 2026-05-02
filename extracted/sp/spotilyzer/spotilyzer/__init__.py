"""
spotilyzer entry point
"""

# system imports
import sys

# project imports
from .cli import parse_cmdline
from .driver import run


def main(argv=sys.argv):
    """
    Entry point for spotilyzer. All exceptions are caught displayed and
    returned as a failing exit code.
    :param argv: command line arguments
    :return: exit code
    """
    try:
        args = parse_cmdline(argv)
        run(args)
    except SystemExit as exit_code:
        return exit_code
    except Exception as err:
        print(f"[error]: {err}")
        return 1
    return 0
