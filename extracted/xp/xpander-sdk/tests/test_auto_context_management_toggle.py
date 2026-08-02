"""Unit tests for the ``Agent.with_auto_context_management`` toggle.

When an agent has ``with_auto_context_management=False`` the SDK must skip the
entire context-optimization pipeline: ``XPanderContextOptimizer.acompress``
returns immediately, so no layer (L1/L2/L3/emergency) runs and no context
status is published. When the flag is True — or absent (legacy agents) — the
pipeline runs as before.

Pure unit tests — no LLM calls, no network. A duck-typed agent stub provides the
few attributes the gate reads, and the per-layer entrypoints are stubbed so the
enabled path stops after the first (cheap) call.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co


def _agent(with_auto_context_management=True, *, with_flag=True):
    """Duck-typed agent. ``with_flag=False`` omits the attribute entirely to
    exercise the ``getattr(..., True)`` default."""
    kwargs = dict(
        id="agent-1",
        configuration=SimpleNamespace(organization_id="org-1"),
    )
    if with_flag:
        kwargs["with_auto_context_management"] = with_auto_context_management
    return SimpleNamespace(**kwargs)


def _task():
    return SimpleNamespace(id="task-1")


def _spied_optimizer(monkeypatch, agent):
    """Build an optimizer whose pipeline entrypoints are replaced with spies so
    the enabled path is observable and never touches the network."""
    calls = {"layer_1": 0, "publish": 0}

    async def _spy_layer_1(self, messages: list) -> None:
        """Spy replacing layer_1_microcompact; records the call."""
        calls["layer_1"] += 1

    async def _spy_publish(
        self, messages: list, *, force: bool = False, estimated: int | None = None
    ) -> None:
        """Spy replacing _publish_context_status; records the call."""
        calls["publish"] += 1

    monkeypatch.setattr(co.XPanderContextOptimizer, "layer_1_microcompact", _spy_layer_1)
    monkeypatch.setattr(co.XPanderContextOptimizer, "_publish_context_status", _spy_publish)
    return co.XPanderContextOptimizer(agent=agent, task=_task()), calls


@pytest.mark.asyncio
async def test_acompress_skips_pipeline_when_disabled(monkeypatch):
    opt, calls = _spied_optimizer(monkeypatch, _agent(False))
    await opt.acompress([])
    assert calls == {"layer_1": 0, "publish": 0}


@pytest.mark.asyncio
async def test_acompress_runs_pipeline_when_enabled(monkeypatch):
    opt, calls = _spied_optimizer(monkeypatch, _agent(True))
    await opt.acompress([])
    assert calls["layer_1"] == 1
    assert calls["publish"] == 1


@pytest.mark.asyncio
async def test_acompress_runs_pipeline_when_flag_absent(monkeypatch):
    # Legacy agents without the attribute default to enabled.
    opt, calls = _spied_optimizer(monkeypatch, _agent(with_flag=False))
    await opt.acompress([])
    assert calls["layer_1"] == 1


def test_compress_sync_wrapper_skips_when_disabled(monkeypatch):
    # The sync wrapper delegates to acompress, so the gate must hold there too.
    opt, calls = _spied_optimizer(monkeypatch, _agent(False))
    opt.compress([])
    assert calls == {"layer_1": 0, "publish": 0}
