from __future__ import annotations

__all__ = [
    "BASE_MODEL_TYPE",
    "RATE_MODEL_TYPE",
    "Simulator",
    "_AbstractRateModel",
    "_AbstractStoichiometricModel",
    "_BaseRateSimulator",
    "_BaseSimulator",
    "_LabelSimulate",
    "_LinearLabelSimulate",
    "_Simulate",
]

import warnings
from typing import TYPE_CHECKING, Dict, List, Type, Union, overload

from modelbase.ode.integrators import AbstractIntegrator, Scipy
from modelbase.ode.models import (
    BASE_MODEL_TYPE,
    RATE_MODEL_TYPE,
    _AbstractRateModel,
    _AbstractStoichiometricModel,
)
from modelbase.ode.models import LabelModel as _LabelModel
from modelbase.ode.models import LinearLabelModel as _LinearLabelModel
from modelbase.ode.models import Model as _Model

from .abstract_simulator import _BaseRateSimulator, _BaseSimulator
from .labelsimulator import _LabelSimulate
from .linearlabelsimulator import _LinearLabelSimulate
from .simulator import _Simulate

if TYPE_CHECKING:
    from modelbase.typing import Array, ArrayLike

try:
    from modelbase.ode.integrators import Assimulo

    default_integrator: type[AbstractIntegrator] = Assimulo
except ImportError:  # pragma: no cover
    warnings.warn("Assimulo not found, disabling sundials support.")
    default_integrator = Scipy


@overload
def Simulator(model: _Model) -> _Simulate:
    ...


@overload
def Simulator(model: _LabelModel) -> _LabelSimulate:
    ...


@overload
def Simulator(model: _LinearLabelModel) -> _LinearLabelSimulate:
    ...


def Simulator(
    model: _LabelModel | _LinearLabelModel | _Model,
    integrator: type[AbstractIntegrator] = default_integrator,
    y0: ArrayLike | None = None,
    time: list[Array] | None = None,
    results: list[Array] | None = None,
    parameters: list[dict[str, float]] | None = None,
) -> _LabelSimulate | _LinearLabelSimulate | _Simulate:
    """Choose the simulator class according to the model type.

    If a simulator different than assimulo is required, it can be chosen
    by the integrator argument.

    Parameters
    ----------
    model : modelbase.model
        The model instance

    Returns
    -------
    Simulate : object
        A simulate object according to the model type

    """
    if isinstance(model, _LabelModel):
        return _LabelSimulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
            parameters=parameters,
        )
    if isinstance(model, _LinearLabelModel):
        return _LinearLabelSimulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
        )
    if isinstance(model, _Model):
        return _Simulate(
            model=model,
            integrator=integrator,
            y0=y0,
            time=time,
            results=results,
            parameters=parameters,
        )
    raise NotImplementedError
