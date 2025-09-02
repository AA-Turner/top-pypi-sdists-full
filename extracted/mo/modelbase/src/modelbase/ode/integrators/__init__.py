from __future__ import annotations

__all__ = [
    "AbstractIntegrator",
    "Assimulo",
    "Scipy",
]

import contextlib

from .abstract_integrator import AbstractIntegrator

with contextlib.suppress(ImportError):
    from .int_assimulo import _IntegratorAssimulo as Assimulo
from .int_scipy import _IntegratorScipy as Scipy
