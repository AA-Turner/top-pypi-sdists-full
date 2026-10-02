"""Rich domain objects for the resources tree.

Each rich type subclasses its generated v3 DTO and mixes in capabilities.
All DTO fields are inherited; the mixins add behavior (read content, archive,
share, tag, classify) bound to the manager that produced the object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field, StrictStr

from istari_digital_client.sdk._base import (
    Archivable,
    Classifiable,
    ClientHaving,
    Readable,
    Shareable,
    Taggable,
)
from istari_digital_client.sdk._generated.v3.models.comment_dto import CommentDto
from istari_digital_client.sdk._generated.v3.models.resource_dto import ResourceDto
from istari_digital_client.sdk._generated.v3.models.resource_revision_dto import ResourceRevisionDto
from istari_digital_client.sdk._generated.v3.models.revision_relationship_dto import (
    RevisionRelationshipDto,
)
from istari_digital_client.sdk._generated.v3.models.revision_relationship_type_dto import (
    RevisionRelationshipTypeDto,
)

if TYPE_CHECKING:
    from istari_digital_client.sdk._generated.v2.models.tracked_file import TrackedFile


class Resource(
    ResourceDto,
    ClientHaving,
    Readable,
    Shareable,
    Taggable,
    Classifiable,
    Archivable,
):
    """A registry resource (model, artifact, or file).

    Fields: resource_id, file_revision_id, name (str | None),
    extension (str | None), size (int | None, bytes), mime (str | None),
    resource_type (str: "model" | "artifact" | "file"),
    description (str | None), version_name (str | None),
    display_name (str | None), external_identifier (str | None),
    content_token, archived (bool),
    created (datetime), created_by_id (str),
    updated (datetime), updated_by_id (str).

    Readable: call read_bytes(), read_text(), or read_json()
    to fetch file content or metadata from storage.
    Archivable: call archive() to soft-delete or restore() to make active again.
    Shareable: manage who can access this resource.
    Taggable: add or remove control tags.
    Classifiable: set or read the infosec classification level.
    """

    #: ``file_id`` is a storage-layer implementation detail (the underlying
    #: ``File`` record). ``resource_id`` is the identifier callers use, so we keep
    #: ``file_id`` off the facade's data model: excluded from ``model_dump()`` /
    #: ``to_dict()`` / JSON and from ``repr()`` so it does not leak into how humans
    #: or agents understand a Resource. The value is still populated (the generated
    #: DTO carries it); this only controls what is *surfaced*. Remove once the API
    #: drops the field.
    file_id: StrictStr = Field(exclude=True, repr=False)

    def related(
        self, *, relationship: str | None = None, direction: str = "outgoing"
    ) -> list[Resource]:
        """The resources related to this one, resolved — the one-call lineage drill-down.

        Aliases: lineage provenance children produced derived downstream upstream trace

        ``resources.relationships.list`` hands back *revision* edges you must resolve
        to resources yourself; this returns the related :class:`Resource` objects
        directly. Answers "what did this model produce", "what was extracted from this
        connected file", "what is this derived from".

        ``direction``: "outgoing" (default) returns the derived/produced resources
        (a model's produced artifacts, a connected pointer's extracted records);
        "incoming" returns this resource's sources/parents; "both" returns either.
        ``relationship`` filters by relationship type name (e.g. "produces"); ``None``
        returns all. Edges whose other end is not an owned resource (a job, secret, or
        unowned revision) are skipped. Returns a de-duplicated list of active
        resources.
        """
        return self._mgr._related_resources(
            self, relationship=relationship, direction=direction
        )

    @property
    def is_connected_pointer(self) -> bool:
        """True if this resource is a connected-file POINTER, not real content.

        Files connected from an external system (DOORS, Jira, Confluence,
        SharePoint/Microsoft 365, Teamwork Cloud) are stored as a small metadata
        pointer with an ``istari_<tool>_metadata`` extension — a link/module path,
        NOT the external requirements/tickets/data. ``read_bytes()`` / ``read_text()``
        / ``read_json()`` on a pointer return that metadata, not the content the user
        asked for; call :meth:`extracted` to reach the real records Istari pulled in.
        """
        ext = (self.extension or "").lower()
        return ext.startswith("istari_") and ext.endswith("metadata")

    def extracted(self) -> list[Resource]:
        """The records extracted from this connected pointer into Istari — the real data behind the stub.

        Aliases: contents inside data records requirements search find where-is
        locate full-text sweep

        Answers "what data is inside this connected DOORS/Jira/Confluence file". A
        connected pointer's real content lives in the artifacts Istari extracted from
        it; this returns those resources (equivalent to
        ``related(direction="outgoing")``). Read each returned resource for the actual
        content — the external system itself is NOT reachable from here (you cannot
        fetch its URL or follow the link), so report these extracted records and hand
        the user the link rather than implying you read the external page. Empty if
        nothing has been extracted yet, or if this is not a connected pointer — check
        :attr:`is_connected_pointer` first.

        To FIND a fact when you do not know which file holds it, do NOT open pointers
        one at a time — run the COMPLETE survey once and read it. ``contents`` with
        ``include_extracted=True`` returns every tracked resource AND everything
        extracted from every connected pointer in a single call::

            # branch = system.get_branch("<name>") or the branch you are working in.
            survey = branch.contents(include_extracted=True, max_chars_per_file=2000)
            # Judge relevance by READING the rows — do NOT pre-filter with a keyword
            # match. A substring grep misses a requirement phrased differently than
            # your query (e.g. "34 ft span: VERIFIED" for "is the wingspan verified?"),
            # which is how a content search silently reports "not found" for data that
            # is right there. Rows carrying ``extracted_from`` are the extracted records.
            result = survey
            # Then read the single row that holds the answer in full:
            #   client.resources.get("<resource_id>").read_text()

        Do this BEFORE concluding a fact is not in the system: a branch listing shows
        only tracked resources, so the answer is often inside a connected pointer's
        extraction, which the listing never shows.
        """
        return self.related(direction="outgoing")


class TrackedResource(Resource):
    """A branch tracked file joined with its resource.

    Returned by ``branch.resources()`` / ``systems.branches.resources()`` and
    ``branch.search()`` / ``systems.branches.search()``. It **is** a
    :class:`Resource`, so every resource field (``resource_id``,
    ``name``, ``size``, ``description``, ``mime``, ``extension``,
    ``resource_type``, ``version_name``, tokens, ...) and every capability
    (Readable ``read_bytes()`` / ``read_text()`` / ``read_json()`` /
    Archivable, Shareable, Taggable, Classifiable) is
    available directly.

    It additionally carries the branch git-context of the tracked file:

    - ``path`` — the file's path within the system configuration.
    - ``specifier_type`` — "Locked" (pinned to a revision) or "Latest"
      (tracks the latest revision).
    - ``current_file_revision_id`` — the revision the branch currently resolves to.
    - ``pinned_file_revision_id`` — the pinned revision ("Locked" only), else None.
    - ``tracked_file_id`` — the TrackedFile row id (distinct from resource_id).
    - ``tracked_file`` — the raw TrackedFile DTO, if you need the rest of it.

    Example::

        for f in branch.resources():
            print(f.path, f.name, f.size, f.specifier_type)
            text = f.read_text()
    """

    if TYPE_CHECKING:
        _tracked_file: TrackedFile

    @classmethod
    def _attach(cls, resource: Resource, tracked_file: TrackedFile) -> TrackedResource:
        """Re-class an already-bound Resource as a TrackedResource in place (zero-copy).

        ``resource`` keeps its manager and all its fields; the tracked file rides
        along as plain data so the branch/tracking context is available too.
        """
        resource.__class__ = cls
        object.__setattr__(resource, "_tracked_file", tracked_file)
        return resource  # type: ignore[return-value]

    @property
    def tracked_file(self) -> TrackedFile:
        """The underlying v2 TrackedFile DTO (full branch/tracking context)."""
        return self._tracked_file

    @property
    def path(self) -> str:
        """The tracked file's path within the system configuration."""
        return self._tracked_file.path

    @property
    def specifier_type(self) -> str:
        """"Locked" (pinned to a specific revision) or "Latest" (tracks the latest)."""
        st = self._tracked_file.specifier_type
        return st.value if hasattr(st, "value") else str(st)

    @property
    def current_file_revision_id(self) -> str:
        """The file revision this branch currently resolves the tracked file to."""
        return self._tracked_file.current_file_revision_id

    @property
    def pinned_file_revision_id(self) -> str | None:
        """The pinned revision id for a "Locked" tracked file, else None."""
        return self._tracked_file.pinned_file_revision_id

    @property
    def tracked_file_id(self) -> str:
        """The TrackedFile row id (distinct from resource_id)."""
        return self._tracked_file.id


