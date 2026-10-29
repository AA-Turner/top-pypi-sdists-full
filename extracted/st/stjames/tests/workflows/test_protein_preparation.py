"""Test protein preparation residue selector serialization."""

from stjames.workflows.protein_preparation import ProteinPreparationWorkflow


def test_retained_residue_indices_survive_json_round_trip() -> None:
    """Restore indexed retention selectors from frontend JSON payloads."""
    workflow = ProteinPreparationWorkflow.model_validate(
        {
            "protein": "protein-uuid",
            "retain_non_polymer": {"100": "OCCO", "ZN": None},
        }
    )
    restored = ProteinPreparationWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.retain_non_polymer == {100: "OCCO", "ZN": None}
