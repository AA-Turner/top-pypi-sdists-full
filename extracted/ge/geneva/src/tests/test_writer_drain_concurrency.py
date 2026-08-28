# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Teardown drains every writer session together, not one after another.

Draining session-by-session deadlocks when writers contend for memory. Each
sealed session owns its own FragmentWriter actor, a writer's Ray reservation is
returned only by ``sess.shutdown()`` -> ``ray.kill``, and a serial loop blocks
inside one session's drain on a write future belonging to an actor Ray may never
have placed. When only one writer fits on the node and Ray places the one whose
session sits *later* in the iteration order, its memory is never reaped, the
blocked session's actor never becomes placeable, and the job burns
``MAX_WRITER_RESTARTS x WRITER_NO_PROGRESS_TIMEOUT_S`` committing nothing.

Measured before the fix, on an 8 GiB container: eight fragments produced eight
writer actors at once, every applier already dead, and the run committed 0 rows
across ~50 minutes of silent restarts.
"""

from unittest.mock import MagicMock

import pytest

from geneva.runners.ray import pipeline as pipeline_mod
from tests.ray_pipeline_test_utils import (
    attach_started_writer_future,
    make_fragment_write_result,
    make_fragment_writer_manager,
    make_fragment_writer_session,
)


def _sealed_session(frag_id: int):  # noqa: ANN202
    """A session that is sealed and waiting on exactly one write future."""
    sess = make_fragment_writer_session(frag_id=frag_id)
    sess.sealed = True
    fut = attach_started_writer_future(sess)
    return sess, fut


def _scripted_wait(monkeypatch: pytest.MonkeyPatch, schedule: list[list[object]]):  # noqa: ANN202
    """Install a ``ray.wait`` that resolves futures on a schedule.

    Models resolution as accumulating state rather than counting calls: a
    blocking wait (``timeout`` truthy) releases the next batch in ``schedule``,
    a non-blocking one (``timeout=0``) only reports what is already resolved.
    The drain legitimately calls wait twice per round -- once to block, once to
    sweep up everything else that finished -- so a fake that popped a batch per
    *call* would resolve futures the schedule never released.
    """
    resolved: set[int] = set()

    def _wait(futures, num_returns=1, timeout=None):  # noqa: ANN001, ANN202
        futures = list(futures)
        if timeout and schedule:
            resolved.update(id(f) for f in schedule.pop(0))
        ready = [f for f in futures if id(f) in resolved][:num_returns]
        return ready, [f for f in futures if f not in ready]

    monkeypatch.setattr(pipeline_mod.ray, "wait", _wait)


@pytest.fixture
def _no_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Silence the commit machinery; this is a test about draining."""
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterManager,
        "_drain_pending_fragment_records",
        lambda self, max_to_drain=None: 0,
    )
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterManager,
        "_commit_if_n_fragments",
        lambda self, n, robust=False: None,
    )
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterManager,
        "_shutdown_fragment_record_executor",
        lambda self: None,
    )


