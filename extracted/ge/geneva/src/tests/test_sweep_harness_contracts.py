# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Contracts of the differential sweep harnesses themselves, not of geneva.

A sweep that cannot see a violation reports green forever, so the detection
machinery needs its own negative controls: the srid-off no-mutation snapshot must
notice a view moving underneath it, and the fault sweep's verdict-parity check
must refuse configurations that would compare a run against itself or against a
baseline that was never written. Both failures are invisible from the sweep's own
exit code -- that is exactly why they are pinned here.

The sweeps monkeypatch ``ray`` before importing geneva, so anything touching them
runs as a subprocess rather than in this pytest session.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_SWEEPS = Path(__file__).parent


def _run(argv: list[str], env: dict[str, str], timeout: int = 600) -> tuple:
    """Run a sweep/driver subprocess, returning ``(returncode, stdout, stderr)``."""
    r = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=timeout,
        env={**os.environ, **env},
    )
    return r.returncode, r.stdout, r.stderr


# --- srid-off no-mutation snapshot ------------------------------------------
# _mv_snapshot backs GUARD-MUTATE: after the cross-version refresh guard raises,
# the view must be unchanged. A rows-only snapshot cannot see a commit whose
# content happens to match, so the driver below moves the view's version and
# schema metadata while holding its rows fixed -- the one mutation shape a
# row-comparison misses -- and asserts the snapshot still notices.

_SNAPSHOT_DRIVER = """
import sys, tempfile
sys.path.insert(0, "@SWEEPS@")
import ray_shim
ray_shim.install()

import mv_differential_sweep as m
from geneva import connect

assert m._SRID is False, "driver must run with GENEVA_MVDIFF_SRID=off"

db = connect(tempfile.mkdtemp(prefix="snapcontract_"))
source = m._mk_source(db, "s")
mv = source.search(None).select(["id", "value"]).create_materialized_view(db, "m")
mv.refresh(_admission_check=False)

before = m._mv_snapshot(mv)

# Bump the view's version without touching a single row: a metadata-only commit.
ds = mv.to_lance()
ds.replace_schema_metadata({"sweep_contract_probe": "1"})

after = m._mv_snapshot(mv)

# The premise: rows really are identical, so a rows-only snapshot compares equal
# and every GUARD-MUTATE check built on one would be vacuous here.
assert before.rows == after.rows, "probe changed rows; it must not"
assert after.version != before.version, "probe did not bump the view version"

# The contract: the snapshot spans version and schema, so it sees the mutation.
assert before != after, "snapshot missed an identical-content view mutation"
diff = m._snap_diff(after, before)
assert "version" in diff, f"diff should name the version change, got {diff!r}"

print("SNAPSHOT-CONTRACT-OK", diff)
"""


@pytest.mark.slow
def test_mv_snapshot_detects_identical_content_mutation() -> None:
    """The srid-off snapshot spans version and schema, not just rows.

    A guard raise that still commits an identical-content version has mutated
    the view; a rows-only snapshot would pass it as untouched, making every
    GUARD-MUTATE verdict vacuous for that mutation shape.
    """
    code = _SNAPSHOT_DRIVER.replace("@SWEEPS@", str(_SWEEPS))
    rc, out, err = _run(
        [sys.executable, "-c", code], {"GENEVA_MVDIFF_SRID": "off"}, timeout=900
    )
    detail = (
        f"snapshot contract driver failed (exit {rc}).\n"
        f"--- stdout ---\n{out[-2000:]}\n--- stderr ---\n{err[-2000:]}"
    )
    assert rc == 0, detail
    assert "SNAPSHOT-CONTRACT-OK" in out, detail


# --- fault sweep verdict-parity configuration -------------------------------
# The parity check is the only thing measuring that srid-off keeps srid-on's fault
# coverage. Both rejections below are validated before the sweep runs, so these
# stay fast (no cases are executed) -- and a rejection that arrived only in the
# summary would already have cost the whole nightly leg.

