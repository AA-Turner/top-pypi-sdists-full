"""Define geometric coordinates independently of scans and restraints."""

from typing import Annotated, Literal, Self, TypeAlias

from pydantic import AfterValidator, BaseModel, Field, FiniteFloat, PositiveInt, model_validator

from .pdb import ResidueAtomRef

_Atoms: TypeAlias = tuple[int, ...] | tuple[ResidueAtomRef, ...]


def _validate_atoms(atoms: _Atoms) -> _Atoms:
    if len(set(atoms)) != len(atoms):
        raise ValueError("Coordinate atoms must be distinct")
    first, last = atoms[0], atoms[-1]
    reverse = last < first if isinstance(first, int) and isinstance(last, int) else repr(last) < repr(first)
    return atoms[::-1] if reverse else atoms


class DistanceCoordinate(BaseModel):
    """Distance between two atoms, in Å.

    Attributes:
        type: coordinate discriminator
        atoms: positive molecule atom indices (1-based) or PDB atom references, ordered by endpoint
    """

    type: Literal["distance"] = "distance"
    atoms: Annotated[tuple[PositiveInt, PositiveInt] | tuple[ResidueAtomRef, ResidueAtomRef], AfterValidator(_validate_atoms)]


class AngleCoordinate(BaseModel):
    """Angle between three atoms, in degrees, with the vertex second.

    Attributes:
        type: coordinate discriminator
        atoms: positive molecule atom indices (1-based) or PDB atom references, reversed when the last endpoint sorts before the first
    """

    type: Literal["angle"] = "angle"
    atoms: Annotated[tuple[PositiveInt, PositiveInt, PositiveInt] | tuple[ResidueAtomRef, ResidueAtomRef, ResidueAtomRef], AfterValidator(_validate_atoms)]


class DihedralCoordinate(BaseModel):
    """Signed dihedral angle between four atoms, in degrees.

    Attributes:
        type: coordinate discriminator
        atoms: positive molecule atom indices (1-based) or PDB atom references, reversed when the last endpoint sorts before the first
    """

    type: Literal["dihedral"] = "dihedral"
    atoms: Annotated[
        tuple[PositiveInt, PositiveInt, PositiveInt, PositiveInt] | tuple[ResidueAtomRef, ResidueAtomRef, ResidueAtomRef, ResidueAtomRef],
        AfterValidator(_validate_atoms),
    ]


class LinearCombinationCoordinate(BaseModel):
    """Weighted sum of distances, in Å.

    Attributes:
        type: coordinate discriminator
        coordinates: distinct distances using one atom-reference convention
        coefficients: nonzero, dimensionless weights in coordinate order
    """

    type: Literal["linear_combination"] = "linear_combination"
    coordinates: Annotated[list[DistanceCoordinate], Field(min_length=1)]
    coefficients: list[FiniteFloat]

    @model_validator(mode="after")
    def validate_combination(self) -> Self:
        """Require matching nonzero weights and distinct, consistently addressed distances."""
        if len(self.coordinates) != len(self.coefficients):
            raise ValueError("Each coordinate requires one coefficient")
        if any(coefficient == 0 for coefficient in self.coefficients):
            raise ValueError("Coordinate coefficients must be nonzero")
        if len({frozenset(coordinate.atoms) for coordinate in self.coordinates}) != len(self.coordinates):
            raise ValueError("Combined distances must be unique")
        if len({isinstance(coordinate.atoms[0], int) for coordinate in self.coordinates}) != 1:
            raise ValueError("Combined distances must use one atom-reference convention")
        return self


Coordinate: TypeAlias = Annotated[
    DistanceCoordinate | AngleCoordinate | DihedralCoordinate | LinearCombinationCoordinate,
    Field(discriminator="type"),
]
