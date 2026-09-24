# -*- coding: utf-8 -*-
"""calendar_validator.py -- validate GEOGLAM Crop Monitor calendars against NDVI.

For every (country, crop, season, calendar region) it compares the phenological
transitions implied by the satellite record with the days the Crop Monitor
calendar asserts, and reports the signed difference in days.

Usage::

    from geocif import calendar_validator
    calendar_validator.run([
        "config/cropcal/geobase.txt",
        "config/cropcal/countries.txt",
        "config/cropcal/crops.txt",
        "config/cropcal/geoextract.txt",
    ])

Pipeline: geoextract (per-region daily EO) -> this runner.

Outputs, under ``{dir_output}/calendar_validation/{today}/``::

    frame_all.csv          one row per region, scored or skipped with a reason;
                           columns follow score.RegionScore (calendar_*_doy,
                           satellite_*_doy, <transition>_diff_days, ...)
    frame_subset.csv       rows whose NDVI peak falls inside calendar stage 2
    {crop}.csv             per-crop splits
    summary_{delta}.csv    per-crop medians, within-tolerance shares, circular r2
    skips.csv              every unscored region and why
    models/                four-target comparison: design_matrix, predictions,
                           metrics (with skill vs the climatology null and a
                           bootstrap interval, plus the Franch et al. 2022
                           comparables: R2, calibration line, debiased RMSE,
                           60-day blunder share), consistency (season order and
                           length across the four predicted days), cv_schemes
                           (with the duplicate-row leakage per scheme),
                           model_failures
    plots/, maps/, csvs/   per-region diagnostics and difference maps, each
                           with a companion CSV
    run_manifest.json      versions, targets, feature groups, column_scheme = 2
"""
from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Optional

import arrow as ar
import numpy as np
import pandas as pd
from geoprepare import base

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import cv, features, models, naming, pipeline, score

logger = logging.getLogger(__name__)

SECTION = "CROPCAL"


