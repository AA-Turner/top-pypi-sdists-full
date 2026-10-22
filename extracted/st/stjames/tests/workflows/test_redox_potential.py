"""Test redox potential behavior and validation."""

from pytest import fixture, mark, param, raises

from stjames import Method, Mode, Molecule, Settings, Solvent, SolventModel, SolventSettings, Task
from stjames.workflows import RedoxPotentialWorkflow
from stjames.workflows.multistage_opt import MultiStageOptSettings


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


MECN_CPCM = SolventSettings(solvent=Solvent.ACETONITRILE, model=SolventModel.CPCM)
MECN_CPCMX = SolventSettings(solvent=Solvent.ACETONITRILE, model=SolventModel.CPCMX)
MECN_ALPB = SolventSettings(solvent=Solvent.ACETONITRILE, model=SolventModel.ALPB)


@fixture
def simple_msos() -> MultiStageOptSettings:
    """Provide two-stage optimization and single-point settings."""
    return MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C, solvent_settings=MECN_CPCM),
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


def test_invalid_mode_still_raises(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Modes outside VALID_REDOX_MODES are still rejected."""
    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.DEBUG, multistage_opt_settings=simple_msos)


@mark.parametrize("nnp", [Method.UMA_S_1_2_OMOL, Method.ORB_V3_CONSERVATIVE_OMOL])
@mark.parametrize("mode", [param({}, id="omitted"), param({"mode": None}, id="null")])
def test_custom_msos_without_mode_is_manual(water: Molecule, mode: dict[str, None], nnp: Method) -> None:
    """User-supplied settings with an omitted or null mode are recorded as MANUAL and kept as given."""
    msos = MultiStageOptSettings(
        optimization_settings=[Settings(method=nnp, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=nnp, tasks=[Task.ENERGY], solvent_settings=MECN_CPCMX),
    )
    wf = RedoxPotentialWorkflow(initial_molecule=water, multistage_opt_settings=msos, **mode)

    assert wf.mode == Mode.MANUAL
    assert wf.multistage_opt_settings is msos
    assert RedoxPotentialWorkflow.model_validate_json(wf.model_dump_json()).multistage_opt_settings.level_of_theory == msos.level_of_theory


def test_manual_requires_msos(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """MANUAL mode is accepted with settings and rejected without them."""
    assert RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.MANUAL, multistage_opt_settings=simple_msos).mode == Mode.MANUAL

    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.MANUAL)  # ty: ignore[missing-argument]


def test_energy_stage_without_singlepoint(water: Molecule) -> None:
    """Last optimization defines the energy when there is no singlepoint, so it must be solvated."""
    solvated = Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE], solvent_settings=MECN_ALPB)
    RedoxPotentialWorkflow(initial_molecule=water, multistage_opt_settings=MultiStageOptSettings(optimization_settings=[solvated]))

    gas = Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])
    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, multistage_opt_settings=MultiStageOptSettings(optimization_settings=[gas]))


GFN2_OPT = Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])


@mark.parametrize(
    ("optimization_settings", "singlepoint_settings"),
    [
        param([], Settings(method=Method.R2SCAN3C, solvent_settings=MECN_CPCM), id="no optimization"),
        param(
            [Settings(method=Method.AIMNET2_WB97MD3, tasks=[Task.OPTIMIZE])],
            Settings(method=Method.R2SCAN3C, solvent_settings=MECN_CPCM),
            id="closed-shell engine",
        ),
        param(
            [Settings(method=Method.ORB_V3_CONSERVATIVE_INF_OMAT, tasks=[Task.OPTIMIZE])],
            Settings(method=Method.R2SCAN3C, solvent_settings=MECN_CPCM),
            id="no charge or spin",
        ),
        param(
            [GFN2_OPT],
            Settings(method=Method.R2SCAN3C, solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCM)),
            id="not acetonitrile",
        ),
        param([GFN2_OPT], Settings(method=Method.R2SCAN3C), id="unsolvated singlepoint"),
        param([GFN2_OPT], Settings(method=Method.GFN_FF, solvent_settings=MECN_ALPB), id="force field singlepoint"),
        param([GFN2_OPT], Settings(method=Method.GFN0_XTB, solvent_settings=MECN_ALPB), id="non-self-consistent singlepoint"),
    ],
)
def test_invalid_custom_msos(water: Molecule, optimization_settings: list[Settings], singlepoint_settings: Settings) -> None:
    """Settings that cannot compute an acetonitrile redox potential are rejected."""
    msos = MultiStageOptSettings(optimization_settings=optimization_settings, singlepoint_settings=singlepoint_settings)
    with raises(ValueError):
        RedoxPotentialWorkflow(initial_molecule=water, multistage_opt_settings=msos)


def test_no_half_reaction_rejected(water: Molecule) -> None:
    """Requesting neither reduction nor oxidation is rejected at construction."""
    with raises(ValueError, match="Neither reduction nor oxidation"):
        RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, reduction=False, oxidation=False)  # ty: ignore[missing-argument]


def test_legacy_redox_type_not_falsely_rejected(water: Molecule) -> None:
    """Legacy redox_type sets the half-reaction; the check runs after that fixup."""
    wf = RedoxPotentialWorkflow(initial_molecule=water, mode=Mode.RAPID, redox_type="reduction", reduction=False, oxidation=False)  # ty: ignore[missing-argument]
    assert wf.reduction
    assert not wf.oxidation
