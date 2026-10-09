"""Test bde behavior and validation."""

from pytest import fixture, mark, raises

from stjames import Method, Mode, Molecule, Settings, Task
from stjames.workflows import BDE, BDEWorkflow
from stjames.workflows.multistage_opt import MultiStageOptSettings


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


@fixture
def ethane() -> Molecule:
    """Provide ethane geometry with equivalent hydrogen atoms."""
    return Molecule.from_xyz("""\
C  -0.75  0.00  0.00
C   0.75  0.00  0.00
H  -1.15  0.00 -1.00
H  -1.15 -1.00  0.50
H  -1.15  0.85  0.50
H   1.15 -0.85 -0.50
H   1.15  0.85 -0.50
H   1.15  0.00  1.10
""")


@fixture
def chloroethane() -> Molecule:
    """Provide chloroethane geometry with distinct bond environments."""
    return Molecule.from_xyz("""\
C  -0.75  0.00  0.00
C   0.75  0.00  0.00
Cl -1.15  0.00 -1.00
H  -1.15 -1.00  0.50
H  -1.15  0.85  0.50
H   1.15 -0.85 -0.50
H   1.15  0.85 -0.50
H   1.15  0.00  1.10
""")


@fixture
def simple_msos() -> MultiStageOptSettings:
    """Provide two-stage optimization and single-point settings."""
    return MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
    )


def test_raises(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Reject out-of-range atoms and incompatible BDE workflow settings."""
    with raises(ValueError):
        BDEWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=simple_msos, atoms=(5,))


def test_auto(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Resolve automatic BDE mode to rapid defaults."""
    wf = BDEWorkflow(initial_molecule=water, mode=Mode.AUTO, multistage_opt_settings=simple_msos, atoms=(1, 2))

    assert wf.mode == Mode.RAPID


def test_frequencies(water: Molecule) -> None:
    """Propagate frequency calculations through BDE optimization settings."""
    msos_freq = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
        frequencies=True,
    )
    msos_no_freq = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
    )
    wf = BDEWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=msos_freq, atoms=(1, 2))
    wf2 = BDEWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=msos_no_freq, atoms=(1, 2))
    wf3 = BDEWorkflow(initial_molecule=water, mode=Mode.RAPID, multistage_opt_settings=msos_no_freq, atoms=(1, 2))

    assert wf.multistage_opt_settings.frequencies
    assert not wf2.multistage_opt_settings.frequencies
    assert not wf3.multistage_opt_settings.frequencies


