"""Test redox potential behavior and validation."""

from pytest import fixture, mark, raises

from stjames import Method, Mode, Molecule, Settings, Solvent, SolventModel, Task
from stjames.workflows import RedoxPotentialWorkflow
from stjames.workflows.multistage_opt import MultiStageOptSettings


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


@fixture
def simple_msos() -> MultiStageOptSettings:
    """Provide two-stage optimization and single-point settings."""
    return MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
    )


def test_only_mecn(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Restrict redox potential calculations to acetonitrile solvent."""
    wf = RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=simple_msos, solvent=Solvent.ACETONITRILE)
    assert wf.solvent == Solvent.ACETONITRILE

    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=simple_msos, solvent=None)

    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=simple_msos, solvent=Solvent.WATER)


@mark.parametrize(
    ("mode", "sp_method"),
    [
        (Mode.RECKLESS, Method.GFN2_XTB),
        (Mode.RAPID, Method.R2SCAN3C),
        (Mode.CAREFUL, Method.WB97X3C),
        (Mode.METICULOUS, Method.WB97MD3BJ),
    ],
)
def test_auto_mso_from_mode(water: Molecule, mode: Mode, sp_method: Method) -> None:
    """MSO is auto-built from mode with acetonitrile on the singlepoint."""
    wf = RedoxPotentialWorkflow(initial_molecule=water, mode=mode)  # ty: ignore[missing-argument]

    sp = wf.multistage_opt_settings.singlepoint_settings
    assert sp is not None
    assert sp.method == sp_method
    assert sp.solvent_settings is not None
    assert sp.solvent_settings.solvent == Solvent.ACETONITRILE
    expected_model = SolventModel.CPCMX if sp_method == Method.GFN2_XTB else SolventModel.CPCM
    assert sp.solvent_settings.model == expected_model


def test_auto_mode_resolves_to_rapid(water: Molecule) -> None:
    """Mode.AUTO resolves to RAPID and triggers MSO auto-build."""
    wf = RedoxPotentialWorkflow(initial_molecule=water)  # ty: ignore[missing-argument]

    assert wf.mode == Mode.RAPID
    sp = wf.multistage_opt_settings.singlepoint_settings
    assert sp is not None
    assert sp.method == Method.R2SCAN3C


def test_user_msos_wins(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """User-supplied multistage_opt_settings is not overridden by mode."""
    wf = RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos)

    assert wf.multistage_opt_settings is simple_msos


def test_invalid_mode_still_raises(water: Molecule) -> None:
    """Modes outside VALID_REDOX_MODES are still rejected."""
    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.MANUAL)  # ty: ignore[missing-argument]


def test_no_half_reaction_rejected(water: Molecule) -> None:
    """Requesting neither reduction nor oxidation is rejected at construction."""
    with raises(ValueError, match="Neither reduction nor oxidation"):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, reduction=False, oxidation=False)  # ty: ignore[missing-argument]


def test_legacy_redox_type_not_falsely_rejected(water: Molecule) -> None:
    """Legacy redox_type sets the half-reaction; the check runs after that fixup."""
    wf = RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, redox_type="reduction", reduction=False, oxidation=False)  # ty: ignore[missing-argument]
    assert wf.reduction
    assert not wf.oxidation
