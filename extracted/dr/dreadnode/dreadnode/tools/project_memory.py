"""Agent-facing toolset for durable platform project memory."""

import os
import re
import typing as t

from pydantic import Field

from dreadnode.agents.tools import Toolset, tool_method
from dreadnode.app.api.client import AuthenticationError, ConflictError, NotFoundError
from dreadnode.tracing.span import get_current_task_span

_STATUS_RE = re.compile(r"^(?P<status>\d{3}):\s*(?P<detail>.*)$")
_PROJECT_MEMORY_SCOPE_PROJECT = "project"


class ProjectMemory(Toolset):
    """Platform-backed durable memory scoped to the active project."""

    session_id: str = Field(..., min_length=1, description="Active runtime session identifier.")
    project_key: str | None = Field(
        default=None, description="Active project key for memory tools."
    )
    scope_kind: str = Field(
        default=_PROJECT_MEMORY_SCOPE_PROJECT,
        min_length=1,
        description="Project memory scope kind. Defaults to 'project'.",
    )
    capability_id: str | None = Field(
        default=None,
        description="Optional capability identifier for write provenance.",
    )

    @tool_method(name="list_project_memories")
    def list_memories(
        self,
        *,
        include_closed: t.Annotated[
            bool,
            "Include closed memories in results. Defaults to false.",
        ] = False,
        subtype: t.Annotated[
            str | None,
            "Optional subtype filter.",
        ] = None,
        limit: t.Annotated[
            int,
            "Maximum number of records to return (1-200).",
        ] = 50,
    ) -> dict[str, t.Any]:
        """List durable memories for the active project."""
        try:
            api, org, workspace, project = self._resolve_context()
            payload = api.list_project_memories(
                org,
                workspace,
                project,
                scope_kind=self.scope_kind,
                include_closed=include_closed,
                subtype=subtype,
                limit=limit,
            )
            memories = payload.get("memories") if isinstance(payload, dict) else []
            if not isinstance(memories, list):
                memories = []
            return {
                "ok": True,
                "operation": "list_memories",
                "project": project,
                "scope_kind": self.scope_kind,
                "count": len(memories),
                "memories": memories,
                "error": None,
            }
        except Exception as exc:
            return self._error_response("list_memories", exc)

    @tool_method(name="get_project_memory")
    def get_memory(
        self,
        memory_id: t.Annotated[str, "Project memory UUID to load."],
        *,
        include_closed: t.Annotated[
            bool,
            "Allow loading closed memories.",
        ] = False,
    ) -> dict[str, t.Any]:
        """Load one durable project memory by id."""
        try:
            api, org, workspace, project = self._resolve_context()
            payload = api.get_project_memory(
                org,
                workspace,
                project,
                memory_id=memory_id,
                scope_kind=self.scope_kind,
                include_closed=include_closed,
            )
        except Exception as exc:
            return self._error_response("get_memory", exc)
        else:
            memory = payload.get("memory") if isinstance(payload, dict) else None
            return {
                "ok": True,
                "operation": "get_memory",
                "project": project,
                "scope_kind": self.scope_kind,
                "memory": memory,
                "error": None,
            }

    @tool_method(name="save_project_memory")
    def save_memory(
        self,
        title: t.Annotated[str, "Memory title."],
        body: t.Annotated[str, "Memory body content."],
        *,
        summary: t.Annotated[str | None, "Optional summary."] = None,
        subtype: t.Annotated[str | None, "Optional subtype tag."] = None,
        payload_json: t.Annotated[
            dict[str, t.Any] | None,
            "Optional structured payload attached to the memory.",
        ] = None,
        memory_id: t.Annotated[
            str | None,
            "Memory UUID for updates. Omit to create.",
        ] = None,
        expected_version: t.Annotated[
            int | None,
            "Required for updates; optimistic concurrency version.",
        ] = None,
    ) -> dict[str, t.Any]:
        """Create or update durable project memory."""
        try:
            api, org, workspace, project = self._resolve_context()
            provenance, warnings = self._write_provenance()
            payload = api.save_project_memory(
                org,
                workspace,
                project,
                scope_kind=self.scope_kind,
                title=title,
                summary=summary,
                body=body,
                subtype=subtype,
                payload_json=payload_json,
                memory_id=memory_id,
                expected_version=expected_version,
                runtime_id=provenance.get("runtime_id"),
                session_id=provenance.get("session_id"),
                run_id=provenance.get("run_id"),
                tool_event_id=provenance.get("tool_event_id"),
                capability_id=provenance.get("capability_id"),
            )
        except Exception as exc:
            return self._error_response("save_memory", exc)
        else:
            memory = payload.get("memory") if isinstance(payload, dict) else None
            return {
                "ok": True,
                "operation": "save_memory",
                "project": project,
                "scope_kind": self.scope_kind,
                "memory": memory,
                "warnings": warnings,
                "error": None,
            }

    @tool_method(name="close_project_memory")
    def close_memory(
        self,
        memory_id: t.Annotated[str, "Project memory UUID to close."],
        expected_version: t.Annotated[int, "Current latest version for optimistic close."],
        close_reason: t.Annotated[str, "Close reason (resolved, stale, duplicate, etc.)."],
        *,
        note: t.Annotated[str | None, "Optional close note for audit trail."] = None,
    ) -> dict[str, t.Any]:
        """Close a durable project memory record."""
        try:
            api, org, workspace, project = self._resolve_context()
            provenance, warnings = self._write_provenance()
            payload = api.close_project_memory(
                org,
                workspace,
                project,
                scope_kind=self.scope_kind,
                memory_id=memory_id,
                expected_version=expected_version,
                close_reason=close_reason,
                runtime_id=provenance.get("runtime_id"),
                session_id=provenance.get("session_id"),
                run_id=provenance.get("run_id"),
                tool_event_id=provenance.get("tool_event_id"),
                capability_id=provenance.get("capability_id"),
                note=note,
            )
        except Exception as exc:
            return self._error_response("close_memory", exc)
        else:
            memory = payload.get("memory") if isinstance(payload, dict) else None
            return {
                "ok": True,
                "operation": "close_memory",
                "project": project,
                "scope_kind": self.scope_kind,
                "memory": memory,
                "warnings": warnings,
                "error": None,
            }

    def _resolve_context(self) -> tuple[t.Any, str, str, str]:
        """Resolve API client + active org/workspace/project from the runtime session/profile."""
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
            raise RuntimeError("No active project found for ProjectMemory toolset")
        return default_project

    def _write_provenance(self) -> tuple[dict[str, str | None], list[str]]:
        """Collect server-injected write provenance for memory mutations."""
        span = get_current_task_span()
        run_id = span.run_id if span is not None else None
        tool_event_id = span.task_id if span is not None else None
        runtime_id = os.environ.get("DREADNODE_RUNTIME_ID", "").strip() or None
        capability_id = self.capability_id.strip() if self.capability_id else None

        warnings: list[str] = []
        if capability_id is None:
            warnings.append("capability_id_unavailable")

        return (
            {
                "runtime_id": runtime_id,
                "session_id": self.session_id,
                "run_id": run_id,
                "tool_event_id": tool_event_id,
                "capability_id": capability_id,
            },
            warnings,
        )

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
