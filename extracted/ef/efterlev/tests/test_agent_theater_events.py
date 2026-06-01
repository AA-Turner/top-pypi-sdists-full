"""Tests for the Phase-1 agent-theater event layer.

Covers: the gap agent emitting AgentStarted/BatchStarted/KsiClassified/
AgentFinished onto an active bus (additively — nothing without a bus) and
the keyless scripted-demo generator.
"""

from __future__ import annotations

from efterlev.events import (
    AgentFinished,
    AgentStarted,
    EventBus,
    KsiClassified,
    active_event_bus,
)
from efterlev.studio.demo import demo_events

# --- scripted demo -----------------------------------------------------


def test_demo_events_shape() -> None:
    cats = {f"KSI-X-{i:02d}": ("scanner" if i % 2 else "procedural") for i in range(60)}
    events = demo_events(cats)
    assert events[0].kind == "agent_started"
    assert events[-1].kind == "agent_finished"
    classified = [e for e in events if e.kind == "ksi_classified"]
    assert len(classified) == 60  # one verdict per KSI
    # every verdict is a valid status
    valid = {
        "implemented",
        "partial",
        "not_implemented",
        "not_applicable",
        "evidence_layer_inapplicable",
    }
    assert all(e.status in valid for e in classified)  # type: ignore[attr-defined]
    # deterministic
    assert [e.kind for e in demo_events(cats)] == [e.kind for e in events]


def test_demo_finished_counts_sum_to_total() -> None:
    cats = {f"KSI-X-{i:02d}": "scanner" for i in range(20)}
    events = demo_events(cats)
    finished = events[-1]
    assert isinstance(finished, AgentFinished)
    assert sum(finished.counts.values()) == 20


# --- gap agent emits onto the bus -------------------------------------


def test_gap_agent_emits_agent_theater_events() -> None:
    """A real gap run (fake LLM client) on a bound bus emits the lifecycle
    stream — AgentStarted, KsiClassified per verdict, AgentFinished —
    additively (the run is otherwise unchanged)."""
    import hashlib
    import json
    from dataclasses import dataclass, field
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from efterlev.agents.gap import GapAgent, GapAgentInput
    from efterlev.events import AgentFinished
    from efterlev.llm.base import LLMMessage, LLMResponse
    from efterlev.models import Indicator
    from efterlev.provenance import ProvenanceStore, active_store

    response = json.dumps(
        {
            "reasoning_summary": "Surveyed.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-SVC-SNT",
                    "status": "evidence_layer_inapplicable",
                    "rationale": "no detector evidence",
                    "evidence_ids": [],
                }
            ],
            "unmapped_findings": [],
        }
    )

    @dataclass
    class _Stub:
        model: str = "stub-haiku"
        last_messages: list[LLMMessage] = field(default_factory=list)

        def complete(self, *, system, messages, model, max_tokens=4096, on_chunk=None):  # type: ignore[no-untyped-def]
            joined = system + "".join(m.content for m in messages)
            return LLMResponse(
                text=response,
                model=self.model,
                prompt_hash=hashlib.sha256(joined.encode()).hexdigest(),
            )

    bus = EventBus()
    events: list[object] = []
    bus.subscribe(events.append)

    indicators = [Indicator(id="KSI-SVC-SNT", theme="SVC", name="x", statement="s", controls=[])]
    with (
        TemporaryDirectory() as tmp,
        ProvenanceStore(Path(tmp)) as store,
        active_store(store),
        active_event_bus(bus),
    ):
        agent = GapAgent(client=_Stub(), model="stub-haiku")  # type: ignore[arg-type]
        agent.run(GapAgentInput(indicators=indicators, evidence=[]))

    kinds = [e.kind for e in events]  # type: ignore[attr-defined]
    assert kinds[0] == "agent_started"
    assert kinds[-1] == "agent_finished"
    started = next(e for e in events if isinstance(e, AgentStarted))
    assert started.total_ksis == 1
    classified = [e for e in events if isinstance(e, KsiClassified)]
    assert len(classified) == 1
    assert classified[0].ksi == "KSI-SVC-SNT"
    assert classified[0].status == "evidence_layer_inapplicable"
    finished = next(e for e in events if isinstance(e, AgentFinished))
    assert finished.counts.get("evidence_layer_inapplicable") == 1
