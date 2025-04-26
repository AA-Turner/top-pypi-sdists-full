#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

""" MCLI Entrypoint """
import argparse
import logging
import sys
from typing import Tuple

from mcli import config
from mcli.cli.m_connect.m_connect import add_connect_argparser
from mcli.cli.m_create.m_create import add_create_argparser
from mcli.cli.m_debug.m_debug import add_debug_argparser
from mcli.cli.m_delete.m_delete import add_delete_argparser
from mcli.cli.m_deploy.m_deploy import add_deploy_argparser
from mcli.cli.m_describe.m_describe import add_describe_parser
from mcli.cli.m_diff.m_diff import add_diff_argparser
from mcli.cli.m_get.m_get import add_get_argparser
from mcli.cli.m_init.m_init import initialize_mcli
from mcli.cli.m_interactive.m_interactive import add_interactive_argparser
from mcli.cli.m_kube.m_kube import add_kube_argparser
from mcli.cli.m_log.m_log import add_log_parser
from mcli.cli.m_ping.m_ping import add_ping_parser
from mcli.cli.m_predict.m_predict import add_predict_parser
from mcli.cli.m_root.m_config import m_get_config
from mcli.cli.m_run.m_run import add_run_argparser
from mcli.cli.m_set_unset.m_set import add_set_argparser
from mcli.cli.m_set_unset.m_unset import add_unset_argparser
from mcli.cli.m_stop.m_stop import add_stop_parser
from mcli.cli.m_update.m_update import add_update_argparser
from mcli.cli.m_util.m_util import add_util_argparser
from mcli.cli.m_watchdog.m_watchdog import add_watchdog_argparser
from mcli.utils.utils_cli import MCLIArgumentParser
from mcli.utils.utils_completers import apply_autocomplete
from mcli.utils.utils_logging import console_handler
from mcli.utils.utils_model import SubmissionType
from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available
from mcli.version import get_formatted_version, print_version

logger = logging.getLogger('mcli')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def add_root_commands(subparser: argparse._SubParsersAction) -> None:
    """Adds root level commands to the CLI

    Args:
        subparser: The subparser to add commands to
    """
    config_parser: argparse.ArgumentParser = subparser.add_parser(
        'config', aliases=['c'], help='Printout details on the current mcli configuration')
    config_parser.set_defaults(func=m_get_config)

    init_parser: argparse.ArgumentParser = subparser.add_parser('init', aliases=['i'], help='Initialize MCLI')
    mcloud_mode = init_parser.add_mutually_exclusive_group()
    mcloud_mode.add_argument(
        '--mcloud',
        action='store_true',
        # Not used or displayed to user, kept for backwards compatibilty in
        # case they have the `mcli init --mcloud` command lying around
        help=argparse.SUPPRESS,
    )
    init_parser.add_argument('--no-input', action='store_true', help='Do not query for user input')
    init_parser.set_defaults(func=initialize_mcli)

    version_parser: argparse.ArgumentParser = subparser.add_parser('version', help='MCLI Version')
    version_parser.set_defaults(func=print_version)


def get_mcli_root(name: str) -> Tuple[argparse.ArgumentParser, argparse._SubParsersAction]:
    """Common `mcli` root to be used by all subparsers

    This doesn't assume any local setup has been done yet
    """
    common = MCLIArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose', action='count', help='Increase CLI verbosity', default=0)
    common.add_argument('--version', action='version', help='MCLI version', version=get_formatted_version())
    parents = [common]

    parser = MCLIArgumentParser(prog=name, parents=parents)
    subparser = parser.add_subparsers(title='MCLI Commands',
                                      description='The table below shows the commands that are available',
                                      help='DESCRIPTION',
                                      metavar='COMMAND')

    def print_help(**kwargs):
        del kwargs
        parser.print_help()

    parser.set_defaults(func=print_help)

    add_root_commands(subparser=subparser)
    return parser, subparser


def get_parser(is_admin: bool = False) -> argparse.ArgumentParser:
    parser, subparser = get_mcli_root('mcli' if not is_admin else 'mcli-admin')

    # Commands that CREATE objects (eg. runs, deployments, secrets) are not
    # currently supported in admin mode. Allowing admins to create these
    # objects on behalf of other users is something that should be scoped
    # properly to avoid security issues.

    if not is_admin:
        # Hide connect for now because its not supported in MINT.
        # Will need to consider how to support this in the future.
        add_connect_argparser(subparser=subparser)
    add_create_argparser(subparser=subparser)
    if is_admin:
        add_debug_argparser(subparser=subparser)
    add_delete_argparser(subparser=subparser)
    if not is_admin:
        add_deploy_argparser(subparser=subparser)
    add_describe_parser(subparser=subparser, is_admin=is_admin)
    add_get_argparser(subparser=subparser, is_admin=is_admin)
    add_diff_argparser(subparser=subparser)
    if not is_admin:
        add_interactive_argparser(subparser=subparser)
    add_kube_argparser(subparser=subparser)
    add_log_parser(subparser=subparser, submission_type=SubmissionType.TRAINING)
    add_ping_parser(subparser=subparser)
    add_predict_parser(subparser=subparser)
    add_run_argparser(subparser=subparser, is_admin=is_admin)
    add_set_argparser(subparser=subparser, is_admin=is_admin)
    add_stop_parser(subparser=subparser, is_admin=is_admin)
    add_unset_argparser(subparser=subparser, is_admin=is_admin)
    add_update_argparser(subparser=subparser)
    add_util_argparser(subparser=subparser, is_admin=is_admin)
    add_watchdog_argparser(subparser=subparser)

    return parser


def _main(parser: argparse.ArgumentParser) -> int:
    try:
        check_new_update_available()
    except NeedsUpdateError:
        return 1

    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_help()
        return 0

    if args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    console_handler.markup = True

    var_args = vars(args)
    # Need to delete the custom args from the dict because they are added to `args` Namespace by default
    del var_args['verbose']
    try:
        return args.func(**var_args)
    except KeyboardInterrupt as k:
        del k
        logger.info('\nExiting with Keyboard Interrupt')
        return 1
    except Exception as e:
        raise e


def admin() -> int:
    """The admin entrypoint
    """

    config.ADMIN_MODE = True
    parser = get_parser(is_admin=True)
    return _main(parser)


def main() -> int:
    """The main entrypoint
    """
    parser = get_parser()
    apply_autocomplete(parser)
    return _main(parser)


if __name__ == '__main__':
    sys.exit(main())
