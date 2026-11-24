from __future__ import annotations

import re
from typing import Any

from matrx_ai.db._registry import get_base, get_model
from matrx_ai.utils.carried_failure import FailureDict

ProjectsBase = get_base("ProjectsBase")
Projects = get_model("Projects")

# Fields a caller may set on create / change on update. Everything else (id, org, created_by,
# version, stamps) is never accepted from a caller.
_MUTABLE_FIELDS = frozenset(
    {"name", "description", "status", "priority", "start_date", "target_date", "shown_to"}
)
_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "project"


def _s(v: Any) -> str | None:
    return str(v) if v not in (None, "") else None


def _row(p: Any) -> dict[str, Any]:
    return {
        "id": str(p.id),
        "name": p.name,
        "description": getattr(p, "description", None),
        "status": getattr(p, "status", None),
        "priority": _s(getattr(p, "priority", None)),
        "start_date": _s(getattr(p, "start_date", None)),
        "target_date": _s(getattr(p, "target_date", None)),
        "slug": getattr(p, "slug", None),
        "organization_id": _s(getattr(p, "organization_id", None)),
        "shown_to": _s(getattr(p, "shown_to", None)),
        "created_at": _s(getattr(p, "created_at", None)),
        "updated_at": _s(getattr(p, "updated_at", None)),
        "version": getattr(p, "version", None),
    }


def _not_visible(operation: str, project_id: str) -> dict[str, Any]:
    return {
        "success": False,
        "operation": operation,
        "project_id": project_id,
        "error_type": "not_found",
        "error": f"Project {project_id} was not found, or you do not have access to it.",
    }


def _no_write_access(operation: str, project_id: str) -> dict[str, Any]:
    return {
        "success": False,
        "operation": operation,
        "project_id": project_id,
        "error_type": "no_access",
        "error": f"You can view project {project_id} but you do not have permission to change it.",
    }


def _err(operation: str, error: Exception, **extra: Any) -> dict[str, Any]:
    return FailureDict(
        {"success": False, "operation": operation, "error": str(error), **extra},
        exception=error,
    )


class ProjectsManager(ProjectsBase):
    """projects.projects for a tool acting as the person.

    ACCESS IS NOT DECIDED HERE: callers run these inside the person's RLS session
    (``matrx_ai.tools.person_session``). Every by-id read is authoritative (``use_cache=False``).
    """

    _instance: ProjectsManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> ProjectsManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Any) -> None:
        pass

    async def _read_live(self, project_id: str) -> Any:
        return await self.load_item_or_none(use_cache=False, **self._pk_filter(project_id))

    async def get_project(self, project_id: str) -> dict[str, Any]:
        try:
            project = await self._read_live(project_id)
        except Exception as e:
            return _err("get_project", e, project_id=project_id)
        if project is None or getattr(project, "deleted_at", None) is not None:
            return _not_visible("get_project", project_id)
        return {"success": True, "project": _row(project)}

    async def list_projects(self) -> dict[str, Any]:
        """Every live project the caller can see (RLS), across all their organizations."""
        try:
            rows = await self._get_items(order_by="-updated_at", deleted_at__isnull=True)
            return {"success": True, "projects": [_row(p) for p in rows if p]}
        except Exception as e:
            return _err("list_projects", e)

    async def _unique_slug(self, organization_id: str, base: str) -> str:
        rows = await Projects.filter(organization_id=organization_id, slug__startswith=base).values("slug")
        taken = {r["slug"] for r in rows if r.get("slug")}
        if base not in taken:
            return base
        n = 2
        while f"{base}-{n}" in taken:
            n += 1
        return f"{base}-{n}"

    async def create_project(
        self, user_id: str, name: str, *, organization_id: str, **fields: Any
    ) -> dict[str, Any]:
        if not organization_id:
            return {"success": False, "operation": "create_project", "error": "organization_id is required to create a project."}
        try:
            payload: dict[str, Any] = {
                "name": name,
                "created_by": user_id,
                "organization_id": organization_id,
                "slug": await self._unique_slug(organization_id, _slugify(name)),
            }
            payload.update({k: v for k, v in fields.items() if k in _MUTABLE_FIELDS and v not in (None, "")})
            project = await self.create_item(**payload)
            return {"success": True, "project": _row(project)}
        except Exception as e:
            return _err("create_project", e)

    async def update_project(self, project_id: str, **updates: Any) -> dict[str, Any]:
        safe = {k: v for k, v in updates.items() if k in _MUTABLE_FIELDS}
        if not safe:
            return {"success": False, "operation": "update_project", "project_id": project_id, "error": "No changeable fields provided."}
        try:
            project = await self._read_live(project_id)
        except Exception as e:
            return _err("update_project", e, project_id=project_id)
        if project is None or getattr(project, "deleted_at", None) is not None:
            return _not_visible("update_project", project_id)
        prior = _row(project)
        try:
            async with self._governed_write():
                project = await self._update_item(project, **safe)
        except Exception as e:
            if any(m in str(e) for m in _RLS_REFUSAL_MARKERS):
                return _no_write_access("update_project", project_id)
            return _err("update_project", e, project_id=project_id)
        return {"success": True, "project": _row(project), "prior": prior}


projects_manager_instance = ProjectsManager()
