"""Provides numba.prange, or range as a fallback.
"""
# adapted from https://github.com/mmore500/hstrat/blob/683bc79118d3aabb07f9db54dc58cf6771fa4bf1/hstrat/_auxiliary_lib/_jit_numpy_int64_t.py

import sys

from ._is_in_coverage_run import is_in_coverage_run

try:
    import numba as nb  # noqa: F401

    jit_prange = nb.prange
except (AttributeError, ImportError, ModuleNotFoundError):  # pragma: no cover
    jit_prange = range
else:
    if is_in_coverage_run() or sys.version_info < (3, 12):  # pragma: no cover
        jit_prange = range
