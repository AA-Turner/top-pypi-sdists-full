"""Flat, join-ready prediction CSV from the GeoCIF results database.

The results DB is the system of record, but it is not a deliverable: the
predictions live in one table per ``{country}_{crop}``, the stage column is an
internal window label, and the region is a composite NAME rather than an id
anyone can join on. Every hand-off so far has been a bespoke SQL + pandas
snippet, which is how the same export ends up subtly different each time.

This module is the one implementation. It emits exactly the columns that are
NOT already in the boundary shapefile, keyed by the shapefile's own id column
(``id_col`` in the geobase section, e.g. ``num_ID``), so the recipient joins
once and gets every name, code and geometry from the shapefile itself::

    year, lead, stage_month_name, <id_col>,
    observed_yield_t_ha, predicted_yield_t_ha, area_ha, model

Deliberately absent: country / admin-1 / admin-2 names, the municipality code
(identical to the join key) and the shapefile's own display name -- all
reachable through the join. Also absent is ``Region_ID``: despite the name it
is the POOLING CLUSTER id (1..N under ``cluster_strategy``), not an admin
code, so exporting it invites exactly the mistake it looks like it prevents.

Stage is expressed as ``lead`` + ``stage_month_name``. ``lead`` is the number
of months of data the forecast saw (1 = first month of that region's season),
which -- unlike a month number -- keeps sorting correctly across the New Year
for southern-hemisphere seasons that run Sep -> Apr.

Two entry points, because a run should produce its deliverable without anyone
remembering to:

* ``export_from_parser`` -- called at the end of ``geocif_runner.main`` when
  ``[ML] export_predictions_csv`` is on. One CSV per DB the run wrote.
* ``python -m geocif.predictions_export`` -- merges N DBs into one CSV, which
  is what a per-fold (one DB per forecast year) run needs.
"""

import argparse
import ast
import sqlite3
import sys
from pathlib import Path

import pandas as pd

from geocif.viz._outlook_db import dedup_upserts

# Output schema. The id column is named at runtime from the geobase `id_col`,
# so the header matches the shapefile field the user joins on.
OBS_OUT = "observed_yield_t_ha"
PRED_OUT = "predicted_yield_t_ha"

_MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_NUM = {m: i + 1 for i, m in enumerate(_MONTH_ABBR)}
_MONTH_FULL = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def _q(col):
    """Quote a SQL identifier."""
    return '"' + col.replace('"', '""') + '"'


def _resolve_yield_columns(table_cols):
    """Actual Predicted/Observed yield column names in the DB.

    With ``rename_target = True`` the writer stores ``"Predicted Yield"``
    rather than the canonical ``"Predicted Yield (tn per ha)"``, so the names
    are matched by prefix rather than assumed. Mirrors
    ``yield_outlook._resolve_yield_columns``; duplicated rather than imported
    because ``yield_outlook`` imports ``geocif_runner``, which imports this
    module -- the import would be circular.
    """
    pred = next((c for c in table_cols
                 if c.startswith("Predicted ") and "Yield" in c), None)
    obs = next((c for c in table_cols
                if c.startswith("Observed ") and "Yield" in c
                and not c.endswith("_class")), None)
    return pred, obs


def _swd_month(token):
    """Month number from a Stage-Window-Display endpoint (``"Sep 1"`` -> 9)."""
    if not isinstance(token, str) or not token.strip():
        return None
    return _MONTH_NUM.get(token.strip()[:3].title())


def _lead_and_month(swd):
    """``'Sep 1-Apr 30'`` -> ``(8, 'April')``.

    ``Stage Window Display`` is always calendar-order (``<planting> 1-<as-of>
    31``), so the left endpoint is the season start and the right is the month
    the data ran through. Lead counts inclusively from the season start and
    wraps the New Year: Sep->Sep is 1, Sep->Apr is 8.

    ``Stage Name`` is NOT usable here -- for ``_r`` methods its endpoints are
    reversed (see ``utils.friendly_stage_label``), which would silently
    invert the lead.
    """
    if not isinstance(swd, str) or "-" not in swd:
        return (None, None)
    left, right = swd.split("-", 1)
    start, end = _swd_month(left), _swd_month(right)
    if start is None or end is None:
        return (None, None)
    return ((end - start) % 12 + 1, _MONTH_FULL[end - 1])


def _tables_from_parser(parser):
    """``[(country, crop, table_name), ...]`` for everything this config runs."""
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    pooled = parser.getboolean("ML", "pool_countries", fallback=False)
    out = []
    for country in countries:
        for crop in ast.literal_eval(parser.get(country, "crops")):
            table = f"pooled_{crop}" if pooled else f"{country}_{crop}"
            out.append((country, crop, table))
    return out


