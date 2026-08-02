"""Emergency-compaction connectivity recovery/breaker (Mercury).

Emergency compaction bypasses the failure circuit breaker (overflow is a "true
ceiling"), so a provider that can't be reached would spin the emergency path
forever — the Mercury self-hosted worker logged `compaction #16 …
consecutive_failures=16/3`. The optimizer now retries emergency compaction with
exponential backoff: a transient outage self-recovers, and only a persistently
dead provider aborts the task with ``ProviderUnreachableError``.

Pure unit tests — no LLM calls, no real sleeps. ``layer_2_auto_compact`` is
stubbed to drive ``_emergency_connectivity_failures`` (the internal handler sets
it > 0 only when the compaction model itself was unreachable).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Callable, Dict, Tuple

import pytest

from xpander_sdk import ProviderUnreachableError
from xpander_sdk.core.context_optimizer import constants as const
from xpander_sdk.core.context_optimizer import context_optimizer as co


def _agent() -> SimpleNamespace:
    """Duck-typed agent stub exposing only what the optimizer gate reads."""
    return SimpleNamespace(
        id="agent-1",
        configuration=SimpleNamespace(organization_id="org-1"),
        with_auto_context_management=True,
    )


def _emergency_optimizer(
    monkeypatch: pytest.MonkeyPatch,
    layer_2_behaviour: Callable[[Any, int], None],
) -> Tuple[Any, Dict[str, Any]]:
    """Build an optimizer with the pipeline stubbed so only the emergency branch runs.

    ``layer_2_behaviour(self, attempt)`` runs in place of the real compaction and
    sets ``self._emergency_connectivity_failures`` to mimic a connectivity failure
    (> 0) or a success / non-connectivity failure (0), as the internal handler would.
    """
    state: Dict[str, Any] = {"l2_calls": 0, "sleeps": []}

    async def _noop(self: Any, *a: Any, **k: Any) -> None:
        return None

    async def _spy_layer_2(
        self: Any, messages: Any, run_metrics: Any = None,
        custom_instructions: str = "", trigger: str = "auto",
    ) -> None:
        attempt = state["l2_calls"]
        state["l2_calls"] += 1
        layer_2_behaviour(self, attempt)

    async def _fake_sleep(delay: float) -> None:
        state["sleeps"].append(delay)

    monkeypatch.setattr(co.XPanderContextOptimizer, "layer_1_microcompact", _noop)
    monkeypatch.setattr(co.XPanderContextOptimizer, "_publish_context_status", _noop)
    monkeypatch.setattr(co.XPanderContextOptimizer, "_should_auto_compact", lambda self, m, estimated=0: False)
    monkeypatch.setattr(co.XPanderContextOptimizer, "_should_emergency_compact", lambda self, m, estimated=0: True)
    monkeypatch.setattr(co.XPanderContextOptimizer, "layer_2_auto_compact", _spy_layer_2)
    monkeypatch.setattr(co.asyncio, "sleep", _fake_sleep)

    opt = co.XPanderContextOptimizer(agent=_agent(), task=SimpleNamespace(id="task-1"))
    return opt, state


@pytest.mark.asyncio
async def test_emergency_succeeds_first_try_no_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    """A compaction that succeeds immediately does not retry or sleep."""

    def _ok(self: Any, attempt: int) -> None:
        self._emergency_connectivity_failures = 0

    opt, state = _emergency_optimizer(monkeypatch, _ok)
    await opt.acompress([])
    assert state["l2_calls"] == 1
    assert state["sleeps"] == []


@pytest.mark.asyncio
async def test_emergency_recovers_after_transient_connectivity(monkeypatch: pytest.MonkeyPatch) -> None:
    """A transient outage self-recovers: fail twice, back off, then succeed."""

    def _flaky(self: Any, attempt: int) -> None:
        self._emergency_connectivity_failures = 0 if attempt >= 2 else attempt + 1

    opt, state = _emergency_optimizer(monkeypatch, _flaky)
    await opt.acompress([])
    assert state["l2_calls"] == 3  # 2 failed + 1 recovered
    assert state["sleeps"] == [2.0, 4.0]  # exponential backoff before each retry


@pytest.mark.asyncio
async def test_emergency_aborts_when_provider_stays_dead(monkeypatch: pytest.MonkeyPatch) -> None:
    """A persistently dead provider aborts with ProviderUnreachableError after the window."""

    def _dead(self: Any, attempt: int) -> None:
        self._emergency_connectivity_failures = attempt + 1  # never recovers

    opt, state = _emergency_optimizer(monkeypatch, _dead)
    with pytest.raises(ProviderUnreachableError):
        await opt.acompress([])
    assert state["l2_calls"] == const.EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS + 1
    assert len(state["sleeps"]) == const.EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS
    assert max(state["sleeps"]) <= const.EMERGENCY_CONNECTIVITY_RETRY_MAX_DELAY


@pytest.mark.asyncio
async def test_emergency_non_connectivity_failure_does_not_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    """A non-connectivity failure (counter stays 0) must not enter the retry loop."""

    def _other_failure(self: Any, attempt: int) -> None:
        self._emergency_connectivity_failures = 0

    opt, state = _emergency_optimizer(monkeypatch, _other_failure)
    await opt.acompress([])
    assert state["l2_calls"] == 1
    assert state["sleeps"] == []