# The discriminating test: verified to fail against the serial drain with
# "a serial per-session drain gives [0, 1]". The timeout is a backstop, since
# the real-world symptom of this bug is a wait that never ends.
@pytest.mark.timeout(60)
@pytest.mark.usefixtures("_no_commit")
def test_a_blocked_session_does_not_stall_the_others(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fix, stated as an ordering property.

    Fragment 0 is first in iteration order and its writer never becomes ready
    -- it stands in for an actor stuck in ``PENDING_CREATION`` because another
    writer holds the node's memory. Fragment 1 is ready immediately.

    A serial drain would sit on fragment 0 and never touch fragment 1, so
    fragment 1's writer would never be killed and its memory never returned.
    Draining the union means fragment 1 is consumed and reaped first.
    """
    blocked, blocked_fut = _sealed_session(0)
    ready, ready_fut = _sealed_session(1)
    # Insertion order matters: the blocked session is the one a serial loop
    # would reach first.
    manager = make_fragment_writer_manager(sessions={0: blocked, 1: ready})

    recorded: list[int] = []
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterManager,
        "_record_fragment",
        lambda self, frag_id, *a, **kw: recorded.append(frag_id),
    )

    # Fragment 1 resolves on the first blocking wait; fragment 0 only on a
    # later one, so the test fails if the drain insists on finishing fragment 0
    # first.
    _scripted_wait(monkeypatch, [[ready_fut], [blocked_fut]])
    monkeypatch.setattr(
        pipeline_mod.ray,
        "get",
        lambda fut: make_fragment_write_result(
            frag_id=0 if fut is blocked_fut else 1, rows_written=16
        ),
    )
    monkeypatch.setattr(pipeline_mod.ray, "kill", MagicMock())

    manager.cleanup()

    assert recorded == [1, 0], (
        "expected the ready fragment to be consumed before the blocked one; a "
        f"serial per-session drain gives {recorded}"
    )
    assert not manager.sessions, "every session should be reaped by teardown"


# Documents the reaping property rather than catching the bug: it passes
# against the serial drain too, because there the futures happen to resolve in
# iteration order. Kept so a future change cannot quietly move reaping to a
# sweep at the end, which is what would reintroduce the deadlock.
@pytest.mark.timeout(60)
@pytest.mark.usefixtures("_no_commit")
def test_each_writer_is_reaped_as_soon_as_it_finishes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reaping is what actually returns memory, so it must not wait for the
    slowest session. Each writer is killed on the round its future resolves,
    not in a sweep after every session has drained."""
    first, first_fut = _sealed_session(0)
    second, second_fut = _sealed_session(1)
    manager = make_fragment_writer_manager(sessions={0: first, 1: second})

    # attrs slots class: patch the method on the class, not the instance.
    killed: list[int] = []
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterSession,
        "shutdown",
        lambda self, **kw: killed.append(self.frag_id),
    )

    # Snapshot which writers had been reaped at the moment each result landed.
    reaped_when_recorded: dict[int, list[int]] = {}
    monkeypatch.setattr(
        pipeline_mod.FragmentWriterManager,
        "_record_fragment",
        lambda self, frag_id, *a, **kw: reaped_when_recorded.setdefault(
            frag_id, list(killed)
        ),
    )

    _scripted_wait(monkeypatch, [[first_fut], [second_fut]])
    monkeypatch.setattr(
        pipeline_mod.ray,
        "get",
        lambda fut: make_fragment_write_result(
            frag_id=0 if fut is first_fut else 1, rows_written=16
        ),
    )

    manager.cleanup()

    # Fragment 0 finishes first, so by the time fragment 1's result is recorded
    # fragment 0's writer must already have released its reservation.
    assert 0 in reaped_when_recorded[1], (
        "fragment 0's writer was still holding its reservation when fragment 1 "
        f"completed; reaped so far was {reaped_when_recorded[1]}"
    )
    assert set(killed) == {0, 1}


@pytest.mark.timeout(60)
@pytest.mark.usefixtures("_no_commit")
def test_no_progress_watchdog_still_fires_under_the_shared_drain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The watchdog changed drivers, so prove it still runs.

    ``drain()`` used to tick each session's no-progress deadline itself. The
    shared loop waits on every session at once, so it calls
    ``poll_liveness()`` on each sealed session whenever a round passes with no
    future resolving. Losing that would turn a genuinely wedged writer into a
    silent forever-wait -- strictly worse than the deadlock being fixed.
    """
    monkeypatch.setattr(pipeline_mod, "WRITER_NO_PROGRESS_TIMEOUT_S", 0.05)
    monkeypatch.setattr(pipeline_mod, "_DRAIN_POLL_INTERVAL_S", 0.01)

    wedged, _fut = _sealed_session(0)
    manager = make_fragment_writer_manager(sessions={0: wedged})

    restarts: list[int] = []

    def _fake_restart(self) -> None:  # noqa: ANN001
        restarts.append(self.frag_id)
        # Stand in for the restart succeeding, so the drain can terminate.
        self.inflight.clear()

    monkeypatch.setattr(pipeline_mod.FragmentWriterSession, "_restart", _fake_restart)
    # The probe never resolves: exactly the last=None case seen in production.
    monkeypatch.setattr(pipeline_mod.ray, "wait", lambda futures, **kw: ([], futures))
    monkeypatch.setattr(pipeline_mod.ray, "kill", MagicMock())

    manager.cleanup()

    assert restarts == [0], (
        "a wedged writer was never restarted -- the no-progress watchdog is not "
        "being driven by the shared drain loop"
    )
