"""Test types behavior and validation."""

import json

import pytest
from pydantic import TypeAdapter, ValidationError

from stjames.types import NonPolymerResidueMapping, ProteinMDTrajectory
from stjames.workflows.protein_md import BindingPoseTrajectory


def test_protein_md_trajectory_radius_of_gyration():
    """Preserve radius-of-gyration measurements and representative-frame metadata."""
    traj = ProteinMDTrajectory(
        uuid="test-uuid",
        isotropic_radius_of_gyration=[4.1, 4.2],
        mean_structure_uuid="mean-uuid",
        median_structure_frame_index=1,
    )
    assert traj.isotropic_radius_of_gyration == [4.1, 4.2]


def test_binding_pose_trajectory_inherits_radius_of_gyration():
    """Preserve inherited radius-of-gyration fields in binding pose trajectories."""
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


@pytest.mark.parametrize("mapping", [{0: "CCO", 100: "OCCO", "EDO": "OCCO", "ZN": None}, {}])
def test_non_polymer_residue_mapping_json_round_trip(mapping: dict[str | int, str | None]) -> None:
    """Preserve residue indices through SDK and HTTP JSON serialization."""
    adapter = TypeAdapter(NonPolymerResidueMapping)
    assert adapter.validate_json(adapter.dump_json(mapping)) == mapping
    assert adapter.validate_python(json.loads(json.dumps(mapping))) == mapping


def test_non_polymer_residue_mapping_frontend_keys() -> None:
    """Normalize frontend decimal keys while preserving alphanumeric residue names."""
    mapping = {"000": "CCO", "100": "OCCO", "1PE": "CCO", "EDO": "OCCO", "ZN": None}
    assert TypeAdapter(NonPolymerResidueMapping).validate_python(mapping) == {
        0: "CCO",
        100: "OCCO",
        "1PE": "CCO",
        "EDO": "OCCO",
        "ZN": None,
    }
    assert "000" in mapping


@pytest.mark.parametrize("mapping", [{-1: "CCO"}, {"-1": "CCO"}, {"100": None}, {100: "CCO", "100": "CO"}, {"0": "CCO", "00": "CO"}])
def test_non_polymer_residue_mapping_rejects_invalid_indices(mapping: dict[str | int, str | None]) -> None:
    """Reject negative indices, missing SMILES, and ambiguous duplicate selectors."""
    with pytest.raises(ValidationError):
        TypeAdapter(NonPolymerResidueMapping).validate_python(mapping)
