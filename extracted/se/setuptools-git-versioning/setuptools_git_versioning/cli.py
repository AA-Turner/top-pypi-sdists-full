import argparse
import logging
import sys

from setuptools_git_versioning.log import DEBUG, LOG_FORMAT, VERBOSITY_LEVELS
from setuptools_git_versioning.setup import get_version


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="setuptools-git-versioning",
        description="Get version based on git information and 'setup.py' or 'pyproject.toml' config",
    )
    parser.add_argument(
        "root",
        type=str,
        default=None,
        nargs="?",
        help="Path to folder containing 'setup.py' or 'pyproject.toml' file. Default: current dir",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity level. Can be used multiple times: -v for INFO messages, -vv for DEBUG",
    )
    return parser


def main():
    parser = get_parser()
    namespace = parser.parse_args()
    log_level = VERBOSITY_LEVELS.get(namespace.verbose, DEBUG)
    logging.basicConfig(level=log_level, format=LOG_FORMAT, stream=sys.stderr)
    print(str(get_version(root=namespace.root)))  # noqa: T201
