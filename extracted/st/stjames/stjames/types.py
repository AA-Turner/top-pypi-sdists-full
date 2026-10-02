from typing import Annotated, Callable, Iterable, Protocol, TypeAlias, overload

from pydantic import AfterValidator, NonNegativeInt

from .base import Base
from .residue_constants import ION_RESIDUES, WATER_RESIDUES

UUID: TypeAlias = str
ProteinUUID: TypeAlias = UUID


def validate_non_polymer_residue_mapping(
    residues: dict[str | NonNegativeInt, str | None],
) -> dict[str | NonNegativeInt, str | None]:
    """
    Validate residue selectors and parameterization inputs for non-polymers.

    :param residues: mapping from residue name or 0-based non-polymer index to
        SMILES, or `None` for known ions and waters
    :return: validated mapping
    :raises ValueError: if a SMILES value is empty
    :raises ValueError: if an unknown residue maps to `None`
    """
    for key, smiles in residues.items():
        if smiles == "":
            raise ValueError(f"non-polymer residue entry {key!r} has an empty SMILES string")
        if smiles is None and not (isinstance(key, str) and key.upper() in ION_RESIDUES | WATER_RESIDUES):
            raise ValueError(f"non-polymer residue entry {key!r} is not a known ion/water residue and requires a SMILES string")
    return residues


NonPolymerResidueMapping: TypeAlias = Annotated[
    dict[str | NonNegativeInt, str | None],
    AfterValidator(validate_non_polymer_residue_mapping),
]


class _Iterable_Rounder(Protocol):
    """Callable with return types conditioned on the input type(s)."""

    @overload
    def __call__(self, values: None, /) -> None: ...
    @overload
    def __call__(self, values: Iterable[float], /) -> list[float]: ...
    @overload
    def __call__(self, values: Iterable[float | None], /) -> list[float | None]: ...


def round_list(round_to: int = 6) -> _Iterable_Rounder:
    """Round values (even if Nones), preserving types."""

    @overload
    def rounder(values: None, /) -> None: ...
    @overload
    def rounder(values: Iterable[float], /) -> list[float]: ...
    @overload
    def rounder(values: Iterable[float | None], /) -> list[float | None]: ...

    def rounder(values: Iterable[float] | Iterable[float | None] | None, /) -> list[float] | list[float | None] | None:
        if values is None:
            return None

        return [round(v, round_to) if v is not None else None for v in values]

    return rounder


class SimpleProteinMDTrajectory(Base):
    """
    Minimal reference to a molecular dynamics trajectory stored in S3.

    :param uuid: UUID of the DCD trajectory file in S3 storage
    """

    uuid: UUID


class ProteinMDTrajectory(SimpleProteinMDTrajectory):
    """
    Reference to a molecular dynamics trajectory stored in S3, with full analysis results.

    The trajectory is stored as a DCD file containing atomic coordinates
    across multiple frames. The corresponding topology (atom names, residues,
    connectivity) comes from the protein PDB associated with the workflow.

    Inherited:
    :param uuid: UUID of the DCD trajectory file in S3 storage

    New:
    :param cluster_centroid_indices: indices of frames corresponding to cluster centroids
    :param cluster_indices_by_frame: cluster that each frame belongs to
    :param isotropic_radius_of_gyration: per-frame protein Rg (all polymer chains; excludes
        small molecules, waters, and solvent ions), in Å
    :param sasa: per-frame total solvent-accessible surface area of all polymer chains
        (excludes small molecules, waters, and solvent ions), in Å²; length n_frames; None at
        unsampled frames, float at strided frames; empty if analysis not requested
    :param polar_sasa: per-frame polar (non-H, non-C) solvent-accessible surface area of
        all polymer chains (excludes small molecules, waters, and solvent ions), in Å²; length
        n_frames; None at unsampled frames, float at strided frames; empty if analysis not requested
    :param protein_rmsd: per-frame Cα RMSD vs frame 0, computed with an internal Kabsch
        alignment on all protein Cα (receptor + any protein binder chains), in Å
    :param rmsf: per-Cα RMSF relative to mean structure across all protein Cα
        (receptor + any protein binder chains), in Å; length = number of protein Cα
    :param potential_energy: per-frame potential energy of the whole simulated system
        (includes solvent), in Hartree
    :param mean_structure_uuid: UUID of saved PDB for coordinate-averaged (mean) structure
    :param median_structure_frame_index: index of medoid frame (minimum total RMSD to all other frames)
    """

    cluster_centroid_indices: list[int] = []
    cluster_indices_by_frame: list[int] = []
    isotropic_radius_of_gyration: Annotated[list[float], AfterValidator(round_list(3))] = []
    sasa: Annotated[list[float | None], AfterValidator(round_list(3))] = []
    polar_sasa: Annotated[list[float | None], AfterValidator(round_list(3))] = []
    protein_rmsd: Annotated[list[float], AfterValidator(round_list(3))] = []
    rmsf: Annotated[list[float], AfterValidator(round_list(3))] = []
    potential_energy: Annotated[list[float], AfterValidator(round_list(6))] = []
    mean_structure_uuid: UUID | None = None
    median_structure_frame_index: NonNegativeInt | None = None


