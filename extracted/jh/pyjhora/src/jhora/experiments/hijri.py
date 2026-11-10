#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# py -- routines for computing tithi, vara, etc.
#
# Copyright (C) 2013 Satish BD  <bdsatish@gmail.com>
# Downloaded from https://github.com/bdsatish/drik-panchanga
#
# This file is part of the "drik-panchanga" Python library
# for computing Hindu luni-solar calendar based on the Swiss ephemeris
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Copyright (C) Open Astro Technologies, USA.
# Modified by Sundar Sundaresan, USA. carnaticmusicguru2015@comcast.net
# Downloaded from https://github.com/naturalstupid/PyJHora
"""
hijri.py — Hijri/Islamic date with two modes:

1) TABLE MODE (DEFAULT): hijridate (Umm al-Qura civil table)
   - Place independent, date-only conversion.
   - Best when you want a stable, widely used civil Hijri calendar.

2) CALCULATED MODE: calculated sighting (research-style)
   - Place/policy/criterion configurable (LOCAL / ANCHOR / GLOBAL_VISIBILITY).
   - Uses drik for sunset/moonset/new_moon + Swiss Ephemeris for Moon altitude.
   - Intended to approximate "sightability by calculation" (not actual reports).

 !!!! CAUTION: This code was generated using AI (Gemini / CoPoilot) - so review before using it !!!!

"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import IntFlag, auto
from math import floor
from types import SimpleNamespace
from typing import Optional, Tuple, Sequence, Dict, Union, List, Any
from datetime import date as _date

from pyIslam.praytimes import PrayerConf, Prayer, LIST_FAJR_ISHA_METHODS

from jhora import utils
""" 
    drik here is generic model name can be surya_sidhantha or drik depending on value 
    of const.astrology_model_default value
