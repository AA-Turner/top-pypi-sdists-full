"""Kinds for the workbench-surface tool results: ``task`` · ``skill`` ·
``picklist`` (KIND_TOOL_LEDGER, ``lead-w2f``). All three are package-hosted
action dispatchers with NO active ``tool.binding`` row (the census's
no-binding set), so their runtime half is proven by direct calls of the real
implementations, the ``sql`` precedent.

WHY ``task`` DOES NOT REUSE ``agent_task_list`` OR ``task_list``: this tool
works ``workbench`` project tasks (priority, due_date, project/parent/assignee
ids) — not the per-conversation agent tasklist (``agent_task_list``) and not
the content checklist (``task_list``). Three genuinely different shapes.

All placeholder tier. Union rule: every key any success branch can emit is
declared, action-specific keys optional.
"""

from __future__ import annotations

from pydantic import Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "task_tool_result",
    label="Task Tool Result",
    family="workbench",
    example={"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Ship the report", "status": "open", "priority": "high"},
    # PLACEHOLDER — the get/list/create/update/delete union over workbench tasks.
    maturity="placeholder",
)
class TaskToolResult(KindModel):
    #: `get` (full record) / `create` / `update` — the single-task branches
    #: keep their flat live shape.
    id: str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: str | None = None
    project_id: str | None = None
    parent_task_id: str | None = None
    assignee_id: str | None = None
    is_public: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    #: `update` — immutable fields the manager ignored.
    warning: str | None = None
    #: `list` — compact rows + the self-cap state.
    tasks: list[dict] | None = None
    count: int | None = None
    shown: int | None = None
    truncated: bool | None = None
    note: str | None = None
    #: `delete` receipt.
    deleted: bool | None = None
    task_id: str | None = None


@kind(
    "skill_tool_result",
    label="Skill Tool Result",
    family="skills",
    example={
        "category": "writing",
        "count": 1,
        "hints": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "label": "Blog post"}],
    },
    # PLACEHOLDER — the list/get(full|page)/search union over the skills system.
    maturity="placeholder",
)
class SkillToolResult(KindModel):
    #: category overview (list with no category).
    categories: list[dict] | None = None
    total_active: int | None = None
    hint: str | None = None
    #: `list` / `search` — hint rows.
    category: str | None = None
    query: str | None = None
    count: int | None = None
    hints: list[dict] | None = None
    #: `get` — the skill body header…
    id: str | None = None
    skill_id: str | None = None
    label: str | None = None
    description: str | None = None
    skill_type: str | None = None
    category_path: JsonValue | None = None
    version: int | None = None
    allowed_tools: list[str] | None = None
    disable_auto_invocation: bool | None = None
    trigger_patterns: JsonValue | None = None
    #: …plus the full-or-paged body.
    mode: str | None = None
    body: str | None = None
    total_chars: int | None = None
    offset: int | None = None
    chars_returned: int | None = None
    has_more: bool | None = None
    next_offset: int | None = None


@kind(
    "picklist_tool_result",
    label="Picklist Tool Result",
    family="picklists",
    example={"list_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "list_name": "Industries", "item_count": 12, "already_existed": False, "message": "List 'Industries' created with 12 items."},
    # PLACEHOLDER — the list/get/create/update_item/batch_update union.
    maturity="placeholder",
)
class PicklistToolResult(KindModel):
    #: `create` receipt.
    list_id: str | None = None
    list_name: str | None = None
    item_count: int | None = None
    already_existed: bool | None = None
    message: str | None = None
    #: `list` page.
    lists: JsonValue | None = None
    page: int | None = None
    page_size: int | None = None
    count: int | None = None
    #: `get` — the list row + its items. The wire key is "list"; the Python
    #: name is aliased because a field literally named `list` shadows the
    #: builtin during annotation evaluation (KindModel populates by name AND
    #: serializes by alias, so the payload key stays "list").
    list_: JsonValue | None = Field(default=None, alias="list")
    items: list[JsonValue] | None = None
    is_grouped: bool | None = None
    #: `update_item` / `batch_update` receipts.
    item_id: str | None = None
    success_count: int | None = None
    failed_count: int | None = None
    failed_items: list[JsonValue] | None = None


__all__ = ["TaskToolResult", "SkillToolResult", "PicklistToolResult"]
