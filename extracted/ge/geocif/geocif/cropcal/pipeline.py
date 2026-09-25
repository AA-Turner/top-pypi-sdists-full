# -*- coding: utf-8 -*-
"""One region, end to end: calendar row + EO climatology -> a scored result.

This is the only place the modules are wired together, so both the runner and
the tests exercise the same path. Everything it needs is passed in; it opens no
config and writes no files.

Order of operations, and why each step can bail out:

1. calendar row -> four transition days (a malformed row is recorded, not raised)
2. EO CSVs -> per-day NDVI and GDD medians, plus the optional moisture and
   stress variables (a region with no NDVI/temperature extraction is recorded;
   the original silently skipped it)
3. Fourier fit + peak detection (more than five peaks means the signal is too
   noisy to validate -- the original's rule, kept)
4. build the model-comparison feature row -- BEFORE the rules run, so a
   region the rule-based method cannot handle still enters the model sample.
   The rules need a finite curve inside the calendar window; that is a
   calendar-dependent selection, and gating the models on it biased their
   sample toward regions where calendar and NDVI already agree.
5. mask the curve to the season and derive the remote-sensing transitions
6. score against the calendar

Every result row, scored or skipped, is built through :class:`score.RegionScore`
so the output frame has one header and one vocabulary.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

from geocif.cropcal import calendar as cropcal_calendar
from geocif.cropcal import curve, features, naming, score, series, transitions

logger = logging.getLogger(__name__)


@dataclass
class RegionContext:
    """Everything about a region that does not come from the EO archive."""

    key: str
    country: str
    country_slug: str
    region: str
    region_id: object
    crop: str
    season: int
    cm_group: str = ""
    grouping: str = ""
    climate_zone: str = "Temperate"
    hemisphere: str = "N"
    lat: float = float("nan")
    lon: float = float("nan")


@dataclass
class Settings:
    """Knobs, all config-driven. Defaults reproduce the original."""

    #: geoprepare's ``params.dir_output`` -- already project-scoped, see
    #: :func:`geocif.cropcal.series.region_dir`.
    root: Path
    floor: int = 1
    scale: str = "admin_1"
    num_years: int = series.DEFAULT_NUM_YEARS
    years: Optional[tuple[int, ...]] = None
    max_delta: int = score.MAX_DELTA
    convention: str = "calendar"
    legacy_wrap_gate: bool = False
    circular_peak_distance: bool = True
    fix_gdd100_offset: bool = False
    max_peaks: int = curve.MAX_PEAKS


@dataclass
class RegionOutcome:
    """What one region produced: a score row, a feature row, or a reason."""

    row: dict
    feature_row: Optional[dict] = None
    diagnostics: dict = field(default_factory=dict)

    @property
    def scored(self) -> bool:
        return not self.row.get("skip_reason")


def _skip(
    context: RegionContext,
    reason: str,
    *,
    feature_row: Optional[dict] = None,
    **extra,
) -> RegionOutcome:
    row = score.make_row(
        key=context.key,
        country=context.country,
        region=context.region,
        crop=context.crop,
        season=context.season,
        cm_group=context.cm_group,
        grouping=context.grouping,
        climate_zone=context.climate_zone,
        hemisphere=context.hemisphere,
        lat=context.lat,
        lon=context.lon,
        skip_reason=reason,
        **extra,
    )
    return RegionOutcome(row=row, feature_row=feature_row)


def run_region(
    context: RegionContext,
    calendar_row,
    settings: Settings,
) -> RegionOutcome:
    """Validate one (country, crop, season, region).

    Args:
        context: identity, geography and climate class of the region.
        calendar_row: one row of a :func:`geocif.cropcal.calendar.read_sheet` frame.
        settings: the run's knobs.

    Returns:
        A :class:`RegionOutcome`. ``skip_reason`` is set and the comparison
        columns are NaN when the region could not be scored; the reason is
        always specific enough to act on. A ``feature_row`` is present whenever
        the EO climatology and curve exist, even if the transition rules then
        failed -- the model comparison is not gated on the rule-based method.
    """
    params = naming.crop_params(context.crop)
    if params is None:
        return _skip(context, naming.skip_reason_for_crop(context.crop) or "unknown crop")

    # 1. Calendar -------------------------------------------------------
    geoglam, bins, reason = cropcal_calendar.row_stage_days(
        calendar_row, convention=settings.convention
    )
    if reason is not None:
        return _skip(context, reason)
    calendar_flags = {
        "calendar_wraps_year": bool(bins.wraps_year),
        "calendar_wall_to_wall": bool(bins.wall_to_wall),
    }

    # 2. EO climatology -------------------------------------------------
    try:
        climatology = series.build_climatology(
            settings.root,
            settings.floor,
            context.country_slug,
            settings.scale,
            context.crop,
            context.region,
            context.region_id,
            params=params,
            years=settings.years,
            num_years=settings.num_years,
        )
    except series.SeriesError as exc:
        return _skip(context, f"no EO data: {exc}", **calendar_flags)

    if not climatology.usable:
        return _skip(context, "EO climatology is all NaN or all zero", **calendar_flags)

    # 3. Curve ----------------------------------------------------------
    try:
        fitted = curve.fit_fourier(climatology.ndvi)
    except ValueError as exc:
        return _skip(context, f"curve fit failed: {exc}", **calendar_flags)

    peaks, valleys = curve.detect_peaks_valleys(
        fitted, mph_fraction=curve.mph_fraction_for(context.crop)
    )

    # 4. Feature row ----------------------------------------------------
    # Everything here is calendar-free except the targets themselves, and it
    # is built before the rules run so their failure does not shrink the model
    # sample. The baselines are filled in only if the rules succeed.
    feature_row = features.build_row(
        key=context.key,
        country=context.country,
        region=context.region,
        crop=context.crop,
        season=context.season,
        cm_group=context.cm_group,
        climate_zone=context.climate_zone,
        hemisphere=context.hemisphere,
        lat=context.lat,
        lon=context.lon,
        ndvi=climatology.ndvi,
        gdd=climatology.gdd,
        agdd=climatology.agdd,
        peaks=peaks,
        valleys=valleys,
        fitted=fitted,
        tmean=climatology.tmean,
        precip=climatology.precip,
        precip_years=climatology.precip_years,
        esi_years=climatology.esi_years,
        sm_surface=climatology.sm_surface,
        sm_surface_years=climatology.sm_surface_years,
        sm_rootzone=climatology.sm_rootzone,
        sm_rootzone_years=climatology.sm_rootzone_years,
        tdew=climatology.tdew,
        elevation=climatology.elevation,
        slope=climatology.slope,
        targets={name: geoglam[features.CALENDAR_KEY[name]] for name in features.TARGETS},
        **calendar_flags,
    )
    for column in features.BASELINE_COLUMNS.values():
        feature_row[column] = float("nan")

    if len(peaks) > settings.max_peaks:
        return _skip(
            context,
            f"signal too noisy: {len(peaks)} peaks (limit {settings.max_peaks})",
            feature_row=feature_row,
            n_peaks=len(peaks),
            n_years=climatology.n_years,
            **calendar_flags,
        )
    if len(peaks) == 0:
        return _skip(
            context,
            "no NDVI peak detected",
            feature_row=feature_row,
            n_peaks=0,
            n_years=climatology.n_years,
            **calendar_flags,
        )

    # 5. Mask and derive ------------------------------------------------
    masked = curve.mask_to_season(
        fitted,
        peaks,
        valleys,
        midgreenup=geoglam["midgreenup"],
        midgreendown=geoglam["midgreendown"],
        plant=geoglam["plant"],
        harvest=geoglam["harvest"],
        legacy_wrap_gate=settings.legacy_wrap_gate,
        circular_distance=settings.circular_peak_distance,
    )

    try:
        rs = transitions.rs_transitions(
            masked.values,
            climatology.gdd,
            plant=int(geoglam["plant"]),
            crop=context.crop,
            params=params,
            climate_zone=context.climate_zone,
            hemisphere=context.hemisphere,
            fix_gdd100_offset=settings.fix_gdd100_offset,
        )
    except transitions.TransitionError as exc:
        return _skip(
            context,
            f"no usable curve inside the season: {exc}",
            feature_row=feature_row,
            n_peaks=len(peaks),
            n_years=climatology.n_years,
            **calendar_flags,
        )

    # 6. Score ----------------------------------------------------------
    scored = score.score_region(
        geoglam=geoglam,
        rs_midgreenup=rs.midgreenup,
        rs_midgreendown=rs.midgreendown,
        fitted=fitted,
        masked=masked.values,
        gdd=climatology.gdd,
        max_delta=settings.max_delta,
    )

    row = score.make_row(
        key=context.key,
        country=context.country,
        region=context.region,
        crop=context.crop,
        season=context.season,
        cm_group=context.cm_group,
        grouping=context.grouping,
        climate_zone=context.climate_zone,
        hemisphere=context.hemisphere,
        lat=context.lat,
        lon=context.lon,
        n_peaks=len(peaks),
        depeaked=masked.depeaked,
        n_years=climatology.n_years,
        crop_params_trusted=params.trusted,
        skip_reason="",
        notes="; ".join(rs.notes),
        **calendar_flags,
        **scored,
    )

    # The rule-based answer rides along so the model tables can score it as
    # the baseline without recomputing anything. It is NOT a feature: see
    # features.feature_columns.
    feature_row[features.BASELINE_COLUMNS["midgreenup"]] = float(rs.midgreenup)
    feature_row[features.BASELINE_COLUMNS["midgreendown"]] = float(rs.midgreendown)

    return RegionOutcome(
        row=row,
        feature_row=feature_row,
        diagnostics={
            "fitted": fitted,
            "masked": masked.values,
            "peaks": peaks,
            "valleys": valleys,
            "climatology": climatology,
            "geoglam": geoglam,
            "rs": rs,
        },
    )