_FAULT_SWEEP = _SWEEPS / "differential_fault_sweep.py"
# Smallest possible matrix: config errors are caught before any case runs, so
# these knobs only bound the damage if that ordering ever regresses.
_TINY = {
    "GENEVA_FAULTSWEEP_MAXLEN": "1",
    "GENEVA_FAULTSWEEP_FLAVORS": "backfill-skip",
    "GENEVA_FAULTSWEEP_OPS": "A",
    "SWEEP_WORKERS": "2",
}


def test_fault_sweep_rejects_self_parity_baseline(tmp_path: Path) -> None:
    """Dumping verdicts to the parity baseline's own path is a config error.

    The dump happens before the comparison, so a shared path would overwrite the
    baseline and compare the run against itself: parity is then "OK" by
    construction and measures nothing.
    """
    shared = tmp_path / "verdicts.json"
    baseline = {"meta": {"srid": "on"}, "verdicts": {"sentinel-case": "HEAL"}}
    shared.write_text(json.dumps(baseline))

    rc, out, err = _run(
        [sys.executable, str(_FAULT_SWEEP)],
        {
            **_TINY,
            "GENEVA_FAULTSWEEP_VERDICTS_OUT": str(shared),
            "GENEVA_FAULTSWEEP_COMPARE": str(shared),
        },
    )
    assert rc == 2, (
        f"expected config-error exit 2, got {rc}.\n{out[-2000:]}\n{err[-800:]}"
    )
    assert "same file" in out, f"exit reason should name the clash, got:\n{out[-2000:]}"
    # The baseline must survive: clobbering it is the harm being prevented.
    assert json.loads(shared.read_text()) == baseline, "baseline was overwritten"


def test_fault_sweep_rejects_self_parity_baseline_via_indirect_path(
    tmp_path: Path,
) -> None:
    """The same-file check resolves paths; it is not a string comparison."""
    shared = tmp_path / "verdicts.json"
    shared.write_text(json.dumps({"meta": {"srid": "on"}, "verdicts": {}}))
    indirect = tmp_path / "sub" / ".." / "verdicts.json"

    rc, out, _err = _run(
        [sys.executable, str(_FAULT_SWEEP)],
        {
            **_TINY,
            "GENEVA_FAULTSWEEP_VERDICTS_OUT": str(indirect),
            "GENEVA_FAULTSWEEP_COMPARE": str(shared),
        },
    )
    assert rc == 2, f"expected exit 2 for an aliased path, got {rc}.\n{out[-2000:]}"


def test_fault_sweep_fails_on_missing_parity_baseline(tmp_path: Path) -> None:
    """An absent baseline fails the run, before the sweep rather than after it.

    The baseline producer writes its verdicts even when it exits non-zero, so a
    missing file means it died earlier -- and an unmeasured parity check is not a
    passing one. Reporting that only in the summary would waste the whole run
    first, which for the nightly leg means a night.
    """
    rc, out, _err = _run(
        [sys.executable, str(_FAULT_SWEEP)],
        {**_TINY, "GENEVA_FAULTSWEEP_COMPARE": str(tmp_path / "absent.json")},
    )
    assert rc == 1, f"expected exit 1 for a missing baseline, got {rc}.\n{out[-2000:]}"
    assert "does not exist" in out, f"expected a clean FAIL line, got:\n{out[-2000:]}"
    assert "Traceback" not in out, "missing baseline should not raise"
    assert "=== fault sweep:" not in out, (
        "the missing baseline was reported only after sweeping; it is a config "
        f"error and must be caught before any case runs.\n{out[-2000:]}"
    )


# --- nightly reachability ---------------------------------------------------
# The srid-off legs were unreachable twice: once behind the default
# first-failure step abort, then behind `if: !cancelled()` while the preceding
# L=5 step exhausted the job timeout (a timed-out job is cancelled). Both times
# the workflow looked correct and delivered zero coverage, and nothing failed --
# a skipped step is silent. These assert the srid-off legs can actually run.

_WORKFLOWS = Path(__file__).resolve().parents[2] / ".github" / "workflows"


def _jobs(name: str) -> dict:
    yaml = pytest.importorskip("yaml")
    return yaml.safe_load((_WORKFLOWS / name).read_text())["jobs"]


