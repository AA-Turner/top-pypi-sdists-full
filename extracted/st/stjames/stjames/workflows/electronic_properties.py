"""Electronic properties workflow."""

from itertools import pairwise
from typing import Annotated, Literal, Self

from pydantic import AfterValidator, BaseModel, Field, NonNegativeFloat, NonNegativeInt, PositiveInt, model_validator

from ..base import round_float, round_optional_float
from ..engine import Engine
from ..excited_state_settings import TDDFTSettings
from ..settings import Settings
from ..types import UUID, FloatPerAtom, Matrix3x3, Vector3D, round_optional_float_per_atom, round_optional_matrix3x3, round_optional_vector3d
from .workflow import MoleculeWorkflow

ALLOWED_ENGINES = {Engine.PSI4, Engine.PYSCF, Engine.GPU4PYSCF}


class PropertyCubePoint(BaseModel):
    """
    A point in a cube file, all values rounded to 6 decimal places.

    :param x: x coordinate, in Å
    :param y: y coordinate, in Å
    :param z: z coordinate, in Å
    :param val: value of property at point, in atomic units (property dependent)
    """

    x: Annotated[float, AfterValidator(round_float(3))]
    y: Annotated[float, AfterValidator(round_float(3))]
    z: Annotated[float, AfterValidator(round_float(3))]
    val: Annotated[float, AfterValidator(round_float(6))]


class PropertyCube(BaseModel):
    """
    Represents a "cubefile" of some property.

    :param cube_points: points of property on an axis-aligned grid, coordinates in Å
    """

    cube_points: list[PropertyCubePoint]


class MolecularOrbitalCube(PropertyCube):
    """
    Cube of a molecular orbital.

    Inherits `cube_data`.

    :param occupation: number of electrons occupying orbital
    :param energy: orbital energy, in Hartree
    :param symmetry: irreducible representation label (e.g. a1g), if available
    """

    occupation: NonNegativeInt
    energy: Annotated[float, AfterValidator(round_float(6))]
    symmetry: str | None = None


class OrbitalTransition(BaseModel):
    """
    Single occupied → virtual contribution to an excitation.

    :param occupied: 1-indexed occupied MO, over all MOs of its spin block
    :param virtual: 1-indexed virtual MO, over all MOs of its spin block
    :param amplitude: excitation coefficient of pair, dimensionless
    :param weight: fractional contribution of pair to excitation, dimensionless
    :param spin: spin block of pair, empty for restricted reference
    """

    occupied: PositiveInt
    virtual: PositiveInt
    amplitude: Annotated[float, AfterValidator(round_float(6))]
    weight: Annotated[float, Field(ge=0, le=1), AfterValidator(round_float(6))]
    spin: Literal["", "α", "β"] = ""


class NaturalTransitionOrbitalPair(BaseModel):
    """
    Hole/particle natural transition orbital pair of one excited state.

    :param index: 1-indexed pair within its spin block, descending by weight
    :param weight: fraction of excitation described by pair (λ), dimensionless
    :param spin: spin block of pair, empty for restricted reference
    :param hole: hole (occupied) NTO, as a cube
    :param particle: particle (virtual) NTO, as a cube
    """

    index: PositiveInt
    weight: Annotated[float, Field(ge=0, le=1), AfterValidator(round_float(6))]
    spin: Literal["", "α", "β"] = ""
    hole: PropertyCube
    particle: PropertyCube


class ExcitedState(BaseModel):
    """
    Excited state of the molecule.

    λ over `natural_transition_orbitals` may sum to less than 1, as pairs of
    negligible weight are omitted; the truncation threshold is not recorded. For
    an unrestricted reference the sum runs over both spin blocks together.

    :param root: 1-indexed root, ordered by ascending energy
    :param energy: absolute energy of root, in Hartree
    :param oscillator_strength: transition strength from ground state, dimensionless
    :param rotatory_strength: signed velocity-gauge ECD rotatory strength from ground state, in 10⁻⁴⁰ esu²·cm²
    :param transitions: dominant occupied → virtual contributions, descending by weight
    :param natural_transition_orbitals: hole/particle NTO pairs, descending by weight
    :param transition_density: signed, spin-summed ground-to-excited-state transition density on a spatial grid, in atomic units
    """

    root: PositiveInt
    energy: Annotated[float, AfterValidator(round_float(6))]
    oscillator_strength: Annotated[float, AfterValidator(round_float(4))]
    rotatory_strength: Annotated[float | None, AfterValidator(round_optional_float(4))] = None
    transitions: list[OrbitalTransition] = []
    natural_transition_orbitals: list[NaturalTransitionOrbitalPair] = []
    transition_density: PropertyCube


