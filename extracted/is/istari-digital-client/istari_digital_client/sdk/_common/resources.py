"""Resources tree manager (Istari common-user surface).

Resources is the single source of truth for the resources tree: create / get /
list / archive / restore, returning rich Resource objects, plus the revisions /
comments / relationships child-collection sub-managers.
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Any, List

from istari_digital_client.sdk._base import Page, coerce_enum
from istari_digital_client.sdk._generated.v3.models.archive_status import ArchiveStatus
from istari_digital_client.sdk._generated.v3.models.resource_create_dto import ResourceCreateDto
from istari_digital_client.sdk._generated.v3.models.resource_type_dto import ResourceTypeDto
from istari_digital_client.sdk._generated.v3.models.token_create_dto import TokenCreateDto
from istari_digital_client.sdk._common._capabilities import (
    _SupportsAccess,
    _SupportsControlTags,
    _SupportsInfosec,
    _SupportsRead,
)
from istari_digital_client.sdk._common.comments import Comments
from istari_digital_client.sdk._common.relationships import Relationships
from istari_digital_client.sdk._common.resource_types import Resource
from istari_digital_client.sdk._common.revisions import Revisions


class Resources(_SupportsRead, _SupportsAccess, _SupportsControlTags, _SupportsInfosec):
    """Manage resources: create, get, list, archive, and restore registry resources.

    Reached via ``istari.resources``. No parent id is required — resources are
    top-level objects.

    Sub-managers:
    - ``revisions``: list revision history and create new revisions of a resource.
    - ``comments``: create, read, update, and archive comments on a resource.
    - ``relationships``: create typed relationships between resource revisions and
      list the available relationship types.

    Usage::

        # 1. Upload a file and register it as a new resource
        resource = istari.resources.create(
            "/path/to/model.onnx",
            "model",
            description="Baseline model v1",
            version_name="v1.0",
        )
        print(resource.resource_id)

        # 2. Read the resource content back immediately
        data = resource.read_bytes()

        # 3. Fetch the resource by id
        r = istari.resources.get(resource.resource_id)

        # 4. List only active FILE resources whose name contains "report"
        for r in istari.resources.list(name=["report"], type_name=["file"]):
            print(r.name, r.size)

        # 5. List archived resources
        for r in istari.resources.list(archive_status="archived"):
            print(r.resource_id)

        # 6. Archive and restore
        istari.resources.archive(resource.resource_id)
        restored = istari.resources.restore(resource.resource_id)

        # 7. List revision history
        for rev in istari.resources.revisions.list(resource.resource_id):
            print(rev.file_revision_id, rev.size)
    """

    def _acl_ref(self, obj: Any) -> tuple[str, str]:
        """Return the v2 ACL identity for a resource: its resource_type kind and resource_id."""
        rt = obj.resource_type
        kind = rt.value if hasattr(rt, "value") else str(rt)
        return kind, obj.resource_id

    @cached_property
    def revisions(self) -> Revisions:
        """Sub-manager for resource revisions.

        Use this to create new revisions of an existing resource or list its full
        revision history. Each revision is a ResourceRevision with fields:
        file_revision_id (also .id), name (str | None), extension (str | None),
        size (int | None, bytes), mime (str | None), description (str | None),
        version_name (str | None), display_name (str | None),
        external_identifier (str | None), content_token,
        archived (bool | None), created (datetime | None), created_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        on any revision to fetch its content.

        Example::

            for rev in istari.resources.revisions.list(resource_id):
                print(rev.file_revision_id, rev.version_name)
        """
        return Revisions(self._engine)

    @cached_property
    def comments(self) -> Comments:
        """Sub-manager for resource comments.

        Use this to create, read, update, and archive comments attached to a resource.
        Comments store their body as a content blob (Readable) and can be archived or
        restored (Archivable).

        Example::

            comment = istari.resources.comments.create(resource_id, "/path/to/note.txt")
            text = comment.read_text()
            istari.resources.comments.archive(comment.id)
        """
        return Comments(self._engine)

    @cached_property
    def relationships(self) -> Relationships:
        """Sub-manager for typed relationships between resource revisions.

        Use this to create a relationship between two resource revisions, list
        existing relationships for a revision, delete a relationship, or enumerate
        the available RelationshipType objects (each with an id, name, and optional
        description).

        Example::

            types = list(istari.resources.relationships.list_types())
            rel = istari.resources.relationships.create(
                left_revision_id=rev_a.id,
                right_revision_id=rev_b.id,
                relationship_type_id=types[0].id,
            )
            print(rel.id, rel.relationship_type_id)
        """
        return Relationships(self._engine)

    def create(
        self,
        path: str | Path,
        resource_type: ResourceTypeDto | str,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> Resource:
        """Upload a file and register it as a new resource in the registry.

        Mutates: true

        Aliases: upload register import add ingest

        ``path`` is the local filesystem path to the file to upload.
        ``resource_type`` accepts "model" | "artifact" | "file" (case-insensitive,
        or the equivalent ResourceTypeDto enum value). All other parameters are
        optional metadata.

        Returns a Resource with fields: resource_id, file_revision_id,
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), resource_type (str: "model" | "artifact" | "file"),
        description (str | None), version_name (str | None), display_name (str | None),
        external_identifier (str | None), content_token,
        archived (bool), created (datetime), created_by_id (str),
        updated (datetime), updated_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        to fetch content from storage. Archivable: call archive() or restore().
        """
        if isinstance(resource_type, str):
            try:
                rt = ResourceTypeDto(resource_type.lower())
            except ValueError:
                valid = ", ".join(m.value for m in ResourceTypeDto)
                raise ValueError(
                    f"resource_type must be one of {valid} (case-insensitive); "
                    f"got {resource_type!r}"
                ) from None
        else:
            rt = resource_type
        rev = self._engine.storage.upload(
            path,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )
        dto = self._call(
            self._engine.v3_api.create_resource,
            resource_create_dto=ResourceCreateDto(
                name=rev.name,
                extension=rev.extension,
                size=rev.size,
                mime=rev.mime,
                description=rev.description,
                version_name=rev.version_name,
                external_identifier=rev.external_identifier,
                display_name=rev.display_name,
                content_token=TokenCreateDto(
                    sha=rev.content_token.sha, salt=rev.content_token.salt
                ),
                properties_token=TokenCreateDto(
                    sha=rev.properties_token.sha, salt=rev.properties_token.salt
                ),
                resource_type=rt,
            ),
        )
        return Resource._bind(dto, mgr=self)

    def get(self, resource_id: str) -> Resource:
        """Fetch a single resource by its UUID.

        Aliases: open view load

        Returns a Resource with fields: resource_id, file_revision_id,
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), resource_type (str: "model" | "artifact" | "file"),
        description (str | None), version_name (str | None), display_name (str | None),
        external_identifier (str | None), content_token,
        archived (bool), created (datetime), created_by_id (str),
        updated (datetime), updated_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        to fetch content from storage. Archivable: call archive() or restore().

        If ``resource_id`` turns out to be a *file* id (a common mix-up — the v3
        resource route rejects a file id with a misleading 403, not a 404; see
        ``ai-chat-file-id-misroute-plan.md``), this transparently resolves the file
        to its resource and retries once, so callers holding a file id still get
        the right resource instead of a confusing permission error.

        Raises NotFoundError if no resource with that id exists (and the id is not
        a file id that resolves to one).
        """
        dto = self._call_healing_id(self._engine.v3_api.get_resource, resource_id)
        return Resource._bind(dto, mgr=self)

    def list(
        self,
        *,
        name: list[str] | None = None,
        type_name: list[str] | None = None,
        version_name: list[str] | None = None,
        description: list[str] | None = None,
        external_identifier: list[str] | None = None,
        display_name: list[str] | None = None,
        mime_type: list[str] | None = None,
        created_by_id: list[str] | None = None,
        resource_id: list[str] | None = None,
        has_parents: bool | None = None,
        has_children: bool | None = None,
        archive_status: str | None = None,
        size: int | None = None,
    ) -> Page[Resource]:
        """List resources with optional filters, returning an auto-paging sequence.

        Aliases: find browse search

        All filter parameters are optional. List parameters (name, type_name,
        version_name, description, external_identifier, display_name, mime_type,
        created_by_id, resource_id) accept multiple values treated as OR filters.
        ``has_parents`` and ``has_children`` are booleans that filter by relationship
        presence. ``archive_status`` filters by archive state: "active" (default) |
        "archived" | "all" (accepted case-insensitively). ``size`` sets the page size.

        Returns an auto-paging sequence of Resource objects with fields: resource_id,
        file_revision_id, name (str | None), extension (str | None),
        size (int | None, bytes), mime (str | None),
        resource_type (str: "model" | "artifact" | "file"),
        description (str | None), version_name (str | None), display_name (str | None),
        external_identifier (str | None), content_token,
        archived (bool), created (datetime), created_by_id (str),
        updated (datetime), updated_by_id (str).
        Iterate directly — subsequent pages are fetched automatically.
        Readable: call read_bytes(), read_text(), or read_json()
        on any item. Archivable: call archive() or restore().
        """

        archive_status_enum = coerce_enum(
            ArchiveStatus, archive_status, param="archive_status"
        )
        # The registry type filter is an exact, lowercase enum (model|artifact|file,
        # `!` negation allowed); accept any case from callers so a stray "MODEL"
        # doesn't silently return [] — same forgiveness create() already applies.
        if type_name is not None:
            type_name = [t.lower() for t in type_name]

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_resources,
                cursor=cursor,
                size=size,
                name=name,
                type_name=type_name,
                version_name=version_name,
                description=description,
                external_identifier=external_identifier,
                display_name=display_name,
                mime_type=mime_type,
                created_by_id=created_by_id,
                resource_id=resource_id,
                has_parents=has_parents,
                has_children=has_children,
                archive_status=archive_status_enum,
            )

        return self._paginate(fetch, lambda d: Resource._bind(d, mgr=self))

    def archive(self, resource_id: str) -> None:
        """Archive a resource by its UUID.

        Mutates: true

        Archived resources are excluded from default list() results but remain
        accessible by passing archive_status="archived". To archive via the rich
        object, call archive() on the Resource instance instead.

        If ``resource_id`` is actually a *file* id (a common mix-up that the
        registry answers with a misleading 403), it is transparently resolved to
        its resource and retried once.

        Raises NotFoundError if no resource with that id exists.
        """
        self._call_healing_id(self._engine.v3_api.archive_resource, resource_id)

    def restore(self, resource_id: str) -> Resource:
        """Restore a previously archived resource.

        Mutates: true

        Returns the updated Resource with fields: resource_id,
        file_revision_id, name (str | None), extension (str | None),
        size (int | None, bytes), mime (str | None),
        resource_type (str: "model" | "artifact" | "file"),
        description (str | None), version_name (str | None), display_name (str | None),
        external_identifier (str | None), content_token,
        archived (bool), created (datetime), created_by_id (str),
        updated (datetime), updated_by_id (str).

        If ``resource_id`` is actually a *file* id (a common mix-up that the
        registry answers with a misleading 403), it is transparently resolved to
        its resource and retried once.

        Raises NotFoundError if no resource with that id exists.
        Raises ConflictError if the resource is already active.
        """
        dto = self._call_healing_id(self._engine.v3_api.restore_resource, resource_id)
        return Resource._bind(dto, mgr=self)

    def get_related_resources(
        self,
        resource_id: str,
        *,
        relationship: str | None = None,
        direction: str = "outgoing",
    ) -> List[Resource]:
        """One-call lineage drill-down: the resources RELATED to this one, resolved.

        ``relationships.list`` returns *revision* edges you must resolve back to
        resources by hand; this does that bridge for you and returns the related
        :class:`Resource` objects directly. Use it to answer "what did this model
        produce", "what artifacts were extracted from this connected file", or
        "what is this derived from".

        ``direction``:
          - "outgoing" (default): edges where this resource is the SOURCE; returns
            the derived/produced resources (a model's produced artifacts, a connected
            pointer's extracted records).
          - "incoming": edges where this resource is the derived side; returns its
            sources/parents.
          - "both": related resources in either direction.
        ``relationship`` filters by relationship type name (e.g. "produces");
        ``None`` returns every relationship type.

        Returns a de-duplicated list of active Resource objects. Edges whose other
        end is not an owned resource (a job, secret, or unowned revision) are
        skipped. Accepts a *file* id for ``resource_id`` (self-healed to its
        resource).
        """
        return self._related_resources(
            self.get(resource_id), relationship=relationship, direction=direction
        )

    def _related_resources(
        self,
        obj: Any,
        *,
        relationship: str | None = None,
        direction: str = "outgoing",
    ) -> List[Resource]:
        """Core lineage resolution shared by get_related_resources() and Resource.related().

        Lists the relationships on ``obj``'s current revision, keeps the edges that
        match ``direction``/``relationship``, resolves each edge's *other* revision to
        its owning resource id (via the file-id healing path), and fetches those
        resources in a single ``list()`` call.
        """
        if direction not in ("outgoing", "incoming", "both"):
            raise ValueError(
                f"direction must be 'outgoing', 'incoming', or 'both'; got {direction!r}"
            )
        want_out = direction in ("outgoing", "both")
        want_in = direction in ("incoming", "both")
        rev_id = obj.file_revision_id

        related_file_ids: list[str] = []
        for edge in self.relationships.list(rev_id):
            left_id = edge.left_revision.file_revision_id
            right_id = edge.right_revision.file_revision_id
            if rev_id == left_id and want_out:
                other = edge.right_revision
            elif rev_id == right_id and want_in:
                other = edge.left_revision
            else:
                continue
            if relationship and edge.relationship_type_name != relationship:
                continue
            related_file_ids.append(other.file_id)

        # Resolve each related revision's file to its owning resource id (one lookup
        # each), de-dup, then fetch them all in a single list() call. Edges whose
        # other end has no owning resource (jobs, secrets, unowned revisions) resolve
        # to None and are dropped.
        # ponytail: one get_file per edge; batch the file lookups if edge counts grow.
        resource_ids: list[str] = []
        seen: set[str] = set()
        for fid in related_file_ids:
            rid = self._resource_id_from_file_id(fid)
            if rid and rid not in seen:
                seen.add(rid)
                resource_ids.append(rid)
        if not resource_ids:
            return []
        return list(self.list(resource_id=resource_ids))

    # --- Archivable hook. Archivable is a shared capability (the object mixin lives
    #     in _base), but its endpoint differs per object type — archive_resource here,
    #     archive_comment for comments, archive_system/_job for those — and the ids
    #     differ, so there's no single body to share: each manager wires its own,
    #     the same way it supplies _acl_ref. ---

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.archive_resource, obj.resource_id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.restore_resource, obj.resource_id)
