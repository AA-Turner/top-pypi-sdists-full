"""Rich system domain types: System, Branch, ChangeRequest."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from istari_digital_client.sdk._base import Archivable, Classifiable, ClientHaving, Page, Shareable
from istari_digital_client.sdk._exceptions import NotFoundError
from istari_digital_client.sdk._generated.v2.models.open_change_request_response import (
    OpenChangeRequestResponse as _GenOpenCR,
)
from istari_digital_client.sdk._generated.v2.models.snapshot_subsystem_item import (
    SnapshotSubsystemItem as _GenSnapshotSubsystemItem,
)
from istari_digital_client.sdk._generated.v2.models.snapshot_tag import SnapshotTag as _GenSnapshotTag
from istari_digital_client.sdk._generated.v2.models.system import System as _GenSystem

if TYPE_CHECKING:
    from istari_digital_client.sdk._base import _Manager
    from istari_digital_client.sdk._common.branches import Branches
    from istari_digital_client.sdk._common.change_requests import ChangeRequests
    from istari_digital_client.sdk._common.systems import Systems
    from istari_digital_client.sdk._common.resource_types import TrackedResource
    from istari_digital_client.sdk._common.workflow_types import WorkflowLogEntry


class System(_GenSystem, ClientHaving, Archivable, Shareable, Classifiable):
    """A system (project / version-controlled model container) holding branches and change requests.

    Aliases: project model-tree container repository


    A system is a version-controlled container that holds branches and change
    requests. Systems nest: a branch can track other systems as subsystems
    (child systems pinned to one of their branches) — see ``subsystems()``.
    All branch, subsystem and change-request operations are available directly
    on the instance — no manager reference is needed by callers.

    Fields: id (str), name (str), description (str),
    archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime),
    created_by_id (str).

    Object methods: archive(), restore(), branches(), get_branch(),
    subsystems(), create_branch(), create_change_request(),
    list_change_requests(), list_workflows(), create_workflow().

    Usage::

        # 1. Create a system
        system = istari.systems.create("Sim Platform", "Primary simulation system")

        # 2. List its branches
        for branch in system.branches():
            print(branch.tag, branch.id)

        # 3. Create a branch seeded from an existing one
        feature = system.create_branch("feature/new-model", from_branch=system.get_branch("main"))

        # 4. Open a change request and close it
        cr = system.create_change_request(feature, system.get_branch("main"), title="Add new model")
        print(cr.change_request_id, cr.status)  # status is "OPEN"
        cr.close()
    """

    if TYPE_CHECKING:
        _mgr: Systems  # narrows from _Manager

    def branches(self, *, archive_status: str | None = None) -> "Page[Branch]":
        """List all branches of this system.

        ``archive_status`` filters by archive state: "ACTIVE" (default) | "ARCHIVED".

        Returns an auto-paging sequence of Branch objects. Each Branch has fields:
        id (str), tag (str — the branch name), snapshot_id (str), is_baseline (bool),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime).
        Object methods on each Branch: archive(), restore(), resources(), commit(),
        create_change_request().

        Iterate directly — subsequent pages are fetched automatically.
        """
        return self._mgr.branches.list(self.id, archive_status=archive_status)

    def get_branch(self, name: str) -> "Branch":
        """Fetch a single branch of this system by its tag name.

        Scans all pages until an exact name match is found.

        Returns a Branch with fields: id (str), tag (str — the branch name),
        snapshot_id (str), is_baseline (bool), archive_status (str: "ACTIVE" |
        "ARCHIVED"), created (datetime). Object methods: archive(), restore(),
        resources(), commit(), create_change_request().

        Raises NotFoundError if no branch with that name exists on this system.
        """
        return self._mgr.branches.get(self.id, name)

    def baseline_branch(self) -> "Branch":
        """Return this system's baseline branch (the one with ``is_baseline`` true)."""
        for branch in self._mgr.branches.list(self.id):
            if getattr(branch, "is_baseline", False):
                return branch
        raise NotFoundError(f"System {self.id!r} has no baseline branch")

    def resources(self, *, name: str | None = None) -> "Page[TrackedResource]":
        """List the resources tracked on this system's baseline branch (METADATA only).

        Answers "list the resources / models / artifacts / files in this system". A
        convenience for ``baseline_branch().resources()`` — for another branch, use
        ``get_branch(name).resources()``.

        Aliases: files file model artifact
        """
        return self.baseline_branch().resources(name=name)

    def subsystems(self) -> "Page[Subsystem]":
        """List the subsystems (child systems) tracked on this system's baseline branch.

        Answers "does this system have subsystems / child systems / nested systems"
        and "list the subsystems of this system". A convenience for
        ``baseline_branch().subsystems()`` — for another branch, use
        ``get_branch(name).subsystems()``. Empty when the system tracks no subsystems.

        Each :class:`Subsystem` carries the child's ``system_id`` / ``system_name`` /
        ``system_description`` and the child branch it is pinned to; call
        ``.system()`` for the full child System or ``.branch()`` for that branch.

        Aliases: subsystem sub-system child-system nested component
        """
        return self.baseline_branch().subsystems()

    def contents(
        self,
        *,
        name: str | None = None,
        max_chars_per_file: int | None = None,
        include_extracted: bool = False,
    ) -> "list[dict]":
        """Summarize this system — read its resources AND their content in one call.

        The one call for "summarize this system" / "tell me about this system" /
        "what is in this system". A convenience for ``baseline_branch().contents()``:
        every tracked resource's metadata plus, for text/JSON/data resources, the
        decoded ``content`` inline (binary → ``content=None``). For a specific branch,
        use ``get_branch(name).contents()``.

        By default each file's ``content`` is the FULL text. Pass ``max_chars_per_file``
        for a bounded SURVEY — each file capped, with a marker naming the resource id to
        read in full — when handing the result to an LLM or when files may be large, so
        it fits one context window; for one file's full content, read it directly.

        Set ``include_extracted=True`` to also read what is inside every connected-file
        pointer (DOORS/Confluence/SharePoint/Teamwork Cloud/Jira), whose extracted
        records a listing never shows — the complete survey to run BEFORE concluding a
        fact is absent. Let the reader judge each row rather than keyword-filtering it.
        Extracted rows carry ``extracted_from``.

        Aliases: summarize summary overview describe tell-me-about whats-in read-all
        contents search find where-is locate full-text sweep
        """
        return self.baseline_branch().contents(
            name=name,
            max_chars_per_file=max_chars_per_file,
            include_extracted=include_extracted,
        )

    def create_branch(
        self,
        name: str,
        *,
        from_branch: "Branch | None" = None,
    ) -> "Branch":
        """Create a new branch on this system.

        Mutates: true

        If ``from_branch`` is provided the new branch is seeded from its snapshot;
        otherwise the system's baseline snapshot is used. ``name`` must be unique
        within this system.

        Returns the new Branch with fields: id (str), tag (str — the branch name),
        snapshot_id (str), is_baseline (bool), archive_status (str: "ACTIVE" |
        "ARCHIVED"), created (datetime). Object methods: archive(), restore(),
        resources(), commit(), create_change_request().

        Raises ConflictError if a branch with that name already exists on this system.
        """
        return self._mgr.branches.create(self.id, name, from_branch=from_branch)

    def create_change_request(
        self,
        source: "Branch",
        target: "Branch",
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> "ChangeRequest":
        """Open a change request proposing to merge ``source`` into ``target``.

        Mutates: true

        ``source`` and ``target`` must be branches that belong to this system.
        ``title`` and ``description`` are optional human-readable metadata.

        Returns a ChangeRequest with fields: change_request_id (str, also .id),
        status (str: "OPEN" | "CLOSED"), source_tag_id (str), target_tag_id (str),
        system_id (str), current_source_snapshot_id (str),
        current_target_snapshot_id (str), current_source_tag_revision_id (str),
        current_target_tag_revision_id (str), title (str | None),
        description (str | None), created (datetime), created_by_id (str).
        Object methods: close(), reopen().
        """
        return self._mgr.change_requests.create(
            self.id, source.id, target.id, title=title, description=description
        )

    def list_change_requests(
        self,
        *,
        status: str | None = None,
        source_tag_id: str | None = None,
        target_tag_id: str | None = None,
    ) -> "Page[ChangeRequest]":
        """List change requests for this system.

        ``status`` filters by change request state: "OPEN" | "CLOSED".
        ``source_tag_id`` and ``target_tag_id`` filter by the UUID of the
        source or target branch respectively. All filters are optional.

        Returns an auto-paging sequence of ChangeRequest objects. Each has fields:
        change_request_id (str, also .id), status (str: "OPEN" | "CLOSED"),
        source_tag_id (str), target_tag_id (str), system_id (str),
        current_source_snapshot_id (str), current_target_snapshot_id (str),
        current_source_tag_revision_id (str), current_target_tag_revision_id (str),
        title (str | None), description (str | None), created (datetime),
        created_by_id (str). Object methods: close(), reopen().

        Iterate directly — subsequent pages are fetched automatically.
        """
        return self._mgr.change_requests.list(
            self.id,
            status=status,
            source_tag_id=source_tag_id,
            target_tag_id=target_tag_id,
        )

    def list_workflows(
        self,
        *,
        size: int | None = None,
        branch_id: list[str] | None = None,
        title: list[str] | None = None,
        status: list[str] | None = None,
        archive_status: str | None = None,
    ) -> "Page[WorkflowLogEntry]":
        """List workflow runs (simulation / analysis run records) for this system.

        ``branch_id``, ``title``, and ``status`` each accept a list of strings
        for OR filtering; prefix a value with "!" to negate it.
        ``status`` values: "SUCCESS" | "FAILED" | "UNSPECIFIED" | "RUNNING" | "CANCELED".
        ``archive_status`` filters by archive state: "ACTIVE" (default) | "ARCHIVED" | "all".

        Returns an auto-paging sequence of WorkflowLogEntry objects. Each entry has
        fields: id (str), system_id (str), title (str | None), status (str: "SUCCESS" |
        "FAILED" | "UNSPECIFIED" | "RUNNING" | "CANCELED"), workflow_type (str),
        configuration_id (str | None), branch_id (str | None), branch_name (str | None),
        branchless (bool), file_count (int), total_file_size (int, bytes),
        archived (bool), created (datetime), created_by_id (str).
        Object methods: archive(), restore().

        Entries returned here do not have their outputs list populated. Call
        ``istari.systems.workflows.get(system_id, entry.id)`` to retrieve a single
        entry with its outputs.

        Iterate directly — subsequent pages are fetched automatically.
        """
        return self._mgr.workflows.list(
            self.id,
            size=size,
            branch_id=branch_id,
            title=title,
            status=status,
            archive_status=archive_status,
        )

    def create_workflow(
        self,
        *,
        title: str | None = None,
        status: str = "UNSPECIFIED",
        workflow_type: str = "external",
        configuration_id: str | None = None,
        branch_id: str | None = None,
        branchless: bool = False,
        output_ids: list[str] | None = None,
    ) -> "WorkflowLogEntry":
        """Log a workflow run (record a simulation / analysis run) for this system.

        Mutates: true

        Aliases: log record run simulation analysis


        ``title`` names the run. ``status`` records the outcome:
        "UNSPECIFIED" (default) | "SUCCESS" | "FAILED" | "RUNNING" | "CANCELED".
        ``workflow_type`` identifies the kind of workflow (default: "external").
        Pass ``branch_id`` to link the entry to a branch, or ``branchless=True``
        for runs with no branch provenance. Pass ``output_ids`` to attach
        previously created workflow output files by UUID.

        Returns a WorkflowLogEntry with fields: id (str), system_id (str),
        title (str | None), status (str: "SUCCESS" | "FAILED" | "UNSPECIFIED" |
        "RUNNING" | "CANCELED"), workflow_type (str), configuration_id (str | None),
        branch_id (str | None), branch_name (str | None), branchless (bool),
        file_count (int), total_file_size (int, bytes), archived (bool),
        created (datetime), created_by_id (str). Object methods: archive(), restore().

        The returned entry has an empty outputs list even if output_ids were supplied —
        call ``istari.systems.workflows.get(system_id, entry.id)`` to retrieve the
        entry with outputs populated.
        """
        return self._mgr.workflows.create(
            self.id,
            title=title,
            status=status,
            workflow_type=workflow_type,
            configuration_id=configuration_id,
            branch_id=branch_id,
            branchless=branchless,
            output_ids=output_ids,
        )


class Branch(_GenSnapshotTag, ClientHaving, Archivable):
    """A branch (named snapshot / version) of a system's tracked files.

    Aliases: snapshot version


    A branch is a named pointer to a configuration snapshot within a system. You
    can list its tracked files and the subsystems (child systems) it tracks,
    advance it by committing file revisions, and open change requests from it.

    Fields: id (str), tag (str — the branch name), snapshot_id (str),
    is_baseline (bool), archive_status (str: "ACTIVE" | "ARCHIVED"),
    created (datetime).

    Object methods: archive(), restore(), resources(), subsystems(), search(),
    commit(), create_change_request().

    Usage::

        # List tracked files on the branch — each is a readable resource that
        # also carries its branch git-context.
        for f in branch.resources():
            print(f.path, f.name, f.size, f.specifier_type)
            text = f.read_text()

        # Search the branch's resources
        for f in branch.search(name=["report"]):
            print(f.path, f.name)

        # Commit a new file revision onto the branch
        updated = branch.commit(add=[revision], remove=[old_revision])

        # Open a change request from this branch into main
        main = system.get_branch("main")
        cr = branch.create_change_request(main, title="Promote my changes")
    """

    _system_id: str
    # ``_systems_mgr`` is a second live manager ref and must be detached alongside
    # ``_mgr`` on copy/serialize; ``_system_id`` is plain data and rides along.
    _TRANSIENT_ATTRS: ClassVar[frozenset[str]] = frozenset({"_mgr", "_systems_mgr"})

    if TYPE_CHECKING:
        _mgr: Branches  # narrows from _Manager
        _systems_mgr: Systems  # narrows from Any

    @classmethod
    def _bind_with_system(
        cls, dto: Any, *, mgr: "_Manager", system_id: str, systems_mgr: Any
    ) -> "Branch":
        """Rebind a generated SnapshotTag DTO to a rich Branch in place (zero-copy).

        Factory used internally whenever a Branch needs to be returned. Injects
        the owning system's UUID and a reference to the Systems manager so that
        commit and change-request helpers work without additional lookups.
        """
        dto.__class__ = cls
        object.__setattr__(dto, "_mgr", mgr)
        object.__setattr__(dto, "_system_id", system_id)
        object.__setattr__(dto, "_systems_mgr", systems_mgr)
        return dto

    def resources(self, *, name: str | None = None) -> "Page[TrackedResource]":
        """List this branch's tracked resources — models, artifacts, files (METADATA only).

        Answers "list the resources / models / artifacts / files in this branch". Pass
        ``name`` to filter by a case-insensitive substring match on the resource name.

        Returns an auto-paging sequence of :class:`TrackedResource` objects, one per
        tracked resource — each a full resource (``resource_id``, ``name``, ``size``,
        ``description``, ``mime``, ``resource_type``, ``path``, ...). This is the
        listing; it does NOT read content. Use :meth:`contents` to get the content
        of every tracked resource in one call.

        Tracked resources with no ``resource_id`` (a known data gap) are logged and
        omitted rather than silently misrouted.

        Aliases: files file model artifact
        """
        return self._mgr.resources(self, name=name)

    def subsystems(self) -> "Page[Subsystem]":
        """List the subsystems (child systems) tracked on this branch.

        Answers "does this branch have subsystems / child systems / nested systems"
        and "list the subsystems of this branch". Systems nest: alongside its files a
        branch tracks other systems, each pinned to a specific branch of the child.
        Empty when the branch tracks no subsystems.

        Each :class:`Subsystem` carries the child's ``system_id`` / ``system_name`` /
        ``system_description`` and the pinned ``tag_id`` / ``tagged_snapshot_id``;
        call ``.system()`` for the full child System or ``.branch()`` for the pinned
        child Branch.

        Aliases: subsystem sub-system child-system nested component
        """
        return self._mgr.subsystems(self)

    def contents(
        self,
        *,
        name: str | None = None,
        max_chars_per_file: int | None = None,
        include_extracted: bool = False,
    ) -> "list[dict]":
        """Summarize this branch — read its tracked resources AND their content in one call.

        The one call for "summarize this branch" / "what is in this branch". For every
        tracked resource it returns the metadata plus, for text/JSON/data resources,
        the decoded ``content`` inline — so you never make a second per-file read.
        Binary resources (CAD, mesh, image) come back with ``content=None`` (their
        bytes are not summarizable; use ``read_bytes()`` only if you need them).

        By default each file's ``content`` is the FULL text. Pass ``max_chars_per_file``
        for a bounded SURVEY — each file capped, with a marker naming the resource id to
        read in full — when handing the result to an LLM or when files may be large, so
        it fits one context window; for one file's full content, read it directly.

        Set ``include_extracted=True`` to also read what is inside every connected-file
        pointer (DOORS/Confluence/SharePoint/Teamwork Cloud/Jira) — those extracted
        records are otherwise invisible to a branch listing. This is the complete survey
        to run BEFORE concluding a fact is not in the system; let the reader judge each
        row rather than keyword-filtering it. Extracted rows carry ``extracted_from``.

        Each row: ``{resource_id, name, resource_type, description, path, mime,
        size, content}`` (extracted rows add ``extracted_from``). Use :meth:`resources`
        when you only need the listing.

        Aliases: summarize summary overview describe tell-me-about whats-in read-all
        contents search find where-is locate full-text sweep
        """
        return self._mgr.contents(
            self,
            name=name,
            max_chars_per_file=max_chars_per_file,
            include_extracted=include_extracted,
        )

    def search(
        self,
        *,
        name: list[str] | None = None,
        type_name: list[str] | None = None,
        version_name: list[str] | None = None,
        description: list[str] | None = None,
        external_identifier: list[str] | None = None,
        display_name: list[str] | None = None,
        mime_type: list[str] | None = None,
    ) -> "Page[TrackedResource]":
        """Search the resources tracked on this branch.

        Like :meth:`files`, but with the resource filters of ``Resources.list``
        scoped to just this branch's tracked files. Every parameter accepts
        multiple values treated as OR filters and matches as a case-insensitive
        substring. Returns an auto-paging sequence of :class:`TrackedResource`.

        Example::

            for f in branch.search(name=["report"], type_name=["model"]):
                print(f.path, f.name)
        """
        return self._mgr.search(
            self,
            name=name,
            type_name=type_name,
            version_name=version_name,
            description=description,
            external_identifier=external_identifier,
            display_name=display_name,
            mime_type=mime_type,
        )

    def commit(
        self,
        *,
        add: list[Any] | None = None,
        remove: list[Any] | None = None,
    ) -> "Branch":
        """Commit file revisions onto this branch (add/remove tracked files), creating a new snapshot.

        Mutates: true

        Aliases: commit add-file stage update


        ``add`` is a list of revision-like objects (identified by ``.id``, the
        revision id) to include in the new snapshot as LOCKED tracked files.
        ``remove`` is a list of revision-like objects whose ``.id`` will be
        dropped from the tracked file list. Both are optional.

        Returns the updated Branch with its snapshot_id pointing at the new
        snapshot. Fields: id (str), tag (str), snapshot_id (str),
        is_baseline (bool), archive_status (str: "ACTIVE" | "ARCHIVED"),
        created (datetime).
        """
        return self._mgr.commit(self, add=add, remove=remove)

    def create_change_request(
        self,
        target: "Branch",
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> "ChangeRequest":
        """Open a change request with this branch as the source.

        Mutates: true

        ``target`` is the branch to merge into; it must belong to the same system
        as this branch. ``title`` and ``description`` are optional metadata.

        Returns a ChangeRequest with fields: change_request_id (str, also .id),
        status (str: "OPEN" | "CLOSED"), source_tag_id (str), target_tag_id (str),
        system_id (str), current_source_snapshot_id (str),
        current_target_snapshot_id (str), current_source_tag_revision_id (str),
        current_target_tag_revision_id (str), title (str | None),
        description (str | None), created (datetime), created_by_id (str).
        Object methods: close(), reopen().
        """
        return self._systems_mgr.change_requests.create(
            self._system_id, self.id, target.id, title=title, description=description
        )


class Subsystem(_GenSnapshotSubsystemItem, ClientHaving):
    """A child system tracked by a branch, pinned to one of the child's branches.

    Aliases: sub-system child-system nested component

    Returned by ``system.subsystems()`` / ``branch.subsystems()``. Systems nest:
    alongside its files a branch tracks other systems, and each entry pins the
    child to a specific branch (and snapshot) of that child system.

    Fields: system_id (str — the child system's id), system_name (str),
    system_description (str | None), tag_id (str — the pinned child branch's id),
    tagged_configuration_id (str), tagged_configuration_name (str — the child
    configuration that branch points at), tagged_snapshot_id (str — the child
    snapshot the parent pins), is_archived (bool — the child system is archived),
    created (datetime), created_by_id (str).

    Object methods: system() — the child as a full System; branch() — the child
    Branch viewed at the pinned snapshot (what the parent tracks).

    Usage::

        for sub in system.subsystems():
            print(sub.system_name, sub.system_id)
            child = sub.system()    # full System: .branches(), .resources(), .contents()
            pinned = sub.branch()   # the child Branch the parent tracks
            for f in pinned.resources():
                print(f.path, f.name)
    """

    if TYPE_CHECKING:
        _mgr: Branches  # narrows from _Manager

    def system(self) -> "System":
        """Fetch the child system as a full :class:`System` (branches, resources, contents, ...).

        Aliases: open get resolve child
        """
        return self._mgr._systems_mgr.get(self.system_id)

    def branch(self) -> "Branch":
        """Fetch the child branch this entry pins, viewed at the pinned snapshot.

        The returned Branch's ``snapshot_id`` is ``tagged_snapshot_id`` — what the
        parent tracks and what the system tree shows — so ``.resources()`` /
        ``.contents()`` / ``.subsystems()`` read exactly that content even if the
        child branch has since advanced. It is a read view: ``commit()`` on it
        raises; to change the child, use ``system().get_branch(name)``.

        Aliases: pinned child
        """
        return self._mgr._branch_by_id(
            self.system_id, self.tag_id, snapshot_id=self.tagged_snapshot_id
        )


class ChangeRequest(_GenOpenCR, ClientHaving):
    """A change request (merge / pull request) proposing to merge one branch into another.

    Aliases: change-request merge-request pull-request PR review


    A change request proposes merging a source branch into a target branch within
    a system. Use close(), reopen(), and merge() to manage its lifecycle.

    Fields: change_request_id (str, also .id), status (str: "OPEN" | "CLOSED" | "MERGED"),
    source_tag_id (str), target_tag_id (str), system_id (str),
    current_source_snapshot_id (str), current_target_snapshot_id (str),
    current_source_tag_revision_id (str), current_target_tag_revision_id (str),
    title (str | None), description (str | None), created (datetime),
    created_by_id (str).

    Object methods: close(), reopen(), merge().
    """

    _system_id: str

    if TYPE_CHECKING:
        _mgr: ChangeRequests  # narrows from _Manager

    @classmethod
    def _from_response(
        cls, response: Any, *, mgr: "_Manager", system_id: str
    ) -> "ChangeRequest":
        """Construct a ChangeRequest by unwrapping the OneOf API response wrapper.

        Internal factory. Extracts the actual instance from the polymorphic OneOf
        container, copies its fields without re-validation, and injects manager
        references for subsequent instance-method calls. Fields that may be absent
        on certain CR subtypes are read with empty-string defaults.
        """
        actual = response.actual_instance
        cr = cls.model_construct(
            status=actual.status,
            change_request_id=actual.change_request_id,
            system_id=actual.system_id,
            source_tag_id=actual.source_tag_id,
            target_tag_id=actual.target_tag_id,
            current_source_snapshot_id=getattr(
                actual, "current_source_snapshot_id", ""
            ),
            current_target_snapshot_id=getattr(
                actual, "current_target_snapshot_id", ""
            ),
            current_source_tag_revision_id=getattr(
                actual, "current_source_tag_revision_id", ""
            ),
            current_target_tag_revision_id=getattr(
                actual, "current_target_tag_revision_id", ""
            ),
            title=getattr(actual, "title", None),
            description=getattr(actual, "description", None),
            created_by_id=actual.created_by_id,
            created=actual.created,
        )
        object.__setattr__(cr, "_mgr", mgr)
        object.__setattr__(cr, "_system_id", system_id)
        return cr

    @property
    def id(self) -> str:
        """Convenience alias for change_request_id (the CR's UUID string)."""
        return self.change_request_id

    def close(self) -> "ChangeRequest":
        """Close this change request (status → "CLOSED") and return the refreshed object.

        Mutates: true

        The returned ChangeRequest reflects the new status; ``self`` is left as-is
        (its ``status`` still reads the pre-close value). A closed change request can
        be reopened with reopen().
        """
        self._mgr.update_status(self._system_id, self.change_request_id, "CLOSED")
        return self._mgr.get(self._system_id, self.change_request_id)

    def reopen(self) -> "ChangeRequest":
        """Reopen a closed change request (status → "OPEN") and return the refreshed object.

        Mutates: true

        The returned ChangeRequest reflects the new status; ``self`` is left as-is.
        """
        self._mgr.update_status(self._system_id, self.change_request_id, "OPEN")
        return self._mgr.get(self._system_id, self.change_request_id)

    def merge(
        self,
        *,
        comment: str | None = None,
        check_only: bool = False,
        head_pair_token: str | None = None,
    ) -> "ChangeRequest":
        """Merge this change request, applying source branch changes to the target.

        Mutates: true

        ``comment`` is an optional merge comment. If ``check_only`` is True, the
        staleness check is performed but the merge is not executed — use this to
        verify the merge will succeed before committing. ``head_pair_token`` is
        an optional optimistic concurrency token.

        Returns the updated ChangeRequest. After a successful merge, the status
        will be "MERGED" and the target branch's snapshot will include the
        source branch's changes.

        Raises ConflictError if the change request is stale (source or target
        has been modified since the CR was created) and cannot be merged.
        """
        return self._mgr.merge(
            self._system_id,
            self.change_request_id,
            comment=comment,
            check_only=check_only,
            head_pair_token=head_pair_token,
        )


__all__ = ["Branch", "ChangeRequest", "System"]
