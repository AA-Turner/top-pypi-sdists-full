"""
spotilyzer cli
"""

# system imports
import argparse
import os

# project imports
from .subcommands import subcommands

# constants
SUBCOMMAND_ARG = 'subcommand'


def parse_cmdline(argv):
    """
    Convert command line arguments to a argparse Namespace. Load subparsers
    from each subcommand.
    :param argv: list of command line arguments
    :return: argparse Namespace
    """
    parser = argparse.ArgumentParser(description="AWS spot fleet analyzer")
    subparsers = parser.add_subparsers(
        dest=SUBCOMMAND_ARG,
        description=f"use {os.path.basename(argv[0])} <subcommand> -h for "
                    "subcommand details"
    )
    for subcommand in subcommands:
        subcommand.add_parser(subparsers)
    return parser.parse_args(argv[1:])
