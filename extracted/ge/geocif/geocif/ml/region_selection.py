"""Promote a fraction of the FORECAST year's regions into the training set.

Motivation: the standard LOOCV split holds out the whole forecast year
(``geocif.py:_prepare_train_test_split``), so no region of that year is ever
seen during training. In reality some districts report yields early. This
module answers "if we knew the current year's yield for ~5% of regions, how
much would the rest improve, and does it matter WHICH 5%?".

**These runs are a research UPPER BOUND, not a deployable forecast.** The
selector may pick regions using the very year being forecast (``ga`` mode), so
the resulting skill is optimistic by construction. Label it as such wherever it
is reported.

Two invariants make the comparison honest, and both live in
:func:`apply_region_promotion`:

1. Promoted rows are tagged with ``neighbor_leakage.LEAK_COLUMN`` so every
   downstream statistic that must not see them can filter them out (geocif
   exposes ``_df_train_leakfree()`` for exactly this).
2. Promoted regions are **removed from the test set in the same step**. They
   are in training; scoring them would be self-congratulatory. Every arm —
   including the ``none`` baseline — must therefore be scored on the same
   held-out subset, which is what makes the arms comparable.

Selector modes:
  ``none``     no promotion (current pipeline behaviour, bit-for-bit)
  ``random``   uniformly random subset, reproducible from a seed
  ``explicit`` a caller-supplied region list (how the GA feeds a candidate in)
"""

from __future__ import annotations

import logging
import math
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd

from .neighbor_leakage import LEAK_COLUMN

VALID_MODES = ("none", "random", "explicit")


def leakfree(df: Optional[pd.DataFrame]):
    """Rows of ``df`` that were NOT promoted from the forecast year.

    A free function rather than a method so it works on any frame and on the
    lightweight stubs the baseline tests build — the baseline code paths are
    exercised with ``types.SimpleNamespace``, which has no methods.

    Returns ``df`` unchanged when nothing was promoted (no ``LEAK_COLUMN``), so
    the normal pipeline is bit-for-bit unaffected and this is safe to call
    unconditionally at every hazard site.
    """
    if df is None or LEAK_COLUMN not in getattr(df, "columns", []):
        return df
    return df[df[LEAK_COLUMN].isna()]


def n_to_promote(n_regions: int, fraction: float) -> int:
    """How many regions a fraction corresponds to.

    Rounds to nearest, then clamps to ``[0, n_regions - 1]``: promoting *every*
    region would leave nothing to score, so at least one region always stays
    held out. A positive fraction over a non-empty region set always promotes
    at least one region — otherwise a 5% request on 10 regions would silently
    round to zero and the run would look like the ``none`` arm.
    """
    if n_regions <= 1 or fraction <= 0:
        return 0
    k = int(round(float(fraction) * n_regions))
    k = max(1, k)
    return min(k, n_regions - 1)


def select_regions(
    candidate_regions: Sequence[str],
    fraction: float,
    mode: str = "none",
    explicit: Optional[Iterable[str]] = None,
    seed: int = 0,
) -> list:
    """Choose which forecast-year regions to promote into training.

    ``candidate_regions`` must already be restricted to regions whose forecast
    year yield is actually known — a real-time forecast has none, and promoting
    a NaN-target row would teach the model nothing while still shrinking the
    scored set.
    """
    mode = (mode or "none").strip().lower()
    if mode not in VALID_MODES:
        raise ValueError(f"forecast_year_selector must be one of {VALID_MODES}, got {mode!r}")
    cands = [str(r) for r in candidate_regions]
    if mode == "none" or not cands:
        return []

    if mode == "explicit":
        chosen = [r for r in map(str, explicit or []) if r in set(cands)]
        return sorted(chosen)

    k = n_to_promote(len(cands), fraction)
    if k <= 0:
        return []
    rng = np.random.default_rng(int(seed))
    idx = rng.choice(len(cands), size=k, replace=False)
    return sorted(cands[i] for i in idx)


def apply_region_promotion(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    df_full: pd.DataFrame,
    target_year: int,
    target_col: str,
    fraction: float,
    mode: str = "none",
    explicit: Optional[Iterable[str]] = None,
    seed: int = 0,
    region_col: str = "Region",
    year_col: str = "Harvest Year",
    logger: Optional[logging.Logger] = None,
):
    """Promote forecast-year regions from test into train.

    Returns ``(df_train, df_test, promoted_regions)``. A no-op returning the
    inputs unchanged when ``mode='none'``, nothing is selected, or no candidate
    region has a known yield at ``target_year`` (real-time forecast).
    """
    if (mode or "none").strip().lower() == "none":
        return df_train, df_test, []
    if df_test is None or df_test.empty or region_col not in df_test.columns:
        return df_train, df_test, []

    # Only regions whose forecast-year yield is actually known can be promoted.
    known = df_full[
        (df_full[year_col] == target_year) & df_full[target_col].notna()
    ][region_col].astype(str).unique()
    test_regions = df_test[region_col].astype(str).unique()
    candidates = sorted(set(test_regions) & set(known))
    if not candidates:
        if logger is not None:
            logger.info(
                f"  region_promotion: no known {target_col} at year={target_year} "
                f"among the {len(test_regions)} test region(s) — real-time "
                f"forecast, skipping promotion."
            )
        return df_train, df_test, []

    promoted = select_regions(candidates, fraction, mode=mode,
                              explicit=explicit, seed=seed)
    if not promoted:
        return df_train, df_test, []

    promo = set(promoted)
    rows = df_full[
        df_full[region_col].astype(str).isin(promo)
        & (df_full[year_col] == target_year)
        & df_full[target_col].notna()
    ].copy()
    if rows.empty:
        return df_train, df_test, []

    rows[LEAK_COLUMN] = int(target_year)
    if LEAK_COLUMN not in df_train.columns:
        df_train = df_train.assign(**{LEAK_COLUMN: pd.NA})
    df_train = pd.concat([df_train, rows], ignore_index=True)

    # Keep the two frames' schemas aligned. `_get_common_columns` derives the
    # per-region column whitelist from df_train and `_extract_region_subset`
    # then applies it to BOTH frames, so a column present only on df_train
    # raises KeyError("['__leaked_from_year__'] not in index"). Test rows were
    # by definition never promoted, so NA is the correct value.
    if LEAK_COLUMN not in df_test.columns:
        df_test = df_test.assign(**{LEAK_COLUMN: pd.NA})

    # THE honest-metrics step: a promoted region is in training, so it must not
    # be scored. Dropping here (rather than filtering at report time) means
    # every downstream consumer — DB rows, CSVs, plots — is automatically
    # consistent, and no metric can accidentally include a region the model saw.
    df_test = df_test[~df_test[region_col].astype(str).isin(promo)].copy()

    if logger is not None:
        logger.info(
            f"  region_promotion[{mode}]: promoted {len(promoted)} of "
            f"{len(candidates)} candidate region(s) ({fraction:.1%} requested) "
            f"into training at year={target_year}; {len(df_test)} test row(s) "
            f"remain scored. UPPER-BOUND RUN — not an operational forecast."
        )
    return df_train, df_test, promoted
