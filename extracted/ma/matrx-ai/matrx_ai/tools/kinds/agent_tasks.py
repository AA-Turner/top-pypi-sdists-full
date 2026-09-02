"""Kind for the ``tasks`` tool — the agent's per-conversation tasklist
(KIND_TOOL_LEDGER, ``lead-w2f``). Implementation:
``aidream/tools/agent_tasks_tool.py`` (server-executed writes to
``chat.agent_task``).

WHY NOT ``task_list`` / ``task_item``
-------------------------------------
The registered ``task_list`` family is the CONTENT checklist shape —
``{title, checked, children, item_type}`` items with no ids and a boolean
``checked``. The ``tasks`` tool returns DB rows — ``{id, title, status, note}``
with a five-state status enum and no nesting — plus the action receipt around
them. Binding it to ``task_list`` would declare keys it never emits and drop
the keys it does (the trace batch's finding: claim-time guesses are candidates,
never conclusions).

PLACEHOLDER tier: one union across the eight actions; every branch returns
``ok`` + ``action`` + the full post-action ``tasks`` snapshot, with the
``add``/``remove``/``clear_completed`` receipts optional.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind


class AgentTask(KindSubModel):
    """One ``chat.agent_task`` row as the tool reports it. Not registered —
    tool-local repeated structure."""

    id: str = ""
    title: str = ""
    #: pending | in_progress | done | blocked | skipped
    status: str = "pending"
    note: str | None = None


@kind(
    "agent_task_list",
    label="Agent Task List",
    family="agent_tasks",
    example={
        "ok": True,
        "action": "add",
        "tasks": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Draft the intro", "status": "pending", "note": None}],
        "created": [{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Draft the intro", "status": "pending"}],
    },
    maturity="placeholder",
)
class AgentTaskList(KindModel):
    ok: bool = True
    action: str | None = None
    #: The FULL tasklist after the action, in position order.
    tasks: list[AgentTask] = []
    #: ``add`` receipt — just the rows this call created.
    created: list[dict] | None = None
    #: ``remove`` / ``clear_completed`` receipt — the deleted ids.
    removed: list[str] | None = None
    #: Structured-failure branch only (success=False payloads share the shape).
    message: str | None = None


__all__ = ["AgentTask", "AgentTaskList"]