def test_water(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Select equivalent O-H bond dissociations without duplicate fragments."""
    all_Hs = BDEWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos, atoms=(1, 2), optimize_fragments=True)
    duplicated = BDEWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos, atoms=(1, 2, 1, 2))
    all_CH = BDEWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos, all_CH=True, optimize_fragments=False)
    all_CX = BDEWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos, all_CX=True)

    assert repr(all_Hs) == "<BDEWorkflow METICULOUS>"
    assert str(all_Hs) == "BDEWorkflow METICULOUS\n(1,)\n(2,)"

    assert all_Hs.fragment_indices == ((1,), (2,))
    assert duplicated.fragment_indices == ((1,), (2,))
    assert all_CH.fragment_indices == ()
    assert all_CX.fragment_indices == ()

    assert all_Hs.optimize_fragments
    assert duplicated.optimize_fragments
    assert not all_CH.optimize_fragments
    assert all_CX.optimize_fragments


def test_ethane(ethane: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Select equivalent ethane C-H dissociations without duplicate fragments."""
    all_Hs = BDEWorkflow(initial_molecule=ethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, atoms=(3, 4, 5, 6, 7, 8), optimize_fragments=True)
    duplicated = BDEWorkflow(initial_molecule=ethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, atoms=(3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8))
    all_CH = BDEWorkflow(initial_molecule=ethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, all_CH=True, optimize_fragments=False)
    all_CX = BDEWorkflow(initial_molecule=ethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, all_CX=True)
    ch3_frag_and_all_CH = BDEWorkflow(
        initial_molecule=ethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, fragment_indices=((2, 6, 7, 8),), all_CH=True
    )

    assert repr(all_Hs) == "<BDEWorkflow RAPID>"
    assert str(all_Hs) == "BDEWorkflow RAPID\n(3,)\n(4,)\n(5,)\n(6,)\n(7,)\n(8,)"

    assert all_Hs.fragment_indices == all_CH.fragment_indices
    assert all_Hs.fragment_indices == duplicated.fragment_indices
    assert all_CX.fragment_indices == ()
    assert ch3_frag_and_all_CH.fragment_indices == ((2, 6, 7, 8), (3,), (4,), (5,), (6,), (7,), (8,))

    assert all_Hs.optimize_fragments
    assert duplicated.optimize_fragments
    assert not all_CH.optimize_fragments
    assert all_CX.optimize_fragments
    assert ch3_frag_and_all_CH.optimize_fragments


def test_chloroethane(chloroethane: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Select distinct C-H and C-Cl dissociations in chloroethane."""
    all_Hs = BDEWorkflow(initial_molecule=chloroethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, atoms=(4, 5, 6, 7, 8))
    all_CH = BDEWorkflow(initial_molecule=chloroethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, all_CH=True)
    all_CX = BDEWorkflow(initial_molecule=chloroethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, all_CX=True)
    duplicated = BDEWorkflow(initial_molecule=chloroethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, all_CX=True, atoms=(3,))
    ch3_frag_and_all_CH = BDEWorkflow(
        initial_molecule=chloroethane, mode=Mode.RAPID, multistage_opt_settings=simple_msos, fragment_indices=((2, 6, 7, 8),), all_CH=True
    )

    assert repr(all_Hs) == "<BDEWorkflow RAPID>"
    assert str(all_Hs) == "BDEWorkflow RAPID\n(4,)\n(5,)\n(6,)\n(7,)\n(8,)"

    assert all_Hs.fragment_indices == all_CH.fragment_indices
    assert all_CX.fragment_indices == ((3,),)
    assert duplicated.fragment_indices == ((3,),)
    assert ch3_frag_and_all_CH.fragment_indices == ((2, 6, 7, 8), (4,), (5,), (6,), (7,), (8,))


@mark.parametrize(
    ("mode", "opt_frag"),
    [
        (Mode.RECKLESS, False),
        (Mode.RAPID, True),
        (Mode.CAREFUL, True),
        (Mode.METICULOUS, True),
    ],
)
def test_mode_defaults(chloroethane: Molecule, mode: Mode, opt_frag: bool, simple_msos: MultiStageOptSettings) -> None:
    """Verify mode defaults."""
    wf = BDEWorkflow(initial_molecule=chloroethane, mode=mode, multistage_opt_settings=simple_msos, atoms=(4, 5, 6, 7, 8))

    assert wf.fragment_indices == ((4,), (5,), (6,), (7,), (8,))
    assert wf.optimize_fragments == opt_frag


def test_BDE_none() -> None:
    """Test that a BDE with None for an energy is fine."""
    BDE(fragment_idxs=(1, 2), energy=None, fragment_energies=(1, None), calculation_uuids=(["1", "2"], ["2", "3"]))
    BDE(fragment_idxs=(1, 2), energy=None, fragment_energies=(None, 2), calculation_uuids=(["1", "2"], ["2", "3"]))
    BDE(fragment_idxs=(1, 2), energy=None, fragment_energies=(1, 2), calculation_uuids=(["1", "2"], ["2", "3"]))


@mark.parametrize(
    ("mode", "sp_method"),
    [
        (Mode.RECKLESS, Method.GFN2_XTB),
        (Mode.RAPID, Method.R2SCAN3C),
        (Mode.CAREFUL, Method.WB97X3C),
        (Mode.METICULOUS, Method.WB97MD3BJ),
    ],
)
def test_auto_mso_from_mode(chloroethane: Molecule, mode: Mode, sp_method: Method) -> None:
    """MSO is auto-built from mode when not supplied."""
    wf = BDEWorkflow(initial_molecule=chloroethane, mode=mode, atoms=(4,))  # ty: ignore[missing-argument]

    assert wf.multistage_opt_settings.singlepoint_settings is not None
    assert wf.multistage_opt_settings.singlepoint_settings.method == sp_method
    assert wf.multistage_opt_settings.singlepoint_settings.solvent_settings is None


def test_user_msos_wins(water: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """User-supplied multistage_opt_settings is not overridden by mode."""
    wf = BDEWorkflow(initial_molecule=water, mode=Mode.METICULOUS, multistage_opt_settings=simple_msos, atoms=(1,))

    assert wf.multistage_opt_settings is simple_msos


def test_new_methods(chloroethane: Molecule) -> None:
    """Resolve composite BDE method names to multistage settings."""
    g_xtb = BDEWorkflow(initial_molecule=chloroethane, mode="G_XTB", atoms=(4, 5, 6, 7, 8))  # ty: ignore[missing-argument]
    g_xtb__gfn2_xtb = BDEWorkflow(initial_molecule=chloroethane, mode="G_XTB//GFN2_XTB", all_CH=True)  # ty: ignore[missing-argument]
    BDEWorkflow(initial_molecule=chloroethane, mode="R2SCAN3C//GFN2_XTB", all_CX=True)  # ty: ignore[missing-argument]
    BDEWorkflow(initial_molecule=chloroethane, mode="OMOL25_CONSERVING_S", all_CX=True, atoms=(3,))  # ty: ignore[missing-argument]

    assert str(g_xtb) == "BDEWorkflow G_XTB\n(4,)\n(5,)\n(6,)\n(7,)\n(8,)"
    assert repr(g_xtb__gfn2_xtb) == "<BDEWorkflow G_XTB//GFN2_XTB>"
    assert g_xtb.multistage_opt_settings is not None
    assert g_xtb__gfn2_xtb.multistage_opt_settings is not None
