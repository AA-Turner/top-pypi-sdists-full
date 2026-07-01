""" mcli describe Endpoint """
from __future__ import annotations

import argparse
import logging

from mcli.cli.m_describe.describe_clusters import describe_cluster
from mcli.cli.m_describe.describe_inference_deployments import describe_deploy
from mcli.cli.m_describe.describe_runs import describe_run
from mcli.cli.m_describe.describe_users import describe_me, describe_user
from mcli.utils import utils_completers

logger = logging.getLogger(__name__)


def describe_entrypoint(parser, **kwargs):
    del kwargs
    parser.print_help()


def describe_runs_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser = subparser.add_parser('run', help='List metadata about a specific run')
    run_name_parser = run_parser.add_argument(
        'run_name',
        type=str,
        nargs='?',
        help='The name of the run. If not provided, will describe the latest run',
    )
    run_name_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore
    yaml_grp = run_parser.add_mutually_exclusive_group()
    yaml_grp.add_argument(
        '--no-yaml',
        action='store_true',
        default=False,
        help='Do not print the original run config',
    )

    yaml_grp.add_argument(
        '--yaml-only',
        action='store_true',
        default=False,
        help='Only print the original run config',
    )
    run_parser.set_defaults(func=describe_run)


def describe_user_argparser(subparser: argparse._SubParsersAction) -> None:
    user_parser = subparser.add_parser('user', help='List metadata about a specific user')
    user_parser.add_argument(
        'user_identifier',
        type=str,
        help='The ID or email of the user.',
    )
    user_parser.set_defaults(func=describe_user)


def describe_deployments_argparser(subparser: argparse._SubParsersAction) -> None:
    deploy_parser = subparser.add_parser('deployment', help='List metadata about a specific inference deployment')
    deployment_name_parser = deploy_parser.add_argument(
        'deployment_name',
        type=str,
        help='Inference Deployment name',
    )
    deployment_name_parser.completer = utils_completers.DeploymentNameCompleter()  # pyright: ignore
    deploy_parser.set_defaults(func=describe_deploy)


def describe_cluster_argparser(subparser: argparse._SubParsersAction) -> None:
    cluster_parser = subparser.add_parser('cluster', help='List instances and utilization of a specific cluster')
    cluster_parser.add_argument('cluster_name', type=str, nargs='?', help='Cluster name')
    cluster_parser.set_defaults(func=describe_cluster)


def add_describe_parser(subparser: argparse._SubParsersAction, is_admin: bool = False) -> argparse.ArgumentParser:
    describe_parser: argparse.ArgumentParser = subparser.add_parser(
        'describe',
        help='Get detailed information on an object',
    )
    return _configure_argparser(parser=describe_parser, is_admin=is_admin)


def _configure_argparser(parser: argparse.ArgumentParser, is_admin: bool = False) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you can describe',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=describe_entrypoint, parser=parser)
    describe_runs_argparser(subparser=subparsers)
    describe_deployments_argparser(subparser=subparsers)
    describe_cluster_argparser(subparser=subparsers)
    subparsers.add_parser(
        'me',
        help='List detailed information about the current user',
    ).set_defaults(func=describe_me)
    if is_admin:
        describe_user_argparser(subparser=subparsers)
    return parser
