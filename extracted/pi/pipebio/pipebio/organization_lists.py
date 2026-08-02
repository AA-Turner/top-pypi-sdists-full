"""Operations on organization-level lists (workflows, scaffolds, germlines).

Organizations own reusable lists used across analyses. This module wraps the
``organizations/{id}/lists`` endpoints and is exposed as
:attr:`PipebioClient.organization_lists`.
"""

from typing import Any, List, Dict

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.util import Util


class OrganizationLists:
    """Wraps the ``organizations/{id}/lists`` API endpoints.

    Obtain an instance via :attr:`PipebioClient.organization_lists` rather than
    constructing it directly. When ``organization_id`` is omitted, the user's
    default organization is used.
    """

    _session: BaseUrlSession
    _url: str
    _user: Any

    def __init__(self, session: BaseUrlSession, user: Any) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
            user: The authenticated user object (used to resolve the default
                organization).
        """
        self._session = Util.mount_standard_session(session)
        self._url = 'organizations'
        self._user = user

    def get_workflow(self, workflow_id: str, organization_id: str = None) -> Any:
        """Fetch a single workflow list by id.

        Args:
            workflow_id: Id of the workflow list to fetch.
            organization_id: Organization id. Defaults to the user's default org.

        Returns:
            The workflow list object.

        Raises:
            ValueError: If the list is missing or is not of kind ``WORKFLOW``.

        .. API reference (generated - do not edit) ::

        **GET** ``/organizations/{organizationId}/lists/{listId}``

        Get one

        Returns a specific list within your organization.

        API parameters:
            * ``organizationId`` (path) -- Id of the organization that owns the list.
            * ``listId`` (path) -- Id of the organization list to fetch.

        .. end API reference ::
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        url = f'{self._url}/{_organization_id}/lists/{workflow_id}'
        response = self._session.get(url)

        Util.raise_detailed_error(response)

        workflow_json = response.json()

        if workflow_json is None:
            raise ValueError('Workflow not found')
        if workflow_json['kind'] != 'WORKFLOW':
            raise ValueError(f'A list was found for the given id "{workflow_id}" but it is not of type "WORKFLOW"')

        return workflow_json

    def get_scaffolds(self, organization_id: str = None) -> Any:
        """List the scaffold lists for an organization.

        Args:
            organization_id: Organization id. Defaults to the user's default org.

        Returns:
            The scaffolds response object.

        .. API reference (generated - do not edit) ::

        **GET** ``/organizations/{organizationId}/lists``

        List

        Returns all available lists in your organization and also those you own specifically.

        API parameters:
            * ``organizationId`` (path) -- Id of the organization that owns the lists.
            * ``kind`` (query) -- Filter lists by kind.

        .. end API reference ::
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        url = f'{self._url}/{_organization_id}/lists?kind=scaffold'
        response = self._session.get(url)

        Util.raise_detailed_error(response)

        return response.json()

    def get_germlines(self, organization_id: str = None) -> List[Dict[str, Any]]:
        """List the germline lists for an organization.

        Args:
            organization_id: Organization id. Defaults to the user's default org.

        Returns:
            The list of germline list objects.

        .. API reference (generated - do not edit) ::

        **GET** ``/organizations/{organizationId}/lists``

        List

        Returns all available lists in your organization and also those you own specifically.

        API parameters:
            * ``organizationId`` (path) -- Id of the organization that owns the lists.
            * ``kind`` (query) -- Filter lists by kind.

        .. end API reference ::
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = organization_id if organization_id is not None else Util.get_organization_id(self._user)

        url = f'{self._url}/{_organization_id}/lists?kind=germline'
        response = self._session.get(url)

        Util.raise_detailed_error(response)

        return response.json()['data']
