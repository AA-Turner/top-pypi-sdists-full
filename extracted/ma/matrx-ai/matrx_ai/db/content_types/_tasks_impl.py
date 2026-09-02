from __future__ import annotations

import textwrap
from typing import Any, Literal

from matrx_ai.db._registry import get_base, get_model

TasksBase = get_base("TasksBase")
Tasks = get_model("Tasks")


# ---------------------------------------------------------------------------
# XML rendering templates
# ---------------------------------------------------------------------------

XML_TEMPLATE_FULL = """\
<task>
  <id>{id}</id>
  <title>{title}</title>
  <status>{status}</status>
  <priority>{priority}</priority>
  <due_date>{due_date}</due_date>
  <project_id>{project_id}</project_id>
  <assignee_id>{assignee_id}</assignee_id>
  <description>
{description}
  </description>
</task>"""

XML_TEMPLATE_COMPACT = """\
<task>
  <id>{id}</id>
  <title>{title}</title>
  <status>{status}</status>
  <priority>{priority}</priority>
  <description>{description}</description>
</task>"""

DEFAULT_XML_TEMPLATE = "full"

_XML_TEMPLATES: dict[str, str] = {
    "full": XML_TEMPLATE_FULL,
    "compact": XML_TEMPLATE_COMPACT,
}


def render_task_snapshot_xml(data: dict[str, Any], template: str = DEFAULT_XML_TEMPLATE) -> str:
    """Render an LLM-friendly task XML block from a client-supplied dict.

    The "snapshot" / attach-by-value path: the caller hands us the task fields
    directly and we render them verbatim without any database fetch. Mirrors
    TasksManager._to_llm_xml but reads from a plain dict instead of a model.
    """
    tmpl = _XML_TEMPLATES.get(template, XML_TEMPLATE_FULL)
    description = textwrap.indent(str(data.get("description") or "").strip(), "    ")
    return tmpl.format(
        id=data.get("id") or "",
        title=data.get("title") or "",
        status=data.get("status") or "",
        priority=data.get("priority") or "",
        due_date=data.get("due_date") or "",
        project_id=data.get("project_id") or "",
        assignee_id=data.get("assignee_id") or "",
        description=description,
    )


# ---------------------------------------------------------------------------
# Fields the LLM must never touch.
# ---------------------------------------------------------------------------
_IMMUTABLE_FIELDS = frozenset(
    {
        "id",
        "user_id",
        "created_at",
        "updated_at",
        "dto",
    }
)

_MUTABLE_FIELDS = frozenset(
    {
        "title",
        "description",
        "status",
        "priority",
        "due_date",
        "project_id",
        "parent_task_id",
        "assignee_id",
        "organization_id",
        "settings",
        "is_public",
    }
)

TaskStatus = Literal["incomplete", "completed"]
TaskPriority = Literal["low", "medium", "high", "urgent"]


# ---------------------------------------------------------------------------
# Result / error helpers
# ---------------------------------------------------------------------------


def _ok(task: Tasks) -> dict[str, Any]:
    return {"success": True, "task": task.to_dict()}


def _err(operation: str, task_id: str, error: Exception, **extra: Any) -> dict[str, Any]:
    return {
        "success": False,
        "operation": operation,
        "task_id": task_id,
        "error_type": type(error).__name__,
        "error": str(error),
        **extra,
    }


