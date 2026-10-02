import pytest
from pydantic import TypeAdapter, ValidationError

from stjames.types import NonPolymerResidueMapping, ProteinMDTrajectory
from stjames.workflows.protein_md import BindingPoseTrajectory


def test_protein_md_trajectory_radius_of_gyration():
    traj = ProteinMDTrajectory(
        uuid="test-uuid",
        isotropic_radius_of_gyration=[4.1, 4.2],
        mean_structure_uuid="mean-uuid",
        median_structure_frame_index=1,
    )
    assert traj.isotropic_radius_of_gyration == [4.1, 4.2]


def test_binding_pose_trajectory_inherits_radius_of_gyration():
    traj = BindingPoseTrajectory(
        uuid="test-uuid",
        isotropic_radius_of_gyration=[4.1, 4.2],
        mean_structure_uuid="mean-uuid",
        median_structure_frame_index=1,
    )
    assert traj.isotropic_radius_of_gyration == [4.1, 4.2]


def test_non_polymer_residue_mapping_accepts_parameterized_molecules_and_known_ions() -> None:
    """Residue mapping accepts SMILES and template-backed ions."""
    mapping = {"NAD": "NC(=O)c1ccncc1", "ZN": None}

    assert TypeAdapter(NonPolymerResidueMapping).validate_python(mapping) == mapping


@pytest.mark.parametrize("mapping", [{"NAD": ""}, {"NAD": None}, {0: None}])
def test_non_polymer_residue_mapping_rejects_missing_parameterization(
    mapping: dict[str | int, str | None],
) -> None:
    """Unknown residues and indexed residues require non-empty SMILES."""
    with pytest.raises(ValidationError, match="non-polymer residue entry"):
        TypeAdapter(NonPolymerResidueMapping).validate_python(mapping)
