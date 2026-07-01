"""Implementation of mcli describe user"""
from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Dict, Generator, List, Optional

from rich.table import Table

from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.users.api_get_users import User, get_current_user, get_users
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table
from mcli.utils.utils_logging import FormatString, format_string
from mcli.version import print_version

logger = logging.getLogger(__name__)


class MCLIDescribeUserDisplay(MCLIGetDisplay):
    """ Vertical table view of user details """

    def __init__(self, user: User):
        self.user = user

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, data: List[Dict[str, str]]) -> Optional[Table]:
        return create_vertical_display_table(data=data[0])

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        organization_names = '\n'.join([f'- {org.name} ({org.id})' for org in self.user.organizations]) if len(
            self.user.organizations) > 0 else "None"
        display_config = {
            'ID': self.user.id,
            'Name': self.user.name,
            'Email': self.user.email,
            'Organizations': organization_names,
        }
        item = MCLIDisplayItem(display_config)
        yield item


@cli_error_handler("mcli describe user")
def describe_user(user_identifier: str | None, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a User
    """
    del kwargs
    args = {}
    if user_identifier is not None:

        if user_identifier.find('@') != -1:
            args['user_emails'] = [user_identifier]
        else:
            args['users'] = [user_identifier]
    else:
        raise MAPIException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            'User ID or email must be provided.',
        )
    users = get_users(**args)

    if not users:
        raise MAPIException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f'User {user_identifier} not found.',
        )

    print(format_string('User Details', FormatString.BOLD))
    user_display = MCLIDescribeUserDisplay(users[0])
    user_display.print(output)


@cli_error_handler("mcli describe me")
def describe_me(output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    del kwargs

    print_version()

    user = get_current_user()

    print(format_string('User Details', FormatString.BOLD))
    user_display = MCLIDescribeUserDisplay(user)
    user_display.print(output)
