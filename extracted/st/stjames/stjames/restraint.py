"""Harmonic and flat-bottom restraints on atoms and residues."""

from typing import Annotated, Self

from pydantic import Field, FiniteFloat, model_validator

from .base import Base, LowercaseStrEnum
from .pdb import ResidueAtomRef, ResidueRef


class RestraintType(LowercaseStrEnum):
    """Geometric quantities restrained during molecular dynamics."""

    POSITION = "position"
    DISTANCE = "distance"
    ANGLE = "angle"
    DIHEDRAL = "dihedral"


class MDRestraints(Base):
    """Harmonic restraint with a flat-bottom tolerance around the target.

    Atom selections use atom positions. Residue selections use centers of mass
    computed from elemental masses, including any added hydrogens.
    Position restraints keep the selected atom or residue center near its location
    before minimization.
    Each selected residue must be part of a single molecule connected by bonds.
    That molecule must not start split across opposite sides of the simulation box.

    Attributes:
        restraint_type: restrained geometric quantity
        selections: one, two, three, or four atom or residue references
        force_constant: spring constant, in kcal/mol/Å² for position and distance, kcal/mol/rad² for angle and dihedral restraints
        target: desired distance or angle, omitted for position restraints, in Å or degrees
        flat_bottom_range: tolerance around the target, zero for harmonic, in Å or degrees
    """

    restraint_type: RestraintType
    selections: list[ResidueRef | ResidueAtomRef]
    force_constant: Annotated[FiniteFloat, Field(gt=0)]
    target: FiniteFloat | None = None
    flat_bottom_range: Annotated[FiniteFloat, Field(ge=0)] = 0

    @model_validator(mode="after")
    def validate_geometry(self) -> Self:
        """Validate selection counts, references, and targets."""
        count = {
            RestraintType.POSITION: 1,
            RestraintType.DISTANCE: 2,
            RestraintType.ANGLE: 3,
            RestraintType.DIHEDRAL: 4,
        }[self.restraint_type]
        if len(self.selections) != count:
            raise ValueError(f"{self.restraint_type} restraint requires {count} selections")
        for reference in self.selections:
            residue = reference.residue if isinstance(reference, ResidueAtomRef) else reference
            if not residue.key or (residue.entity_type == "polymer" and not residue.residue_key):
                raise ValueError("Restraint residue reference must identify a residue")
            if isinstance(reference, ResidueAtomRef) and not reference.atom_name.strip():
                raise ValueError("Restraint atom name must not be empty")
        if self.restraint_type == RestraintType.POSITION:
            if self.target is not None:
                raise ValueError("Position restraints do not accept a target")
        elif self.target is None:
            raise ValueError("Distance, angle, and dihedral restraints require a target")
        elif self.restraint_type == RestraintType.DIHEDRAL:
            if not -180 <= self.target <= 180:
                raise ValueError("Dihedral target must be between -180 and 180 degrees")
        elif self.target < 0:
            raise ValueError("Restraint target must be nonnegative")
        elif self.restraint_type == RestraintType.ANGLE and self.target > 180:
            raise ValueError("Angle target must be between 0 and 180 degrees")
        return self
