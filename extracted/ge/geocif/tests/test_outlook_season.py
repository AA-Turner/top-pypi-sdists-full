"""Regression tests for per-season yield-outlook handling.

Multi-season countries (e.g. Somalia: Season 1 = Gu, Season 2 = Deyr) store an
integer ``Season`` column in the outlook DB. ``_compute_outlook_index`` must
then return one row per (Country, Region, Season); single-season / older DBs
that lack the column must keep the original one-row-per-region behavior
byte-for-byte. ``_season_iter`` drives the per-season map fan-out and must be a
no-op (single, untokenized pass) whenever there is no Season column OR exactly
one season, so filenames + maps stay identical to the pre-season pipeline.

The full ``geocif.yield_outlook`` import pulls heavy geo deps (pygeoutil,
cartopy) that only exist on the cluster, so the two target functions are
extracted from source via ``ast`` and exec'd against pandas/numpy. This lets
the logic be tested anywhere. A behavioral variant guarded by ``importorskip``
runs the real functions where the geo stack is installed.
"""
import ast
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_SRC_PATH = Path(__file__).resolve().parents[1] / "geocif" / "yield_outlook.py"
_SRC = _SRC_PATH.read_text(encoding="utf-8")
_TREE = ast.parse(_SRC)

_PRED = "Predicted Yield (tn per ha)"


def _extract(*names):
    """Exec just the named top-level functions with pandas/numpy in scope."""
    ns = {"pd": pd, "np": np}
    for name in names:
        node = next(
            n for n in _TREE.body
            if isinstance(n, ast.FunctionDef) and n.name == name
        )
        exec(ast.get_source_segment(_SRC, node), ns)
    return tuple(ns[n] for n in names)


_compute_outlook_index, _season_iter = _extract(
    "_compute_outlook_index", "_season_iter"
)


def _two_season_df():
    """2 regions x 2 seasons x 4 years; each (region, season) has a distinct
    level so current_predicted differs across seasons within a region."""
    rows = []
    for region, base in (("A", 2.0), ("B", 5.0)):
        for season in (1, 2):
            for yr in (2021, 2022, 2023, 2024):
                val = base + (0.5 if season == 2 else 0.0) + (0.3 if yr == 2024 else 0.0)
                rows.append({
                    "Country": "somalia", "Region": region, "Season": season,
                    "Harvest Year": yr, "Stage Name": "Grain", _PRED: val,
                })
    df = pd.DataFrame(rows)
    df["Season"] = df["Season"].astype("Int64")
    return df


class TestComputeOutlookIndexSeason:
    def test_multi_season_two_rows_per_region_distinct(self):
        out = _compute_outlook_index(
            _two_season_df(), current_year=2024, n_years=10, aggregation="mean"
        )
        assert "Season" in out.columns
        # 2 regions x 2 seasons = 4 rows; exactly 2 per region
        assert len(out) == 4
        assert (out.groupby("Region").size() == 2).all()
        # current_predicted differs between the two seasons of each region
        for region in ("A", "B"):
            vals = out[out["Region"] == region].sort_values("Season")[
                "current_predicted"
            ].tolist()
            assert vals[0] != vals[1], f"seasons not distinct for {region}: {vals}"
        # merge key stays region-only (no season token)
        assert set(out["Country Region"]) == {"somalia a", "somalia b"}

    def test_single_season_column_present(self):
        df1 = _two_season_df()
        df1 = df1[df1["Season"] == 1].copy()
        out = _compute_outlook_index(df1, 2024, 10, "mean")
        assert len(out) == 2
        assert (out.groupby("Region").size() == 1).all()

    def test_no_season_column_legacy_unchanged(self):
        df0 = _two_season_df().drop(columns=["Season"])
        df0 = df0.drop_duplicates(subset=["Region", "Harvest Year"])
        out = _compute_outlook_index(df0, 2024, 10, "mean")
        assert "Season" not in out.columns, "legacy path must not add a Season column"
        assert len(out) == 2
        assert (out.groupby("Region").size() == 1).all()


class TestSeasonIter:
    def test_multi_season_tokens_and_labels(self):
        out = _compute_outlook_index(_two_season_df(), 2024, 10, "mean")
        seen = [(s, tok, lbl) for (s, _sub, tok, lbl) in _season_iter(out)]
        assert {tok for _s, tok, _l in seen} == {"_s1", "_s2"}
        assert all(lbl.endswith(("Season 1", "Season 2")) for _s, _t, lbl in seen)
        # each sub-frame is one season -> one row per region (no 2-rows/region)
        for _s, sub, _tok, _lbl in _season_iter(out):
            assert (sub.groupby("Region").size() == 1).all()

    def test_single_season_no_token(self):
        df1 = _two_season_df()
        df1 = df1[df1["Season"] == 1].copy()
        out = _compute_outlook_index(df1, 2024, 10, "mean")
        seen = list(_season_iter(out))
        assert len(seen) == 1
        assert seen[0][2] == "" and seen[0][3] == "", "single season must emit no token"

    def test_no_season_column_single_none_pass(self):
        df0 = _two_season_df().drop(columns=["Season"]).drop_duplicates(
            subset=["Region", "Harvest Year"]
        )
        out = _compute_outlook_index(df0, 2024, 10, "mean")
        seen = list(_season_iter(out))
        assert len(seen) == 1
        s, sub, tok, lbl = seen[0]
        assert s is None and tok == "" and lbl == ""
        assert sub is out  # same frame passed straight through


class TestBehavioralWhereGeoDepsPresent:
    """Runs the real functions when the cluster geo stack is importable."""

    def test_real_module_matches(self):
        yo = pytest.importorskip("geocif.yield_outlook")
        out = yo._compute_outlook_index(_two_season_df(), 2024, 10, "mean")
        assert "Season" in out.columns and len(out) == 4
        assert {tok for _s, _sub, tok, _l in yo._season_iter(out)} == {"_s1", "_s2"}
