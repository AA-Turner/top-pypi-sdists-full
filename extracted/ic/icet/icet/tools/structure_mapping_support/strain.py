"""
Strain measures used when mapping a structure onto a reference structure.
"""

import numpy as np
import scipy.linalg


def calculate_strain_tensor(A: np.ndarray,
                            B: np.ndarray) -> np.ndarray:
    """Calculates the strain tensor for mapping a cell A onto cell B. The
    strain calculated is the Biot strain tensor and is rotationally invariant.

    Parameters
    ----------
    A
        Reference cell (row-major format).
    B
        Target cell (row-major format).

    Returns
    -------
        Biot strain tensor, i.e. the right stretch tensor relating the two
        cells minus the identity matrix. The tensor is symmetric and vanishes
        if the two cells are related by a pure rotation.

    Raises
    ------
    ValueError
        If either cell is not a 3x3 matrix.

    Example
    -------
    A cell that is inflated by two percent is strained by two percent along each
    of the three principal directions::

        >>> import numpy as np
        >>> from icet.tools.structure_mapping_support.strain import calculate_strain_tensor
        >>> A = np.array([[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]])
        >>> strain = calculate_strain_tensor(A, 1.02 * A)
        >>> np.round(np.diag(strain), 6).tolist()
        [0.02, 0.02, 0.02]

    The tensor is invariant under a rotation of either cell, so a structure that
    is merely rotated is not strained::

        >>> rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        >>> float(np.abs(calculate_strain_tensor(A, A @ rotation.T)).max())
        0.0
    """
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    for name, cell in (('A', A), ('B', B)):
        if cell.shape != (3, 3):
            raise ValueError('Cell {} is not a 3x3 matrix, its shape is {}.'.format(
                name, cell.shape))

    # Calculate deformation gradient (F) in column-major format
    F = np.linalg.solve(A, B).T

    # Calculate right stretch tensor (U)
    _, U = scipy.linalg.polar(F)

    # return Biot strain tensor
    return U - np.eye(3)


def get_periodic_frame(cell: np.ndarray, pbc: np.ndarray = None) -> np.ndarray:
    """Returns the cell with the vectors along non-periodic directions replaced by an
    orthonormal basis of the complement of the periodic subspace.

    Both the extent and the direction of a cell vector along a direction that is not periodic
    are a matter of how much empty space to carry, so neither may enter a strain. Substituting
    the vector of the reference cell for that of the target removes the extent but not the
    direction: holding an oblique vector fixed while the periodic subspace is deformed is
    itself a deformation, and it inflates the strain.

    Replacing the vector by a unit vector orthogonal to the periodic subspace removes both. The
    deformation relating two cells treated this way maps the periodic subspace and its
    complement separately, so the strain of the complement vanishes and that of the subspace is
    left exactly as it is. The sign is chosen so that the handedness of the cell is preserved.

    Parameters
    ----------
    cell
        Cell metric (row-major format).
    pbc
        Boundary conditions. The cell is returned unchanged if every direction is periodic,
        which is also what happens if this is not given.

    Returns
    -------
        Cell of shape ``(3, 3)`` whose periodic rows are those of :attr:`cell`.
    """
    cell = np.asarray(cell, dtype=np.float64)
    if pbc is None:
        return cell
    periodic = np.asarray(pbc, dtype=bool)
    if periodic.all():
        return cell
    if not periodic.any():
        # nothing is periodic, so there is no subspace to compare and no strain to report
        return np.eye(3)

    frame = np.array(cell)
    # the columns of Q beyond the rank of the periodic vectors span their complement
    basis, _ = np.linalg.qr(cell[periodic].T, mode='complete')
    frame[~periodic] = basis[:, periodic.sum():].T
    if np.linalg.det(frame) < 0:
        frame[np.flatnonzero(~periodic)[0]] *= -1
    return frame


def transfer_positions(positions: np.ndarray,
                       source_frame: np.ndarray,
                       target_frame: np.ndarray) -> np.ndarray:
    """Returns the positions expressed in the target cell rather than the source cell.

    Along the periodic directions the reduced coordinates are kept, which is what carries an
    atom to the corresponding place in a cell of a different size or orientation. Along the
    remaining directions the Cartesian component is kept instead. Scaling those as well would
    let the amount and the direction of empty space around a slab move its atoms, and a slab
    whose vacuum vector is merely oblique would come out sheared.

    Parameters
    ----------
    positions
        Cartesian positions, of shape ``(N, 3)``.
    source_frame
        Frame the positions are given in, as returned by :func:`get_corresponding_frames`.
    target_frame
        Frame they are wanted in, the other of that pair.

    Returns
    -------
        Cartesian positions in the target frame, of shape ``(N, 3)``.
    """
    positions = np.asarray(positions, dtype=np.float64)
    reduced = np.linalg.solve(np.asarray(source_frame, dtype=np.float64).T, positions.T).T
    return reduced @ np.asarray(target_frame, dtype=np.float64)


