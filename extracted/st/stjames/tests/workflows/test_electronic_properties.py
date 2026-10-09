"""Test electronic properties behavior and validation."""

from typing import Literal

import pytest
from pytest import fixture

from stjames import (
    Atom,
    ElectronicPropertiesWorkflow,
    ExcitedState,
    MolecularOrbitalCube,
    Molecule,
    NaturalTransitionOrbitalPair,
    OrbitalTransition,
    PropertyCube,
    PropertyCubePoint,
    Settings,
)
from stjames.basis_set import BasisSet
from stjames.engine import Engine
from stjames.excited_state_settings import TDDFTSettings
from stjames.method import Method


def cube() -> PropertyCube:
    """Build volumetric orbital data for electronic-property tests."""
    return PropertyCube(cube_points=[PropertyCubePoint(x=0, y=0, z=0, val=0.1), PropertyCubePoint(x=0.2, y=0, z=0, val=-0.1)])


def pair(index: int = 1, weight: float = 0.9, spin: Literal["", "α", "β"] = "") -> NaturalTransitionOrbitalPair:
    """Build natural transition orbital pairs with adjustable spin."""
    return NaturalTransitionOrbitalPair(index=index, weight=weight, spin=spin, hole=cube(), particle=cube())


def tddft_settings(num_excitations: int = 5) -> Settings:
    """Provide time-dependent DFT settings for excited-state tests."""
    return Settings(
        method=Method.PBE,
        basis_set=BasisSet(name="def2-SVP"),
        engine=Engine.PYSCF,
        excited_state_settings=TDDFTSettings(num_excitations=num_excitations),
    )


@fixture
def Mn() -> Molecule:
    """Provide open-shell manganese geometry."""
    return Molecule(charge=0, multiplicity=2, atoms=[Atom(atomic_number=25, position=(0, 0, 0))])


@fixture
def Fe() -> Molecule:
    """Provide iron geometry for electronic-state tests."""
    return Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=26, position=(0, 0, 0))])


def test_electronic_properties(Mn: Molecule, Fe: Molecule) -> None:
    """Initialize electronic-property workflows with empty results and explicit output flags."""
    epw1 = ElectronicPropertiesWorkflow(
        initial_molecule=Mn,
        settings=Settings(
            method=Method.PBE,
            basis_set=BasisSet(name="def2-SVP"),
        ),
    )

    assert epw1.compute_density_cube is True
    assert epw1.compute_electrostatic_potential_cube is True
    assert epw1.compute_num_occupied_orbitals == 1
    assert epw1.compute_num_virtual_orbitals == 1
    assert epw1.calc_uuid is None
    assert epw1.dipole is None
    assert epw1.quadrupole is None
    assert epw1.lowdin_charges is None
    assert epw1.mulliken_charges is None
    assert epw1.wiberg_bond_orders == []
    assert epw1.mayer_bond_orders == []
    assert epw1.density_cube is None
    assert epw1.density_cube_alpha is None
    assert epw1.density_cube_beta is None
    assert epw1.density_cube_difference is None
    assert epw1.electrostatic_potential_cube is None
    assert epw1.molecular_orbitals == {}
    assert epw1.molecular_orbitals_alpha == {}
    assert epw1.molecular_orbitals_beta == {}
    assert epw1.ground_state_energy is None
    assert epw1.excited_states == []

    epw2 = ElectronicPropertiesWorkflow(
        initial_molecule=Fe,
        settings=Settings(
            method=Method.PBE0,
            basis_set=BasisSet(name="def2-SVP"),
        ),
        compute_density_cube=False,
        compute_electrostatic_potential_cube=False,
        compute_num_occupied_orbitals=2,
        compute_num_virtual_orbitals=2,
    )

    assert epw2.compute_density_cube is False
    assert epw2.compute_electrostatic_potential_cube is False
    assert epw2.compute_num_occupied_orbitals == 2
    assert epw2.compute_num_virtual_orbitals == 2
    assert epw2.calc_uuid is None
    assert epw2.dipole is None
    assert epw2.quadrupole is None
    assert epw2.lowdin_charges is None
    assert epw2.mulliken_charges is None
    assert epw2.wiberg_bond_orders == []
    assert epw2.mayer_bond_orders == []
    assert epw2.density_cube is None
    assert epw2.density_cube_alpha is None
    assert epw2.density_cube_beta is None
    assert epw2.density_cube_difference is None
    assert epw2.electrostatic_potential_cube is None
    assert epw2.molecular_orbitals == {}
    assert epw2.molecular_orbitals_alpha == {}
    assert epw2.molecular_orbitals_beta == {}
    assert epw2.ground_state_energy is None
    assert epw2.excited_states == []


