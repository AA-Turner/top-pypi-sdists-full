import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Iterable, Self, Sequence, TypeAlias, TypedDict, TypeVar

import numpy as np
import pydantic
from pydantic import AfterValidator, NonNegativeInt, PositiveInt, ValidationError

from .atom import Atom
from .base import Base, round_float, round_optional_float
from .cosmors import COSMORSData
from .data import SYMBOL_ELEMENT
from .periodic_cell import PeriodicCell
from .periodic_properties import BandStructure
from .types import (
    FloatPerAtom,
    Matrix3x3,
    Matrix6x6,
    Vector3D,
    Vector3DPerAtom,
    round_list,
    round_optional_float_per_atom,
    round_optional_matrix3x3,
    round_optional_matrix6x6,
    round_optional_vector3d,
    round_optional_vector3d_per_atom,
    round_vector3d_per_atom,
    round_xrd_peaks,
)

logger = logging.getLogger(__name__)


def _coerce_metadata_value(s: str) -> bool | float | int | str:
    """
    Coerce a string from an XYZ comment line to the most specific scalar type.

    :param s: raw string value
    :return: bool, int, float, or str

    >>> _coerce_metadata_value("true")
    True
    >>> _coerce_metadata_value("False")
    False
    >>> _coerce_metadata_value("42")
    42
    >>> _coerce_metadata_value("1.25")
    1.25
    >>> _coerce_metadata_value("hello")
    'hello'
    """
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


# 1 Hartree/Å³ in GPa, from CODATA 2018 (Hartree = 4.3597447222060e-18 J).
HARTREE_PER_CUBIC_ANGSTROM_TO_GPA = 4359.7447222060

if TYPE_CHECKING:
    from rdkit import Chem

    RdkitMol: TypeAlias = Chem.rdchem.Mol | Chem.rdchem.RWMol
else:
    RdkitMol = Any


class MoleculeReadError(RuntimeError):
    """Error raised when molecule parsing fails."""


class VibrationalMode(Base):
    """
    Vibrational mode from frequency analysis.

    :param frequency: vibrational frequency, in cm⁻¹
    :param reduced_mass: reduced mass, in amu
    :param force_constant: force constant, in mDyne/Å
    :param displacements: atomic displacement vectors, in Å
    :param ir_intensity: infrared intensity, in km/mol
    :param symmetry_label: irreducible representation of mode, interpreted per Molecule.symmetry point group (e.g. "A1", "B2g", "E'")
    """

    frequency: Annotated[float, AfterValidator(round_float(3))]
    reduced_mass: Annotated[float, AfterValidator(round_float(3))]
    force_constant: Annotated[float, AfterValidator(round_float(3))]
    displacements: Annotated[Vector3DPerAtom, AfterValidator(round_vector3d_per_atom(6))]
    ir_intensity: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    symmetry_label: str | None = None