Vector3D: TypeAlias = tuple[float, float, float]
Vector3DPerAtom: TypeAlias = list[Vector3D]

FloatPerAtom: TypeAlias = list[float]

Matrix3x3: TypeAlias = tuple[Vector3D, Vector3D, Vector3D]
Matrix6x6: TypeAlias = tuple[
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
]


def round_vector3d(round_to: int = 6) -> Callable[[Vector3D], Vector3D]:
    """Create a validator that rounds each component of a Vector3D to a given number of decimal places."""

    def rounder(vector: Vector3D) -> Vector3D:
        return (round(vector[0], round_to), round(vector[1], round_to), round(vector[2], round_to))

    return rounder


def round_optional_vector3d(round_to: int = 6) -> Callable[[Vector3D | None], Vector3D | None]:
    """Create a validator that rounds each component of a Vector3D to a given number of decimal places, handling None."""

    def rounder(vector: Vector3D | None) -> Vector3D | None:
        if vector is None:
            return None
        return (round(vector[0], round_to), round(vector[1], round_to), round(vector[2], round_to))

    return rounder


def round_vector3d_per_atom(round_to: int = 6) -> Callable[[Vector3DPerAtom], Vector3DPerAtom]:
    """Create a validator that rounds each vector in Vector3DPerAtom to a given number of decimal places."""
    vector_rounder = round_vector3d(round_to)

    def rounder(vectors: Vector3DPerAtom) -> Vector3DPerAtom:
        return [vector_rounder(v) for v in vectors]

    return rounder


def round_optional_vector3d_per_atom(round_to: int = 6) -> Callable[[Vector3DPerAtom | None], Vector3DPerAtom | None]:
    """Create a validator that rounds each vector in Vector3DPerAtom to a given number of decimal places, handling None."""
    vector_rounder = round_vector3d(round_to)

    def rounder(vectors: Vector3DPerAtom | None) -> Vector3DPerAtom | None:
        if vectors is None:
            return None
        return [vector_rounder(v) for v in vectors]

    return rounder


def round_matrix3x3(round_to: int = 6) -> Callable[[Matrix3x3], Matrix3x3]:
    """Create a validator that rounds each vector in a Matrix3x3 to a given number of decimal places."""

    # Use the round_vector3d function to round each Vector3D in the Matrix3x3
    vector_rounder = round_vector3d(round_to)

    def rounder(matrix: Matrix3x3) -> Matrix3x3:
        return (vector_rounder(matrix[0]), vector_rounder(matrix[1]), vector_rounder(matrix[2]))

    return rounder