def test_molecular_orbital_symmetry() -> None:
    """Verify molecular orbital symmetry."""
    mo = MolecularOrbitalCube(cube_points=[], occupation=2, energy=-0.5)
    assert mo.symmetry is None

    labeled = MolecularOrbitalCube(cube_points=[], occupation=2, energy=-0.5, symmetry="a1g")
    assert labeled.symmetry == "a1g"
    assert MolecularOrbitalCube.model_validate(labeled.model_dump()).symmetry == "a1g"


@pytest.mark.parametrize("engine", [Engine.PSI4, Engine.PYSCF, Engine.GPU4PYSCF])
def test_allowed_engines(Mn: Molecule, engine: Engine) -> None:
    """Verify allowed engines."""
    epw = ElectronicPropertiesWorkflow(
        initial_molecule=Mn,
        settings=Settings(method=Method.PBE, basis_set=BasisSet(name="def2-SVP"), engine=engine),
    )

    assert epw.settings.engine == engine


@pytest.mark.parametrize(
    ("method", "engine"),
    [
        (Method.PBE, Engine.QUANTUM_ESPRESSO),
        (Method.GFN2_XTB, Engine.XTB),
        (Method.AIMNET2_WB97MD3, Engine.AIMNET2),
    ],
)
def test_disallowed_engines(Mn: Molecule, method: Method, engine: Engine) -> None:
    """Verify disallowed engines."""
    with pytest.raises(ValueError, match="Unsupported engine"):
        ElectronicPropertiesWorkflow(initial_molecule=Mn, settings=Settings(method=method, engine=engine))


def test_excited_states(Fe: Molecule) -> None:
    """Preserve excited-state roots, transitions, and orbital pairs."""
    epw = ElectronicPropertiesWorkflow(
        initial_molecule=Fe,
        settings=tddft_settings(),
        ground_state_energy=-1262.123456,
        excited_states=[
            ExcitedState(
                root=1,
                energy=-1262.0,
                oscillator_strength=0.1234,
                transitions=[OrbitalTransition(occupied=4, virtual=12, amplitude=0.7, weight=0.98)],
                transition_density=cube(),
            ),
            ExcitedState(transition_density=cube(), root=2, energy=-1261.9, oscillator_strength=0.0, natural_transition_orbitals=[pair(1, 0.8), pair(2, 0.15)]),
        ],
    )

    assert [state.root for state in epw.excited_states] == [1, 2]
    assert epw.excited_states[1].natural_transition_orbitals[0].spin == ""
    assert epw.excited_states[1].transition_density == cube()
    assert ElectronicPropertiesWorkflow.model_validate_json(epw.model_dump_json()).excited_states[0].transition_density == cube()


def test_no_excited_state_settings(Fe: Molecule) -> None:
    """Verify no excited state settings."""
    epw = ElectronicPropertiesWorkflow(initial_molecule=Fe, settings=Settings(method=Method.PBE, basis_set=BasisSet(name="def2-SVP")))

    assert epw.settings.excited_state_settings is None
    assert epw.excited_states == []


def test_root_out_of_range(Fe: Molecule) -> None:
    """Verify root out of range."""
    with pytest.raises(ValueError, match="excited_states roots must be <= num_excitations"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Fe,
            settings=tddft_settings(),
            ground_state_energy=-1262.0,
            excited_states=[ExcitedState(transition_density=cube(), root=9, energy=-1261.0, oscillator_strength=0.1)],
        )


@pytest.mark.parametrize("roots", [(2, 1), (1, 1)])
def test_unordered_roots(Fe: Molecule, roots: tuple[int, int]) -> None:
    """Verify unordered roots."""
    with pytest.raises(ValueError, match="excited_states roots must be unique and ascending"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Fe,
            settings=tddft_settings(),
            ground_state_energy=-1262.0,
            excited_states=[ExcitedState(transition_density=cube(), root=root, energy=-1261.0, oscillator_strength=0.1) for root in roots],
        )


def test_ground_state_energy_alone(Fe: Molecule) -> None:
    """Verify ground state energy alone."""
    epw = ElectronicPropertiesWorkflow(initial_molecule=Fe, settings=tddft_settings(), ground_state_energy=-1262.1234567)

    assert epw.ground_state_energy == -1262.123457
    assert epw.excited_states == []


