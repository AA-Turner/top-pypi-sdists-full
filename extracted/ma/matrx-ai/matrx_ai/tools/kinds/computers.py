"""Kind for the ``computers`` agent tool (aidream ``tools/computers_tool.py``): the person's Matrx 2
computers with their honest online state (``list``), and a Claude Code or Codex session started on
the one the agent chose (``start_coding``)."""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "computers_result",
    disposition="record",
    label="Computers Result",
    family="computers",
    example={
        "action": "list",
        "computers": [
            {
                "device_id": "6b0f0c1e-0000-4000-8000-000000000000",
                "name": "Arman's MacBook Pro",
                "platform": "darwin",
                "state": "online",
                "reason": None,
                "can_code": True,
                "last_seen": "2026-10-14T18:02:11Z",
            }
        ],
        "count": 1,
    },
)
class ComputersResult(KindModel):
    action: str = ""
    computers: list[dict] | None = None
    count: int | None = None
    device_id: str | None = None
    computer: str | None = None
    session_id: str | None = None
    run_id: str | None = None
    queued: bool | None = None
    provider: str | None = None
    folder: str | None = None
    link: str | None = None


COMPUTERS_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {"computers": ComputersResult}

__all__ = ["COMPUTERS_TOOL_RESULT_KINDS", "ComputersResult"]
