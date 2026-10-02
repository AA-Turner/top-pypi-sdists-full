#!/usr/bin/python3
"""Land or ocean: the mask, shared.

Several modules split their statistics by surface -- zone, histogram,
timeserie -- and the regions drawn on a map want a coastline. All of them
read the same grid, so it lives here rather than in whichever module
happened to need it first.

The grid comes from ``global_land_mask``; the package ships it as a
compressed archive, so the first run writes it once as plain ``.npy``
under PATHWORK and every worker afterwards memory-maps that file. Without
the cache each worker would decompress a 0.9 GB array of its own.

    from pikobs.configobs.landmask import is_land_function, surface_sql

    conn.create_function("is_land_sql", 2, is_land_function(pathwork))
    where = "1=1" + surface_sql('ocean')
"""

import os
from typing import Optional

import numpy as np

__all__ = ["LAND_MASK_CACHE_SUBDIR", "land_mask_cache_dir", "has_land_mask", "mmap_land_mask",
           "is_land_function", "surface_sql", "register"]

LAND_MASK_CACHE_SUBDIR = "landmask_cache"

# whether the package is there, found without importing it: on import it
# loads its whole grid into memory (0.93 GB), and every Dask worker imports
# pikobs -- 80 workers, 74 GB before any work. The grid itself is read
# from the shared cache below, mapped, never loaded.
import importlib.util as _ilu
_HAS_LAND_MASK = _ilu.find_spec("global_land_mask") is not None


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


LAND_MASK_FILES = ("mask", "lat", "lon")


def land_mask_cache_dir(pathwork: str) -> str:
    """Where the decompressed grid lives -- once, not in every PATHWORK.

    The grid is 933 million cells, one byte each: 891 MB. It used to be
    written into every output folder that split land and ocean, and built
    again whenever a module wiped its folder. The first of these that
    works is used:

      1. $PIKOBS_LANDMASK_CACHE, when set (a folder shared between users);
      2. <python environment>/share/pikobs/landmask, the user's own
         environment: no home quota spent, every run shares it;
      3. <pathwork>/landmask_cache, as before.

    A complete cache is used even where it cannot be written.
    """
    import sys as _sys
    candidates = []
    env = os.environ.get("PIKOBS_LANDMASK_CACHE")
    if env:
        candidates.append(env)
    candidates.append(os.path.join(_sys.prefix, "share", "pikobs", "landmask"))
    candidates.append(os.path.join(pathwork, LAND_MASK_CACHE_SUBDIR))

    def complete(d):
        return all(os.path.isfile(os.path.join(d, f"{n}.npy")) for n in LAND_MASK_FILES)

    for d in candidates:
        if complete(d):
            return d
    for d in candidates:
        try:
            os.makedirs(d, exist_ok=True)
        except OSError:
            continue
        if os.access(d, os.W_OK):
            return d
    return candidates[-1]


def mmap_land_mask(pathwork: str):
    """The land mask grid, cached once as plain .npy and memory-mapped.

    Every worker on the same filesystem reads the same file, so the mask
    is not rebuilt per task.
    """
    cache = land_mask_cache_dir(pathwork)
    paths = {n: os.path.join(cache, f"{n}.npy")
             for n in ("mask", "lat", "lon")}
    if not all(os.path.isfile(p) for p in paths.values()):
        os.makedirs(cache, exist_ok=True)
        # its folder, found without importing it (the import loads the grid)
        _spec = _ilu.find_spec("global_land_mask")
        npz = os.path.join(os.path.dirname(_spec.origin),
                           "globe_combined_mask_compressed.npz")
        data = np.load(npz)
        for name, dest in paths.items():
            tmp = f"{dest}.tmp{os.getpid()}.npy"
            np.save(tmp, data[name])
            os.replace(tmp, dest)
    return (np.load(paths["mask"], mmap_mode="r"), np.load(paths["lat"]),
            np.load(paths["lon"]))


