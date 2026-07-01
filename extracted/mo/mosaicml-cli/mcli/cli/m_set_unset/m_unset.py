""" mcli unset Entrypoint """
import argparse

from mcli.cli.m_set_unset.feature_flag import use_feature_flag
from mcli.cli.m_set_unset.organization import modify_organization
from mcli.cli.m_set_unset.user import modify_user


def unset_entrypoint(**kwargs):
    del kwargs
    mock_parser = configure_argparser(parser=argparse.ArgumentParser())
    mock_parser.print_help()
    return 0


def configure_argparser(parser: argparse.ArgumentParser, is_admin: bool = False) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=unset_entrypoint)

    feature_parser = subparsers.add_parser('feature', help='Deactivate a feature flag')
    feature_parser.add_argument('feature', nargs='?', help='The name of the feature flag')
    feature_parser.set_defaults(func=use_feature_flag, activate=False)

    if is_admin:
        user_parser = subparsers.add_parser('user', help='Unset the user id')
        user_parser.set_defaults(func=modify_user)

        org_parser = subparsers.add_parser('organization', aliases=['org'], help='Unset the organization id')
        org_parser.set_defaults(func=modify_organization)

    return parser


def add_unset_argparser(subparser: argparse._SubParsersAction, is_admin: bool = False) -> argparse.ArgumentParser:
    """Adds the unset parser to a subparser

    Args:
        subparser: the Subparser to add the Use parser to
    """
    unset_parser: argparse.ArgumentParser = subparser.add_parser(
        'unset',
        help='Unset local configuration variables',
    )
    unset_parser = configure_argparser(parser=unset_parser, is_admin=is_admin)
    return unset_parser
