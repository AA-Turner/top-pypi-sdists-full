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
        return inputs.model_dump()

    @classmethod
    async def run(cls, **kwargs) -> AgentRunResult:
        cls.seen_kwargs = kwargs
        return AgentRunResult(success=True, output='{"title":"Package"}')


@pytest.mark.asyncio
async def test_package_seam_invokes_host_completion_for_exact_resolution(monkeypatch) -> None:
    completion = AsyncMock()

    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        assert mandate_key == "package.writer"
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id="resolved-version", is_version=True),
            config_overrides={"temperature": 0.2},
            complete=completion,
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver)

    result = await mandates.run_mandated(
        _PackageAgent,
        inputs={"topic": "runtime honesty"},
        config_overrides={"temperature": 0.5},
    )

    assert result.success is True
    assert _PackageAgent.seen_kwargs["source_override"] == AgentRecordSource(
        agent_id="resolved-version",
        is_version=True,
    )
    assert _PackageAgent.seen_kwargs["config_overrides"] == {"temperature": 0.5}
    completion.assert_awaited_once_with(
        result,
        {"topic": "runtime honesty"},
        None,
    )


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
    _PackageAgent.seen_kwargs = {}

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
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)
    _PackageAgent.seen_kwargs = {}

    with pytest.raises(mandates.MandateResolutionUnavailable) as excinfo:
        await mandates.run_mandated(_PackageAgent, inputs={"topic": "no resolver"})

    assert _PackageAgent.seen_kwargs == {}
    assert "no mandate resolver is installed" in str(excinfo.value)


@pytest.mark.asyncio
async def test_a_class_without_a_mandate_key_is_unmandated_and_still_runs(monkeypatch) -> None:
    """The refusal is scoped to MANDATED agents. A class that declares no
    mandate_key was never mandate-managed and must keep running on its own source."""

    class _Unmandated(_PackageAgent):
        mandate_key = None
        seen_kwargs: ClassVar[dict[str, object]] = {}

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    result = await mandates.run_mandated(_Unmandated, inputs={"topic": "unmandated"})

    assert result.success is True
