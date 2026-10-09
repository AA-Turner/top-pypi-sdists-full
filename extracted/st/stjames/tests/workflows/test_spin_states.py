"""Test spin states behavior and validation."""

from pydantic import ValidationError
from pytest import fixture, mark, raises

from stjames import Atom, Method, Molecule, Settings, Task
from stjames.workflows import MultiStageOptSettings, SpinStatesWorkflow
from stjames.workflows.spin_states import SpinState


@fixture
def Mn() -> Molecule:
    """Provide open-shell manganese geometry."""
    return Molecule(charge=0, multiplicity=2, atoms=[Atom(atomic_number=25, position=(0, 0, 0))])


@fixture
def Fe() -> Molecule:
    """Provide iron geometry for electronic-state tests."""
    return Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=26, position=(0, 0, 0))])


@fixture
def simple_msos() -> MultiStageOptSettings:
    """Provide two-stage optimization and single-point settings."""
    return MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
    )


def test_raises(Mn: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Reject incompatible spin-state multiplicities and optimization modes."""
    with raises(ValidationError):
        # ty is correct, but needs to be silenced to test pydantic error
        SpinStatesWorkflow(initial_molecule=Mn, multistage_opt_settings=simple_msos)  # ty: ignore[missing-argument]

    with raises(ValueError):
        SpinStatesWorkflow(
            initial_molecule=Mn,
            states=[1, 3, 4],
            multistage_opt_settings=simple_msos,
        )

    with raises(ValueError):
        SpinStatesWorkflow(
            initial_molecule=Mn,
            states=[2, 4, 5],
            multistage_opt_settings=simple_msos,
        )

    with raises(ValidationError):
        # missing multistage_opt_settings
        SpinStatesWorkflow(initial_molecule=Mn, states=[2, 4, 6])  # ty: ignore[missing-argument]


@mark.smoke
def test_manual(Fe: Molecule) -> None:
    """Builds a manual SpinStatesWorkflow."""
    optimization_settings = [
        Settings(method=Method.GFN0_XTB, tasks=[Task.OPTIMIZE]),
        Settings(method=Method.B3LYP, basis_set="def2-SVP", tasks=[Task.OPTIMIZE]),
    ]
    singlepoint_settings = Settings(method=Method.PBE, basis_set="def2-TZVP")
    msos = MultiStageOptSettings(
        optimization_settings=optimization_settings,
        singlepoint_settings=singlepoint_settings,
    )
    spin_states = SpinStatesWorkflow(
        initial_molecule=Fe,
        states=[1, 3, 5],
        multistage_opt_settings=msos,
    )

    assert spin_states.states == [1, 3, 5]
    assert spin_states.level_of_theory == "pbe/def2-tzvp//b3lyp/def2-svp//gfn0_xtb"
    assert str(spin_states) == "<SpinStatesWorkflow [1, 3, 5] pbe/def2-tzvp//b3lyp/def2-svp//gfn0_xtb>"

    msos = spin_states.multistage_opt_settings
    assert msos
    assert msos.optimization_settings
    assert len(msos.optimization_settings) == 2
    assert msos.singlepoint_settings
    assert msos.singlepoint_settings.method == Method.PBE
    assert msos.singlepoint_settings.basis_set
    assert msos.singlepoint_settings.basis_set.name == "def2-TZVP"
    assert msos.singlepoint_settings.solvent_settings is None

    msos_opt0, msos_opt1 = msos.optimization_settings

    assert msos_opt0.method == Method.GFN0_XTB
    assert msos_opt0.tasks == [Task.OPTIMIZE]
    assert msos_opt0.corrections == []
    assert msos_opt0.solvent_settings is None

    assert msos_opt1.method == Method.B3LYP
    assert msos_opt1.tasks == [Task.OPTIMIZE]
    assert msos_opt1.corrections == []
    assert msos_opt1.solvent_settings is None
    assert msos_opt1.basis_set
    assert msos_opt1.basis_set.name == "def2-SVP"


def test_frequencies(Mn: Molecule) -> None:
    """Propagate frequency calculations to spin-state optimization stages."""
    msos_freq = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE, Task.FREQUENCIES])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
        frequencies=True,
    )
    spin_states = SpinStatesWorkflow(
        initial_molecule=Mn,
        states=[2, 4, 6],
        multistage_opt_settings=msos_freq,
    )
    assert spin_states.multistage_opt_settings.frequencies


def test_validate_spin_states(Fe: Molecule, simple_msos: MultiStageOptSettings) -> None:
    """Test validation of computed spin state results."""
    ss = SpinStatesWorkflow(initial_molecule=Fe, states=[1, 3, 5], multistage_opt_settings=simple_msos)
    assert ss.spin_states == []

    with raises(ValueError):
        SpinStatesWorkflow(
            initial_molecule=Fe,
            states=[1, 3, 5],
            multistage_opt_settings=simple_msos,
            spin_states=[
                SpinState(multiplicity=1, energy=-10.0, calculation=[]),
                SpinState(multiplicity=1, energy=-9.0, calculation=[]),  # duplicate
            ],
        )
