"""Unit tests for the recent-actions block injected into the L2 continuation
message.

Pure unit tests — no LLM calls, no agent wiring. Synthetic ``Message`` objects
exercise ``_build_recent_actions_block`` and the head/tail preview helper.
"""

from __future__ import annotations

import json

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co
from xml.etree import ElementTree as ET

from xpander_sdk.core.context_optimizer.context_optimizer import (
    RECENT_ACTIONS_ARGS_HEAD,
    RECENT_ACTIONS_ARGS_TAIL,
    RECENT_ACTIONS_RESULT_HEAD,
    RECENT_ACTIONS_RESULT_TAIL,
    _build_recent_actions_block,
    _head_tail_preview,
    _looks_like_error_payload,
    _redact_sensitive_payload,
    _redact_sensitive_text,
    _strip_illegal_xml_chars,
    _xml_attr_escape,
)

# --------------------------------------------------------------------- #
#  Fake Message — duck-types the agno.Message attrs the helper reads.
# --------------------------------------------------------------------- #


class _Msg:
    def __init__(
        self,
        role,
        content="",
        tool_name=None,
        tool_call_id=None,
        tool_args=None,
        tool_calls=None,
        tool_call_error=None,
        created_at="",
    ):
        self.role = role
        self.content = content
        self.tool_name = tool_name
        self.tool_call_id = tool_call_id
        self.tool_args = tool_args
        self.tool_calls = tool_calls
        self.tool_call_error = tool_call_error
        self.created_at = created_at


def _assistant_with_tool_call(call_id, name, arguments_obj):
    return _Msg(
        role="assistant",
        tool_calls=[
            {
                "id": call_id,
                "function": {
                    "name": name,
                    "arguments": json.dumps(arguments_obj),
                },
            }
        ],
    )


def _tool_msg(name, call_id, content, **kw):
    return _Msg(
        role="tool",
        tool_name=name,
        tool_call_id=call_id,
        content=content,
        **kw,
    )


# --------------------------------------------------------------------- #
#  _head_tail_preview
# --------------------------------------------------------------------- #


def test_head_tail_short_passthrough():
    text = "abcde"
    assert _head_tail_preview(text, head=10, tail=10) == "abcde"


def test_head_tail_elides_middle_with_marker():
    text = "A" * 100 + "B" * 100 + "C" * 100  # 300 chars
    out = _head_tail_preview(text, head=50, tail=50)
    assert out.startswith("A" * 50)
    assert out.endswith("C" * 50)
    assert "[…200 chars summarized…]" in out


def test_head_tail_empty():
    assert _head_tail_preview("", 10, 10) == ""


# --------------------------------------------------------------------- #
#  _looks_like_error_payload
# --------------------------------------------------------------------- #


def test_error_heuristic_detects_error_prefix():
    assert _looks_like_error_payload("error(500): boom")
    assert _looks_like_error_payload('{"detail":"error(500): bad"}')
    assert _looks_like_error_payload("Internal Server Error happened")


def test_error_heuristic_passes_normal_payload():
    assert not _looks_like_error_payload('{"stdout":"ok","exit_code":0}')
    assert not _looks_like_error_payload("")


# --------------------------------------------------------------------- #
#  _build_recent_actions_block
# --------------------------------------------------------------------- #


def test_basic_5_of_7_chronological():
    msgs = []
    for i in range(7):
        msgs.append(_assistant_with_tool_call(f"id{i}", f"tool_{i}", {"x": i}))
        msgs.append(_tool_msg(f"tool_{i}", f"id{i}", f"result_{i}"))

    block = _build_recent_actions_block(msgs)

    # Should contain the last 5 (tool_2..tool_6), NOT tool_0 / tool_1.
    assert "tool_0" not in block
    assert "tool_1" not in block
    for i in range(2, 7):
        assert f"tool_{i}" in block
    # Chronological ordering — index="1" appears before index="5".
    assert block.index('index="1"') < block.index('index="5"')


def test_includes_all_tool_names_no_skipping():
    msgs = [
        _assistant_with_tool_call("a", "think", {}),
        _tool_msg("think", "a", "reasoning..."),
        _assistant_with_tool_call("b", "analyze", {}),
        _tool_msg("analyze", "b", "analysis..."),
        _assistant_with_tool_call("c", "xpcompact_context", {}),
        _tool_msg("xpcompact_context", "c", "compacted"),
        _assistant_with_tool_call("d", "xpworkspace-bash", {"cmd": "ls"}),
        _tool_msg("xpworkspace-bash", "d", '{"stdout":"file","exit_code":0}'),
    ]
    block = _build_recent_actions_block(msgs)
    for name in ("think", "analyze", "xpcompact_context", "xpworkspace-bash"):
        assert name in block


