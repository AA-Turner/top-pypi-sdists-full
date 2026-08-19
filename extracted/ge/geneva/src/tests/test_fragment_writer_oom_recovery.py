# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Driver-owned, shrinking FragmentWriter OOM recovery (GEN-780)."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
import ray
from ray_pipeline_test_utils import (
    MockedRayWriterHarness,
    make_fragment_write_result,
    make_fragment_writer_manager,
    make_fragment_writer_session,
)

from geneva.errors import FatalWorkerOOMError
from geneva.runners.ray.oom_recovery_budget import (
    OOMRecoveryBudgetConfig,
    OOMRecoveryBudgetTracker,
)
from geneva.runners.ray.pipeline import _SEAL_SENTINEL, FragmentWriterManager


def _tracker(*, same_range_limit: int = 3) -> OOMRecoveryBudgetTracker:
    return OOMRecoveryBudgetTracker(
        config=OOMRecoveryBudgetConfig(
            enabled=True,
            max_total_oom_recoveries=same_range_limit,
            max_same_range_oom_recoveries=same_range_limit,
        )
    )


def _writer_kwargs(harness: MockedRayWriterHarness, attempt: int) -> dict[str, Any]:
    return harness.writer.options.return_value.remote.call_args_list[attempt].kwargs


def test_classified_writer_oom_restarts_with_smaller_tranches() -> None:
    """The same complete replay log is consumed with a strictly smaller cap."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        sess = make_fragment_writer_session(
            oom_budget_tracker=_tracker(),
            job_id="job-gen-780",
        )
        sess.ingest_task(0, "ckpt_range-0-8", 8)
        sess.seal()
        failed_future = harness.write_futures[0]

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("writer OOM"),
        ):
            assert sess.consume_ready_future(failed_future) is None

    assert not sess.failed
    assert sess.writer_max_rows == 4
    assert sess._restart_count == 0, "OOM must not consume the transient-loss budget"
    assert len(harness.actors) == 2
    assert _writer_kwargs(harness, 0)["max_rows_per_batch"] is None
    assert _writer_kwargs(harness, 1)["max_rows_per_batch"] == 4
    assert sess.cached_tasks == [(0, "ckpt_range-0-8", 8)]
    expected_replay = [(0, "ckpt_range-0-8", 8), _SEAL_SENTINEL]
    assert harness.batch_calls(1) == [expected_replay]


def test_non_oom_restart_keeps_the_current_writer_cap() -> None:
    """A transient loss after OOM full-replays at the already reduced cap."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
        patch(
            "geneva.runners.ray.pipeline._get_current_k8s_pod_statuses",
            return_value=None,
        ),
    ):
        sess = make_fragment_writer_session(
            oom_budget_tracker=_tracker(),
            job_id="job-gen-780",
        )
        sess.ingest_task(0, "ckpt_range-0-8", 8)
        sess.seal()

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("writer OOM"),
        ):
            assert sess.consume_ready_future(harness.write_futures[0]) is None

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.ActorDiedError(),
        ):
            assert sess.consume_ready_future(harness.write_futures[1]) is None

    assert not sess.failed
    assert sess.writer_max_rows == 4
    assert sess._restart_count == 1
    assert _writer_kwargs(harness, 0)["max_rows_per_batch"] is None
    assert _writer_kwargs(harness, 1)["max_rows_per_batch"] == 4
    assert _writer_kwargs(harness, 2)["max_rows_per_batch"] == 4
    assert harness.batch_calls(2) == [[(0, "ckpt_range-0-8", 8), _SEAL_SENTINEL]]


