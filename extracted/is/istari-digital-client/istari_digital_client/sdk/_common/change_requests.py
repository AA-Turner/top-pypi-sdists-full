"""ChangeRequests sub-manager (reached via ``istari.systems.change_requests``).

Create, list, and update change requests for a system. All methods take
``system_id`` as the first positional argument.
"""

from __future__ import annotations

from typing import Any

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.system_types import ChangeRequest
from istari_digital_client.sdk._generated.v2.models.change_request_create_request import (
    ChangeRequestCreateRequest,
)
from istari_digital_client.sdk._generated.v2.models.change_request_merge_request import (
    ChangeRequestMergeRequest,
)
from istari_digital_client.sdk._generated.v2.models.change_request_update_request import (
    ChangeRequestUpdateRequest,
)


class ChangeRequests(_Manager):
    """Open, review, and merge change requests (merge / pull requests) between branches.

    Aliases: change-request merge-request pull-request PR review propose

    Reached via ``istari.systems.change_requests``. All methods take ``system_id``
    as the first positional argument.

    Sub-managers: none (change requests are a leaf collection).

    Usage::

        # 1. Open a change request proposing to merge a feature branch into main
        main = istari.systems.branches.get(system_id, "main")
        feature = istari.systems.branches.get(system_id, "feature/my-change")
        cr = istari.systems.change_requests.create(
            system_id,
            source_id=feature.id,
            target_id=main.id,
            title="Add new sensor model",
        )
        print(cr.change_request_id, cr.status)  # status starts as "OPEN"

        # 2. List all open change requests for a system
        for cr in istari.systems.change_requests.list(system_id, status="OPEN"):
            print(cr.change_request_id, cr.title)

        # 3. Close a change request
        cr.close()
        # or equivalently:
        istari.systems.change_requests.update_status(system_id, cr.change_request_id, "CLOSED")
    """

    def create(
        self,
        system_id: str,
        source_id: str,
        target_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> ChangeRequest:
        """Open a change request proposing to merge ``source_id`` into ``target_id``.

        Mutates: true

        ``source_id`` and ``target_id`` are the UUIDs of the source and target
        branches (snapshot tag ids) respectively. ``title`` and ``description``
        are optional human-readable metadata.

        Returns a ChangeRequest with fields: change_request_id (str, also .id),
        status (str: "OPEN" | "CLOSED"), source_tag_id (str), target_tag_id (str),
        system_id (str), current_source_snapshot_id (str),
        current_target_snapshot_id (str), current_source_tag_revision_id (str),
        current_target_tag_revision_id (str), title (str | None),
        description (str | None), created (datetime), created_by_id (str).
        Object methods: close(), reopen(). The status starts as "OPEN".
        """
        response = self._call(
            self._engine.v2_api.create_change_request,
            system_id,
            ChangeRequestCreateRequest(
                source_tag_id=source_id,
                target_tag_id=target_id,
                title=title,
                description=description,
            ),
        )
        return ChangeRequest._from_response(response, mgr=self, system_id=system_id)

    def get(self, system_id: str, change_request_id: str) -> ChangeRequest:
        """Fetch a single change request by UUID.

        Returns a ChangeRequest (see create() for the field list). Object methods:
        close(), reopen(), merge().

        Raises NotFoundError if the change request does not exist.
        Raises PermissionDeniedError if the caller cannot access the system.
        """
        response = self._call(
            self._engine.v2_api.get_change_request,
            system_id,
            change_request_id,
        )
        return ChangeRequest._from_response(response, mgr=self, system_id=system_id)

    def list(
        self,
        system_id: str,
        *,
        status: str | None = None,
        source_tag_id: str | None = None,
        target_tag_id: str | None = None,
    ) -> Page[ChangeRequest]:
        """List change requests (merge / pull requests) for a system.

        ``status`` filters by change request state: "OPEN" | "CLOSED". Pass None
        to return all change requests regardless of status. ``source_tag_id`` and
        ``target_tag_id`` narrow results to change requests originating from or
        targeting a specific branch UUID. All filters are optional and combinable.

        Returns an auto-paging sequence of ChangeRequest objects. Iterate
        directly — subsequent pages are fetched automatically. Each ChangeRequest
        has fields: change_request_id (str, also .id),
        status (str: "OPEN" | "CLOSED"), source_tag_id (str),
        target_tag_id (str), system_id (str),
        current_source_snapshot_id (str), current_target_snapshot_id (str),
        current_source_tag_revision_id (str),
        current_target_tag_revision_id (str), title (str | None),
        description (str | None), created (datetime), created_by_id (str).
        Object methods: close(), reopen().
        """

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_change_requests,
                system_id,
                status=status,
                source_tag_id=source_tag_id,
                target_tag_id=target_tag_id,
                page=page_num,
                size=100,
            )

        return self._paginate_offset(
            fetch,
            lambda item: ChangeRequest._from_response(
                item, mgr=self, system_id=system_id
            ),
        )

    def update_status(self, system_id: str, cr_id: str, status: str) -> None:
        """Set the status of a change request.

        Mutates: true

        ``cr_id`` is the change request UUID. ``status`` accepts "OPEN" | "CLOSED".
        Prefer the convenience methods close() and reopen() on the ChangeRequest
        object itself rather than calling this directly. Returns None.
        """
        self._call(
            self._engine.v2_api.update_change_request,
            system_id,
            cr_id,
            ChangeRequestUpdateRequest(status=status),
        )

    def merge(
        self,
        system_id: str,
        cr_id: str,
        *,
        comment: str | None = None,
        check_only: bool = False,
        head_pair_token: str | None = None,
    ) -> ChangeRequest:
        """Merge a change request, applying source branch changes to the target.

        Mutates: true

        ``cr_id`` is the change request UUID. ``comment`` is an optional merge
        comment. If ``check_only`` is True, the staleness check is performed but
        the merge is not executed — use this to verify the merge will succeed
        before committing. ``head_pair_token`` is an optional optimistic
        concurrency token.

        Returns the updated ChangeRequest. After a successful merge, the status
        will be "MERGED" and the target branch's snapshot will include the
        source branch's changes.

        Raises ConflictError if the change request is stale (source or target
        has been modified since the CR was created) and cannot be merged.
        """
        response = self._call(
            self._engine.v2_api.merge_change_request,
            system_id,
            cr_id,
            ChangeRequestMergeRequest(comment=comment),
            check_only=check_only,
            x_head_pair_token=head_pair_token,
        )
        return ChangeRequest._from_response(response, mgr=self, system_id=system_id)
