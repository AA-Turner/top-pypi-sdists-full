"""Tests for geocif/ml/stage_labels.py — the one chronological stage-order
helper behind every "latest stage" pick (audit A7).

The bug it replaces: ``sort_values("Stage Name")`` / ``sorted(stage_names)``
ordered the labels as TEXT. Names start with a month abbreviation, so
``"May" > "Jul"`` and ``"Sep" > "Oct"`` — the headline forecast was shown at
the wrong month and hindcast diagnostics were scored at the wrong stage
whenever ``run_time_steps = all``.
"""
import numpy as np
import pandas as pd
import pytest

from geocif.ml.stage_labels import (
    infer_label_order,
    infer_planting_month,
    latest_stage_rows,
    sort_stage_names,
    stage_rank,
    stage_sort_key,
)

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"

# USA-maize-style reverse-cumulative (``monthly_r``) labels for a
# March-planted season: first month = as-of, second = planting.
R_STAGES = ["Mar 1-Mar 31", "Apr 1-Mar 31", "May 1-Mar 31", "Jun 1-Mar 31",
            "Jul 1-Mar 31", "Aug 1-Mar 31", "Sep 1-Mar 31", "Oct 1-Mar 31"]


def test_lexical_max_is_not_the_latest_stage():
    """The literal failure mode: alphabetical max of a March-planted season
    is "Sep ..." (S > O > M > J > A), chronological latest is "Oct ..."."""
    assert max(R_STAGES) == "Sep 1-Mar 31"
    assert sort_stage_names(R_STAGES)[-1] == "Oct 1-Mar 31"
    assert sort_stage_names(R_STAGES) == R_STAGES


def test_reverse_labels_order_across_the_year_boundary():
    """Southern-hemisphere / cross-year season (planting Oct): Jan..Mar of
    the next calendar year must come AFTER Nov/Dec."""
    names = ["Jan 1-Oct 31", "Nov 1-Oct 31", "Mar 1-Oct 31", "Dec 1-Oct 31",
             "Oct 1-Oct 31", "Feb 1-Oct 31"]
    assert sort_stage_names(names) == [
        "Oct 1-Oct 31", "Nov 1-Oct 31", "Dec 1-Oct 31",
        "Jan 1-Oct 31", "Feb 1-Oct 31", "Mar 1-Oct 31",
    ]


def test_pre_season_sorts_before_every_in_season_stage():
    # Pre-season inits form a contiguous block (Jan, Feb) -> planting = Mar.
    names = ["Jul 1-Mar 31", "Pre-Season (init Feb)", "Mar 1-Mar 31",
             "Pre-Season (init Jan)", "In-Season (init Mar)"]
    out = sort_stage_names(names)
    assert out[:3] == ["Pre-Season (init Jan)", "Pre-Season (init Feb)",
                       "In-Season (init Mar)"]
    assert out[-1] == "Jul 1-Mar 31"
    assert infer_planting_month(names) == 3  # Feb is the latest init -> Mar
    # An "(init Mar)" with March planting scores 0, the in-season
    # "Mar 1-Mar 31" also 0: the rank keeps them apart.
    assert stage_rank("In-Season (init Mar)", planting_month=3) < stage_rank(
        "Mar 1-Mar 31", planting_month=3)


def test_forward_labels_detected_and_ordered():
    """Non-``_r`` labels are calendar order and share a start month; the old
    key SHRANK as the window grew (the B-row "reversed for non-_r methods")."""
    names = ["Mar 1-Jun 30", "Mar 1-Apr 30", "Mar 1-May 31", "Mar 1-Mar 31"]
    assert infer_label_order(names) == "forward"
    assert sort_stage_names(names) == [
        "Mar 1-Mar 31", "Mar 1-Apr 30", "Mar 1-May 31", "Mar 1-Jun 30"]
    assert stage_sort_key("Mar 1-Jun 30", forward=True) == 3
    # The production convention stays the default.
    assert infer_label_order(R_STAGES) == "reverse"
    assert stage_sort_key("Jun 1-Mar 31") == 3


def test_season_normalized_labels_order_by_window_end():
    assert sort_stage_names(["10%-30%", "10%-20%", "10%-100%", "10%"]) == [
        "10%", "10%-20%", "10%-30%", "10%-100%"]
    assert sort_stage_names(["Stages 1-3", "Stage 1", "Stages 1-2"]) == [
        "Stage 1", "Stages 1-2", "Stages 1-3"]


def _frame(rows, swd=None):
    df = pd.DataFrame(rows, columns=["Region", "Harvest Year", "Stage Name", PRED])
    if swd is not None:
        df["Stage Window Display"] = swd
    return df


