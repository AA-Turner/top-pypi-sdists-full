"""Operating Systems manager (IstariIntegrations surface).

``OperatingSystems`` does ``create`` / ``get`` / ``list`` / ``update``
against the v2 API, returning rich OperatingSystem objects.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._integrations.integration_types import OperatingSystem as OSType
from istari_digital_client.sdk._generated.v2.models.new_operating_system import NewOperatingSystem


class OperatingSystems(_Manager):
    """Manage operating systems (OS/platform targets): create / get / list / update.

    Aliases: os platform environment target


    Reached via ``integrations.operating_systems``. Operating systems are
    reference data for function variants and job targets (e.g., "Windows 11",
    "Ubuntu 22.04").

    Sub-managers: none (OperatingSystems is a leaf collection).

    Usage::

        # 1. Create a new OS entry
        os = integrations.operating_systems.create("Ubuntu 24.04")

        # 2. List all operating systems
        for os in integrations.operating_systems.list():
            print(os.name)

        # 3. Update an OS name
        updated = integrations.operating_systems.update(os.id, name="Ubuntu 24.04 LTS")
    """

    def create(self, name: str) -> OSType:
        """Create a new operating system entry.

        Mutates: true

        Args:
            name: The operating system name (e.g., "Windows 11", "Ubuntu 22.04").

        Returns:
            An OperatingSystem with fields: id (str), name (str), created (datetime).
        """
        dto = self._call(
            self._engine.v2_api.create_operating_system,
            NewOperatingSystem(name=name),
        )
        return OSType._bind(dto, mgr=self)

    def get(self, operating_system_id: str) -> OSType:
        """Fetch an operating system by its UUID.

        Args:
            operating_system_id: The UUID of the operating system to fetch.

        Returns:
            An OperatingSystem with fields: id (str), name (str), created (datetime).

        Raises:
            NotFoundError: If no operating system with that id exists.
        """
        dto = self._call(self._engine.v2_api.get_operating_system, operating_system_id)
        return OSType._bind(dto, mgr=self)

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        sort: str | None = None,
    ) -> Page[OSType]:
        """List operating systems (OS/platform targets), returning an auto-paging sequence.

        Aliases: os platform environment


        Iterating the returned Page automatically fetches subsequent pages.

        Args:
            page: Optional page number (1-indexed).
            size: Optional page size.
            sort: Sort field and order.

        Returns:
            A Page of OperatingSystem objects, each with fields: id, name, created.
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_operating_systems,
                page=page_num,
                size=size,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: OSType._bind(d, mgr=self), start_page=page or 1
        )

    def update(self, operating_system_id: str, *, name: str) -> OSType:
        """Update an operating system's name.

        Mutates: true

        Args:
            operating_system_id: The UUID of the operating system to update.
            name: The new name for the operating system.

        Returns:
            The updated OperatingSystem with fields: id, name, created.

        Raises:
            NotFoundError: If no operating system with that id exists.
        """
        dto = self._call(
            self._engine.v2_api.update_operating_system,
            operating_system_id,
            NewOperatingSystem(name=name),
        )
        return OSType._bind(dto, mgr=self)
