"""Per-region error scatters must name only extremes, not every region.

At admin_2 scale the old code annotated every row of the per-model panel — a
Kenya county run put ~260 overlapping names on each of the 4 figures, which
hid the outliers the plot exists to surface. Only the worst-error regions
(plus the largest-x ones) are labelled now; every region is still plotted.
"""
from pathlib import Path

import pandas as pd

from geocif import yield_outlook as yo

SRC = Path(yo.__file__)


def _select(sub, metric, xcol):
    """Mirror of the label-selection rule in the scatter block."""
    lab = sub.nlargest(yo._SCATTER_LABEL_N, metric)
    if yo._SCATTER_LABEL_N_X:
        lab = pd.concat([lab, sub.nlargest(yo._SCATTER_LABEL_N_X, xcol)])
    return lab.drop_duplicates(subset=["Region"])


def _frame(n=260):
    return pd.DataFrame({
        "Region": [f"r{i:03d}" for i in range(n)],
        "RMSE": [i / 100.0 for i in range(n)],
        "area_pct_of_country": [(n - i) / 100.0 for i in range(n)],
    })


def test_label_budget_is_small():
    assert 0 < yo._SCATTER_LABEL_N <= 15, "label budget must stay readable"
    assert 0 <= yo._SCATTER_LABEL_N_X <= 5


def test_only_a_handful_labelled_out_of_many_regions():
    df = _frame(260)
    lab = _select(df, "RMSE", "area_pct_of_country")
    assert len(lab) <= yo._SCATTER_LABEL_N + yo._SCATTER_LABEL_N_X
    assert len(lab) < 15, f"still labelling too many: {len(lab)}"


def test_worst_error_regions_are_labelled():
    df = _frame(260)
    lab = _select(df, "RMSE", "area_pct_of_country")
    worst = df.nlargest(yo._SCATTER_LABEL_N, "RMSE")["Region"].tolist()
    assert set(worst).issubset(set(lab["Region"])), "must name the worst errors"


def test_largest_x_regions_are_labelled():
    """A huge region with unremarkable error should still be identifiable."""
    df = _frame(260)
    lab = _select(df, "RMSE", "area_pct_of_country")
    big = df.nlargest(yo._SCATTER_LABEL_N_X, "area_pct_of_country")["Region"].tolist()
    assert set(big).issubset(set(lab["Region"]))


def test_no_duplicate_labels():
    """A region extreme on BOTH axes must not be annotated twice."""
    df = pd.DataFrame({
        "Region": ["a", "b", "c", "d"],
        "RMSE": [9.0, 1.0, 2.0, 3.0],
        "area_pct_of_country": [9.0, 1.0, 2.0, 3.0],  # 'a' tops both
    })
    lab = _select(df, "RMSE", "area_pct_of_country")
    assert lab["Region"].is_unique


def test_small_region_count_unaffected():
    """Fewer regions than the budget -> all still labelled."""
    df = _frame(5)
    lab = _select(df, "RMSE", "area_pct_of_country")
    assert set(lab["Region"]) == set(df["Region"])


def test_scatter_block_does_not_annotate_every_row():
    """Guard the call site itself, not just the rule."""
    src = SRC.read_text(encoding="utf-8")
    i = src.index("_fname = f\"region_error_")
    block = src[i:i + 4000]
    assert "_lab.iterrows()" in block, "must iterate the trimmed label set"
    assert "_sub.iterrows()" not in block, "must not annotate every region"


# ---------------------------------------------------------------------------
# log-axis rule (added with the labelling fix; same figure family)
# ---------------------------------------------------------------------------

def test_log_scale_on_for_heavy_tailed_mape():
    """Kenya-like MAPE: bulk ~25%, junk-yield outliers to 8000%."""
    vals = [25.0] * 258 + [6000.0, 8000.0]
    assert yo._log_scale_appropriate(vals)


def test_log_scale_off_for_narrow_rmse():
    vals = [0.2 + 0.005 * i for i in range(260)]  # ~0.2..1.5
    assert not yo._log_scale_appropriate(vals)


def test_log_scale_off_when_zeros_present():
    """Share axes contain exact zeros — log would silently drop points."""
    vals = [0.0] + [25.0] * 100 + [8000.0]
    assert not yo._log_scale_appropriate(vals)


def test_log_scale_off_for_few_points():
    assert not yo._log_scale_appropriate([1.0, 1000.0])


def test_log_scale_ignores_nan_but_respects_data():
    import numpy as np
    vals = [float("nan")] * 5 + [25.0] * 100 + [8000.0]
    assert yo._log_scale_appropriate(vals)


def test_region_error_block_wires_log_rule():
    src = SRC.read_text(encoding="utf-8")
    i = src.index("_fname = f\"region_error_")
    block = src[i:i + 6000]
    assert "_log_scale_appropriate(_df_area[_metric]" in block
    assert 'set_yscale("log")' in block