def test_open_shell_natural_transition_orbitals(Mn: Molecule) -> None:
    """Verify open shell natural transition orbitals."""
    epw = ElectronicPropertiesWorkflow(
        initial_molecule=Mn,
        settings=tddft_settings(),
        ground_state_energy=-1150.0,
        excited_states=[
            ExcitedState(
                transition_density=cube(),
                root=1,
                energy=-1149.9,
                oscillator_strength=0.01,
                transitions=[OrbitalTransition(occupied=5, virtual=8, amplitude=0.7, weight=0.9, spin="α")],
                natural_transition_orbitals=[pair(1, 0.7, "α"), pair(1, 0.2, "β")],
            )
        ],
    )

    assert [nto.spin for nto in epw.excited_states[0].natural_transition_orbitals] == ["α", "β"]


def test_restricted_pairs_on_open_shell(Mn: Molecule) -> None:
    """Verify restricted pairs on open shell."""
    with pytest.raises(ValueError, match="natural_transition_orbitals of root 1 has spin"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Mn,
            settings=tddft_settings(),
            ground_state_energy=-1150.0,
            excited_states=[
                ExcitedState(transition_density=cube(), root=1, energy=-1149.9, oscillator_strength=0.01, natural_transition_orbitals=[pair(1, 0.7)])
            ],
        )


def test_alpha_pairs_on_closed_shell(Fe: Molecule) -> None:
    """Verify alpha pairs on closed shell."""
    with pytest.raises(ValueError, match="natural_transition_orbitals of root 1 has spin"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Fe,
            settings=tddft_settings(),
            ground_state_energy=-1262.0,
            excited_states=[
                ExcitedState(transition_density=cube(), root=1, energy=-1261.0, oscillator_strength=0.01, natural_transition_orbitals=[pair(1, 0.7, "α")])
            ],
        )


def test_alpha_transitions_on_closed_shell(Fe: Molecule) -> None:
    """Verify alpha transitions on closed shell."""
    with pytest.raises(ValueError, match="transitions of root 1 has spin"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Fe,
            settings=tddft_settings(),
            ground_state_energy=-1262.0,
            excited_states=[
                ExcitedState(
                    transition_density=cube(),
                    root=1,
                    energy=-1261.0,
                    oscillator_strength=0.01,
                    transitions=[OrbitalTransition(occupied=4, virtual=12, amplitude=0.7, weight=0.9, spin="α")],
                )
            ],
        )


def test_duplicate_pair_index(Fe: Molecule) -> None:
    """Verify duplicate pair index."""
    with pytest.raises(ValueError, match="must have unique"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Fe,
            settings=tddft_settings(),
            ground_state_energy=-1262.0,
            excited_states=[
                ExcitedState(
                    transition_density=cube(), root=1, energy=-1261.0, oscillator_strength=0.01, natural_transition_orbitals=[pair(1, 0.7), pair(1, 0.2)]
                )
            ],
        )


def test_ascending_pair_weights(Mn: Molecule) -> None:
    """Verify ascending pair weights."""
    with pytest.raises(ValueError, match="must be ordered by non-increasing weight"):
        ElectronicPropertiesWorkflow(
            initial_molecule=Mn,
            settings=tddft_settings(),
            ground_state_energy=-1150.0,
            excited_states=[
                ExcitedState(
                    transition_density=cube(),
                    root=1,
                    energy=-1149.9,
                    oscillator_strength=0.01,
                    natural_transition_orbitals=[pair(1, 0.2, "α"), pair(1, 0.7, "β")],
                )
            ],
        )


def test_excited_state_round_trip() -> None:
    """Verify excited state round trip."""
    state = ExcitedState(
        root=1,
        energy=-75.841235,
        oscillator_strength=0.0123,
        transitions=[OrbitalTransition(occupied=4, virtual=12, amplitude=-0.7071, weight=0.5)],
        natural_transition_orbitals=[pair(1, 0.95)],
        transition_density=cube(),
    )

    assert ExcitedState.model_validate_json(state.model_dump_json()) == state


def test_rounding() -> None:
    """Round excited-state energies, orbital weights, and transition strengths to schema precision."""
    state = ExcitedState(
        transition_density=cube(),
        root=1,
        energy=-75.8412345678,
        oscillator_strength=0.00012345,
        rotatory_strength=-1.234567,
        transitions=[OrbitalTransition(occupied=1, virtual=2, amplitude=0.1234567, weight=0.1234567)],
        natural_transition_orbitals=[pair(1, 0.1234567)],
    )

    assert state.energy == -75.841235
    assert state.oscillator_strength == 0.0001
    assert state.rotatory_strength == -1.2346
    assert state.transitions[0].amplitude == 0.123457
    assert state.transitions[0].weight == 0.123457
    assert state.natural_transition_orbitals[0].weight == 0.123457