def test_latest_stage_rows_picks_chronological_latest_per_group():
    df = _frame([
        ("a", 2024, "Sep 1-Mar 31", 1.0),   # lexical max
        ("a", 2024, "Oct 1-Mar 31", 2.0),   # chronological latest
        ("a", 2024, "May 1-Mar 31", 3.0),
        ("a", 2023, "Jul 1-Mar 31", 4.0),   # other year: its own latest
        ("b", 2024, "Jun 1-Mar 31", 5.0),
        ("b", 2024, "Apr 1-Mar 31", 6.0),
    ])
    out = latest_stage_rows(df, by=["Region", "Harvest Year"])
    got = {(r, y): v for r, y, v in out[["Region", "Harvest Year", PRED]].itertuples(index=False)}
    assert got == {("a", 2024): 2.0, ("a", 2023): 4.0, ("b", 2024): 5.0}
    # Row order / index preserved (a filter, not a re-sort).
    assert list(out.index) == [1, 3, 4]
    # Missing key names are ignored, keep="last" collapses to one row/group.
    out2 = latest_stage_rows(df, by=["Region", "Season", "Harvest Year"], keep="last")
    assert len(out2) == 3


def test_latest_stage_rows_prefers_stage_window_display():
    """``Stage Window Display`` is calendar order whatever the method, so it
    ranks correctly even where the raw name convention is ambiguous."""
    # Forward-method names with two planting calendars in one frame: the
    # name heuristic cannot tell forward from reverse, the display can.
    df = _frame(
        [("a", 2024, "Mar 1-Apr 30", 1.0), ("a", 2024, "Mar 1-Aug 31", 2.0),
         ("b", 2024, "Apr 1-May 31", 3.0), ("b", 2024, "Apr 1-Sep 30", 4.0)],
        swd=["Mar 1-Apr 30", "Mar 1-Aug 31", "Apr 1-May 31", "Apr 1-Sep 30"],
    )
    out = latest_stage_rows(df, by=["Region", "Harvest Year"])
    assert out[PRED].tolist() == [2.0, 4.0]
    # Reverse names + display (the real DB layout): same answer either way.
    df_r = _frame(
        [("a", 2024, "Sep 1-Mar 31", 1.0), ("a", 2024, "Oct 1-Mar 31", 2.0)],
        swd=["Mar 1-Sep 30", "Mar 1-Oct 31"],
    )
    assert latest_stage_rows(df_r, by=["Region"])[PRED].tolist() == [2.0]


def test_latest_stage_rows_pre_season_and_nan_never_beat_in_season():
    df = _frame([
        ("a", 2024, "Pre-Season (init Feb)", 1.0),
        ("a", 2024, "Apr 1-Mar 31", 2.0),
        ("a", 2024, np.nan, 3.0),
        ("b", 2024, "Pre-Season (init Jan)", 4.0),   # only pre-season -> kept
        ("c", 2024, np.nan, 5.0),                      # only NaN -> kept
    ])
    out = latest_stage_rows(df, by=["Region", "Harvest Year"])
    assert out[PRED].tolist() == [2.0, 4.0, 5.0]


def test_latest_stage_rows_passthrough_without_stage_column():
    df = pd.DataFrame({"Region": ["a"], PRED: [1.0]})
    assert latest_stage_rows(df, by=["Region"]) is df
    assert latest_stage_rows(df.iloc[0:0], by=["Region"]).empty
    assert latest_stage_rows(None, by=["Region"]) is None


def _alphabetical_stage_sorts(src):
    """Line numbers of ``.sort_values("Stage Name")`` / ``.sort_values([...
    "Stage Name" ...])`` calls and key-less ``sorted(<"Stage Name" expr>)``
    calls — CODE only, comments and docstrings are not inspected."""
    import ast

    def _mentions_stage(node):
        return any(isinstance(n, ast.Constant) and n.value == "Stage Name"
                   for n in ast.walk(node))

    hits = []
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "sort_values":
            args = list(node.args) + [kw.value for kw in node.keywords if kw.arg == "by"]
            if any(_mentions_stage(a) for a in args):
                hits.append(node.lineno)
        elif (isinstance(f, ast.Name) and f.id == "sorted" and node.args
              and not any(kw.arg == "key" for kw in node.keywords)
              and _mentions_stage(node.args[0])):
            hits.append(node.lineno)
    return sorted(set(hits))  # ast.walk is breadth-first, not line order


def test_old_alphabetical_pattern_is_gone_from_owned_modules():
    """Structural guard: no owned module may fall back to the text sort."""
    import inspect

    from geocif import compare_forecasts, fdw_export, report_lite, yield_outlook
    from geocif.viz import aggregation, diagnostics

    for mod in (yield_outlook, fdw_export, report_lite, compare_forecasts,
                aggregation, diagnostics):
        hits = _alphabetical_stage_sorts(inspect.getsource(mod))
        assert not hits, f"{mod.__name__}: alphabetical Stage Name sort at lines {hits}"
    # The guard itself recognises the pattern it is meant to catch.
    assert _alphabetical_stage_sorts(
        'x = df.sort_values("Stage Name").groupby("Region").last()\n'
        'y = sorted(d["Stage Name"].unique())[-1]\n'
        'z = sorted(names, key=f)\n'
    ) == [1, 2]
