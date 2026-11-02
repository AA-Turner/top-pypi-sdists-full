"""Tests for render_document in record_discovery_baseline."""

from __future__ import annotations

import datetime as dt

from tests.scripts.record_discovery_baseline import baseline


def _units():
    return [
        baseline.Unit("agent", "agdt.set", ".github/agents/agdt.set.agent.md"),
        baseline.Unit("prompt", "/agdt.set", ".github/prompts/agdt.set.prompt.md"),
        baseline.Unit("skill", "run-checks", ".agents/skills/run-checks/SKILL.md"),
    ]


def test_preamble_states_the_date_and_the_regeneration_command():
    """The preamble records when the snapshot was taken and how to redo it."""
    document = baseline.render_document(_units(), dt.date(2026, 8, 16))
    assert "**Generated:** 2026-08-16" in document
    assert f"**Regenerate with:** `{baseline.REGENERATION_COMMAND}`" in document
    assert "snapshot, not a specification" in document


def test_counts_table_reports_per_surface_and_total_counts():
    """Each surface count and the total are rendered from the unit list."""
    document = baseline.render_document(_units(), dt.date(2026, 8, 16))
    assert "| prompt | 1 |" in document
    assert "| agent | 1 |" in document
    assert "| skill | 1 |" in document
    assert "| **total** | **3** |" in document


def test_document_ends_with_a_footnotes_section():
    """The footnote section exists so client discrepancies can be recorded."""
    document = baseline.render_document([], dt.date(2026, 8, 16))
    assert "## Footnotes" in document
    assert document.endswith("- None recorded.\n")


def test_custom_footnotes_body_is_rendered_verbatim():
    """A caller-supplied footnotes body replaces the default placeholder."""
    note = "- /agdt.foo — not offered by VS Code Copilot Chat."
    document = baseline.render_document([], dt.date(2026, 8, 16), footnotes_body=note)
    assert note in document
    assert "None recorded" not in document