class Molecule(Base):
    """
    A molecular structure with associated properties.

    :param charge: total charge of the Molecule
    :param multiplicity: spin multiplicity of the Molecule
    :param atoms: Atom objects representing the atoms in the Molecule
    :param cell: PeriodicCell for periodic boundary conditions
    :param energy: targeted electronic energy (ground state if no target root), in Hartree
    :param scf_iterations: number of SCF iterations
    :param scf_completed: whether the SCF converged
    :param elapsed: time taken for the calculation, in seconds
    :param homo_lumo_gap: energy of the HOMO-LUMO gap, in eV
    :param gradient: energy gradient with respect to position, in Hartree/Å
    :param stress: stress matrix
    :param velocities: velocities of the atoms, in Å/fs
    :param mulliken_charges: Mulliken charges
    :param mulliken_spin_densities: Mulliken spin densities
    :param dipole: dipole moment, in Debye
    :param vibrational_modes: vibrations
    # https://docs.rowansci.com/science/quantum-chemistry/frequencies-and-thermochemistry
    :param zero_point_energy: zero-point energy, in Hartree
    :param thermal_energy_corr: ZPE + non-zero-temperature effects, in Hartree
    :param thermal_enthalpy_corr: thermal_energy_corr + pV, in Hartree
    :param thermal_free_energy_corr: thermal_enthalpy_corr - 298.15 x S, in Hartree
    :param excited_state_energies: absolute energies per root [root 0 (typically ground state), root 1, ...], in Hartree; meaningful only in multistate regime
    :param oscillator_strengths: transition strengths from ground state per root [root 0 (typically ground state), root 1, ...]; ground-to-ground defined as 0
    :param rotatory_strengths: signed velocity-gauge ECD rotatory strengths per root [root 0, root 1, ...], in 10⁻⁴⁰ esu²·cm²; ground-to-ground defined as 0
    :param cosmo_rs_data: COSMO-RS solvation free energy and its component breakdown
    :param symmetry: space group number (1–230) or point group symbol
    :param x_ray_diffraction_peaks: XRD reflections as (h, k, l, intensity in a.u.) tuples
    :param band_structure: electronic band structure and density of states (periodic systems only)
    :param elastic_tensor: elastic stiffness matrix in GPa, Voigt order xx yy zz yz xz xy
    :param smiles: SMILES corresponding to the Molecule
    :param calculation_index: index in a calculation output
    :param name: molecule's name
    :param metadata: any other associated data
    """

    charge: int
    multiplicity: PositiveInt
    atoms: list[Atom]

    cell: PeriodicCell | None = None

    energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    scf_iterations: NonNegativeInt | None = None
    scf_completed: bool | None = None
    elapsed: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    homo_lumo_gap: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    gradient: Annotated[Vector3DPerAtom | None, AfterValidator(round_optional_vector3d_per_atom(6))] = None
    stress: Annotated[Matrix3x3 | None, AfterValidator(round_optional_matrix3x3(6))] = None  # Hartree/Å

    velocities: Annotated[Vector3DPerAtom | None, AfterValidator(round_optional_vector3d_per_atom(6))] = None

    mulliken_charges: Annotated[FloatPerAtom | None, AfterValidator(round_optional_float_per_atom(6))] = None
    mulliken_spin_densities: Annotated[FloatPerAtom | None, AfterValidator(round_optional_float_per_atom(6))] = None
    dipole: Annotated[Vector3D | None, AfterValidator(round_optional_vector3d(6))] = None

    vibrational_modes: list[VibrationalMode] | None = None

    zero_point_energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    thermal_energy_corr: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    thermal_enthalpy_corr: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    thermal_free_energy_corr: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    excited_state_energies: Annotated[list[float] | None, AfterValidator(round_list(6))] = None
    oscillator_strengths: Annotated[list[float] | None, AfterValidator(round_list(3))] = None
    rotatory_strengths: Annotated[list[float] | None, AfterValidator(round_list(4))] = None

    cosmo_rs_data: COSMORSData | None = None

    symmetry: str | int | None = None

    x_ray_diffraction_peaks: Annotated[list[tuple[int, int, int, float]] | None, AfterValidator(round_xrd_peaks(3))] = None

    band_structure: BandStructure | None = None
    elastic_tensor: Annotated[Matrix6x6 | None, AfterValidator(round_optional_matrix6x6(3))] = None

    smiles: str | None = None
    calculation_index: int | None = None
    name: str | None = None
    metadata: dict[str, bool | float | int | str] | None = None

    def __len__(self) -> int:
        return len(self.atoms)

    def distance(self, i: PositiveInt, j: PositiveInt) -> float:
        r"""
        Calculate the distance between atoms, in Å.

        >>> mol = Molecule.from_xyz("H 0 1 0\nH 0 0 1")
        >>> mol.distance(1, 2)
        1.4142135623730951
        """
        return sum((q2 - q1) ** 2 for q1, q2 in zip(self.atoms[i - 1].position, self.atoms[j - 1].position, strict=True)) ** 0.5

    def angle(self, i: PositiveInt, j: PositiveInt, k: PositiveInt, degrees: bool = True) -> float:
        r"""
        Calculate the angle between three atoms.

        >>> Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1").angle(1, 2, 3)
        90.0
        """

        return angle(self.coordinates[i - 1], self.coordinates[j - 1], self.coordinates[k - 1], degrees=degrees)

    def dihedral(self, i: int, j: int, k: int, l: int, degrees: bool = True, positive_domain: bool = True) -> float:
        r"""
        Calculate the dihedral angle between four atoms.

        >>> Molecule.from_xyz("H 0 0 0\nO 0 0 1\nO 0 1 1\nH 1 1 1").dihedral(1, 2, 3, 4)
        270.0
        """
        return dihedral(
            self.coordinates[i - 1],
            self.coordinates[j - 1],
            self.coordinates[k - 1],
            self.coordinates[l - 1],
            degrees=degrees,
            positive_domain=positive_domain,
        )

    @property
    def coordinates(self) -> Vector3DPerAtom:
        """Cartesian coordinates of all atoms, in Å."""
        return [a.position for a in self.atoms]

    def translated(self, vector: Vector3D) -> Self:
        r"""
        Translate the molecule by a vector, in Å.

        >>> mol = Molecule.from_xyz("H 0 0 0\nH 0 0 1")
        >>> print(mol.translated((1, 0, 0)).to_xyz())
        2
        charge: 0; multiplicity: 1;
        H     1.0000000000    0.0000000000    0.0000000000
        H     1.0000000000    0.0000000000    1.0000000000
        """

        def translated(position: Vector3D) -> Vector3D:
            return tuple(q + v for q, v in zip(position, vector, strict=True))  # ty: ignore[invalid-return-type]

        atoms = [atom.model_copy(update={"position": translated(atom.position)}) for atom in self.atoms]

        return self.model_copy(update={"atoms": atoms})

    @property
    def atomic_numbers(self) -> list[NonNegativeInt]:
        """Atomic numbers of all atoms."""
        return [a.atomic_number for a in self.atoms]

    @pydantic.computed_field
    @property
    def pressure_gpa(self) -> float | None:
        r"""
        Hydrostatic pressure from stress tensor, in GPa.

        Computed as -trace(stress) / 3, converted from Hartree/Å³ to GPa.
        Returns None if stress is not set.

        >>> atoms = [Atom(atomic_number=1, position=(0, 0, 0)), Atom(atomic_number=1, position=(0, 0, 1))]
        >>> Molecule(charge=0, multiplicity=1, atoms=atoms).pressure_gpa is None
        True
        >>> stress = ((1e-4, 0, 0), (0, 1e-4, 0), (0, 0, 1e-4))
        >>> Molecule(charge=0, multiplicity=1, atoms=atoms, stress=stress).pressure_gpa
        -0.435974
        """
        if self.stress is None:
            return None
        trace = self.stress[0][0] + self.stress[1][1] + self.stress[2][2]
        return round(-trace / 3 * HARTREE_PER_CUBIC_ANGSTROM_TO_GPA, 6)

    @property
    def sum_energy_zpe(self) -> float | None:
        """Electronic energy plus zero-point energy, in Hartree."""
        if (self.energy is None) or (self.zero_point_energy is None):
            return None
        return self.energy + self.zero_point_energy

    @property
    def sum_energy_thermal_corr(self) -> float | None:
        """Electronic energy plus thermal energy correction, in Hartree."""
        if (self.energy is None) or (self.thermal_energy_corr is None):
            return None
        return self.energy + self.thermal_energy_corr

    @property
    def sum_energy_enthalpy(self) -> float | None:
        """Electronic energy plus enthalpy correction, in Hartree."""
        if (self.energy is None) or (self.thermal_enthalpy_corr is None):
            return None
        return self.energy + self.thermal_enthalpy_corr

    @property
    def enthalpy(self) -> float | None:
        """Alias for sum_energy_enthalpy, in Hartree."""
        return self.sum_energy_enthalpy

    @property
    def sum_energy_free_energy(self) -> float | None:
        """Electronic energy plus Gibbs free energy correction, in Hartree."""
        if (self.energy is None) or (self.thermal_free_energy_corr is None):
            return None
        return self.energy + self.thermal_free_energy_corr

    @property
    def gibbs_free_energy(self) -> float | None:
        """Alias for sum_energy_free_energy, in Hartree."""
        return self.sum_energy_free_energy

    @pydantic.model_validator(mode="after")
    def check_electron_sanity(self) -> Self:
        """Check that the charge and multiplicity combination is possible."""
        if self.cell is not None:
            # Periodic solids don't obey molecular electron-pairing rules
            return self

        num_electrons = sum(self.atomic_numbers) - self.charge
        num_unpaired_electrons = self.multiplicity - 1
        if (num_electrons - num_unpaired_electrons) % 2 != 0:
            raise ValueError(
                f"The combination of {num_electrons} electrons, charge {self.charge}, and multiplicity {self.multiplicity} is impossible. "
                "Double-check the charge and multiplicity values given and verify that they are correct."
            )

        return self

    @pydantic.model_validator(mode="after")
    def check_excited_state_consistency(self) -> Self:
        """Check that excited-state energies, oscillator strengths, and rotatory strengths describe the same roots."""
        if self.excited_state_energies is None:
            return self

        n_energies = len(self.excited_state_energies)
        for name, strengths in {"oscillator_strengths": self.oscillator_strengths, "rotatory_strengths": self.rotatory_strengths}.items():
            if strengths is not None and len(strengths) != n_energies:
                raise ValueError(f"excited_state_energies ({n_energies}) and {name} ({len(strengths)}) must have the same length.")

        return self

    @classmethod
    def from_file(cls: type[Self], filename: Path | str, format: str | None = None, charge: int | None = None, multiplicity: PositiveInt | None = None) -> Self:
        r"""
        Read a molecule from a file.

        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile("w+", suffix=".xyz") as f:
        ...    _ = f.write("2\nComment\nH 0 0 0\nF 0 0 1")
        ...    _ = f.seek(0)
        ...    mol = Molecule.from_file(f.name)
        >>> print(mol.to_xyz())
        2
        charge: 0; multiplicity: 1;
        H     0.0000000000    0.0000000000    0.0000000000
        F     0.0000000000    0.0000000000    1.0000000000
        """
        filename = Path(filename)
        if not format:
            format = filename.suffix[1:]

        match format:
            case "xyz":
                with open(filename) as f:
                    return cls.from_xyz_lines(f.readlines(), charge=charge, multiplicity=multiplicity)
            case "extxyz":
                with open(filename) as f:
                    return cls.from_extxyz_lines(f.readlines(), charge=charge, multiplicity=multiplicity)
            case "sdf" | "mol":
                return cls.molecules_from_sdf(filename)[0]
            case "mol2":
                return cls.molecules_from_mol2(filename)[0]
            case _:
                raise ValueError(f"Unsupported {format=}")

    @classmethod
    def from_xyz(cls: type[Self], xyz: str, charge: int | None = None, multiplicity: PositiveInt | None = None) -> Self:
        r"""
        Generate a Molecule from an XYZ string.

        Note: only supports single molecule inputs.

        >>> len(Molecule.from_xyz("2\nComment\nH 0 0 0\nH 0 0 1"))
        2
        """
        return cls.from_xyz_lines(xyz.strip().splitlines(), charge=charge, multiplicity=multiplicity)

    @classmethod
    def from_xyz_lines(cls: type[Self], lines: Iterable[str], charge: int | None = None, multiplicity: PositiveInt | None = None) -> Self:
        r"""
        Read a molecule from a xyz lines.

        >>> mol = Molecule.from_xyz_lines(["2", "charge: 0; multiplicity: 1; cell: [[1, 2e1, 3], [4, 5, 6], [7, 8, 9.1]]", "H 0 0 0", "F 0 0 1"])
        >>> print(mol.to_xyz())
        2
        charge: 0; multiplicity: 1; cell: ((1.0, 20.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.1)); is_periodic: (True, True, True);
        H     0.0000000000    0.0000000000    0.0000000000
        F     0.0000000000    0.0000000000    1.0000000000
        >>> mol = Molecule.from_xyz_lines(["2", "energy: abc", "H 0 0 0", "F 0 0 1"])
        >>> print(mol.to_xyz())
        2
        charge: 0; multiplicity: 1;
        H     0.0000000000    0.0000000000    0.0000000000
        F     0.0000000000    0.0000000000    1.0000000000
        """
        lines = list(lines)
        data: dict[str, Any] = {}
        if len(lines[0].split()) == 1:
            natoms, comment, *lines = lines
            if (not natoms.strip().isdigit()) or (int(natoms) != len(lines)):
                raise MoleculeReadError(f"First line of XYZ file should be the number of atoms ({len(lines)}), got: {natoms}")

            data = cls._parse_comment_line(comment)

        charge = charge if charge is not None else data.get("charge", 0)
        multiplicity = multiplicity or data.get("multiplicity", 1)
        data |= {"charge": charge, "multiplicity": multiplicity}

        try:
            return cls(atoms=[Atom.from_xyz(line) for line in lines], **data)
        except (ValueError, ValidationError):
            pass

        try:
            return cls(atoms=[Atom.from_xyz(line) for line in lines], charge=charge, multiplicity=multiplicity)
        except (ValueError, ValidationError) as e:
            raise MoleculeReadError("Error reading molecule from xyz") from e

    @classmethod
    def _parse_comment_line(cls, comment: str) -> dict[str, Any]:
        """
        Parse the comment line of an XYZ file.

        :param comment: comment line from an XYZ file

        >>> Molecule._parse_comment_line("charge: -1; multiplicity: 2; cell: [[1,2,3],[4,5,6],[7,8,9]]; is_periodic: (True, False, True); energy: -75.0")
        {'charge': '-1', 'multiplicity': '2', 'energy': '-75.0', 'cell':\
        PeriodicCell(lattice_vectors=((1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)), is_periodic=(True, False, True))}
        >>> Molecule._parse_comment_line(" energy: -0.320207535977 gnorm: 0.071552110436 xtb: 6.6.1 (8d0f1dd)")  # Unfortunate
        {'energy': '-0.320207535977 gnorm: 0.071552110436 xtb: 6.6.1 (8d0f1dd)'}
        >>> Molecule._parse_comment_line('charge: 0; key: value; smiles: CC;')
        {'charge': '0', 'smiles': 'CC', 'metadata': {'key': 'value'}}
        """
        data: dict[str, Any] = {}
        for kv in comment.strip(";").split(";"):
            try:
                key, value = kv.split(":", 1)
                data[key.strip()] = value.strip()
            except ValueError:
                logger.error(f"Error parsing key/value: {kv}")
                continue

        if cell := data.pop("cell", None):
            try:
                data["cell"] = PeriodicCell.from_string(cell)
                if is_periodic := data.pop("is_periodic", None):
                    x, y, z = is_periodic.strip(" ([)]").split(",")
                    true_values = {"true", "1", "yes"}
                    data["cell"].is_periodic = tuple((v.strip().lower() in true_values) for v in (x, y, z))  # ty: ignore[invalid-assignment]
            except ValueError as e:
                logger.error(f"Error parsing XYZ cell: {e}")

        known_keys = set(cls.model_fields.keys()) - {"atoms", "metadata"}
        metadata: dict[str, bool | float | int | str] = {}
        for key in list(data.keys()):
            if key not in known_keys:
                metadata[key] = _coerce_metadata_value(data.pop(key))
        if metadata:
            data["metadata"] = metadata

        return data

    def to_xyz(self, comment: str | None = None, out_file: Path | str | None = None) -> str:
        r"""
        Generate an XYZ string.

        :param comment: optional comment line (defaults to standard Rowan XYZ comment line format)
        :param out_file: optional output file path to write the XYZ string to
        :return: XYZ string

        >>> mol = Molecule.from_xyz("2\nenergy: 1.0; smiles: HF;\nH 0 1 2\nF 1 2 3")
        >>> print(mol.to_xyz())
        2
        charge: 0; multiplicity: 1; energy: 1.0; smiles: HF;
        H     0.0000000000    1.0000000000    2.0000000000
        F     1.0000000000    2.0000000000    3.0000000000
        >>> mol2 = Molecule.from_xyz('2\ncharge: 0; multiplicity: 1; key: value; smiles: HF;\nH 0 1 2\nF 1 2 3')
        >>> mol2.metadata
        {'key': 'value'}
        >>> mol2.smiles
        'HF'
        >>> 'key: value;' in mol2.to_xyz()
        True
        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as directory:
        ...     file = Path(directory) / "mol.xyz"
        ...     out = mol.to_xyz(out_file=file)
        ...     with file.open() as f:
        ...         Molecule.from_xyz(f.read()).to_xyz() == out
        True
        """
        geom = "\n".join(map(str, self.atoms))
        if comment is None:
            data = self.model_dump(exclude_none=True, exclude={"atoms"})

            if cell := data.pop("cell", None):
                data["cell"] = cell["lattice_vectors"]
                data["is_periodic"] = cell["is_periodic"]

            if metadata := data.pop("metadata", None):
                for k, v in metadata.items():
                    data[k] = str(v).lower() if isinstance(v, bool) else v

            comment = " ".join(f"{key}: {value};" for key, value in data.items())

        out = f"{len(self)}\n{comment}\n{geom}"

        if out_file:
            with Path(out_file).open("w") as f:
                f.write(out)

        return out

    @classmethod
    def from_extxyz(cls: type[Self], extxyz: str, charge: int = 0, multiplicity: PositiveInt = 1) -> Self:
        r"""
        Generate a Molecule from a EXTXYZ string. Currently only supporting Lattice and Properties fields.

        >>> Molecule.from_extxyz('''
        ... 2
        ... Lattice="6.0 0.0 0.0 6.0 0.0 0.0 6.0 0.0 0.0"Properties=species:S:1:pos:R:3
        ... H 0 0 0
        ... H 0 0 1
        ... ''').cell.lattice_vectors
        ((6.0, 0.0, 0.0), (6.0, 0.0, 0.0), (6.0, 0.0, 0.0))
        """

        return cls.from_extxyz_lines(extxyz.strip().splitlines(), charge=charge, multiplicity=multiplicity)

    @classmethod
    def from_extxyz_lines(
        cls: type[Self],
        lines: Iterable[str],
        charge: int | None = None,
        multiplicity: PositiveInt | None = None,
        cell: PeriodicCell | None = None,
    ) -> Self:
        """
        Parses an EXTXYZ file, extracting atom positions, forces (if present), and metadata.

        Supports:
        - Lattice vectors (cell information)
        - Properties field (species, positions, forces, etc.)
        - Other metadata like charge, multiplicity, energy, etc.

        :param lines: Iterable of lines from an EXTXYZ file
        :param charge: total charge of the molecule (default: 0 if not found)
        :param multiplicity: spin multiplicity of the molecule (default: 1 if not found)
        :param cell: PeriodicCell containing lattice vectors
        :return: Molecule
        :raises MoleculeReadError: if the file is not in the correct format
        """
        lines_list: list[str] = list(lines)

        # Ensure first line contains number of atoms
        if len(lines_list[0].split()) == 1:
            natoms = lines_list[0].strip()
            if not natoms.isdigit() or (int(natoms) != len(lines_list) - 2):
                raise MoleculeReadError(f"First line should be number of atoms, got: {lines_list[0]} != {len(lines_list) - 2}")
            data_line, *lines_list = lines_list[1:]
        else:
            raise MoleculeReadError(f"First line should be an integer denoting atom count. Got {lines_list[0].split()}")

        metadata = parse_extxyz_comment_line(data_line)

        T = TypeVar("T")

        def metadata_optional_get(key: str, value: T | None, default: T) -> T:
            """Set key to default if not found in metadata"""
            if value is None:
                return metadata.get(key, default)

            return value

        charge = metadata_optional_get("total_charge", charge, 0)
        multiplicity = metadata_optional_get("multiplicity", multiplicity, 1)
        cell = cell or metadata.get("cell")
        energy = metadata.get("energy", None)

        force_idx = None
        if properties := metadata.get("properties", "").split(":"):
            if properties[0].lower() != "species":
                raise MoleculeReadError(f"Invalid or missing 'Properties' field in EXTXYZ, got: {properties}")

            # Identify column indices for position and force data
            pos_idx = None
            current_idx = 0  # Start after 'species:S'

            while current_idx < len(properties):
                if properties[current_idx].lower() == "pos" and properties[current_idx + 1].lower() == "r" and properties[current_idx + 2] == "3":
                    pos_idx = current_idx
                elif properties[current_idx].lower() == "forces" and properties[current_idx + 1].lower() == "r" and properties[current_idx + 2] == "3":
                    force_idx = current_idx
                current_idx += 3

            if pos_idx is None:
                raise MoleculeReadError("No position data ('pos:R:3') found in Properties field.")

        def parse_line_atoms(line: str) -> Atom:
            symbol, sx, sy, sz, *_ = line.split()
            atomic_number = SYMBOL_ELEMENT[symbol.title()]
            x, y, z = map(float, (sx, sy, sz))

            return Atom(atomic_number=atomic_number, position=(x, y, z))

        def parse_line_with_grad(line: str) -> tuple[Atom, Vector3D]:
            symbol, sx, sy, sz, sgx, sgy, sgz, *_ = line.split()
            atomic_number = SYMBOL_ELEMENT[symbol.title()]
            x, y, z = map(float, (sx, sy, sz))
            gx, gy, gz = map(float, (sgx, sgy, sgz))

            return (
                Atom(atomic_number=atomic_number, position=(x, y, z)),
                (-gx, -gy, -gz),
            )

        atoms: list[Atom]
        gradients: list[Vector3D] | None
        if force_idx is not None:
            atoms, gradients = zip(*map(parse_line_with_grad, lines_list), strict=True)  # ty: ignore[invalid-assignment]
        else:
            atoms = [parse_line_atoms(line) for line in lines_list]
            gradients = None

        return cls(atoms=atoms, cell=cell, charge=charge, multiplicity=multiplicity, energy=energy, gradient=gradients)

    @classmethod
    def from_rdkit(cls: type[Self], rdkm: RdkitMol, cid: int = 0, multiplicity: int = 1) -> Self:
        """
        Build a Molecule from an RDKit molecule.

        Uses the ``smiles`` property if set; otherwise computes one from the bond
        graph when the mol carries real bond orders. Leaves smiles unset when
        the mol has no bonds (e.g., XYZ-derived without DetermineBonds).

        :param rdkm: RDKit molecule
        :param cid: conformer id to read coordinates from
        :param multiplicity: spin multiplicity
        :return: Molecule
        """
        from rdkit import Chem  # noqa: PLC0415

        if len(rdkm.GetConformers()) == 0:
            rdkm = _embed_rdkit_mol(rdkm)

        atomic_numbers = [atom.GetAtomicNum() for atom in rdkm.GetAtoms()]
        atoms = [
            Atom(atomic_number=atom, position=xyz)  # keep open
            for atom, xyz in zip(atomic_numbers, rdkm.GetConformers()[cid].GetPositions(), strict=True)
        ]

        charge = Chem.GetFormalCharge(rdkm)

        smiles: str | None = None
        if rdkm.HasProp("smiles"):
            smiles = rdkm.GetProp("smiles").strip() or None
        if smiles is None and _has_serializable_topology(rdkm):
            try:
                smiles = Chem.MolToSmiles(rdkm)
            except ValueError as e:
                logger.warning(f"Could not generate SMILES from RDKit molecule, leaving unset: {e}")

        name = rdkm.GetProp("_Name").strip() if rdkm.HasProp("_Name") else None
        props = rdkm.GetPropsAsDict(includePrivate=False, includeComputed=False, autoConvertStrings=True)
        metadata: dict[str, str | float | int | bool] = {}
        for key, value in props.items():
            if isinstance(value, bool | str | int | float):
                metadata[key] = value

        return cls(atoms=atoms, charge=charge, multiplicity=multiplicity, smiles=smiles, name=name or None, metadata=metadata or None)

    @classmethod
    def from_smiles(cls: type[Self], smiles: str) -> Self:
        from rdkit import Chem  # noqa: PLC0415

        rdkm = Chem.MolFromSmiles(smiles)
        assert rdkm is not None
        return cls.from_rdkit(rdkm)

    @classmethod
    def molecules_from_sdf(cls: type[Self], path: Path | str) -> list[Self]:
        """
        Read multiple molecules from an SDF file.

        :param path: Path to the SDF file.
        :returns: List of Molecule instances, one per record.
        :raises ValueError: If no valid molecules are found in the file.

        Example::

            mols = Molecule.molecules_from_sdf("ligands.sdf")
        """
        from rdkit import Chem  # noqa: PLC0415

        supplier = Chem.SDMolSupplier(str(path), removeHs=False)
        mols = [cls.from_rdkit(rdkm) for rdkm in supplier if rdkm is not None]
        if not mols:
            raise ValueError(f"No valid molecules found in {path}")
        return mols

    @classmethod
    def molecules_from_mol2(cls: type[Self], path: Path | str) -> list[Self]:
        """
        Read multiple molecules from a MOL2 file.

        :param path: Path to the MOL2 file.
        :returns: List of Molecule instances, one per record.
        :raises ValueError: If no valid molecules are found in the file.

        Example::

            mols = Molecule.molecules_from_mol2("ligands.mol2")
        """
        from rdkit import Chem  # noqa: PLC0415

        text = Path(path).read_text()
        blocks = [b for b in text.split("@<TRIPOS>MOLECULE") if b.strip()]
        mols = []
        for block in blocks:
            rdkm = Chem.MolFromMol2Block("@<TRIPOS>MOLECULE" + block, removeHs=False)
            if rdkm is not None:
                mols.append(cls.from_rdkit(rdkm))
        if not mols:
            raise ValueError(f"No valid molecules found in {path}")
        return mols