def _read_table(db_path, table, *, experiment_name="default", models=None):
    """One results table, read-only, de-duplicated.

    Returns an empty frame (rather than raising) when the table is missing, so
    a DB written by a partial run -- one crop of several -- still exports what
    it does have.
    """
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        present = pd.read_sql(f"PRAGMA table_info({_q(table)})", con)["name"].tolist()
        if not present:
            return pd.DataFrame()
        pred_col, obs_col = _resolve_yield_columns(present)
        if pred_col is None:
            raise ValueError(
                f"{db_path.name}:{table} has no 'Predicted ... Yield' column "
                f"(found: {present[:12]}...)"
            )
        if "Stage Window Display" not in present:
            raise ValueError(
                f"{db_path.name}:{table} predates the 'Stage Window Display' "
                f"column (added 0.4.788). Lead/month cannot be derived safely "
                f"from 'Stage Name' alone -- its endpoints are reversed for _r "
                f"methods. Re-run the ML step to repopulate the DB."
            )
        wanted = ["Region", "Harvest Year", "Stage Name", "Stage Window Display",
                  "Model", "Date", "Time"]
        cols = [c for c in wanted if c in present]
        cols += [c for c in ("Area (ha)", "Season") if c in present]
        cols.append(pred_col)
        if obs_col:
            cols.append(obs_col)
        sql = (f"SELECT {','.join(_q(c) for c in cols)} FROM {_q(table)} "
               f"WHERE {_q('Experiment Name')} = ?")
        params = [experiment_name]
        if models:
            sql += f" AND {_q('Model')} IN ({','.join('?' * len(models))})"
            params += list(models)
        df = pd.read_sql(sql, con, params=params)
    except (pd.errors.DatabaseError, sqlite3.OperationalError):
        return pd.DataFrame()
    finally:
        con.close()
    if df.empty:
        return df

    rename = {pred_col: PRED_OUT}
    if obs_col:
        rename[obs_col] = OBS_OUT
    df = df.rename(columns=rename)
    if OBS_OUT not in df.columns:
        df[OBS_OUT] = pd.NA

    # Key on the DB's own column names, and on Season too when present --
    # multi-season countries legitimately hold two rows per region-year-stage.
    key = [c for c in ("Model", "Region", "Harvest Year", "Stage Name", "Season")
           if c in df.columns]
    df = dedup_upserts(df, key, f"{db_path.name}:{table}")

    df["year"] = pd.to_numeric(df["Harvest Year"], errors="coerce").astype("Int64")
    for c in (PRED_OUT, OBS_OUT, "Area (ha)"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # A row without a prediction is not a result. Observed is left NaN on
    # purpose: the live forecast year has no truth yet and must not vanish.
    return df.dropna(subset=[PRED_OUT, "year"]).copy()


def _region_id_lookup(parser, country):
    """``(name -> id)`` from the boundary shapefile, plus the id column's name.

    The DB stores ``Region`` as a display NAME; the shapefile's ``id_col``
    (``num_ID`` for Brazil) is the join key the user actually wants. Both
    sides are normalised with the SAME helper the yield join uses, so the
    export cannot disagree with what the model trained on.
    """
    from geocif.ml.stats import _norm_region_name
    from geocif.utils import load_country_boundary_gdf

    shp_file = parser.get(country, "boundary_file")
    shp_path = Path(parser.get("PATHS", "dir_boundary_files")) / shp_file
    id_col = parser.get(Path(shp_file).stem, "id_col", fallback="ADM_ID")
    admin_zone = parser.get(country, "admin_level", fallback="admin_1")

    gdf = load_country_boundary_gdf(parser, shp_path, country=country)
    name_col = "ADM2_NAME" if admin_zone == "admin_2" else "ADM1_NAME"
    if name_col not in gdf.columns:
        name_col = next((c for c in ("ADM2_NAME", "ADM1_NAME")
                         if c in gdf.columns), None)
    if name_col is None or "ADM_ID" not in gdf.columns:
        raise ValueError(
            f"{shp_path.name} lacks a usable name/id pair after the geobase "
            f"rename (columns: {list(gdf.columns)}). Set adm1_col/adm2_col/"
            f"id_col in the [{Path(shp_file).stem}] section."
        )
    lookup = {_norm_region_name(n): i
              for n, i in zip(gdf[name_col], gdf["ADM_ID"])}
    return lookup, id_col


def export_predictions(parser, db_paths, out_path, *, models=None,
                       experiment_name="default", verbose=True):
    """Write the join-ready CSV for one or more result DBs. Returns the path.

    ``db_paths`` may hold several databases -- a per-fold run writes one DB per
    forecast year, and the deliverable is their concatenation.
    """
    from geocif.ml.stats import _norm_region_name

    if isinstance(db_paths, (str, Path)):
        db_paths = [db_paths]
    db_paths = [Path(p) for p in db_paths]

    frames, lookups, id_col = [], {}, None
    dropped_regions = set()
    for country, crop, table in _tables_from_parser(parser):
        if country not in lookups:
            lookups[country] = _region_id_lookup(parser, country)
        lookup, id_col = lookups[country]
        for db_path in db_paths:
            if not db_path.exists():
                raise FileNotFoundError(f"database not found: {db_path}")
            df = _read_table(db_path, table, experiment_name=experiment_name,
                             models=models)
            if df.empty:
                continue
            lead_month = [_lead_and_month(s) for s in df["Stage Window Display"]]
            df["lead"] = [lm[0] for lm in lead_month]
            df["stage_month_name"] = [lm[1] for lm in lead_month]
            df[id_col] = [lookup.get(_norm_region_name(r)) for r in df["Region"]]
            unmatched = sorted(set(df.loc[df[id_col].isna(), "Region"]))
            if unmatched:
                print(f"  WARNING {db_path.name}:{table}: {len(unmatched)} region(s) "
                      f"absent from the boundary file, dropped "
                      f"(e.g. {unmatched[:3]})")
                df = df[df[id_col].notna()]
                dropped_regions.update(unmatched)
            # An all-unmatched table must NOT reach the concat: an empty frame
            # there produces a headers-only CSV and no error at all.
            if df.empty:
                continue
            df["model"] = df["Model"]
            df["area_ha"] = df["Area (ha)"] if "Area (ha)" in df.columns else pd.NA
            frames.append(df)

    if not frames:
        if dropped_regions:
            raise ValueError(
                f"every row was dropped: none of the {len(dropped_regions)} "
                f"region name(s) in the DB match the boundary file "
                f"(e.g. {sorted(dropped_regions)[:3]}). The DB's 'Region' and "
                f"the shapefile's admin-name column must be the same names."
            )
        raise ValueError(
            f"no rows for Experiment Name = '{experiment_name}' in "
            f"{[p.name for p in db_paths]}. geocif_runner writes 'default'; "
            f"yield_outlook writes 'outlook'."
        )

    out = pd.concat(frames, ignore_index=True)
    out[id_col] = out[id_col].astype("int64")
    cols = ["year", "lead", "stage_month_name", id_col,
            OBS_OUT, PRED_OUT, "area_ha", "model"]
    out = (out[cols]
           .sort_values(["model", "year", "lead", id_col], kind="stable")
           .reset_index(drop=True))

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)
    if verbose:
        print(f"\n{len(out):,} rows x {len(cols)} columns -> {out_path}")
        print(f"  join key    : {id_col} ({out[id_col].nunique():,} regions)")
        print(f"  years       : {int(out['year'].min())}-{int(out['year'].max())}")
        print(f"  leads       : {int(out['lead'].min())}-{int(out['lead'].max())}")
        print(f"  models      : {', '.join(sorted(out['model'].unique()))}")
        print(f"  observed    : {out[OBS_OUT].notna().sum():,} of {len(out):,} rows")
    return out_path


