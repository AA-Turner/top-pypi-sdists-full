"""Kind for the ``outlook`` agent tool (aidream ``services/outlook``): one union across draft,
list, read and calendar, always naming the channel that acted and why each earlier one was
skipped. ``sent`` is always false: the tool composes and reads; it never sends."""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "outlook_result",
    disposition="record",
    label="Outlook Result",
    family="outlook",
    example={
        "intent": "draft",
        "channel": "classic_outlook",
        "channel_label": "classic Outlook for Windows on your computer",
        "skipped": [
            {"channel": "graph", "reason": "drafting through Microsoft needs Mail.ReadWrite"},
            {"channel": "work_iq", "reason": "Work IQ is not wired into agent tools yet"},
        ],
        "handoffs": [],
        "sent": False,
        "draft": {"id": "AAMk", "folder": "Drafts", "sent": False},
    },
)
class OutlookResult(KindModel):
    intent: str = ""
    channel: str | None = None
    channel_label: str | None = None
    skipped: list[dict] = []
    handoffs: list[dict] = []
    sent: bool = False
    notices: list[str] | None = None
    draft: dict | None = None
    message: dict | None = None
    messages: list[dict] | None = None
    count: int | None = None
    folder: str | None = None
    account: str | None = None
    calendar: dict | None = None


OUTLOOK_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {"outlook": OutlookResult}

__all__ = ["OUTLOOK_TOOL_RESULT_KINDS", "OutlookResult"]