def calculate_maximum_biot_strains(A: np.ndarray,
                                   B: np.ndarray,
                                   pbc: np.ndarray = None) -> np.ndarray:
    """Returns the largest absolute eigenvalue of the Biot strain tensor for each of a stack
    of reference cells mapped onto one target cell.

    The measure is taken from the metric tensors of the two cells rather than from the
    deformation gradient. Writing the metric of the target as :math:`G_B = A C A^T` for the
    reference cell :math:`A`, with :math:`C` the square of the right stretch, the eigenvalues
    of the stretch are the square roots of those of :math:`G_A^{-1} G_B`. Only the metric
    tensors therefore enter, which has two consequences: a whole stack of cells is evaluated
    at once, which matters because the search for a transformation matrix applies the measure
    to every candidate it generates, and the measure restricts to a subspace by taking the
    metric tensors of that subspace alone.

    Parameters
    ----------
    A
        Reference cells (row-major format), of shape ``(N, 3, 3)``.
    B
        Target cell (row-major format), of shape ``(3, 3)``.
    pbc
        Boundary conditions. The measure is taken over the subspace spanned by the periodic
        cell vectors, so that the cell vectors along the remaining directions, whose extent is
        arbitrary, do not enter at all. Every direction is taken to be periodic if this is not
        given, and the measure then covers the whole cell.

    Returns
    -------
        Array of shape ``(N,)`` holding the largest absolute eigenvalue for each cell. It
        vanishes if no direction is periodic, there being no strain to speak of.

    Example
    -------
    Inflating a cell by two percent strains it by two percent, whatever its orientation::

        >>> import numpy as np
        >>> from icet.tools.structure_mapping_support.strain import (
        ...     calculate_maximum_biot_strains)
        >>> A = np.array([[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]])
        >>> np.round(calculate_maximum_biot_strains(A[None, :, :], 1.02 * A), 6).tolist()
        [0.02]
    """
    A = np.asarray(A, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)

    periodic = np.ones(3, dtype=bool) if pbc is None else np.asarray(pbc, dtype=bool)
    A = A[..., periodic, :]
    B = B[..., periodic, :]
    if A.shape[-2] == 0:
        return np.zeros(A.shape[:-2])

    gram_reference = A @ np.swapaxes(A, -1, -2)
    gram_target = np.broadcast_to(B @ np.swapaxes(B, -1, -2), gram_reference.shape)

    # The eigenvalues sought are those of the inverse of one metric tensor times the other.
    # Reducing with the Cholesky factor of the former gives a symmetric matrix with the same
    # eigenvalues, which is both cheaper and better conditioned than forming the product.
    factor = np.linalg.cholesky(gram_reference)
    reduced = np.linalg.solve(factor, gram_target)
    reduced = np.linalg.solve(factor, np.swapaxes(reduced, -1, -2))

    stretches = np.sqrt(np.maximum(np.linalg.eigvalsh(reduced), 0.0))
    return np.abs(stretches - 1).max(axis=-1)


def calculate_strain_eigenvalues(strain_tensor: np.ndarray) -> np.ndarray:
    """Calculates the eigenvalues of a strain tensor.

    Parameters
    ----------
    strain_tensor
        Strain tensor, which is assumed to be symmetric.

    Returns
    -------
        The three eigenvalues in ascending order. They are real, since the
        strain tensor is symmetric.
    """
    eigenvalues, _ = np.linalg.eigh(strain_tensor)
    return eigenvalues


def calculate_volumetric_strain(strain_tensor: np.ndarray) -> float:
    """Calculates the volumetric strain, i.e. the relative change of the volume,
    corresponding to a strain tensor.

    Parameters
    ----------
    strain_tensor
        Biot strain tensor, as returned by :func:`calculate_strain_tensor`.

    Returns
    -------
        Relative change of the volume. Since the Biot strain tensor is the right
        stretch tensor minus the identity matrix, the ratio of the volumes is the
        determinant of the former plus the identity matrix.

    Example
    -------
    An isotropic strain of two percent changes the volume by somewhat more than
    six percent::

        >>> import numpy as np
        >>> from icet.tools.structure_mapping_support.strain import (
        ...     calculate_volumetric_strain)
        >>> round(calculate_volumetric_strain(0.02 * np.eye(3)), 6)
        0.061208
    """
    return float(np.linalg.det(strain_tensor + np.eye(3)) - 1)
