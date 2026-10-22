"""Test multistage opt workflow behavior and validation."""

from pytest import fixture, mark, raises

from stjames import Atom, BasisSet, Method, Molecule, Settings, Solvent, SolventModel, SolventSettings, Task
from stjames.workflows import MultiStageOptWorkflow, build_mso_settings, multi_stage_opt_settings_from_workflow
from stjames.workflows.multistage_opt import MultiStageOptSettings


@fixture
def He() -> Molecule:
    """Provide helium geometry for optimization tests."""
    return Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=(0, 0, 0))])


def test_basic(He: Molecule) -> None:
    """Construct multistage optimization workflows for helium."""
    s1 = Settings(method=Method.GFN0_XTB, tasks=[Task.OPTIMIZE])
    s2 = Settings(method=Method.R2SCAN3C)
    msos = MultiStageOptSettings(optimization_settings=[s1], singlepoint_settings=s2)

    assert msos.level_of_theory == "r2scan_3c//gfn0_xtb"
    assert str(msos) == "<MultiStageOptSettings r2scan_3c//gfn0_xtb>"
    assert msos.optimization_settings
    assert msos.singlepoint_settings


def test_workflow(He: Molecule) -> None:
    """Preserve completed calculation results in optimization workflows."""
    s1 = Settings(method=Method.GFN0_XTB, tasks=[Task.OPTIMIZE])
    s2 = Settings(method=Method.R2SCAN3C, solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCM))
    msow = MultiStageOptWorkflow(initial_molecule=He, optimization_settings=[s1], singlepoint_settings=s2)

    assert msow.level_of_theory == "r2scan_3c/cpcm(water)//gfn0_xtb"
    assert str(msow) == "<MultiStageOptWorkflow r2scan_3c/cpcm(water)//gfn0_xtb>"
    assert msow.optimization_settings
    assert msow.singlepoint_settings


def test_manual(He: Molecule) -> None:
    """Builds a manual MultiStageOptWorkflow."""
    optimization_settings = [
        Settings(method=Method.GFN0_XTB, tasks=[Task.OPTIMIZE]),
        Settings(method=Method.B3LYP, basis_set=BasisSet(name="def2-SVP"), tasks=[Task.OPTIMIZE]),
    ]
    singlepoint_settings = Settings(
        method=Method.PBE, basis_set=BasisSet(name="def2-TZVP"), solvent_settings=SolventSettings(solvent=Solvent.OCTANE, model=SolventModel.CPCM)
    )
    msow = MultiStageOptWorkflow(initial_molecule=He, optimization_settings=optimization_settings, singlepoint_settings=singlepoint_settings)

    level_of_theory = "pbe/def2-tzvp/cpcm(octane)//b3lyp/def2-svp//gfn0_xtb"

    assert str(msow) == f"<MultiStageOptWorkflow {level_of_theory}>"
    assert msow.level_of_theory == level_of_theory

    assert msow.optimization_settings
    assert len(msow.optimization_settings) == 2

    assert msow.singlepoint_settings
    assert msow.singlepoint_settings.method == Method.PBE
    assert msow.singlepoint_settings.basis_set
    assert msow.singlepoint_settings.basis_set.name == "def2-TZVP"
    assert msow.singlepoint_settings.solvent_settings
    assert msow.singlepoint_settings.solvent_settings.solvent == "octane"

    msow_opt0, msow_opt1 = msow.optimization_settings

    assert msow_opt0.method == Method.GFN0_XTB
    assert msow_opt0.basis_set is None
    assert msow_opt0.tasks == [Task.OPTIMIZE]
    assert msow_opt0.corrections == []
    assert msow_opt0.solvent_settings is None

    assert msow_opt1.method == Method.B3LYP
    assert msow_opt1.basis_set
    assert msow_opt1.basis_set == BasisSet(name="def2-SVP")
    assert msow_opt1.tasks == [Task.OPTIMIZE]
    assert msow_opt1.corrections == []
    assert msow_opt1.solvent_settings is None


