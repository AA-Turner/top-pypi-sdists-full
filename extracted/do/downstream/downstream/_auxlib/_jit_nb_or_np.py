"""Provides numba, or numpy as a fallback.

Type must be declared outside jit'ed function or numba fails.
"""
# adapted from https://github.com/mmore500/hstrat/blob/683bc79118d3aabb07f9db54dc58cf6771fa4bf1/hstrat/_auxiliary_lib/_jit_numpy_int64_t.py

import sys

from ._is_in_coverage_run import is_in_coverage_run

try:
    import numba as nb_or_np  # noqa: F401

    nb_or_np.jit
except (AttributeError, ImportError, ModuleNotFoundError):  # pragma: no cover
    import numpy as nb_or_np  # noqa: F401
else:
    if is_in_coverage_run() or sys.version_info < (3, 12):  # pragma: no cover
        import numpy as nb_or_np  # noqa: F401
