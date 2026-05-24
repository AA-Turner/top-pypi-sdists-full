"""
soil.py — derive AquaCrop hydraulic parameters from SoilGrids 5 km TIFs.

Pipeline:
    1.  Read 5 km SoilGrids products produced by geoprepare/datasets/SOILGRIDS.py:
            ${dir_intermed}/soilgrids/tif/sand_0-30cm.tif    (g/kg)
            ${dir_intermed}/soilgrids/tif/clay_0-30cm.tif    (g/kg)
            ${dir_intermed}/soilgrids/tif/soc_0-30cm.tif     (dg/kg)
            ${dir_intermed}/soilgrids/tif/bdod_0-30cm.tif    (cg/cm³)
        These are pre-aggregated via depth-weighted mean to a single
        rooting-zone layer (0-30 cm by default; configurable via
        [AQUACROP] soil_depth_cm).
    2.  Per cell: read sand/clay/SOC/BD via single-pixel rasterio.read with
        Window. Cache the four open datasets across the cell loop.
    3.  Apply Saxton-Rawls (2006) pedotransfer functions to obtain:
            θWP  — wilting point (m³/m³)
            θFC  — field capacity (m³/m³)
            θS   — saturation (m³/m³)
            Ksat — saturated hydraulic conductivity (mm/day)
    4.  Wrap into an aquacrop.Soil object via add_layer(thickness, ...).

Mean-aggregation of inputs THEN apply Saxton-Rawls (locked-in Q4).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

import numpy as np
import rasterio
from rasterio.windows import Window

logger = logging.getLogger(__name__)


# SoilGrids unit conversions (g/kg → % sand/clay, dg/kg → % OC, etc.)
SOILGRIDS_CONV = {
    "sand": 0.1,    # g/kg → %
    "clay": 0.1,    # g/kg → %
    "soc": 0.01,    # dg/kg → % (÷10 for g/kg, ÷10 for %)
    "bdod": 0.01,   # cg/cm³ → g/cm³
}

# OC → OM multiplier (Van Bemmelen factor)
OC_TO_OM = 1.724


def _country_slug(country: str) -> str:
    """Mirror of geoprepare.datasets.SOILGRIDS._country_slug."""
    return country.lower().replace(" ", "_")


def _soilgrids_path(
    intermed_dir: Path, country: str, var: str, depth_cm: int,
) -> Path:
    """Construct path for SoilGrids 5 km product (per-country, geoprepare 0.6.242+)."""
    return (
        intermed_dir / "soilgrids" / _country_slug(country) / "tif"
        / f"{var}_0-{depth_cm}cm.tif"
    )


class SoilReader:
    """Per-worker soil property reader.

    Opens the 4 SoilGrids TIFs once and reads single pixels via Window
    for the cell-by-cell loop. Cheap to construct, holds 4 file handles.
    """

    def __init__(self, parser, country: str):
        # Initialize FIRST so __del__ → close() never races a partial init
        # (if any subsequent parser.get / getint raises before this attr is
        # set, __del__ would otherwise hit AttributeError and bury the real
        # traceback).
        self._datasets: dict[str, Optional[rasterio.DatasetReader]] = {}
        self.parser = parser
        self.country = country
        self.dir_intermed = Path(parser.get("PATHS", "dir_intermed"))
        self.depth = parser.getint("AQUACROP", "soil_depth_cm", fallback=30)

        for var in ("sand", "clay", "soc", "bdod"):
            path = _soilgrids_path(self.dir_intermed, country, var, self.depth)
            if not path.is_file():
                logger.warning(f"SoilGrids missing: {path}")
                self._datasets[var] = None
                continue
            try:
                self._datasets[var] = rasterio.open(path)
            except (rasterio.RasterioIOError, OSError) as exc:
                logger.warning(f"Cannot open {path}: {exc}")
                self._datasets[var] = None

    def close(self) -> None:
        for ds in self._datasets.values():
            if ds is not None:
                try:
                    ds.close()
                except Exception:  # noqa: BLE001
                    pass
        self._datasets.clear()

    def __del__(self):
        self.close()

    def _read_pixel(self, var: str, lon: float, lat: float) -> Optional[float]:
        ds = self._datasets.get(var)
        if ds is None:
            return None
        try:
            col, row = ~ds.transform * (lon, lat)
            col, row = int(col), int(row)
            if not (0 <= row < ds.height and 0 <= col < ds.width):
                return None
            val = ds.read(1, window=Window(col, row, 1, 1))[0, 0]
            if val == ds.nodata:
                return None
            return float(val) * SOILGRIDS_CONV[var]
        except (ValueError, IndexError, rasterio.RasterioIOError):
            return None

    def get_properties(
        self, lon: float, lat: float,
    ) -> Optional[dict[str, float]]:
        """Read sand/clay/OM/BD at one cell. Returns None if any missing."""
        sand = self._read_pixel("sand", lon, lat)
        clay = self._read_pixel("clay", lon, lat)
        soc = self._read_pixel("soc", lon, lat)
        bd = self._read_pixel("bdod", lon, lat)

        if any(v is None for v in (sand, clay, soc, bd)):
            return None

        om = soc * OC_TO_OM

        # Plausibility: sand+clay should be < 100, OM < 30, BD in 0.5-2.0.
        if sand + clay > 100 or not 0 < om < 30 or not 0.5 < bd < 2.0:
            logger.debug(
                f"Implausible soil at ({lon:.3f}, {lat:.3f}): "
                f"sand={sand:.1f} clay={clay:.1f} OM={om:.2f} BD={bd:.2f}"
            )
            return None

        return {"sand": sand, "clay": clay, "om": om, "bd": bd}


def saxton_rawls_2006(
    sand_pct: float, clay_pct: float, om_pct: float, bd: float = 1.3,
) -> dict[str, float]:
    """Saxton-Rawls (2006) pedotransfer functions for soil hydraulic params.

    Inputs are fractions in 0-1 internally; accepts percentages 0-100.
    Reference: Saxton & Rawls, SSSAJ 70:1569-1578 (2006).

    Returns dict with keys:
        thWP  — wilting point at 1500 kPa (m³/m³)
        thFC  — field capacity at 33 kPa (m³/m³)
        thS   — saturation (m³/m³)
        Ksat  — saturated conductivity (mm/day)
    """
    S = sand_pct / 100.0
    C = clay_pct / 100.0
    OM = om_pct / 100.0

    # Wilting point (Eq. 1 from Saxton-Rawls 2006)
    theta_1500t = (
        -0.024 * S + 0.487 * C + 0.006 * OM
        + 0.005 * S * OM - 0.013 * C * OM
        + 0.068 * S * C + 0.031
    )
    theta_1500 = theta_1500t + (0.14 * theta_1500t - 0.02)

    # Field capacity (Eq. 2)
    theta_33t = (
        -0.251 * S + 0.195 * C + 0.011 * OM
        + 0.006 * S * OM - 0.027 * C * OM
        + 0.452 * S * C + 0.299
    )
    theta_33 = theta_33t + (1.283 * theta_33t ** 2 - 0.374 * theta_33t - 0.015)

    # Saturation - PAW (Eq. 3)
    theta_s33t = (
        0.278 * S + 0.034 * C + 0.022 * OM
        - 0.018 * S * OM - 0.027 * C * OM
        - 0.584 * S * C + 0.078
    )
    theta_s33 = theta_s33t + (0.636 * theta_s33t - 0.107)
    theta_s = theta_33 + theta_s33 - 0.097 * S + 0.043

    # Saturated hydraulic conductivity (Eq. 16)
    if theta_s - theta_33 <= 0 or theta_33 <= theta_1500:
        # Degenerate texture — fall back to a typical loam
        return {"thWP": 0.15, "thFC": 0.28, "thS": 0.45, "Ksat": 1200.0}

    lambda_ = (np.log(theta_33) - np.log(theta_1500)) / \
              (np.log(1500.0) - np.log(33.0))
    ksat_mm_hr = 1930.0 * np.power(theta_s - theta_33, 3.0 - lambda_)
    ksat_mm_day = ksat_mm_hr * 24.0

    # Plausibility clamps
    theta_1500 = float(np.clip(theta_1500, 0.02, 0.35))
    theta_33 = float(np.clip(theta_33, theta_1500 + 0.05, 0.50))
    theta_s = float(np.clip(theta_s, theta_33 + 0.05, 0.60))
    ksat_mm_day = float(np.clip(ksat_mm_day, 10.0, 5000.0))

    return {
        "thWP": theta_1500,
        "thFC": theta_33,
        "thS": theta_s,
        "Ksat": ksat_mm_day,
    }


def build_aquacrop_soil(props: dict[str, float]):
    """Wrap soil properties into an aquacrop.Soil object.

    Builds a single 1.5 m custom layer — adequate for annual crops since
    max root depth in AquaCrop's default crops is < 1.5 m. Caller has
    already filtered out implausible cells via SoilReader.get_properties.

    Args:
        props: dict with keys sand, clay, om, bd (percentages and g/cm³).

    Returns:
        aquacrop.Soil object with one calibrated layer.
    """
    # Import here so the module is importable in environments without
    # aquacrop installed (e.g. when running just the data prep step).
    from aquacrop import Soil

    hyd = saxton_rawls_2006(props["sand"], props["clay"], props["om"], props["bd"])

    soil = Soil(soil_type="custom")
    soil.add_layer(
        thickness=1.5,           # m
        thWP=hyd["thWP"],
        thFC=hyd["thFC"],
        thS=hyd["thS"],
        Ksat=hyd["Ksat"],
        penetrability=100,
    )
    return soil