def is_land_function(pathwork: str):
    """A scalar (lat, lon) -> 0/1 for SQLite.

    Nearest neighbour on the regular grid, the same as
    ``global_land_mask.is_land``; note that its array stores is_OCEAN,
    hence the inversion.
    """
    mask, lat_grid, lon_grid = mmap_land_mask(pathwork)
    lat0, lat_step = float(lat_grid[0]), float(lat_grid[1] - lat_grid[0])
    lon0, lon_step = float(lon_grid[0]), float(lon_grid[1] - lon_grid[0])
    lat_lo, lat_hi = float(lat_grid.min()), float(lat_grid.max())
    lon_lo, lon_hi = float(lon_grid.min()), float(lon_grid.max())

    def _is_land(lat, lon):
        if lat is None or lon is None:
            return 0
        la = min(max(lat, lat_lo), lat_hi)
        lo = min(max(lon, lon_lo), lon_hi)
        return 0 if mask[int((la - lat0) / lat_step),
                         int((lo - lon0) / lon_step)] else 1

    return _is_land


# ─────────────────────────────────────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────────────────────────────────────

# GPS-RO: every departure is divided by a reference refractivity profile
# before it is summed, B_ref = 300 exp(-h / 6500), so a level near the
# ground, where refractivity is hundreds of times larger, does not flatten
# the stratosphere; and a profile passes the quality gates of the
# operational verification before it counts.
RO_FAMILIES = ('ro', 'ro_qc', 'gpsocc')


def has_land_mask() -> bool:
    """Is the package that holds the grid installed?"""
    # found, not imported: importing it loads its 0.93 GB grid
    return _ilu.find_spec("global_land_mask") is not None


def surface_sql(land_ocean: str, lat: str = 'lat', lon: str = 'lon') -> str:
    """The condition of a surface: land, ocean, or everything.

    The function it calls has to be registered on the connection first,
    with :func:`register`.
    """
    if str(land_ocean).lower() == 'land':
        return f" AND is_land_sql({lat}, {lon}) = 1"
    if str(land_ocean).lower() == 'ocean':
        return f" AND is_land_sql({lat}, {lon}) = 0"
    return ""


def register(conn, land_oceans, pathwork: str) -> None:
    """Give a connection the mask, but only when a surface asks for it.

    Reading the grid costs a second and some memory, so a run that only
    wants 'all' never touches it.
    """
    if any(str(lo).lower() != 'all' for lo in land_oceans):
        conn.create_function("is_land_sql", 2, is_land_function(pathwork))


def register_surface(conn, land_oceans, pathwork) -> None:
    """is_land_sql() in a SQLite connection, only when a surface asks for
    it: with all alone the mask is never read."""
    if any(lo not in (None, '', 'all') for lo in land_oceans or ()):
        conn.create_function("is_land_sql", 2, is_land_function(pathwork))


def is_land_array(lat, lon, pathwork: str) -> np.ndarray:
    """is_land_sql for whole arrays: 1 on land, 0 at sea (int8).

    The same grid, the same nearest cell and the same clipping as
    :func:`is_land_function`, done once for a whole column instead of once
    per row -- for a module that holds its rows in memory (mapobs). A
    missing position counts as sea, as there.
    """
    mask, lat_grid, lon_grid = mmap_land_mask(pathwork)
    lat0, lat_step = float(lat_grid[0]), float(lat_grid[1] - lat_grid[0])
    lon0, lon_step = float(lon_grid[0]), float(lon_grid[1] - lon_grid[0])
    la = np.asarray(lat, dtype=float)
    lo = np.asarray(lon, dtype=float)
    ok = np.isfinite(la) & np.isfinite(lo)
    la = np.clip(np.where(ok, la, lat0), float(lat_grid.min()), float(lat_grid.max()))
    lo = np.clip(np.where(ok, lo, lon0), float(lon_grid.min()), float(lon_grid.max()))
    # int() of the scalar version truncates toward zero, and so does astype
    i = ((la - lat0) / lat_step).astype(np.int64)
    j = ((lo - lon0) / lon_step).astype(np.int64)
    out = np.where(np.asarray(mask[i, j]), 0, 1).astype(np.int8)
    out[~ok] = 0
    return out
