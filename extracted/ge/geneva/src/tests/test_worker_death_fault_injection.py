# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Run the shim-backed worker-death scenarios as subprocesses; each exits 0 iff geneva
held its invariant (a fault at a durability boundary fails loud or leaves no silent
loss). green == correct. Scenarios whose bug is unfixed on this branch are
``xfail(strict=True)`` with the bug named, so they show as xfail (never a green pass)
and a fix surfaces as a strict XPASS. Each runs in its own process (it monkeypatches
``ray`` before importing geneva); bug/fix detail lives in ``worker_death_faults.py``.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow

# The verdict line a scenario prints when the known bug it targets is present.
_BUG_PRESENT_MARK = "FAIL (bug present"


class _BugPresentError(AssertionError):
    """The scenario ran and reported its targeted bug is present (its FAIL line).

    Distinct from a generic failure so the xfail markers below can be ``raises=
    _BugPresentError``: an INCONCLUSIVE scenario, or one that silently stopped firing (a
    renamed actor/method -> NOFIRE), exits non-zero WITHOUT the bug-present line and
    raises a plain failure instead, so it surfaces as a hard error rather than a
    masked, meaningless XFAIL.
    """


def _run_scenario(scenario: str) -> None:
    script = Path(__file__).parent / "worker_death_faults.py"
    r = subprocess.run(
        [sys.executable, str(script), scenario],
        capture_output=True,
        text=True,
        timeout=300,
        env={**os.environ},
    )
    if r.returncode == 0:
        return  # the invariant held (geneva behaved correctly)
    tail = (
        f"worker-death scenario {scenario!r} exited {r.returncode}.\n"
        f"--- stderr (last 1500 chars) ---\n{r.stderr[-1500:]}\n"
        f"--- stdout (verdict) ---\n{r.stdout[-2000:]}"
    )
    if _BUG_PRESENT_MARK in r.stdout:
        raise _BugPresentError(tail)
    # Non-zero without the bug-present line: INCONCLUSIVE, a crash, or the fault
    # silently stopped firing. Never an expected xfail -- fail hard.
    pytest.fail(tail)


# --- invariants that currently HOLD (these pass green) ----------------------


def test_resume_after_worker_death_heals() -> None:
    _run_scenario("resume-heals")


def test_short_fragment_write_fails_loud() -> None:
    # A SHORT fragment write (fewer rows than the manifest) must fail loud before
    # the short file is committed, so the table stays readable and a re-run heals
    # it -- never a corrupt false success (unreadable table behind a success
    # report).
    _run_scenario("short-fragment-write-fails-loud")


def test_checkpoint_write_loss_is_loud_and_recoverable() -> None:
    # Dropping a checkpoint write (vs the commit) fails loud and a resume heals it.
    _run_scenario("checkpoint-loss-recovers")


def test_schema_change_recomputes_the_column() -> None:
    # Re-adding a dropped column with a different UDF recomputes every row, never
    # reusing the prior UDF's checkpointed value.
    _run_scenario("schema-change-recomputes")


def test_source_change_is_recomputed_or_loud_never_silently_stale() -> None:
    # After an in-place source update, a re-backfill recomputes or fails loud, never
    # silently leaving a stale derived value (in-process this fails loud on a commit
    # conflict; the true silent-stale risk needs a concurrent mutation on real Ray).
    _run_scenario("source-change-not-silently-stale")


def test_applier_death_fails_loud_and_resume_heals() -> None:
    # Faithful actor death: killing the applier surfaces a RayActorError and drives
    # geneva's real ActorPool death path; with no skip budget the job fails loud and a
    # resume heals every row.
    _run_scenario("applier-death-fails-loud")


def test_applier_death_under_zero_skip_budget_fails_loud() -> None:
    # A worker death under skip_on_error(max_skip_count=0) must fail loud: the skip
    # budget is charged BEFORE the null checkpoint is persisted, so a zero or exceeded
    # budget raises instead of silently NULLing the dead task's rows -- and leaves no
    # orphaned null checkpoint. The scenario's second phase retries the backfill clean
    # and asserts zero NULLs (no poisoned checkpoint consumed as cached results).
    _run_scenario("applier-death-skip-budget-bypass")


def test_concurrent_append_during_backfill_resolves() -> None:
    # A deterministic concurrent-writer race: an append commits between the backfill's
    # version read and its fragment commit. geneva's conflict handling must leave every
    # pre-existing row correct and the table readable.
    _run_scenario("concurrent-append-during-backfill")


def test_fragment_write_failure_is_not_a_silent_success() -> None:
    # A failed fragment now fails the job with attribution after the healthy
    # fragments commit, instead of degrading into a success with NULL rows.
    _run_scenario("graceful-degradation")


def test_dropped_data_commit_leaves_no_durable_done_marker() -> None:
    # A dropped fragment write now fails the job, so no durable completion marker
    # lands and a resume re-dispatches instead of recording a NULL gap as DONE.
    _run_scenario("marker-after-dropped-commit")


def test_mv_refresh_does_not_report_success_while_incomplete() -> None:
    # Row-count reconciliation in the copy-table path confirms the placeholder append
    # landed every new source row; a dropped Table.add fails the refresh loud instead
    # of reporting a false success, and a later refresh re-selects and heals the gap.
    _run_scenario("mv-refresh-lost-append")


def test_repair_resume_is_not_a_silent_noop() -> None:
    # A filtered repair that dies after writing per-range checkpoints but before
    # committing now replans the fully-checkpointed fragment as a single commit
    # task on resume (reusing the checkpoints, no recompute) instead of treating
    # the stale pre-repair output data file as proof the fragment is done.
    _run_scenario("repair-resume-noop")


def test_mv_refresh_does_not_expose_placeholder_rows() -> None:
    # A projection MV refresh appends its new rows fully populated, so a reader at
    # the intermediate (post-append) version never sees NULL view columns.
    _run_scenario("mv-refresh-exposes-placeholders")


def test_mixed_view_refresh_does_not_expose_projected_placeholders() -> None:
    # A mixed view (projection + per-column UDF) appends its new rows with the
    # projected columns populated, so a reader at the intermediate (post-append)
    # version never sees NULL projected columns. The UDF column staying NULL until
    # the fill pass is acceptable and out of scope here.
    _run_scenario("mv-refresh-mixed-view-exposes-placeholders")
