"""National progression plots must show how many regions back each stage.

Stage windows are not modelled over the same regions: a window only exists
for a region once that region's own season has started. nsp sorghum's "April"
window is Texas-only (22 of 81 counties, Texas being the sole state planting
in April), so its MAPE sits far below every later stage purely because it is
a different, smaller sample. Without the count on the axis that reads as
skill that decays as the season progresses, which is backwards.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from geocif.yield_outlook import _plot_national_progression

STAGES = ["April", "April-May", "April-June"]


def _frame():
    """April covers 2 regions; the later stages cover 5."""
    rows = []
    for stage in STAGES:
        regions = ["r1", "r2"] if stage == "April" else [f"r{i}" for i in range(1, 6)]
        for region in regions:
            for year in (2020, 2021):
                rows.append({
                    "Stage Name": stage,
                    "Region": region,
                    "Country": "united_states_of_america",
                    "Harvest Year": year,
                    "MAPE": 10.0 if stage == "April" else 25.0,
                    "Observed Yield (tn per ha)": 3.0,
                    "Predicted Yield (tn per ha)": 3.3,
                })
    return pd.DataFrame(rows)


def test_plot_is_written(tmp_path):
    _plot_national_progression(
        _frame(), STAGES, "MAPE", "MAPE (%)", "test",
        tmp_path, "progression.png", has_area=False,
    )
    out = tmp_path / "progression.png"
    assert out.exists() and out.stat().st_size > 0


def test_tick_labels_carry_region_counts(tmp_path, monkeypatch):
    captured = {}
    orig = plt.Axes.set_xticklabels

    def spy(self, labels, *a, **kw):
        captured["labels"] = [str(t) for t in labels]
        return orig(self, labels, *a, **kw)

    monkeypatch.setattr(plt.Axes, "set_xticklabels", spy)
    _plot_national_progression(
        _frame(), STAGES, "MAPE", "MAPE (%)", "test",
        tmp_path, "progression.png", has_area=False,
    )

    labels = captured["labels"]
    assert len(labels) == len(STAGES), labels
    # The small-sample stage must be visibly distinguishable from the others.
    assert "(n=2)" in labels[0], labels
    assert "(n=5)" in labels[1] and "(n=5)" in labels[2], labels
    # The stage name itself must survive alongside the count.
    assert "April" in labels[0]


def test_counts_reflect_excluded_regions(tmp_path, monkeypatch):
    """MAPE>100 regions are dropped from the line, so the count must drop too."""
    captured = {}
    orig = plt.Axes.set_xticklabels
    monkeypatch.setattr(
        plt.Axes, "set_xticklabels",
        lambda self, labels, *a, **kw: (
            captured.__setitem__("labels", [str(t) for t in labels]),
            orig(self, labels, *a, **kw),
        )[1],
    )
    df = _frame()
    # r5 is a wild region in every stage it appears in -> excluded entirely.
    df.loc[df.Region == "r5", "MAPE"] = 500.0
    _plot_national_progression(
        df, STAGES, "MAPE", "MAPE (%)", "test",
        tmp_path, "progression.png", has_area=False,
    )
    labels = captured["labels"]
    assert "(n=2)" in labels[0], labels
    assert "(n=4)" in labels[1], labels
