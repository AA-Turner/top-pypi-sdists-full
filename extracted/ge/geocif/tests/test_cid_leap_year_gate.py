"""Regression tests for the percentile-indices Feb-29 gate.

The Feb-29 drop in `compute_indices` is correct for percentile / spell
indices (whose per-DOY thresholds require a 365-day baseline) but
**breaks** non-percentile indices with `slice_mode=("season", ...)` when
the season spans Feb 29 — icclim returns NaN for the incomplete
leap-year season and the downstream `fillna(0)` turns it into a false 0
(symptom: TXn = 0.0 for every Zimbabwe maize leap-year harvest).

History: the unconditional drop was introduced 2026-04-13 in commit
9752a94 (0.4.366, "Fix leap year shape mismatch in percentile CID
indices"). The gate restoring correct behaviour landed in 0.4.690.
"""

from geocif.cid.indices import _PERCENTILE_INDICES


# Percentile thresholds + spell-duration indices that MUST keep the Feb-29
# drop (their per-DOY thresholds need a clean 365-day baseline).
_MUST_INCLUDE = frozenset({
    "TG10p", "TN10p", "TX10p",
    "TG90p", "TN90p", "TX90p",
    "R75p", "R75pTOT", "R95p", "R95pTOT", "R99p", "R99pTOT",
    "CSDI", "WSDI",
})

# Extreme / sum / count / range indices that MUST NOT be in the gate set.
# Inclusion would resurrect the leap-year bug for any season window
# spanning Feb 29.
_MUST_EXCLUDE = frozenset({
    "TXn", "TNn", "TXx", "TNx",
    "TG", "TN", "TX",
    "GD4", "HD17",
    "DTR", "ETR", "vDTR",
    "FD", "ID", "SU", "TR", "CFD", "CSU",
    "PRCPTOT", "RR1", "SDII", "CWD", "CDD",
    "R10mm", "R20mm", "RX1day", "RX5day",
    "CD", "CW",
})


def test_percentile_indices_set_includes_all_percentile_families():
    missing = _MUST_INCLUDE - _PERCENTILE_INDICES
    assert not missing, (
        f"Percentile / spell-duration indices missing from gate "
        f"(Feb 29 will NOT be dropped, percentile threshold corrupted): {sorted(missing)}"
    )


def test_percentile_indices_set_excludes_non_percentile_families():
    leaking = _MUST_EXCLUDE & _PERCENTILE_INDICES
    assert not leaking, (
        f"Non-percentile indices erroneously in gate "
        f"(Feb 29 WILL be dropped, leap-year seasons → NaN → fillna(0) = 0): {sorted(leaking)}"
    )


def test_txn_not_in_percentile_gate():
    # Pinned because TXn is the specific index that surfaced this regression
    # in zimbabwe/maize (Nov-Apr seasons, all 8 admin-1 regions, every leap
    # year 1984..2020 read 0.0 instead of ~25 C).
    assert "TXn" not in _PERCENTILE_INDICES
