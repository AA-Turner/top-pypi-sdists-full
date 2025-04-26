"""mcli debug Entrypoint"""
import argparse

from mcli.cli.m_debug.debug_run import debug_run
from mcli.utils import utils_completers


def _debug_entrypoint(parser, **kwargs):
    del kwargs
    parser.print_help()


def _configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=_debug_entrypoint, parser=parser)

    run_parser = subparsers.add_parser('run', help='Get debug information for a specific run')
    run_name_parser = run_parser.add_argument(
        'run_name',
        type=str,
        help='The name of the run.',
    )
    run_name_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore

    run_parser.add_argument('--resumption',
                            type=int,
                            default=None,
                            metavar='N',
                            dest='resumption',
                            help='Resumption (0-indexed) of the run to get debug information for. '
                            'The default is the latest resumption.')
    run_parser.set_defaults(func=debug_run)

    return parser


def add_debug_argparser(subparser: argparse._SubParsersAction) -> argparse.ArgumentParser:
    debug_parser: argparse.ArgumentParser = subparser.add_parser(
        'debug',
        help='Get debug information on an object',
    )
    debug_parser = _configure_argparser(parser=debug_parser)
    return debug_parser