class ResourceRevision(ResourceRevisionDto, ClientHaving, Readable):
    """A single point-in-time revision of a resource.

    Fields: file_revision_id (also accessible as .id),
    name (str | None), extension (str | None), size (int | None, bytes),
    mime (str | None), description (str | None), version_name (str | None),
    display_name (str | None), external_identifier (str | None),
    content_token, archived (bool | None),
    created (datetime | None), created_by_id (str).

    Readable: call read_bytes(), read_text(), or read_json()
    to fetch revision content or metadata from storage.
    Use .id (alias for file_revision_id) when passing this revision to Branch.commit().
    """

    #: See :class:`Resource.file_id` — kept off the facade data model (excluded from
    #: dumps/JSON and repr) while still populated by the generated DTO.
    file_id: StrictStr = Field(exclude=True, repr=False)

    @property
    def id(self) -> str:
        """Alias for file_revision_id — use when passing a revision to Branch.commit()."""
        return self.file_revision_id


class Comment(CommentDto, ClientHaving, Readable, Archivable):
    """A comment attached to a resource.

    The comment body is stored as a content blob. Readable: call read_bytes(),
    read_text(), or read_json() to retrieve the comment body
    from storage. Archivable: call archive() to soft-delete or restore() to
    reinstate the comment.
    """


class RevisionRelationship(RevisionRelationshipDto, ClientHaving):
    """A lineage/provenance link between two resource revisions (e.g. produces / derived-from).

    Fields: id, relationship_type_id, relationship_type_name (str, forward
    direction, e.g. "produces"), relationship_type_name_inverse (str, reverse
    direction, e.g. "produced_by"), left_revision (the source revision's full
    details), right_revision (the derived revision's full details),
    created (datetime), created_by_id (str).

    The endpoints are the full revision records (``left_revision`` /
    ``right_revision``), not bare ids; read each one's ``.file_revision_id``
    (also ``.id``) for its revision id.

    Data-only: no content to read, no archive/restore capability.
    """


class RelationshipType(RevisionRelationshipTypeDto, ClientHaving):
    """A named type that can be applied to relationships between resource revisions.

    Fields: id, name (str, forward direction, e.g. "produces"),
    name_inverse (str, reverse direction, e.g. "produced_by"),
    description (str), created (datetime).

    Data-only: use the id when creating a RevisionRelationship via
    istari.resources.relationships.create().
    """
