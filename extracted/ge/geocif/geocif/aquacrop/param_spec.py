"""
param_spec.py — wrap tunable AquaCrop crop parameters for the PyGMO
calibration loop.

Adapted from the EPIC reference at
``D:/Users/ritvik/projects/crop_models/kenya_maize/geoepic/io/cropcom.py``
(CropCom class) — keeps the same 5-method interface (constraints,
var_names, current, edit, apply) so AquaCropPygmoProblem can drive
multiple AquaCropParamSpec instances generically.

Difference from CropCom: AquaCrop crops are Python objects, not .DAT
files. We don't read/write files; we mutate ``aquacrop.Crop`` attributes
in memory via ``apply(crop_obj)``.

Bound provenance:
    SSA literature ranges (Ngetich 2012, Akumaga 2017, Mhizha 2014,
    Hadebe 2017, Bello & Walker 2016, Kanda 2021, Araya 2011, ...) for
    Maize / Sorghum / PearlMillet / Cowpea / Tef. Where the literature
    range disagrees with smallholder reality (e.g. HI0 Maize = 0.40-0.50
    for well-managed trials vs ~0.10-0.20 actually realised in rainfed
    subsistence systems), the lower bound is widened to allow PSO to
    fit yield-gap-adjusted values without losing the commercial upper.

    For commercial-farming runs, narrow the bounds at the top of
    ``_DEFAULT_BOUNDS`` or pass ``bounds_override`` to the spec.
"""

from __future__ import annotations

from typing import Optional

import numpy as np


