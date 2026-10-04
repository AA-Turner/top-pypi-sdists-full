"""Regression tests: yield_outlook's fallback summary must read the folders the
run's Geocif objects wrote their fallback CSVs to.

Geocif._record_fallback writes ``<P>/ml/analysis/<MMMM_DD_YYYY>/fallbacks/
fallback_<pid>.csv`` (its dir_analysis, New York date at construction), but
run() summarized ``dir_outlook.parent`` = ``<P>/ml/analysis/<MMMM_DD_YYYY_HHhmm>``,
which never has a fallbacks/ folder, so the summary always came up empty.
"""
import ast
from pathlib import Path

import arrow as ar
import pandas as pd

from geocif import yield_outlook as yo

_YIELD_OUTLOOK = Path(__file__).resolve().parent.parent / "geocif" / "yield_outlook.py"


def _write_fallbacks(date_dir, pid, n_rows):
    path = date_dir / "fallbacks" / f"fallback_{pid}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({
        "timestamp": ["2026-10-03T14:10:00-04:00"] * n_rows,
        "pid": [pid] * n_rows,
        "category": ["pearson_summary_missing"] * n_rows,
        "model": ["catboost"] * n_rows,
        "country": ["kenya"] * n_rows,
        "crop": ["maize"] * n_rows,
        "forecast_season": [2026] * n_rows,
        "stage_name": [""] * n_rows,
    }).to_csv(path, index=False)


def test_fallback_summary_reads_date_folder_not_stamp_folder(tmp_path, monkeypatch):
    # 2026-10-03: G1, introduced in fecbdf0 (0.4.699) — summarized the outlook
    # stamp folder instead of the Geocif date folder.
    proj = tmp_path / "outputs" / "kenya_proj"
    stamp_dir = proj / "ml" / "analysis" / "October_03_2026_14h05"
    (stamp_dir / "outlook").mkdir(parents=True)
    date_dir = proj / "ml" / "analysis" / "October_03_2026"
    _write_fallbacks(date_dir, pid=101, n_rows=2)
    _write_fallbacks(date_dir, pid=102, n_rows=1)

    monkeypatch.setattr(yo.ar, "utcnow", lambda: ar.Arrow(2026, 10, 3, 20, 0, tzinfo="UTC"))
    started = ar.Arrow(2026, 10, 3, 14, 5, tzinfo="America/New_York")
    dirs = yo._run_analysis_dirs(proj, started)
    assert dirs == [date_dir]

    yo._summarize_fallbacks(stamp_dir, dirs)
    summary = pd.read_csv(stamp_dir / "fallbacks_summary.csv")
    assert len(summary) == 3
    counts = pd.read_csv(stamp_dir / "fallbacks_summary_counts.csv")
    assert counts["n_events"].sum() == 3


def test_fallback_summary_spans_midnight_date_folders(tmp_path, monkeypatch):
    # 2026-10-03: G1, introduced in fecbdf0 (0.4.699) — a run crossing midnight
    # (New York) writes fallbacks into two date folders; both must be read.
    proj = tmp_path / "outputs" / "kenya_proj"
    stamp_dir = proj / "ml" / "analysis" / "October_02_2026_23h50"
    (stamp_dir / "outlook").mkdir(parents=True)
    day1 = proj / "ml" / "analysis" / "October_02_2026"
    day2 = proj / "ml" / "analysis" / "October_03_2026"
    _write_fallbacks(day1, pid=101, n_rows=2)
    _write_fallbacks(day2, pid=202, n_rows=3)

    # 04:20 UTC on Oct 3 is 00:20 in New York.
    monkeypatch.setattr(yo.ar, "utcnow", lambda: ar.Arrow(2026, 10, 3, 4, 20, tzinfo="UTC"))
    started = ar.Arrow(2026, 10, 2, 23, 50, tzinfo="America/New_York")
    dirs = yo._run_analysis_dirs(proj, started)
    assert dirs == [day2, day1]

    yo._summarize_fallbacks(stamp_dir, dirs)
    assert len(pd.read_csv(stamp_dir / "fallbacks_summary.csv")) == 5


def test_outlook_run_passes_geocif_analysis_dirs_not_stamp_dir():
    # 2026-10-03: G1/G2, introduced in fecbdf0 (0.4.699) — run() must hand the
    # Geocif date folders to the fallback summary and the PDF report, and bind
    # _ml_started before the reuse_db branch (no UnboundLocalError on reuse_db).
    tree = ast.parse(_YIELD_OUTLOOK.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run")

    reuse_idx = next(
        i for i, n in enumerate(fn.body)
        if isinstance(n, ast.If) and "reuse_db" in ast.unparse(n.test)
    )
    bound_before = {
        t.id for n in fn.body[:reuse_idx] if isinstance(n, ast.Assign)
        for t in n.targets if isinstance(t, ast.Name)
    }
    assert "_ml_started" in bound_before

    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    summary_calls = [ast.unparse(c) for c in calls if c.func.id == "_summarize_fallbacks"]
    assert summary_calls == ["_summarize_fallbacks(dir_outlook.parent, _analysis_dirs)"]
    dirs_calls = [ast.unparse(c) for c in calls if c.func.id == "_run_analysis_dirs"]
    assert dirs_calls == ["_run_analysis_dirs(_dir_output_proj, _ml_started)"]
    report_kwargs = [
        {k.arg: ast.unparse(k.value) for k in c.keywords}
        for c in calls if c.func.id == "generate_report"
    ]
    assert report_kwargs == [{"analysis_dirs": "_analysis_dirs"}]
