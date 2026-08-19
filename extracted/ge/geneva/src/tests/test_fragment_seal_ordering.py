# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Seal hand-off must keep the sentinel behind its checkpoints.

The queue actor applies separately submitted ``put_nowait`` tasks out of order,
so a sentinel submitted last can still arrive first and make the writer treat
covered rows as a gap. These tests pin the single-``put_nowait_batch`` shape
that prevents it.
"""

import inspect
from typing import Any
from unittest.mock import MagicMock

import pytest
import ray
import ray.util.queue
from ray_pipeline_test_utils import (
    make_fragment_writer_manager,
    make_fragment_writer_session,
)

from geneva.runners.ray.pipeline import _SEAL_SENTINEL, FragmentWriterSession


class _FakeQueueActor:
    """Records the shape of every enqueue call made by a session."""

    def __init__(self) -> None:
        self.batch_calls: list[list[tuple[int, Any, int]]] = []
        self.item_calls: list[tuple[int, Any, int]] = []

    @property
    def put_nowait_batch(self) -> Any:
        outer = self

        class _Remote:
            @staticmethod
            def remote(items: list[tuple[int, Any, int]]) -> Any:
                outer.batch_calls.append(list(items))
                return MagicMock(name="batch-ack")

        return _Remote

    @property
    def put_nowait(self) -> Any:
        outer = self

        class _Remote:
            @staticmethod
            def remote(item: tuple[int, Any, int]) -> Any:
                outer.item_calls.append(item)
                return MagicMock(name="item-ack")

        return _Remote


def _session_with_fake_queue(
    monkeypatch: pytest.MonkeyPatch, n_tasks: int
) -> tuple[FragmentWriterSession, _FakeQueueActor]:
    """Session holding ``n_tasks`` ingested-but-not-enqueued checkpoints."""
    fake_actor = _FakeQueueActor()

    def _fake_start_writer(self: FragmentWriterSession) -> None:
        queue = MagicMock()
        queue.actor = fake_actor
        self.queue = queue
        self.actor = MagicMock(name="writer-actor")

    def _fake_shutdown(
        self: FragmentWriterSession, *, force_queue: bool = False
    ) -> None:
        self.queue = None
        self.actor = None
        self._shutdown = True

    monkeypatch.setattr(FragmentWriterSession, "_start_writer", _fake_start_writer)
    monkeypatch.setattr(FragmentWriterSession, "shutdown", _fake_shutdown)

    sess = make_fragment_writer_session()
    for offset in range(n_tasks):
        sess.ingest_task(offset * 10, f"ckp-{offset}", 10)
    assert not sess.started, "writer startup must stay lazy until seal"
    return sess, fake_actor


def test_lazy_seal_sends_one_batch_with_sentinel_last(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The common path: one batched call, sentinel last, no per-item enqueues."""
    sess, fake_actor = _session_with_fake_queue(monkeypatch, n_tasks=5)

    sess.seal()

    assert len(fake_actor.batch_calls) == 1, (
        "seal must hand off in exactly one put_nowait_batch; per-item enqueues "
        "let the sentinel overtake checkpoint data"
    )
    assert fake_actor.item_calls == [], (
        "seal must not use per-item put_nowait on the lazy path"
    )

    items = fake_actor.batch_calls[0]
    assert items[-1] == _SEAL_SENTINEL, "sentinel must be the final item"
    assert items[:-1] == [(offset * 10, f"ckp-{offset}", 10) for offset in range(5)]
    assert _SEAL_SENTINEL not in items[:-1]


def test_seal_retains_ack_for_failure_detection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The batch is fire-and-forget, so its ack must be kept to be inspected."""
    sess, _ = _session_with_fake_queue(monkeypatch, n_tasks=2)

    sess.seal()

    assert sess._seal_ack_ref is not None, (
        "dropping the ack makes a failed hand-off invisible: the writer would "
        "wait forever for a sentinel that never arrived"
    )


def test_restart_replay_keeps_sentinel_in_the_same_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Replay after a restart keeps the sentinel in the same batch."""
    sess, fake_actor = _session_with_fake_queue(monkeypatch, n_tasks=3)
    sess.seal()
    fake_actor.batch_calls.clear()
    fake_actor.item_calls.clear()

    sess._restart()

    assert len(fake_actor.batch_calls) == 1, "sealed replay must be one batch"
    assert fake_actor.item_calls == [], "sealed replay must not enqueue per item"
    items = fake_actor.batch_calls[0]
    assert items[-1] == _SEAL_SENTINEL
    assert items[:-1] == [(offset * 10, f"ckp-{offset}", 10) for offset in range(3)]


