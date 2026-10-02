"""Branches sub-manager (reached via ``istari.systems.branches``).

List, get, create, and advance branches (snapshot tags) for a system. All
methods take ``system_id`` as the first positional argument.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.resource_types import Resource, TrackedResource
from istari_digital_client.sdk._common.system_types import Branch, Subsystem

if TYPE_CHECKING:
    from istari_digital_client.sdk._engine import _Engine
    from istari_digital_client.sdk._common.systems import Systems
from istari_digital_client.sdk._generated.v2.models.new_snapshot_tag import NewSnapshotTag
from istari_digital_client.sdk._generated.v2.models.new_system_configuration import NewSystemConfiguration
from istari_digital_client.sdk._generated.v2.models.new_tracked_file import NewTrackedFile
from istari_digital_client.sdk._generated.v2.models.tracked_file_specifier_type import (
    TrackedFileSpecifierType,
)
from istari_digital_client.sdk._generated.v2.models.update_tag import UpdateTag
from istari_digital_client.sdk._exceptions import IstariError, NotFoundError

_log = logging.getLogger(__name__)

# MIME types whose content is text we can decode and inline in ``contents()``.
# Anything else (binary: CAD, mesh, image, archives) is left with ``content=None``.
_TEXT_MIME_EXACT = frozenset(
    {
        "application/json",
        "application/xml",
        "application/yaml",
        "application/x-yaml",
        "application/csv",
        "application/x-ndjson",
        "application/toml",
        "application/x-sh",
        "application/javascript",
    }
)


def _is_text_mime(mime: str | None) -> bool:
    """True if a resource's content is text worth inlining for a summary."""
    if not mime:
        return False
    m = mime.lower().split(";", 1)[0].strip()
    return (
        m.startswith("text/")
        or m in _TEXT_MIME_EXACT
        or m.endswith("+json")
        or m.endswith("+xml")
    )


def _chain_cached_pages(
    pages: List[List[Any]], total: int | None
) -> Page[TrackedResource]:
    """Rebuild the chained :class:`Page` sequence from cached per-page item lists.

    Reproduces the uncached ``_paginate`` shape exactly — same ``has_next()``,
    per-page ``.items``, and ``.total`` — but the ``fetch_next`` closures walk the
    cached pages instead of the transport. Each page's list is copied so a caller
    mutating ``.items`` cannot corrupt the cache.
    """

    def make(i: int) -> Page[TrackedResource]:
        nxt = (lambda: make(i + 1)) if i + 1 < len(pages) else None
        return Page(list(pages[i]), fetch_next=nxt, total=total)

    return make(0) if pages else Page([], fetch_next=None, total=total)


def _content_row(r: Resource, max_chars_per_file: int | None) -> dict:
    """One survey row for a resource: metadata + (bounded) inline text content.

    Text/JSON resources get their decoded content inline; binary resources get
    ``content=None``. When ``max_chars_per_file`` is set, oversized content is
    truncated to a preview with a marker naming the resource id to read in full.
    """
    content: str | None = None
    if _is_text_mime(r.mime):
        try:
            content = r.read_text()
        except Exception:
            content = None
        if (
            content is not None
            and max_chars_per_file is not None
            and len(content) > max_chars_per_file
        ):
            content = (
                content[:max_chars_per_file]
                + f"\n… [preview: showing {max_chars_per_file} of "
                f"{len(content)} chars. If the answer isn't in this preview, "
                f"read the whole file: "
                f"resources.get('{r.resource_id}').read_text()]"
            )
    rt = r.resource_type
    return {
        "resource_id": r.resource_id,
        "name": r.name,
        "resource_type": rt.value if hasattr(rt, "value") else str(rt),
        "description": r.description,
        "path": getattr(r, "path", None),
        "mime": r.mime,
        "size": r.size,
        "content": content,
    }


