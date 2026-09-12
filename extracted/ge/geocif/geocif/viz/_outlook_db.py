"""One loader for the outlook DBs that both viz consumers read.

``geocif/viz/cone.py`` and ``geocif/viz/leadtime.py`` each grew their own copy
of the same sqlite read (ro-URI + PRAGMA column probe + ``Experiment Name =
'outlook'`` filter + rename/coerce). The fork was not cosmetic:

* Only cone's copy de-duplicated upsert duplicates. The writer's key includes
  the wall-clock ``Time``, so re-running an outlook into an existing DB
  appends a SECOND copy of every logical row rather than replacing it —
  which meant leadtime silently DOUBLE-WEIGHTED every region-year in its
  national lead-time skill scores on any re-run DB.
* Cone's own dedup sorted the string ``Date``/``Time`` columns
  lexicographically, but geocif writes them month-name-first
  (``Date='September_06_2026'``, ``Time='September-06-2026 11:31:05'`` —
  built in ``geocif/geocif.py`` with arrow's ``MMMM_DD_YYYY`` /
  ``MMMM-DD-YYYY HH:mm:ss``). Alphabetical is not chronological across
  months ('December' < 'February') or even across years within one month
  ('September_06_2026' < 'September_10_2025'), so ``keep='last'`` could keep
  a STALE row.

This module is the single corrected implementation; the former copies are now
thin wrappers around :func:`load_outlook`. The stage-coverage and
common-sample helpers shared by the two ``prepare()`` functions live here too,
so a fix in one product cannot silently miss the other again.
"""

import sqlite3

import numpy as np
import pandas as pd

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"
LO = "lower CI"
HI = "upper CI"

# The writer's formats (geocif/geocif.py: self.today at line ~83, `now` in
# _create_base_dataframe): month NAME first, so these strings must be PARSED
# before any ordering decision — never sorted raw.
DATE_FORMAT = "%B_%d_%Y"            # arrow MMMM_DD_YYYY
TIME_FORMAT = "%B-%d-%Y %H:%M:%S"   # arrow MMMM-DD-YYYY HH:mm:ss


def _written_at(df):
    """Wall-clock write timestamp per row: parsed Time, falling back to Date."""
    ts = pd.to_datetime(df["Time"], format=TIME_FORMAT, errors="coerce")
    return ts.fillna(pd.to_datetime(df["Date"], format=DATE_FORMAT,
                                    errors="coerce"))


def load_outlook(db_path, table, *, model=None, extra_columns=(),
                 require_obs=False, validate_ci=False):
    """Read one crop table's outlook rows with the shared cleanup applied.

    Parameters
    ----------
    model : str or None
        Filter to one model when given (the cone draws exactly one); ``None``
        keeps every model (leadtime compares them on one axis).
    extra_columns : tuple of str
        Optional numeric DB columns to carry along, e.g. ``Area (ha)`` or the
        CI bounds. Columns absent from the table are backfilled with NaN so
        callers never have to probe for them.
    require_obs : bool
        Drop rows without an observed yield. Skill scoring needs the truth on
        every row (leadtime); the cone must NOT set this because the live
        forecast year has no observed value yet and would silently vanish.
    validate_ci : bool
        Fail loudly on inconsistent intervals / mixed alphas (cone). The
        tabpfn quantile path repairs monotonicity, so a violation here means
        the DB is not what we think.
    """
    cols = ['"Model"', '"Region"', '"Harvest Year"', '"Stage Name"',
            f'"{PRED}"', f'"{OBS}"']
    # Date/Time are always fetched, whatever the caller asked for: the
    # de-duplication below needs them to decide which of two writes is fresh.
    optional = ("Stage Window Display",) + tuple(extra_columns) + ("Date", "Time")
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        present = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        for opt in optional:
            if opt in present:
                cols.append(f'"{opt}"')
        query = (f'SELECT {",".join(cols)} FROM "{table}" '
                 f"WHERE \"Experiment Name\" = 'outlook'")
        if model is not None:
            df = pd.read_sql(f'{query} AND "Model" = ?', con, params=(model,))
        else:
            df = pd.read_sql(query, con)
    finally:
        con.close()
    for opt in optional:
        if opt not in df.columns:
            df[opt] = np.nan
    df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                            "Stage Window Display": "swd"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    for c in (OBS, PRED) + tuple(extra_columns):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    subset = [OBS, PRED, "year"] if require_obs else [PRED, "year"]
    df = df.dropna(subset=subset)
    df = df[(df[OBS].isna()) | (df[OBS] > 0)].copy()

    # De-duplicate (Model, Region, year, stage). The writer's upsert key
    # includes the wall-clock Time, so re-running an outlook into an existing
    # DB appends a SECOND copy of every logical row rather than replacing it.
    # Duplicates double-weight a region in every aggregate and make the
    # cone's full-pool calibration filters reject every year — silently.
    # Model is part of the key because leadtime loads every model at once; a
    # model-free key would "dedup" cubist against tabpfn.
    key = ["Model", "Region", "year", "stage"]
    if df.duplicated(key).any():
        n_dup = int(df.duplicated(key).sum())
        # Sort on the PARSED write time, never the raw strings: Date/Time are
        # month-name-first, so a lexicographic sort orders 'December' before
        # 'February' and keep='last' would keep the stale copy. The stable
        # sort keeps insertion order among ties, so equal (or missing)
        # timestamps still resolve to the last-inserted copy.
        df = (df.assign(_ts=_written_at(df))
              .sort_values("_ts", na_position="first", kind="stable")
              .drop_duplicates(key, keep="last")
              .drop(columns="_ts"))
        print(f"{table}: dropped {n_dup} duplicate (Model, Region, year, stage) "
              f"row(s); kept the most recently written copy of each")
    df = df.copy()

    if validate_ci:
        # Each bound is checked on its own — a row with a populated lower CI
        # and a NULL upper one must not slip past because the pair test needs
        # both. Guarded on column presence so a caller that never asked for
        # the CI columns cannot trip on the check.
        if LO in df.columns and HI in df.columns:
            bad = df[((df[LO].notna()) & (df[LO] > df[PRED]))
                     | ((df[HI].notna()) & (df[PRED] > df[HI]))]
            if len(bad):
                raise ValueError(
                    f"{table}: {len(bad)} row(s) violate lower CI <= pred <= "
                    f"upper CI "
                    f"(first: {bad.iloc[0][['Region', 'year', 'stage']].to_dict()})"
                )
        if "alpha" in df.columns:
            alphas = df.loc[df["alpha"].notna(), "alpha"].unique()
            if len(alphas) > 1 or (len(alphas) == 1 and abs(alphas[0] - 0.2) > 1e-9):
                raise ValueError(
                    f"{table}: expected a single alpha of 0.2, got {alphas}")
    return df


