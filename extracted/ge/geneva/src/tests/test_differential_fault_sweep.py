# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Run differential_fault_sweep.py as a subprocess at L=1 and assert it exits 0.

A passing run has only HEAL / NOFIRE / KNOWN_STALE verdicts; a non-zero exit means some
fault produced a FALSE_SUCCESS (the job reported DONE while rows were missing/stale),
left the table silently diverged from the oracle, or left it CORRUPT/STUCK, and the
sweep summary names every failing case. Runs as a subprocess because the sweep
monkeypatches ``ray`` before importing geneva.

Every sweep fault is a failure a durable write can actually exhibit (a real storage
error, a lost write, or a faithful worker death -- no fabricated partial/short writes),
so every finding is a defensible bug. Red until the write-completeness fixes land.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Red by design until the write-completeness fixes land (it asserts the sweep is all
# green), so it runs in the nightly workflow, not the per-PR gate.
pytestmark = [pytest.mark.slow, pytest.mark.nightly]


def test_differential_fault_sweep_heals_or_fails_loud() -> None:
    script = Path(__file__).parent / "differential_fault_sweep.py"
    r = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=3600,
        # L=1 over 6 flavors x faithful faults (~480 cases); 4 workers ~= 1.5 GB peak.
        # The nightly workflow runs the deeper sweep (L=3) via make test-fault-sweep.
        env={**os.environ, "GENEVA_FAULTSWEEP_MAXLEN": "1", "SWEEP_WORKERS": "4"},
    )
    assert r.returncode == 0, (
        f"fault sweep found {r.returncode}+ robustness failure(s) (exit "
        f"{r.returncode}): a fault left the table CORRUPT/STUCK (loud) or DIVERGED "
        f"(silent) instead of healing. See the FAIL summary below.\n"
        f"--- sweep logs (stderr, last 1500 chars) ---\n{r.stderr[-1500:]}\n"
        f"--- sweep result (stdout: summary + failing cases) ---\n{r.stdout[-3000:]}"
    )
