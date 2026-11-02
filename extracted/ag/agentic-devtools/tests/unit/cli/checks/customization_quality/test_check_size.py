"""Tests for the Q5 size-budget rule."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import (
    AGENT_BODY_MAX_CHARS,
    ALWAYS_LOADED_MAX_BYTES,
    SKILL_BODY_MAX_WORDS,
    check_size,
)
from tests.unit.cli.checks.customization_quality._support import make_unit


class TestCheckSize:
    def test_accepts_units_inside_their_budget(self) -> None:
        """A small skill body is within the 5,000-word cap."""
        assert check_size(make_unit(body="word " * 10)) == []

    def test_flags_an_always_loaded_file_over_the_byte_cap(self) -> None:
        """An always-loaded instruction file is capped at 32 KiB."""
        unit = make_unit(
            path=".github/instructions/a.instructions.md",
            listing=".github/instructions",
            kind="always_loaded",
            body="x",
            size_bytes=ALWAYS_LOADED_MAX_BYTES + 1,
        )

        violations = check_size(unit)

        assert [v.rule for v in violations] == ["Q5"]
        assert "always-loaded" in violations[0].message

    def test_accepts_an_always_loaded_file_at_the_byte_cap(self) -> None:
        """The cap itself is allowed; only exceeding it fails."""
        unit = make_unit(
            path=".github/instructions/a.instructions.md",
            listing=".github/instructions",
            kind="always_loaded",
            body="x",
            size_bytes=ALWAYS_LOADED_MAX_BYTES,
        )

        assert check_size(unit) == []

    def test_flags_an_agent_body_over_the_char_cap(self) -> None:
        """A custom-agent body is capped at 30,000 characters."""
        unit = make_unit(path=".agents/skills/demo/demo.agent.md", kind="agent", body="x" * (AGENT_BODY_MAX_CHARS + 1))

        assert any("agent body" in v.message for v in check_size(unit))

    def test_accepts_an_agent_body_at_the_char_cap(self) -> None:
        """A body exactly at the cap passes."""
        unit = make_unit(path=".agents/skills/demo/demo.agent.md", kind="agent", body="x" * AGENT_BODY_MAX_CHARS)

        assert check_size(unit) == []

    def test_flags_a_skill_body_over_the_word_cap(self) -> None:
        """A skill body is capped at 5,000 words."""
        unit = make_unit(body="word " * (SKILL_BODY_MAX_WORDS + 1))

        assert any("skill body" in v.message for v in check_size(unit))

    def test_ignores_kinds_without_a_published_cap(self) -> None:
        """Scoped instruction files and documents carry no size rule."""
        unit = make_unit(
            path=".github/instructions/a.instructions.md",
            listing=".github/instructions",
            kind="scoped",
            body="word " * (SKILL_BODY_MAX_WORDS + 1),
            size_bytes=ALWAYS_LOADED_MAX_BYTES * 2,
        )

        assert check_size(unit) == []
