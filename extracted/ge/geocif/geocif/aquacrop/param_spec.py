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
"""

from __future__ import annotations

from typing import Optional

import numpy as np


# Default bounds derived from FAO-56 + the AquaCrop reference manual.
# Conservative widths so PSO stays inside agronomically defensible ranges.
# Override via aquacrop.txt [<crop>_AQUACROP_BOUNDS] section if needed.
_DEFAULT_BOUNDS: dict[str, dict[str, tuple[float, float]]] = {
    "Maize":     {"HI0": (0.30, 0.55), "WP": (15.0, 22.0), "CCx": (0.85, 0.98)},
    "MaizeGDD":  {"HI0": (0.30, 0.55), "WP": (15.0, 22.0), "CCx": (0.85, 0.98)},
    "Wheat":     {"HI0": (0.30, 0.50), "WP": (13.0, 18.0), "CCx": (0.85, 0.98)},
    "WheatGDD":  {"HI0": (0.30, 0.50), "WP": (13.0, 18.0), "CCx": (0.85, 0.98)},
    "Rice":      {"HI0": (0.35, 0.50), "WP": (15.0, 20.0), "CCx": (0.90, 0.99)},
    "PaddyRice": {"HI0": (0.35, 0.50), "WP": (15.0, 20.0), "CCx": (0.90, 0.99)},
    "Soybean":   {"HI0": (0.30, 0.45), "WP": (14.0, 18.0), "CCx": (0.85, 0.97)},
    "Sorghum":   {"HI0": (0.25, 0.45), "WP": (28.0, 35.0), "CCx": (0.85, 0.97)},
    "Tef":       {"HI0": (0.25, 0.40), "WP": (10.0, 15.0), "CCx": (0.85, 0.95)},
    "DryBean":   {"HI0": (0.25, 0.40), "WP": (13.0, 17.0), "CCx": (0.85, 0.97)},
    "Cotton":    {"HI0": (0.30, 0.45), "WP": (14.0, 18.0), "CCx": (0.85, 0.97)},
}


class AquaCropParamSpec:
    """Per-crop tunable parameter set.

    One instance per crop being calibrated. Holds the param names + bounds
    + current values; ``apply(crop_obj)`` writes the current values onto
    an instantiated ``aquacrop.Crop`` via setattr.

    Args:
        crop_name: AquaCrop canonical crop name ('Maize', 'Wheat',
            'PaddyRice', ...). Must match what grid_simulator passes to
            ``aquacrop.Crop(crop_name, ...)``.
        params: list of Crop attribute names to tune. Defaults to
            ['HI0', 'WP', 'CCx'] — the 3-param starter from the plan.
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
        return {p: float(getattr(c, p)) for p in self.params}

    def __repr__(self) -> str:
        return (
            f"AquaCropParamSpec(crop={self.crop_name!r}, "
            f"params={self.params}, bounds={self.bounds})"
        )
