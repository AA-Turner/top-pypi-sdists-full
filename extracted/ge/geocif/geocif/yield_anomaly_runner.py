"""Runner for BEAST-based yield anomaly detection.

Reads the HarvestStat (or any long-format) yield CSV pointed to by
the geocif config, runs the spike+revert detector on every
(country, admin_1, admin_2, product, season_name) series, writes:

  yield_anomalies.csv          — every flagged year, one row per flag
  yield_anomalies_summary.csv  — per-series counts (n_flags, etc.)
  plots/{country}_{crop}/      — per-flagged-region PNG with BEAST
                                  trend + cp_prob + flagged years

Outputs land at::

  ${dir_output}/yield_anomaly/<MMMM_DD_YYYY>/

The runner is config-driven the same way every other geocif runner is:
4-path cfg list passed to ``yield_anomaly_runner.run(paths)``.

Detection thresholds + crop/season filters are read from the
``[YIELD_ANOMALY]`` section of geocif.txt (see config docs).
"""
from __future__ import annotations

import ast
import logging
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import arrow as ar
import numpy as np
import pandas as pd

from geocif.ml.yield_anomaly_beast import (
    AnomalyThresholds,
    detect_spikes_batch,
    plot_series_with_flags,
)


def _make_parser(path_config_files: list) -> ConfigParser:
    """Load + concatenate every config file into one ConfigParser.
    Mirrors how the other runners read configs (see cell_optimizer.run /
    geocif_runner.run for the standard pattern)."""
    parser = ConfigParser(inline_comment_prefixes=(";",), interpolation=
                          __import__("configparser").ExtendedInterpolation())
    for p in path_config_files:
        parser.read(p)
    return parser


def _setup_logger(name: str = "yield_anomaly") -> logging.Logger:
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    if not log.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            "%Y-%m-%d %H:%M:%S",
        ))
        log.addHandler(h)
    log.propagate = False
    return log


def _read_thresholds(parser: ConfigParser) -> AnomalyThresholds:
    """Read [YIELD_ANOMALY] section with safe defaults."""
    sec = "YIELD_ANOMALY"
    def _f(key, default):
        if parser.has_option(sec, key):
            return float(parser.get(sec, key))
        return default
    def _i(key, default):
        if parser.has_option(sec, key):
            return int(parser.get(sec, key))
        return default
    def _b(key, default):
        if parser.has_option(sec, key):
            return parser.get(sec, key).strip().lower() in ("true", "1", "yes", "on")
        return default
    return AnomalyThresholds(
        z_threshold=_f("z_threshold", 2.0),
        cp_threshold=_f("cp_threshold", 0.5),
        revert_threshold=_f("revert_threshold", 1.0),
        min_years=_i("min_years", 10),
        include_negative_spikes=_b("include_negative_spikes", False),
        mcmc_seed=_i("mcmc_seed", 42),
    )


def _resolve_yield_csv(parser: ConfigParser, logger: logging.Logger) -> Path:
    """Find the HarvestStat-style CSV. Order:
      1. [YIELD_ANOMALY] input_csv (explicit override)
      2. [DEFAULT] production_statistics_file in dir_production_statistics
      3. Hardcoded fallback: hvstat_africa_data_v1.0.csv
    """
    sec = "YIELD_ANOMALY"
    if parser.has_option(sec, "input_csv"):
        p = Path(parser.get(sec, "input_csv"))
        if p.is_file():
            return p
        logger.warning(f"  YIELD_ANOMALY input_csv not found: {p}")

    dir_stats = parser.get("PATHS", "dir_production_statistics", fallback=None)
    fn = parser.get("DEFAULT", "production_statistics_file",
                    fallback="hvstat_africa_data_v1.0.csv")
    if dir_stats:
        p = Path(dir_stats) / fn
        if p.is_file():
            return p

    raise FileNotFoundError(
        f"Could not resolve yield CSV. Set [YIELD_ANOMALY] input_csv or "
        f"[PATHS] dir_production_statistics + [DEFAULT] "
        f"production_statistics_file."
    )


