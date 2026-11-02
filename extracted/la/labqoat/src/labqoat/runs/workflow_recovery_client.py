"""Typed bounded previews and frozen graph progress for failed-descendant recovery."""

from urllib.parse import urlencode

from labqoat._generated.recovery_request import RecoveryRequest
from labqoat._generated.workflow_plan_page import WorkflowPlanPage
from labqoat._generated.workflow_preview import WorkflowPreview
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.runs.recovery_client import RecoveryClient
from labqoat.runs.recovery_handle import RecoveryHandle


class WorkflowRecoveryClient(BaseClient):
    """Recover retained orchestration with explicit resume-required child policy and ordinary operation handles."""

    def preview(
        self,
        run_id: str,
        *,
        parent_id: str | None = None,
        include_cancelled: bool = False,
        limit: int = 50,
        cursor: str | None = None,
    ) -> WorkflowPreview:
        """Read an advisory root and bounded child page; select a nested parent to explore its children."""
        query = self._page(limit, cursor)
        query["include_cancelled"] = str(include_cancelled).lower()
        if parent_id is not None:
            query["parent_id"] = parent_id
        path = f"/api/v1/runs/{self.encode_ref(run_id)}/recovery/workflow?" + urlencode(query)
        page = self.decode(self.send("GET", path), path, WorkflowPreview.from_dict)
        if page.run_id != run_id or page.parent_id != (parent_id or run_id):
            raise ApiError("Workflow preview identity mismatch")
        return page

    def plan(self, run_id: str, operation_id: str, *, limit: int = 50, cursor: str | None = None) -> WorkflowPlanPage:
        """Read frozen node selections and captured child admission/cycle progress for one operation."""
        path = f"/api/v1/runs/{self.encode_ref(run_id)}/recoveries/{self.encode_ref(operation_id)}/workflow?"
        path += urlencode(self._page(limit, cursor))
        page = self.decode(self.send("GET", path), path, WorkflowPlanPage.from_dict)
        if page.run_id != run_id or page.operation_id != operation_id:
            raise ApiError("Workflow plan identity mismatch")
        return page

    def recover(
        self,
        run_id: str,
        *,
        expected_state_version: int,
        reason: str = "",
        include_cancelled: bool = False,
        operation_key: str | None = None,
    ) -> RecoveryHandle:
        """Freeze failed-only graph recovery; interrupted fits must resume and never-started children restart."""
        request = RecoveryRequest(
            expected_state_version,
            "restart",
            scope="failed_descendants",
            child_strategy="resume_required",
            include_cancelled=include_cancelled,
            reason=reason,
        )
        return RecoveryClient(self._transport).create(run_id, request, operation_key=operation_key)

    @staticmethod
    def _page(limit: int, cursor: str | None) -> dict[str, str]:
        """Keep page boundaries explicit and preserve opaque server cursors."""
        query = {"limit": str(limit)}
        if cursor is not None:
            query["cursor"] = cursor
        return query
