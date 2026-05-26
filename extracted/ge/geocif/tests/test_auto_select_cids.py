"""Regression tests for the at-least-X-above-Y CID selection schema.

See plan in `~/.claude/plans/replicated-sniffing-candle.md` for the
algorithm (dedup-first relaxation up to ρ_max, then |r| floor down
to ``auto_abs_r_floor``). Shipped in 0.4.692.
"""

import numpy as np
import pandas as pd

from geocif.utils import auto_select_cids, greedy_dedup_by_mutual_corr


def _make_inputs(abs_r_by_cid: dict[str, float], rho_pairs: dict[tuple[str, str], float]):
    """Build (pearson_df, corr) from explicit |r| and pairwise |ρ| specs.

    Diagonal ρ is 1.0; missing pairs default to 0 (uncorrelated).
    """
    cids = list(abs_r_by_cid.keys())
    pearson_df = pd.DataFrame(
        {
            "abs_r": [abs_r_by_cid[c] for c in cids],
            "pearson_r": [abs_r_by_cid[c] for c in cids],
        },
        index=cids,
    )
    pearson_df.index.name = "cid"
    corr = pd.DataFrame(0.0, index=cids, columns=cids)
    for c in cids:
        corr.at[c, c] = 1.0
    for (a, b), v in rho_pairs.items():
        corr.at[a, b] = v
        corr.at[b, a] = v
    return pearson_df, corr


def test_strict_pass_when_constraints_met():
    abs_r = {f"C{i}": 0.5 - i * 0.01 for i in range(10)}
    pearson_df, corr = _make_inputs(abs_r, {})
    selected, log = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    assert len(selected) == 10
    assert log == [("none", 0.90, 0.30, 10)]


def test_dedup_relax_when_too_few_after_strict_prune():
    # 8 strong CIDs, but 3 of them are tight twins of C0 at |ρ|=0.92.
    # At ρ=0.90 only 5 survive (C0, C1, C2, C3, C4) — three twins pruned.
    # Relax dedup → ρ=0.93 admits one twin, ρ=0.96 admits another, ρ=0.99 the third.
    abs_r = {f"C{i}": 0.5 - i * 0.01 for i in range(5)}
    abs_r.update({f"T{i}": 0.48 - i * 0.01 for i in range(3)})
    rho = {("T0", "C0"): 0.92, ("T1", "C0"): 0.93, ("T2", "C0"): 0.95}
    pearson_df, corr = _make_inputs(abs_r, rho)
    selected, log = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    assert len(selected) == 8, f"expected 8 after dedup relax, got {len(selected)}: {selected}"
    assert any(s[0] == "dedup" for s in log), f"no dedup relax step in {log}"


def test_abs_r_relax_when_dedup_exhausted():
    # All CIDs are independent (corr identity), only 5 have |r| > 0.30,
    # the next 4 are at 0.20. Y must slide from 0.30 → 0.25 → 0.20 to admit
    # them; dedup relax doesn't help (no twins to recover).
    abs_r = {**{f"S{i}": 0.45 - i * 0.02 for i in range(5)},
             **{f"W{i}": 0.20 for i in range(4)}}
    pearson_df, corr = _make_inputs(abs_r, {})
    selected, log = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    assert len(selected) >= 8
    assert any(s[0] == "abs_r" for s in log), f"no abs_r relax step in {log}"
    # The terminating step must report a |r| floor below 0.30.
    assert log[-1][2] < 0.30


def test_floor_returns_whatever_survives():
    # No CID has |r| > 0.10 — relaxation cannot help; the schema must
    # return the empty (or short) set tagged with step="floor".
    abs_r = {f"N{i}": 0.05 for i in range(6)}
    pearson_df, corr = _make_inputs(abs_r, {})
    selected, log = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    assert log[-1][0] == "floor", f"expected 'floor' at end of {log}"
    assert len(selected) == 0


def test_deterministic_same_input_same_output():
    abs_r = {f"C{i}": 0.5 - i * 0.01 for i in range(5)}
    abs_r.update({f"T{i}": 0.48 for i in range(3)})
    rho = {("T0", "C0"): 0.92, ("T1", "C0"): 0.93, ("T2", "C0"): 0.95}
    pearson_df, corr = _make_inputs(abs_r, rho)
    a, log_a = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    b, log_b = auto_select_cids(
        pearson_df, corr,
        min_count=8, min_abs_r=0.30,
        dedup_threshold=0.90, dedup_max=0.99,
        abs_r_floor=0.10, abs_r_step=0.05,
    )
    assert a == b
    assert log_a == log_b


def test_greedy_dedup_helper_preserves_rank_order():
    # Independence test for the shared helper: highest-rank CID always
    # survives over its conflicting twins, regardless of order in corr.
    corr = pd.DataFrame(
        [[1.0, 0.95, 0.92],
         [0.95, 1.0, 0.91],
         [0.92, 0.91, 1.0]],
        index=["A", "B", "C"],
        columns=["A", "B", "C"],
    )
    kept, pruned = greedy_dedup_by_mutual_corr(["A", "B", "C"], corr, 0.90)
    assert kept == ["A"]
    assert pruned == {"B": ("A", 0.95), "C": ("A", 0.92)}
