"""Adds the mcli kube subcommand"""
import argparse
from typing import List, Optional

from mcli.cli.m_kube.m_get_config import add_get_config_parser
from mcli.cli.m_kube.m_merge_config import add_merge_config_parser


def kube_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='Kubernetes config commands',
                                       description='The table below shows what you can do with Kubernetes configs',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=kube_entrypoint, parser=parser)

    add_get_config_parser(subparsers)
    add_merge_config_parser(subparsers)

    return parser


def add_kube_argparser(subparser: argparse._SubParsersAction,
                       parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    """Adds the kube parser to a subparser

    Args:
        subparser: the Subparser to add the Kube parser to
    """
    del parents

    kube_parser: argparse.ArgumentParser = subparser.add_parser(
        'kube',
        help='Work with Kubernetes config files',
    )
    kube_parser = configure_argparser(parser=kube_parser)
    return kube_parser
