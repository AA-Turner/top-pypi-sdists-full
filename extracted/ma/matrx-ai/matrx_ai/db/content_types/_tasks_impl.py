from __future__ import annotations

import textwrap
from typing import Any, Literal

from matrx_utils.row_access import ShownToLiteral, publish_columns

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
# workspace.tasks is a canonical entity: the owner is ``created_by``; the web lane is
# ``published_to_web`` and the list filter is ``shown_to``. ``user_id`` / ``is_public`` are
# the retired spellings — writing them makes the ORM refuse the whole call
# ("Unknown field(s) on Tasks"), which is how the `task` tool died on every action.
_IMMUTABLE_FIELDS = frozenset(
    {
        "id",
        "created_by",
        "updated_by",
        "organization_id",
        "created_at",
        "updated_at",
        "deleted_at",
        "version",
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
        "settings",
        "published_to_web",
        "published_to_web_at",
        "published_to_web_by",
        "shown_to",
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


def _not_visible(operation: str, task_id: str) -> dict[str, Any]:
    """The task does not exist FOR THIS CALLER — missing and hidden read the same.

    Under the caller's RLS session a row they may not see is simply absent, so
    the two cases are one honest answer that names the id and leaks nothing.
    """
    return {
        "success": False,
        "operation": operation,
        "task_id": task_id,
        "error_type": "not_found",
        "error": f"Task {task_id} was not found, or you do not have access to it.",
    }


def _no_write_access(operation: str, task_id: str, **extra: Any) -> dict[str, Any]:
    """The caller can see the task but the database refused the write."""
    return {
        "success": False,
        "operation": operation,
        "task_id": task_id,
        "error_type": "no_access",
        "error": f"You can view task {task_id} but you do not have permission to change it.",
        **extra,
    }


_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")


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
    # ACCESS IS NOT DECIDED HERE. Callers acting for a person run these
    # methods inside that person's RLS session
    # (``matrx_ai.tools.person_session.as_the_person``); Postgres RLS decides
    # what exists and what may change. Every by-id read is AUTHORITATIVE
    # (``use_cache=False``): the ORM's identity cache is shared across callers
    # and knows nothing about who is asking, so a cached row loaded for one
    # person must never answer for another.
    # ------------------------------------------------------------------

    async def _read_live(self, task_id: str) -> Tasks | None:
        return await self.load_item_or_none(use_cache=False, **self._pk_filter(task_id))

    async def _explain_refused_write(
        self,
        operation: str,
        task_id: str,
        version_before: Any,
        error: Exception,
        **extra: Any,
    ) -> dict[str, Any]:
        """Name why a write to a task the caller could SEE did not land.

        RLS refuses an UPDATE silently (0 rows) or, for a WITH CHECK breach,
        with 42501. Either way the task is still there, unchanged, for this
        caller — that is a permission refusal, not a conflict. The database
        made the decision; this only reports it.
        """
        text = str(error)
        if any(marker in text for marker in _RLS_REFUSAL_MARKERS):
            return _no_write_access(operation, task_id, **extra)
        try:
            now = await self._read_live(task_id)
        except Exception:
            return _err(operation, task_id, error, **extra)
        if now is None:
            return _not_visible(operation, task_id)
        if getattr(now, "version", None) == version_before:
            return _no_write_access(operation, task_id, **extra)
        return _err(operation, task_id, error, **extra)

    async def _write_visible(
        self, operation: str, task_id: str, updates: dict[str, Any], **extra: Any
    ) -> tuple[Tasks | None, dict[str, Any] | None]:
        """Read the task as the caller, then write to exactly that row.

        Returns ``(task, None)`` on success or ``(None, error_dict)``.
        """
        try:
            task = await self._read_live(task_id)
        except Exception as e:
            return None, _err(operation, task_id, e, **extra)
        if task is None:
            return None, _not_visible(operation, task_id)
        version_before = getattr(task, "version", None)
        try:
            async with self._governed_write():
                task = await self._update_item(task, **updates)
        except Exception as e:
            return None, await self._explain_refused_write(
                operation, task_id, version_before, e, **extra
            )
        return task, None

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_task(self, task_id: str) -> dict[str, Any]:
        """Return the full task dict, or a structured error.

        A task the caller may not see is ``error_type='not_found'`` naming the id.
        """
        try:
            task = await self._read_live(task_id)
        except Exception as e:
            return _err("get_task", task_id, e)
        if task is None:
            return _not_visible("get_task", task_id)
        return _ok(task)

    async def get_task_as_xml(
        self, task_id: str, template: str = DEFAULT_XML_TEMPLATE
    ) -> dict[str, Any]:
        """Return the task rendered as LLM-friendly XML."""
        try:
            task = await self._read_live(task_id)
        except Exception as e:
            return _err("get_task_as_xml", task_id, e)
        if task is None:
            return _not_visible("get_task_as_xml", task_id)
        return {"success": True, "xml": self._to_llm_xml(task, template=template)}

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
            tasks = await self._get_items(
                order_by="-created_at", project_id=project_id, deleted_at__isnull=True
            )
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

    async def list_tasks_for_user(
        self, user_id: str, organization_id: str | None = None
    ) -> dict[str, Any]:
        """
        Return a compact list of the live (not soft-deleted) tasks a person
        created — id, title, status, priority, project_id — across ALL their
        organizations.

        ``organization_id`` is an explicit optional filter (None = every
        organization); the selected organization never narrows a list
        (access-belongs-to-the-person, 2026-09-25).
        """
        filters: dict[str, Any] = {
            "created_by": user_id,
            "deleted_at__isnull": True,
        }
        if organization_id:
            filters["organization_id"] = organization_id
        try:
            tasks = await self._get_items(order_by="-created_at", **filters)
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
            return {
                "success": True,
                "user_id": user_id,
                "organization_id": organization_id or None,
                "tasks": summary,
            }
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
            tasks = await self._get_items(
                order_by="-created_at", parent_task_id=parent_task_id, deleted_at__isnull=True
            )
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
        *,
        organization_id: str,
        description: str = "",
        project_id: str | None = None,
        parent_task_id: str | None = None,
        status: TaskStatus = "incomplete",
        priority: TaskPriority | None = None,
        due_date: str | None = None,
        assignee_id: str | None = None,
        published_to_web: bool = False,
        shown_to: ShownToLiteral | None = None,
    ) -> dict[str, Any]:
        """
        Create a new task.  Explicit parameters only — immutable fields
        like id and created_at are never accepted.

        ``organization_id`` is required — workspace.tasks.organization_id is
        NOT NULL. Callers carry it from the verified request context
        (``ToolContext.organization_id``); never defaulted here.

        ``user_id`` is the person creating the task — written as ``created_by``.
        ``published_to_web`` is always written explicitly (never the table default);
        ``shown_to`` omitted leaves the type's list-filter knob in charge.
        """
        if not organization_id:
            return {
                "success": False,
                "operation": "create_task",
                "error": "organization_id is required to create a task.",
            }
        try:
            payload: dict[str, Any] = {
                "created_by": user_id,
                "organization_id": organization_id,
                "title": title,
                "status": status,
            }
            payload.update(publish_columns(published_to_web, user_id))
            if shown_to:
                payload["shown_to"] = shown_to
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

        Immutable fields (id, created_by, updated_by, organization_id,
        created_at, updated_at, deleted_at, version, dto) are stripped and
        reported.  Unknown fields are stripped and reported so the
        caller knows what was ignored.

        Mutable fields: title, description, status, priority, due_date,
        project_id, parent_task_id, assignee_id, settings, published_to_web
        (+ its ``_at`` / ``_by`` stamps), shown_to.
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

        task, error = await self._write_visible(
            "update_task",
            task_id,
            safe,
            stripped_immutable=stripped_immutable,
            unknown_fields=unknown,
        )
        if error is not None:
            return error
        result = _ok(task)
        if stripped_immutable:
            result["warning_stripped_immutable"] = stripped_immutable
        if unknown:
            result["warning_unknown_fields"] = unknown
        return result

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    async def delete_task(self, task_id: str) -> dict[str, Any]:
        """
        Soft-delete a task: stamp ``deleted_at`` (workspace.tasks is a
        soft-delete entity — the tasks screen archives the same way and every
        list here reads live rows only). The row stays recoverable.
        """
        from datetime import UTC, datetime

        _, error = await self._write_visible(
            "delete_task", task_id, dict(deleted_at=datetime.now(UTC))
        )
        if error is not None:
            return error
        return {"success": True, "task_id": task_id, "archived": True}


tasks_manager_instance = TasksManager()
