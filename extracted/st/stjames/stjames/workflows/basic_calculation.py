"""Basic calculation workflow."""

from typing import Self

from pydantic import model_validator

from ..base import UniqueList
from ..engine import Engine
from ..engine_compatibility import ENGINE_DISABLED_TASKS
from ..settings import Settings
from ..task import Task
from ..types import UUID
from .workflow import MoleculeWorkflow


class BasicCalculationWorkflow(MoleculeWorkflow):
    """
    Workflow for a basic calculation.

    Inherited:
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow

    New:
    :param settings: Settings for running the calculation
    :param tasks: tasks to perform; defaults to ENERGY, CHARGE, and DIPOLE
    :param engine: deprecated engine override; specify settings.engine instead
    :param calculation_uuid: UUID of the calculation; None before a UUID is assigned
    """

    settings: Settings
    tasks: UniqueList[Task] = [Task.ENERGY, Task.CHARGE, Task.DIPOLE]
    calculation_uuid: UUID | None = None

    # DEPRECATED - specify in settings now
    engine: Engine = None  # ty: ignore[invalid-assignment]

    @model_validator(mode="after")
    def set_engine_and_validate(self) -> Self:
        """Set the calculation engine and validate task compatibility."""
        self.engine = self.engine or self.settings.engine

        if Task.ELASTIC_TENSOR in self.settings.tasks:
            if self.initial_molecule.cell is None:
                raise ValueError("Task.ELASTIC_TENSOR requires a periodic cell")
            if Task.ELASTIC_TENSOR in ENGINE_DISABLED_TASKS.get(self.engine, set()):
                raise ValueError(f"{self.engine} does not support Task.ELASTIC_TENSOR")

        if Task.BAND_STRUCTURE in self.settings.tasks and self.initial_molecule.cell is None:
            raise ValueError("Task.BAND_STRUCTURE requires a periodic cell")

        return self