class CalendarValidator(base.BaseGeo):
    """Config + orchestration. The per-region work lives in cropcal.pipeline."""

    def __init__(self, path_config_files):
        super().__init__(path_config_files)
        self._config_files = path_config_files
        self.parse_config()

    def _get(self, option, default=None, sections=(SECTION, "DEFAULT")):
        for section in sections:
            if self.parser.has_option(section, option):
                return self.parser.get(section, option)
        return default

    def _getbool(self, option, default=False):
        value = self._get(option)
        return default if value is None else str(value).strip().lower() in {"1", "true", "yes"}

    def _getint(self, option, default):
        value = self._get(option)
        return default if value is None else int(value)

    def _getlist(self, option, default):
        value = self._get(option)
        if value in (None, ""):
            return list(default)
        return list(ast.literal_eval(value))

    def parse_config(self, section="DEFAULT"):
        self.project_name = self.parser.get("DEFAULT", "project_name")
        super().parse_config(project_name=self.project_name, section="DEFAULT")

        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.today_tag = ar.now().format("MMMM_DD_YYYY")

        self.start_year = int(self.parser.get("DEFAULT", "start_year"))
        self.end_year = int(self.parser.get("DEFAULT", "end_year"))
        self.floor = int(self.parser.get("DEFAULT", "floor", fallback="1"))

        # Algorithm knobs. Defaults reproduce the GEOGLAM original except where
        # DEVIATIONS.md says otherwise.
        self.num_years = self._getint("num_years", 5)
        self.max_delta = self._getint("max_delta", score.MAX_DELTA)
        self.convention = self._get("doy_convention", "calendar")
        self.legacy_wrap_gate = self._getbool("legacy_wrap_gate", False)
        self.circular_peak_distance = self._getbool("circular_peak_distance", True)
        self.fix_gdd100_offset = self._getbool("fix_gdd100_offset", False)

        # Model comparison.
        self.run_models = self._getbool("run_models", True)
        self.models = self._getlist("models", models.DEFAULT_MODELS)
        self.cv_schemes = self._getlist("cv_schemes", cv.SCHEME_NAMES)
        self.n_splits = self._getint("n_splits", cv.DEFAULT_N_SPLITS)
        self.block_degrees = float(self._get("block_degrees", cv.DEFAULT_BLOCK_DEGREES))
        self.seed = self._getint("seed", 0)
        self.encodings = self._getlist("target_encodings", models.ENCODINGS)
        # {scheme: [models]} -- run only these models under that scheme. Lets
        # leave-one-country-out (145 folds) run for the cheap models without
        # paying 30+ hours for tabpfn/tabicl on it.
        raw = self._get("cv_scheme_models")
        self.scheme_models = dict(ast.literal_eval(raw)) if raw not in (None, "") else {}

        self.make_plots = self._getbool("make_plots", True)
        # Deliberately NOT named `crops`/`countries`: both already exist in
        # countries.txt [DEFAULT] and geoextract.txt [DEFAULT] for geoextract's
        # own use, and _get() falls through to [DEFAULT]. Reading `crops` here
        # picked up geoextract's `crops = ['maize']` default and silently
        # narrowed a 145-country run to maize alone, reporting success.
        self.crops_filter = self._getlist("validate_crops", [])
        self.countries_filter = self._getlist("validate_countries", [])

        self.calendar_file = self._get_country_option("calendar_file")
        self.boundary_file = self._get_country_option("boundary_file")
        self.scale = self._get_country_option("admin_level") or "admin_1"

    def _get_country_option(self, option):
        """Read an option that lives in the per-country sections' DEFAULT."""
        for country in self.countries:
            if self.parser.has_option(country, option):
                return self.parser.get(country, option)
        return None

    # ------------------------------------------------------------------
    @property
    def output_dir(self) -> Path:
        return Path(self.dir_output) / "calendar_validation" / self.today_tag

    def region_metadata(self) -> pd.DataFrame:
        """Region geography and class, from the prepared boundary file.

        Columns: ``key, num_ID, ADM0_NAME, Name, CM_Group, Region, lat, lon``.
        """
        import geopandas as gpd

        path = Path(self.dir_boundary_files) / self.boundary_file
        gdf = gpd.read_file(path, engine="pyogrio")
        if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)
        centroids = gdf.geometry.to_crs("+proj=eqearth").centroid.to_crs(epsg=4326)
        out = pd.DataFrame(
            {
                "key": gdf["Key"].map(naming.clean_text),
                "region_id": gdf["num_ID"],
                "country": gdf["ADM0_NAME"].map(naming.clean_text),
                "country_slug": gdf["ADM0_NAME"].map(naming.country_slug),
                "region_name": gdf["Name"].map(naming.clean_text),
                "cm_group": gdf.get("CM_Group", pd.Series("", index=gdf.index)),
                "grouping": gdf.get("Region", pd.Series("", index=gdf.index)),
                "lat": centroids.y.to_numpy(),
                "lon": centroids.x.to_numpy(),
            }
        )
        return out.set_index("key")

    def zone_metadata(self) -> pd.DataFrame:
        """``country -> (climate_zone, hemisphere)`` from metadata/countries.csv.

        Both change the algorithm: the winter-wheat greenup rules branch on
        hemisphere, and the GDD bounds are scaled by 0.75 outside the tropics.
        A country missing from the file falls back to Temperate/N and is
        reported, because silently defaulting would change its transitions.
        """
        path = Path(self.dir_metadata) / (self._get_country_option("zone_file") or "countries.csv")
        frame = pd.read_csv(path)
        frame["_join"] = frame["country"].map(naming.normalize)

        # countries.csv carries duplicate rows, sometimes with CONFLICTING
        # values -- bangladesh is listed both Temperate and Tropical, bolivia
        # both Tropical and Temperate, and the russian federation appears under
        # two spellings that normalise to one key. A duplicated index makes
        # `.loc[key, "region"]` return a Series, and str() of that is a
        # multi-line repr, so the caller silently got a garbage climate zone
        # that equals neither "Temperate" nor "Tropical": the winter-wheat
        # greenup rules never fire and the GDD scaling is decided by accident.
        duplicated = frame[frame.duplicated("_join", keep=False)]
        if not duplicated.empty:
            conflicting = [
                key
                for key, part in duplicated.groupby("_join")
                if part["region"].nunique() > 1 or part["hemisphere"].nunique() > 1
            ]
            logger.warning(
                f"{path.name}: {duplicated['_join'].nunique()} duplicated country "
                f"key(s); keeping the first row of each. Conflicting values for: "
                f"{sorted(conflicting)}"
            )
        frame = frame.drop_duplicates("_join", keep="first")
        return frame.set_index("_join")[["region", "hemisphere"]]