def test_manual_from_factory(He: Molecule) -> None:
    """Builds a manual MultiStageOptWorkflow via build_mso_settings."""
    msos = build_mso_settings(
        sp_method=Method.PBE,
        sp_basis_set=BasisSet(name="def2-TZVP"),
        opt_methods=[Method.GFN0_XTB, Method.B3LYP],
        opt_basis_sets=[None, BasisSet(name="def2-SVP")],
        solvent=Solvent.OCTANE,
        use_solvent_for_opt=False,
    )

    level_of_theory = "pbe/def2-tzvp/cpcm(octane)//b3lyp/def2-svp//gfn0_xtb"

    assert str(msos) == f"<MultiStageOptSettings {level_of_theory}>"
    assert msos.level_of_theory == level_of_theory

    assert msos.optimization_settings
    assert len(msos.optimization_settings) == 2

    assert msos.singlepoint_settings
    assert msos.singlepoint_settings.method == Method.PBE
    assert msos.singlepoint_settings.basis_set
    assert msos.singlepoint_settings.basis_set.name == "def2-TZVP"
    assert msos.singlepoint_settings.solvent_settings
    assert msos.singlepoint_settings.solvent_settings.solvent == "octane"

    msos_opt0, msos_opt1 = msos.optimization_settings

    assert msos_opt0.method == Method.GFN0_XTB
    assert msos_opt0.basis_set is None
    assert msos_opt0.tasks == [Task.OPTIMIZE]
    assert msos_opt0.corrections == []
    assert msos_opt0.solvent_settings is None

    assert msos_opt1.method == Method.B3LYP
    assert msos_opt1.basis_set
    assert msos_opt1.basis_set == BasisSet(name="def2-SVP")
    assert msos_opt1.tasks == [Task.OPTIMIZE]
    assert msos_opt1.corrections == []
    assert msos_opt1.solvent_settings is None


def test_build_mso_settings_solvent_for_opt() -> None:
    """Test that use_solvent_for_opt correctly applies solvent to opt steps."""
    msos_no_solv = build_mso_settings(
        sp_method=Method.R2SCAN3C,
        sp_basis_set=None,
        opt_methods=[Method.GFN2_XTB],
        opt_basis_sets=[None],
        solvent=Solvent.HEXANE,
        use_solvent_for_opt=False,
    )
    msos_with_solv = build_mso_settings(
        sp_method=Method.R2SCAN3C,
        sp_basis_set=None,
        opt_methods=[Method.GFN2_XTB],
        opt_basis_sets=[None],
        solvent=Solvent.HEXANE,
        use_solvent_for_opt=True,
    )

    assert msos_no_solv.optimization_settings[0].solvent_settings is None
    assert msos_no_solv.singlepoint_settings
    assert msos_no_solv.singlepoint_settings.solvent_settings
    assert msos_no_solv.singlepoint_settings.solvent_settings.solvent == "hexane"

    assert msos_with_solv.optimization_settings[0].solvent_settings is not None
    assert msos_with_solv.optimization_settings[0].solvent_settings.solvent == "hexane"
    assert msos_with_solv.singlepoint_settings
    assert msos_with_solv.singlepoint_settings.solvent_settings
    assert msos_with_solv.singlepoint_settings.solvent_settings.solvent == "hexane"


def test_msos_from_msow(He: Molecule) -> None:
    """Round-trip: MultiStageOptWorkflow → MultiStageOptSettings."""
    s1 = Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])
    s2 = Settings(method=Method.WB97X3C, solvent_settings=SolventSettings(solvent=Solvent.ACETONE, model=SolventModel.CPCM))
    msow = MultiStageOptWorkflow(initial_molecule=He, optimization_settings=[s1], singlepoint_settings=s2)

    msos = multi_stage_opt_settings_from_workflow(msow)

    assert msos.level_of_theory == msow.level_of_theory
    assert msos.optimization_settings
    assert len(msos.optimization_settings) == 1
    assert msos.singlepoint_settings
    assert msos.singlepoint_settings.method == Method.WB97X3C
    assert msos.singlepoint_settings.solvent_settings
    assert msos.singlepoint_settings.solvent_settings.solvent == "acetone"

    assert msos.optimization_settings[0].method == Method.GFN2_XTB


@mark.parametrize(
    ("method", "model"),
    [
        (Method.GFN2_XTB, SolventModel.CPCMX),
        (Method.BP86, SolventModel.COSMORS),
    ],
)
def test_energy_only_solvent_rejected_for_optimization(He: Molecule, method: Method, model: SolventModel) -> None:
    """Solvent models without gradients are allowed on the singlepoint but not on optimizations."""
    sp = Settings(method=method, tasks=[Task.ENERGY], solvent_settings=SolventSettings(solvent=Solvent.WATER, model=model))
    opt = Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])
    MultiStageOptSettings(optimization_settings=[opt], singlepoint_settings=sp)

    solvated_opt = sp.model_copy(update={"tasks": [Task.OPTIMIZE]})
    with raises(ValueError):
        MultiStageOptSettings(optimization_settings=[solvated_opt])
    with raises(ValueError):
        MultiStageOptWorkflow(initial_molecule=He, optimization_settings=[solvated_opt])
