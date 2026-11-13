"""Define geometric scan workflows."""

from typing import Annotated, Self

import numpy as np
from numpy.typing import NDArray
from pydantic import AfterValidator, ConfigDict, PositiveFloat, field_validator, model_validator

from ..base import Base, round_optional_float
from ..coordinate import AngleCoordinate, Coordinate, DihedralCoordinate, DistanceCoordinate, LinearCombinationCoordinate
from ..engine import Engine
from ..molecule import Molecule
from ..settings import Settings
from ..types import UUID
from .workflow import MoleculeWorkflow


class ScanPoint(Base):
    """A point in a scan.

    Attributes:
        index: index of the point
        index_2d: index of the point in 2nd dimension, if applicable
        molecule: Molecule at the point
        energy: energy of the point
        uuid: UUID of the calculation
    """

    index: int
    index_2d: int = 0
    molecule: Molecule
    energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    uuid: UUID | None = None


class ScanSettings(Base):
    """Settings for a scan.

    `type` and `atoms` remain supported. Their deprecation in favor of `coordinate`
    is tentatively planned for the end of 2026; no removal date is set.
    Consumers should use `resolved_coordinate` to handle either representation.
    Explicit coordinates leave `type` and `atoms` as `None`.

    Attributes:
        coordinate: geometric coordinate, supplied instead of type and atoms
        type: legacy scan type (bond, angle, dihedral)
        atoms: legacy indices of atoms to scan
        start: start of scan
        stop: end of scan
        num: number of points in the scan
        force_constant: umbrella stiffness, in kcal/mol/Å². Unset for constrained scans.
    """

    coordinate: Coordinate | None = None
    type: str | None = None
    atoms: list[int] | None = None
    start: float
    stop: float
    num: int
    force_constant: PositiveFloat | None = None

    def vals(self) -> NDArray[np.float64]:
        """Generate evenly spaced values across the scan range.

        Returns:
            scan values
        """
        return np.linspace(self.start, self.stop, self.num)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_coordinate(self) -> Self:
        """Require either a coordinate or legacy scan type and atom indices."""
        if self.coordinate is not None:
            if self.type is not None or self.atoms is not None:
                raise ValueError("Supply coordinate instead of type and atoms")
        elif self.type is None or self.atoms is None:
            raise ValueError("Scan settings require coordinate or both type and atoms")
        return self

    @property
    def resolved_coordinate(self) -> Coordinate:
        """Return explicit or legacy geometry as a coordinate."""
        if self.coordinate is not None:
            return self.coordinate
        coordinate_class = {"bond": DistanceCoordinate, "angle": AngleCoordinate, "dihedral": DihedralCoordinate}.get(self.type or "")
        if coordinate_class is None:
            raise ValueError(f"Unknown scan type: {self.type!r}")
        return coordinate_class.model_validate({"atoms": self.atoms})


class ScanWorkflow(MoleculeWorkflow):
    """Workflow for scanning a bond, angle, or dihedral.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)

        scan_settings: what coordinate(s) to scan; if more than one, all will be performed simultaneously and should have the same number of steps
        scan_settings_2d: what additional coordinate(s) to scan; makes a grid with `scan_settings`
        wavefront_propagation: use wavefront propagation (10.1063/5.0009232) for more expensive but smoother scans when true
        calc_settings: settings for the calculation
        calc_engine: deprecated engine override; populated from `calc_settings.engine` when omitted
        scan_points: calculation UUIDs for scan points
    """

    scan_settings: ScanSettings | list[ScanSettings]
    scan_settings_2d: ScanSettings | list[ScanSettings] = []
    calc_settings: Settings

    # DEPRECATED - will be removed in future
    calc_engine: Engine = None  # ty: ignore[invalid-assignment]

    wavefront_propagation: bool = True

    # UUIDs of scan points
    scan_points: list[UUID | None] = []

    @field_validator("scan_settings", "scan_settings_2d", mode="after")
    @classmethod
    def validate_scan_settings(cls, val: ScanSettings | list[ScanSettings]) -> list[ScanSettings]:
        """Ensure that scan_settings is a list, and that every list item has the same number of steps.

        Args:
            val: scan settings to validate
        """
        if isinstance(val, ScanSettings):
            val = [val]

        for ss in val:
            if ss.force_constant is not None:
                raise ValueError("Constrained scans do not use umbrella stiffness")
            coordinate = ss.coordinate
            if isinstance(coordinate, LinearCombinationCoordinate) or (coordinate is not None and any(not isinstance(atom, int) for atom in coordinate.atoms)):
                raise ValueError("Molecule scans require a distance, angle, or dihedral with molecule atom indices")
            if ss.num != val[0].num:
                raise ValueError("Concerted scan settings must have same number of steps!")

        return val

    @model_validator(mode="after")
    def set_calc_engine(self) -> Self:
        """Set the calculation engine."""
        self.calc_engine = self.calc_engine or self.calc_settings.engine
        return self
