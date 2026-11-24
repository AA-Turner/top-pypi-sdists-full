"""No job buys a restricted model: a top-tier call is the person's own access, whatever mandate runs.

Arman, 2026-11-02: "Make sure that Fable and all Max models are fully blocked on the admin account ...
that's how they ran up a two thousand dollar bill in two weeks." A same-day change let the agent-building
mandates run top-tier models for anyone (admin@admin.com built on claude-fable-5-1); it was removed.

Fails when: a call running under any mandate (an agent builder included) is admitted for a person without
top-tier access, or the gate grows a second, job-keyed way in.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.providers import model_tier_gate as gate

TOP = SimpleNamespace(model_cost_rating=6, model_name="top-model", model_id="m1")


@pytest.fixture(autouse=True)
def _no_access():
    before = gate._resolver
    gate.set_top_tier_access_resolver(lambda user_id: False)
    yield
    gate._resolver = before


@pytest.mark.parametrize("mandate_key", ["agent_factory.structure_builder", "any.other.job", None])
def test_a_restricted_model_is_refused_whatever_job_runs(mandate_key: str | None) -> None:
    ctx = SimpleNamespace(user_id="u1", metadata={"mandate_key": mandate_key} if mandate_key else {})
    assert gate.refusal_for(TOP, ctx) is not None


def test_the_gate_has_one_door_the_persons_access() -> None:
    setters = sorted(n for n in dir(gate) if n.startswith("set_") and callable(getattr(gate, n)))
    assert setters == ["set_top_tier_access_resolver"]


def test_a_person_with_access_still_runs_it() -> None:
    gate.set_top_tier_access_resolver(lambda user_id: True)
    assert gate.refusal_for(TOP, SimpleNamespace(user_id="u1", metadata={})) is None
