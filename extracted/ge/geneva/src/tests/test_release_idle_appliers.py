# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Backfill releases idle applier actors during a long tail (GEN-1018).

With ``JOB__RELEASE_IDLE_APPLIERS`` on, appliers that finish their last task
while one slow task still runs are killed, once idle for
``JOB__RELEASE_IDLE_APPLIERS_AFTER_S``, instead of idling (and holding their
GPU) until the job ends. Each backfill here has one slow row whose UDF call
waits until the processes of every other applier that ran a row have exited,
then records what it saw. That only happens if the driver released those
appliers mid-job; with the setting off they stay alive until the slow task
returns. With a long grace, late work reuses an idle applier instead.
"""

from __future__ import annotations

import contextlib
import json
import logging
import uuid
from typing import TYPE_CHECKING, Literal

import pyarrow as pa
import pytest
import ray

import geneva
from geneva import udf
from geneva.debug.error_store import ExceptionMatcher, skip_on_error
from geneva.runners.ray._mgr import ray_cluster

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from geneva.db import Connection
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)

ROWS = 6
SLOW_ROW = 3
CONCURRENCY = 3
# Quick rows sleep so the work spreads over several appliers.
QUICK_ROW_S = 2.0
# Idle grace for the release tests: short, but not 0, so they cover an
# applier going once its grace ends, at the driver's next 30s poll.
TAIL_GRACE_S = 1
# A grace no test outlasts, so idle appliers stay for late work.
WARM_GRACE_S = 600
# Upper bound on the slow row's wait for the other appliers to exit: one
# 30s driver poll after the grace, plus generous slack.
RELEASE_WAIT_S = 90.0

CrashMode = Literal["never", "once", "always"]


@pytest.fixture(scope="module")
def release_ray_context(request: pytest.FixtureRequest) -> Iterator[None]:
    """Local Ray whose workers, including the backfill driver, enable release.

    The driver task resolves ``JobConfig`` in its own Ray worker, so the
    settings ride in the job's runtime env rather than this process's
    environment (which would also leak into other tests' cached config).
    The idle grace defaults to ``TAIL_GRACE_S``; a test can pass another
    through indirect parametrization, which starts a separate cluster.
    """
    grace_s = getattr(request, "param", TAIL_GRACE_S)
    with contextlib.suppress(Exception):
        ray.shutdown()
    with ray_cluster(
        local=True,
        log_to_driver=True,
        logging_level=logging.INFO,
        extra_env={
            "JOB__RELEASE_IDLE_APPLIERS": "true",
            "JOB__RELEASE_IDLE_APPLIERS_AFTER_S": str(grace_s),
        },
    ):
        yield


def _tail_udf(
    marker_dir: Path,
    *,
    crash: CrashMode = "never",
    on_error: list[ExceptionMatcher] | None = None,
    wait_for_release: bool = True,
    every_applier_runs_a_row: bool = False,
) -> UDF:
    """A UDF whose ``SLOW_ROW`` call waits for the other appliers to exit.

    Every call touches ``pid-<pid>``; quick rows touch ``done-<row>``. The
    slow row's first attempt waits for all quick rows, then (unless
    ``wait_for_release`` is off) for every other applier process that ran a
    row to exit, and writes ``slow.json``. With ``crash`` set it then kills
    its own worker, so the driver must run replacement work after the
    release. Retries touch ``replacement-<pid>`` and crash again only when
    ``crash == "always"``. With ``every_applier_runs_a_row``, quick rows
    first wait until ``CONCURRENCY`` appliers have started a row, so with
    one task per applier no applier takes two.
    """
    root = str(marker_dir)
    slow_row = SLOW_ROW
    quick_rows = ROWS - 1
    quick_row_s = QUICK_ROW_S
    release_wait_s = RELEASE_WAIT_S
    wait_for_exit = wait_for_release
    wait_for_appliers = CONCURRENCY if every_applier_runs_a_row else 0

    @udf(data_type=pa.int64(), version=uuid.uuid4().hex, on_error=on_error)
    def tail(x: int) -> int:
        import json as _json
        import os
        import time
        from pathlib import Path as _Path

        import geneva as worker_geneva

        markers = _Path(root)
        pid = os.getpid()
        (markers / f"pid-{pid}").touch()
        if x != slow_row:
            started_by = time.monotonic() + release_wait_s
            while (
                time.monotonic() < started_by
                and len(list(markers.glob("pid-*"))) < wait_for_appliers
            ):
                time.sleep(0.1)
            time.sleep(quick_row_s)
            (markers / f"done-{x}").touch()
            return x * 10

        crashed = markers / "crashed"
        if crashed.exists():
            (markers / f"replacement-{pid}").touch()
            if crash == "always":
                os._exit(137)
            return x * 10

        def alive(other: int) -> bool:
            # A killed actor's worker may linger as a zombie until reaped.
            try:
                import psutil
            except ImportError:
                try:
                    os.kill(other, 0)
                except ProcessLookupError:
                    return False
                return True
            try:
                return psutil.Process(other).status() != psutil.STATUS_ZOMBIE
            except psutil.NoSuchProcess:
                return False

        deadline = time.monotonic() + release_wait_s
        while (
            time.monotonic() < deadline
            and len(list(markers.glob("done-*"))) < quick_rows
        ):
            time.sleep(0.2)
        ran_pids = {int(path.name.split("-", 1)[1]) for path in markers.glob("pid-*")}
        others = ran_pids - {pid}
        while (
            wait_for_exit
            and time.monotonic() < deadline
            and any(alive(o) for o in others)
        ):
            time.sleep(0.2)
        (markers / "slow.json").write_text(
            _json.dumps(
                {
                    "pid": pid,
                    "done": len(list(markers.glob("done-*"))),
                    "others": sorted(others),
                    "alive": sorted(o for o in others if alive(o)),
                    "geneva": worker_geneva.__file__,
                }
            )
        )
        if crash != "never":
            crashed.touch()
            os._exit(137)
        return x * 10

    return tail


def _create_table(db: Connection, *, one_row_fragments: bool) -> str:
    """Create a ``ROWS``-row table, either one fragment or one per row."""
    name = f"tail_{uuid.uuid4().hex[:8]}"
    rows = pa.table({"x": pa.array(range(ROWS), type=pa.int64())})
    if not one_row_fragments:
        db.create_table(name, rows)
        return name
    tbl = db.create_table(name, rows.slice(0, 1))
    for i in range(1, ROWS):
        tbl.add(rows.slice(i, 1))
    return name


def _column_values(db: Connection, name: str) -> dict[int, int | None]:
    values: dict[int, int | None] = {}
    for batch in db.open_table(name).to_batches():
        xs = batch.column("x").to_pylist()
        values.update(zip(xs, batch.column("y").to_pylist(), strict=True))
    return values


def _job_metrics(db: Connection, job_id: str) -> dict[str, int]:
    return {m.name: m.n for m in db.get_job(job_id).metrics or []}


def _assert_released_during_tail(marker_dir: Path) -> dict:
    report = json.loads((marker_dir / "slow.json").read_text())
    _LOG.info("slow-row report: %s", report)
    assert report["done"] == ROWS - 1
    # Guards against a vacuous pass: other appliers ran rows.
    assert report["others"], "every quick row ran on the slow row's applier"
    assert report["alive"] == [], (
        "appliers with no work left were still alive while the slow task ran"
    )
    # Workers import the same geneva as this process (not another checkout).
    assert report["geneva"] == geneva.__file__
    return report


@pytest.mark.ray
@pytest.mark.timeout(300)
@pytest.mark.parametrize(
    "one_row_fragments", [True, False], ids=["direct-writes", "checkpoint-writes"]
)
def test_idle_appliers_released_while_last_task_runs(
    release_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
    one_row_fragments: bool,
) -> None:
    """Other appliers exit before the slow last task finishes; output is
    correct whether released appliers wrote fragments directly or via
    checkpoints the writer assembles."""
    marker_dir = tmp_path / "markers"
    marker_dir.mkdir()
    db = geneva.connect(str(tmp_path / "db"))
    name = _create_table(db, one_row_fragments=one_row_fragments)
    tbl = db.open_table(name)
    tbl.add_columns({"y": _tail_udf(marker_dir)})

    result = tbl.backfill(
        "y",
        concurrency=CONCURRENCY,
        task_size=1,
        _admission_check=False,
    )

    assert result.status == "DONE"
    _assert_released_during_tail(marker_dir)
    assert _column_values(db, name) == {x: x * 10 for x in range(ROWS)}
    metrics = _job_metrics(db, result.job_id)
    # Each start counts once and each release or shutdown kill uncounts once.
    assert metrics.get("workers") == 0
    if one_row_fragments:
        assert metrics.get("direct_fragment_writes") == ROWS
    else:
        assert metrics.get("checkpoint_fragment_writes") == 1


@pytest.mark.ray
@pytest.mark.timeout(300)
@pytest.mark.parametrize(
    ("crash", "on_error", "expected_slow_value"),
    [
        ("once", None, SLOW_ROW * 10),
        ("always", skip_on_error(), None),
    ],
    ids=["retry", "skip-bisect"],
)
def test_late_replacement_work_runs_after_release(
    release_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
    crash: CrashMode,
    on_error: list[ExceptionMatcher] | None,
    expected_slow_value: int | None,
) -> None:
    """The slow task's worker dies after the other appliers were released.
    Its replacement work (a retry, or bisected halves) restarts appliers and
    the job still completes with the right output."""
    marker_dir = tmp_path / "markers"
    marker_dir.mkdir()
    db = geneva.connect(str(tmp_path / "db"))
    name = _create_table(db, one_row_fragments=False)
    tbl = db.open_table(name)
    tbl.add_columns({"y": _tail_udf(marker_dir, crash=crash, on_error=on_error)})

    # Two-row tasks: the slow task also holds row SLOW_ROW - 1, so a skip
    # policy bisects it into two replacements.
    result = tbl.backfill(
        "y",
        concurrency=CONCURRENCY,
        task_size=2,
        _admission_check=False,
    )

    assert result.status == "DONE"
    report = _assert_released_during_tail(marker_dir)
    replacement_pids = {
        int(path.name.split("-", 1)[1]) for path in marker_dir.glob("replacement-*")
    }
    assert replacement_pids, "no replacement work ran for the slow row"
    assert report["pid"] not in replacement_pids
    expected = {x: x * 10 for x in range(ROWS)}
    expected[SLOW_ROW] = expected_slow_value
    assert _column_values(db, name) == expected


# Last in the module: its own grace needs its own cluster, and pytest starts
# that only once the tests above have run on the default one.
@pytest.mark.ray
@pytest.mark.timeout(300)
@pytest.mark.parametrize("release_ray_context", [WARM_GRACE_S], indirect=True)
def test_late_retry_within_the_grace_reuses_a_warm_applier(
    release_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
) -> None:
    """With a long idle grace, appliers that finished their tasks stay while
    the slow task runs. When its worker dies, the retry runs on one of those
    warm appliers instead of a newly started one."""
    marker_dir = tmp_path / "markers"
    marker_dir.mkdir()
    db = geneva.connect(str(tmp_path / "db"))
    name = _create_table(db, one_row_fragments=False)
    tbl = db.open_table(name)
    tbl.add_columns(
        {
            "y": _tail_udf(
                marker_dir,
                crash="once",
                wait_for_release=False,
                every_applier_runs_a_row=True,
            )
        }
    )

    # One two-row task per applier; the slow task holds row SLOW_ROW - 1 too.
    result = tbl.backfill(
        "y",
        concurrency=CONCURRENCY,
        task_size=2,
        _admission_check=False,
    )

    assert result.status == "DONE"
    report = json.loads((marker_dir / "slow.json").read_text())
    _LOG.info("slow-row report: %s", report)
    assert report["done"] == ROWS - 1
    assert len(report["others"]) == CONCURRENCY - 1
    # Nothing was released while the slow task ran.
    assert report["alive"] == report["others"]
    replacement_pids = {
        int(path.name.split("-", 1)[1]) for path in marker_dir.glob("replacement-*")
    }
    assert len(replacement_pids) == 1, replacement_pids
    assert replacement_pids <= set(report["others"]), (
        "the retry ran on a new applier instead of a warm one"
    )
    assert _column_values(db, name) == {x: x * 10 for x in range(ROWS)}