class Branches(_Manager):
    """Manage branches (snapshot tags) for a system: list, get, create, commit, archive, restore.

    Reached via ``istari.systems.branches``. All methods take ``system_id`` as
    the first positional argument.

    Sub-managers: none (branches are a leaf collection).

    Usage::

        # 1. List all active branches on a system
        for branch in istari.systems.branches.list(system_id):
            print(branch.tag, branch.id)

        # 2. Get a specific branch by name
        main = istari.systems.branches.get(system_id, "main")

        # 3. Create a new branch forked from an existing one
        feature = istari.systems.branches.create(
            system_id, "feature/my-change", from_branch=main
        )

        # 4. Commit file revisions onto the branch
        updated = istari.systems.branches.commit(
            feature,
            add=[rev_a, rev_b],    # revision objects (from resources.revisions / branch.resources())
            remove=[old_rev],      # objects with .id matching a tracked revision
        )

        # 5. List the subsystems (child systems) a branch tracks
        for sub in istari.systems.branches.subsystems(main):
            print(sub.system_name, sub.system_id)
    """

    def __init__(self, engine: "_Engine", systems_mgr: "Systems") -> None:
        super().__init__(engine)
        self._systems_mgr = systems_mgr

    def list(
        self, system_id: str, *, archive_status: str | None = None
    ) -> Page[Branch]:
        """List all branches of a system.

        ``archive_status`` filters which branches are returned: "ACTIVE" (default,
        live branches only) | "ARCHIVED" (archived only). Pass None to use the
        server default.

        Returns an auto-paging sequence of Branch objects. Iterate directly —
        subsequent pages are fetched automatically. Each Branch has fields:
        id (str), tag (str — the branch name), snapshot_id (str),
        is_baseline (bool), archive_status (str: "ACTIVE" | "ARCHIVED"),
        created (datetime). Object methods: archive(), restore(), resources(),
        commit(), create_change_request().
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_tags,
                system_id=system_id,
                page=page_num,
                size=100,
                archive_status=archive_status,
            )

        return self._paginate_offset(
            fetch,
            lambda d: Branch._bind_with_system(
                d, mgr=self, system_id=system_id, systems_mgr=self._systems_mgr
            ),
        )

    def get(self, system_id: str, name: str) -> Branch:
        """Fetch a branch by its tag name, scanning all pages until found.

        Does an exact string match on the branch's tag field. Returns a Branch
        with fields: id (str), tag (str — the branch name), snapshot_id (str),
        is_baseline (bool), archive_status (str: "ACTIVE" | "ARCHIVED"),
        created (datetime). Object methods: archive(), restore(), resources(),
        commit(), create_change_request().

        Raises NotFoundError if no branch with that name exists on the given system.
        """
        page_num = 1
        while True:
            raw = self._call(
                self._engine.v2_api.list_tags,
                system_id=system_id,
                page=page_num,
                size=100,
            )
            for tag in raw.items or []:
                if tag.tag == name:
                    return Branch._bind_with_system(
                        tag,
                        mgr=self,
                        system_id=system_id,
                        systems_mgr=self._systems_mgr,
                    )
            if page_num >= raw.pages:
                break
            page_num += 1
        raise NotFoundError(f"Branch {name!r} not found on system {system_id!r}")

    def create(
        self,
        system_id: str,
        name: str,
        *,
        from_branch: Branch | None = None,
    ) -> Branch:
        """Create a new branch on a system.

        Mutates: true

        ``name`` becomes the branch's human-readable tag string and must be unique
        within the system. If ``from_branch`` is provided the new branch is seeded
        from that branch's current snapshot; if omitted it is seeded from the
        system's baseline snapshot.

        Returns a Branch with fields: id (str), tag (str — the branch name),
        snapshot_id (str), is_baseline (bool),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime).
        Object methods: archive(), restore(), resources(), commit(),
        create_change_request().
        """
        if from_branch is None:
            baseline = self._call(self._engine.v2_api.get_system_baseline, system_id)
            snapshot_id = baseline.snapshot_id
        else:
            snapshot_id = from_branch.snapshot_id
        dto = self._call(
            self._engine.v2_api.create_tag,
            snapshot_id,
            NewSnapshotTag(tag=name),
        )
        return Branch._bind_with_system(
            dto, mgr=self, system_id=system_id, systems_mgr=self._systems_mgr
        )

    def commit(
        self,
        branch: Branch,
        *,
        add: List[Any] | None = None,
        remove: List[Any] | None = None,
    ) -> Branch:
        """Advance a branch by committing a new set of file revisions onto it.

        Mutates: true

        This is the primary mutation operation for a branch. The current tracked-file
        list is read, ``add`` and ``remove`` are applied, and a new configuration
        snapshot is created. The branch pointer is then updated to that snapshot.

        ``add``: a list of revision objects identified by ``.id`` (str, the
        revision id) — e.g. objects returned by ``istari.resources.revisions`` or
        ``branch.resources()``. Each object is added to the branch as a LOCKED tracked
        file, meaning the branch is pinned to that exact revision rather than
        floating to the latest.

        ``remove``: a list of objects that expose ``.id`` (str). Any currently
        tracked file whose ``current_file_revision_id`` matches an object's ``.id``
        is dropped from the new configuration. Pass a revision object obtained from
        ``resources()`` or a resource revision.

        Both lists are optional and can be combined in a single call.

        Returns the updated Branch with the new snapshot pointer. Fields: id (str),
        tag (str — the branch name), snapshot_id (str), is_baseline (bool),
        archive_status (str: "ACTIVE" | "ARCHIVED"), created (datetime).
        """
        if getattr(branch, "_pinned", False):
            raise IstariError(
                "This Branch is a pinned read view from Subsystem.branch(); committing through it "
                "would rebuild the child from the pinned snapshot and drop later changes. "
                "Commit via system().get_branch(name) instead."
            )
        system_id = branch._system_id
        snapshot = self._call(self._engine.v2_api.get_snapshot, branch.snapshot_id)
        current_files = self._all_tracked_resources(snapshot.configuration_id)
        remove_ids = {r.id for r in (remove or [])}
        new_tracked: list[NewTrackedFile] = [
            NewTrackedFile(
                specifier_type=tf.specifier_type,
                file_id=tf.file_id,
                pinned_file_revision_id=tf.pinned_file_revision_id,
            )
            for tf in current_files
            if tf.current_file_revision_id not in remove_ids
        ]
        for rev in add or []:
            new_tracked.append(
                NewTrackedFile(
                    specifier_type=TrackedFileSpecifierType.LOCKED,
                    file_id=self._owning_file_id(rev),
                    pinned_file_revision_id=rev.id,
                )
            )
        cfg = self._call(
            self._engine.v2_api.create_configuration,
            system_id,
            NewSystemConfiguration(
                name=f"{branch.tag}-commit",
                tracked_files=new_tracked,
            ),
        )
        try:
            snap_page = self._call(
                self._engine.v2_api.list_snapshots,
                configuration_id=cfg.id,
                size=1,
                sort="-created",
            )
            if not snap_page.items:
                raise RuntimeError(f"No snapshot created for configuration {cfg.id!r}")
            updated = self._call(
                self._engine.v2_api.update_tag,
                branch.id,
                UpdateTag(snapshot_id=snap_page.items[0].id),
            )
        except Exception:
            # If post-creation steps fail, archive the orphaned configuration and re-raise
            try:
                self._call(self._engine.v2_api.archive_configuration, cfg.id)
            except Exception:
                pass  # Best-effort cleanup; original exception is more important
            raise
        return Branch._bind_with_system(
            updated, mgr=self, system_id=system_id, systems_mgr=self._systems_mgr
        )

    @staticmethod
    def _owning_file_id(rev: Any) -> str:
        """Internal plumbing: the storage File id the v2 tracked-file API keys on.

        Callers pass rich revision/resource objects identified by ``.id`` (the
        revision id) and never deal with file ids. The v2 configuration API still
        needs the owning File id, which every rich resource/revision object carries,
        so we read it here rather than exposing it in ``commit``'s public contract.
        """
        file_id = getattr(rev, "file_id", None)
        if not file_id:
            raise ValueError(
                "commit(add=...) expects revision or resource objects "
                "(e.g. from istari.resources.revisions or branch.resources()); "
                f"got {rev!r}"
            )
        return file_id

    def resources(
        self,
        branch: Branch,
        *,
        name: str | None = None,
    ) -> Page[TrackedResource]:
        """List a branch's tracked resources — models, artifacts, files (METADATA only).

        Answers "list the resources / models / artifacts / files in this branch". Pass
        ``name`` to filter by a case-insensitive substring match on the resource name.

        Returns an auto-paging sequence of :class:`TrackedResource` objects — each
        one is a full :class:`Resource` (``resource_id``, ``name``, ``size``,
        ``description``, ``mime``, ``resource_type``, ``path``, ...) plus the read
        verbs (``read_bytes()`` / ``read_text()`` / ``read_json()``). This is the
        listing; it does NOT read content — use :meth:`contents` to get the content
        of every tracked resource in one call.

        This resolves each tracked file to its resource, so callers never juggle
        file ids vs resource ids. Any tracked file with no ``resource_id`` (a known
        data gap) is logged and omitted rather than silently misrouted.

        Aliases: files file model artifact
        """
        return self._tracked_resources(branch, name=[name] if name else None)

    def subsystems(self, branch: Branch) -> Page[Subsystem]:
        """List the subsystems (child systems) a branch tracks.

        Answers "list the subsystems of this branch / system" and "does this system
        have child systems". Systems nest: alongside its files a branch tracks other
        systems, each pinned to a specific branch of the child. Returns an auto-paging
        sequence of :class:`Subsystem` — the child's ``system_id`` / ``system_name`` /
        ``system_description`` plus the pinned ``tag_id`` / ``tagged_snapshot_id``;
        ``.system()`` resolves the full child System and ``.branch()`` the pinned child
        Branch. Empty when the branch tracks no subsystems.

        Aliases: subsystem sub-system child-system nested component
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_snapshot_subsystems,
                branch.snapshot_id,
                page=page_num,
                size=100,
            )

        return self._paginate_offset(fetch, lambda d: Subsystem._bind(d, mgr=self))

    def contents(
        self,
        branch: Branch,
        *,
        name: str | None = None,
        max_chars_per_file: int | None = None,
        include_extracted: bool = False,
    ) -> List[dict]:
        """Read a branch's tracked resources AND their content in one call.

        Answers "summarize this branch" / "what is in this branch". For every
        tracked resource it returns the metadata plus, for text/JSON/data
        resources, the decoded ``content`` inline — so you never make a second
        per-file read. Binary resources (CAD, mesh, image) return their metadata
        with ``content=None`` (their bytes are not summarizable; fetch them with
        ``read_bytes()`` only if actually needed).

        By default (``max_chars_per_file=None``) each file's ``content`` is the FULL
        text — nothing is dropped, this is a data API. Pass a non-negative int to get
        a bounded SURVEY instead: each file's content is capped to that many
        characters of preview, then a short marker naming the resource id to read in
        full is appended (the marker is metadata beyond the cap, so a row's field is
        ``max_chars_per_file`` chars of content plus the marker; ``0`` yields marker
        only, a negative value raises ``ValueError``). Use the bound when handing the
        result to an LLM or when files may be large, so the combined result fits one
        context window regardless of file size; to then answer a detailed question
        about ONE file, read it directly and compute over it
        (``resources.get(id).read_text()`` returns the entire file uncapped).

        Set ``include_extracted=True`` to make the survey COMPLETE for content
        search: any tracked resource that is a connected-file pointer (DOORS,
        Confluence, SharePoint, Teamwork Cloud, Jira — see
        :attr:`Resource.is_connected_pointer`) holds only a stub, while its real
        content lives in the resources Istari extracted from it. With this flag
        those extracted children are read and appended as their own rows, each
        carrying ``extracted_from`` = the pointer's ``resource_id``. This is the
        one call to make BEFORE concluding a fact is absent: a branch listing shows
        only tracked resources, so the answer is often invisible without it. Bound
        it with ``max_chars_per_file`` and let the reader judge every row
        semantically — do NOT keyword-filter the survey yourself; a substring grep
        misses a requirement phrased differently than the query.

        Each row: ``{resource_id, name, resource_type, description, path, mime,
        size, content}`` (extracted rows add ``extracted_from``). Use
        :meth:`resources` instead when you only need the listing.

        Aliases: summarize summary overview describe tell-me-about whats-in read-all
        search find grep scan where-is locate full-text sweep across everything
        """
        if max_chars_per_file is not None and max_chars_per_file < 0:
            raise ValueError("max_chars_per_file must be None or a non-negative int")
        rows: List[dict] = []
        for r in self.resources(branch, name=name):
            rows.append(_content_row(r, max_chars_per_file))
            if include_extracted and r.is_connected_pointer:
                for child in r.extracted():
                    child_row = _content_row(child, max_chars_per_file)
                    child_row["extracted_from"] = r.resource_id
                    rows.append(child_row)
        return rows

    def search(
        self,
        branch: Branch,
        *,
        name: List[str] | None = None,
        type_name: List[str] | None = None,
        version_name: List[str] | None = None,
        description: List[str] | None = None,
        external_identifier: List[str] | None = None,
        display_name: List[str] | None = None,
        mime_type: List[str] | None = None,
    ) -> Page[TrackedResource]:
        """Search the resources tracked on a branch.

        Like :meth:`files`, but with the resource filters of
        ``Resources.list`` scoped to just this branch's tracked files. Every list
        parameter (``name``, ``type_name``, ``version_name``, ``description``,
        ``external_identifier``, ``display_name``, ``mime_type``) accepts multiple
        values treated as OR filters and matches as a case-insensitive substring.

        Returns an auto-paging sequence of :class:`TrackedResource` objects (see
        :meth:`files`). Tracked files with no ``resource_id`` are logged and
        omitted.

        Example::

            for f in system.get_branch("main").search(name=["report"], type_name=["model"]):
                print(f.path, f.name)
        """
        # Registry type filter is exact + lowercase (model|artifact|file); accept any
        # case so a stray "MODEL" doesn't silently return [] (mirrors Resources.list).
        if type_name is not None:
            type_name = [t.lower() for t in type_name]
        return self._tracked_resources(
            branch,
            name=name,
            type_name=type_name,
            version_name=version_name,
            description=description,
            external_identifier=external_identifier,
            display_name=display_name,
            mime_type=mime_type,
        )

    def _tracked_resources(
        self, branch: Branch, **resource_filters: Any
    ) -> Page[TrackedResource]:
        """Resolve a branch's tracked files to TrackedResource, applying resource filters.

        Batches the resolution: collects the tracked files' resource ids and issues
        a single ``list_resources`` query per page (no per-file N+1). Tracked files
        with no ``resource_id`` are logged and omitted.

        When the client opted into the listing cache, the assembled result is cached
        per ``(branch_id, snapshot_id, filters)`` — the snapshot id is already on the
        branch object (no extra call), and it changes whenever the branch advances, so
        the cache self-invalidates without a TTL. Page boundaries are preserved, so the
        cached path returns the same chained :class:`Page` (same ``has_next()`` /
        ``.items`` / ``.total``) as the uncached path — only the transport is saved.
        """
        cache = self._engine.listing_cache
        cache_key = None
        if cache is not None:
            cache_key = (
                branch.id,
                branch.snapshot_id,
                tuple(sorted(
                    (k, tuple(v) if v is not None else None)
                    for k, v in resource_filters.items()
                )),
            )
            cached = cache.get(cache_key)
            if cached is not None:
                pages, total = cached
                return _chain_cached_pages(pages, total)

        # Imported lazily to avoid a manager import cycle (Resources pulls in the
        # comments/relationships/revisions sub-managers).
        from istari_digital_client.sdk._common.resources import Resources

        snapshot = self._call(self._engine.v2_api.get_snapshot, branch.snapshot_id)
        tracked_by_id: dict[str, Any] = {}
        unreadable: list[str] = []
        for tf in self._all_tracked_resources(snapshot.configuration_id):
            resource_id = getattr(tf, "resource_id", None)
            if resource_id:
                tracked_by_id[resource_id] = tf
            else:
                unreadable.append(tf.path)

        if unreadable:
            _log.warning(
                "Branch %s has %d tracked file(s) with no resource_id; they cannot "
                "be read as resources and are omitted: %s",
                branch.id,
                len(unreadable),
                ", ".join(sorted(unreadable)),
            )

        if not tracked_by_id:
            if cache is not None and cache_key is not None:
                cache.put(cache_key, ([], 0))
            return Page([], fetch_next=None, total=0)

        ids = list(tracked_by_id.keys())
        resources_mgr = Resources(self._engine)

        def bind(dto: Any) -> TrackedResource:
            resource = Resource._bind(dto, mgr=resources_mgr)
            tracked_file = tracked_by_id.get(dto.resource_id)
            if tracked_file is None:
                # Defensive: list_resources is filtered to `ids`, so every returned
                # resource has a tracked file. Fall back to the plain resource.
                return resource  # type: ignore[return-value]
            return TrackedResource._attach(resource, tracked_file)

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_resources,
                cursor=cursor,
                resource_id=ids,
                **resource_filters,
            )

        page = self._paginate(fetch, bind)
        if cache is None or cache_key is None:
            return page
        # Walk the chain once, keeping each page's items separate so the cached
        # replay reproduces the same paged Page (has_next/.items/.total), not a
        # single flattened page.
        page_lists: list[list[Any]] = []
        total = page.total
        p: Page[TrackedResource] | None = page
        while p is not None:
            page_lists.append(p.items)
            p = p.next_page()
        cache.put(cache_key, (page_lists, total))
        return _chain_cached_pages(page_lists, total)

    def archive(self, branch_id: str) -> None:
        """Archive a branch by its UUID.

        Mutates: true

        Archived branches are excluded from default list() results; pass
        archive_status="ARCHIVED" to retrieve them. The system's other branches
        and its revision history are unaffected. Returns None.
        """
        self._call(self._engine.v2_api.archive_tag, branch_id)

    def restore(self, branch_id: str) -> None:
        """Restore a previously archived branch by its UUID.

        Mutates: true

        Returns None. Call get() or list() to obtain the refreshed Branch object
        if needed.
        """
        self._call(self._engine.v2_api.restore_tag, branch_id)

    def _branch_by_id(
        self, system_id: str, branch_id: str, *, snapshot_id: str | None = None
    ) -> Branch:
        """Fetch a branch by tag id; ``snapshot_id`` pins the view to that snapshot instead of the tag's head."""
        raw = self._call(self._engine.v2_api.get_tag, branch_id)
        if snapshot_id is not None:
            raw.snapshot_id = snapshot_id
            object.__setattr__(raw, "_pinned", True)
        return Branch._bind_with_system(
            raw, mgr=self, system_id=system_id, systems_mgr=self._systems_mgr
        )

    def _all_tracked_resources(self, configuration_id: str) -> List[Any]:
        result: list[Any] = []
        page_num = 1
        while True:
            raw = self._call(
                self._engine.v2_api.list_tracked_files,
                configuration_id,
                page=page_num,
                size=100,
            )
            result.extend(raw.items or [])
            if page_num >= raw.pages:
                break
            page_num += 1
        return result

    # Archivable hook — branches only ever archive/restore tags
    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v2_api.archive_tag, obj.id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v2_api.restore_tag, obj.id)
