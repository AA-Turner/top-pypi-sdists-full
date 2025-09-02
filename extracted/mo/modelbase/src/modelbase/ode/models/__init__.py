from __future__ import annotations

__all__ = [
    "DerivedStoichiometry",
    "LabelModel",
    "LinearLabelModel",
    "Model",
    "_AbstractRateModel",
    "_AbstractStoichiometricModel",
]

from typing import TypeVar

from .abstract_model import _AbstractRateModel, _AbstractStoichiometricModel
from .labelmodel import LabelModel
from .linearlabelmodel import LinearLabelModel
from .model import DerivedStoichiometry, Model

BASE_MODEL_TYPE = TypeVar("BASE_MODEL_TYPE", bound=_AbstractStoichiometricModel)
RATE_MODEL_TYPE = TypeVar("RATE_MODEL_TYPE", bound=_AbstractRateModel)