def _scalar(value, default):
    """First element of a possibly-duplicated lookup, as a plain string.

    Belt and braces alongside the de-duplication in ``zone_metadata``: a
    ``.loc`` on a duplicated index returns a Series, and ``str()`` of one is a
    multi-line repr that silently fails every ``== "Temperate"`` test
    downstream instead of raising.
    """
    if isinstance(value, pd.Series):
        value = value.iloc[0] if len(value) else default
    text = str(value).strip()
    return text or default


def _collect(obj: CalendarValidator) -> tuple[pd.DataFrame, pd.DataFrame, list]:
    """Run every region and return ``(scored_frame, feature_frame, diagnostics)``."""
    calendar_path = Path(obj.dir_crop_calendars) / obj.calendar_file
    sheets = cropcal_calendar.read_workbook(calendar_path)
    regions = obj.region_metadata()

    try:
        zones = obj.zone_metadata()
    except Exception as exc:  # noqa: BLE001 - fall back rather than abort the run
        logger.warning(f"zone file unavailable ({exc}); defaulting every country to Temperate/N")
        zones = pd.DataFrame(columns=["region", "hemisphere"])

    settings = pipeline.Settings(
        root=Path(obj.dir_output),
        floor=obj.floor,
        scale=obj.scale,
        num_years=obj.num_years,
        years=tuple(range(obj.start_year, obj.end_year + 1)),
        max_delta=obj.max_delta,
        convention=obj.convention,
        legacy_wrap_gate=obj.legacy_wrap_gate,
        circular_peak_distance=obj.circular_peak_distance,
        fix_gdd100_offset=obj.fix_gdd100_offset,
    )

    wanted_countries = {naming.normalize(c) for c in obj.countries}
    if obj.countries_filter:
        wanted_countries &= {naming.normalize(c) for c in obj.countries_filter}
    wanted_crops = {naming.normalize(c) for c in obj.crops_filter} if obj.crops_filter else None

    rows, feature_rows, diagnostics, missing_zone = [], [], [], set()

    for crop_season, frame in sorted(sheets.items()):
        crop, season = crop_season.crop, crop_season.season
        if naming.skip_reason_for_crop(crop):
            continue
        if wanted_crops and crop not in wanted_crops:
            continue

        for _, calendar_row in frame.iterrows():
            key = calendar_row["key"]
            if key not in regions.index:
                continue
            meta = regions.loc[key]
            if isinstance(meta, pd.DataFrame):
                meta = meta.iloc[0]
            if naming.normalize(meta["country_slug"]) not in wanted_countries:
                continue

            zone_key = naming.normalize(meta["country"])
            if zone_key in zones.index:
                climate_zone = _scalar(zones.loc[zone_key, "region"], "Temperate")
                hemisphere = _scalar(zones.loc[zone_key, "hemisphere"], "N")
            else:
                climate_zone, hemisphere = "Temperate", "N"
                missing_zone.add(meta["country"])

            context = pipeline.RegionContext(
                key=key,
                country=meta["country"],
                country_slug=meta["country_slug"],
                region=naming.normalize(meta["region_name"]),
                region_id=meta["region_id"],
                crop=crop,
                season=season,
                cm_group=str(meta["cm_group"]),
                grouping=str(meta["grouping"]),
                climate_zone=climate_zone,
                hemisphere=hemisphere,
                lat=float(meta["lat"]),
                lon=float(meta["lon"]),
            )

            outcome = pipeline.run_region(context, calendar_row, settings)
            rows.append(outcome.row)
            if outcome.feature_row is not None:
                feature_rows.append(outcome.feature_row)
            if outcome.scored and outcome.diagnostics:
                diagnostics.append((context, outcome.diagnostics))

    if missing_zone:
        logger.warning(
            f"{len(missing_zone)} country(ies) absent from the zone file, defaulted to "
            f"Temperate/N: {sorted(missing_zone)[:10]}"
        )

    return pd.DataFrame(rows), features.design_matrix(feature_rows), diagnostics