# Per-crop tunable parameter table. Each entry maps the AquaCrop-OSPy
# attribute name to its (low, high) PSO search range.
#
# Sources per crop noted inline; see also
# ``D:/Users/ritvik/projects/geocif/docs/aquacrop_africa_calibration_parameters.csv``
# for the full literature-derived table.
_DEFAULT_BOUNDS: dict[str, dict[str, tuple[float, float]]] = {
    # ------------------------- Maize -------------------------------------
    # Refs: Ngetich 2012, Akumaga 2017, Mhizha 2014, Hsiao 2009, Vanuytrecht 2014
    "Maize": {
        # Reference harvest index. Lit 0.40-0.50; lower widened for SSA
        # smallholder yield gap (rainfed, nutrient-limited, harvest losses).
        "HI0":        (0.15, 0.50),
        # Normalised water productivity (C4). Lit 30-35 g/m^2; lower
        # widened to capture realised WP under nutrient stress.
        "WP":         (10.0, 35.0),
        # Max canopy cover. Lit 0.65-0.90; lower widened for sparse
        # smallholder stands.
        "CCx":        (0.50, 0.90),
        # Canopy growth coefficient (fraction/GDD). Lit 0.008-0.013.
        "CGC":        (0.006, 0.013),
        # Canopy decline coefficient (fraction/GDD). Lit 0.006-0.012.
        "CDC":        (0.006, 0.013),
        # Max effective rooting depth (m). Lit 0.6-1.7; AquaCrop default
        # 2.3 is unrealistically deep for shallow tropical soils — this
        # range is the single biggest lever on year-to-year variability
        # in water-limited systems.
        "Zmax":       (0.6, 1.7),
        # GDD to flowering (start of HI build-up). Lit 750-1100.
        "HIstart":    (700.0, 1100.0),
        # GDD duration of flowering. Lit 150-250.
        "Flowering":  (150.0, 250.0),
        # GDD to senescence. Lit 1200-1700.
        "Senescence": (1200.0, 1700.0),
        # GDD to maturity. Lit 1400-2200.
        "Maturity":   (1400.0, 2200.0),
        # GDD to emergence. Lit 60-110.
        "Emergence":  (60.0, 110.0),
        # GDD to max rooting. Lit 500-900.
        "MaxRooting": (500.0, 900.0),
        # Stress thresholds (medium priority). Refs Vanuytrecht 2014,
        # Mhizha 2014, Akumaga 2017.
        "p_up1":      (0.10, 0.30),
        "p_up2":      (0.45, 0.70),
        "p_up3":      (0.65, 0.85),
    },
    # ------------------------- Sorghum -----------------------------------
    # Refs: Hadebe 2017, Araya 2016
    "Sorghum": {
        # Lit HI0 0.35-0.42; lower widened for SSA smallholder.
        "HI0":        (0.15, 0.42),
        # Lit WP 30-33 g/m^2; lower widened.
        "WP":         (10.0, 33.0),
        # Lit CCx 0.75-0.85; lower widened.
        "CCx":        (0.50, 0.85),
        # Lit Zmax 1.5-2.0 m; lower widened slightly.
        "Zmax":       (0.8, 2.0),
        # Lit Maturity 1700-2500 GDD.
        "Maturity":   (1700.0, 2500.0),
        # Lit p_up2 (stomatal closure) 0.70-0.80.
        "p_up2":      (0.55, 0.80),
        "CGC":        (0.006, 0.013),
    },
    # ----------------------- Pearl Millet --------------------------------
    # Refs: Bello & Walker 2016, Karunaratne 2011
    # Note: AquaCrop-OSPy does not ship Pearl Millet by default; this
    # entry supports a future custom Crop registration.
    "PearlMillet": {
        "HI0":        (0.10, 0.30),
        "WP":         (10.0, 33.0),
        "CCx":        (0.45, 0.75),
        "Zmax":       (0.8, 2.0),
        "Maturity":   (1300.0, 1700.0),
        "p_up2":      (0.55, 0.80),
    },
    # ------------------------- Cowpea ------------------------------------
    # Refs: Kanda 2021
    # Not shipped by AquaCrop-OSPy default; entry ready for custom Crop.
    "Cowpea": {
        "HI0":        (0.10, 0.30),
        "WP":         (10.0, 17.0),
        "CCx":        (0.50, 0.85),
        "Zmax":       (0.6, 1.5),
    },
    # ------------------------- Tef ---------------------------------------
    # Refs: Araya 2011
    "Tef": {
        "HI0":        (0.10, 0.25),
        "WP":         (10.0, 17.0),
        "CCx":        (0.50, 0.80),
        "Zmax":       (0.4, 1.2),
    },
    # ------------------ Non-SSA / commercial crops -----------------------
    # Kept at the pre-CSV smallholder-conservative bounds. Bump the upper
    # bounds back toward FAO commercial defaults if running these in
    # well-managed contexts (US Midwest maize, Argentina soy, etc.).
    "MaizeGDD":  {"HI0": (0.15, 0.50), "WP": (10.0, 35.0), "CCx": (0.50, 0.90),
                  "CGC": (0.006, 0.013), "Zmax": (0.6, 1.7)},
    "Wheat":     {"HI0": (0.15, 0.45), "WP": (8.0, 17.0),  "CCx": (0.55, 0.95)},
    "WheatGDD":  {"HI0": (0.15, 0.45), "WP": (8.0, 17.0),  "CCx": (0.55, 0.95)},
    "Rice":      {"HI0": (0.20, 0.45), "WP": (10.0, 19.0), "CCx": (0.65, 0.95)},
    "PaddyRice": {"HI0": (0.25, 0.50), "WP": (13.0, 19.0), "CCx": (0.75, 0.95)},
    "Soybean":   {"HI0": (0.18, 0.45), "WP": (10.0, 17.0), "CCx": (0.55, 0.90)},
    "DryBean":   {"HI0": (0.15, 0.40), "WP": (10.0, 15.0), "CCx": (0.55, 0.90)},
    "Cotton":    {"HI0": (0.15, 0.40), "WP": (10.0, 17.0), "CCx": (0.55, 0.90)},
}


# Per-crop High-priority parameter list (from the SSA calibration CSV).
# Returned when [AQUACROP_CALIBRATION] params is unset or set to "auto".
#
# Selection rule: include all "High" priority parameters from the CSV
# that are tunable model parameters (not external inputs like PlantPop,
# which is better fixed from agricultural-census data). Phenology GDDs
# only included for crops where the AquaCrop default uses CalendarType=2
# (GDD mode) — Maize, Sorghum, PearlMillet all do. For CalendarType=1
# (calendar-day) crops the GDD attributes are ignored by the simulator.
_DEFAULT_PARAMS_BY_CROP: dict[str, list[str]] = {
    "Maize":       ["HI0", "WP", "CCx", "CGC", "Zmax",
                    "HIstart", "Senescence", "Maturity"],
    "MaizeGDD":    ["HI0", "WP", "CCx", "CGC", "Zmax"],
    "Sorghum":     ["HI0", "WP", "CCx", "Zmax", "Maturity"],
    "PearlMillet": ["HI0", "WP", "CCx", "Zmax", "Maturity"],
    "Cowpea":      ["HI0", "WP"],
    "Tef":         ["HI0", "WP"],
    # Crops without explicit SSA-CSV guidance fall back to the 3-param
    # starter — the lookup below uses this when crop_name isn't a key.
}


