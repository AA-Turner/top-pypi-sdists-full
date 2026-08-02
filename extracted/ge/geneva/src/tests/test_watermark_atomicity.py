# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Run the shim-backed MV-refresh watermark-atomicity scenarios as subprocesses; each
exits 0 iff geneva held its invariant. green == correct.

The MV refresh records its ``last_refreshed`` watermark by a write that is NOT atomic
with the data commit (it lands client-side after the refresh job returns), so a dropped
data commit can leave the watermark advanced past rows the MV never durably landed. The
first scenario proves that inflated-watermark state is reachable; the other two prove it
does NOT cause silent data loss -- a forward refresh re-detects and re-adds the missing
rows (new-row detection is destination-state-driven, not watermark-driven), and a
backward refresh keyed on the bogus watermark deletes no valid rows (deletion is keyed
on actual source-row presence). The non-atomic watermark is therefore benign / self
repairing; these scenarios are regression guards against that property regressing into
real loss. Each runs in its own process (it monkeypatches ``ray`` before importing
geneva); detail lives in ``watermark_atomicity_faults.py``.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow


def _run_scenario(scenario: str) -> None:
    script = Path(__file__).parent / "watermark_atomicity_faults.py"
    r = subprocess.run(
        [sys.executable, str(script), scenario],
        capture_output=True,
        text=True,
        timeout=300,
        env={**os.environ},
    )
    assert r.returncode == 0, (
        f"watermark-atomicity scenario {scenario!r} did not hold its invariant "
        f"(exit {r.returncode}).\n"
        f"--- stderr (last 1500 chars) ---\n{r.stderr[-1500:]}\n"
        f"--- stdout (verdict) ---\n{r.stdout[-2000:]}"
    )


def test_lost_append_advances_watermark_is_reachable() -> None:
    # Precondition: a dropped placeholder append leaves the MV incomplete yet the
    # refresh reports success and the watermark advances past the lost rows.
    _run_scenario("lost-append-advances-watermark")


def test_inflated_watermark_forward_refresh_heals() -> None:
    # A forward refresh re-detects the missing source fragments and re-adds every row
    # despite the inflated watermark -- no silent gap.
    _run_scenario("inflated-watermark-forward-heals")


def test_inflated_watermark_backward_refresh_does_not_misdelete() -> None:
    # A backward (point-in-time) refresh against the inflated watermark deletes no valid
    # rows -- deletion is keyed on actual source-row presence, not the watermark value.
    _run_scenario("inflated-watermark-no-misdelete")
