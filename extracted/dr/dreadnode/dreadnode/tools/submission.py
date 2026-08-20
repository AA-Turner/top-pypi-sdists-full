"""Agent-facing toolset for staging platform item submissions."""

import os
import re
import typing as t

from pydantic import Field

from dreadnode.agents.tools import Toolset, tool_method
from dreadnode.app.api.client import AuthenticationError, ConflictError, NotFoundError
from dreadnode.tracing.span import get_current_task_span

_STATUS_RE = re.compile(r"^(?P<status>\d{3}):\s*(?P<detail>.*)$")
_SUBMISSION_ACTION_LIMIT = 200


class Submission(Toolset):
    """Platform-backed item staging tools scoped to the active project.

    Local TUI sessions do not require ``DREADNODE_RUNTIME_ID``. Managed sandboxes
    supply their runtime identity automatically.
    """

    session_id: str = Field(..., min_length=1, description="Active runtime session identifier.")
    project_key: str | None = Field(
        default=None, description="Active project key for staging tools."
    )
    capability_name: str = Field(
        ..., min_length=1, description="Active capability name for staging provenance."
    )
    capability_version: str = Field(
        ..., min_length=1, description="Active capability version for staging provenance."
    )

    @tool_method(name="list_staging_actions")
    def list_staging_actions(self) -> dict[str, t.Any]:
        """List enabled submission actions that allow agent staging."""
        try:
            api, org, workspace, project = self._resolve_context()
            actions = self._list_agent_actions(api, org, workspace, project)
            return {
                "ok": True,
                "operation": "list_staging_actions",
                "project": project,
                "count": len(actions),
                "actions": actions,
                "error": None,
            }
        except Exception as exc:
            return self._error_response("list_staging_actions", exc)

    @tool_method(name="stage_item")
    def stage_item(
        self,
        item_id: t.Annotated[str, "Item UUID to stage."],
        action_id: t.Annotated[str, "Submission action UUID to stage for."],
    ) -> dict[str, t.Any]:
        """Stage an item for later human review with platform-validated provenance."""
        try:
            api, org, workspace, project = self._resolve_context()
            stage = api.create_submission_stage(
                org,
                workspace,
                project,
                item_id=item_id,
                action_id=action_id,
                provenance=self._stage_provenance(),
            )
        except Exception as exc:
            return self._error_response("stage_item", exc)
        else:
            return {
                "ok": True,
                "operation": "stage_item",
                "project": project,
                "item_id": item_id,
                "action_id": action_id,
                "stage": stage,
                "error": None,
            }

    def _resolve_context(self) -> tuple[t.Any, str, str, str]:
        """Resolve API client + active org/workspace/project from the runtime profile."""
        from dreadnode import _get_default_instance

        instance = _get_default_instance()
        if not instance.can_sync:
            raise RuntimeError("Platform sync is disabled for this runtime session")

        profile = instance.profile
        org = profile.org_key
        workspace = profile.workspace_key
        project = self._resolve_project_key(instance=instance, org=org, workspace=workspace)
        return instance.api, org, workspace, project

    def _resolve_project_key(self, *, instance: t.Any, org: str, workspace: str) -> str:
        """Resolve project key from session override, profile, or workspace default."""
        if self.project_key is not None and self.project_key.strip():
            return self.project_key.strip()

        profile = instance.profile
        profile_project = getattr(profile, "project_key", None)
        if isinstance(profile_project, str) and profile_project.strip():
            return profile_project.strip()

        instance_project = getattr(instance, "project", None)
        if isinstance(instance_project, str) and instance_project.strip():
            return instance_project.strip()

        default_project = instance.api.get_default_project_key(org, workspace)
        if default_project is None:
            raise RuntimeError("No active project found for staging toolset")
        return default_project

    def _list_agent_actions(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        project: str,
        *,
        first_only: bool = False,
    ) -> list[dict[str, t.Any]]:
        """Return actions that are safe to expose to agents."""
        actions: list[dict[str, t.Any]] = []
        page = 1
        while True:
            payload = api.list_submission_actions(
                org,
                workspace,
                project,
                page=page,
                limit=_SUBMISSION_ACTION_LIMIT,
            )
            raw_actions = payload.get("actions") if isinstance(payload, dict) else []
            if not isinstance(raw_actions, list):
                break
            page_actions = [
                action
                for action in raw_actions
                if isinstance(action, dict)
                and action.get("agent_stage") is True
                and action.get("enabled") is not False
                and action.get("connection_deleted") is not True
                and action.get("deleted_at") is None
            ]
            actions.extend(page_actions)
            if first_only and page_actions:
                break

            total = payload.get("total") if isinstance(payload, dict) else None
            if isinstance(total, int):
                if page * _SUBMISSION_ACTION_LIMIT >= total:
                    break
            elif len(raw_actions) < _SUBMISSION_ACTION_LIMIT:
                break
            page += 1
        return actions

    def _stage_provenance(self) -> dict[str, str | None]:
        """Collect server-injected provenance for an item stage."""
        span = get_current_task_span()
        return {
            "runtime_id": os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None,
            "platform_session_id": self.session_id,
            "root_run_id": span.run_id if span is not None else None,
            "capability_name": self.capability_name,
            "capability_version": self.capability_version,
            "current_task_id": span.task_id if span is not None else None,
            "trace_id": span.trace_id if span is not None else None,
            "span_id": span.span_id if span is not None else None,
        }

    def _error_response(self, operation: str, exc: Exception) -> dict[str, t.Any]:
        """Normalize failures as structured agent-friendly JSON."""
        return {
            "ok": False,
            "operation": operation,
            "error": self._normalize_error(exc),
        }

    def _normalize_error(self, exc: Exception) -> dict[str, t.Any]:
        """Map runtime/client exceptions into stable error payloads."""
        message = str(exc).strip() or type(exc).__name__
        if isinstance(exc, AuthenticationError):
            return {
                "code": "authentication_error",
                "status_code": 401,
                "message": message,
            }
        if isinstance(exc, NotFoundError):
            return {
                "code": "not_found",
                "status_code": 404,
                "message": message,
            }
        if isinstance(exc, ConflictError):
            return {
                "code": "conflict",
                "status_code": 409,
                "message": message,
            }

        status_match = _STATUS_RE.match(message)
        if status_match:
            status_code = int(status_match.group("status"))
            detail = status_match.group("detail") or message
            code_map = {
                400: "invalid_request",
                401: "authentication_error",
                403: "forbidden",
                404: "not_found",
                409: "conflict",
                422: "validation_error",
            }
            return {
                "code": code_map.get(status_code, "request_failed"),
                "status_code": status_code,
                "message": detail,
            }

        return {
            "code": "request_failed",
            "message": message,
        }
