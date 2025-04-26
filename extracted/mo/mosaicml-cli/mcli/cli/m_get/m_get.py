""" CLI Get options"""
import argparse
from functools import partial
from typing import List, Optional

from mcli import config
from mcli.cli.m_get import cli_get_secrets, get_clusters, get_organizations, get_users
from mcli.cli.m_get.display import OutputDisplay
from mcli.cli.m_get.inference_deployments import get_deployments_argparser
from mcli.cli.m_get.runs import get_runs_argparser
from mcli.cli.m_log.m_log import add_log_parser
from mcli.models.mcli_secret import SecretType
from mcli.utils.utils_model import SubmissionType


def get_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-o',
                        '--output',
                        type=OutputDisplay,
                        choices=list(OutputDisplay),
                        default=OutputDisplay.TABLE,
                        metavar='FORMAT',
                        help=f'Output display format. Should be one of {list(OutputDisplay)}')


def configure_argparser(parser: argparse.ArgumentParser, is_admin: bool = False) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Objects',
                                       description='The table below shows the objects that you can get information on',
                                       help='DESCRIPTION',
                                       metavar='OBJECT')
    parser.set_defaults(func=get_entrypoint, parser=parser)

    cluster_parser = subparsers.add_parser('clusters',
                                           aliases=['cluster', 'platforms', 'platform'],
                                           help='List registered clusters')
    cluster_parser.add_argument('--ids',
                                action='store_true',
                                dest='include_ids',
                                default=config.ADMIN_MODE,
                                help='Include the cluster ids in the output')
    add_common_arguments(cluster_parser)
    cluster_parser.set_defaults(func=partial(get_clusters, include_all=is_admin))

    if is_admin:
        user_parser = subparsers.add_parser('user', aliases=['users'], help='List users')
        mcli_config = config.MCLIConfig.load_config()
        kwargs = {'type': str, 'dest': 'org_id', 'help': 'Filter users by organization id'}
        if mcli_config.organization_id:
            kwargs['default'] = mcli_config.organization_id
        user_parser.add_argument('--org', **kwargs)
        add_common_arguments(user_parser)
        user_parser.set_defaults(func=get_users)

        org_parser = subparsers.add_parser('org',
                                           aliases=['orgs', 'organizations', 'organization'],
                                           help='List organizations')
        add_common_arguments(org_parser)
        org_parser.set_defaults(func=get_organizations)

    # pylint: disable-next=invalid-name
    SECRET_EXAMPLES = """

Examples:

> mcli get secrets
NAME         TYPE
foo          environment
docker-cred  docker_registry
file         mounted

> mcli get secrets --type environment
NAME         TYPE
foo          environment
    """
    secrets_parser = subparsers.add_parser(
        'secrets',
        aliases=['secret'],
        help='List registered secrets and credentials',
        description='List all of your registered secrets and credentials. Each '
        'listed secret will be added to your run automatically. For details on '
        'exactly how each type of secret is added to your run, look to the '
        'individual secret type docs.',
        epilog=SECRET_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_common_arguments(secrets_parser)
    secrets_parser.set_defaults(func=cli_get_secrets)
    secrets_parser.add_argument('--type',
                                choices=["all"] + [i.name for i in SecretType if i != SecretType.generic],
                                default="all",
                                dest='secret_type',
                                help='Filter and show only secrets of this type')
    secrets_parser.add_argument('--ids',
                                action='store_true',
                                dest='include_ids',
                                default=config.ADMIN_MODE,
                                help='Include the secret ids in the output')
    runs_parser = get_runs_argparser(subparsers)
    add_common_arguments(runs_parser)
    deployments_parser = get_deployments_argparser(subparsers)
    add_common_arguments(deployments_parser)
    deployment_details_parsers = deployments_parser.add_subparsers(title='Deployment Details')

    # mcli get deployment logs
    add_log_parser(deployment_details_parsers, SubmissionType.INFERENCE)

    return parser


def add_get_argparser(subparser: argparse._SubParsersAction,
                      is_admin: bool = False,
                      parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    del parents

    get_parser: argparse.ArgumentParser = subparser.add_parser(
        'get',
        aliases=['g'],
        help='Get info about objects created with mcli',
    )
    get_parser = configure_argparser(parser=get_parser, is_admin=is_admin)
    return get_parser