def test_pairs_args_from_assistant_tool_calls():
    msgs = [
        _assistant_with_tool_call("abc", "file_read", {"path": "/x"}),
        _tool_msg("file_read", "abc", "file contents"),
    ]
    block = _build_recent_actions_block(msgs)
    assert '"path": "/x"' in block or '"path":"/x"' in block


def test_args_head_tail_preview_applied():
    long_args = {"data": "Z" * 5000}
    msgs = [
        _assistant_with_tool_call("k", "big_args", long_args),
        _tool_msg("big_args", "k", "ok"),
    ]
    block = _build_recent_actions_block(msgs)
    # The marker means the args were elided, not just truncated.
    assert "chars summarized" in block


def test_result_head_tail_preview_applied():
    big_result = "R" * 5000
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", big_result),
    ]
    block = _build_recent_actions_block(msgs)
    assert "chars summarized" in block
    # Head and tail still present.
    assert "R" * RECENT_ACTIONS_RESULT_HEAD in block
    assert "R" * RECENT_ACTIONS_RESULT_TAIL in block


def test_short_payload_no_marker():
    msgs = [
        _assistant_with_tool_call("k", "fetch", {"q": "hi"}),
        _tool_msg("fetch", "k", "small result"),
    ]
    block = _build_recent_actions_block(msgs)
    assert "chars summarized" not in block
    assert "small result" in block


def test_empty_messages_returns_empty_string():
    assert _build_recent_actions_block([]) == ""


def test_no_tool_messages_returns_empty_string():
    msgs = [
        _Msg(role="system", content="sys"),
        _Msg(role="user", content="hi"),
        _Msg(role="assistant", content="hello"),
    ]
    assert _build_recent_actions_block(msgs) == ""


def test_missing_tool_call_id_renders_empty_args():
    # No assistant message preceding — no way to recover args.
    msgs = [_tool_msg("orphan", None, "result text")]
    block = _build_recent_actions_block(msgs)
    assert "<args>{}</args>" in block
    assert "orphan" in block


def test_xml_escaping_of_dangerous_content():
    msgs = [
        _assistant_with_tool_call("k", "render", {"html": "<b>x</b>"}),
        _tool_msg("render", "k", "<script>alert(1)</script>"),
    ]
    block = _build_recent_actions_block(msgs)
    assert "<script>alert(1)</script>" not in block
    assert "&lt;script&gt;" in block


def test_feature_flag_disabled(monkeypatch):
    monkeypatch.setattr(co, "INCLUDE_RECENT_ACTIONS", False)
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", "x"),
    ]
    assert co._build_recent_actions_block(msgs) == ""


def test_status_error_from_tool_call_error_attr():
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", '{"ok":true}', tool_call_error=True),
    ]
    block = _build_recent_actions_block(msgs)
    assert 'status="error"' in block


def test_status_error_from_payload_heuristic():
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg(
            "fetch",
            "k",
            '{"detail":"error(500): Internal server error"}',
        ),
    ]
    block = _build_recent_actions_block(msgs)
    assert 'status="error"' in block


def test_status_ok_default():
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", '{"stdout":"hi","exit_code":0}'),
    ]
    block = _build_recent_actions_block(msgs)
    # Look only inside <action ...> tag — the block header includes the
    # literal words "ok" / "error" as documentation.
    action_line_start = block.index("<action ")
    action_line_end = block.index(">", action_line_start)
    action_open_tag = block[action_line_start : action_line_end + 1]
    assert 'status="ok"' in action_open_tag
    assert 'status="error"' not in action_open_tag


def test_args_short_passthrough_no_marker():
    """Args under head+tail budget should not be elided."""
    msgs = [
        _assistant_with_tool_call("k", "fetch", {"q": "small"}),
        _tool_msg("fetch", "k", "ok"),
    ]
    block = _build_recent_actions_block(msgs)
    assert "chars summarized" not in block
    assert RECENT_ACTIONS_ARGS_HEAD + RECENT_ACTIONS_ARGS_TAIL >= len(
        json.dumps({"q": "small"})
    )


def test_redact_sensitive_payload_masks_known_keys():
    obj = {
        "api_key": "sk-secret123",
        "Authorization": "Bearer abcdef0123456789",
        "nested": {"x_api_key": "xxx", "user": "alice"},
        "list": [{"password": "p"}, {"q": 1}],
        "ok": "value",
    }
    out = _redact_sensitive_payload(obj)
    assert out["api_key"] == "[REDACTED]"
    assert out["Authorization"] == "[REDACTED]"
    assert out["nested"]["x_api_key"] == "[REDACTED]"
    assert out["nested"]["user"] == "alice"
    assert out["list"][0]["password"] == "[REDACTED]"
    assert out["list"][1]["q"] == 1
    assert out["ok"] == "value"


