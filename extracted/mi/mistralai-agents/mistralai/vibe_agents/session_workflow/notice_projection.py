"""Pure projection of Harness notices onto the legacy Task Protocol."""

from typing import Literal

from mistralai.vibe_agents.session_workflow.task_protocol import (
    AlertStateContent,
    AlertStatePayload,
    ProgressStateContent,
    ProgressStatePayload,
)

type NoticeLevel = Literal["info", "success", "warning", "error"]
type NoticePayload = ProgressStatePayload | AlertStatePayload

_TOOL_DISCOVERY_PROGRESS_TITLE = "Searched for relevant tools"


def notice_to_legacy_task_protocol_payload(
    *,
    notice_kind: str | None,
    level: NoticeLevel,
    message: str,
) -> NoticePayload:
    """Map a Harness notice onto the public legacy Task Protocol contract."""
    if notice_kind == "tool_discovery":
        return ProgressStatePayload(
            content=ProgressStateContent(
                status="success",
                title=_TOOL_DISCOVERY_PROGRESS_TITLE,
                content="",
            )
        )
    return AlertStatePayload(
        content=AlertStateContent(
            variant=level,
            title=message,
            level="public",
        )
    )