"""
drik = utils.hora_engine_proxy

import swisseph as swe

# ==========================================================
# Prayer Times (pyIslam + islamic_times) Options & Config
# ==========================================================

@dataclass(frozen=True)
class IslamicTimesConfig:
    """
    Configuration for the 'islamic_times' engine (ITLocation).
    """
    elevation: float = 0.0
    temperature: float = 10.0
    pressure: float = 101.325  # kPa
    find_local_tz: bool = False

    # 0 = middle of sunset→sunrise, 1 = middle of sunset→fajr
    midnight_type: int = 0

    # Optional custom angles in degrees: (fajr_angle, maghrib_angle, isha_angle)
    custom_angles: Optional[Tuple[float, float, float]] = None

    # Method string fallback if mapping isn't available
    method_fallback: str = "ISNA"


class ISLAMIC_PRAYER_OPTIONS(IntFlag):
    ENGINE_PYISLAM = auto()
    ENGINE_ISLAMIC_TIMES = auto()

    # --- Calculation method (pick ONE) ---
    METHOD_KARACHI = auto()
    METHOD_MWL = auto()
    METHOD_EGYPT = auto()
    METHOD_UMM_AL_QURA = auto()
    METHOD_ISNA = auto()
    METHOD_UOIF = auto()
    METHOD_SINGAPORE = auto()
    METHOD_RUSSIA = auto()
    METHOD_FIXED_90 = auto()

    # --- Asr madhab (pick ONE) ---
    ASR_SHAFII_MALIKI_HANBALI = auto()
    ASR_HANAFI = auto()

    # --- DST / summer time handling ---
    DST_OFF = auto()
    DST_ON = auto()

    # --- Output extras ---
    INCLUDE_MIDNIGHT = auto()
    INCLUDE_QIYAM_LAST_THIRD = auto()


# Default flags (explicit engine)
ISLAMIC_PRAYER_OPTIONS.DEFAULT = (
    ISLAMIC_PRAYER_OPTIONS.ENGINE_PYISLAM |
    ISLAMIC_PRAYER_OPTIONS.METHOD_ISNA |
    ISLAMIC_PRAYER_OPTIONS.ASR_SHAFII_MALIKI_HANBALI |
    ISLAMIC_PRAYER_OPTIONS.DST_OFF
)

# Convenience namespaces
ISLAMIC_PRAYER_OPTIONS.ENGINE = SimpleNamespace(
    PYISLAM=ISLAMIC_PRAYER_OPTIONS.ENGINE_PYISLAM,
    ISLAMIC_TIMES=ISLAMIC_PRAYER_OPTIONS.ENGINE_ISLAMIC_TIMES
)
ISLAMIC_PRAYER_OPTIONS.METHOD = SimpleNamespace(
    KARACHI=ISLAMIC_PRAYER_OPTIONS.METHOD_KARACHI,
    MWL=ISLAMIC_PRAYER_OPTIONS.METHOD_MWL,
    EGYPT=ISLAMIC_PRAYER_OPTIONS.METHOD_EGYPT,
    UMM_AL_QURA=ISLAMIC_PRAYER_OPTIONS.METHOD_UMM_AL_QURA,
    ISNA=ISLAMIC_PRAYER_OPTIONS.METHOD_ISNA,
    UOIF=ISLAMIC_PRAYER_OPTIONS.METHOD_UOIF,
    SINGAPORE=ISLAMIC_PRAYER_OPTIONS.METHOD_SINGAPORE,
    RUSSIA=ISLAMIC_PRAYER_OPTIONS.METHOD_RUSSIA,
    FIXED_90=ISLAMIC_PRAYER_OPTIONS.METHOD_FIXED_90,
)
ISLAMIC_PRAYER_OPTIONS.ASR = SimpleNamespace(
    JOMHOR=ISLAMIC_PRAYER_OPTIONS.ASR_SHAFII_MALIKI_HANBALI,
    HANAFI=ISLAMIC_PRAYER_OPTIONS.ASR_HANAFI
)
ISLAMIC_PRAYER_OPTIONS.DST = SimpleNamespace(
    OFF=ISLAMIC_PRAYER_OPTIONS.DST_OFF,
    ON=ISLAMIC_PRAYER_OPTIONS.DST_ON
)
ISLAMIC_PRAYER_OPTIONS.OUTPUT = SimpleNamespace(
    MIDNIGHT=ISLAMIC_PRAYER_OPTIONS.INCLUDE_MIDNIGHT,
    QIYAM_LAST_THIRD=ISLAMIC_PRAYER_OPTIONS.INCLUDE_QIYAM_LAST_THIRD
)


@dataclass(frozen=True)
class IslamicPrayerTimesConfig:
    # Seconds to add/subtract to each prayer time (can be negative)
    # Order: fajr, sunrise, dhuhr, asr, maghrib, isha
    offsets_seconds: Sequence[float] = (0, 0, 0, 0, 0, 0)

    # Hijri correction used by pyIslam
    correction_val: int = 0

    # islamic_times engine config (THIS FIXES YOUR ERROR)
    islamic_times: IslamicTimesConfig = field(default_factory=IslamicTimesConfig)


def islamic_prayer_times(
    jd: float,
    place,
    prayer_options: Optional[Union[ISLAMIC_PRAYER_OPTIONS, int]] = None,
    config: Optional[IslamicPrayerTimesConfig] = None
) -> List[float]:
    """
    Compute prayer times for the Gregorian date corresponding to Julian Day `jd`
    at the given `place`.

    Returns float hours local time:
      [fajr, sunrise, dhuhr, asr, maghrib, isha]
    Optionally appends [midnight] and/or [last_third] if enabled.
    """
    if prayer_options is None:
        prayer_options = ISLAMIC_PRAYER_OPTIONS.DEFAULT
    else:
        prayer_options = ISLAMIC_PRAYER_OPTIONS(prayer_options)

    if config is None:
        config = IslamicPrayerTimesConfig()

    offs = list(config.offsets_seconds)
    if len(offs) != 6:
        raise ValueError("config.offsets_seconds must have 6 elements (fajr..isha)")

    # ---- Choose engine ----
    use_islamic_times = bool(prayer_options & ISLAMIC_PRAYER_OPTIONS.ENGINE_ISLAMIC_TIMES)
    use_pyislam = bool(prayer_options & ISLAMIC_PRAYER_OPTIONS.ENGINE_PYISLAM)

    # If neither engine flag is set, default to pyIslam (backwards compatible)
    if use_islamic_times:
        engine = "islamic_times"
    elif use_pyislam or not (use_islamic_times or use_pyislam):
        engine = "pyislam"
    else:
        engine = "pyislam"

    # ---- Convert Julian Day -> Gregorian date ----
    y, m, d = utils.jd_to_gregorian(jd)[:-1]
    gdate = _date(int(y), int(m), int(floor(d)))

    # ---- Asr madhab mapping ----
    hanafi = bool(prayer_options & ISLAMIC_PRAYER_OPTIONS.ASR_HANAFI)

    # ---- DST handling ----
    dst_on = bool(prayer_options & ISLAMIC_PRAYER_OPTIONS.DST_ON)

    # Helper: unwrap islamic_times Prayer -> .time
    # islamic_times webapp does: t = prayer.time (Prayer dataclass) [1](https://github.com/hassantahan/islamictimes-org/blob/main/app.py)
    def _unwrap_prayer_time(obj: Any) -> Any:
        # islamic_times.it_dataclasses.Prayer has attribute 'time'
        if hasattr(obj, "time"):
            return getattr(obj, "time")
        return obj

    # Helper: convert supported objects to float hour
    def _to_float_hour(obj: Any, tzinfo_local=None) -> float:
        obj = _unwrap_prayer_time(obj)

        # islamic_times may supply datetime or float hour.
        # The demo app handles datetime or numeric values. [1](https://github.com/hassantahan/islamictimes-org/blob/main/app.py)
        if isinstance(obj, (int, float)):
            if math.isinf(obj):
                raise ValueError("Prayer time does not exist (infinite).")
            # treat as hour-of-day decimal
            x = float(obj) % 24.0
            return x

        if isinstance(obj, datetime):
            dt = obj
            # Ensure tz-aware in the same local tz used to build ITLocation
            if dt.tzinfo is None and tzinfo_local is not None:
                dt = dt.replace(tzinfo=tzinfo_local)
            elif tzinfo_local is not None:
                # normalize to local tz for consistent float hour
                dt = dt.astimezone(tzinfo_local)
            return dt.hour + dt.minute / 60.0 + dt.second / 3600.0

        # datetime.time-like
        if hasattr(obj, "hour") and hasattr(obj, "minute"):
            sec = getattr(obj, "second", 0) or 0
            return float(obj.hour) + float(obj.minute) / 60.0 + float(sec) / 3600.0

        # string "HH:MM" or "HH:MM:SS" fallback
        if isinstance(obj, str):
            s = obj.strip()
            parts = s.split(":")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                hh = int(parts[0])
                mm = int(parts[1])
                ss = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 0
                return hh + mm / 60.0 + ss / 3600.0

        raise TypeError(f"Unsupported time type: {type(obj)} value={obj!r}")

    # ======================================================================
    # Engine: islamic_times
    # ======================================================================
    if engine == "islamic_times":
        try:
            from islamic_times.islamic_times import ITLocation
        except ImportError as e:
            raise ImportError(
                "islamic_times engine requested but library not installed. "
                "Install with: pip install islamic_times"
            ) from e

        it_cfg = config.islamic_times

        # Map your flags -> islamic_times method strings (presets).
        # Library supports method presets and custom angles. [2](https://pypi.org/project/islamic-times/)[1](https://github.com/hassantahan/islamictimes-org/blob/main/app.py)
        method_string = it_cfg.method_fallback
        if prayer_options & ISLAMIC_PRAYER_OPTIONS.METHOD_ISNA:
            method_string = "ISNA"
        elif prayer_options & ISLAMIC_PRAYER_OPTIONS.METHOD_MWL:
            method_string = "MWL"
        elif prayer_options & ISLAMIC_PRAYER_OPTIONS.METHOD_EGYPT:
            method_string = "Egyptian"
        elif prayer_options & ISLAMIC_PRAYER_OPTIONS.METHOD_UMM_AL_QURA:
            method_string = "Umm al-Qura"
        elif prayer_options & ISLAMIC_PRAYER_OPTIONS.METHOD_KARACHI:
            method_string = "Karachi"
        else:
            method_string = it_cfg.method_fallback

        asr_type = 1 if hanafi else 0  # 0 standard, 1 hanafi

        # Build timezone-aware datetime at local noon for stability
        tz_hours = float(place.timezone) + (1.0 if dst_on else 0.0)
        tzinfo = timezone(timedelta(hours=tz_hours))
        local_noon = datetime(gdate.year, gdate.month, gdate.day, 12, 0, 0, tzinfo=tzinfo)
        place_elevation = utils.get_elevation(place.latitude, place.longitude)
        loc = ITLocation(
            latitude=float(place.latitude),
            longitude=float(place.longitude),
            elevation=place_elevation if place_elevation > 0.0 else float(it_cfg.elevation),
            temperature=float(it_cfg.temperature),
            pressure=float(it_cfg.pressure),
            date=local_noon,
            method=str(method_string),
            find_local_tz=bool(it_cfg.find_local_tz),
        )
        # Apply asr/midnight options if available
        if hasattr(loc, "set_asr_type"):
            loc.set_asr_type(int(asr_type))
        elif hasattr(loc, "asr_type"):
            try:
                setattr(loc, "asr_type", int(asr_type))
            except Exception:
                pass

        if hasattr(loc, "set_midnight_type"):
            loc.set_midnight_type(int(it_cfg.midnight_type))
        elif hasattr(loc, "midnight_type"):
            try:
                setattr(loc, "midnight_type", int(it_cfg.midnight_type))
            except Exception:
                pass

        # Optional custom angles
        if it_cfg.custom_angles and hasattr(loc, "set_custom_prayer_angles"):
            fa, ma, ia = it_cfg.custom_angles
            loc.set_custom_prayer_angles(float(fa), float(ma), float(ia))

        prayers = loc.prayer_times()

        # Pull Prayer objects (or times) from PrayerTimes dataclass
        # The webapp accesses: getattr(times, "fajr").time etc. [1](https://github.com/hassantahan/islamictimes-org/blob/main/app.py)
        fajr = getattr(prayers, "fajr")
        sunrise = getattr(prayers, "sunrise")
        # islamic_times uses "zuhr" attribute name in its app example [1](https://github.com/hassantahan/islamictimes-org/blob/main/app.py)
        zuhr = getattr(prayers, "zuhr", getattr(prayers, "dhuhr", None))
        asr = getattr(prayers, "asr")
        maghrib = getattr(prayers, "maghrib")
        isha = getattr(prayers, "isha")

        if zuhr is None:
            raise AttributeError("Could not find zuhr/dhuhr attribute in islamic_times PrayerTimes result.")

        times = [
            _to_float_hour(fajr, tzinfo) + offs[0] / 3600.0,
            _to_float_hour(sunrise, tzinfo) + offs[1] / 3600.0,
            _to_float_hour(zuhr, tzinfo) + offs[2] / 3600.0,
            _to_float_hour(asr, tzinfo) + offs[3] / 3600.0,
            _to_float_hour(maghrib, tzinfo) + offs[4] / 3600.0,
            _to_float_hour(isha, tzinfo) + offs[5] / 3600.0,
        ]

        # Optional extras
        if prayer_options & ISLAMIC_PRAYER_OPTIONS.INCLUDE_MIDNIGHT:
            midnight = getattr(prayers, "midnight", None)
            if midnight is not None:
                times.append(_to_float_hour(midnight, tzinfo))
            else:
                # fallback midpoint sunset->sunrise
                sunset = getattr(prayers, "sunset")
                ss = _to_float_hour(sunset, tzinfo)
                sr = _to_float_hour(sunrise, tzinfo)
                mid = (ss + sr + 24.0) / 2.0
                while mid >= 24.0:
                    mid -= 24.0
                times.append(mid)

        if prayer_options & ISLAMIC_PRAYER_OPTIONS.INCLUDE_QIYAM_LAST_THIRD:
            start = _to_float_hour(maghrib, tzinfo)
            end = _to_float_hour(fajr, tzinfo)
            if end <= start:
                end += 24.0
            night_len = end - start
            last_third_start = end - night_len / 3.0
            while last_third_start >= 24.0:
                last_third_start -= 24.0
            times.append(last_third_start)

        return times

    # ======================================================================
    # Engine: pyIslam (existing implementation)
    # ======================================================================

    method_map = {
        ISLAMIC_PRAYER_OPTIONS.METHOD_KARACHI: 1,
        ISLAMIC_PRAYER_OPTIONS.METHOD_MWL: 2,
        ISLAMIC_PRAYER_OPTIONS.METHOD_EGYPT: 3,
        ISLAMIC_PRAYER_OPTIONS.METHOD_UMM_AL_QURA: 4,
        ISLAMIC_PRAYER_OPTIONS.METHOD_ISNA: 5,
        ISLAMIC_PRAYER_OPTIONS.METHOD_UOIF: 6,
        ISLAMIC_PRAYER_OPTIONS.METHOD_SINGAPORE: 7,
        ISLAMIC_PRAYER_OPTIONS.METHOD_RUSSIA: 8,
        ISLAMIC_PRAYER_OPTIONS.METHOD_FIXED_90: 9,
    }

    chosen_method_id = 5
    for flag, mid in method_map.items():
        if prayer_options & flag:
            chosen_method_id = mid
            break

    if not (1 <= chosen_method_id <= len(LIST_FAJR_ISHA_METHODS)):
        chosen_method_id = 5

    asr_madhab = 2 if hanafi else 1
    enable_summer_time = dst_on

    pconf = PrayerConf(
        float(place.longitude),
        float(place.latitude),
        float(place.timezone),
        int(chosen_method_id),
        int(asr_madhab),
        bool(enable_summer_time),
    )

    p = Prayer(pconf, gdate, correction_val=int(config.correction_val))

    def _t2h(t) -> float:
        return t.hour + (t.minute / 60.0) + (t.second / 3600.0)

    times = [
        _t2h(p.fajr_time(shift=offs[0])),
        _t2h(p.sherook_time(shift=offs[1])),
        _t2h(p.dohr_time(shift=offs[2])),
        _t2h(p.asr_time(shift=offs[3])),
        _t2h(p.maghreb_time(shift=offs[4])),
        _t2h(p.ishaa_time(shift=offs[5])),
    ]

    if prayer_options & ISLAMIC_PRAYER_OPTIONS.INCLUDE_MIDNIGHT:
        times.append(_t2h(p.midnight()))
    if prayer_options & ISLAMIC_PRAYER_OPTIONS.INCLUDE_QIYAM_LAST_THIRD:
        times.append(_t2h(p.last_third_of_night()))

    return times

# ==========================================================
# Everything below is your Hijri logic (UNCHANGED)
# (Only HTML escapes fixed, and small print bugs fixed)
# ==========================================================

class ISLAMIC_OPTIONS(IntFlag):
    METHOD_HIJRIDATE = auto()
    METHOD_CALCULATED = auto()

    POLICY_LOCAL = auto()
    POLICY_ANCHOR_PLACE = auto()
    POLICY_GLOBAL_VISIBILITY = auto()

    CRITERIA_MOONSET_ONLY = auto()
    CRITERIA_AGE_LAG_ELONG = auto()
    CRITERIA_ECFR_8_5 = auto()

    BOUNDARY_SUNSET = auto()
    BOUNDARY_MIDNIGHT = auto()

    LABEL_TABULAR = auto()

    DEFAULT = METHOD_HIJRIDATE | BOUNDARY_MIDNIGHT


ISLAMIC_OPTIONS.METHOD = SimpleNamespace(
    HIJRDATE=ISLAMIC_OPTIONS.METHOD_HIJRIDATE,
    CALCULATED=ISLAMIC_OPTIONS.METHOD_CALCULATED
)
ISLAMIC_OPTIONS.POLICY = SimpleNamespace(
    LOCAL=ISLAMIC_OPTIONS.POLICY_LOCAL,
    ANCHOR_PLACE=ISLAMIC_OPTIONS.POLICY_ANCHOR_PLACE,
    GLOBAL_VISIBILITY=ISLAMIC_OPTIONS.POLICY_GLOBAL_VISIBILITY
)
ISLAMIC_OPTIONS.CRITERIA = SimpleNamespace(
    MOONSET_ONLY=ISLAMIC_OPTIONS.CRITERIA_MOONSET_ONLY,
    AGE_LAG_ELONG=ISLAMIC_OPTIONS.CRITERIA_AGE_LAG_ELONG,
    ECFR_8_5=ISLAMIC_OPTIONS.CRITERIA_ECFR_8_5
)
ISLAMIC_OPTIONS.BOUNDARY = SimpleNamespace(
    SUNSET=ISLAMIC_OPTIONS.BOUNDARY_SUNSET,
    MIDNIGHT=ISLAMIC_OPTIONS.BOUNDARY_MIDNIGHT
)
ISLAMIC_OPTIONS.LABEL = SimpleNamespace(
    TABULAR=ISLAMIC_OPTIONS.LABEL_TABULAR
)


@dataclass(frozen=True)
class HijriCriteriaConfig:
    min_age_hours: float = 18.0
    min_lag_minutes: float = 40.0
    min_elong_deg: float = 10.0
    at_pressure_mbar: float = 1013.25
    at_temperature_c: float = 15.0
    observer_alt_m: float = 0.0
    scan_days: int = 3
    lon_step_deg: int = 15
    lat_samples: Tuple[float, ...] = (-30.0, 0.0, 30.0)
    use_solar_tz_for_scan: bool = True
    global_pick: str = "earliest"


GREENWICH = drik.Place("Greenwich", 0.0, 0.0, 0.0)


def _jd_to_ut(jd_local: float, place) -> float:
    return jd_local - place.timezone / 24.0


def _ut_to_local(jd_ut: float, place) -> float:
    return jd_ut + place.timezone / 24.0


def _get_boundary_start(jd_local: float, place, options: ISLAMIC_OPTIONS) -> float:
    if options & ISLAMIC_OPTIONS.BOUNDARY.MIDNIGHT:
        return math.floor(jd_local + 0.5) - 0.5
    ss_today = drik.sunset(jd_local, place)[2]
    return ss_today if jd_local >= ss_today else drik.sunset(jd_local - 1.0, place)[2]


def _get_conjunction_ut(jd_probe_ut: float) -> float:
    jd_ref = _ut_to_local(jd_probe_ut, GREENWICH)
    tithi_idx = drik.tithi(jd_ref, GREENWICH)[0]
    nm_local = drik.new_moon(jd_ref, tithi_idx, opt=-1)
    return _jd_to_ut(nm_local, GREENWICH)


def _is_visible(ss_local: float, place, nm_ut: float, options: ISLAMIC_OPTIONS, cfg: HijriCriteriaConfig) -> bool:
    nm_local = _ut_to_local(nm_ut, place)
    if ss_local <= nm_local:
        return False
    ms_local = drik.moonset(ss_local, place)[2]
    if ms_local <= ss_local:
        return False
    if options & ISLAMIC_OPTIONS.CRITERIA.MOONSET_ONLY:
        return True
    jd_ut = _jd_to_ut(ss_local, place)
    elon = (drik.lunar_longitude(jd_ut) - drik.solar_longitude(jd_ut)) % 360.0
    elon = 360.0 - elon if elon > 180.0 else elon
    if options & ISLAMIC_OPTIONS.CRITERIA.AGE_LAG_ELONG:
        age = (ss_local - nm_local) * 24.0
        lag = (ms_local - ss_local) * 1440.0
        return age >= cfg.min_age_hours and lag >= cfg.min_lag_minutes and elon >= cfg.min_elong_deg
    if options & ISLAMIC_OPTIONS.CRITERIA.ECFR_8_5:
        swe.set_topo(float(place.longitude), float(place.latitude), float(cfg.observer_alt_m))
        flags = swe.FLG_EQUATORIAL | swe.FLG_TOPOCTR
        pos, _ = swe.calc_ut(jd_ut, swe.MOON, flags)
        _, alt, _ = swe.azalt(
            jd_ut, swe.EQU2HOR,
            [float(place.longitude), float(place.latitude), float(cfg.observer_alt_m)],
            cfg.at_pressure_mbar, cfg.at_temperature_c,
            [pos[0], pos[1], pos[2]]
        )
        return elon >= 8.0 and alt >= 5.0
    return False


_TRIGGER_CACHE: Dict[Tuple, float] = {}


def _find_trigger_ut(nm_ut: float, place, options: ISLAMIC_OPTIONS, cfg: HijriCriteriaConfig, anchor=None) -> float:
    key = (round(nm_ut, 4), int(options), getattr(anchor, "Place", None) if anchor else None)
    if key in _TRIGGER_CACHE:
        return _TRIGGER_CACHE[key]

    if options & ISLAMIC_OPTIONS.POLICY.LOCAL:
        search_places = [place]
    elif options & ISLAMIC_OPTIONS.POLICY.ANCHOR_PLACE:
        search_places = [anchor]
    else:
        search_places = []
        for lat in cfg.lat_samples:
            for lon in range(-180, 181, cfg.lon_step_deg):
                search_places.append(drik.Place("SCAN", float(lat), float(lon), lon / 15.0))

    best_ut = None
    for day in range(cfg.scan_days):
        for p in search_places:
            ss_l = drik.sunset(_ut_to_local(nm_ut, p) + 0.2 + day, p)[2]
            if _is_visible(ss_l, p, nm_ut, options, cfg):
                ut = _jd_to_ut(ss_l, p)
                if best_ut is None or ut < best_ut:
                    best_ut = ut
        if best_ut is not None:
            break

    res = best_ut if best_ut else nm_ut + 2.0
    _TRIGGER_CACHE[key] = res
    return res


def _get_month_start_boundary(nm_ut: float, place, options: ISLAMIC_OPTIONS, cfg: HijriCriteriaConfig, anchor=None) -> float:
    trig_ut = _find_trigger_ut(nm_ut, place, options, cfg, anchor)
    trig_l = _ut_to_local(trig_ut, place)
    if options & ISLAMIC_OPTIONS.BOUNDARY.MIDNIGHT:
        m_start = math.floor(trig_l + 0.5) - 0.5
        return m_start if m_start >= trig_l else m_start + 1.0
    ss = drik.sunset(trig_l, place)[2]
    return ss if ss >= trig_l else drik.sunset(ss + 1.1, place)[2]


def _islamic_from_jd_tabular(jd: float) -> Tuple[int, int, int]:
    days = math.floor(jd + 0.5) - math.floor(1948439.5 + 0.5) + 1
    year = int(math.floor((30 * days + 10646) / 10631))
    first = (year - 1) * 354 + math.floor((3 + 11 * year) / 30)
    month = int(min(12, math.ceil((days - first) / 29.5)))
    day = int(days - first - math.ceil(29.5 * (month - 1)))
    return year, max(1, min(12, month)), max(1, min(30, day))


def islamic_lunar_date(jd: float, place=None, options=None, cfg=None, anchor_place=None) -> Tuple[int, int, int]:
    if options is None:
        options = ISLAMIC_OPTIONS.DEFAULT

    if options & ISLAMIC_OPTIONS.METHOD_HIJRIDATE:
        from hijridate import Gregorian
        y, m, d, _ = utils.jd_to_gregorian(jd)
        h = Gregorian(y, m, d).to_hijri()
        return h.year, h.month, h.day

    if place is None:
        raise ValueError("Place argument is required for METHOD_CALCULATED")
    if cfg is None:
        cfg = HijriCriteriaConfig()

    current_boundary = _get_boundary_start(jd, place, options)
    probe_ut = _jd_to_ut(current_boundary + 0.5, place)
    nm_ut = _get_conjunction_ut(probe_ut)
    month_start = _get_month_start_boundary(nm_ut, place, options, cfg, anchor_place)

    if current_boundary < (month_start - 0.001):
        nm_ut = _get_conjunction_ut(_jd_to_ut(month_start - 5.0, place))
        month_start = _get_month_start_boundary(nm_ut, place, options, cfg, anchor_place)

    day = int(round(current_boundary - month_start)) + 1
    y, m, _ = _islamic_from_jd_tabular(month_start + 5.0)
    return y, m, day


def run_option_matrix_tests(jd: float, place, anchor_place):
    policies = [
        ("LOCAL", ISLAMIC_OPTIONS.POLICY.LOCAL),
        ("ANCHOR", ISLAMIC_OPTIONS.POLICY.ANCHOR_PLACE),
        ("GLOBAL", ISLAMIC_OPTIONS.POLICY.GLOBAL_VISIBILITY),
    ]
    criteria = [
        ("MOONSET_ONLY", ISLAMIC_OPTIONS.CRITERIA.MOONSET_ONLY),
        ("AGE_LAG_ELONG", ISLAMIC_OPTIONS.CRITERIA.AGE_LAG_ELONG),
        ("ECFR_8_5", ISLAMIC_OPTIONS.CRITERIA.ECFR_8_5),
    ]
    boundaries = [
        ("SUNSET", ISLAMIC_OPTIONS.BOUNDARY.SUNSET),
        ("MIDNIGHT", ISLAMIC_OPTIONS.BOUNDARY.MIDNIGHT),
    ]

    cfg = HijriCriteriaConfig()

    for b_name, b_flag in boundaries:
        print("\n=== Boundary:", b_name, "===")
        for p_name, p_flag in policies:
            for c_name, c_flag in criteria:
                opts = (ISLAMIC_OPTIONS.METHOD_CALCULATED | p_flag | c_flag | b_flag | ISLAMIC_OPTIONS.LABEL_TABULAR)
                try:
                    res = islamic_lunar_date(jd, place, options=opts, cfg=cfg, anchor_place=anchor_place)
                    print(f"{p_name:6} {c_name:12} -> {res}")
                except Exception as e:
                    print(f"{p_name:6} {c_name:12} -> ERROR: {e}")


# ==========================================================
# Simple test runner (prints both engines)
# ==========================================================

def _format_prayer_times(times: List[float]) -> List[str]:
    # Try your jhora resource strings, but don't crash if extra items exist.
    label_keys = [
        "fajr_str", "shurook_str", "dhuhr_str", "asr_str", "maghrib_str", "isha_str",
        "midnight_str", "last_third_str"
    ]
    out = []
    for i, t in enumerate(times):
        if i < len(label_keys) and label_keys[i] in getattr(utils, "resource_strings", {}):
            label = utils.resource_strings[label_keys[i]]
        else:
            # Fallback labels
            fallback = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", "Midnight", "LastThird"]
            label = fallback[i] if i < len(fallback) else f"T{i+1}"
        out.append(f"{label}:{utils.to_dms(t)}")
    return out


if __name__ == "__main__":
    utils.set_language('ta')
    Date = drik.Date
    Place = drik.Place

    chicago = Place("Chicago,US", 41.85, -87.65, -5.0)
    mecca = Place("Mecca",21.42664,39.82563,+3.0)
    dob = Date(2026, 4, 1)
    tob = (8, 30, 0)
    jd = utils.julian_day_number(dob, tob)

    # --- pyIslam test (default engine if no engine flag is given) ---
    times_pyislam = islamic_prayer_times(
        jd,
        chicago,
        prayer_options=(
            ISLAMIC_PRAYER_OPTIONS.METHOD.ISNA |
            ISLAMIC_PRAYER_OPTIONS.ASR.JOMHOR |
            ISLAMIC_PRAYER_OPTIONS.DST.OFF
        ),
        config=IslamicPrayerTimesConfig()
    )
    print("pyIslam:", _format_prayer_times(times_pyislam))

    # --- islamic_times test ---
    opts_it = (
        ISLAMIC_PRAYER_OPTIONS.ENGINE.ISLAMIC_TIMES |
        ISLAMIC_PRAYER_OPTIONS.METHOD.MWL |
        ISLAMIC_PRAYER_OPTIONS.ASR.HANAFI |
        ISLAMIC_PRAYER_OPTIONS.OUTPUT.MIDNIGHT
    )

    cfg_it = IslamicPrayerTimesConfig(
        offsets_seconds=(0, 0, 0, 0, 0, 0),
        islamic_times=IslamicTimesConfig(
            elevation=250.0,
            find_local_tz=False,
            midnight_type=1
        )
    )

    times_it = islamic_prayer_times(jd, chicago, opts_it, cfg_it)
    print("islamic_times:", _format_prayer_times(times_it))
    # loop for 60 days
    for d in range(60):
        # 1. default: hijridate (table)
        table_y, table_m, table_d = islamic_lunar_date(jd)
        
        # 2. calculated model (sighting)
        calc_y, calc_m, calc_d = islamic_lunar_date(
            jd, chicago,
            options=(ISLAMIC_OPTIONS.METHOD_CALCULATED |
                     ISLAMIC_OPTIONS.POLICY.GLOBAL_VISIBILITY |
                     ISLAMIC_OPTIONS.CRITERIA.ECFR_8_5 |
                     ISLAMIC_OPTIONS.BOUNDARY.SUNSET |
                     ISLAMIC_OPTIONS.LABEL_TABULAR),
            cfg=HijriCriteriaConfig(),
            anchor_place=mecca
        )

        g = utils.jd_to_gregorian(jd)
        print(f"{g[:3]}", 
              (table_y, utils.ISLAMIC_MONTH_LIST[table_m-1], table_d),
              (calc_y, utils.ISLAMIC_MONTH_LIST[calc_m-1], calc_d))
        jd += 1

    # Matrix test for a specific date
    jd_test = utils.julian_day_number(Date(2026, 4, 19), (8, 30, 0))
    run_option_matrix_tests(jd_test, chicago, mecca)
