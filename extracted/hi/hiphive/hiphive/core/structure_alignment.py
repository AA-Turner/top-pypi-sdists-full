import itertools
import numpy as np
import spglib as spg
from . import atoms as atoms_module
from ..input_output.logging_tools import logger
from .utilities import ase_atoms_to_spglib_tuple

logger = logger.getChild('relate_structures')


def align_supercell(supercell, prim, symprec=None):
    """Rotate and translate a supercell configuration such that it is aligned
    with the target primitive cell.

    Parameters
    ----------
    sc : ase.Atoms
        supercell configuration
    prim : ase.Atoms
        target primitive configuration
    symprec : float
        precision parameter forwarded to spglib

    Returns
    -------
    tuple(ase.Atoms, numpy.ndarray, numpy.ndarray)
        aligned supercell configuration as well as rotation matrix
        (`3x3` array) and translation vector (`3x1` array) that relate
        the input to the aligned supercell configuration.
    """

    # TODO: Make sure the input is what we expect

    # find rotation and translation
    R, T = relate_structures(supercell, prim, symprec=symprec)

    # Create the aligned system
    aligned_supercell = rotate_atoms(supercell, R)
    aligned_supercell.translate(T)
    aligned_supercell.wrap()
    return aligned_supercell, R, T


def relate_structures(reference, target, symprec=1e-5):
    """Finds rotation and translation operations that align two structures with
    periodic boundary conditions.

    The rotation and translation in Cartesian coordinates will map the
    reference structure onto the target

    Aligning reference with target can be achieved via the transformations::

        R, T = relate_structures(atoms_ref, atoms_target)
        atoms_ref_rotated = rotate_atoms(atoms_ref, R)
        atoms_ref_rotated.translate(T)
        atoms_ref_rotated.wrap()
        atoms_ref_rotated == atoms_target

    Parameters
    ----------
    reference : ase.Atoms
        The reference structure to be mapped
    target : ase.Atoms
        The target structure

    Returns
    -------
    R : numpy.ndarray
        rotation matrix in Cartesian coordinates (`3x3` array)
    T : numpy.ndarray
        translation vector in Cartesian coordinates
    """

    logger.debug('Reference atoms:')
    _debug_log_atoms(reference)

    reference_primitive_cell = get_primitive_cell(reference, symprec=symprec)

    logger.debug('Reference primitive cell')
    _debug_log_atoms(reference_primitive_cell)

    logger.debug('Target atoms:')
    _debug_log_atoms(target)

    target_primitive_cell = get_primitive_cell(target, symprec=symprec)

    logger.debug('Target primitive cell')
    _debug_log_atoms(target_primitive_cell)

    logger.debug('Sane check that primitive cells can match...')
    _assert_structures_match(reference_primitive_cell, target_primitive_cell)

    logger.debug('Finding rotations...')
    rotations = _find_rotations(reference_primitive_cell.cell,
                                target_primitive_cell.cell)

    logger.debug('Finding transformations...')
    for R in rotations:
        rotated_reference_primitive_cell = \
            rotate_atoms(reference_primitive_cell, R)
        T = _find_translation(rotated_reference_primitive_cell,
                              target_primitive_cell)
        if T is not None:
            break
    else:
        raise Exception(('Found no translation!\n'
                         'Reference primitive cell basis:\n'
                         '{}\n'
                         'Target primitive cell basis:\n'
                         '{}')
                        .format(reference_primitive_cell.basis,
                                target_primitive_cell.basis))

    logger.debug(('Found rotation\n'
                  '{}\n'
                  'and translation\n'
                  '{}')
                 .format(R, T))

    return R, T


def is_rotation(R, cell_metric=None):
    """Checks if rotation matrix is orthonormal

    A cell metric can be passed of the rotation matrix is in scaled coordinates

    Parameters
    ----------
    R : numpy.ndarray
        rotation matrix (`3x3` array)
    cell_metric : numpy.ndarray
        cell metric if the rotation is in scaled coordinates
    """
    if not cell_metric:
        cell_metric = np.eye(3)

    V = cell_metric
    V_inv = np.linalg.inv(V)
    lhs = np.linalg.multi_dot([V_inv, R.T, V, V.T, R, V_inv.T])

    return np.allclose(lhs, np.eye(3), atol=1e-4)  # TODO: tol


def _find_rotations(reference_cell_metric, target_cell_metric):
    """ Generates all proper and improper rotations aligning two cell
    metrics. """

    rotations = []
    V1 = reference_cell_metric
    for perm in itertools.permutations([0, 1, 2]):
        # Make sure the improper rotations are included
        for inv in itertools.product([1, -1], repeat=3):
            V2 = np.diag(inv) @ target_cell_metric[perm, :]
            R = np.linalg.solve(V1, V2).T
            # Make sure the rotation is orthonormal
            if is_rotation(R):
                for R_tmp in rotations:
                    if np.allclose(R, R_tmp):  # TODO: tol
                        break
                else:
                    rotations.append(R)

    assert rotations, ('Found no rotations! Reference cell metric:\n'
                       '{}\n'
                       'Target cell metric:\n'
                       '{}').format(reference_cell_metric, target_cell_metric)

    logger.debug('Found {} rotations'.format(len(rotations)))

    return rotations