class TasksManager(TasksBase):
    _instance: TasksManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> TasksManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Tasks) -> None:
        pass

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_task(self, task_id: str) -> dict[str, Any]:
        """Return the full task dict, or a structured error."""
        try:
            task = await self.load_by_id(task_id)
            return _ok(task)
        except Exception as e:
            return _err("get_task", task_id, e)

    async def get_task_as_xml(
        self, task_id: str, template: str = DEFAULT_XML_TEMPLATE
    ) -> dict[str, Any]:
        """Return the task rendered as LLM-friendly XML."""
        try:
            task = await self.load_by_id(task_id)
            return {"success": True, "xml": self._to_llm_xml(task, template=template)}
        except Exception as e:
            return _err("get_task_as_xml", task_id, e)

    def _to_llm_xml(self, task: Tasks, template: str = DEFAULT_XML_TEMPLATE) -> str:
        tmpl = _XML_TEMPLATES.get(template, XML_TEMPLATE_FULL)
        raw_description = getattr(task, "description", "") or ""
        description = textwrap.indent(raw_description.strip(), "    ")
        return tmpl.format(
            id=task.id,
            title=task.title,
            status=task.status,
            priority=getattr(task, "priority", "") or "",
            due_date=getattr(task, "due_date", "") or "",
            project_id=getattr(task, "project_id", "") or "",
            assignee_id=getattr(task, "assignee_id", "") or "",
            description=description,
        )

    async def list_tasks_for_project(self, project_id: str) -> dict[str, Any]:
        """
        Return a compact list of all tasks in a project — just id, title,
        status, and priority.  Use this first to orient before fetching
        individual tasks in full.
        """
        try:
            tasks = await self._get_items(order_by="-created_at", project_id=project_id)
            summary = [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "status": t.status,
                    "priority": getattr(t, "priority", None),
                }
                for t in tasks
                if t
            ]
            return {"success": True, "project_id": project_id, "tasks": summary}
        except Exception as e:
            return {
                "success": False,
                "operation": "list_tasks_for_project",
                "project_id": project_id,
                "error": str(e),
            }

    async def list_tasks_for_user(self, user_id: str) -> dict[str, Any]:
        """
        Return a compact list of all tasks owned by a user —
        id, title, status, priority, and project_id.
        """
        try:
            tasks = await self._get_items(order_by="-created_at", user_id=user_id)
            summary = [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "status": t.status,
                    "priority": getattr(t, "priority", None),
                    "project_id": str(t.project_id) if getattr(t, "project_id", None) else None,
                    "due_date": str(t.due_date) if getattr(t, "due_date", None) else None,
                }
                for t in tasks
                if t
            ]
            return {"success": True, "user_id": user_id, "tasks": summary}
        except Exception as e:
            return {
                "success": False,
                "operation": "list_tasks_for_user",
                "user_id": user_id,
                "error": str(e),
            }

    async def list_subtasks(self, parent_task_id: str) -> dict[str, Any]:
        """Return a compact list of all direct subtasks of a given task."""
        try:
            tasks = await self._get_items(order_by="-created_at", parent_task_id=parent_task_id)
            summary = [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "status": t.status,
                    "priority": getattr(t, "priority", None),
                }
                for t in tasks
                if t
            ]
            return {"success": True, "parent_task_id": parent_task_id, "subtasks": summary}
        except Exception as e:
            return {
                "success": False,
                "operation": "list_subtasks",
                "parent_task_id": parent_task_id,
                "error": str(e),
            }

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: str = "",
        project_id: str | None = None,
        parent_task_id: str | None = None,
        status: TaskStatus = "incomplete",
        priority: TaskPriority | None = None,
        due_date: str | None = None,
        assignee_id: str | None = None,
        is_public: bool = False,
    ) -> dict[str, Any]:
        """
        Create a new task.  Explicit parameters only — immutable fields
        like id and created_at are never accepted.
        """
        try:
            payload: dict[str, Any] = {
                "user_id": user_id,
                "title": title,
                "status": status,
                "is_public": is_public,
            }
            if description:
                payload["description"] = description
            if project_id:
                payload["project_id"] = project_id
            if parent_task_id:
                payload["parent_task_id"] = parent_task_id
            if priority:
                payload["priority"] = priority
            if due_date:
                payload["due_date"] = due_date
            if assignee_id:
                payload["assignee_id"] = assignee_id

            task = await self.create_item(**payload)
            return _ok(task)
        except Exception as e:
            return {"success": False, "operation": "create_task", "error": str(e)}

    # ------------------------------------------------------------------
    # Update — one flexible method, immutable fields stripped automatically
    # ------------------------------------------------------------------

    async def update_task(self, task_id: str, **updates: Any) -> dict[str, Any]:
        """
        Update any combination of mutable fields on a task.

        Immutable fields (id, user_id, created_at, updated_at, dto) are
        silently stripped.  Unknown fields are stripped and reported so the
        caller knows what was ignored.

        Mutable fields: title, description, status, priority, due_date,
        project_id, parent_task_id, assignee_id, organization_id,
        settings, is_public.
        """
        safe = {k: v for k, v in updates.items() if k in _MUTABLE_FIELDS}
        stripped_immutable = [k for k in updates if k in _IMMUTABLE_FIELDS]
        unknown = [k for k in updates if k not in _MUTABLE_FIELDS and k not in _IMMUTABLE_FIELDS]

        if not safe:
            return {
                "success": False,
                "operation": "update_task",
                "task_id": task_id,
                "error": "No mutable fields provided.",
                "stripped_immutable": stripped_immutable,
                "unknown_fields": unknown,
            }

        try:
            task = await self.update_item(task_id, **safe)
            result = _ok(task)
            if stripped_immutable:
                result["warning_stripped_immutable"] = stripped_immutable
            if unknown:
                result["warning_unknown_fields"] = unknown
            return result
        except Exception as e:
            return _err(
                "update_task",
                task_id,
                e,
                stripped_immutable=stripped_immutable,
                unknown_fields=unknown,
            )

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    async def delete_task(self, task_id: str) -> dict[str, Any]:
        """
        Permanently delete a task.  Note: deleting a parent task cascades
        to all subtasks per the DB constraint.
        """
        try:
            success = await self.delete_item(task_id)
            return {"success": success, "task_id": task_id}
        except Exception as e:
            return _err("delete_task", task_id, e)


tasks_manager_instance = TasksManager()
