"""Test pocket settings migration and mixed-solvent sampling controls."""

from typing import Any

from pydantic import ValidationError
from pytest import approx, mark, raises

from stjames import Method, MixMDSettings, PocketDetectionWorkflow, PocketeerSettings, ProteinForceField, Solvent, WaterForceField


@mark.parametrize(
    ("fields", "distance"),
    [
        ({"merge_distance": 2.5}, 2.5),
        ({"merge_distance": 0}, 0),
        ({"merge_distance": 2.5, "settings": PocketeerSettings()}, 2.5),
        ({"merge_distance": 2.5, "settings": PocketeerSettings(merge_distance=1.75)}, 1.75),
        ({"merge_distance": 2.5, "settings": {"settings_type": "pocketeer", "merge_distance": 3.5}}, 3.5),
    ],
)
def test_merge_distance_compatibility(fields: dict[str, Any], distance: float) -> None:
    """Promote legacy distance without replacing explicitly supplied settings."""
    workflow = PocketDetectionWorkflow.model_validate({"protein": "protein-uuid"} | fields)
    restored = PocketDetectionWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.model_dump()["settings"]["merge_distance"] == approx(distance)


def test_mixmd_settings_roundtrip() -> None:
    """Preserve probe, force fields, and shared controls through the settings union."""
    settings = MixMDSettings(
        probe=Solvent.ISOPROPANOL,
        small_molecule_ff=Method.OFF_SAGE_2_2_1,
        protein_ff=ProteinForceField.FF19SB,
        water_ff=WaterForceField.OPC,
        hydrogen_mass=2,
        constrain_hydrogens=False,
        nonbonded_cutoff=9,
        random_seed=42,
        langevin_timescale_ps=2,
        ionic_strength_M=0.2,
        frame_save_interval_ps=0.1,
        analysis_interval_ps=0.3,
    )
    workflow = PocketDetectionWorkflow(protein="protein-uuid", settings=settings, merge_distance=9)
    restored = PocketDetectionWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.settings == settings
    assert restored.model_dump(mode="json")["settings"]["probe"] == Solvent.ISOPROPANOL.value


@mark.parametrize(
    "fields",
    [
        {"small_molecule_ff": Method.MANGO_1_0_0},
        {"analysis_interval_ps": 5},
        {"analysis_interval_ps": 15},
        {"simulation_time_ns": 1, "analysis_interval_ps": 1000},
    ],
)
def test_invalid_mixmd_protocol(fields: dict[str, Any]) -> None:
    """Reject unsupported force fields and invalid analysis windows or cadences."""
    with raises(ValidationError):
        MixMDSettings.model_validate(fields)
