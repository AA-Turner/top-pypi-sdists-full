"""CLI getter for users"""
import logging
from typing import Generator

from mcli.api.exceptions import cli_error_handler
from mcli.api.users.api_get_users import get_users as api_get_users
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay

logger = logging.getLogger(__name__)


class UserDisplay(MCLIGetDisplay):
    """`mcli get users` display class
    """

    def __init__(self, users):
        users = [
            MCLIDisplayItem({
                'organization_id': o.id,
                'organization_name': o.name,
                'id': u.id,
                'name': u.name,
                'email': u.email,
            }) for u in users for o in u.organizations
        ]

        def sort_key(x: MCLIDisplayItem) -> str:
            return f'{x.__getattribute__("organization_name")}-{x.__getattribute__("email")}'

        self.users = sorted(users, key=sort_key)

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        last_org = None
        for u in self.users:
            org_id = u.__getattribute__('organization_id')
            if last_org == org_id:
                u.__setattr__('organization_id', '')
                u.__setattr__('organization_name', '')

            yield u

            last_org = org_id

    @property
    def index_label(self) -> str:
        return 'organization_id'


@cli_error_handler('mcli get users')
def get_users(org_id: str, output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    users = api_get_users(organization=org_id)
    display = UserDisplay(users)
    display.print(output)

    return 0