def _read_crop_filter(parser: ConfigParser) -> Optional[list]:
    """[YIELD_ANOMALY] crops = ['Maize','Wheat',...] — list of products
    to keep. None / empty → all crops."""
    sec = "YIELD_ANOMALY"
    if parser.has_option(sec, "crops"):
        raw = parser.get(sec, "crops").strip()
        if not raw:
            return None
        try:
            crops = ast.literal_eval(raw)
            return [str(c) for c in crops]
        except (ValueError, SyntaxError):
            return None
    return None


def _read_country_filter(parser: ConfigParser) -> Optional[list]:
    """[YIELD_ANOMALY] countries override; otherwise falls back to
    [DEFAULT] countries (same convention as other runners)."""
    sec = "YIELD_ANOMALY"
    raw = None
    if parser.has_option(sec, "countries"):
        raw = parser.get(sec, "countries").strip()
    if not raw and parser.has_option("DEFAULT", "countries"):
        raw = parser.get("DEFAULT", "countries").strip()
    if not raw:
        return None
    try:
        cs = ast.literal_eval(raw)
        return [str(c) for c in cs]
    except (ValueError, SyntaxError):
        return None


def _load_and_filter(
    csv_path: Path,
    crop_filter: Optional[list],
    country_filter: Optional[list],
    logger: logging.Logger,
) -> pd.DataFrame:
    """Read the HarvestStat-style CSV and apply crop/country filters.
    Returns a normalized DataFrame with columns:
        country, admin_1, admin_2, fnid, product, season_name,
        crop_production_system, harvest_year, area, production, yield
    """
    logger.info(f"  reading yield CSV: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    n_in = len(df)

    # Normalize string columns — country sometimes has stray quotes.
    for c in ("country", "admin_1", "admin_2", "product", "season_name",
              "crop_production_system"):
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.strip('"')

    # Coerce numeric columns.
    for c in ("harvest_year", "planting_year", "area", "production", "yield"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if country_filter:
        wanted = {c.lower() for c in country_filter}
        df = df[df["country"].str.lower().isin(wanted)]
    if crop_filter:
        wanted = {c.lower() for c in crop_filter}
        df = df[df["product"].str.lower().isin(wanted)]

    df = df.dropna(subset=["yield", "harvest_year"])
    df = df[df["harvest_year"] > 0]
    df["harvest_year"] = df["harvest_year"].astype(int)

    logger.info(
        f"  after filter: {len(df)}/{n_in} rows, "
        f"{df['country'].nunique()} countries, "
        f"{df['product'].nunique()} crops, "
        f"{df['season_name'].nunique()} seasons"
    )
    return df


def _build_output_dirs(parser: ConfigParser, logger: logging.Logger) -> tuple:
    """Resolve where to write outputs, namespaced by today's date.
    Returns (root, plots_dir)."""
    dir_output = parser.get("PATHS", "dir_output", fallback=None)
    if dir_output is None:
        dir_output = parser.get("DEFAULT", "dir_output", fallback="./outputs")
    today_tag = ar.now().format("MMMM_DD_YYYY")
    root = Path(dir_output) / "yield_anomaly" / today_tag
    plots_dir = root / "plots"
    root.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"  output dir: {root}")
    return root, plots_dir


def run(path_config_files: list) -> Path:
    """Main entry. Mirrors the other geocif runners' (cfg-list) call shape.
    Returns the path to the master yield_anomalies.csv."""
    logger = _setup_logger()
    parser = _make_parser(path_config_files)

    logger.info("=" * 78)
    logger.info("GeoCIF Yield Anomaly Detector (BEAST)")
    logger.info("=" * 78)

    thresholds = _read_thresholds(parser)
    logger.info(
        f"  thresholds: z>{thresholds.z_threshold}, cp<{thresholds.cp_threshold}, "
        f"revert<|{thresholds.revert_threshold}|, "
        f"min_years={thresholds.min_years}, "
        f"include_negative={thresholds.include_negative_spikes}"
    )

    csv_path = _resolve_yield_csv(parser, logger)
    crop_filter = _read_crop_filter(parser)
    country_filter = _read_country_filter(parser)
    if crop_filter:
        logger.info(f"  crop filter: {crop_filter}")
    if country_filter:
        logger.info(f"  country filter: {country_filter}")

    df = _load_and_filter(csv_path, crop_filter, country_filter, logger)
    if df.empty:
        logger.warning("  no rows after filter — nothing to do.")
        return Path()

    root, plots_dir = _build_output_dirs(parser, logger)

    # Detect. Group by (country, admin_1, admin_2, product, season_name).
    # Several countries also distinguish crop_production_system (e.g.
    # rainfed vs irrigated). Include it in the group key so each system
    # gets its own series.
    group_cols = ("country", "admin_1", "admin_2", "product",
                  "season_name", "crop_production_system")
    # Some rows have empty admin_2 — that's fine, treat as part of the key.
    for c in group_cols:
        if c not in df.columns:
            df[c] = ""

    n_jobs = (
        int(parser.get("YIELD_ANOMALY", "n_jobs", fallback="-1"))
        if parser.has_section("YIELD_ANOMALY") else -1
    )
    do_plot = (
        parser.get("YIELD_ANOMALY", "do_plot", fallback="True")
              .strip().lower() in ("true", "1", "yes", "on")
        if parser.has_section("YIELD_ANOMALY") else True
    )

    logger.info(
        f"  running BEAST on {df.groupby(list(group_cols)).ngroups} series "
        f"(n_jobs={n_jobs})..."
    )
    flagged, outputs = detect_spikes_batch(
        df,
        group_cols=group_cols,
        year_col="harvest_year",
        target_col="yield",
        thresholds=thresholds,
        n_jobs=n_jobs,
        logger=logger,
        return_series_outputs=True,
    )

    # Master flagged CSV.
    flagged_path = root / "yield_anomalies.csv"
    flagged.to_csv(flagged_path, index=False)
    logger.info(f"  wrote {flagged_path} ({len(flagged)} flagged years)")

    # Summary: per-series counts.
    summary_rows = []
    for key, res in outputs.items():
        row = {col: val for col, val in zip(group_cols, key)}
        flags = res.get("flags", [])
        row["n_years_used"] = res.get("n_years_used", 0)
        row["status"] = res.get("status", "")
        row["n_flags_total"] = len(flags)
        row["n_spike_revert"] = sum(
            1 for f in flags if f["anomaly_type"] == "spike_revert"
        )
        row["n_end_of_series"] = sum(
            1 for f in flags if f["anomaly_type"] == "end_of_series_spike"
        )
        row["n_spike_no_revert"] = sum(
            1 for f in flags if f["anomaly_type"] == "spike_no_revert"
        )
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows)
    summary_path = root / "yield_anomalies_summary.csv"
    summary.to_csv(summary_path, index=False)
    logger.info(f"  wrote {summary_path}")

    # Per-region plots — only for series WITH flags (skip clean ones).
    if do_plot:
        n_plotted = 0
        for key, res in outputs.items():
            flags = res.get("flags", [])
            if not flags:
                continue
            country, admin_1, admin_2, product, season, system = key
            sub_dir = plots_dir / _safe_filename(f"{country}_{product}")
            sub_dir.mkdir(parents=True, exist_ok=True)
            stem = _safe_filename(
                f"{admin_1}__{admin_2}__{season}__{system}"
            )
            out_path = sub_dir / f"{stem}.png"
            title = (
                f"{country} — {product} ({season}, {system or 'unspecified'})\n"
                f"{admin_1} / {admin_2}"
            )
            try:
                plot_series_with_flags(res, title=title, out_path=out_path)
                n_plotted += 1
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"  plot failed for {key}: {exc}")
        logger.info(f"  wrote {n_plotted} plots to {plots_dir}")

    logger.info("=" * 78)
    logger.info(f"DONE. Flagged years: {len(flagged)}; series: {len(outputs)}")
    logger.info("=" * 78)
    return flagged_path


def _safe_filename(s: str) -> str:
    """Sanitize a string for use as a filename: replace path separators
    and other unsafe characters with underscores. Keeps unicode letters."""
    s = str(s).strip()
    bad = '/\\:*?"<>|'
    for ch in bad:
        s = s.replace(ch, "_")
    return s.replace(" ", "_") or "_"
