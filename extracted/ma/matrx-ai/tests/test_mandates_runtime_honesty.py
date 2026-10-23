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

import pytest
from pydantic import BaseModel

from matrx_ai import mandates
from matrx_ai.agents.executor import AgentRunResult


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


class _RunStopper(RuntimeError):
    """What the host raises for an answer missing required keys from a Holder
    chosen although it does not declare them (aidream MandateOutputError)."""

    fails_the_run = True