def run(path_config_files):
    """Entry point. Prints the run parameters, then validates every region."""
    from rich.console import Console
    from rich.table import Table

    from geocif import __version__ as geocif_version

    obj = CalendarValidator(path_config_files)
    out_dir = obj.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    console = Console()
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column()
    table.add_row("Version", f"geocif {geocif_version}")
    table.add_row("Usage", "from geocif import calendar_validator; calendar_validator.run(cfg)")
    table.add_row("Project", obj.project_name)
    table.add_row("Countries", str(len(obj.countries)))
    table.add_row("Calendar", str(obj.calendar_file))
    table.add_row("Regions", str(obj.boundary_file))
    table.add_row("Years", f"{obj.start_year} - {obj.end_year} (median over {obj.num_years})")
    table.add_row("DOY convention", obj.convention)
    table.add_row("max_delta", f"{obj.max_delta} days")
    table.add_row("legacy_wrap_gate", str(obj.legacy_wrap_gate))
    table.add_row("circular_peak_distance", str(obj.circular_peak_distance))
    table.add_row("fix_gdd100_offset", str(obj.fix_gdd100_offset))
    table.add_row("Models", ", ".join(obj.models) if obj.run_models else "(disabled)")
    table.add_row("Targets", ", ".join(features.TARGETS))
    table.add_row("Encodings", ", ".join(obj.encodings))
    table.add_row("CV schemes", ", ".join(obj.cv_schemes))
    if obj.scheme_models:
        table.add_row("Scheme-limited", "; ".join(f"{k}: {', '.join(v)}" for k, v in obj.scheme_models.items()))
    table.add_row("Features", f"{len(features.FEATURE_NAMES)} in {len(features.FEATURE_GROUPS)} groups")
    table.add_row("Figures", str(obj.make_plots))
    table.add_row("Output", str(out_dir))
    console.print(table)

    frame, design, diagnostics = _collect(obj)
    if frame.empty:
        # Never just log-and-return here. Under the cluster launcher nothing
        # configures logging to stdout, so an empty run printed its banner and
        # exited 0 -- indistinguishable from success, and it cost a full cycle
        # to notice that the CSVs being read were the previous run's.
        message = (
            "no regions were processed -- check that the calendar keys join the "
            "boundary file and that the country slugs match ADM0_NAME"
        )
        console.print(f"[bold red]ERROR[/bold red] {message}")
        raise SystemExit(message)

    scored = frame[frame["skip_reason"] == ""].copy()
    skipped = frame[frame["skip_reason"] != ""].copy()

    # Stale outputs from an earlier run on the same day would otherwise sit
    # alongside this one's and read as current.
    for old in out_dir.glob("*.csv"):
        old.unlink()

    import json

    (out_dir / "run_manifest.json").write_text(
        json.dumps(
            {
                "geocif_version": geocif_version,
                "finished": ar.now().format("YYYY-MM-DD HH:mm:ss"),
                "config_files": [str(f) for f in path_config_files],
                "calendar_file": str(obj.calendar_file),
                "boundary_file": str(obj.boundary_file),
                "rows_total": int(len(frame)),
                "rows_scored": int(len(scored)),
                "rows_skipped": int(len(skipped)),
                "crops": sorted(frame["crop"].unique().tolist()),
                "column_scheme": 2,
                "targets": list(features.TARGETS),
                "target_encodings": list(obj.encodings),
                "cv_scheme_models": {k: list(v) for k, v in obj.scheme_models.items()},
                "feature_groups": {k: len(v) for k, v in features.FEATURE_GROUPS.items()},
                "n_features": len(features.FEATURE_NAMES),
                "doy_convention": obj.convention,
                "legacy_wrap_gate": obj.legacy_wrap_gate,
                "circular_peak_distance": obj.circular_peak_distance,
                "fix_gdd100_offset": obj.fix_gdd100_offset,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    frame.to_csv(out_dir / "frame_all.csv", index=False)
    skipped.to_csv(out_dir / "skips.csv", index=False)
    if "peak_in_calendar_stage2" in scored.columns:
        scored[scored["peak_in_calendar_stage2"] == True].to_csv(  # noqa: E712
            out_dir / "frame_subset.csv", index=False
        )
    for crop, part in scored.groupby("crop"):
        part.to_csv(out_dir / f"{crop}.csv", index=False)

    summary = None
    if not scored.empty:
        summary = score.summarise(scored, max_delta=obj.max_delta, by="crop")
        summary.to_csv(out_dir / f"summary_delta_{obj.max_delta}.csv", index=False)
        score.summarise(scored, max_delta=obj.max_delta, by="cm_group").to_csv(
            out_dir / f"summary_delta_{obj.max_delta}_by_cm_group.csv", index=False
        )
        console.print(
            f"\n[bold]scored[/bold] {len(scored)}  "
            f"[bold]skipped[/bold] {len(skipped)}  "
            f"median |diff| greenup "
            f"{scored['midgreenup_diff_days'].abs().median():.0f} d, greendown "
            f"{scored['midgreendown_diff_days'].abs().median():.0f} d"
        )
        if not skipped.empty:
            console.print("\nskip reasons:")
            for reason, count in skipped["skip_reason"].value_counts().items():
                console.print(f"  {count:5d}  {reason}")

    if obj.run_models and not design.empty:
        model_dir = out_dir / "models"
        model_dir.mkdir(parents=True, exist_ok=True)
        # Same staleness hazard as the top-level tree: this directory is not
        # covered by the out_dir sweep, and model_failures.csv used to be
        # written only when something failed -- so a previous run's failures
        # survived a clean run and reported a working model as broken.
        for old_csv in model_dir.glob("*.csv"):
            old_csv.unlink()
        schemes = cv.build_schemes(
            design,
            n_splits=obj.n_splits,
            block_degrees=obj.block_degrees,
            seed=obj.seed,
            names=obj.cv_schemes,
        )
        cv.describe(schemes, design).to_csv(model_dir / "cv_schemes.csv", index=False)
        evaluation = models.evaluate(
            design,
            models=obj.models,
            schemes=schemes,
            baseline_columns=features.BASELINE_COLUMNS,
            tolerance=obj.max_delta,
            encodings=obj.encodings,
            seed=obj.seed,
            n_splits=obj.n_splits,
            block_degrees=obj.block_degrees,
            scheme_models=obj.scheme_models,
        )
        design.to_csv(model_dir / "design_matrix.csv", index=False)
        evaluation.predictions.to_csv(model_dir / "predictions.csv", index=False)
        evaluation.metrics.to_csv(model_dir / "metrics.csv", index=False)
        # Cross-target consistency: the four days are predicted independently,
        # so whether they land in season order with a plausible season length
        # is a property of the model, not of any one target.
        evaluation.consistency.to_csv(model_dir / "consistency.csv", index=False)
        # Always written, even empty: an absent file is ambiguous, and a stale
        # one is worse than either.
        pd.DataFrame({"failure": evaluation.failures}).to_csv(
            model_dir / "model_failures.csv", index=False
        )
        _print_model_table(console, evaluation.metrics, obj.max_delta)

    if obj.make_plots and diagnostics:
        from geocif.cropcal import plots

        plots.render_all(
            out_dir,
            scored,
            diagnostics,
            summary=summary,
            boundary_file=Path(obj.dir_boundary_files) / obj.boundary_file,
            max_region_figures=obj._getint("max_region_figures", 200) or None,
        )

    console.print(f"\nwrote {out_dir}")


def _print_model_table(console, metrics: pd.DataFrame, tolerance: int) -> None:
    """Headline comparison: overall circular MAE per model x encoding and CV scheme.

    One table per target, all rows, every row a (model, encoding) pair. The
    climatology null and the rule-based port appear as rows like any model;
    ``skill`` is 1 - MAE / MAE_null under the spatial-block null, with its
    bootstrap interval, for the non-leaky scheme when present.
    """
    from rich.table import Table

    if metrics.empty:
        return
    overall = metrics[(metrics["split"] == "overall") & (metrics["sample"] == "all")]
    for target, part in overall.groupby("target", sort=False):
        table = Table(title=f"{target}: circular MAE (days), all rows", box=None)
        table.add_column("model", style="bold cyan")
        table.add_column("encoding")
        schemes = sorted(part["scheme"].unique())
        for scheme in schemes:
            table.add_column(scheme, justify="right")
        table.add_column("skill [90% CI]", justify="right")
        for (model_name, encoding), rows in part.groupby(["model", "encoding"], sort=False):
            cells = []
            for scheme in schemes:
                hit = rows[rows["scheme"] == scheme]["mae_days"]
                cells.append(f"{hit.iloc[0]:.1f}" if len(hit) and pd.notna(hit.iloc[0]) else "-")
            honest = rows[~rows["scheme"].isin(["random", "none"])]
            pick = honest.iloc[0] if len(honest) else rows.iloc[0]
            if pd.notna(pick.get("skill_vs_climatology", float("nan"))):
                skill = (
                    f"{pick['skill_vs_climatology']:+.2f} "
                    f"[{pick['skill_ci_low']:+.2f}, {pick['skill_ci_high']:+.2f}]"
                )
            else:
                skill = "-"
            table.add_row(str(model_name), str(encoding), *cells, skill)
        console.print()
        console.print(table)