def _assert_structures_match(ref, prim):
    """ Asserts the structures are compatible with respect to number of atoms,
    atomic numbers and volume.

    TODO: tol
    """

    if len(ref) != len(prim):
        raise ValueError(
            'Number of atoms in reference primitive cell {} does not match '
            'target primitive {}'.format(len(ref), len(prim)))

    if sorted(ref.numbers) != sorted(prim.numbers):
        raise ValueError('Atomic numbers do not match\nReference: {}\nTarget:'
                         ' {}\n'.format(ref.numbers, prim.numbers))

    if not np.isclose(ref.get_volume(), prim.get_volume()):
        raise ValueError(
            'Volume for reference primitive cell {} does not match target '
            'primitive cell {}\n'.format(ref.get_volume(), prim.get_volume()))


def get_primitive_cell(atoms, to_primitive=True, no_idealize=True,
                       symprec=1e-5):
    """ Gets primitive cell from spglib.

    Parameters
    ----------
    atoms : ase.Atoms
        atomic structure
    to_primitive : bool
        passed to spglib
    no_idealize : bool
        passed to spglib
    """
    if not all(atoms.pbc):
        raise ValueError('atoms must have pbc.')
    atoms_as_tuple = ase_atoms_to_spglib_tuple(atoms)
    spg_primitive_cell = spg.standardize_cell(atoms_as_tuple, to_primitive=True,
                                              no_idealize=True,
                                              symprec=symprec)
    primitive_cell = atoms_module.Atoms(cell=spg_primitive_cell[0],
                                        scaled_positions=spg_primitive_cell[1],
                                        numbers=spg_primitive_cell[2],
                                        pbc=True)
    return primitive_cell


def _debug_log_atoms(atoms):
    logger.debug('cell:\n{}'.format(atoms.cell))
    logger.debug('spos:\n{}'.format(atoms.get_scaled_positions()))
    logger.debug('pos:\n{}'.format(atoms.positions))
    logger.debug('numbers:\n{}'.format(atoms.numbers))


def rotate_atoms(atoms, rotation):
    """Rotates the cell and positions of Atoms and returns a copy

    Parameters
    ----------
    atoms : ase.Atoms
        atomic structure
    rotation : numpy.ndarray
        rotation matrix (`3x3` array)
    """
    cell = np.dot(rotation, atoms.cell.T).T
    positions = np.dot(rotation, atoms.positions.T).T
    return atoms_module.Atoms(cell=cell, positions=positions,
                              numbers=atoms.numbers, pbc=atoms.pbc)


def _find_translation(reference, target):
    """Returns the translation between two compatible atomic structures.

    The two structures must describe the same structure when infinitely
    repeated but differ by a translation.

    Parameters
    ----------
    reference : ase.Atoms
    target : ase.Atoms

    Returns
    -------
    numpy.ndarray or None
        translation vector or `None` if structures are incompatible
    """

    atoms = atoms_module.Atoms(cell=target.cell,
                               positions=reference.positions,
                               numbers=reference.numbers,
                               pbc=True)
    atoms.wrap()

    atoms_atom_0 = atoms[0]
    for atom in target:
        if atoms_atom_0.symbol != atom.symbol:
            continue
        T = atom.position - atoms_atom_0.position
        atoms_copy = atoms.copy()
        atoms_copy.positions += T
        if are_nonpaired_configurations_equal(atoms_copy, target):
            return T
    return None


def are_nonpaired_configurations_equal(atoms1, atoms2):
    """ Checks whether two configurations are identical.  To be considered
    equal the structures must have the same cell metric, elemental
    occupation, scaled positions (modulo one), and periodic boundary
    conditions.

    Unlike the ``__eq__`` operator of :class:`ase.Atoms` the order of the
    atoms does not matter.

    Parameters
    ----------
    atoms1 : ase.Atoms
    atoms2 : ase.Atoms

    Returns
    -------
    bool
        True if atoms are equal, False otherwise

    TODO: tol
    """
    n_atoms = len(atoms1)
    if not (np.allclose(atoms1.cell, atoms2.cell, atol=1e-4) and
            n_atoms == len(atoms2) and
            sorted(atoms1.numbers) == sorted(atoms2.numbers) and
            all(atoms1.pbc == atoms2.pbc)):
        return False
    new_cell = (atoms1.cell + atoms2.cell) / 2
    pos = [a.position for a in atoms1] + [a.position for a in atoms2]
    num = [a.number for a in atoms1] + [a.number for a in atoms2]
    s3 = atoms_module.Atoms(cell=new_cell, positions=pos, numbers=num,
                            pbc=True)
    for i in range(n_atoms):
        for j in range(n_atoms, len(s3)):
            d = s3.get_distance(i, j, mic=True)
            if abs(d) < 1e-4:  # TODO: tol
                if s3[i].number != s3[j].number:
                    return False
                break
        else:
            return False
    return True
