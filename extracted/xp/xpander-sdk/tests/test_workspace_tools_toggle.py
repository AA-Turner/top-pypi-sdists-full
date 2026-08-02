"""Unit tests for the ``Agent.workspace_tools_enabled`` toggle (PRO-1455).

When an agent has ``workspace_tools_enabled=False`` the SDK must suppress all
workspace I/O while keeping non-workspace context compaction:

- ``XPanderContextOptimizer._save_to_workspace`` returns ``None`` (the single
  choke for both inline and fallback L1 offload).
- ``maybe_offload_content`` then leaves content inline — ``(None, None)``.
- The L2 session-backup write is skipped (covered indirectly via the
  ``_workspace_enabled`` gate).
- ``ActionLedger.aappend`` keeps the in-memory entry but queues no workspace
  write; ``aload`` no-ops.

Pure unit tests — no LLM calls, no network. Stubs duck-type the few agent/task
attributes the gates read.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from xpander_sdk.core.context_optimizer import context_optimizer as co
from xpander_sdk.core.context_optimizer.action_ledger import ActionLedger
from xpander_sdk.models.action_ledger import LedgerEntry, LedgerEntryClass

# --------------------------------------------------------------------- #
#  Stubs
# --------------------------------------------------------------------- #


def _agent(workspace_tools_enabled=True, *, with_flag=True):
    """Duck-typed agent. ``with_flag=False`` omits the attribute entirely to
    exercise the ``getattr(..., True)`` default."""
    kwargs = dict(
        id="agent-1",
        configuration=SimpleNamespace(organization_id="org-1"),
    )
    if with_flag:
        kwargs["workspace_tools_enabled"] = workspace_tools_enabled
    return SimpleNamespace(**kwargs)


def _task():
    return SimpleNamespace(id="task-1")


def _entry(seq=1):
    return LedgerEntry(
        seq=seq,
        ts=f"t{seq}",
        tool_name="some_tool",
        entry_class=LedgerEntryClass.WRITE,
        target="tbl",
        status="ok",
    )


_BIG = "x" * 20_000  # well above max_content_length (8_000)


# --------------------------------------------------------------------- #
#  Optimizer: _workspace_enabled
# --------------------------------------------------------------------- #


def test_optimizer_workspace_enabled_reflects_flag():
    assert (
        co.XPanderContextOptimizer(agent=_agent(True), task=_task())._workspace_enabled
        is True
    )
    assert (
        co.XPanderContextOptimizer(agent=_agent(False), task=_task())._workspace_enabled
        is False
    )


def test_optimizer_workspace_enabled_defaults_true_when_attr_missing():
    opt = co.XPanderContextOptimizer(agent=_agent(with_flag=False), task=_task())
    assert opt._workspace_enabled is True


# --------------------------------------------------------------------- #
#  Optimizer: offload gating
# --------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_save_to_workspace_returns_none_when_disabled():
    opt = co.XPanderContextOptimizer(agent=_agent(False), task=_task())
    assert await opt._save_to_workspace(_BIG) is None


@pytest.mark.asyncio
async def test_maybe_offload_passthrough_when_disabled():
    opt = co.XPanderContextOptimizer(agent=_agent(False), task=_task())
    assert await opt.maybe_offload_content(_BIG, "some_tool") == (None, None)


@pytest.mark.asyncio
async def test_maybe_offload_offloads_when_enabled(monkeypatch):
    # Isolate from the network — the background write would POST to the
    # workspace endpoint; we only care that an offload path is produced.
    async def _fake_write(self, path, content):
        return None

    monkeypatch.setattr(co.XPanderContextOptimizer, "_do_workspace_write", _fake_write)
    opt = co.XPanderContextOptimizer(agent=_agent(True), task=_task())
    # Pressured context so the base 8K threshold applies, not the wide
    # low-headroom band — this test is about the workspace toggle, not banding.
    opt._last_estimated_tokens = int(opt.context_window * 0.8)
    replacement, path = await opt.maybe_offload_content(_BIG, "some_tool")
    assert path is not None
    assert path.startswith("CONTEXT_OPTIMIZATION/")
    assert replacement is not None


# --------------------------------------------------------------------- #
#  ActionLedger: persistence gating
# --------------------------------------------------------------------- #


def test_ledger_workspace_enabled_reflects_flag():
    assert ActionLedger(agent=_agent(True), task=_task())._workspace_enabled is True
    assert ActionLedger(agent=_agent(False), task=_task())._workspace_enabled is False


@pytest.mark.asyncio
async def test_ledger_aappend_keeps_memory_skips_write_when_disabled():
    led = ActionLedger(agent=_agent(False), task=_task())
    await led.aappend(_entry(1))
    assert len(led.entries) == 1  # in-memory entry retained
    assert led._pending_writes == []  # nothing queued to the workspace


@pytest.mark.asyncio
async def test_ledger_aappend_queues_write_when_enabled(monkeypatch):
    # No optimizer cache attached to the stub task, so aappend falls back to
    # its own _pending_writes task list. Stub the POST so nothing hits the net.
    async def _fake_append(self, ciphertext_line):
        return None

    monkeypatch.setattr(ActionLedger, "_do_workspace_append", _fake_append)
    led = ActionLedger(agent=_agent(True), task=_task())
    await led.aappend(_entry(1))
    assert len(led.entries) == 1
    assert len(led._pending_writes) == 1


@pytest.mark.asyncio
async def test_ledger_aload_noop_when_disabled():
    # Would raise if it attempted a request (stub config has no real client),
    # and must not flip _loaded.
    led = ActionLedger(agent=_agent(False), task=_task())
    await led.aload()
    assert led._loaded is False
