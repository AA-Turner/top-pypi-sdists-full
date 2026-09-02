from __future__ import annotations

from matrx_ai.tools.implementations.web import _cap_research_section


def test_research_section_cap_bounds_output_with_recovery_hint() -> None:
    out, truncated = _cap_research_section("x" * 80_000, limit=10_000, label="final_result")

    assert truncated is True
    assert len(out) < 11_000
    assert "final_result" in out
    assert "web" in out


def test_research_section_cap_leaves_small_output_untouched() -> None:
    out, truncated = _cap_research_section("small", limit=10_000, label="final_result")

    assert out == "small"
    assert truncated is False