def test_redact_sensitive_text_inline_patterns():
    samples = [
        "Authorization: Bearer abcdef0123456789",
        '{"api_key":"sk-1234567890"}',
        "X-API-Key=mysecretvalue",
        "Set-Cookie: session=abc123def456",
    ]
    for s in samples:
        out = _redact_sensitive_text(s)
        assert "[REDACTED]" in out
    # Untouched payloads stay intact.
    assert _redact_sensitive_text("hello world") == "hello world"


def test_recent_actions_block_redacts_args_and_results():
    secret = "sk-supersecretvalue123456"
    msgs = [
        _assistant_with_tool_call(
            "k",
            "fetch",
            {"api_key": secret, "url": "https://example.com"},
        ),
        _tool_msg(
            "fetch",
            "k",
            f'{{"detail":"ok","Authorization":"Bearer {secret}"}}',
        ),
    ]
    block = _build_recent_actions_block(msgs)
    assert secret not in block
    assert "[REDACTED]" in block
    # Non-sensitive value preserved.
    assert "https://example.com" in block


def test_strip_illegal_xml_chars_removes_control_bytes():
    raw = "ok\x00\x08\x0b\x0c\x1b[31m\x7f\x9fdone"
    out = _strip_illegal_xml_chars(raw)
    # All illegal control bytes stripped; printable + TAB/LF/CR preserved.
    assert "\x00" not in out
    assert "\x1b" not in out
    assert "\x7f" not in out
    assert out.startswith("ok")
    assert out.endswith("done")


def test_strip_illegal_xml_chars_keeps_tab_lf_cr():
    raw = "a\tb\nc\rd"
    assert _strip_illegal_xml_chars(raw) == raw


def test_xml_attr_escape_handles_quote():
    # Plain xml escape leaves `"` intact — would break attribute. The helper
    # must encode it as &quot; so the resulting attribute parses cleanly.
    raw = 'tool"name<>'
    escaped = _xml_attr_escape(raw)
    assert "&quot;" in escaped
    # Embed in attribute and parse — must be well-formed.
    ET.fromstring(f'<x attr="{escaped}"/>')


def test_xml_attr_escape_strips_illegal_chars():
    raw = "tool\x00name\x1b"
    escaped = _xml_attr_escape(raw)
    assert "\x00" not in escaped
    assert "\x1b" not in escaped


def test_recent_actions_block_quote_in_tool_name_keeps_attr_well_formed():
    """Tool name with `"` must be encoded as `&quot;` so the action's
    attribute open tag parses cleanly. The block intro contains literal
    prose like `<work_completed>` and is NOT a parseable XML document — only
    the dynamic <action ...> tag is checked here."""
    msgs = [
        _Msg(role="assistant", tool_calls=[]),
        _tool_msg('weird"tool', None, "ok"),
    ]
    block = _build_recent_actions_block(msgs)
    # Raw `"` inside attribute would have broken parsing; encoded form must
    # appear instead.
    assert 'tool="weird"tool"' not in block
    assert "weird&quot;tool" in block
    # Extract the <action ...> open tag and parse it standalone.
    import re

    match = re.search(r"<action [^>]*/>?|<action [^>]*>", block)
    assert match is not None
    open_tag = match.group(0)
    if not open_tag.endswith("/>"):
        open_tag = open_tag.rstrip(">") + "/>"
    ET.fromstring(open_tag)


def test_recent_actions_block_strips_illegal_control_chars():
    """Tool result containing ANSI escape / null byte (illegal XML 1.0
    control chars) must not appear verbatim in the rendered block — they'd
    make any downstream XML consumer fail."""
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", "red\x1b[31mtext\x00more"),
    ]
    block = _build_recent_actions_block(msgs)
    assert "\x1b" not in block
    assert "\x00" not in block
    # Visible characters survive.
    assert "redtext" in block.replace("[31m", "")


def test_recent_actions_block_escapes_close_tag_injection():
    """Tool result containing `</recent_actions>` must be escaped so a
    crafted payload cannot close the block early."""
    msgs = [
        _assistant_with_tool_call("k", "fetch", {}),
        _tool_msg("fetch", "k", "data </recent_actions> rest"),
    ]
    block = _build_recent_actions_block(msgs)
    # Must NOT contain a second literal closing tag inside the result.
    assert block.count("</recent_actions>") == 1
    assert "&lt;/recent_actions&gt;" in block


def test_args_within_1000_budget_passthrough():
    """Args up to 1000 chars (500 head + 500 tail) render verbatim."""
    payload = "Z" * 900
    msgs = [
        _assistant_with_tool_call("k", "big_args", {"data": payload}),
        _tool_msg("big_args", "k", "ok"),
    ]
    block = _build_recent_actions_block(msgs)
    assert "chars summarized" not in block
    assert payload in block
