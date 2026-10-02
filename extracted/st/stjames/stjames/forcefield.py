"""Versioned schemas for ligand force-field parameterization."""

from typing import Any, Literal, Self

from pydantic import BaseModel, Field, PositiveInt, model_validator

from .base import LowercaseStrEnum
from .message import Message


class NonbondedParameter(BaseModel):
    """Nonbonded parameters for one mapped atom."""

    atom_map: PositiveInt
    charge: float
    sigma_angstrom: float
    epsilon_kj_mol: float


class BondParameter(BaseModel):
    """Harmonic bond between mapped atoms."""

    atom_maps: tuple[PositiveInt, PositiveInt]
    length_angstrom: float
    force_constant_kj_mol_angstrom2: float


class AngleParameter(BaseModel):
    """Harmonic angle between mapped atoms."""

    atom_maps: tuple[PositiveInt, PositiveInt, PositiveInt]
    angle_radians: float
    force_constant_kj_mol_radian2: float


class PeriodicTorsionTerm(BaseModel):
    """One ``k * (1 + cos(n*theta - phase))`` term."""

    periodicity: PositiveInt
    phase_radians: float
    force_constant_kj_mol: float


class TorsionParameter(BaseModel):
    """Periodic torsion terms assigned to four mapped atoms."""

    atom_maps: tuple[PositiveInt, PositiveInt, PositiveInt, PositiveInt]
    terms: list[PeriodicTorsionTerm]


class LigandParameterizationOutcome(LowercaseStrEnum):
    """Outcome of one ligand parameterization request."""

    MANGO = "mango"
    SAGE_GATE = "sage_gate"
    SAGE_FALLBACK = "sage_fallback"
    FAILED = "failed"


class MangoParameterSetV1(BaseModel):
    """Lossless mapped-atom Mango parameter set independent of OpenFF JSON.

    Explicit-hydrogen mapped SMILES is the topology and atom-identity source of
    truth. Atom maps must be unique and contiguous from one. Field names encode
    all units used by stored numerical parameters.
    """

    parameter_set_type: Literal["mango_parameter_set_v1"] = Field(default="mango_parameter_set_v1", frozen=True)
    mapped_smiles: str
    nonbonded: list[NonbondedParameter] = Field(min_length=1)
    bonds: list[BondParameter]
    angles: list[AngleParameter]
    proper_torsions: list[TorsionParameter]
    improper_torsions: list[TorsionParameter]
    release_id: str

    @model_validator(mode="after")
    def validate_atom_maps(self) -> Self:
        """Validate complete atom-map coverage and parameter references."""
        atom_maps = [parameter.atom_map for parameter in self.nonbonded]
        expected = set(range(1, len(atom_maps) + 1))
        if set(atom_maps) != expected or len(atom_maps) != len(expected):
            raise ValueError("nonbonded atom maps must be unique and contiguous from one")

        referenced = [
            atom_map
            for parameter in [
                *self.bonds,
                *self.angles,
                *self.proper_torsions,
                *self.improper_torsions,
            ]
            for atom_map in parameter.atom_maps
        ]
        if any(atom_map not in expected for atom_map in referenced):
            raise ValueError("parameter set contains an unknown atom map")
        return self


class LigandParameterizationResult(BaseModel):
    """Independent parameterization outcome for one named ligand."""

    outcome: LigandParameterizationOutcome
    parameter_set: MangoParameterSetV1 | None = None
    messages: list[Message] = Field(default_factory=list)
    error: str | None = None
    diagnostics: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_outcome(self) -> Self:
        """Require parameters for successful outcomes and errors for failures."""
        if self.outcome == "failed":
            if self.parameter_set is not None:
                raise ValueError("failed ligand parameterization cannot contain a parameter set")
            if not self.error:
                raise ValueError("failed ligand parameterization must include an error")
        elif self.parameter_set is None:
            raise ValueError("successful ligand parameterization must contain a parameter set")
        return self
