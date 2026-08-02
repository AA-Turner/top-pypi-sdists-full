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


def test_concurrent_append_during_backfill_resolves() -> None:
    # A deterministic concurrent-writer race: an append commits between the backfill's
    # version read and its fragment commit. geneva's conflict handling must leave every
    # pre-existing row correct and the table readable.
    _run_scenario("concurrent-append-during-backfill")


# --- invariants currently VIOLATED by a known, not-yet-fixed bug ------------
# xfail(strict): each asserts the CORRECT behavior, so it stays xfailed while the bug
# is live and turns into a strict XPASS (hard failure) the moment a fix lands -- forcing
# the marker off. Reasons name the bug in plain English (ticket refs live in the PR).


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a stranded fragment (writer death swallowed to success) lands a durable "
    "completion marker, so the agent records the job DONE and never re-dispatches -- "
    "the NULL gap is persistent",
)
def test_dropped_data_commit_leaves_no_durable_done_marker() -> None:
    _run_scenario("marker-after-dropped-commit")


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a lost append makes the refresh report success while the MV is incomplete "
    "(transient -- a later refresh heals it, but the success report is still false)",
)
def test_mv_refresh_does_not_report_success_while_incomplete() -> None:
    _run_scenario("mv-refresh-lost-append")


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a healthy refresh exposes intermediate placeholder rows with NULL view "
    "columns and no read-side signal to exclude them (the __is_set gate is dead)",
)
def test_mv_refresh_does_not_expose_placeholder_rows() -> None:
    _run_scenario("mv-refresh-exposes-placeholders")


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a fragment-write failure is swallowed into a graceful-degradation success "
    "with that fragment's rows NULL; pending the fail-loud cleanup fix",
)
def test_fragment_write_failure_is_not_a_silent_success() -> None:
    _run_scenario("graceful-degradation")


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a filtered repair that dies after writing per-range checkpoints but before "
    "committing silently no-ops on a clean resume: the planner sees full checkpoint "
    "coverage plus the pre-existing output data file and skips the fragment as done, "
    "leaving the target rows at their stale pre-repair values",
)
def test_repair_resume_is_not_a_silent_noop() -> None:
    _run_scenario("repair-resume-noop")


@pytest.mark.xfail(
    strict=True,
    raises=_BugPresentError,
    reason="a worker death under skip_on_error(max_skip_count=0) silently NULLs the "
    "dead task's rows and reports success, bypassing the zero skip budget",
)
def test_applier_death_under_zero_skip_budget_fails_loud() -> None:
    _run_scenario("applier-death-skip-budget-bypass")
