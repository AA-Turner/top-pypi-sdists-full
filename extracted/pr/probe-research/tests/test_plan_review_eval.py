"""`evals/triggering/plan_review.py` scores its own judge replies, and its
numbers are quoted in `agent_rules.PLAN_REVIEW_OFF_PARAGRAPHS` and the eval
README. An eval that silently mis-scores produces a figure people quote, so the
scoring and the case file are held here offline (no key, no network)."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

EVAL_DIR = Path(__file__).resolve().parents[1] / "evals" / "triggering"


@pytest.fixture(scope="module")
def plan_review():
    sys.path.insert(0, str(EVAL_DIR))
    try:
        yield importlib.import_module("plan_review")
    finally:
        sys.path.remove(str(EVAL_DIR))


class _Reply:
    def __init__(self, text: str):
        self._text = text

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"content": [{"type": "text", "text": self._text}]}


class _Client:
    def __init__(self, text: str):
        self.text = text

    def post(self, *args, **kwargs) -> _Reply:
        return _Reply(self.text)


@pytest.mark.parametrize(
    ("reply", "ran"),
    [
        ('{"first_actions": ["Read"], "skill": "probe-research:plan-research-review"}', True),
        ('{"first_actions": ["Read"], "skill": "plan_research_review"}', True),
        ('{"first_actions": ["Read"], "skill": "plan research review"}', True),
        ('{"first_actions": ["Read", "Grep"], "skill": "track-work"}', False),
        ('{"first_actions": ["probe ask", "plan-research-review"], "skill": null}', False),
        ('{"first_actions": [], "skill": null}', False),
    ],
)
def test_the_judge_reply_is_scored_by_what_it_reached_for(plan_review, monkeypatch, reply, ran):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    assert plan_review._call(_Client(reply), "m", "s", "u")["plan_review"] is ran


def test_a_reply_without_first_actions_is_an_error_not_a_quiet_no(plan_review, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    with pytest.raises(ValueError):
        plan_review._call(_Client('{"skill": "plan-research-review"}'), "m", "s", "u")


def test_the_cases_split_evenly_with_unique_ids():
    cases = json.loads((EVAL_DIR / "plan_review_cases.json").read_text())["cases"]
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))
    assert sum(c["expect_review"] for c in cases) == sum(not c["expect_review"] for c in cases) == 8


def test_each_arm_lists_the_skills_its_profile_ships(plan_review):
    agent = plan_review.PROFILE_SKILLS[plan_review.agent_rules.Profile.AGENT]
    daemon = plan_review.PROFILE_SKILLS[plan_review.agent_rules.Profile.DAEMON]
    assert "track-work" in agent and "track-work" not in daemon
    assert "plan-research-review" in agent and "plan-research-review" in daemon


def test_every_arm_reads_a_skill_file_that_ships(plan_review):
    """Each arm lists its profile's skills from the files that ship: the lean
    plugin's moved to `agent-skills/` (2026-10-12), and a stale folder made
    every daemon arm exit before its first judge call."""
    for profile, names in plan_review.PROFILE_SKILLS.items():
        for name in names:
            assert plan_review._description(profile, name), (profile, name)
