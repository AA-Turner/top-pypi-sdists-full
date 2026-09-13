"""THE WORKFLOW STEP HOLDER, proven — ``matrx_ai.graph_nodes.mandates.hold_step``.

What is being proven: an authored AI step RESOLVES ``workflow.step_intelligence``
on every run through the one mandate door, RUNS ON ITS AUTHOR'S OWN CONFIG AND
SCREAMS when nothing holds it (D20/D21/D23 — never a refusal), lets the author's
own values win over the Holder, lets the winning binding's overrides win over
the Holder's definition, fills only fields the step type carries, and stamps the
resolved Holder onto the request metadata under the key the runtime gate reads.

Why it is a forcing test: every assertion runs the real ``hold_step`` against
the real resolver seam (``matrx_ai.mandates._MANDATE_RESOLVER``), with only the
host's resolver replaced by a fixture — the same replacement the host does at
startup. Planting the bug — resolving nothing and returning the step as-is —
turns every test but the first red.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import mandates as mandates_mod
from matrx_ai.agents.named import AgentSource
from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    hold_step,
)
from matrx_ai.mandates import MandateResolution
from matrx_ai.orchestrator.mandate_carrier import (
    MANDATE_HOLDER_METADATA_KEY,
    MANDATE_HOLDER_UNBOUND_KIND,
    MANDATE_UNHELD_METADATA_KEY,
    reset_reported_signatures,
)


class _HolderConfig:
    """The slice of a UnifiedConfig the merge reads."""

    model = "holder-model"
    system_instruction = "HOLDER RULES"
    temperature = 0.9
    max_tokens = 4096


class _Holder:
    name = "Workflow Step Intelligence"
    config = _HolderConfig()


class _Source(AgentSource):
    agent_id: str = "holder-agent-id"
    is_version: bool = False
    fail: bool = False

    async def load(self) -> Any:
        if self.fail:
            raise RuntimeError("the agent table is unreachable")
        return _Holder()


def _install(resolution: MandateResolution | Exception | None, monkeypatch) -> list[str]:
    asked: list[str] = []

    async def _resolver(mandate_key: str) -> MandateResolution:
        asked.append(mandate_key)
        if isinstance(resolution, Exception):
            raise resolution
        assert resolution is not None
        return resolution

    monkeypatch.setattr(mandates_mod, "_MANDATE_RESOLVER", None if resolution is None else _resolver)
    return asked


STEP = {
    "model": "author-model",
    "messages": [{"role": "user", "content": "hi"}],
    "system_instruction": None,
    "temperature": None,
}


@pytest.fixture(autouse=True)
def _fresh_scream_dedupe():
    """The scream is one row per code path PER PROCESS — reset between tests."""
    reset_reported_signatures()
    yield
    reset_reported_signatures()


@pytest.mark.asyncio
async def test_unbound_mandate_runs_the_authors_step_and_screams(monkeypatch) -> None:
    """THE REGRESSION OF 2026-09-12. No resolver installed = no Holder at any
    rung, which is this mandate's DECLARED state (seedless on purpose, D21).
    The step runs on the config its author chose, and the missing Holder is
    screamed — it is NEVER a refusal. Refusing here took every authored ai.*
    step on production down (run fbe577d6…, definition 129a4ec1…)."""
    _install(None, monkeypatch)

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["model"] == "author-model", "the author's own model ran"
    assert held.config["messages"] == STEP["messages"]
    assert held.config["system_instruction"] is None, "nothing was invented for it"
    assert held.filled_by_holder == ()
    assert MANDATE_HOLDER_METADATA_KEY not in held.metadata, "nothing held it, so no Holder stamp"
    unheld = held.metadata[MANDATE_UNHELD_METADATA_KEY]
    assert unheld["reason"] == MANDATE_HOLDER_UNBOUND_KIND
    assert unheld["mandate_key"] == WORKFLOW_STEP_INTELLIGENCE_MANDATE
    assert unheld["consumer"] == "ai.llm.chat"
    assert unheld["model"] == "author-model"
    assert WORKFLOW_STEP_INTELLIGENCE_MANDATE in unheld["remedy"]


@pytest.mark.asyncio
async def test_unbound_mandate_files_one_system_error_row(monkeypatch) -> None:
    """The scream reaches the platform's own error door, once per code path."""
    rows: list[dict[str, Any]] = []

    def _record_error(error, **fields):
        rows.append({"error": str(error), **fields})
        return None

    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "record_error", _record_error)
    _install(None, monkeypatch)

    await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")
    await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert len(rows) == 1, "one row per code path per process, not one per step"
    row = rows[0]
    assert row["kind"] == MANDATE_HOLDER_UNBOUND_KIND
    assert row["source_app"] == "mandate-scan"
    assert row["payload"]["mandate_key"] == WORKFLOW_STEP_INTELLIGENCE_MANDATE
    assert "NO HOLDER" in row["error"]


