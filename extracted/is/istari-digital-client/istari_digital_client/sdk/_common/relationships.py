"""Revision relationships sub-manager (``istari.resources.relationships``).

Create typed relationships between two resource revisions, list the relationships
of a revision, and list the available relationship types.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._generated.v3.models.new_revision_relationship_dto import (
    NewRevisionRelationshipDto,
)
from istari_digital_client.sdk._common.resource_types import RelationshipType, RevisionRelationship


class Relationships(_Manager):
    """Trace and manage data lineage — typed provenance links (produces / derived-from) between resource revisions.

    Reached via ``istari.resources.relationships``. Relationships link a source
    revision (left) to a destination revision (right) using a named type from the
    registry. Call list_types() first to discover the type ids available in your
    deployment.

    Sub-managers: none (relationships are a leaf collection).

    Usage::

        # 1. Discover available relationship types and pick one
        for rt in istari.resources.relationships.list_types():
            print(rt.id, rt.name)  # use rt.id as relationship_type_id

        # 2. Create a relationship from one revision to another
        rel = istari.resources.relationships.create(
            left_revision_id=source_rev.file_revision_id,
            right_revision_id=dest_rev.file_revision_id,
            relationship_type_id=rt.id,
        )

        # 3. List all relationships involving a revision
        for r in istari.resources.relationships.list(source_rev.file_revision_id):
            print(r.id, r.relationship_type_name,
                  r.left_revision.file_revision_id, r.right_revision.file_revision_id)
    """

    def create(
        self,
        *,
        left_revision_id: str,
        right_revision_id: str,
        relationship_type_id: str,
    ) -> RevisionRelationship:
        """Link two revisions to record lineage/provenance (e.g. this model produced that artifact).

        Mutates: true

        Aliases: relate link connect

        ``left_revision_id`` is the source revision UUID (the "from" side);
        ``right_revision_id`` is the destination revision UUID (the "to" side).
        Direction is significant: swapping left and right produces a different
        relationship even with the same type.

        ``relationship_type_id`` is the UUID of the relationship type. Call
        list_types() to discover the available types and their ids — the id field
        on each RelationshipType is exactly what you pass here.

        Returns a RevisionRelationship with fields: id, relationship_type_id,
        relationship_type_name (str, e.g. "produces"), relationship_type_name_inverse
        (str, e.g. "produced_by"), left_revision (source revision's full details),
        right_revision (derived revision's full details), created (datetime),
        created_by_id (str). The endpoints are full revision records, not bare ids —
        use ``left_revision.file_revision_id`` / ``right_revision.file_revision_id``.

        Raises NotFoundError if either revision UUID or the relationship_type_id
        does not exist.
        Raises PermissionDeniedError if the caller cannot write relationships.
        Raises ConflictError if an identical relationship already exists.
        """
        dto = self._call(
            self._engine.v3_api.create_revision_relationship,
            new_revision_relationship_dto=NewRevisionRelationshipDto(
                relationship_type_id=relationship_type_id,
                left_revision_id=left_revision_id,
                right_revision_id=right_revision_id,
            ),
        )
        return RevisionRelationship._bind(dto, mgr=self)

    def list(
        self,
        revision_id: str,
        *,
        size: int | None = None,
        left_revision_id: list[str] | None = None,
        right_revision_id: list[str] | None = None,
        owning_entity_type: list[str] | None = None,
    ) -> Page[RevisionRelationship]:
        """List a revision's lineage — the provenance relationships it appears in (upstream and downstream).

        ``revision_id`` is the UUID of the revision to query. Returns relationships
        where that revision appears on either the left (source) or right (destination)
        side. Iterate the returned Page directly — subsequent pages are fetched
        automatically.

        Filter further with optional lists of UUIDs: ``left_revision_id`` restricts to
        relationships originating from those revisions; ``right_revision_id`` restricts
        to relationships pointing to those revisions. ``owning_entity_type`` narrows by
        entity kind. Multiple values in a list are treated as OR filters. ``size``
        controls the page size (default: server default).

        Each RevisionRelationship has fields: id, relationship_type_id,
        relationship_type_name (str, e.g. "produces"), relationship_type_name_inverse
        (str, e.g. "produced_by"), left_revision (source revision's full details),
        right_revision (derived revision's full details), created (datetime),
        created_by_id (str). The endpoints are full revision records, not bare ids —
        use ``left_revision.file_revision_id`` / ``right_revision.file_revision_id``.

        Raises NotFoundError if revision_id does not exist.
        Raises PermissionDeniedError if the caller cannot see the revision.
        """

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_revision_relationships,
                revision_id,
                cursor=cursor,
                size=size,
                left_revision_id=left_revision_id,
                right_revision_id=right_revision_id,
                owning_entity_type=owning_entity_type,
            )

        return self._paginate(fetch, lambda d: RevisionRelationship._bind(d, mgr=self))

    def list_types(self, *, size: int | None = None) -> Page[RelationshipType]:
        """List the relationship types available in this deployment and return an auto-paging sequence of RelationshipType objects.

        Use this method to discover what relationship types exist before calling
        create(). Iterate the returned Page directly — subsequent pages are fetched
        automatically.

        Each RelationshipType has fields: id (str), name (str, forward direction,
        e.g. "produces"), name_inverse (str, reverse direction, e.g. "produced_by"),
        description (str), created (datetime).
        The id field is what you pass as ``relationship_type_id`` to create().

        ``size`` controls the page size (default: server default).

        Raises PermissionDeniedError if the caller cannot list relationship types.
        """

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_revision_relationship_types,
                cursor=cursor,
                size=size,
            )

        return self._paginate(fetch, lambda d: RelationshipType._bind(d, mgr=self))