class ElectronicPropertiesWorkflow(MoleculeWorkflow):
    """
    Workflow for computing electronic properties.

    Inherited
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow (currently unused)

    Config settings:
    :param settings: settings for the calculation
    :param compute_density_cube: whether to compute the density cube
    :param compute_electrostatic_potential_cube: whether to compute the electrostatic potential cube
    :param compute_num_occupied_orbitals: number of occupied orbitals to save
    :param compute_num_virtual_orbitals: number of virtual orbitals to save

    Populated while running:
    :param calc_uuid: UUID of the calculation
    :param dipole: dipole moment, in Debye
    :param quadrupole: quadrupole moment, in atomic units (e·a₀²)
    :param lowdin_charges: Löwdin charges, in e
    :param mulliken_charges: Mulliken charges, in e
    :param wiberg_bond_orders: Wiberg bond orders (`atom1`, `atom2`, `order`), dimensionless
    :param mayer_bond_orders: Mayer bond orders (`atom1`, `atom2`, `order`), dimensionless

    :param density_cube: electron density, as a cube
    :param density_cube_alpha: α electron density, as a cube
    :param density_cube_beta: β electron density, as a cube
    :param density_cube_difference: difference spin densities, as a cube

    :param electrostatic_potential_cube: electrostatic potential, as a cube

    :param molecular_orbitals: MOs, key is absolute orbital index (for closed-shell species (RHF))
    :param molecular_orbitals_alpha: α MOs, key is absolute orbital index (for open-shell species (UHF/ROHF))
    :param molecular_orbitals_beta: β MOs, key is absolute orbital index (for open-shell species (UHF/ROHF))

    :param ground_state_energy: absolute energy of root 0, in Hartree
    :param excited_states: computed excited states, ordered by root, populated whenever the calculation carried excited-state settings

    :raises ValueError: if engine is not Psi4, PySCF, or GPU4PySCF
    """

    # Config settings
    settings: Settings
    compute_density_cube: bool = True
    compute_electrostatic_potential_cube: bool = True
    compute_num_occupied_orbitals: NonNegativeInt = 1
    compute_num_virtual_orbitals: NonNegativeInt = 1

    # Results
    calc_uuid: UUID | None = None

    dipole: Annotated[Vector3D | None, AfterValidator(round_optional_vector3d(6))] = None
    quadrupole: Annotated[Matrix3x3 | None, AfterValidator(round_optional_matrix3x3(6))] = None

    mulliken_charges: Annotated[FloatPerAtom | None, AfterValidator(round_optional_float_per_atom(6))] = None
    lowdin_charges: Annotated[FloatPerAtom | None, AfterValidator(round_optional_float_per_atom(6))] = None

    wiberg_bond_orders: list[tuple[NonNegativeInt, NonNegativeInt, NonNegativeFloat]] = []
    mayer_bond_orders: list[tuple[NonNegativeInt, NonNegativeInt, NonNegativeFloat]] = []

    density_cube: PropertyCube | None = None
    density_cube_alpha: PropertyCube | None = None
    density_cube_beta: PropertyCube | None = None
    density_cube_difference: PropertyCube | None = None

    electrostatic_potential_cube: PropertyCube | None = None

    molecular_orbitals: dict[NonNegativeInt, MolecularOrbitalCube] = {}
    molecular_orbitals_alpha: dict[NonNegativeInt, MolecularOrbitalCube] = {}
    molecular_orbitals_beta: dict[NonNegativeInt, MolecularOrbitalCube] = {}

    ground_state_energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    excited_states: list[ExcitedState] = []

    @model_validator(mode="after")
    def validate_engine(self) -> Self:
        """Ensure engine supports electronic properties."""
        if self.settings.engine not in ALLOWED_ENGINES:
            allowed = ", ".join(sorted(engine.value for engine in ALLOWED_ENGINES))
            raise ValueError(f"Unsupported engine: {self.settings.engine}, must be one of: {allowed}")

        return self

    @model_validator(mode="after")
    def validate_roots(self) -> Self:
        """Ensure roots are within range, unique, and ascending."""
        roots = [state.root for state in self.excited_states]

        if roots != sorted(set(roots)):
            raise ValueError(f"excited_states roots must be unique and ascending: {roots}")

        excited_state_settings = self.settings.excited_state_settings
        if isinstance(excited_state_settings, TDDFTSettings):
            num_excitations = excited_state_settings.num_excitations
            if any(root > num_excitations for root in roots):
                raise ValueError(f"excited_states roots must be <= num_excitations ({num_excitations}): {roots}")

        return self

    @model_validator(mode="after")
    def validate_natural_transition_orbitals(self) -> Self:
        """Ensure NTO pairs are uniquely labelled, ordered, and spin-tagged to match the reference."""
        restricted = self.initial_molecule.multiplicity == 1
        allowed_spins = {""} if restricted else {"α", "β"}

        for state in self.excited_states:
            pairs = state.natural_transition_orbitals

            keys = [(pair.spin, pair.index) for pair in pairs]
            if len(set(keys)) != len(keys):
                raise ValueError(f"natural_transition_orbitals of root {state.root} must have unique (spin, index): {keys}")

            weights = [pair.weight for pair in pairs]
            if any(later > earlier for earlier, later in pairwise(weights)):
                raise ValueError(f"natural_transition_orbitals of root {state.root} must be ordered by non-increasing weight: {weights}")

            for pair in pairs:
                if pair.spin not in allowed_spins:
                    raise ValueError(f"natural_transition_orbitals of root {state.root} has spin {pair.spin!r}, must be one of: {sorted(allowed_spins)}")

            for transition in state.transitions:
                if transition.spin not in allowed_spins:
                    raise ValueError(f"transitions of root {state.root} has spin {transition.spin!r}, must be one of: {sorted(allowed_spins)}")

        return self