@pytest.mark.asyncio
async def test_resolver_failure_runs_and_screams(monkeypatch) -> None:
    _install(RuntimeError("no Holder at any rung"), monkeypatch)

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["model"] == "author-model"
    assert "no Holder at any rung" in held.metadata[MANDATE_UNHELD_METADATA_KEY]["detail"]


@pytest.mark.asyncio
async def test_step_resolves_the_mandate_and_stamps_the_holder(monkeypatch) -> None:
    asked = _install(MandateResolution(source=_Source()), monkeypatch)

    held = await hold_step(
        dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat", metadata={"run": "r1"}
    )

    assert asked == [WORKFLOW_STEP_INTELLIGENCE_MANDATE], "resolved through the one door"
    stamp = held.metadata[MANDATE_HOLDER_METADATA_KEY]
    assert stamp["mandate_key"] == WORKFLOW_STEP_INTELLIGENCE_MANDATE
    assert stamp["agent_id"] == "holder-agent-id"
    assert stamp["holder_type"] == "agent"
    assert stamp["name"] == "Workflow Step Intelligence"
    assert held.metadata["spec_type"] == "ai.llm"
    assert held.metadata["run"] == "r1", "the caller's own metadata survives"


@pytest.mark.asyncio
async def test_author_wins_holder_fills_only_the_unset(monkeypatch) -> None:
    """THE PINS LAW in action: the author's model stays; the Holder is the floor."""
    _install(MandateResolution(source=_Source()), monkeypatch)

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["model"] == "author-model"
    assert held.config["messages"] == STEP["messages"]
    assert held.config["system_instruction"] == "HOLDER RULES"
    assert held.config["temperature"] == 0.9
    assert held.filled_by_holder == ("system_instruction", "temperature")
    assert held.metadata[MANDATE_HOLDER_METADATA_KEY]["filled"] == [
        "system_instruction",
        "temperature",
    ]


@pytest.mark.asyncio
async def test_binding_overrides_win_over_the_holder_definition(monkeypatch) -> None:
    """agent definition → binding overrides → (pins) → run scope; later wins."""
    _install(
        MandateResolution(source=_Source(), config_overrides={"temperature": 0.2}),
        monkeypatch,
    )

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["temperature"] == 0.2, "the binding's digital layer beats the definition"
    assert held.config["system_instruction"] == "HOLDER RULES", "and the definition fills the rest"


@pytest.mark.asyncio
async def test_a_step_type_without_the_field_never_gains_it(monkeypatch) -> None:
    """An image step has no system instruction; the Holder must not invent one."""
    _install(MandateResolution(source=_Source()), monkeypatch)
    image_step = {"model": "img-model", "messages": [{"role": "user", "content": "a cat"}]}

    held = await hold_step(dict(image_step), spec_type="ai.image", consumer="ai.image")

    assert held.config == image_step
    assert held.filled_by_holder == ()
    assert "filled" not in held.metadata[MANDATE_HOLDER_METADATA_KEY]


@pytest.mark.asyncio
async def test_a_workflow_holder_runs_and_screams_with_the_reason(monkeypatch) -> None:
    _install(
        MandateResolution(source=None, holder_type="workflow", workflow_id="wf-1"),
        monkeypatch,
    )

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["model"] == "author-model"
    assert "AGENT Holder" in held.metadata[MANDATE_UNHELD_METADATA_KEY]["detail"]


@pytest.mark.asyncio
async def test_a_holder_that_cannot_load_runs_and_screams(monkeypatch) -> None:
    _install(MandateResolution(source=_Source(fail=True)), monkeypatch)

    held = await hold_step(dict(STEP), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["model"] == "author-model"
    assert "could not be loaded" in held.metadata[MANDATE_UNHELD_METADATA_KEY]["detail"]
