"""Top-level package for geocif."""

# tqdm.rich is alpha and prints a TqdmExperimentalWarning on first instantiation.
# 17 submodules use it directly via `from tqdm.rich import tqdm` (analysis,
# geocif, geocif_runner, indices_runner, utils, ml/*, cid/*, agmet/*, risk/*,
# progress); silencing it once here at package import covers all of them
# without per-file filters.
import warnings as _warnings
try:
    from tqdm import TqdmExperimentalWarning as _TqdmExperimentalWarning
    _warnings.filterwarnings("ignore", category=_TqdmExperimentalWarning)
except ImportError:
    pass

# pandas PerformanceWarning: emitted by the per-CID z-score column add at
# geocif.py:_compute_region_zscore_features (repeated `df[zname] = ...`
# on a wide df fragments the internal block manager). Functionally
# harmless and floods the log when region_zscore_cids has 10+ entries
# × forecasted stages. Filter rather than refactor — the assignments
# happen inside an inner loop and a pd.concat rewrite would be a
# bigger change than this warning is worth.
try:
    from pandas.errors import PerformanceWarning as _PandasPerformanceWarning
    _warnings.filterwarnings("ignore", category=_PandasPerformanceWarning)
except ImportError:
    pass

__author__ = """Ritvik Sahajpal"""
__email__ = "ritvik@umd.edu"
__version__ = "0.4.896"

__all__ = ["ml", "cid", "viz", "agmet", "fdw_export", "dashboard"]