def test_unsealed_restart_replays_without_a_sentinel(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unsealed session replays checkpoints only; ordering among them is free."""
    sess, fake_actor = _session_with_fake_queue(monkeypatch, n_tasks=3)
    sess._start_writer()
    sess.sealed = False

    sess._restart()

    assert fake_actor.batch_calls == [], "unsealed replay must not send a sentinel"
    assert len(fake_actor.item_calls) == 3
    assert _SEAL_SENTINEL not in fake_actor.item_calls


def test_put_nowait_batch_is_still_synchronous_on_this_ray() -> None:
    """The batched hand-off is only atomic while this stays a plain function."""
    fn = ray.util.queue._QueueActor.put_nowait_batch
    assert not inspect.iscoroutinefunction(fn), (
        "ray.util.queue._QueueActor.put_nowait_batch became a coroutine; the "
        "batched seal hand-off is no longer atomic and must be reworked"
    )
    assert "await" not in inspect.getsource(fn), (
        "put_nowait_batch now yields to the event loop; the batched seal "
        "hand-off is no longer atomic and must be reworked"
    )


def test_check_seal_ack_is_a_noop_before_and_after_consumption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No ack outstanding, or ack not yet ready, must not touch the session."""
    sess, _ = _session_with_fake_queue(monkeypatch, n_tasks=1)

    sess.check_seal_ack()  # nothing sealed yet
    assert sess._seal_ack_ref is None

    sess.seal()
    ref = sess._seal_ack_ref
    monkeypatch.setattr(ray, "wait", lambda refs, timeout=None: ([], list(refs)))
    sess.check_seal_ack()
    assert sess._seal_ack_ref is ref, "an unready ack must be left for a later poll"


def test_check_seal_ack_consumes_a_successful_ack(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A clean ack is consumed once and not re-checked."""
    sess, _ = _session_with_fake_queue(monkeypatch, n_tasks=1)
    sess.seal()

    monkeypatch.setattr(ray, "wait", lambda refs, timeout=None: (list(refs), []))
    monkeypatch.setattr(ray, "get", lambda ref: None)
    sess.check_seal_ack()

    assert sess._seal_ack_ref is None


def test_failed_seal_ack_restarts_and_keeps_the_replacement_ack(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A dead queue actor must restart the session and keep the replacement ack."""
    sess, fake_actor = _session_with_fake_queue(monkeypatch, n_tasks=2)
    sess.seal()
    first_ref = sess._seal_ack_ref
    fake_actor.batch_calls.clear()

    def _boom(ref: Any) -> None:
        raise ray.exceptions.ActorDiedError()

    monkeypatch.setattr(ray, "wait", lambda refs, timeout=None: (list(refs), []))
    monkeypatch.setattr(ray, "get", _boom)
    sess.check_seal_ack()

    assert len(fake_actor.batch_calls) == 1, "failed ack must replay via restart"
    assert sess._seal_ack_ref is not None, (
        "the restart's fresh ack was discarded; later hand-off failures would "
        "now be silent"
    )
    assert sess._seal_ack_ref is not first_ref


def test_poll_all_reaps_seal_acks(monkeypatch: pytest.MonkeyPatch) -> None:
    """The reaper is wired into poll_all; without the call it is dead code."""
    sess, _ = _session_with_fake_queue(monkeypatch, n_tasks=1)
    sess.seal()

    manager = make_fragment_writer_manager(sessions={sess.frag_id: sess})
    called: list[int] = []
    monkeypatch.setattr(
        FragmentWriterSession,
        "check_seal_ack",
        lambda self: called.append(self.frag_id),
    )

    manager.poll_all()

    assert called == [sess.frag_id], "poll_all must reap outstanding seal acks"
