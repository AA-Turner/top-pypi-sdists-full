"""
geocif/aquacrop — AquaCrop-OSPy gridded yield estimation.

Runs AquaCrop-OSPy on a 5 km grid over user-configured countries and writes
output in the standard geocif SQLite schema so geocif diagnostics
(scatter_obs_pred, MAPE bars, residuals_vs_cid, FDW export, etc.) can
consume it directly alongside catboost / tabpfn / null model outputs.

Entry point::

    from geocif.aquacrop import aquacrop_runner
    aquacrop_runner.run([
        "config/geobase.txt",
        "config/countries.txt",
        "config/crops.txt",
        "config/aquacrop.txt",
    ])

Pipeline (per country × crop × season × year in LOOCV):

    1.  Build 5 km grid clipped to country boundary (read_masked).
    2.  Per cell: read soil + AgERA5 daily Tmax/Tmin/Rs + CHIRPS daily P,
        crop fraction; lookup planting/harvest from calendar Excel.
    3.  Run AquaCrop-OSPy simulation (rainfed, FC init, Penman-Monteith
        ETo from Rs).
    4.  Yield raster at {dir_output}/{project}/aquacrop/raster/.
    5.  Aggregate raster → admin polygons via geom_extract (crop fraction
        as AFI).
    6.  LOOCV cross-country region_anomaly bias correction against HarvestStat.
    7.  Write DB rows in yield_outlook schema (Model='aquacrop').
    8.  Diagnostics (rRMSEp, sMAPE, R², per-region scatter).
"""

__version__ = "0.1.0"

# `aquacrop_runner` is imported lazily (PEP 562). It pulls in `aquacrop-ospy`,
# an optional extra, so importing it eagerly here made every leaf module in this
# package unreachable without that dependency -- including `calendar`, which is
# pure pandas/datetime and is the single home of the half-month block logic that
# geocif.phenology and geocif.cropcal both reuse. `geocif.aquacrop.calendar` and
# `from geocif.aquacrop import aquacrop_runner` both still work; only the cost
# moved to first use.
__all__ = ["aquacrop_runner", "calendar"]


def __getattr__(name):
    if name in __all__:
        import importlib

        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(__all__))
