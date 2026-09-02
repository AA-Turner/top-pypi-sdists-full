"""Phase 0 — the self-management contract + cap_text primitive.

Pins the building blocks of the tool-result size gate:
  * cap_text trims exactly one field and reports the true size.
  * truncate_with_notice references the call_id + fetch path.
  * ToolResult carries the two declaration fields with safe defaults.
"""

from __future__ import annotations

from matrx_ai.tools.models import ToolResult
from matrx_ai.tools.output_caps import (
    TOOL_RESULT_ABSOLUTE_CEILING_CHARS,
    TOOL_RESULT_CANARY_CHARS,
    TOOL_RESULT_SOFT_CAP_CHARS,
    CapInfo,
    cap_text,
    truncate_with_notice,
)


def test_tier_constants_are_ordered() -> None:
    assert TOOL_RESULT_CANARY_CHARS < TOOL_RESULT_SOFT_CAP_CHARS
    assert TOOL_RESULT_SOFT_CAP_CHARS < TOOL_RESULT_ABSOLUTE_CEILING_CHARS


def test_cap_text_under_limit_is_untouched() -> None:
    text, info = cap_text("hello", limit=100)
    assert text == "hello"
    assert info == CapInfo(total_chars=5, shown_chars=5, truncated=False, limit=100)


def test_cap_text_over_limit_trims_and_reports_true_size() -> None:
    body = "x" * 1000
    text, info = cap_text(body, limit=300)
    assert len(text) == 300
    assert info.truncated is True
    assert info.total_chars == 1000  # the model is told what it's missing
    assert info.shown_chars == 300
    assert info.limit == 300


def test_cap_text_none_is_empty() -> None:
    text, info = cap_text(None, limit=50)
    assert text == ""
    assert info.truncated is False
    assert info.total_chars == 0


def test_cap_text_exact_limit_not_truncated() -> None:
    text, info = cap_text("abc", limit=3)
    assert text == "abc"
    assert info.truncated is False


def test_truncate_with_notice_keeps_head_and_points_at_fetch() -> None:
    body = "A" * 2000
    out = truncate_with_notice(
        body, limit=500, total_chars=2000, call_id="call-xyz", tool_name="data"
    )
    assert out.startswith("A" * 500)
    assert "fetch_tool_result" in out
    assert 'call_id="call-xyz"' in out
    assert "offset=500" in out
    assert "2,000 characters" in out  # true total surfaced
    assert "'data'" in out


def test_toolresult_defaults_are_safe() -> None:
    # The contract fields must default to "no special handling" so every existing
    # tool that never sets them keeps identical behavior.
    r = ToolResult(success=True, output={"ok": True})
    assert r.output_self_capped is False
    assert r.approved_max_chars is None


def test_toolresult_can_declare_self_management() -> None:
    r = ToolResult(
        success=True,
        output={"rows": []},
        output_self_capped=True,
        approved_max_chars=80_000,
    )
    assert r.output_self_capped is True
    assert r.approved_max_chars == 80_000