def test_all_filtered_writer_oom_shrinks_physical_gap_work() -> None:
    """A writer with no checkpoint rows still gets a concrete smaller cap."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        sess = make_fragment_writer_session(
            num_physical_rows=10,
            num_logical_rows=0,
            oom_budget_tracker=_tracker(),
            job_id="job-gen-780",
        )
        sess.seal()

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("gap-fill OOM"),
        ):
            assert sess.consume_ready_future(harness.write_futures[0]) is None

    assert not sess.failed
    assert sess.writer_max_rows == 5
    assert _writer_kwargs(harness, 1)["max_rows_per_batch"] == 5
    assert harness.batch_calls(1) == [[_SEAL_SENTINEL]]


def test_irreducible_writer_oom_is_bounded_without_jobtracker() -> None:
    """A one-row writer unit fails clearly after the driver-local same-range bound."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        sess = make_fragment_writer_session(
            writer_max_rows=1,
            oom_budget_tracker=_tracker(same_range_limit=1),
            job_tracker=None,
            job_id="job-gen-780",
        )
        sess.ingest_task(0, "ckpt_range-0-1", 1)
        sess.seal()

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("atomic writer OOM"),
        ):
            assert sess.consume_ready_future(harness.write_futures[0]) is None

        assert not sess.failed
        assert len(harness.actors) == 2

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("atomic writer OOM"),
        ):
            assert sess.consume_ready_future(harness.write_futures[1]) is None

    assert sess.failed
    assert isinstance(sess.failure_exc, FatalWorkerOOMError)
    assert "OOM recovery budget exceeded" in (sess.failure_reason or "")
    assert len(harness.actors) == 2, "terminal OOM must not launch another actor"

    completed = make_fragment_write_result(frag_id=7)
    manager = make_fragment_writer_manager(sessions={sess.frag_id: sess})
    manager._recorded_fragment_ids.add(completed.frag_id)
    manager._recorded_fragment_ids.add(completed.frag_id)
    manager.to_commit.append((completed.frag_id, completed.new_file, 11))
    committed_fragment_ids: list[int] = []

    def _commit_completed(
        manager_arg: FragmentWriterManager, _minimum: int, *, robust: bool = False
    ) -> None:
        del robust
        committed_fragment_ids.extend(item[0] for item in manager_arg.to_commit)
        manager_arg.to_commit.clear()

    with (
        patch.object(
            FragmentWriterManager,
            "_commit_if_n_fragments",
            autospec=True,
            side_effect=_commit_completed,
        ) as commit_fragments,
        pytest.raises(FatalWorkerOOMError, match="fragment 0"),
    ):
        manager.cleanup()
    assert commit_fragments.call_count >= 1
    assert committed_fragment_ids == [completed.frag_id]
    assert manager._recorded_fragment_ids == {completed.frag_id}


def test_stale_result_after_oom_restart_is_ignored() -> None:
    """Only the replacement future can produce the fragment record."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        sess = make_fragment_writer_session(
            oom_budget_tracker=_tracker(),
            job_id="job-gen-780",
        )
        sess.ingest_task(0, "ckpt_range-0-4", 4)
        sess.seal()
        stale_future = harness.write_futures[0]

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray.exceptions.OutOfMemoryError("writer OOM"),
        ):
            assert sess.consume_ready_future(stale_future) is None

        replacement_future = harness.write_futures[1]
        replacement_result = make_fragment_write_result(frag_id=sess.frag_id)
        with patch("geneva.runners.ray.pipeline.ray.get") as ray_get:
            assert sess.consume_ready_future(stale_future) is None
            ray_get.assert_not_called()

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            return_value=replacement_result,
        ):
            assert sess.consume_ready_future(replacement_future) is replacement_result

    assert sess.completed == 1
    assert not sess.inflight


def test_drain_recovers_from_writer_oom_and_yields_replacement_once() -> None:
    """Final cleanup's blocking drain follows the same shrinking OOM path."""
    harness = MockedRayWriterHarness()
    replacement_result = make_fragment_write_result(frag_id=0)
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.kill"),
        patch(
            "geneva.runners.ray.pipeline.ray.wait",
            side_effect=lambda pending, **_kwargs: (list(pending), []),
        ),
    ):
        sess = make_fragment_writer_session(
            oom_budget_tracker=_tracker(),
            job_id="job-gen-780",
        )
        sess.ingest_task(0, "ckpt_range-0-8", 8)
        sess.seal()

        with patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=[
                ray.exceptions.OutOfMemoryError("writer OOM during drain"),
                replacement_result,
            ],
        ):
            assert list(sess.drain()) == [replacement_result]

    assert sess.writer_max_rows == 4
    assert sess.completed == 1
    assert not sess.failed
    assert not sess.inflight
    assert len(harness.actors) == 2
    assert harness.batch_calls(1) == [[(0, "ckpt_range-0-8", 8), _SEAL_SENTINEL]]
