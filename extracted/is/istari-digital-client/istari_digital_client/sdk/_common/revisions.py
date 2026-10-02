"""Revisions sub-manager (reached via ``istari.resources.revisions``).

Create, get, and list revisions of a resource, returning ResourceRevision objects.
Child-collection methods take the parent ``resource_id`` as their first positional argument.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from istari_digital_client.sdk._base import Page
from istari_digital_client.sdk._common._capabilities import _SupportsRead
from istari_digital_client.sdk._common.resource_types import ResourceRevision
from istari_digital_client.sdk._generated.v3.models.resource_revision_create_dto import (
    ResourceRevisionCreateDto,
)
from istari_digital_client.sdk._generated.v3.models.token_create_dto import TokenCreateDto

_log = logging.getLogger(__name__)


class Revisions(_SupportsRead):
    """Manage a resource's revisions (versions): create, get, and list.

    Aliases: revision version history


    Reached via ``istari.resources.revisions``. All methods take ``resource_id``
    as the first positional argument.

    Sub-managers: none (revisions are a leaf collection).

    Usage::

        # 1. Create a new revision by uploading a local file
        rev = istari.resources.revisions.create(
            resource_id, "/path/to/model_v2.onnx", version_name="v2.0"
        )

        # 2. List all revisions for the resource
        for r in istari.resources.revisions.list(resource_id):
            print(r.file_revision_id, r.version_name)

        # 3. Fetch a single revision by id
        rev = istari.resources.revisions.get(resource_id, rev.file_revision_id)

        # 4. Read its content
        data = rev.read_bytes()
    """

    def create(
        self,
        resource_id: str,
        path: str | Path,
        *,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
    ) -> ResourceRevision:
        """Upload a file and register it as a new revision of an existing resource.

        Mutates: true

        Aliases: upload new

        ``resource_id`` is the UUID of the parent resource. ``path`` is the local
        filesystem path of the file to upload. ``description``, ``version_name``,
        ``external_identifier``, and ``display_name`` are optional metadata attached to
        the revision.

        The file is uploaded to storage first, then registered with the registry.
        If the registry call fails after the upload succeeds, a warning is logged
        (including the content SHA for manual cleanup) and the original exception is
        re-raised. The caller does not need to take any special action for this case.

        Returns a ResourceRevision with fields: file_revision_id (also .id),
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), description (str | None), version_name (str | None),
        display_name (str | None), external_identifier (str | None),
        content_token, archived (bool | None),
        created (datetime | None), created_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        to fetch content from storage.

        Raises NotFoundError if resource_id does not exist.
        Raises PermissionDeniedError if the caller cannot write to the resource.
        """
        rev = self._engine.storage.upload(
            path,
            display_name=display_name,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
        )
        try:
            dto = self._call(
                self._engine.v3_api.create_resource_revision,
                resource_id,
                resource_revision_create_dto=ResourceRevisionCreateDto(
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
                ),
            )
        except Exception:
            _log.warning(
                "create_resource_revision failed after storage upload succeeded; "
                "blobs with sha=%s may be orphaned in storage",
                rev.content_token.sha,
            )
            raise
        return ResourceRevision._bind(dto, mgr=self)

    def get(self, resource_id: str, revision_id: str) -> ResourceRevision:
        """Fetch a single revision of a resource by its UUID.

        ``resource_id`` is the UUID of the parent resource. ``revision_id`` is the
        UUID of the specific revision (the file_revision_id value on the revision).

        Returns a ResourceRevision with fields: file_revision_id (also .id),
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), description (str | None), version_name (str | None),
        display_name (str | None), external_identifier (str | None),
        content_token, archived (bool | None),
        created (datetime | None), created_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        to fetch content from storage.

        Raises NotFoundError if either resource_id or revision_id does not exist.
        Raises PermissionDeniedError if the caller cannot see the resource.
        """
        dto = self._call(
            self._engine.v3_api.get_resource_revision, resource_id, revision_id
        )
        return ResourceRevision._bind(dto, mgr=self)

    def list(
        self,
        resource_id: str,
        *,
        size: int | None = None,
        file_revision_id: list[str] | None = None,
        created_by_id: list[str] | None = None,
        name: list[str] | None = None,
        description: list[str] | None = None,
        version_name: list[str] | None = None,
        external_identifier: list[str] | None = None,
        display_name: list[str] | None = None,
        mime_type: list[str] | None = None,
    ) -> Page[ResourceRevision]:
        """List revisions of a resource and return an auto-paging sequence of ResourceRevision objects.

        Aliases: history versions

        ``resource_id`` is the UUID of the parent resource. Iterate the returned Page
        directly — subsequent pages are fetched automatically.

        All filter parameters are optional lists of strings; multiple values in one list
        are treated as OR filters. ``size`` controls the page size (default: server
        default). Pass ``file_revision_id`` to retrieve specific revisions by UUID.
        Pass ``created_by_id``, ``name``, ``description``, ``version_name``,
        ``external_identifier``, ``display_name``, or ``mime_type`` to narrow results.

        Each ResourceRevision has fields: file_revision_id (also .id),
        name (str | None), extension (str | None), size (int | None, bytes),
        mime (str | None), description (str | None), version_name (str | None),
        display_name (str | None), external_identifier (str | None),
        content_token, archived (bool | None),
        created (datetime | None), created_by_id (str).
        Readable: call read_bytes(), read_text(), or read_json()
        to fetch content from storage.

        Raises NotFoundError if resource_id does not exist.
        Raises PermissionDeniedError if the caller cannot see the resource.
        """

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_resource_revisions,
                resource_id,
                cursor=cursor,
                size=size,
                file_revision_id=file_revision_id,
                created_by_id=created_by_id,
                name=name,
                description=description,
                version_name=version_name,
                external_identifier=external_identifier,
                display_name=display_name,
                mime_type=mime_type,
            )

        return self._paginate(fetch, lambda d: ResourceRevision._bind(d, mgr=self))

    # The Readable hook (_read_contents) is inherited from _SupportsRead —
    # revisions carry the same content token.
