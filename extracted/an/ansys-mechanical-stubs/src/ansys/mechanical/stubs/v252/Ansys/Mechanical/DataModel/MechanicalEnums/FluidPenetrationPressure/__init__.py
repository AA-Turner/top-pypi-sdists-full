"""FluidPenetrationPressure module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CriterionDefinedByType(Enum):
    """
    Specifies the CriterionDefinedByType.
    """

    Unspecified = 0
    ProgramControlled = 1
    UserSpecifiedCriterion = 2

class FluidPathType(Enum):
    """
    Specifies the FluidPathType.
    """

    Unspecified = 0
    HistoryDependentPath = 2
    HistoryIndependentPath = 1

class GraphDisplay(Enum):
    """
    Specifies the GraphDisplay.
    """

    Unspecified = 0
    FluidPressureCriterionGraph = 2
    FluidPressureGraph = 1

class PenetrationPressureUpdateType(Enum):
    """
    Specifies the PenetrationPressureUpdateType.
    """

    EachIterationUpdate = 2
    EachSubstepUpdate = 1
    Unspecified = 0

class StartPointScopingType(Enum):
    """
    Specifies the StartPointScopingType.
    """

    Unspecified = 0
    StartPointDefineByGeometry = 1
    StartPointDefineByNamedSelection = 2

