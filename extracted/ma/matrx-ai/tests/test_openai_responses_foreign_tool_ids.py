from matrx_ai.config.openai_responses_tool_ids import (
    openai_responses_tool_call_wire_ids,
    openai_responses_tool_result_call_id,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent


def test_native_openai_call_preserved() -> None:
    fc_id, call_id = openai_responses_tool_call_wire_ids(
        "call_abc123",
        openai_item_id="fc_def456",
    )
    assert fc_id == "fc_def456"
    assert call_id == "call_abc123"


def test_anthropic_toolu_remapped() -> None:
    join = "toolu_018MNHxyJMF76E5ZuLjSJfe3"
    fc_id, call_id = openai_responses_tool_call_wire_ids(join)
    assert fc_id == "fc_018MNHxyJMF76E5ZuLjSJfe3"
    assert call_id == "call_018MNHxyJMF76E5ZuLjSJfe3"


def test_gemini_remapped() -> None:
    join = "gemini_a1b2c3d4e5f67890"
    fc_id, call_id = openai_responses_tool_call_wire_ids(join)
    assert fc_id == "fc_a1b2c3d4e5f67890"
    assert call_id == "call_a1b2c3d4e5f67890"


def test_call_only_join_key_without_metadata() -> None:
    fc_id, call_id = openai_responses_tool_call_wire_ids("call_xyz")
    assert fc_id == "fc_xyz"
    assert call_id == "call_xyz"


def test_tool_result_pairs_with_remapped_call() -> None:
    join = "toolu_018MNHxyJMF76E5ZuLjSJfe3"
    _, call_id = openai_responses_tool_call_wire_ids(join)
    assert openai_responses_tool_result_call_id(join) == call_id
    assert call_id == "call_018MNHxyJMF76E5ZuLjSJfe3"


def test_tool_call_content_to_openai_foreign() -> None:
    tc = ToolCallContent(
        id="toolu_018MNHxyJMF76E5ZuLjSJfe3",
        name="context_patch",
        arguments={"key": "working_document", "command": "overwrite"},
    )
    wire = tc.to_openai()
    assert wire["id"].startswith("fc_")
    assert wire["call_id"].startswith("call_")
    assert wire["id"] == "fc_018MNHxyJMF76E5ZuLjSJfe3"


def test_tool_result_content_uses_tool_use_id() -> None:
    tr = ToolResultContent(
        tool_use_id="toolu_018MNHxyJMF76E5ZuLjSJfe3",
        name="context_patch",
        content={"ok": True},
    )
    wire = tr.to_openai()
    assert wire["call_id"] == "call_018MNHxyJMF76E5ZuLjSJfe3"


def test_tool_call_content_native_openai_unchanged() -> None:
    tc = ToolCallContent(
        id="call_native123",
        name="sql",
        arguments={"query": "select 1"},
        metadata={"openai_item_id": "fc_native456"},
    )
    wire = tc.to_openai()
    assert wire["id"] == "fc_native456"
    assert wire["call_id"] == "call_native123"
