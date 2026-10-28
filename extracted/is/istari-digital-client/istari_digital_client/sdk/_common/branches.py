"""Branches sub-manager (reached via ``istari.systems.branches``).

List, get, create, and advance branches (snapshot tags) for a system. All
methods take ``system_id`` as the first positional argument.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.resource_types import Resource, TrackedResource
from istari_digital_client.sdk._common.dependency_types import (
    FolderUpdates,
    Preview,
    Publications,
    Requirements,
    dependency_update,
)
from istari_digital_client.sdk._common.system_types import Branch, Subsystem

if TYPE_CHECKING:
    from istari_digital_client.sdk._engine import _Engine
    from istari_digital_client.sdk._common.systems import Systems
from istari_digital_client.sdk._generated.v2.models.new_snapshot_tag import (
    NewSnapshotTag,
)
from istari_digital_client.sdk._generated.v2.models.branch_commit_dto import (
    BranchCommitDto,
)
from istari_digital_client.sdk._generated.v2.models.branch_file_change import (
    BranchFileChange,
)
from istari_digital_client.sdk._generated.v2.models.dependencies_manifest import (
    DependenciesManifest,
)
from istari_digital_client.sdk._generated.v2.models.dependency_resolve_request import (
    DependencyResolveRequest,
)
from istari_digital_client.sdk._generated.v2.models.manifest_input_dependencies_manifest import (
    ManifestInputDependenciesManifest,
)
from istari_digital_client.sdk._generated.v2.models.manifest_input_publications_manifest import (
    ManifestInputPublicationsManifest,
)
from istari_digital_client.sdk._generated.v2.models.publications_manifest import (
    PublicationsManifest,
)
from istari_digital_client.sdk._generated.v2.models.resolved_folder_dto import (
    ResolvedFolderDto,
)
from istari_digital_client.sdk._generated.v2.models.update_tag import UpdateTag
from istari_digital_client.sdk._exceptions import IstariError, NotFoundError

_log = logging.getLogger(__name__)

# Envoy in front of the registry caps request headers, URL included, at 60 KiB;
# each repeated ``resource_id`` costs 49 bytes, so one lookup carries this many.
_RESOURCE_ID_CHUNK = 400

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
    ``has_children`` says whether anything was extracted from (or produced by) the
    resource, so a binary row with no content is not mistaken for an empty one.
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
        "has_children": bool(getattr(r, "has_children", False)),
    }


class Branches(_Manager):
    """Manage branches (snapshot tags) for a system: list, get, create, commit, preview, archive, restore.

    Reached via ``istari.systems.branches``. All methods take ``system_id`` as
    the first positional argument.

    :meth:`commit` is the one write, and :meth:`preview` plans what it would install.

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
        folders: dict[str, str | None] | None = None,
        publications: str | PublicationsManifest | Publications | None = None,
        dependencies: str | DependenciesManifest | Requirements | None = None,
        resolve: bool = False,
        update: FolderUpdates | None = None,
        preview_id: str | None = None,
        message: str | None = None,
    ) -> Branch:
        """Commit to this branch's reviewed snapshot in one write.

        Mutates: true
        ``add`` takes revision objects and pins them; replacing a file preserves its
        folder. ``remove`` takes objects with a ``file_id``. ``folders`` maps added
        revision IDs to slash-separated relative folders (None moves a file to the root).
        ``publications`` and ``dependencies`` replace a manifest, as YAML text or a typed
        manifest. ``resolve`` installs the branch's requirements, leaving each ``1.x`` folder at
        the version it holds unless a requirement needs a newer one; ``update`` (which implies
        ``resolve``) also moves ``1.x`` folders to the newest release of their line: ``"all"``, or
        folder rows from :meth:`Dependencies.updates`. Pass the
        ``preview_id`` from :meth:`preview` to refuse a commit that would install other
        versions than the ones reviewed. Files tracking latest take their newest revision, as
        on every commit; pinned files and the existing lock stay put unless changed here.
        """
        if getattr(branch, "_pinned", False):
            raise IstariError(
                "This Branch is a pinned read view from Subsystem.branch(); committing through it "
                "would rebuild the child from the pinned snapshot and drop later changes. "
                "Commit via system().get_branch(name) instead."
            )
        if preview_id is not None and not resolve and update is None:
            raise ValueError("commit(preview_id=...) requires resolve=True or update=")
        placements = folders or {}
        changes = []
        for revision in add or []:
            revision_id = getattr(revision, "file_revision_id", None) or getattr(
                revision, "id", None
            )
            if revision_id is None:
                raise ValueError("commit(add=...) expects resource or revision objects")
            change = BranchFileChange(file_revision_id=revision_id)
            if revision_id in placements:
                change.folder_path = placements[revision_id]
            changes.append(change)
        result = self._call(
            self._engine.v2_api.commit_branch,
            branch._system_id,
            self._commit_body(
                branch,
                put=changes,
                remove=[self._owning_file_id(revision) for revision in remove or []],
                publications=publications,
                dependencies=dependencies,
                resolve=resolve,
                update=update,
                preview_id=preview_id,
                message=message,
            ),
        )
        return Branch._bind_with_system(
            branch.model_copy(update={"snapshot_id": result.new_snapshot_id}),
            mgr=self,
            system_id=branch._system_id,
            systems_mgr=self._systems_mgr,
        )

    def preview(
        self,
        branch: Branch,
        *,
        dependencies: str | DependenciesManifest | Requirements | None = None,
        update: FolderUpdates | None = None,
    ) -> Preview:
        """Plan what :meth:`commit` would install, without writing.

        The :class:`Preview` lists the package folders and placements that would change
        against the branch head, counts after the commit, warnings, and errors.
        ``update`` is as for :meth:`commit`. ``preview.commit()`` commits exactly that plan.
        """
        if update is not None and not isinstance(update, (str, ResolvedFolderDto)):
            # The preview sends it now and preview.commit() sends it again, so a one-shot
            # iterator must be read only once.
            update = list(update)
        dto = self._call(
            self._engine.v2_api.preview_branch_commit,
            branch._system_id,
            self._commit_body(
                branch, dependencies=dependencies, resolve=True, update=update
            ),
        )
        return Preview._bind_preview(
            dto, mgr=self, branch=branch, dependencies=dependencies, update=update
        )

    @staticmethod
    def _commit_body(
        branch: Branch,
        *,
        put: List[BranchFileChange] | None = None,
        remove: List[str] | None = None,
        publications: str | PublicationsManifest | Publications | None = None,
        dependencies: str | DependenciesManifest | Requirements | None = None,
        resolve: bool = False,
        update: FolderUpdates | None = None,
        preview_id: str | None = None,
        message: str | None = None,
    ) -> BranchCommitDto:
        if isinstance(publications, Publications):
            publications = publications.to_manifest()
        if isinstance(dependencies, Requirements):
            dependencies = dependencies.to_manifest()
        body = BranchCommitDto(
            branch_id=branch.id,
            expected_head_snapshot_id=branch.snapshot_id,
            put=put or [],
            remove=remove or [],
            commit_message=message,
        )
        if publications is not None:
            body.publications = (
                ManifestInputPublicationsManifest(raw_yaml=publications)
                if isinstance(publications, str)
                else ManifestInputPublicationsManifest(manifest=publications)
            )
        if dependencies is not None:
            body.dependencies = (
                ManifestInputDependenciesManifest(raw_yaml=dependencies)
                if isinstance(dependencies, str)
                else ManifestInputDependenciesManifest(manifest=dependencies)
            )
        if resolve or update is not None:
            body.resolve = DependencyResolveRequest(
                update=dependency_update(update) if update is not None else None,
                preview_id=preview_id,
            )
        return body

    @staticmethod
    def _owning_file_id(rev: Any) -> str:
        """Identify the tracked file to remove, independent of its pinned revision."""
        file_id = getattr(rev, "file_id", None)
        if not file_id:
            raise ValueError(
                "commit(remove=...) expects revision or resource objects "
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
        search. Two kinds of tracked resource hold their substance in children
        rather than in their own bytes: a connected-file pointer (DOORS,
        Confluence, SharePoint, Teamwork Cloud, Jira — see
        :attr:`Resource.is_connected_pointer`) is a stub whose real content is
        the records Istari extracted from it, and an uploaded model (a SysML
        ``.mdzip``, a CAD archive, a PDF) is a binary whose extraction job
        produced artifacts — requirements, element lists, diagrams, part trees.
        With this flag, every resource that has children (``has_children``) has
        them read and appended as their own rows, each carrying
        ``extracted_from`` = the parent's ``resource_id``. This is the one call to
        make BEFORE concluding a fact is absent or a binary is opaque: a branch
        listing shows only tracked resources, so the answer is often invisible
        without it. Bound it with ``max_chars_per_file`` and let the reader judge
        every row semantically — do NOT keyword-filter the survey yourself; a
        substring grep misses a requirement phrased differently than the query.

        Each row: ``{resource_id, name, resource_type, description, path, mime,
        size, content, has_children}`` (extracted rows add ``extracted_from``). A
        row with ``content=None`` and ``has_children=True`` is a binary whose
        extracted artifacts exist and were not read; never report it as having
        nothing inside or offer to extract it. Use :meth:`resources` instead when
        you only need the listing.

        Aliases: summarize summary overview describe tell-me-about whats-in read-all
        search find grep scan where-is locate full-text sweep across everything
        """
        if max_chars_per_file is not None and max_chars_per_file < 0:
            raise ValueError("max_chars_per_file must be None or a non-negative int")
        rows: List[dict] = []
        for r in self.resources(branch, name=name):
            rows.append(_content_row(r, max_chars_per_file))
            if include_extracted and (
                r.is_connected_pointer or getattr(r, "has_children", False)
            ):
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

        Batches the resolution: collects the tracked files' resource ids and queries
        ``list_resources`` for them in chunks of ``_RESOURCE_ID_CHUNK`` ids (no
        per-file N+1, no request URL that grows with the branch). Tracked files with
        no ``resource_id`` are logged and omitted.

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

        def fetch(chunk: list[str], cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_resources,
                cursor=cursor,
                resource_id=chunk,
                **resource_filters,
            )

        page = self._paginate_chunked(fetch, bind, ids, chunk_size=_RESOURCE_ID_CHUNK)
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
