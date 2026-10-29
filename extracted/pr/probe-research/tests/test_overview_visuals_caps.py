"""The recorder's `overview-visuals` skill names the caps the server enforces.

`skills/overview-visuals/SKILL.md` is the recorder's copy of the lane's skill
(plan writer-owns-summary §3.8): read before `probe visuals set`, shipped in the
CLI wheel. The lane fills its copy's caps at serve time; this copy carries them
as plain numbers, written by `make sync-visuals-caps`
(scripts/sync_visuals_caps.py) from `app/blocks/schemas.py`. A cap the skill
states and the checker does not enforce refuses the writer's tables, so the two
must be equal. Read from the server's source when this is the monorepo (the
public agent mirror has no server).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
SCRIPT = AGENT / "scripts" / "sync_visuals_caps.py"
PROPOSED_LINES = (
    "description: Pick an experiment's tables and charts, or a project's tables; you name fields and runs, "
    "the server reads the numbers. Read before `probe visuals set`.",
    "Never type a number. Name what to show; the server reads the values. `probe visuals options --experiment E` "
    "writes the current list to a file (its `path`): edit it, then `probe visuals set --experiment E`.",
    "- Copy keys, paths and run ids verbatim from `probe visuals options`.",
    # Summary pages are custom artifacts (2026-10-28): results may show on the page too.
    "- An experiment's results tables and charts go here, in its Metrics center; its page may also show them "
    "its own way. A project's tables go here. `[]` only when there is nothing to show yet, or one number the "
    "page can say.",
)


def _script():
    spec = importlib.util.spec_from_file_location("_sync_visuals_caps", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_skill_names_the_servers_project_table_caps():
    script = _script()
    if not script.SCHEMAS.is_file():
        pytest.skip("no server source beside the agent")
    values = script.caps(script.SCHEMAS.read_text(encoding="utf-8"))
    skill = script.SKILL.read_text(encoding="utf-8")
    assert script.sentence(values) in skill, "run `make sync-visuals-caps`"
    assert script.render(skill, values) == skill
    assert script.main(["--check"]) == 0


def test_the_sync_rewrites_only_the_caps_sentence():
    script = _script()
    skill = script.SKILL.read_text(encoding="utf-8")
    other = {name: 1000 + i for i, name in enumerate(script.NAMES)}
    rendered = script.render(skill, other)
    assert script.sentence(other) in rendered
    assert rendered.replace(script.sentence(other), "") == script.PATTERN.sub("", skill)


def test_the_recorder_copy_differs_from_the_lanes_in_the_approved_lines_only():
    """The lines the plans change (§3.8; custom artifact pages), plus the lane's own front-matter
    flag and its placeholders: everything else is the lane's text."""
    lane = AGENT.parent / "app" / "generation" / "skills" / "overview-visuals" / "SKILL.md"
    if not lane.is_file():
        pytest.skip("no server source beside the agent")
    ours = (
        (AGENT / "skills" / "overview-visuals" / "SKILL.md")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    theirs = [
        line for line in lane.read_text(encoding="utf-8").splitlines() if line != "substitute: true"
    ]
    changed = [(a, b) for a, b in zip(ours, theirs) if a != b]
    assert len(ours) == len(theirs)
    assert [a for a, _ in changed if "$PROJECT_TABLES" not in _] == list(PROPOSED_LINES)
