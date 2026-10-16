"""Imports from scattering matrix plugin."""

from __future__ import annotations

from tidy3d.plugins.smatrix.component_modelers.base import (
    AbstractComponentModeler,
)
from tidy3d.plugins.smatrix.component_modelers.modal import ModalComponentModeler
from tidy3d.plugins.smatrix.component_modelers.terminal import (
    DirectivityMonitorSpec,
    ModelerLowFrequencySmoothingSpec,
    TerminalComponentModeler,
)
from tidy3d.plugins.smatrix.component_modelers.types import ComponentModelerType
from tidy3d.plugins.smatrix.data.data_array import (
    ModalPortDataArray,
    PortDataArray,
    TerminalPortDataArray,
)
from tidy3d.plugins.smatrix.data.modal import ModalComponentModelerData
from tidy3d.plugins.smatrix.data.terminal import (
    MicrowaveSMatrixData,
    TerminalComponentModelerData,
)
from tidy3d.plugins.smatrix.data.types import ComponentModelerDataType
from tidy3d.plugins.smatrix.ports.base_lumped import ImpedanceSpec
from tidy3d.plugins.smatrix.ports.coaxial_lumped import CoaxialLumpedPort
from tidy3d.plugins.smatrix.ports.modal import AstigmaticGaussianPort, GaussianPort, Port
from tidy3d.plugins.smatrix.ports.rectangular_lumped import LumpedPort
from tidy3d.plugins.smatrix.ports.wave import TerminalWavePort, WavePort

# Legacy type to support previous flows
ComponentModeler = ModalComponentModeler

__all__ = [
    "AbstractComponentModeler",
    "AstigmaticGaussianPort",
    "CoaxialLumpedPort",
    "ComponentModeler",
    "ComponentModelerDataType",
    "ComponentModelerType",
    "DirectivityMonitorSpec",
    "GaussianPort",
    "ImpedanceSpec",
    "LumpedPort",
    "MicrowaveSMatrixData",
    "ModalComponentModeler",
    "ModalComponentModelerData",
    "ModalPortDataArray",
    "ModelerLowFrequencySmoothingSpec",
    "Port",
    "PortDataArray",
    "TerminalComponentModeler",
    "TerminalComponentModelerData",
    "TerminalPortDataArray",
    "TerminalWavePort",
    "WavePort",
]