def drop_sparse_stages(df, min_region_frac):
    """Drop stages covering fewer than ``min_region_frac`` of the regions.

    Such a stage describes a different pool of regions, not an earlier
    forecast — on usa_admin1, maize ``Mar 1-Mar 31`` exists solely because
    Missouri's calendar starts in March (1/10 states). Keeping it would let
    the common-sample rule silently shrink the WHOLE product to that stage's
    subset. Returns ``(frame, dropped)`` with ``dropped`` mapping each removed
    stage to its region count; raises when nothing survives, because
    proceeding with zero stages is never what was meant.
    """
    n_regions = df["Region"].nunique()
    per_stage = df.groupby("stage")["Region"].nunique()
    keep = per_stage[per_stage >= min_region_frac * n_regions].index.tolist()
    dropped = {s: int(per_stage[s]) for s in per_stage.index if s not in keep}
    if not keep:
        raise ValueError(
            f"no stage covers {min_region_frac:.0%} of the {n_regions} region(s) "
            f"— per-stage coverage was {dict(per_stage)}. Lower min_region_frac "
            f"to keep the earlier stages at the cost of a smaller region pool."
        )
    return df[df["stage"].isin(keep)].copy(), dropped


def common_pairs_across_models(df, value_col=PRED):
    """(Region, year) pairs covered in EVERY stage by EVERY model.

    The old leadtime code derived this sample from ONE probe model
    (``df['Model'].iloc[0]``): a model missing a (region, year) the probe had
    was then scored on a smaller sample than everyone else, and the
    model-comparison curves silently compared unlike numbers. The
    intersection makes the sample identical for all models by construction —
    a model missing rows shrinks the sample for everyone, visibly.

    Returns ``(pairs, per_model)``: ``pairs`` is a MultiIndex (``None`` when
    the frame holds no models at all) and ``per_model`` maps each model to
    its OWN complete-pair count, so an empty intersection's error message can
    say who collapsed it.
    """
    stages = sorted(df["stage"].unique())
    pairs, per_model = None, {}
    for model, g in df.groupby("Model"):
        piv = (g.pivot_table(index=["Region", "year"], columns="stage",
                             values=value_col, aggfunc="first")
               # reindex: a stage a model lacks ENTIRELY would otherwise not
               # appear as a pivot column at all, and dropna() would wave the
               # model through as if it covered the stage.
               .reindex(columns=stages))
        idx = piv.dropna().index
        per_model[str(model)] = int(len(idx))
        pairs = idx if pairs is None else pairs.intersection(idx)
    return pairs, per_model
