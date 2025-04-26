"""CLI getter for organization"""
import logging
from typing import Generator, List

from mcli.api.exceptions import cli_error_handler
from mcli.api.model.user import Organization
from mcli.api.organizations.api_get_organizations import get_organizations as api_get_organizations
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay

logger = logging.getLogger(__name__)


class OrganizationDisplay(MCLIGetDisplay):
    """`mcli get organizations` display class
    """

    def __init__(self, organizations: List[Organization]):
        self.organizations = sorted(organizations, key=lambda x: x.name)

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for o in self.organizations:
            yield MCLIDisplayItem({
                'organization_id': o.id,
                'organization_name': o.name,
            })

    @property
    def index_label(self) -> str:
        return 'organization_id'


@cli_error_handler('mcli get organizations')
def get_organizations(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    organizations = api_get_organizations()
    display = OrganizationDisplay(organizations)
    display.print(output)

    return 0