def default_params_for_crop(crop_name: str) -> list[str]:
    """Return the High-priority parameter list for a given AquaCrop crop.

    Used when ``[AQUACROP_CALIBRATION] params = auto`` so each crop in a
    multi-crop run gets a literature-appropriate search space instead of
    one global list. Falls back to the 3-param starter for crops without
    SSA-CSV guidance.
    """
    return list(_DEFAULT_PARAMS_BY_CROP.get(crop_name, ["HI0", "WP", "CCx"]))


class AquaCropParamSpec:
    """Per-crop tunable parameter set.

    One instance per crop being calibrated. Holds the param names + bounds
    + current values; ``apply(crop_obj)`` writes the current values onto
    an instantiated ``aquacrop.Crop`` via setattr.

    Args:
        crop_name: AquaCrop canonical crop name ('Maize', 'Wheat',
            'PaddyRice', ...). Must match what grid_simulator passes to
            ``aquacrop.Crop(crop_name, ...)``.
        params: list of Crop attribute names to tune. Defaults to the
            3-param starter ['HI0', 'WP', 'CCx']. Use
            ``default_params_for_crop(crop_name)`` to get the SSA
            high-priority list.
        bounds_override: dict {param: (low, high)} overriding entries in
            the default bounds table. Use for crop-specific calibration
            (e.g. tighter HI0 range for an irrigation-managed system).
    """

    def __init__(
        self,
        crop_name: str,
        params: Optional[list[str]] = None,
        bounds_override: Optional[dict[str, tuple[float, float]]] = None,
    ):
        self.crop_name = crop_name
        self.params = list(params) if params else ["HI0", "WP", "CCx"]

        base_bounds = _DEFAULT_BOUNDS.get(crop_name, {})
        merged = {**base_bounds, **(bounds_override or {})}
        missing = [p for p in self.params if p not in merged]
        if missing:
            raise ValueError(
                f"AquaCropParamSpec: no default bounds for "
                f"{crop_name}/{missing}. Add to _DEFAULT_BOUNDS or pass "
                f"bounds_override."
            )
        self.bounds = {p: tuple(merged[p]) for p in self.params}
        # Filled lazily from the AquaCrop defaults on first .current access.
        self._current: Optional[dict[str, float]] = None

    def constraints(self) -> list[tuple[float, float]]:
        """List of (low, high) pairs, one per param in self.params order."""
        return [self.bounds[p] for p in self.params]

    def var_names(self) -> list[str]:
        """Flat param names tagged with crop, for human-readable logging."""
        return [f"{p}_{self.crop_name}" for p in self.params]

    @property
    def current(self) -> np.ndarray:
        """Current parameter vector. Reads AquaCrop defaults on first call."""
        if self._current is None:
            self._current = self._read_aquacrop_defaults()
        return np.array([self._current[p] for p in self.params], dtype=float)

    def edit(self, values) -> None:
        """Stage a new parameter vector (does not apply to any Crop yet)."""
        values = np.asarray(values, dtype=float).ravel()
        if len(values) != len(self.params):
            raise ValueError(
                f"AquaCropParamSpec.edit: expected {len(self.params)} values, "
                f"got {len(values)}"
            )
        # Force-init defaults so any param not in self.params keeps its default.
        if self._current is None:
            self._current = self._read_aquacrop_defaults()
        for p, v in zip(self.params, values):
            self._current[p] = float(v)

    def apply(self, crop_obj) -> None:
        """Mutate an instantiated ``aquacrop.Crop`` in place.

        Called inside the worker after ``Crop(...)`` is constructed.
        No-op if .edit() has never been called (preserves AquaCrop defaults).
        """
        if self._current is None:
            return
        for p in self.params:
            setattr(crop_obj, p, self._current[p])

    def overrides_dict(self) -> Optional[dict[str, float]]:
        """Return current overrides as a plain dict (for CellTask field).

        Returns None when .edit() has never been called — preserves defaults.
        """
        if self._current is None:
            return None
        return {p: self._current[p] for p in self.params}

    def _read_aquacrop_defaults(self) -> dict[str, float]:
        """Instantiate a default Crop to read its attribute values."""
        from aquacrop import Crop
        c = Crop(self.crop_name, planting_date="01/01")
        out = {}
        for p in self.params:
            if not hasattr(c, p):
                raise AttributeError(
                    f"AquaCropParamSpec: {self.crop_name!r} has no attribute "
                    f"{p!r}. Either drop it from the params list or upgrade "
                    f"aquacrop-OSPy."
                )
            out[p] = float(getattr(c, p))
        return out

    def __repr__(self) -> str:
        return (
            f"AquaCropParamSpec(crop={self.crop_name!r}, "
            f"params={self.params}, bounds={self.bounds})"
        )
