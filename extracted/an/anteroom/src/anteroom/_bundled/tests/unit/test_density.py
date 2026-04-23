"""Tests for cli.density pure helpers (#1367).

These tests exercise ``ToolResultDensity`` / ``densify_output`` / ``collapse_diff_hunks``
— pure functions with no I/O, no mocks. Cover all four density modes across
realistic shapes (short output, long output, multiline, dict, empty, error).
"""

from __future__ import annotations

import pytest

from anteroom.cli.density import (
    ToolResultDensity,
    collapse_diff_hunks,
    densify_output,
    parse_density,
)


class TestToolResultDensityEnum:
    def test_enum_members(self) -> None:
        assert ToolResultDensity.MINIMAL.value == "minimal"
        assert ToolResultDensity.COMPACT.value == "compact"
        assert ToolResultDensity.NORMAL.value == "normal"
        assert ToolResultDensity.DETAILED.value == "detailed"

    def test_parse_density_accepts_canonical_names(self) -> None:
        for name in ("minimal", "compact", "normal", "detailed"):
            parsed = parse_density(name)
            assert parsed.value == name

    def test_parse_density_case_insensitive(self) -> None:
        assert parse_density("Compact") == ToolResultDensity.COMPACT
        assert parse_density("NORMAL") == ToolResultDensity.NORMAL

    def test_parse_density_unknown_returns_normal(self) -> None:
        # Unknown density strings fall back to NORMAL so mis-typed values
        # never break rendering.
        assert parse_density("bogus") == ToolResultDensity.NORMAL
        assert parse_density("") == ToolResultDensity.NORMAL


class TestDensifyOutputNormal:
    def test_normal_returns_output_unchanged(self) -> None:
        # ``normal`` is the byte-identical-default contract: the helper must
        # return the original payload untouched.
        payload = "line1\nline2\nline3"
        out = densify_output(
            payload,
            ToolResultDensity.NORMAL,
            head_lines=3,
            tail_lines=2,
        )
        assert out == payload

    def test_normal_empty_is_empty(self) -> None:
        assert densify_output("", ToolResultDensity.NORMAL, head_lines=3, tail_lines=2) == ""

    def test_normal_does_not_add_any_marker(self) -> None:
        big = "\n".join(f"line-{i}" for i in range(50))
        out = densify_output(big, ToolResultDensity.NORMAL, head_lines=3, tail_lines=2)
        assert out == big
        assert "[+" not in out


class TestDensifyOutputMinimal:
    def test_minimal_returns_empty_body(self) -> None:
        # Minimal hides the body entirely.
        assert (
            densify_output(
                "some long output",
                ToolResultDensity.MINIMAL,
                head_lines=3,
                tail_lines=2,
            )
            == ""
        )

    def test_minimal_with_empty_input(self) -> None:
        assert densify_output("", ToolResultDensity.MINIMAL, head_lines=3, tail_lines=2) == ""


class TestDensifyOutputCompact:
    def test_compact_short_output_returned_verbatim(self) -> None:
        payload = "one\ntwo"
        # head+tail=5 covers 2 lines with slack — return whole payload, no hint.
        out = densify_output(payload, ToolResultDensity.COMPACT, head_lines=3, tail_lines=2)
        assert out == payload
        assert "[+" not in out

    def test_compact_long_output_head_tail_and_hint(self) -> None:
        lines = [f"line-{i}" for i in range(20)]
        payload = "\n".join(lines)
        out = densify_output(payload, ToolResultDensity.COMPACT, head_lines=3, tail_lines=2)
        # Keeps first 3 + last 2 lines, collapses middle with a "[+N lines]" hint.
        kept = out.split("\n")
        assert kept[0] == "line-0"
        assert kept[1] == "line-1"
        assert kept[2] == "line-2"
        assert kept[-2] == "line-18"
        assert kept[-1] == "line-19"
        assert any("[+" in part and "lines]" in part for part in kept)

    def test_compact_exactly_head_plus_tail_no_collapse(self) -> None:
        payload = "\n".join(f"l{i}" for i in range(5))  # head=3 tail=2 -> exactly 5
        out = densify_output(payload, ToolResultDensity.COMPACT, head_lines=3, tail_lines=2)
        assert out == payload
        assert "[+" not in out

    def test_compact_single_line(self) -> None:
        out = densify_output("single", ToolResultDensity.COMPACT, head_lines=3, tail_lines=2)
        assert out == "single"

    def test_compact_zero_head_and_tail_shows_hint_only(self) -> None:
        lines = "\n".join(f"line-{i}" for i in range(5))
        out = densify_output(lines, ToolResultDensity.COMPACT, head_lines=0, tail_lines=0)
        assert "[+5 lines]" in out
        # No original lines retained.
        for i in range(5):
            assert f"line-{i}" not in out