def _find_step(jobs: dict, needle: str) -> tuple[str, dict, dict]:
    """Locate the one step whose `run` or `env` mentions ``needle``."""
    hits = [
        (job_name, job, step)
        for job_name, job in jobs.items()
        for step in job.get("steps", [])
        if needle in step.get("run", "")
        or needle in " ".join(f"{k}={v}" for k, v in (step.get("env") or {}).items())
    ]
    assert len(hits) == 1, f"expected exactly one step matching {needle!r}, got {hits}"
    return hits[0]


def test_mv_nightly_srid_off_leg_is_an_independent_job() -> None:
    """The mv srid-off leg cannot be skipped by the deep sweep's outcome.

    Sharing the deep sweep's job is what made it unreachable: the L=5 step ran
    into the job timeout, and a timed-out job is cancelled, which every
    conditional short of `always()` skips. Separate jobs with no `needs:` is the
    only arrangement no step-level outcome can suppress; the legs share no state,
    so nothing forces them to be co-located.
    """
    jobs = _jobs("mv-differential-nightly.yml")
    deep_job, _, _ = _find_step(jobs, "GENEVA_MVDIFF_MAXLEN=5")
    off_job, off, _step = _find_step(jobs, "GENEVA_MVDIFF_SRID=off")

    assert off_job != deep_job, (
        "the srid-off leg shares the deep sweep's job; the deep sweep hitting its "
        "job timeout would cancel the job and skip this leg"
    )
    assert not off.get("needs"), (
        f"the srid-off job declares needs={off.get('needs')!r}; a failed or "
        "cancelled dependency would skip it entirely"
    )


def test_mv_nightly_deep_sweep_timeout_is_sized_for_l5() -> None:
    """The deep sweep's job timeout must leave room for the L=5 matrix.

    The 60-minute default cancelled 30 of 30 scheduled runs at ~61 minutes, so
    the deep leg reported nothing for a month. L=5 is 95,458 cases; at the
    measured 12-worker rate that is hours, not one.
    """
    jobs = _jobs("mv-differential-nightly.yml")
    deep_job, job, _ = _find_step(jobs, "GENEVA_MVDIFF_MAXLEN=5")
    timeout = job.get("timeout-minutes")
    detail = (
        f"job {deep_job!r} allows {timeout} min for the L=5 sweep; the measured "
        "matrix needs ~3.5 h and a timeout cancels the job silently"
    )
    assert timeout is not None, detail
    assert timeout >= 300, detail


def test_fault_nightly_srid_off_leg_runs_when_srid_on_leg_is_red() -> None:
    """The fault srid-off leg survives a failing srid-on leg, and reads its dump.

    Unlike the mv nightly these two legs must share a job: the srid-off leg's
    parity baseline is the file the srid-on leg writes. That makes the step
    condition the only thing keeping the leg reachable while the srid-on leg is
    red by design, and the two paths have to actually line up.
    """
    jobs = _jobs("fault-injection-nightly.yml")
    on_job, _, on_step = _find_step(jobs, "GENEVA_FAULTSWEEP_VERDICTS_OUT=")
    off_job, _, off_step = _find_step(jobs, "GENEVA_FAULTSWEEP_SRID=off")

    assert on_job == off_job, "the parity baseline is passed via the job filesystem"
    assert "cancelled" in str(off_step.get("if", "")), (
        "the srid-off leg has no failure-tolerant condition; the srid-on leg is "
        "red by design, and the default first-failure abort would skip this leg"
    )
    assert (
        off_step["env"]["GENEVA_FAULTSWEEP_COMPARE"]
        == (on_step["env"]["GENEVA_FAULTSWEEP_VERDICTS_OUT"])
    ), "the srid-off leg compares against a file the srid-on leg does not write"
    # A leg that dumped over its own baseline would compare against itself; the
    # sweep rejects that outright, so the workflow must not wire it up.
    assert "GENEVA_FAULTSWEEP_VERDICTS_OUT" not in off_step["env"]
