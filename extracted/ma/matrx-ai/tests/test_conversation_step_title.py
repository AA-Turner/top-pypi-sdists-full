from dataclasses import dataclass, field
from typing import Any

from matrx_connect.context.provenance import (
    ORIGIN_CLASS_CLIENT_AUTO,
    ORIGIN_CLASS_HUMAN,
)

from matrx_ai.db.conversation_gate import (
    CONVERSATION_STEP_LABEL_KEY,
    _format_auto_title,
    _resolve_initial_conversation_title,
    compact_step_label,
    resolve_step_label_for_title,
)


@dataclass
class _Ctx:
    source_feature: str = ""
    origin_class: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def test_format_auto_title_uses_compact_prefix() -> None:
    assert _format_auto_title("Podcast Image 1") == "Auto: Podcast Image 1"
    assert _format_auto_title("AUTO: Generate Podcast Image 1") == "Auto: Podcast Image 1"


def test_compact_step_label_drops_generate() -> None:
    assert compact_step_label("Generate Podcast Video 2") == "Podcast Video 2"
    assert compact_step_label("AUTO: Produce Podcast Audio") == "Podcast Audio"


def test_resolve_step_label_prefers_human_label() -> None:
    assert resolve_step_label_for_title("Podcast Image 1") == "Podcast Image 1"


def test_resolve_step_label_uses_agent_display_name_for_slug() -> None:
    assert (
        resolve_step_label_for_title("create_script", "Educational Podcast Script")
        == "Educational Podcast Script"
    )


def test_resolve_initial_title_uses_step_label_before_source_feature() -> None:
    ctx = _Ctx(
        source_feature="podcasts",
        metadata={CONVERSATION_STEP_LABEL_KEY: "Podcast Script"},
    )
    assert _resolve_initial_conversation_title(title=None, ctx=ctx) == "Auto: Podcast Script"


def test_human_conversation_never_gets_auto_placeholder() -> None:
    ctx = _Ctx(source_feature="chat", origin_class=ORIGIN_CLASS_HUMAN)

    assert _resolve_initial_conversation_title(title=None, ctx=ctx) == "New conversation"


def test_client_automation_keeps_auto_placeholder() -> None:
    ctx = _Ctx(source_feature="chat", origin_class=ORIGIN_CLASS_CLIENT_AUTO)

    assert _resolve_initial_conversation_title(title=None, ctx=ctx) == "Auto: New conversation"
