"""Systems manager (Istari common-user surface).

``Systems`` does system CRUD (create / get / list / update / archive / restore)
and exposes ``branches``, ``change_requests``, and ``workflows`` as child-collection
sub-managers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Any

from istari_digital_client.sdk._base import Page
from istari_digital_client.sdk._common._capabilities import _SupportsAccess, _SupportsInfosec
from istari_digital_client.sdk._common.branches import Branches
from istari_digital_client.sdk._common.change_requests import ChangeRequests
from istari_digital_client.sdk._common.system_types import System
from istari_digital_client.sdk._common.workflows import Workflows
from istari_digital_client.sdk._generated.v2.models.new_system import NewSystem
from istari_digital_client.sdk._generated.v2.models.update_system import UpdateSystem


class Systems(_SupportsAccess, _SupportsInfosec):
    """Create, fetch, list, update, archive, and restore systems.

    Reached via ``istari.systems``. System-scoped CRUD lives directly on this
    manager; branch, change-request, and workflow operations are delegated to the
    ``branches``, ``change_requests``, and ``workflows`` sub-managers.

    Sub-managers:
      - ``branches`` — create, list, commit, and archive branches for any system.
      - ``change_requests`` — open, list, close, and reopen change requests.
      - ``workflows`` — log workflow run entries and upload output files.

    Usage::

        # 1. Create a system
        system = istari.systems.create("My System", "Description of my system")

        # 2. Get all branches (returns an auto-paging sequence)
        for branch in system.branches():
            print(branch.tag, branch.id)

        # 3. Create a change request proposing main → release
        main_branch = system.get_branch("main")
        release_branch = system.get_branch("release")
        cr = system.create_change_request(main_branch, release_branch, title="Promote to release")
        print(cr.change_request_id, cr.status)

        # 4. Log a workflow run
        entry = system.create_workflow(title="Simulation Run #1", status="SUCCESS")
        print(entry.id, entry.status)
    """

    @cached_property
    def branches(self) -> Branches:
        """Create, list, commit to, and merge branches (a.k.a. snapshots / versions) of a system.

        Aliases: branch snapshot version commit

        Use this to create, list, commit, and advance branches that belong to any
        system (e.g. ``istari.systems.branches.list(system_id)``).
        """
        return Branches(self._engine, systems_mgr=self)

    @cached_property
    def change_requests(self) -> ChangeRequests:
        """Open, list, merge, and close change requests (merge / pull requests) between branches.

        Aliases: change-request merge-request pull-request PR review

        Use this to open, list, close, and reopen change requests across any
        system (e.g. ``istari.systems.change_requests.create(system_id, ...)``).
        """
        return ChangeRequests(self._engine)

    @cached_property
    def workflows(self) -> Workflows:
        """Log, list, and fetch workflow runs (simulation / analysis run records) and their output files.

        Aliases: workflow run simulation analysis execution

        Use this to create, list, get, archive, and restore workflow log entries,
        and to upload workflow output files, for any system
        (e.g. ``istari.systems.workflows.create(system_id, title="Run #1")``).
        """
        return Workflows(self._engine)

    # ------------------------------------------------------------------ #
    # Capability hooks                                                     #
    # ------------------------------------------------------------------ #

    def _acl_ref(self, obj: Any) -> tuple[str, str]:
        return "system", obj.id

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        assert isinstance(
            obj, System
        ), f"Systems._archive expects System, got {type(obj).__name__}"
        self._call(self._engine.v2_api.archive_system, obj.id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        assert isinstance(
            obj, System
        ), f"Systems._restore expects System, got {type(obj).__name__}"
        self._call(self._engine.v2_api.restore_system, obj.id)

    # ------------------------------------------------------------------ #
    # System CRUD                                                          #
    # ------------------------------------------------------------------ #

    def create(self, name: str, description: str) -> System:
        """Create a new system with the given name and description.

        Mutates: true

        Both ``name`` and ``description`` are required. The returned object is
        immediately usable — its instance methods (``archive()``, ``branches()``,
        ``create_branch()``, etc.) work without any further setup.

        Returns a System with fields: id (str), name (str), description (str),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime),
        created_by_id (str).
        """
        dto = self._call(
            self._engine.v2_api.create_system,
            NewSystem(name=name, description=description),
        )
        return System._bind(dto, mgr=self)

    def get(self, system_id: str) -> System:
        """Fetch a single system by its UUID.

        Returns a System with fields: id (str), name (str), description (str),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime),
        created_by_id (str). Object methods: archive(), restore(), branches(),
        get_branch(), create_branch(), create_change_request(),
        list_change_requests(), list_workflows(), create_workflow().

        Raises NotFoundError if no system with that id exists.
        """
        dto = self._call(self._engine.v2_api.get_system, system_id)
        return System._bind(dto, mgr=self)

    def list(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        name: str | None = None,
        description: str | None = None,
        archive_status: str | None = None,
        filter_by: Any | None = None,
        sort: str | None = None,
    ) -> Page[System]:
        """List systems, returning an auto-paging sequence of System objects.

        Iterating the returned Page automatically fetches subsequent offset pages —
        no manual pagination is required.

        ``name`` and ``description`` perform substring filtering.
        ``archive_status`` filters by archive state: "ACTIVE" (default) | "ARCHIVED".
        ``filter_by`` passes a raw query expression to the registry API.
        ``sort`` controls result ordering.

        Each System in the page has fields: id (str), name (str), description (str),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime),
        created_by_id (str).
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_systems,
                page=page_num,
                size=size,
                name=name,
                description=description,
                archive_status=archive_status,
                filter_by=filter_by,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: System._bind(d, mgr=self), start_page=page or 1
        )

    def update(
        self,
        system_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> System:
        """Update a system's name and/or description.

        Mutates: true

        Aliases: rename edit

        Both fields are required by the registry. If only one is provided, the
        other is read from current state via an extra fetch. At least one of
        ``name`` or ``description`` should differ from the current value;
        passing unchanged values is a no-op that still succeeds.

        **Warning**: When only ``name`` or ``description`` is provided, this
        performs a read-modify-write (GET then UPDATE). Concurrent writes
        between the GET and UPDATE may be silently overwritten. To avoid this,
        always provide both fields, or ensure exclusive access.

        Returns the updated System with fields: id (str), name (str),
        description (str), archive_status (str: "ACTIVE" | "ARCHIVED"),
        created (datetime), created_by_id (str).

        Raises NotFoundError if no system with that id exists.
        """
        if name is None or description is None:
            current = self.get(system_id)
            name = name if name is not None else current.name
            description = (
                description if description is not None else current.description
            )
        dto = self._call(
            self._engine.v2_api.update_system,
            system_id,
            UpdateSystem(name=name, description=description),
        )
        return System._bind(dto, mgr=self)

    def archive(self, system_id: str) -> None:
        """Archive a system by its UUID.

        Mutates: true

        Archived systems are excluded from default list() results but can still be
        retrieved by passing ``archive_status="ARCHIVED"``. To archive via a rich
        System object, call ``system.archive()`` on the instance directly.

        Raises NotFoundError if no system with that id exists.
        """
        self._call(self._engine.v2_api.archive_system, system_id)

    def restore(self, system_id: str) -> System:
        """Restore a previously archived system.

        Mutates: true

        Returns the restored System with fields: id (str), name (str),
        description (str), archive_status (str: "ACTIVE" | "ARCHIVED"),
        created (datetime), created_by_id (str).

        Raises NotFoundError if no system with that id exists.
        Raises ConflictError if the system is already active.
        """
        dto = self._call(self._engine.v2_api.restore_system, system_id)
        return System._bind(dto, mgr=self)
