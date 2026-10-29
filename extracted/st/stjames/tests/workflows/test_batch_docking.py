"""Test batch docking settings, serialization and compatibility."""

from typing import Literal

from pytest import mark, raises

from stjames.workflows.batch_docking import BatchDockingWorkflow
from stjames.workflows.docking import TurboDockPreset, TurboDockSettings, VinaSettings

_PROTEIN = "c3524c98-2e64-4573-89de-ed467026df44"
_POCKET = ((0, 0, 0), (20, 20, 20))


@mark.parametrize(
    ("preset", "exhaustiveness", "max_search_steps", "scoring_function", "run_mmgbsa"),
    [
        (TurboDockPreset.FAST, 128, 20, "vina", False),
        (TurboDockPreset.BALANCED, 384, 40, "vinardo", True),
        (TurboDockPreset.RIGOROUS, 512, 40, "vina", False),
    ],
)
def test_turbodock_roundtrip(
    preset: TurboDockPreset,
    exhaustiveness: int,
    max_search_steps: int,
    scoring_function: Literal["vina", "vinardo"],
    run_mmgbsa: bool,
) -> None:
    """Preserve explicit search and refinement settings while ignoring legacy fields."""
    settings = TurboDockSettings.from_preset(preset, scoring_function=scoring_function, max_poses=3)
    workflow = BatchDockingWorkflow.model_validate(
        {
            "initial_smiles_list": ["CCO"],
            "protein": _PROTEIN,
            "pocket": _POCKET,
            "docking_settings": settings.model_dump() | {"batch_size": 1800},
            "num_poses_to_save": 10,
            "run_mmgbsa": run_mmgbsa,
        }
    )
    restored = BatchDockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.model_dump() == {
        "settings_type": "turbodock",
        "max_poses": 3,
        "scoring_function": scoring_function,
        "exhaustiveness": exhaustiveness,
        "max_search_steps": max_search_steps,
    }
    assert restored.num_poses_to_save == 10
    assert restored.run_mmgbsa is run_mmgbsa


def test_vina_keeps_mmgbsa_and_custom_settings() -> None:
    """Preserve Vina scoring and search controls alongside MM/GBSA refinement."""
    workflow = BatchDockingWorkflow.model_validate(
        {
            "initial_smiles_list": ["CCO"],
            "protein": _PROTEIN,
            "pocket": _POCKET,
            "docking_settings": {
                "settings_type": "vina",
                "scoring_function": "vinardo",
                "exhaustiveness": 32,
                "max_poses": 5,
            },
            "num_poses_to_save": 10,
            "run_mmgbsa": True,
        }
    )
    restored = BatchDockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.model_dump() == workflow.docking_settings.model_dump()
    assert restored.run_mmgbsa is True


def test_batch_docking_defaults_to_vina() -> None:
    """Preserve the default Vina workflow when no engine settings are supplied."""
    workflow = BatchDockingWorkflow.model_validate({"initial_smiles_list": ["CCO"], "protein": _PROTEIN, "pocket": _POCKET})
    restored = BatchDockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.settings_type == "vina"
    assert restored.run_mmgbsa is False


@mark.parametrize("settings", [{}, {"exhaustiveness": 32, "max_poses": 5}])
def test_legacy_vina_settings_without_discriminator(settings: dict[str, int]) -> None:
    """Keep accepting Vina settings serialized before batch docking supported multiple engines."""
    before = settings.copy()
    workflow = BatchDockingWorkflow.model_validate(
        {
            "initial_smiles_list": ["CCO"],
            "protein": _PROTEIN,
            "pocket": _POCKET,
            "docking_settings": settings,
            "run_mmgbsa": True,
        }
    )
    assert settings == before
    restored = BatchDockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.settings_type == "vina"
    assert restored.docking_settings.model_dump() == VinaSettings.model_validate(before).model_dump()
    assert restored.run_mmgbsa is True


def test_batch_docking_rejects_unknown_engine() -> None:
    """Reject explicit unknown engine tags instead of treating them as Vina."""
    with raises(ValueError):
        BatchDockingWorkflow.model_validate(
            {
                "initial_smiles_list": ["CCO"],
                "protein": _PROTEIN,
                "pocket": _POCKET,
                "docking_settings": {"settings_type": "unknown"},
            }
        )


def test_turbodock_preset_returns_independent_settings() -> None:
    """Keep named defaults intact when a caller changes its returned settings."""
    first = TurboDockSettings.from_preset(TurboDockPreset.BALANCED)
    expected = first.model_dump()
    first.exhaustiveness = 1
    first.max_search_steps = 1
    assert TurboDockSettings.from_preset(TurboDockPreset.BALANCED).model_dump() == expected