def round_optional_matrix3x3(round_to: int = 3) -> Callable[[Matrix3x3 | None], Matrix3x3 | None]:
    """Create a validator that rounds each vector in an optional Matrix3x3 to a given number of decimal places."""

    # Use the round_vector3d function to round each Vector3D in the Matrix3x3
    vector_rounder = round_vector3d(round_to)

    def rounder(matrix: Matrix3x3 | None) -> Matrix3x3 | None:
        if matrix is None:
            return None
        return (vector_rounder(matrix[0]), vector_rounder(matrix[1]), vector_rounder(matrix[2]))

    return rounder


def round_matrix6x6(round_to: int = 6) -> Callable[[Matrix6x6], Matrix6x6]:
    """Create a validator that rounds each component of a Matrix6x6."""

    def round_row(
        row: tuple[float, float, float, float, float, float],
    ) -> tuple[float, float, float, float, float, float]:
        return (
            round(row[0], round_to),
            round(row[1], round_to),
            round(row[2], round_to),
            round(row[3], round_to),
            round(row[4], round_to),
            round(row[5], round_to),
        )

    def rounder(matrix: Matrix6x6) -> Matrix6x6:
        return (
            round_row(matrix[0]),
            round_row(matrix[1]),
            round_row(matrix[2]),
            round_row(matrix[3]),
            round_row(matrix[4]),
            round_row(matrix[5]),
        )

    return rounder


def round_optional_matrix6x6(round_to: int = 3) -> Callable[[Matrix6x6 | None], Matrix6x6 | None]:
    """Create a validator that rounds each component of an optional Matrix6x6."""
    matrix_rounder = round_matrix6x6(round_to)

    def rounder(matrix: Matrix6x6 | None) -> Matrix6x6 | None:
        if matrix is None:
            return None
        return matrix_rounder(matrix)

    return rounder


def round_optional_float_per_atom(round_to: int = 6) -> Callable[[FloatPerAtom | None], FloatPerAtom | None]:
    """Create a validator that rounds each float in FloatPerAtom to a given number of decimal places, handling None."""

    def rounder(values: FloatPerAtom | None) -> FloatPerAtom | None:
        if values is None:
            return None
        return [round(value, round_to) for value in values]

    return rounder


def round_float_per_atom(round_to: int = 6) -> Callable[[FloatPerAtom], FloatPerAtom]:
    """Create a validator that rounds each float in FloatPerAtom to a given number of decimal places, handling None."""

    def rounder(values: FloatPerAtom) -> FloatPerAtom:
        return [round(value, round_to) for value in values]

    return rounder


def round_xrd_peaks(round_to: int = 6) -> Callable[[list[tuple[int, int, int, float]] | None], list[tuple[int, int, int, float]] | None]:
    """Create a validator that rounds the intensity of each (h, k, l, intensity) XRD peak, handling None."""

    def rounder(values: list[tuple[int, int, int, float]] | None) -> list[tuple[int, int, int, float]] | None:
        if values is None:
            return None
        return [(h, k, l, round(intensity, round_to)) for h, k, l, intensity in values]

    return rounder


def round_list_of_str_float_pairs(round_to: int = 6) -> Callable[[list[tuple[str, float]]], list[tuple[str, float]]]:
    """Create a validator that rounds the float component of each (str, float) pair in a list."""

    def rounder(values: list[tuple[str, float]]) -> list[tuple[str, float]]:
        return [(s, round(f, round_to)) for s, f in values]

    return rounder


def round_list_of_float_pairs(round_to: int = 6) -> Callable[[list[tuple[float, float]]], list[tuple[float, float]]]:
    """Create a validator that rounds both floats in each (float, float) pair in a list."""

    def rounder(values: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return [(round(a, round_to), round(b, round_to)) for a, b in values]

    return rounder


def round_list_of_lists(round_to: int = 6) -> Callable[[list[list[float]]], list[list[float]]]:
    """Create a validator that rounds each float in FloatPerAtom to a given number of decimal places, handling None."""

    list_rounder = round_list(round_to)

    def rounder(values: list[list[float]]) -> list[list[float]]:
        return [list_rounder(value) for value in values]

    return rounder