def _has_serializable_topology(rdkm: RdkitMol) -> bool:
    """Return True when the mol has a usable bond graph for ``Chem.MolToSmiles``.

    Single atoms are accepted. Multi-atom mols need at least one bond and every
    bond must have a real order (not UNSPECIFIED or ZERO).
    """
    from rdkit import Chem  # noqa: PLC0415

    if rdkm.GetNumAtoms() <= 1:
        return True
    if rdkm.GetNumBonds() == 0:
        return False
    bad = {Chem.BondType.UNSPECIFIED, Chem.BondType.ZERO}
    return all(b.GetBondType() not in bad for b in rdkm.GetBonds())


def _embed_rdkit_mol(rdkm: RdkitMol) -> RdkitMol:
    from rdkit.Chem import AllChem  # noqa: PLC0415

    try:
        AllChem.SanitizeMol(rdkm)  # ty: ignore[unresolved-attribute]
    except Exception as e:
        raise ValueError("Molecule could not be generated -- invalid chemistry!\n") from e

    rdkm = AllChem.AddHs(rdkm)  # ty: ignore[unresolved-attribute]
    try:
        status1 = AllChem.EmbedMolecule(rdkm, maxAttempts=200)  # ty: ignore[unresolved-attribute]
        assert status1 >= 0
    except Exception as e:
        status1 = AllChem.EmbedMolecule(rdkm, maxAttempts=200, useRandomCoords=True)  # ty: ignore[unresolved-attribute]
        if status1 < 0:
            raise ValueError(f"Cannot embed molecule! Error: {e}") from e

    AllChem.MMFFOptimizeMolecule(rdkm, maxIters=200)  # ty: ignore[unresolved-attribute]

    return rdkm


