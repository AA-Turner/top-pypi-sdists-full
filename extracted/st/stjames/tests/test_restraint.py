"""Workflow serialization and restraint-specific validation."""

from pytest import mark, raises

from stjames.pdb import ResidueAtomRef, ResidueRef
from stjames.restraint import MDRestraints, RestraintType
from stjames.workflows.protein_md import ProteinMolecularDynamicsWorkflow

RESIDUE = ResidueRef("polymer", "A", "A.145")
ATOM = ResidueAtomRef(RESIDUE, "SG")


def test_restraint_workflow_roundtrip() -> None:
    """Preserve mixed selections and both restraint modes through workflow JSON."""
    restraints = [
        MDRestraints(restraint_type=RestraintType.POSITION, selections=[RESIDUE], force_constant=1),
        MDRestraints(restraint_type=RestraintType.DISTANCE, selections=[RESIDUE, ATOM], force_constant=2, target=4, flat_bottom_range=1),
    ]
    workflow = ProteinMolecularDynamicsWorkflow(protein="00000000-0000-0000-0000-000000000001", restraints=restraints)
    assert ProteinMolecularDynamicsWorkflow.model_validate_json(workflow.model_dump_json()).restraints == restraints
    with raises(ValueError):
        MDRestraints.model_validate({**restraints[0].model_dump(), "selections": [[RESIDUE, ATOM]]})
    with raises(ValueError, match="mutually exclusive"):
        ProteinMolecularDynamicsWorkflow(protein=workflow.protein, restraints=restraints, protein_restraint_cutoff=10)


@mark.parametrize(
    ("kind", "count", "target", "error"),
    [
        (RestraintType.POSITION, 1, 0, "do not accept a target"),
        (RestraintType.DISTANCE, 2, None, "require a target"),
        (RestraintType.ANGLE, 2, 120, "requires 3 selections"),
        (RestraintType.DIHEDRAL, 4, -181, "between -180 and 180"),
    ],
)
def test_invalid_geometry(kind: RestraintType, count: int, target: float | None, error: str) -> None:
    """Reject incompatible targets and selection counts."""
    with raises(ValueError, match=error):
        MDRestraints(restraint_type=kind, selections=[ATOM] * count, force_constant=1, target=target)
