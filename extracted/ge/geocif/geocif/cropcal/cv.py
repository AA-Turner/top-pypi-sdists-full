# -*- coding: utf-8 -*-
"""Cross-validation splitters, spatial and not.

Calendar regions are not independent samples. Neighbouring regions share a
crop mask, a climate and often a single national calendar row copied across
every zone in the country, so a model can score well by memorising a
neighbourhood rather than learning phenology. A plain shuffled K-fold measures
that memorisation and reports it as skill.

Three schemes are produced side by side so the gap between them is visible
rather than assumed:

``random``
    Shuffled K-fold over rows. Leaky by construction; the optimistic reference,
    and the answer to "what does it look like *without* spatial CV".
``country``
    Leave-one-country-out. Tests transfer to a country never seen in training.
``spatial_block``
    Grouped K-fold over coarse latitude/longitude tiles of the region centroid.
    Breaks the autocorrelation that leave-one-country-out still leaves across a
    shared border.

geocif has no spatial CV anywhere else, so this is new rather than a wrapper.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, KFold, LeaveOneGroupOut

logger = logging.getLogger(__name__)

DEFAULT_N_SPLITS = 5

#: Tile size, in degrees, for the spatial-block grouping.
DEFAULT_BLOCK_DEGREES = 10.0

#: Every scheme this module can build, in reporting order.
SCHEME_NAMES = ("random", "country", "spatial_block")


@dataclass(frozen=True)
class CVScheme:
    """A named set of train/test index pairs."""

    name: str
    description: str
    splits: list[tuple[np.ndarray, np.ndarray]]
    leaky: bool
    n_groups: Optional[int] = None

    @property
    def n_splits(self) -> int:
        return len(self.splits)


def spatial_blocks(
    lat: Sequence[float], lon: Sequence[float], block_degrees: float = DEFAULT_BLOCK_DEGREES
) -> np.ndarray:
    """Group label per row from a coarse lat/lon tiling of the centroid.

    Rows with a missing centroid fall into their own group so they are never
    silently pooled with the tile at (0, 0).
    """
    lat_arr = np.asarray(lat, dtype=float)
    lon_arr = np.asarray(lon, dtype=float)
    rows = np.floor(lat_arr / block_degrees)
    cols = np.floor(lon_arr / block_degrees)
    labels = np.array(
        [
            f"na_{i}" if not (np.isfinite(r) and np.isfinite(c)) else f"{int(r)}_{int(c)}"
            for i, (r, c) in enumerate(zip(rows, cols))
        ]
    )
    return labels


def _grouped_splits(groups: np.ndarray, n_splits: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """GroupKFold, clamped to the number of distinct groups available."""
    n_groups = len(np.unique(groups))
    folds = int(min(n_splits, n_groups))
    if folds < 2:
        raise ValueError(f"need at least 2 groups for a grouped split, have {n_groups}")
    splitter = GroupKFold(n_splits=folds)
    dummy = np.zeros(len(groups))
    return [(tr, te) for tr, te in splitter.split(dummy, groups=groups)]


def build_schemes(
    frame: pd.DataFrame,
    *,
    country_col: str = "country",
    lat_col: str = "lat",
    lon_col: str = "lon",
    n_splits: int = DEFAULT_N_SPLITS,
    block_degrees: float = DEFAULT_BLOCK_DEGREES,
    seed: int = 0,
    names: Iterable[str] = SCHEME_NAMES,
) -> dict[str, CVScheme]:
    """Build the requested schemes for one design matrix.

    A scheme that cannot be built -- too few countries for leave-one-out, say --
    is logged and omitted rather than raising, so a small per-crop frame still
    gets whatever schemes it can support.
    """
    out: dict[str, CVScheme] = {}
    n_rows = len(frame)

    for name in names:
        try:
            if name == "random":
                splitter = KFold(n_splits=min(n_splits, n_rows), shuffle=True, random_state=seed)
                splits = [(tr, te) for tr, te in splitter.split(np.zeros(n_rows))]
                out[name] = CVScheme(
                    name,
                    "Shuffled K-fold over rows (LEAKY: neighbouring regions share a climatology)",
                    splits,
                    leaky=True,
                )

            elif name == "country":
                groups = frame[country_col].to_numpy()
                n_groups = len(np.unique(groups))
                if n_groups < 2:
                    raise ValueError(f"only {n_groups} country in the frame")
                splitter = LeaveOneGroupOut()
                splits = [
                    (tr, te) for tr, te in splitter.split(np.zeros(n_rows), groups=groups)
                ]
                out[name] = CVScheme(
                    name,
                    "Leave-one-country-out",
                    splits,
                    leaky=False,
                    n_groups=n_groups,
                )

            elif name == "spatial_block":
                groups = spatial_blocks(frame[lat_col], frame[lon_col], block_degrees)
                splits = _grouped_splits(groups, n_splits)
                out[name] = CVScheme(
                    name,
                    f"Grouped K-fold over {block_degrees:g} degree centroid tiles",
                    splits,
                    leaky=False,
                    n_groups=len(np.unique(groups)),
                )

            else:
                raise ValueError(f"unknown CV scheme {name!r}")

        except Exception as exc:  # noqa: BLE001 - a scheme that cannot run is not fatal
            logger.warning(f"CV scheme {name!r} unavailable: {exc}")

    return out


def describe(schemes: dict[str, CVScheme]) -> pd.DataFrame:
    """A small table of the schemes actually built, for the run report."""
    return pd.DataFrame(
        [
            {
                "scheme": s.name,
                "folds": s.n_splits,
                "groups": s.n_groups if s.n_groups is not None else "",
                "leaky": s.leaky,
                "description": s.description,
            }
            for s in schemes.values()
        ]
    )
