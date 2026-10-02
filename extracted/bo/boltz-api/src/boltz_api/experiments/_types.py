from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from ..types.predictions import structure_and_binding_start_params
from ..types.small_molecule import design_start_params as small_molecule_design_start_params

SmallMoleculeTargetEntityModification: TypeAlias = (
    small_molecule_design_start_params.TargetEntityProteinEntityModification
)
SmallMoleculeTargetEntity: TypeAlias = small_molecule_design_start_params.TargetEntity

SmallMoleculeTargetBondAtom: TypeAlias = structure_and_binding_start_params.InputBondAtom1
SmallMoleculeTargetBond: TypeAlias = structure_and_binding_start_params.InputBond

SmallMoleculeTargetConstraintContactToken: TypeAlias = (
    structure_and_binding_start_params.InputConstraintContactConstraintToken1
)
SmallMoleculeTargetConstraint: TypeAlias = structure_and_binding_start_params.InputConstraint


class SmallMoleculeTarget(TypedDict, total=False):
    """Scientist SDK target shape for small molecule workflows."""

    entities: Required[Iterable[SmallMoleculeTargetEntity]]
    type: Literal["no_template"]
    pocket_residues: Dict[str, Iterable[int]]
    reference_ligands: SequenceNotStr[str]
    bonds: Iterable[SmallMoleculeTargetBond]
    constraints: Iterable[SmallMoleculeTargetConstraint]
