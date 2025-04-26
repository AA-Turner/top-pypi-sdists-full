""" m delete Entrypoint """
import argparse
from typing import List, Optional

from mcli.cli.common.run_filters import configure_submission_filter_argparser
from mcli.cli.m_delete.delete import delete_deployment, delete_run, delete_secret
from mcli.utils.utils_cli import CLIExample, Description, get_example_text
from mcli.utils.utils_model import SubmissionType

# pylint: disable-next=invalid-name
_description = Description("""
The table below shows the objects that you can delete. For each object below, you can
delete or more of them by name. Each object also supports glob-style selection and --all
to delete all.

To view object-specific additional help, run:

mcli delete <object> --help
""")

_secret_description = Description("""
Delete one or more secrets from your standard workload setup. These secrets will be
removed completely from the secrets database and no longer added to any subsequent runs.
""")
_secret_example_all = CLIExample(example='mcli delete secrets foo bar', description='Delete secrets foo and bar')
_secret_examples = [
    CLIExample(example='mcli delete secret foo', description='Delete a secret named foo'),
    _secret_example_all,
    CLIExample(example='mcli delete secrets --all', description='Delete all secrets'),
]

_run_description = Description("""
Delete a run or set of runs that match some conditions.
""")
_run_example_simple = CLIExample(example='mcli delete run my-run-1', description='Delete a specific run')
_run_example_status = CLIExample(example='mcli delete runs --status failed,completed',
                                 description='Delete all failed and completed runs')

_run_examples = [
    _run_example_simple,
    CLIExample(example='mcli delete runs --cluster rXzX,rXzY', description='Delete all runs on clusters rXzX and rXzY'),
    _run_example_status,
    CLIExample(example='mcli delete runs --all', description='Delete all runs (Please be careful!)'),
]

_deployments_description = Description("""
Delete a deployment or set of deployments by name.
""")

_deployments_example_simple = CLIExample(example='mcli delete deployment <deployment-name>',
                                         description='Delete a specific deployment')

_deployments_examples = [_deployments_example_simple]

_all_examples = [_secret_example_all, _run_example_simple, _run_example_status]


def delete(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument('-y',
                        '--force',
                        dest='force',
                        action='store_true',
                        help='Skip confirmation dialog before deleting. Please be careful!')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(
        title='MCLI Objects',
        help='DESCRIPTION',
        metavar='OBJECT',
    )
    parser.set_defaults(func=delete, parser=parser)

    # Delete a secret
    secrets_parser = subparsers.add_parser(
        'secret',
        aliases=['secrets'],
        help='Delete one or more secrets',
        description=_secret_description,
        epilog=get_example_text(*_secret_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    secrets_parser.add_argument('secret_names',
                                nargs='*',
                                metavar='SECRET',
                                help='The name(s) of the secrets to delete. Also supports glob-style pattern matching.')
    secrets_parser.add_argument('-a', '--all', dest='delete_all', action='store_true', help='Delete all secrets')
    secrets_parser.set_defaults(func=delete_secret)
    add_common_args(secrets_parser)

    # Delete a run
    run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Delete one or more runs',
        description=_run_description,
        epilog=get_example_text(*_run_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    run_parser.add_argument(
        dest='name_filter',
        nargs='*',
        metavar='RUN',
        default=None,
        help='String or glob of the name(s) of the runs to delete',
    )
    configure_submission_filter_argparser('delete', run_parser)
    run_parser.set_defaults(func=delete_run)
    add_common_args(run_parser)

    # Delete an inference deployment
    deployments_parser = subparsers.add_parser(
        'deployment',
        aliases=['deployments'],
        help='Delete one or more deployments',
        description=_deployments_description,
        epilog=get_example_text(*_deployments_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    deployments_parser.add_argument(
        dest='name_filter',
        nargs='*',
        metavar='DEPLOYMENT',
        default=None,
        help='String or glob of the name(s) of the deployments to delete',
    )
    # backwards compatibility
    deployments_parser.add_argument('--name', dest='old_name_filter')

    configure_submission_filter_argparser('delete', deployments_parser, submission_type=SubmissionType.INFERENCE)
    deployments_parser.set_defaults(func=delete_deployment)
    add_common_args(deployments_parser)

    return parser


def add_delete_argparser(subparser: argparse._SubParsersAction,
                         parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    del parents

    delete_parser: argparse.ArgumentParser = subparser.add_parser(
        'delete',
        aliases=['del'],
        help='Delete one or more MCLI objects',
        description=_description,
        epilog=get_example_text(*_all_examples),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    delete_parser = configure_argparser(parser=delete_parser)
    return delete_parser