class EXTXYZMetadata(TypedDict, total=False):
    """Metadata from EXTXYZ file comment line."""

    properties: Any
    total_charge: int
    multiplicity: int
    energy: float
    cell: PeriodicCell


def parse_extxyz_comment_line(line: str) -> EXTXYZMetadata:
    """
    Parse the comment line of an EXTXYZ file, extracting lattice, properties, and metadata.

    Supports:
    - Lattice vectors (cell information)
    - Properties field (species, positions, forces, etc.)
    - Other metadata fields like charge, multiplicity, energy, etc.

    :param line: comment line from an EXTXYZ file
    :return: parsed properties

    >>> parse_extxyz_comment_line('Lattice="6.0 0.0 0.0 6.0 0.0 0.0 6.0 0.0 0.0"Properties=species:S:1:pos:R:3')
    {'cell': PeriodicCell(lattice_vectors=((6.0, 0.0, 0.0), (6.0, 0.0, 0.0), (6.0, 0.0, 0.0)), is_periodic=(True, True, True)), 'properties': 'species:S:1:pos:R:3'}
    """  # noqa: E501

    # Regular expression to match key="value", key='value', or key=value
    pattern = r"(\S+?=(?:\".*?\"|\'.*?\'|\S+))"
    pairs = re.findall(pattern, line)

    prop_dict: EXTXYZMetadata = {}
    for pair in pairs:
        key, value = pair.split("=", 1)
        key = key.lower().strip()
        value = value.strip("'\"")

        if key == "lattice":
            lattice_values = value.split()
            if len(lattice_values) != 9:
                raise MoleculeReadError(f"Lattice should have 9 entries, got {len(lattice_values)}")

            try:
                cell = tuple(tuple(map(float, lattice_values[i : i + 3])) for i in range(0, 9, 3))
            except ValueError as e:
                raise MoleculeReadError(f"Lattice should be floats, got {lattice_values}") from e

            prop_dict["cell"] = PeriodicCell(lattice_vectors=cell)

        elif key == "properties":
            prop_dict["properties"] = value

        elif key == "total_charge":
            prop_dict["total_charge"] = int(value)
        elif key == "multiplicity":
            prop_dict["multiplicity"] = int(value)
        elif key == "energy":
            prop_dict["energy"] = float(value)
        else:
            prop_dict[key] = value  # ty: ignore[invalid-assignment]

    return prop_dict


