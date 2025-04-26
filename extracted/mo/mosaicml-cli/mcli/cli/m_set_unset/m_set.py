""" mcli set Entrypoint """
import argparse

from mcli.cli.m_set_unset.api_key import configure_api_key_argparser, modify_api_key
from mcli.cli.m_set_unset.feature_flag import use_feature_flag
from mcli.cli.m_set_unset.organization import configure_organization_argparser, modify_organization
from mcli.cli.m_set_unset.user import configure_user_argparser, modify_user


def set_entrypoint(**kwargs):
    del kwargs
    mock_parser = configure_argparser(parser=argparse.ArgumentParser())
    mock_parser.print_help()
    return 0


def configure_argparser(parser: argparse.ArgumentParser, is_admin: bool = False) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=set_entrypoint)

    feature_parser = subparsers.add_parser('feature', help='Activate a feature flag')
    feature_parser.add_argument('feature', nargs='?', help='The name of the feature flag')
    feature_parser.set_defaults(func=use_feature_flag, activate=True)

    api_key_parser = subparsers.add_parser(
        'api-key',
        help='Set a MosaicML platform API key that will be used in all of your subsequent workloads',
        description='Set a MosaicML platform API key that will be used in all of your subsequent workloads',
    )
    configure_api_key_argparser(api_key_parser)
    api_key_parser.set_defaults(func=modify_api_key)

    if is_admin:
        user_parser = subparsers.add_parser('user', help='Set the user id to use')
        configure_user_argparser(user_parser)
        user_parser.set_defaults(func=modify_user)

        org_parser = subparsers.add_parser('organization', aliases=['org'], help='Set the organization id to use')
        configure_organization_argparser(org_parser)
        org_parser.set_defaults(func=modify_organization)

    return parser


def add_set_argparser(subparser: argparse._SubParsersAction, is_admin: bool = False) -> argparse.ArgumentParser:
    """Adds the set parser to a subparser

    Args:
        subparser: the Subparser to add the Use parser to
    """
    set_parser: argparse.ArgumentParser = subparser.add_parser(
        'set',
        help='Set local configuration variables',
    )
    set_parser = configure_argparser(parser=set_parser, is_admin=is_admin)
    return set_parser
