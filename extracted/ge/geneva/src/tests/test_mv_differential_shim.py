# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Run the in-process (no-cluster) multi-flavor differential sweep as a subprocess
and assert no new-signature divergence beyond the known bugs (GEN-619 / GEN-611).

The sweep monkeypatches ``ray`` before importing geneva, so it must run in its own
process (not this pytest session). It needs no Ray cluster, so this is fast and is
*not* marked ``ray`` -- any NEW signature fails CI.

Depth and parallelism are kept modest so this stays inside a standard CI runner's
RAM: peak memory is roughly ``SWEEP_WORKERS * 0.5 GB`` (each worker re-imports
geneva/ray/lance). The deep L=5 sweep runs in the nightly workflow on a big runner.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow


def test_mv_differential_shim_sweep() -> None:
    script = Path(__file__).parent / "mv_differential_sweep.py"
    r = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=1200,
        # L=3 over 6 flavors (~717 cases); 4 workers ~= 2 GB peak -- safe on a
        # standard CI runner. Per-case tempdir cleanup keeps memory flat with depth.
        # SRID pinned to "on": the script rejects anything else, and the pytest
        # axis value "both" (test_matview_differential) may sit in ambient env.
        env={
            **os.environ,
            "GENEVA_MVDIFF_MAXLEN": "3",
            "SWEEP_WORKERS": "4",
            "GENEVA_MVDIFF_SRID": "on",
        },
    )
    # The sweep exits 0 iff every divergence is a known bug. On failure, lead with
    # the (large, noisy) logs and END with the sweep summary + NEW-signature lines,
    # so the diagnosis is the last thing shown rather than buried under log spam.
    assert r.returncode == 0, (
        f"shim differential sweep found a new-signature divergence (exit "
        f"{r.returncode}).\n"
        f"--- sweep logs (stderr, last 1500 chars) ---\n{r.stderr[-1500:]}\n"
        f"--- sweep result (stdout: summary + NEW signatures) ---\n{r.stdout[-3000:]}"
    )
