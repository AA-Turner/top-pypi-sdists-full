"""Comments sub-manager (reached via ``istari.resources.comments``).

Create / get / list / update / archive / restore comments on a resource. A comment
body is an uploaded content blob (mirrors the legacy ``add_comment`` flow), so a
comment is :class:`~istari_digital_client._base.Readable`. Child-collection methods take the parent
``resource_id`` (SDK_REDESIGN.md §5.2).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from istari_digital_client.sdk._base import Page
from istari_digital_client.sdk._generated.v3.models.new_comment_create_dto import NewCommentCreateDto
from istari_digital_client.sdk._generated.v3.models.token_create_dto import TokenCreateDto
from istari_digital_client.sdk._generated.v3.models.update_comment_dto import UpdateCommentDto
from istari_digital_client.sdk._common._capabilities import _SupportsRead
from istari_digital_client.sdk._common.resource_types import Comment


class Comments(_SupportsRead):
    """Manager for a resource's comments: create / get / list / update / (un)archive."""

    def _tokens(self, path: str | Path) -> tuple[TokenCreateDto, TokenCreateDto]:
        """Upload ``path`` and return its (content, properties) create-tokens."""
        rev = self._engine.storage.upload(path)
        return (
            TokenCreateDto(sha=rev.content_token.sha, salt=rev.content_token.salt),
            TokenCreateDto(
                sha=rev.properties_token.sha, salt=rev.properties_token.salt
            ),
        )

    def create(
        self,
        resource_id: str,
        path: str | Path,
        *,
        parent_comment_id: str | None = None,
    ) -> Comment:
        """Post a new comment (or threaded reply) on a resource by uploading a file as its body.

        Mutates: true

        Aliases: comment annotate note reply

        Calls the storage helper to upload the file at ``path``, then calls
        ``create_comment`` on the v3 API with the resulting content and properties
        tokens. ``resource_id`` is the UUID of the resource being commented on. Pass
        ``parent_comment_id`` to attach this comment as a threaded reply to an existing
        comment; omit it to post a top-level comment.
        """
        content_token, properties_token = self._tokens(path)
        dto = self._call(
            self._engine.v3_api.create_comment,
            resource_id,
            new_comment_create_dto=NewCommentCreateDto(
                content_token=content_token,
                properties_token=properties_token,
                parent_comment_id=parent_comment_id,
            ),
        )
        return Comment._bind(dto, mgr=self)

    def get(self, resource_id: str, comment_id: str) -> Comment:
        """Fetch a single comment on a resource by its UUID.

        Calls ``get_comment`` on the v3 API. ``resource_id`` is the UUID of the parent
        resource; ``comment_id`` is the UUID of the comment. Raises
        :exc:`~istari_digital_client._exceptions.NotFoundError` if the comment does not exist.
        """
        dto = self._call(self._engine.v3_api.get_comment, resource_id, comment_id)
        return Comment._bind(dto, mgr=self)

    def list(
        self,
        resource_id: str,
        *,
        size: int | None = None,
        comment_id: list[str] | None = None,
        created_by_id: list[str] | None = None,
    ) -> Page[Comment]:
        """List comments on a resource as an auto-paging sequence of Comment objects.

        Calls ``list_comments`` on the v3 API using cursor-based pagination. Iterating
        the returned ``Page`` automatically fetches subsequent pages. All filter
        parameters are optional: pass a list of UUIDs to ``comment_id`` to retrieve
        specific comments, or filter by author with ``created_by_id``. ``size`` controls
        the page size.
        """

        def fetch(cursor: str | None) -> Any:
            return self._call(
                self._engine.v3_api.list_comments,
                resource_id,
                cursor=cursor,
                size=size,
                comment_id=comment_id,
                created_by_id=created_by_id,
            )

        return self._paginate(fetch, lambda d: Comment._bind(d, mgr=self))

    def update(self, resource_id: str, comment_id: str, path: str | Path) -> Comment:
        """Replace a comment's body with a newly uploaded file and return the updated :class:`~istari_digital_client._common.resource_types.Comment`.

        Mutates: true

        Calls the storage helper to upload the file at ``path``, then calls
        ``update_comment`` on the v3 API with the new content and properties tokens.
        ``resource_id`` is the UUID of the parent resource; ``comment_id`` is the UUID
        of the comment to replace.
        """
        content_token, properties_token = self._tokens(path)
        dto = self._call(
            self._engine.v3_api.update_comment,
            resource_id,
            comment_id,
            update_comment_dto=UpdateCommentDto(
                content_token=content_token, properties_token=properties_token
            ),
        )
        return Comment._bind(dto, mgr=self)

    def archive(self, resource_id: str, comment_id: str) -> None:
        """Archive a comment by its UUID.

        Mutates: true

        Calls ``archive_comment`` on the v3 API. ``resource_id`` is the UUID of the
        parent resource. Archived comments are excluded from default ``list`` results.
        To archive via the rich object, use
        :meth:`~istari_digital_client._base.Archivable.archive` on the ``Comment`` instance instead.
        """
        self._call(self._engine.v3_api.archive_comment, resource_id, comment_id)

    def restore(self, resource_id: str, comment_id: str) -> Comment:
        """Restore a previously archived comment and return the updated :class:`~istari_digital_client._common.resource_types.Comment`.

        Mutates: true

        Calls ``restore_comment`` on the v3 API. ``resource_id`` is the UUID of the
        parent resource; ``comment_id`` is the UUID of the comment to restore.
        """
        dto = self._call(self._engine.v3_api.restore_comment, resource_id, comment_id)
        return Comment._bind(dto, mgr=self)

    # --- Archivable hook (read hooks are inherited from _SupportsRead). Comment
    #     archive/restore is its own endpoint pair keyed by (resource_id, comment_id). ---

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.archive_comment, obj.resource_id, obj.id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v3_api.restore_comment, obj.resource_id, obj.id)
