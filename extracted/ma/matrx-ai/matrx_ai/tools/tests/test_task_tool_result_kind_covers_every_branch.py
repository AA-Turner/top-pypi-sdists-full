"""Every success branch of the `task` tool must fit TaskToolResult (additionalProperties:false).

Regression: create/update/delete returned version/previous_version/previous/archived, which the kind
lacked, so stamp_result_kind refused and the executor filed tool_result_kind_missing + drift every call.
"""

from __future__ import annotations

from matrx_ai.tools.kind_stamp import stamp_result_kind
from matrx_ai.tools.kinds.workbench import TaskToolResult
from matrx_ai.tools.models import ToolResult

_BRANCHES = {
    "create": {"id": "a", "title": "t", "status": "incomplete", "project_id": None, "organization_id": "o",
               "published_to_web": False, "shown_to": None, "created_at": "x", "version": 1, "previous_version": None},
    "update": {"id": "a", "title": "t", "status": "s", "priority": None, "updated_at": "x", "version": 3,
               "previous_version": 2, "previous": {"title": "old"}, "warning": "w"},
    "delete": {"deleted": True, "archived": True, "task_id": "a", "previous_version": 4},
    "list": {"tasks": [{"id": "a"}], "count": 1, "shown": 1, "truncated": True, "note": "n"},
}


def test_every_task_branch_is_stamped_with_its_kind() -> None:
    for name, payload in _BRANCHES.items():
        out = stamp_result_kind(ToolResult(success=True, output=dict(payload)), TaskToolResult).output
        assert out.get("__kind") == "task_tool_result", f"{name} branch refused by the kind"
