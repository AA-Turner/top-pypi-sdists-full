"""The NamedAgent funnel applies a binding's consumption map — the rule ``hold_code_call`` applies.

Until 2026-09-28 ``run_mandated`` applied no consumption map: a binding carrying
one on a ``research.*`` / ``ner.*`` / podcast-runner mandate was ignored at run
time, so a value declared for mapping (``mapped_offer``) could never reach a
Holder. These tests drive the REAL ``NamedAgent.run`` to the edge of the
provider call and capture exactly what the Holder receives:

* default pin (no map): with or without the mapping-only extras, the Holder's
  variables and turn are byte-identical to the pre-change flow;
* an extra that would reach the Holder by name refuses in words;
* a bound map: the host pipeline's output is what the Holder runs on, and the
  class's call-site renames are not applied a second time;
* a map with no host pipeline refuses (never silently ignored).

Planted proof: with ``kwargs["consumed_variables"] = consumed`` removed from
``run_mandated``, ``test_bound_map_output_is_what_the_holder_runs_on`` goes red.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel

import matrx_ai.agents.named as named
from matrx_ai import mandates
from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.agents.named import NamedAgent
from matrx_ai.agents.variables import AgentVariable


class _Holder:
    def __init__(self, names: tuple[str, ...]) -> None:
        self.variable_defaults = {n: AgentVariable(name=n) for n in names}
        self.bound: dict[str, Any] = {}
        self.auto_tools_disabled = None
        self.request_metadata: dict[str, Any] = {}

    def set_variables(self, **variables: Any) -> _Holder:
        self.bound.update(variables)
        return self


class _Source:
    agent_id = "00000000-0000-4000-8000-0000000000aa"
    is_version = False

    def __init__(self, holder: _Holder) -> None:
        self._holder = holder

    async def load(self) -> _Holder:
        return self._holder


class _Out(BaseModel):
    answer: str = ""


class _ResearchLike(NamedAgent):
    """A renaming NamedAgent, like the research / ner runners."""

    name = "Funnel Probe"
    mandate_key = "tests.named_funnel_probe"
    variable_map: ClassVar[dict[str, str]] = {"topic": "research_topic"}

    class Inputs(BaseModel):
        topic: str
        question: str = ""

    Output = _Out


SPECS = (
    mandates.OfferedValueSpec(name="topic", kind="text", guaranteed=True),
    mandates.OfferedValueSpec(name="question", kind="text", guaranteed=False),
    mandates.OfferedValueSpec(name="topic_name", kind="text", guaranteed=False, pass_by_name=False),
    mandates.OfferedValueSpec(name="source_count", kind="integer", guaranteed=False, pass_by_name=False),
)
INPUTS = {"topic": "Hard drive shredding", "question": "What does NAID require?"}
EXTRAS = {"topic_name": "Data destruction", "source_count": 4}


def _install(
    monkeypatch: pytest.MonkeyPatch,
    *,
    consumption_map: dict[str, Any] | None = None,
    materialize: Any = None,
) -> tuple[_Holder, dict[str, Any]]:
    holder = _Holder(("research_topic", "question", "topic_name", "source_count", "title"))
    resolution = mandates.MandateResolution(
        source=_Source(holder),
        provision_key="tests.named_funnel_probe",
        offered_values=SPECS,
        consumption_map=consumption_map,
        materialize=materialize,
    )

    async def _resolver(_key: str) -> mandates.MandateResolution:
        return resolution

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    sent: dict[str, Any] = {}

    async def _run_agent(agent: Any, **kwargs: Any) -> AgentRunResult:
        sent["user_input"] = kwargs.get("user_input")
        return AgentRunResult(success=True, output="ok")

    monkeypatch.setattr(named, "run_agent", _run_agent)
    monkeypatch.setattr(
        "matrx_ai.agents.source_tracking.resolve_child_source",
        lambda **kw: ("tests", "named-funnel-probe"),
    )
    return holder, sent


def _payload(holder: _Holder, sent: dict[str, Any]) -> str:
    return json.dumps({"variables": holder.bound, "sent": sent}, sort_keys=True, default=str)


@pytest.mark.asyncio
async def test_default_pin_payload_identical_with_mapping_only_extras(monkeypatch) -> None:
    holder, sent = _install(monkeypatch)
    await mandates.run_mandated(_ResearchLike, inputs=INPUTS, user_input="Go.")
    before = _payload(holder, sent)

    holder, sent = _install(monkeypatch)
    await mandates.run_mandated(_ResearchLike, inputs=INPUTS, user_input="Go.", offered=EXTRAS)
    after = _payload(holder, sent)

    assert after == before
    assert holder.bound == {
        "research_topic": "Hard drive shredding",
        "question": "What does NAID require?",
    }


@pytest.mark.asyncio
async def test_by_name_extra_refuses_in_words(monkeypatch) -> None:
    _install(monkeypatch)
    with pytest.raises(ValueError, match="mapped_offer"):
        await mandates.run_mandated(
            _ResearchLike, inputs=INPUTS, offered={"undeclared_fact": "x"}
        )


@pytest.mark.asyncio
async def test_bound_map_output_is_what_the_holder_runs_on(monkeypatch) -> None:
    seen: dict[str, Any] = {}

    async def _materialize(supplied: dict[str, Any]) -> dict[str, Any]:
        seen.update(supplied)
        # What the host pipeline answers for {"title": topic_name, "research_topic": topic}.
        return {"title": supplied["topic_name"], "research_topic": supplied["topic"]}

    holder, _ = _install(
        monkeypatch,
        consumption_map={
            "title": {"mapType": "offered_value", "target": "topic_name"},
            "research_topic": {"mapType": "offered_value", "target": "topic"},
        },
        materialize=_materialize,
    )
    await mandates.run_mandated(_ResearchLike, inputs=INPUTS, offered=EXTRAS)

    # The pipeline saw the WHOLE offer in call-site names (plus the extras) …
    assert seen["topic"] == "Hard drive shredding"
    assert seen["topic_name"] == "Data destruction"
    assert seen["source_count"] == 4
    # … and the Holder runs on exactly its output — no class rename re-applied.
    assert holder.bound == {"title": "Data destruction", "research_topic": "Hard drive shredding"}


@pytest.mark.asyncio
async def test_map_without_host_pipeline_refuses(monkeypatch) -> None:
    _install(
        monkeypatch,
        consumption_map={"title": {"mapType": "offered_value", "target": "topic_name"}},
        materialize=None,
    )
    with pytest.raises(mandates.MandateResolutionUnavailable):
        await mandates.run_mandated(_ResearchLike, inputs=INPUTS, offered=EXTRAS)