class TestDensifyOutputDetailed:
    def test_detailed_expands_up_to_cap(self) -> None:
        # Detailed returns the whole payload (up to an internal safety cap).
        lines = "\n".join(f"line-{i}" for i in range(8))
        out = densify_output(lines, ToolResultDensity.DETAILED, head_lines=3, tail_lines=2)
        # Detailed keeps all 8 lines.
        for i in range(8):
            assert f"line-{i}" in out

    def test_detailed_caps_absurdly_long_output(self) -> None:
        # Detailed honours an internal safety cap so a 10_000-line dump
        # doesn't flood the terminal.
        lines = "\n".join(f"l{i}" for i in range(10_000))
        out = densify_output(lines, ToolResultDensity.DETAILED, head_lines=3, tail_lines=2)
        assert out.count("\n") < 10_000  # cap enforced
        assert "truncated" in out or "[+" in out


class TestCollapseDiffHunksNormal:
    def test_normal_passes_hunks_through(self) -> None:
        hunk = [(" ", "a"), (" ", "b"), ("+", "c"), (" ", "d"), (" ", "e")]
        out = collapse_diff_hunks(hunk, context_lines=3, density=ToolResultDensity.NORMAL)
        # Normal: no collapsing, returns the same list contents.
        assert list(out) == hunk


class TestCollapseDiffHunksCompact:
    def test_compact_collapses_long_context_run(self) -> None:
        # 10 unchanged context lines surrounding one add.
        hunk = [(" ", f"c{i}") for i in range(5)] + [("+", "new")] + [(" ", f"c{i}") for i in range(5, 10)]
        out = collapse_diff_hunks(hunk, context_lines=1, density=ToolResultDensity.COMPACT)
        # Each side of the change should be truncated to 1 context line plus
        # a sentinel marker row.
        kinds = [tag for tag, _ in out]
        # Marker rows use a special tag value "~".
        assert "~" in kinds
        # Net: fewer lines than the original.
        assert len(out) < len(hunk)

    def test_compact_short_run_no_collapse(self) -> None:
        hunk = [(" ", "a"), ("+", "new"), (" ", "b")]
        out = collapse_diff_hunks(hunk, context_lines=3, density=ToolResultDensity.COMPACT)
        assert list(out) == hunk

    def test_compact_preserves_change_lines(self) -> None:
        hunk = (
            [(" ", f"c{i}") for i in range(10)]
            + [("+", "added")]
            + [("-", "removed")]
            + [(" ", f"c{i}") for i in range(10, 20)]
        )
        out = collapse_diff_hunks(hunk, context_lines=2, density=ToolResultDensity.COMPACT)
        tags = [t for t, _ in out]
        # Change lines survive
        assert "+" in tags
        assert "-" in tags


class TestCollapseDiffHunksMinimal:
    def test_minimal_returns_only_change_lines(self) -> None:
        hunk = [(" ", "c0"), ("+", "added"), (" ", "c1"), ("-", "removed"), (" ", "c2")]
        out = collapse_diff_hunks(hunk, context_lines=3, density=ToolResultDensity.MINIMAL)
        tags = [t for t, _ in out]
        # No unchanged lines survive in minimal mode.
        assert " " not in tags


class TestCollapseDiffHunksDetailed:
    def test_detailed_passes_hunks_through(self) -> None:
        hunk = [(" ", "a"), (" ", "b"), ("+", "c"), (" ", "d"), (" ", "e")]
        out = collapse_diff_hunks(hunk, context_lines=3, density=ToolResultDensity.DETAILED)
        assert list(out) == hunk


class TestDensifyOutputEdgeCases:
    @pytest.mark.parametrize(
        "density",
        [ToolResultDensity.MINIMAL, ToolResultDensity.COMPACT, ToolResultDensity.NORMAL, ToolResultDensity.DETAILED],
    )
    def test_all_modes_accept_empty(self, density: ToolResultDensity) -> None:
        assert densify_output("", density, head_lines=3, tail_lines=2) == ""

    @pytest.mark.parametrize(
        "density",
        [ToolResultDensity.MINIMAL, ToolResultDensity.COMPACT, ToolResultDensity.NORMAL, ToolResultDensity.DETAILED],
    )
    def test_all_modes_return_str(self, density: ToolResultDensity) -> None:
        out = densify_output("hello\nworld", density, head_lines=3, tail_lines=2)
        assert isinstance(out, str)
