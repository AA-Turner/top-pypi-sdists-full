"""Operations on PipeBio shareables (projects).

A *shareable* is the ownership/permission boundary around a set of entities -
most commonly a project. This module wraps the ``shareables`` endpoints and is
exposed as :attr:`PipebioClient.shareables`.
"""

import csv
from io import StringIO
from typing import List

from requests_toolbelt.sessions import BaseUrlSession

from pipebio.util import Util


class Shareables:
    """Wraps the ``shareables`` API endpoints.

    Obtain an instance via :attr:`PipebioClient.shareables` rather than
    constructing it directly.
    """

    def __init__(self, session: BaseUrlSession) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
        """
        self._url = 'shareables'
        self._session = session

    def list(self) -> List[dict]:
        """List the shareables (projects) the user can access.

        Returns:
            The list of shareable objects.

        .. API reference (generated - do not edit) ::

        **GET** ``/shareables``

        List

        List all shareables for the current user.

        API parameters:
            * ``sort`` (query) -- Sort expression in the form "columnName:asc" or "columnName:desc".
            * ``type`` (query) -- Filter shareables by type (e.g. project).

        .. end API reference ::
        """
        response = self._session.get(self._url)

        print(f'ShareablesService:list - response:{response.status_code}')

        Util.raise_detailed_error(response)

        return response.json()['data']

    def create_project(self, name: str, owner_id: str) -> dict:
        """Create a new project shareable.

        Args:
            name: Display name for the project.
            owner_id: Id of the owning organization/user.

        Returns:
            The created project object.

        .. API reference (generated - do not edit) ::

        **POST** ``/shareables``

        Create

        Create a new shareable (project) and configure initial settings such as membership, privacy etc

        API request body:
            * ``type`` -- Type of shareable to create (currently always a project).
            * ``name`` -- Name of the new project.
            * ``description`` (optional) -- Optional description of the project.
            * ``ownerId`` -- Copy your organization id from the admin settings page
            * ``members`` (optional) -- Users to grant access to, with their permission levels.
            * ``labels`` (optional) -- Optional labels used to categorise the project.

        .. end API reference ::
        """
        response = self._session.post(self._url, json={
            'name': name,
            'type': 'PROJECT',
            'ownerId': owner_id,
        })

        print(f'ShareablesService:create - response:{response.status_code}')

        Util.raise_detailed_error(response)

        return response.json()

    def list_entities(self, shareable_id: str) -> List[dict]:
        """List the entities contained in a shareable.

        Args:
            shareable_id: Id of the shareable (project) to list entities from.

        Returns:
            The entities as a list of dict rows parsed from the TSV response.

        .. API reference (generated - do not edit) ::

        **GET** ``/shareables/{id}/entities``

        List entities

        List all entities for the given project.

        API parameters:
            * ``id`` (path) -- Id of the shareable (project) to list entities for.
            * ``visible`` (query) -- If true, only return entities that are visible.
            * ``deleted`` (query) -- If true, only return entities that have been soft-deleted.
            * ``parentId`` (query) -- Only return direct children of this parent entity id.

        .. end API reference ::
        """
        url = f'{self._url}/{shareable_id}/entities'

        response = self._session.get(url)

        print(f'ShareablesService:list_entities - response:{response.status_code}')

        Util.raise_detailed_error(response)

        file = StringIO(response.text)
        reader = csv.DictReader(file, dialect='excel-tab')
        rows = []
        for row in reader:
            rows.append(row)
        return rows

    def get_project(self, project_name: str) -> dict:
        """Find a project by its exact name.

        Args:
            project_name: The exact project name to look for.

        Returns:
            The matching project object.

        Raises:
            Exception: If no project with that name is found.
        """
        projects = self.list()

        # Find a specific project having a name "Example".
        project = next((project for project in projects if project['name'] == project_name), None)
        if project is None:
            raise Exception(f'Error: Project named "{project_name}" not found')

        return project