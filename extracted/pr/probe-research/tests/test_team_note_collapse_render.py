"""The block renders the COLLAPSED note; the file keeps its verbatim bytes.

A struck claim (`> **SUPERSEDED** ...`) must stop costing every session's
context the moment it is struck — but the note FILE is what edits round-trip
against, so only the rendered block may fold, never the source. These tests
pin both halves, plus the health file the session-start audit trigger reads.

Same isolation contract as test_team_note_render.py: CLAUDE_CONFIG_DIR,
CODEX_HOME and XDG_STATE_HOME all point into tmp_path; the real ~/.claude and
~/.codex are live files on a shared box.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import pytest

from probe.cli import agent_rules, team_note_file


@dataclass
class _Settings:
    base_url: str = "https://example.invalid"
    token: str = "probe_pat_test"


@pytest.fixture
def harnesses(tmp_path, monkeypatch):
    claude = tmp_path / "claude"
    codex = tmp_path / "codex"
    claude.mkdir()
    codex.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    monkeypatch.setenv("CODEX_HOME", str(codex))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    files = claude / "CLAUDE.md", codex / "AGENTS.md"
    # Opted in: the note renders only beside the pointer block.
    for path in files:
        agent_rules.install(path)
    return files


_STRUCK = """## decisions

> **SUPERSEDED** 2026-08-21 · metric definition was wrong
> ~~SFT improved BIRD EX by 12.5 points over baseline.~~

The corrected number is a regression.

- still true"""


def test_struck_claim_leaves_the_block_but_marker_survives(harnesses) -> None:
    claude_md, _ = harnesses
    report = team_note_file.render_blocks(_STRUCK, settings=_Settings())

    assert report.ok, report.failures
    text = claude_md.read_text(encoding="utf-8")
    assert "**SUPERSEDED** 2026-08-21" in text  # that a claim fell is context
    assert "12.5 points" not in text  # the claim itself is gone
    assert "corrected number" in text
    assert "still true" in text


def test_markerless_note_renders_verbatim(harnesses) -> None:
    """The regression guard: for every note without a marker — all of them,
    the day this ships — collapse must be a byte-for-byte no-op."""
    claude_md, _ = harnesses
    body = "## rules\n\n- one\n- two"
    team_note_file.render_blocks(body, settings=_Settings())
    assert body in claude_md.read_text(encoding="utf-8")


def test_collapsed_render_is_stable_across_syncs(harnesses) -> None:
    """The current-check hashes the collapsed body; instability here would
    rewrite both instruction files on every Stop of every session forever."""
    settings = _Settings()
    team_note_file.render_blocks(_STRUCK, settings=settings)
    second = team_note_file.render_blocks(_STRUCK, settings=settings)
    assert set(second.unchanged) == {"claude_code", "codex"}
    assert not second.written


def test_striking_a_claim_is_a_content_change(harnesses) -> None:
    claude_md, _ = harnesses
    settings = _Settings()
    plain = "## decisions\n\nSFT improved BIRD EX by 12.5 points over baseline."
    team_note_file.render_blocks(plain, settings=settings)
    assert "12.5 points" in claude_md.read_text(encoding="utf-8")

    report = team_note_file.render_blocks(_STRUCK, settings=settings)
    assert set(report.written) == {"claude_code", "codex"}
    assert "12.5 points" not in claude_md.read_text(encoding="utf-8")


def test_render_records_health_for_the_audit_trigger(harnesses) -> None:
    team_note_file.render_blocks("## rules\n\n- one", settings=_Settings())

    payload = json.loads(team_note_file.note_health_path().read_text(encoding="utf-8"))
    sources = payload["sources"]
    assert set(sources) == {"claude_code", "codex"}
    for entry in sources.values():
        assert entry["degraded"] is False
        assert 0 < entry["pct"] < 0.8  # a tiny note must not trip the size trigger
        assert entry["block_bytes"] <= entry["available_bytes"]


def test_health_reflects_a_degraded_render(harnesses, tmp_path) -> None:
    claude_md, agents_md = harnesses
    rules = claude_md.read_text(encoding="utf-8")
    filler = rules + "x" * (team_note_file.INSTRUCTION_FILE_MAX_BYTES - 2_000 - len(rules.encode("utf-8")))
    claude_md.write_text(filler, encoding="utf-8")
    agents_md.write_text(filler, encoding="utf-8")

    report = team_note_file.render_blocks(
        "## rules\n\n" + "content line\n" * 300, settings=_Settings()
    )
    payload = json.loads(team_note_file.note_health_path().read_text(encoding="utf-8"))
    assert set(report.pointer_only) == {"claude_code", "codex"}, report
    for source in report.pointer_only:
        entry = payload["sources"][source]
        assert entry["degraded"] is True
        assert entry["pct"] >= 0.8  # a degraded machine must wake the trigger