def export_from_parser(parser, logger=None):
    """Run-end hook: export whatever DB this run just wrote.

    Enabled with ``[ML] export_predictions_csv``. Each process owns its own
    DB, so a per-fold run produces one CSV per fold; use the CLI to merge
    them. Returns None when disabled.
    """
    from geocif import geocif as gc

    if not parser.getboolean("ML", "export_predictions_csv", fallback=False):
        return None
    project_name = parser.get("DEFAULT", "project_name")
    obj = gc.Geocif(logger=logger, parser=parser, project_name=project_name)
    db_path = Path(obj.db_path)
    out_path = db_path.parent / f"{db_path.stem}_predictions.csv"
    return export_predictions(parser, [db_path], out_path)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Export a join-ready prediction CSV from GeoCIF result DBs."
    )
    p.add_argument("--config", nargs="+", required=True,
                   help="config files, e.g. geobase.txt countries.txt crops.txt geocif.txt")
    p.add_argument("--db", nargs="+", required=True,
                   help="one or more result DBs; shell globs are expanded")
    p.add_argument("--out", required=True, help="output CSV path")
    p.add_argument("--model", nargs="*", default=None,
                   help="restrict to these models (default: every model in the DB)")
    p.add_argument("--experiment-name", default="default",
                   help="'default' for geocif_runner DBs, 'outlook' for yield_outlook")
    a = p.parse_args(argv)

    from geocif import logger as log

    _, parser = log.setup_logger_parser([Path(c) for c in a.config])
    dbs = []
    for pattern in a.db:
        if any(ch in pattern for ch in "*?["):
            dbs.extend(sorted(Path().glob(pattern)))
        else:
            dbs.append(Path(pattern))
    if not dbs:
        raise SystemExit(f"no databases matched {a.db}")
    print(f"reading {len(dbs)} database(s)")
    export_predictions(parser, dbs, a.out, models=a.model,
                       experiment_name=a.experiment_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
