import logging

from pytest import LogCaptureFixture, raises

from stjames import (
    BasisSet,
    Constraint,
    ConstraintType,
    Engine,
    Method,
    Mode,
    OmegaTuning,
    OptimizationSettings,
    Settings,
    Solvent,
    SolventModel,
    SolventSettings,
    TDDFTSettings,
)
from stjames.engine_compatibility import ENGINE_DISABLED_TASKS, ENGINE_SOLVENT_MODELS
from stjames.task import Task


def test_set_mode_auto() -> None:
    Settings()
    assert Settings().mode == Mode.RAPID


def test_opt_settings() -> None:
    settings_rapid = Settings(mode=Mode.RAPID)
    settings_meticulous = Settings(mode=Mode.METICULOUS)

    cons = [Constraint(atoms=[1, 2], constraint_type=ConstraintType.BOND)]
    settings_careful = Settings(mode=Mode.CAREFUL, opt_settings=OptimizationSettings(constraints=cons))

    rap_opt_set = settings_rapid.opt_settings
    car_opt_set = settings_careful.opt_settings
    met_opt_set = settings_meticulous.opt_settings

    assert not rap_opt_set.constraints
    assert not met_opt_set.constraints
    assert car_opt_set.constraints == cons

    assert rap_opt_set.energy_threshold == 5e-5
    assert rap_opt_set.max_gradient_threshold == 5e-3
    assert rap_opt_set.rms_gradient_threshold == 3.5e-3

    assert car_opt_set.energy_threshold == 1e-6
    assert car_opt_set.max_gradient_threshold == 9e-4
    assert car_opt_set.rms_gradient_threshold == 6e-4

    assert met_opt_set.energy_threshold == 1e-6
    assert met_opt_set.max_gradient_threshold == 3e-5
    assert met_opt_set.rms_gradient_threshold == 2e-5


def test_omega() -> None:
    with raises(ValueError, match="Omega tuning may only be specified for range-separated DFT functionals"):
        Settings(method=Method.B3LYP, omega=OmegaTuning.KOOPMANS)

    Settings(method=Method.CAMB3LYP, omega=OmegaTuning.KOOPMANS)
    Settings(method=Method.CAMB3LYP, omega=0.3)


def test_tddft_settings_basic() -> None:
    """Test basic TDDFTSettings construction."""
    settings = Settings(
        method=Method.WB97MD3BJ,
        basis_set=BasisSet(name="def2-SVP"),
        omega=OmegaTuning.KOOPMANS,
        excited_state_settings=TDDFTSettings(
            tda=False,
            num_excitations=8,
            target_root=2,
        ),
        engine=Engine.PYSCF,
    )

    assert settings.method == Method.WB97MD3BJ
    assert settings.omega == OmegaTuning.KOOPMANS
    assert isinstance(settings.excited_state_settings, TDDFTSettings)
    assert settings.excited_state_settings.tda is False
    assert settings.excited_state_settings.num_excitations == 8
    assert settings.excited_state_settings.target_root == 2


def test_tddft_settings_custom() -> None:
    """Test TDDFTSettings with custom parameters."""
    settings = Settings(
        method=Method.B3LYP,
        basis_set=BasisSet(name="sto-3g"),
        excited_state_settings=TDDFTSettings(
            tda=True,
            num_excitations=10,
            target_root=5,
        ),
        engine=Engine.GPU4PYSCF,
    )

    assert settings.method == Method.B3LYP
    assert settings.omega is None
    assert isinstance(settings.excited_state_settings, TDDFTSettings)
    assert settings.excited_state_settings.tda is True
    assert settings.excited_state_settings.num_excitations == 10
    assert settings.excited_state_settings.target_root == 5


def test_settings_roundtrip() -> None:
    settings = Settings(
        method=Method.B3LYP,
        basis_set=BasisSet(name="sto-3g"),
        excited_state_settings=TDDFTSettings(num_excitations=5),
        engine=Engine.PYSCF,
    )

    data = settings.model_dump(mode="json")
    assert isinstance(data, dict)
    assert isinstance(data["excited_state_settings"], dict)

    stjames_settings = Settings.model_validate(data)

    assert stjames_settings.method == settings.method
    assert stjames_settings.basis_set == settings.basis_set
    assert stjames_settings.engine == settings.engine
    assert isinstance(stjames_settings.excited_state_settings, TDDFTSettings)
    assert stjames_settings.excited_state_settings == settings.excited_state_settings


