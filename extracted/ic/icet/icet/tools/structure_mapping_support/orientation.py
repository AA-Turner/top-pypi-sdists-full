"""
Orientation relationships between a structure and a reference structure.

The rotation relating two cells of the same crystal is only defined up to a
symmetry operation of that crystal, since applying such an operation to one of
them gives an equally valid description. The functions here reduce a rotation to
the smallest angle among those descriptions, which is the quantity that can be
compared between structures.
"""

import numpy as np
import spglib
from ase import Atoms
from scipy.spatial.transform import Rotation

from icet.tools.geometry import ase_atoms_to_spglib_cell, call_spglib

DISORIENTATION_TIE_TOLERANCE = 1e-9
"""Angles in radians that differ by less than this are treated as equal when a rotation is
reduced over the symmetry operations."""


def get_symmetry_rotations(reference: Atoms, symprec: float = 1e-5) -> np.ndarray:
    """Returns the rotations of a structure in reduced coordinates.

    These are the integer matrices that :program:`spglib` reports, which act on reduced
    coordinates. They are what is needed when comparing transformation matrices, whereas
    :func:`get_point_group_operations` gives the corresponding Cartesian operations.

    Parameters
    ----------
    reference
        Structure whose symmetry is analyzed.
    symprec
        Tolerance passed to :program:`spglib`.

    Returns
    -------
        Array of shape ``(N, 3, 3)`` of integer matrices. The identity is returned on its
        own if the symmetry analysis fails.
    """
    try:
        symmetry = call_spglib(spglib.get_symmetry, ase_atoms_to_spglib_cell(reference),
                               symprec=symprec)
    except ValueError:
        return np.eye(3, dtype=int)[None, :, :]
    return np.rint(symmetry['rotations']).astype(int)


def get_point_group_operations(reference: Atoms, symprec: float = 1e-5) -> np.ndarray:
    """Returns the proper rotations of a structure in Cartesian coordinates.

    Improper operations are left out, since they cannot relate two cells of the same
    handedness.

    Parameters
    ----------
    reference
        Structure whose symmetry is analyzed.
    symprec
        Tolerance passed to :program:`spglib`.

    Returns
    -------
        Array of shape ``(N, 3, 3)`` holding the operations. It contains at least the
        identity, which is returned on its own if the symmetry analysis fails.
    """
    rotations = get_symmetry_rotations(reference, symprec)
    cell = np.asarray(reference.cell, dtype=np.float64)
    # an operation W acting on reduced coordinates corresponds to A^T W A^-T in
    # Cartesian coordinates, for a cell A whose rows are the cell vectors
    operations = [cell.T @ rotation @ np.linalg.inv(cell.T) for rotation in rotations]
    operations = [operation for operation in operations
                  if np.linalg.det(operation) > 0]
    if not operations:
        return np.eye(3)[None, :, :]
    return np.array(operations)


def calculate_disorientation(rotation: np.ndarray,
                             operations: np.ndarray) -> tuple[float, np.ndarray]:
    """Returns the angle in degrees and the axis of the smallest rotation among those
    that are equivalent to the given one under the given symmetry operations.

    A rotation relating a structure to a reference structure can be composed with any
    symmetry operation of the reference structure without changing what it describes,
    so only the smallest of the resulting rotations is meaningful. That rotation is known
    as the disorientation. The angle and the axis are taken from one and the same of the
    equivalent descriptions, so that together they reproduce it.

    The axis vanishes if the angle does, since a vanishing rotation has no axis. Should
    several descriptions share the smallest angle, which happens when the misorientation
    lies on a symmetry element, the axis is picked among them in a reproducible way.

    Parameters
    ----------
    rotation
        Rotation to reduce, a proper orthogonal matrix.
    operations
        Symmetry operations to reduce it over, as returned by
        :func:`get_point_group_operations`.

    Raises
    ------
    ValueError
        If the rotation is not a 3x3 matrix.
    """
    rotation = np.asarray(rotation, dtype=np.float64)
    if rotation.shape != (3, 3):
        raise ValueError('The rotation is not a 3x3 matrix, its shape is {}.'.format(
            rotation.shape))

    equivalents = [Rotation.from_matrix(rotation @ operation) for operation in operations]
    angles = np.array([equivalent.magnitude() for equivalent in equivalents])
    smallest = angles.min()

    axes = []
    for equivalent, angle in zip(equivalents, angles):
        if angle > smallest + DISORIENTATION_TIE_TOLERANCE:
            continue
        vector = equivalent.as_rotvec()
        norm = np.linalg.norm(vector)
        axes.append(np.zeros(3) if norm < DISORIENTATION_TIE_TOLERANCE else vector / norm)
    # the smallest angle can be reached by more than one description, in which case the
    # axis is not determined by the crystal, so the candidates are ordered to make the
    # choice among them reproducible
    axis = max(axes, key=lambda candidate: tuple(np.round(candidate, 9)))

    return float(np.degrees(smallest)), axis


def calculate_disorientation_angle(rotation: np.ndarray,
                                   operations: np.ndarray) -> float:
    """Returns the disorientation angle in degrees, i.e. the smallest angle among the
    rotations that are equivalent to the given one under the given symmetry operations.

    This is the angle that :func:`calculate_disorientation` returns, without the axis.

    Parameters
    ----------
    rotation
        Rotation to reduce, a proper orthogonal matrix.
    operations
        Symmetry operations to reduce it over, as returned by
        :func:`get_point_group_operations`.

    Raises
    ------
    ValueError
        If the rotation is not a 3x3 matrix.
    """
    return calculate_disorientation(rotation, operations)[0]
