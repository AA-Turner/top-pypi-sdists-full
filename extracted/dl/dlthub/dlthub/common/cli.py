import os
import argparse
from typing import Optional

from dlthub.common.constants import DEFAULT_PROJECT_CONFIG_FILE


def add_project_opts(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project",
        default=None,
        help=f"Name or path to the dlt package with {DEFAULT_PROJECT_CONFIG_FILE}",
    )
    parser.add_argument(
        "--profile",
        default=os.getenv("DLT_PROJECT_CONFIG_PROFILE", None),
        help="Profile to use from the project configuration file",
    )


def get_existing_subparser(parser: argparse.ArgumentParser) -> Optional[argparse._SubParsersAction]:  # type: ignore[type-arg]
    """
    Retrieve the _SubParsersAction from an ArgumentParser instance.

    Args:
        parser (argparse.ArgumentParser): The parser from which to retrieve the subparsers action.

    Returns:
        Optional[argparse._SubParsersAction]: The subparsers action if found, else None.
    """
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action
    return None
