#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "jax",
#     "numpy",
#     "perfplot",
#     "numba",
#     "pint"
# ]
# ///
# mypy: ignore-errors
from pathlib import Path

import jax
import numpy as np
import perfplot
from airspeed import eas, eas_pure_py, ureg
from numba import njit


def setup(n):
    tas_np = np.random.rand(n) * 250 + 50
    density_np = np.random.rand(n) * 0.825 + 0.4
    return tas_np, density_np


def run_pint_quantity_in(tas_np, density_np):
    tas_pint = tas_np * (ureg.meter / ureg.second)
    density_pint = density_np * (ureg.kilogram / ureg.meter**3)
    result_pint = eas(tas_pint, density_pint)
    return result_pint.magnitude


def run_pint_numpy_in(tas_np, density_np):
    result_pint = eas(tas_np, density_np)
    return result_pint.magnitude  # NOTE: wrong units


def run_numpy(tas_np, density_np):
    return eas_pure_py(tas_np, density_np)


eas_jax_jit_cpu = jax.jit(eas_pure_py, backend="cpu")
eas_numba_jit = njit(eas_pure_py, parallel=True, nogil=True, cache=True)


def run_jax_cpu(tas_np, density_np):
    return eas_jax_jit_cpu(tas_np, density_np)


def run_numba(tas_np, density_np):
    return eas_numba_jit(tas_np, density_np)


def main(path_root: Path = Path(__file__).parent):
    n_range = [2**k for k in range(2, 27)]
    for n in n_range:  # precompile
        run_jax_cpu(*setup(n))
        run_numba(*setup(n))
    out = perfplot.bench(
        setup=setup,
        kernels=[
            run_pint_quantity_in,
            run_pint_numpy_in,
            run_numpy,
            run_jax_cpu,
            run_numba,
        ],
        n_range=n_range,
        labels=[
            "pint (Quantity inputs)",
            "pint",
            "baseline (np.ndarray inputs)",
            "baseline + jax.jit",
            "baseline + numba.njit",
        ],
        xlabel="np.ndarray size",
        equality_check=np.allclose,
    )
    out.save(path_root / "bench.png", transparent=True, bbox_inches="tight")
    out.show()


if __name__ == "__main__":
    main()
