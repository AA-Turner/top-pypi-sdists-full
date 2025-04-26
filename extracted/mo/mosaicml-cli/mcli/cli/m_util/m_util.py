""" mcli util command """
import argparse
from functools import partial

from mcli.cli.m_util.util import get_util


def add_util_argparser(subparser: argparse._SubParsersAction, is_admin: bool = False):
    """Adds the util parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    util_parser: argparse.ArgumentParser = subparser.add_parser(
        'util',
        aliases=['utilization'],
        help='Get cluster utilization',
    )

    util_parser.add_argument(
        'clusters',
        help='Which cluster would you like to get utilization for?',
        nargs='*',
    )

    util_parser.add_argument(
        '--hide-users',
        action='store_true',
        help='Do not show the by user utilization breakdown',
    )

    training_or_inference = util_parser.add_mutually_exclusive_group()

    training_or_inference.add_argument(
        '-t',
        '--training',
        help='Only view training utilization',
        action='store_true',
    )

    training_or_inference.add_argument(
        '-i',
        '--inference',
        help='Only view inference utilization',
        action='store_true',
    )

    util_parser.set_defaults(func=partial(get_util, include_all=is_admin))
    return util_parser
