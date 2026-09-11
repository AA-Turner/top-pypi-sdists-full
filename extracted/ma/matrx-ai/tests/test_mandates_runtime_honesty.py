"""run_mandated — a mandated agent runs ONLY what the mandate resolves to.

SUT: ``matrx_ai.mandates.run_mandated``. Doubles replace only what it CALLS:
the host resolver (``_MANDATE_RESOLVER``), the host ``record_error`` seam, the
host completion callback, and the agent execution itself (``run`` — the LLM
call). The funnel's own work — refusal, source routing, override merge,
mapping/spill forwarding, holder-variable computation, completion hand-off —
runs for real.

Breaks these tests name:
* a missing/failed resolver silently runs the class's own source (seed fallback);
* a workflow-held mandate runs an agent record anyway;
* mandate overrides beat call-site overrides;
* the resolved variable_mapping / spill_variables never reach the run;
* the completion callback sees the caller's raw inputs instead of the
  holder's variables, or an unserialized user_input;
* a resolution failure is not recorded.
"""

from __future__ import annotations

from typing import ClassVar
from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel

from matrx_ai import _ext, mandates
from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.agents.named import AgentRecordSource


class _Inputs(BaseModel):
    topic: str


class _PackageAgent:
    mandate_key = "package.writer"
    Inputs = _Inputs
    seen_kwargs: ClassVar[dict[str, object]] = {}

    @classmethod
    def prepare_variables(cls, inputs: BaseModel) -> dict[str, object]:
        # The HOLDER's vocabulary differs from the call site's on purpose, so
        # the completion callback's variables prove prepare_variables ran.
        return {"article_subject": inputs.topic}

    @classmethod
    async def run(cls, **kwargs) -> AgentRunResult:
        cls.seen_kwargs = kwargs
        return AgentRunResult(success=True, output='{"title":"Package"}')


@pytest.fixture(autouse=True)
def _reset_seen() -> None:
    _PackageAgent.seen_kwargs = {}


@pytest.mark.asyncio
async def test_package_seam_invokes_host_completion_for_exact_resolution(monkeypatch) -> None:
    completion = AsyncMock()

    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        assert mandate_key == "package.writer"
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id="resolved-version", is_version=True),
            config_overrides={"temperature": 0.2, "max_output_tokens": 900},
            complete=completion,
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver)

    result = await mandates.run_mandated(
        _PackageAgent,
        inputs={"topic": "runtime honesty"},
        user_input={"brief": "keep it short"},
        config_overrides={"temperature": 0.5},
    )

    assert result.success is True
    assert _PackageAgent.seen_kwargs["source_override"] == AgentRecordSource(
        agent_id="resolved-version",
        is_version=True,
    )
    # Mandate overrides sit UNDER call-site overrides: the call's temperature wins,
    # the mandate's untouched key survives.
    assert _PackageAgent.seen_kwargs["config_overrides"] == {
        "temperature": 0.5,
        "max_output_tokens": 900,
    }
    completion.assert_awaited_once_with(
        result,
        {"article_subject": "runtime honesty"},
        '{"brief": "keep it short"}',
    )


@pytest.mark.asyncio
async def test_resolved_variable_mapping_and_spill_reach_the_run(monkeypatch) -> None:
    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id="bound-agent", is_version=False),
            variable_mapping={"article_subject": "subject_line"},
            spill_variables=frozenset({"notes"}),
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver)

    await mandates.run_mandated(_PackageAgent, inputs={"topic": "mapping"})

    assert _PackageAgent.seen_kwargs["variable_mapping"] == {"article_subject": "subject_line"}
    assert _PackageAgent.seen_kwargs["spill_variables"] == {"notes"}
    assert "config_overrides" not in _PackageAgent.seen_kwargs


@pytest.mark.asyncio
async def test_a_workflow_held_mandate_refuses_to_run_an_agent_record(monkeypatch) -> None:
    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            holder_type="workflow",
            workflow_id="6c1f7a1e-2d7b-4b6a-9d7e-1f3c5a9b8e21",
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver)

    with pytest.raises(
        mandates.MandateResolutionUnavailable,
        match="resolved to a 'workflow' Holder — this funnel can only run an agent record",
    ):
        await mandates.run_mandated(_PackageAgent, inputs={"topic": "workflow holder"})

    assert _PackageAgent.seen_kwargs == {}


@pytest.mark.asyncio
async def test_a_failed_resolver_refuses_the_run_and_records_it(monkeypatch) -> None:
    """🚨 NO SEED FALLBACK. A resolver failure must never let the agent id
    frozen in the class body run — that is a paid call against an agent nobody
    chose, invisible to the console and immune to every org/user binding. The
    failure is recorded, then the run refuses."""
    captured: list[dict[str, object]] = []

    async def record_error(exc: BaseException, **kwargs) -> None:
        captured.append({"exc": exc, **kwargs})

    async def broken_resolver(mandate_key: str):
        raise RuntimeError(f"cannot resolve {mandate_key}")

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", broken_resolver)
    monkeypatch.setattr(
        _ext,
        "get_ext",
        lambda name: record_error if name == "record_error" else None,
    )

    with pytest.raises(mandates.MandateResolutionUnavailable) as excinfo:
        await mandates.run_mandated(_PackageAgent, inputs={"topic": "fallback"})

    # The agent never ran at all — not on a seed, not on anything.
    assert _PackageAgent.seen_kwargs == {}
    assert excinfo.value.mandate_key == "package.writer"
    assert len(captured) == 1
    assert captured[0]["kind"] == "mandate_resolution_failed"
    assert captured[0]["error_type"] == "mandate_resolution_failed"
    assert captured[0]["payload"] == {
        "mandate_key": "package.writer",
        "consumer": "_PackageAgent",
        "effect": "run REFUSED; no agent ran and nothing was charged",
    }


@pytest.mark.asyncio
async def test_no_installed_resolver_refuses_instead_of_running_the_code_seed(
    monkeypatch,
) -> None:
    """The silent half of the same defect: with no resolver installed, this
    used to run the class's hardcoded id with NO alarm at all — so a host that
    never wired mandate resolution ran frozen agents forever and nothing said so."""

    class _SeededMandatedAgent(_PackageAgent):
        # A stale id left in a class body must never be what runs.
        source = AgentRecordSource(agent_id="stale-seed-id", is_version=False)

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    with pytest.raises(
        mandates.MandateResolutionUnavailable, match="no mandate resolver is installed"
    ):
        await mandates.run_mandated(_SeededMandatedAgent, inputs={"topic": "no resolver"})

    assert _SeededMandatedAgent.seen_kwargs == {}


@pytest.mark.asyncio
async def test_a_class_without_a_mandate_key_is_unmandated_and_still_runs(monkeypatch) -> None:
    """The refusal is scoped to MANDATED agents. A class that declares no
    mandate_key was never mandate-managed and must keep running on its own
    source — with the call's kwargs untouched (no source_override injected)."""

    class _Unmandated(_PackageAgent):
        mandate_key = None

    async def resolver_must_not_be_asked(mandate_key: str):
        raise AssertionError("an unmandated class must not consult the resolver")

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver_must_not_be_asked)

    result = await mandates.run_mandated(
        _Unmandated, inputs={"topic": "unmandated"}, config_overrides={"temperature": 0.1}
    )

    assert result.success is True
    assert _Unmandated.seen_kwargs == {
        "inputs": {"topic": "unmandated"},
        "config_overrides": {"temperature": 0.1},
    }
