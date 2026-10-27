"""A person moves the CLI BACK by hand; auto-update still reaches the newest (plan clean-uninstall-reinstall R3).

Measured on the harness (real uv, release code 0.990.x, 2026-10-26): the
service updated 0.990.0 -> 0.990.1; then `uv tool uninstall probe-research`
and `uv tool install probe-research==0.990.0`. For the next five minutes every
`check-now` answered `recent` (the last check, the one that installed 0.990.1,
was minutes old: CHECK_NOW_COOLDOWN_S), the schedule's next check was
CHECK_EVERY_S (6 h) away, and the lifeboat waits 12 h behind: the machine
stayed on 0.990.0. The last check answered for an install that is no longer
there. Now a cycle records what it left installed (`checked_cli`), and a CLI
older than that (runtime.json, which every CLI start writes) makes a check
due at once, past the cooldown.
"""

from __future__ import annotations

import json
import time

import pytest

from probe.service import paths, updater


@pytest.fixture(autouse=True)
def _auto_update_on(monkeypatch):
    monkeypatch.setattr(updater, "auto_update_enabled", lambda extra_dirs=(): True)


def _updater(version: str) -> updater.Updater:
    return updater.Updater(version=version, emit=lambda *a: None, changed=lambda: None, stop=lambda r: None,
                           action_running=lambda: False, discovering=lambda: False)


def _state(**fields) -> None:
    path = paths.update_state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"v": updater.STATE_VERSION, **fields}))


def _runtime(version: str) -> None:
    path = paths.runtime_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"python": "/x/bin/python", "cli_version": version}))


def test_a_cli_moved_back_by_hand_makes_a_check_due_at_once():
    """The R3 state: the last check (minutes ago) left 0.990.1 installed; a
    person's `uv tool install ==0.990.0` since. A check is due now, and a
    `check-now` is not refused as `recent`."""
    _state(last_check=time.time() - 120, checked_cli="0.990.1")
    _runtime("0.990.0")
    u = _updater("0.990.0")
    assert u.moved_back()
    assert u.due(), "the last check answered for 0.990.1, not for the 0.990.0 installed now"
    u._loop = object()  # `start` needs a loop; recorded instead
    started = []
    u.start = lambda trigger: started.append(trigger) or "c0ffee"  # type: ignore[method-assign]
    answer = u._check_cycle("cli")
    assert answer["outcome"] != updater.CheckOutcome.RECENT and started == ["cli"]


def test_the_same_install_keeps_its_schedule_and_cooldown():
    """Control: nothing moved since the last check -- not due, and a check-now
    within the cooldown is still `recent` (no check storm)."""
    _state(last_check=time.time() - 120, checked_cli="0.990.1")
    _runtime("0.990.1")
    u = _updater("0.990.1")
    assert not u.moved_back() and not u.due()
    assert u._check_cycle("cli")["outcome"] == updater.CheckOutcome.RECENT


def test_a_newer_cli_than_the_check_saw_is_no_reason_to_check_again():
    """A person installed a NEWER one by hand: nothing to catch up with."""
    _state(last_check=time.time() - 120, checked_cli="0.990.0")
    _runtime("0.990.1")
    assert not _updater("0.990.1").due()


def test_a_cycle_records_what_it_left_installed(monkeypatch):
    """`checked_cli`: the self step's version (what the CLI is now), else the
    installed one; the next check compares with it."""
    import asyncio

    u = _updater("0.990.0")
    _runtime("0.990.0")

    async def core(cycle_id, trigger):
        return {"state": updater.StepState.DONE, "exit_code": 0}

    async def app(cycle_id, trigger):
        return {"state": updater.StepState.SKIPPED}

    async def self_step(cycle_id):
        return {"state": updater.StepState.DONE, "from_version": "0.990.0", "to_version": "0.990.1",
                "restart": False}, False

    monkeypatch.setattr(u, "_core", core)
    monkeypatch.setattr(u, "_app", app)
    monkeypatch.setattr(u, "_self", self_step)
    monkeypatch.setattr(u, "_save", lambda: None)
    monkeypatch.setattr(u, "_arm", lambda: None)
    monkeypatch.setattr(u, "followup", lambda restart: None)

    async def run():
        u._loop = asyncio.get_running_loop()
        await u._cycle("c0ffee", "cli")

    asyncio.run(run())
    assert u.state["checked_cli"] == "0.990.1"