def test_gpu4pyscf_solvent() -> None:
    with raises(ValueError, match="gpu4pyscf does not support the COSMO solvent model"):
        Settings(
            method=Method.B3LYP,
            basis_set=BasisSet(name="sto-3g"),
            solvent_settings=SolventSettings(model=SolventModel.COSMO, solvent=Solvent.HEXANE),
            engine=Engine.GPU4PYSCF,
        )


def test_unsupported_solvent_model() -> None:
    """Engines reject solvent models they don't support."""
    with raises(ValueError, match="psi4 does not support the ALPB solvent model"):
        Settings(
            method=Method.B3LYP,
            basis_set=BasisSet(name="sto-3g"),
            solvent_settings=SolventSettings(model=SolventModel.ALPB, solvent=Solvent.WATER),
            engine=Engine.PSI4,
        )

    with raises(ValueError, match="xtb does not support the COSMO solvent model"):
        Settings(
            method=Method.GFN2_XTB,
            solvent_settings=SolventSettings(model=SolventModel.COSMO, solvent=Solvent.WATER),
            engine=Engine.XTB,
        )


def test_cosmors_forces_recipe() -> None:
    """The cosmors solvent model pins BP86/def2-TZVPD regardless of input."""
    settings = Settings(
        method=Method.HARTREE_FOCK,
        solvent_settings=SolventSettings(model=SolventModel.COSMORS, solvent=Solvent.WATER),
    )
    assert settings.method == Method.BP86
    assert settings.basis_set is not None
    assert settings.basis_set.name.lower() == "def2-tzvpd"
    assert settings.engine == Engine.GPU4PYSCF
    assert settings.level_of_theory == "bp86/def2-tzvpd/cosmors(water)"


def test_cosmors_engine_selection() -> None:
    """cosmors runs on PySCF or GPU4PySCF, defaulting to GPU4PySCF."""
    assert SolventModel.COSMORS in ENGINE_SOLVENT_MODELS[Engine.PYSCF]
    assert SolventModel.COSMORS in ENGINE_SOLVENT_MODELS[Engine.GPU4PYSCF]

    default = Settings(
        solvent_settings=SolventSettings(model=SolventModel.COSMORS, solvent=Solvent.OCTANOL),
    )
    assert default.engine == Engine.GPU4PYSCF

    pyscf = Settings(
        solvent_settings=SolventSettings(model=SolventModel.COSMORS, solvent=Solvent.OCTANOL),
        engine=Engine.PYSCF,
    )
    assert pyscf.engine == Engine.PYSCF


def test_cosmors_recipe_override_logs(caplog: LogCaptureFixture) -> None:
    """Forcing the recipe warns only when it overrides a conflicting request."""
    with caplog.at_level(logging.WARNING, logger="stjames.settings"):
        Settings(
            method=Method.HARTREE_FOCK,
            engine=Engine.GPU4PYSCF,
            solvent_settings=SolventSettings(model=SolventModel.COSMORS, solvent=Solvent.WATER),
        )
    assert "overrides the requested recipe" in caplog.text
    assert "Method.HARTREE_FOCK" in caplog.text
    assert "Engine.GPU4PYSCF" in caplog.text

    # A bare cosmors request (nothing to override) is silent.
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger="stjames.settings"):
        Settings(solvent_settings=SolventSettings(model=SolventModel.COSMORS, solvent=Solvent.WATER))
    assert caplog.text == ""


def test_periodic_material_property_task_support() -> None:
    """Band structure stays QE-only; elastic tensor is enabled for QE, TBLite, and OMOL25."""
    elastic_enabled = {Engine.QUANTUM_ESPRESSO, Engine.TBLITE, Engine.OMOL25}
    for engine, disabled in ENGINE_DISABLED_TASKS.items():
        assert (Task.BAND_STRUCTURE in disabled) == (engine != Engine.QUANTUM_ESPRESSO)
        assert (Task.ELASTIC_TENSOR not in disabled) == (engine in elastic_enabled)
