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
``country_block``
    ``spatial_block`` with one repair: a country that fits inside two tiles is
    held out whole. A 10-degree tile splits a large country, so an identical
    national calendar row lands on both sides of the fold and GroupKFold then
    measures memorisation of that row -- the failure the scheme exists to
    prevent. :func:`duplicate_leakage` reports how often that happens for
    every scheme.

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
SCHEME_NAMES = ("random", "country", "spatial_block", "country_block")

#: For ``country_block``: a country spanning at most this many tiles is held
#: out whole; a larger one is split by tile like ``spatial_block``.
COUNTRY_BLOCK_MAX_TILES = 2

#: Columns that identify a calendar row verbatim. A national calendar copied
#: across every zone of a country makes rows with identical values here; when
#: such a twin sits in the training fold, the test row is memorised, not
#: predicted.
DUPLICATE_KEY_COLUMNS = (
    "country", "crop", "season",
    "target_planting", "target_midgreenup", "target_midgreendown", "target_harvest",
)


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


def country_blocks(
    country: Sequence[str],
    lat: Sequence[float],
    lon: Sequence[float],
    block_degrees: float = DEFAULT_BLOCK_DEGREES,
    max_tiles: int = COUNTRY_BLOCK_MAX_TILES,
) -> np.ndarray:
    """Group label per row: the country when it spans few tiles, else the tile."""
    tiles = spatial_blocks(lat, lon, block_degrees)
    countries = np.asarray(list(country), dtype=object)
    span = pd.Series(tiles).groupby(countries).nunique()
    return np.array(
        [
            f"country:{c}" if span.get(c, 0) <= max_tiles else f"tile:{t}"
            for c, t in zip(countries, tiles)
        ]
    )


def duplicate_leakage(
    frame: pd.DataFrame,
    scheme: CVScheme,
    columns: Sequence[str] = DUPLICATE_KEY_COLUMNS,
) -> float:
    """Share of test rows whose calendar-row tuple also appears in training.

    Rows are compared on ``columns`` (country, crop, season and the four
    calendar days). A test row with a verbatim twin in the training fold is
    predicted from a copy of itself; this is the fraction of test rows for
    which that is true, pooled over folds. Zero for ``country`` by
    construction (the country is part of the key). NaN when the columns are
    not all present.
    """
    present = [c for c in columns if c in frame.columns]
    if len(present) != len(columns) or not scheme.splits:
        return float("nan")
    keys = frame[present].astype(str).agg("|".join, axis=1).to_numpy()
    leaked = total = 0
    for train_idx, test_idx in scheme.splits:
        train_keys = set(keys[train_idx])
        leaked += int(sum(k in train_keys for k in keys[test_idx]))
        total += len(test_idx)
    return float(100.0 * leaked / total) if total else float("nan")


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

            elif name == "country_block":
                groups = country_blocks(
                    frame[country_col], frame[lat_col], frame[lon_col], block_degrees
                )
                splits = _grouped_splits(groups, n_splits)
                out[name] = CVScheme(
                    name,
                    f"Grouped K-fold over {block_degrees:g} degree tiles, small countries held out whole",
                    splits,
                    leaky=False,
                    n_groups=len(np.unique(groups)),
                )

            else:
                raise ValueError(f"unknown CV scheme {name!r}")

        except Exception as exc:  # noqa: BLE001 - a scheme that cannot run is not fatal
            logger.warning(f"CV scheme {name!r} unavailable: {exc}")

    return out


def describe(
    schemes: dict[str, CVScheme], frame: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """A small table of the schemes actually built, for the run report.

    With ``frame``, adds ``pct_test_rows_with_train_duplicate`` per scheme
    (see :func:`duplicate_leakage`), so the memorisation each scheme permits
    is a number in the output rather than a caveat in a docstring.
    """
    rows = []
    for s in schemes.values():
        row = {
            "scheme": s.name,
            "folds": s.n_splits,
            "groups": s.n_groups if s.n_groups is not None else "",
            "leaky": s.leaky,
            "description": s.description,
        }
        if frame is not None:
            row["pct_test_rows_with_train_duplicate"] = duplicate_leakage(frame, s)
        rows.append(row)
    return pd.DataFrame(rows)
