""" CLI Diff options"""
import argparse

from mcli.cli.m_diff.diff_deployments import diff_deployments
from mcli.cli.m_diff.diff_runs import diff_runs


def diff_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you cancompare',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=diff_entrypoint, parser=parser)

    diff_runs_argparser(subparser=subparsers)
    diff_deployments_argparser(subparser=subparsers)
    return parser


def diff_runs_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser = subparser.add_parser('run', help='Compare the difference between two runs', aliases=['runs'])
    run_parser.add_argument(
        'run_name1',
        type=str,
        help='The name of the first run',
    )
    run_parser.add_argument(
        'run_name2',
        type=str,
        help='The name of the second run',
    )
    run_parser.set_defaults(func=diff_runs)


def diff_deployments_argparser(subparser: argparse._SubParsersAction) -> None:
    deployments_parser = subparser.add_parser('deployments',
                                              help='Compare the difference between two deployments',
                                              aliases=['deployment'])
    deployments_parser.add_argument(
        'deployment_name1',
        type=str,
        help='The name of the first deployment',
    )
    deployments_parser.add_argument(
        'deployment_name2',
        type=str,
        help='The name of the second deployment',
    )
    deployments_parser.set_defaults(func=diff_deployments)


def add_diff_argparser(subparser: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Adds the diff parser to a subparser

    Args:
        subparser: the Subparser to add the Diff parser to
    """
    diff_parser: argparse.ArgumentParser = subparser.add_parser(
        'diff',
        help='Diff objects created with mcli',
    )
    diff_parser = configure_argparser(parser=diff_parser)
    return diff_parser
