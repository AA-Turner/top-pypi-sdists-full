# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Deterministic, row_index-keyed failure injection for the row-wise stages.

Lets a run reproduce a controlled fraction of per-row failures (download GET /
normalize / phash) WITHOUT real faults, so the resume/repair paths can be
exercised on demand. Pure and deterministic — the same ``(row_index, rate, seed)``
always selects the same rows (same splitmix64 stream the rest of the workbench
uses, mirroring ``dedupe_inject``). Selection is independent of the real work, so a
row is failed before its IO/CPU is attempted.

Because selection is deterministic, re-running a stage with the SAME rate+seed
re-injects the SAME failures. To repair, re-run with ``--inject-failure-rate 0``
targeting the failed rows (download: ``--repair-errors``; normalize/phash:
``--reuse-existing`` / ``--where "<col>.error != ''"``).
"""

from __future__ import annotations

from loadtest.azure_scale_bench.image_distribution import MASK64, row_hash

# Captured into each row-wise stage's error/output when a row is injected-failed.
INJECTED_ERROR = "injected failure"

# Fixed salt, distinct from dedupe_inject's selection/group/base/flip salts, so the
# failure-selection stream is decorrelated from duplicate injection.
_FAIL_SALT = 0x6666_6666_6666_6666


def should_fail(row_index: int, *, rate: float, seed: int) -> bool:
    """Return True if ``row_index`` is a deterministically-injected failure.

    ``rate`` is the target failure fraction in [0, 1]; ``seed`` varies the selection
    between runs. ``rate <= 0`` never fails; ``rate >= 1`` always fails.
    """
    if rate <= 0.0:
        return False
    if rate >= 1.0:
        return True
    h = row_hash((row_index ^ seed ^ _FAIL_SALT) & MASK64)
    return (h / 2.0**64) < rate
