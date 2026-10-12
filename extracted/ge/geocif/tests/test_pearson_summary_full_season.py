"""CID-vs-yield Pearson summary: per-region full season, coverage guard, row alignment.

Found on Afghanistan poppy (2026-10-11): the picker took one longest-chain
column per CID, which only the zones with the longest calendar have (3 of 7
poppy zones were plotted); ENSO CIDs with n = 2 ranked first at r = +-1 (the
ranking feeds auto_/top10_ CID selection); and the pairwise |rho| matrix
concatenated series by position, pairing different region-years whenever two
CIDs had different missing rows.
"""

import numpy as np
import pandas as pd

from geocif import utils
from geocif.viz.diagnostics import cid_vs_yield_scatters

TARGET = "Yield (tn per ha)"
FULL_A, FULL_B = "Aug 1-Oct 31", "Aug 1-Nov 30"  # monthly_r: 11 and 10 stages


def _frame(seed=0):
    rng = np.random.RandomState(seed)
    rows = []
    for region in ("A", "B"):
        for year in range(2001, 2021):
            esi = rng.normal(40, 8)
            rows.append({"Region": region, "Harvest Year": year, "esi": esi,
                         TARGET: 20 + 0.5 * esi + rng.normal(0, 3)})
    df = pd.DataFrame(rows)
    a, b = df["Region"] == "A", df["Region"] == "B"
    # Region A's season starts in October (11 stages), B's in November (10).
    df[f"MIN_ESI4WK {FULL_A}"] = np.where(a, df["esi"], np.nan)
    df[f"MIN_ESI4WK {FULL_B}"] = df["esi"] + np.where(a, 100.0, 0.0)  # A must not use this
    # An ENSO-like CID observed in two region-years only, perfectly "correlated".
    enso = pd.Series(np.nan, index=df.index)
    enso.iloc[[0, 1]] = df[TARGET].iloc[[0, 1]]
    df[f"ONI {FULL_A}"] = enso
    return df.drop(columns="esi")


def test_each_region_uses_its_own_full_season():
    df = _frame()
    values, chains = utils.full_season_cid_values(df, method="monthly_r")["MIN_ESI4WK"]
    a, b = df["Region"] == "A", df["Region"] == "B"
    assert chains == [10, 11]
    pd.testing.assert_series_equal(values[a], df.loc[a, f"MIN_ESI4WK {FULL_A}"], check_names=False)
    pd.testing.assert_series_equal(values[b], df.loc[b, f"MIN_ESI4WK {FULL_B}"], check_names=False)


def test_cid_with_too_few_region_years_is_not_ranked():
    pearson_df, corr = utils.compute_pearson_summary(_frame(), TARGET, method="monthly_r")
    assert "ONI" not in pearson_df.index
    assert pearson_df.loc["MIN_ESI4WK", "n"] == 40  # both regions counted
    assert "ONI" not in corr.index


def test_mutual_correlation_pairs_the_same_rows():
    df = _frame()
    # A second CID equal to the first except for its first five rows missing:
    # on the rows they share they are identical, so |rho| must be exactly 1.
    df[f"COPY {FULL_A}"] = df[f"MIN_ESI4WK {FULL_A}"]
    df[f"COPY {FULL_B}"] = df[f"MIN_ESI4WK {FULL_B}"]
    df.loc[df.index[:5], [f"COPY {FULL_A}", f"COPY {FULL_B}"]] = np.nan
    _, corr = utils.compute_pearson_summary(df, TARGET, method="monthly_r")
    assert np.isclose(corr.loc["MIN_ESI4WK", "COPY"], 1.0)


def test_scatters_cover_every_region_and_drop_low_n_from_summary(tmp_path):
    df = _frame()
    n = cid_vs_yield_scatters(df, TARGET, tmp_path, "afghanistan", "poppy",
                              method="monthly_r", yield_units="kg/ha")
    assert n >= 1
    csvs = tmp_path / "afghanistan" / "poppy" / "csvs"
    per_cid = pd.read_csv(csvs / "MIN_ESI4WK.csv")
    assert set(per_cid["Region"]) == {"A", "B"}
    summary = pd.read_csv(csvs / "pearson_summary.csv")
    assert "ONI" not in set(summary["cid"])
    assert (tmp_path / "afghanistan" / "poppy" / "MIN_ESI4WK_by_region.png").exists()