def angle(p0: Sequence[float], p1: Sequence[float], p2: Sequence[float], degrees: bool = True) -> float:
    """
    Angle between three points.

    :param p0: position of first point
    :param p1: position of vertex point
    :param p2: position of third point
    :param degrees: whether to return in degrees
    :return: angle in radians or degrees
    """
    a0, a1, a2 = (np.asarray(p, dtype=float) for p in (p0, p1, p2))
    u = a1 - a0
    v = a1 - a2

    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    cos_theta = np.dot(u, v) / (nu * nv)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    ang = np.arccos(cos_theta)
    if degrees:
        return float(np.degrees(ang))
    return float(ang)


def dihedral(p0: Sequence[float], p1: Sequence[float], p2: Sequence[float], p3: Sequence[float], degrees: bool = True, positive_domain: bool = True) -> float:
    """
    Dihedral angle between four points.

    :param p0, p1, p2, p3: points
    :param degrees: whether to return in degrees
    :param positive_domain: (0, 360] if True else (-180, 180]
    :return: angle in degrees or radians (or nan if collinearities detected)

    >>> a = [0, 0, 0]
    >>> b = [0, 0, 1]
    >>> c = [0, 1, 1]
    >>> d1 = [0, 1, 2]
    >>> d2 = [0.5, 1, 1.5]
    >>> dihedral(a, b, c, d1)
    180.0
    >>> dihedral(a, b, c, d2, positive_domain=False)
    -135.0
    """
    a0, a1, a2, a3 = (np.asarray(p, dtype=float) for p in (p0, p1, p2, p3))
    b0 = a1 - a0
    b1 = a2 - a1
    b2 = a3 - a2

    b1 = b1 / np.linalg.norm(b1)

    v = b1 * np.dot(b0, b1) - b0
    w = b2 - b1 * np.dot(b2, b1)

    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    ang = np.arctan2(y, x)

    if positive_domain and ang < 0:
        ang += 2 * np.pi

    if degrees:
        return float(np.degrees(ang))
    return float(ang)
