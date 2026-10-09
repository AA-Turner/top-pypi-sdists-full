"""Test phonons behavior and validation."""

from pytest import fixture, raises

from stjames import Atom, Mode, Molecule, OptimizationSettings, Settings
from stjames.method import Method
from stjames.workflows import (
    WORKFLOW_MAPPING,
    PhononBandStructure,
    PhononDensityOfStates,
    PhononResult,
    PhononSettings,
    PhononThermalProperties,
    PhononWorkflow,
    ZoneCenterMode,
    ZoneCenterModes,
)


@fixture
def molecular_Si() -> Molecule:
    """Provide nonperiodic silicon geometry."""
    return Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=14, position=(0, 0, 0))])


@fixture
def result() -> PhononResult:
    """Provide phonon bands, density of states, and thermodynamic results."""
    return PhononResult(
        band_structure=PhononBandStructure(
            qpoint_distances=[0.0, 1.0],
            frequencies=[[0.0, 0.0, 10.0], [1.0, 2.0, 11.0]],
            high_symmetry_points=[("Γ", 0.0), ("X", 1.0)],
        ),
        density_of_states=PhononDensityOfStates(frequency_points=[0.0, 5.0], projected=[[0.1, 0.2], [0.0, 0.3]], projection_labels=[14, 14]),
        thermal_properties=PhononThermalProperties(
            temperatures=[0.0, 300.0], free_energy=[0.01, 0.005], entropy=[0.0, 1.2e-4], heat_capacity=[0.0, 2.3e-4], zero_point_energy=0.012
        ),
        zone_center_modes=ZoneCenterModes(
            point_group="Oh",
            modes=[
                ZoneCenterMode(
                    frequency=0.0,
                    symmetry_label="T1u",
                    electric_dipole_allowed=True,
                    electric_dipole_dipole_polarizability_allowed=False,
                    displacements=[(0, 0, 0), (0, 0, 0)],
                ),
                ZoneCenterMode(
                    frequency=520.0,
                    symmetry_label="T2g",
                    electric_dipole_allowed=False,
                    electric_dipole_dipole_polarizability_allowed=True,
                    displacements=[(0.1, 0, 0), (-0.1, 0, 0)],
                ),
            ],
        ),
        min_frequency=-0.3,
        imaginary_fraction=0.0,
    )


def test_registered() -> None:
    """Resolve the workflow name to its registered schema class."""
    assert WORKFLOW_MAPPING["phonons"] is PhononWorkflow


def test_requires_periodic(molecular_Si: Molecule) -> None:
    """Reject phonon calculations on molecules without periodic cells."""
    with raises(ValueError, match="periodic"):
        PhononWorkflow(
            initial_molecule=molecular_Si,
            phonon_settings=PhononSettings(settings=Settings(method=Method.PBE, opt_settings=OptimizationSettings(optimize_cell=True))),
        )


def test_unset_mode_defaults_to_careful() -> None:
    """Phonons need tighter forces than the Rapid default."""
    settings = PhononSettings(settings={"method": "pbe", "opt_settings": {"optimize_cell": True}}).settings

    assert settings.mode is Mode.CAREFUL
    assert settings.opt_settings.max_gradient_threshold == 9e-4

    assert PhononSettings(settings={"method": "pbe", "mode": "auto", "opt_settings": {"optimize_cell": True}}).settings.mode is Mode.CAREFUL


def test_prebuilt_settings_taken_as_given() -> None:
    """A prebuilt Settings has already resolved its mode."""
    assert PhononSettings(settings=Settings(method=Method.PBE, opt_settings=OptimizationSettings(optimize_cell=True))).settings.mode is Mode.RAPID


def test_rejects_constraints() -> None:
    """Constrained geometries are not stationary points, so frequencies are meaningless."""
    constraints = [{"constraint_type": "freeze_atoms", "atoms": [1]}]

    with raises(ValueError, match="does not support constraints"):
        PhononSettings(settings={"method": "pbe", "opt_settings": {"constraints": constraints}})


def test_rejects_transition_state() -> None:
    """Transition states are not minima, so phonon frequencies are meaningless."""
    with raises(ValueError, match="does not support transition state"):
        PhononSettings(settings={"method": "pbe", "opt_settings": {"transition_state": True}})


def test_derived_accessors(result: PhononResult) -> None:
    """Compute internal energy and total density of states from stored results."""
    assert result.thermal_properties.internal_energy == [0.01, 0.041]
    assert result.density_of_states.total == [0.1, 0.5]


def test_dump_excludes_derived(result: PhononResult) -> None:
    """Omit derived properties from serialized phonon result data."""
    dumped = result.model_dump()
    assert "stability_mesh_frequencies" not in dumped
    assert "gamma_frequencies" not in dumped
    assert "internal_energy" not in dumped["thermal_properties"]
    assert "total" not in dumped["density_of_states"]


def test_round_trip(result: PhononResult) -> None:
    """Preserve calculation results through JSON serialization and validation."""
    restored = PhononResult.model_validate_json(result.model_dump_json())
    assert restored.imaginary_fraction == 0.0
    assert restored.min_frequency == -0.3
    assert [mode.frequency for mode in restored.zone_center_modes.modes] == [0.0, 520.0]
