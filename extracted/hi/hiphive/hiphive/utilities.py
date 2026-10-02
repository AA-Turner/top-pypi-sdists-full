"""
This module contains various support/utility functions.
"""

from typing import List, Tuple
import numpy as np

from ase import Atoms
from ase.calculators.singlepoint import SinglePointCalculator
from ase.geometry import find_mic
from ase.geometry import get_distances
from ase.neighborlist import neighbor_list
from .cluster_space import ClusterSpace
from .force_constants import ForceConstants
from .input_output.logging_tools import logger


logger = logger.getChild('utilities')


def get_displacements(atoms: Atoms,
                      atoms_ideal: Atoms,
                      cell_tol: float = 1e-4) -> np.ndarray:
    """Returns the the smallest possible displacements between a
    displaced configuration relative to an ideal (reference)
    configuration.

    Notes
    -----
    * uses :func:`ase.geometry.find_mic`
    * assumes periodic boundary conditions in all directions

    Parameters
    ----------
    atoms
        configuration with displaced atoms
    atoms_ideal
        ideal configuration relative to which displacements are computed
    cell_tol
        cell tolerance; if cell missmatch more than tol value error is raised
    """
    if not np.array_equal(atoms.numbers, atoms_ideal.numbers):
        raise ValueError('Atomic numbers do not match.')
    if np.linalg.norm(atoms.cell - atoms_ideal.cell) > cell_tol:
        raise ValueError('Cells do not match.')

    raw_position_diff = atoms.positions - atoms_ideal.positions
    wrapped_mic_displacements = find_mic(raw_position_diff, atoms_ideal.cell, pbc=True)[0]
    return wrapped_mic_displacements


def _get_forces_from_atoms(atoms: Atoms, calc=None) -> np.ndarray:
    """ Try to get forces from an atoms object """

    # Check if two calculators are available
    if atoms.calc is not None and calc is not None:
        raise ValueError('Atoms.calc is not None and calculator was provided')

    # If calculator is provided as argument
    if calc is not None:
        atoms_tmp = atoms.copy()
        atoms_tmp.calc = calc
        forces_calc = atoms_tmp.get_forces()
        if 'forces' in atoms.arrays:
            if not np.allclose(forces_calc, atoms.get_array('forces')):
                raise ValueError('Forces in atoms.arrays are different from the calculator forces')
        return forces_calc

    # If calculator is attached
    if atoms.calc is not None:
        if not isinstance(atoms.calc, SinglePointCalculator):
            raise ValueError('atoms.calc is not a SinglePointCalculator')

        forces_calc = atoms.get_forces()
        if 'forces' in atoms.arrays:
            if not np.allclose(forces_calc, atoms.get_array('forces')):
                raise ValueError('Forces in atoms.arrays are different from the calculator forces')
        return forces_calc

    # No calculator attached or provided as argument, forces should therefore be in atoms.arrays
    if 'forces' in atoms.arrays:
        forces = atoms.get_array('forces')
    else:
        raise ValueError('Unable to find forces')
    return forces


def prepare_structure(atoms: Atoms,
                      atoms_ideal: Atoms,
                      calc: SinglePointCalculator = None,
                      check_permutation: bool = True) -> Atoms:
    """Prepare a structure in the format suitable for a
    :class:`StructureContainer <hiphive.StructureContainer>`.

    Either forces should be attached to input atoms object as an array,
    or the atoms object should have a SinglePointCalculator attached to it containing
    forces, or a calculator (calc) should be supplied.

    Parameters
    ----------
    atoms
        input structure
    atoms_ideal
        reference structure relative to which displacements are computed
    check_permutation
        whether find_permutation should be used or not
    calc
        ASE calculator used for computing forces

    Returns
    -------
    ASE atoms object
        prepared ASE atoms object with forces and displacements as arrays
    """
    # get forces
    forces = _get_forces_from_atoms(atoms, calc=calc)

    # setup new atoms
    if check_permutation:
        perm = find_permutation(atoms, atoms_ideal)
    else:
        perm = np.array([f for f in range(len(atoms))])
    atoms_new = atoms.copy()
    atoms_new = atoms_new[perm]
    atoms_new.arrays['forces'] = forces[perm]
    disps = get_displacements(atoms_new, atoms_ideal)
    atoms_new.arrays['displacements'] = disps
    atoms_new.positions = atoms_ideal.positions

    return atoms_new


def prepare_structures(structures: List[Atoms],
                       atoms_ideal: Atoms,
                       calc: SinglePointCalculator = None,
                       check_permutation: bool = True) -> List[Atoms]:
    """Prepares a set of structures in the format suitable for adding them to
    a :class:`StructureContainer <hiphive.StructureContainer>`.

    `structures` should represent a list of supercells with displacements
    while `atoms_ideal` should provide the ideal reference structure (without
    displacements) for the given structures.

    The structures that are returned will have their positions reset to the
    ideal structures. Displacements and forces will be added as arrays to the
    atoms objects.

    If no calculator is provided, then there must be an ASE
    `SinglePointCalculator <ase.calculators.singlepoint>` object attached to
    the structures or the forces should already be attached as
    arrays to the structures.

    If a calculator is provided then it will be used to compute the forces for
    all structures.

    Example
    -------

    The following example illustrates the use of this function::

        db = connect('dft_training_structures.db')
        training_structures = [row.toatoms() for row in db.select()]
        training_structures = prepare_structures(training_structures, atoms_ideal)
        for s in training_structures:
            sc.add_structure(s)

    Parameters
    ----------
    structures
        list of input displaced structures
    atoms_ideal
        reference structure relative to which displacements are computed
    calc
        ASE calculator used for computing forces

    Returns
    -------
    list of prepared structures with forces and displacements as arrays
    """
    return [prepare_structure(s, atoms_ideal, calc, check_permutation) for s in structures]


def find_permutation(atoms: Atoms, atoms_ref: Atoms) -> List[int]:
    """ Returns the best permutation of atoms for mapping one
    configuration onto another.

    Parameters
    ----------
    atoms
        configuration to be permuted
    atoms_ref
        configuration onto which to map

    Examples
    --------
    After obtaining the permutation via ``p = find_permutation(atoms1, atoms2)``
    the reordered structure ``atoms1[p]`` will give the closest match
    to ``atoms2``.
    """
    assert np.linalg.norm(atoms.cell - atoms_ref.cell) < 1e-6
    permutation = []
    for i in range(len(atoms_ref)):
        dist_row = get_distances(
            atoms.positions, atoms_ref.positions[i], cell=atoms_ref.cell, pbc=True)[1][:, 0]
        permutation.append(np.argmin(dist_row))

    if len(set(permutation)) != len(permutation):
        raise Exception('Duplicates in permutation')
    for i, p in enumerate(permutation):
        if atoms[p].symbol != atoms_ref[i].symbol:
            raise Exception('Matching lattice sites have different occupation')
    return permutation


class Shell:
    """
    Neighbor Shell class

    Parameters
    ----------
    types : list or tuple
        atomic types for neighbor shell
    distance : float
        interatomic distance for neighbor shell
    count : int
        number of pairs in the neighbor shell
    """

    def __init__(self,
                 types: List[str],
                 distance: float,
                 count: int = 0):
        self.types = types
        self.distance = distance
        self.count = count

    def __str__(self):
        s = '{}-{}   distance: {:10.6f}    count: {}'.format(*self.types, self.distance, self.count)
        return s

    __repr__ = __str__


def get_neighbor_shells(atoms: Atoms,
                        cutoff: float,
                        dist_tol: float = 1e-5) -> List[Shell]:
    """ Returns a list of neighbor shells.

    Distances are grouped into shells via the following algorithm:

    1. Find smallest atomic distance `d_min`

    2. Find all pair distances in the range `d_min + 1 * dist_tol`

    3. Construct a shell from these and pop them from distance list

    4. Go to 1.

    Parameters
    ----------
    atoms
        configuration used for finding shells
    cutoff
        exclude neighbor shells which have a distance larger than this value
    dist_tol
        distance tolerance
    """

    # get distances
    ijd = neighbor_list('ijd', atoms, cutoff)
    ijd = list(zip(*ijd))
    ijd.sort(key=lambda x: x[2])

    # sort into shells
    symbols = atoms.get_chemical_symbols()
    shells = []
    for i, j, d in ijd:
        types = tuple(sorted([symbols[i], symbols[j]]))
        for shell in shells:
            if abs(d - shell.distance) < dist_tol and types == shell.types:
                shell.count += 1
                break
        else:
            shell = Shell(types, d, 1)
            shells.append(shell)
    shells.sort(key=lambda x: (x.distance, x.types, x.count))

    # warning if two shells are within 2 * tol
    for i, s1 in enumerate(shells):
        for j, s2 in enumerate(shells[i+1:]):
            if s1.types != s2.types:
                continue
            if not s1.distance < s2.distance - 2 * dist_tol:
                logger.warning('Found two shells within 2 * dist_tol')

    return shells


def extract_parameters(fcs: ForceConstants,
                       cs: ClusterSpace,
                       sanity_check: bool = True,
                       lstsq_method: str = 'numpy') \
        -> Tuple[np.ndarray, np.ndarray, int, np.ndarray]:
    """ Extracts parameters from force constants.


    This function can be used to extract parameters to create a
    ForceConstantPotential from a known set of force constants.
    The return values come from NumPy's `lstsq function
    <https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html>`_
    or from SciPy's `sparse lsqr function
    <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.lsqr.html>`_.
    Using `lstsq_method='scipy'` might be faster and have a smaller memory footprint for large
    systems, at the expense of some accuracy. This is due to the use of sparse matrices
    and an iterative solver.

    Parameters
    ----------
    fcs
        force constants
    cs
        cluster space
    sanity_check
        bool whether or not to perform a sanity check by computing the relative error between
        the input fcs and the output fcs
    lstsq_method
        method to use when making a least squares fit of a ForceConstantModel to the given fcs,
        allowed values are 'numpy' for `np.linalg.lstsq` or 'scipy' `for scipy.sparse.linalg.lsqr`

    Returns
    -------
    parameters
        parameters that together with the ClusterSpace generates the best representation of the FCs

    """
    from .force_constant_model import ForceConstantModel
    from .force_constant_potential import ForceConstantPotential
    from scipy.sparse.linalg import lsqr

    if lstsq_method not in ['numpy', 'scipy']:
        raise ValueError('lstsq_method must be either numpy or scipy')

    # extract the parameters
    fcm = ForceConstantModel(fcs.supercell, cs)
    # If the cluster space large, a sparse least squares solver is faster
    if lstsq_method == 'numpy':
        A, b = fcm.get_fcs_sensing(fcs, sparse=False)
        parameters = np.linalg.lstsq(A, b, rcond=None)[0]
    elif lstsq_method == 'scipy':
        A, b = fcm.get_fcs_sensing(fcs, sparse=True)
        # set minimal tolerances to maximize iterative least squares accuracy
        parameters = lsqr(A, b, atol=0, btol=0, conlim=0)[0]

    # calculate the relative force constant error
    if sanity_check:
        fcp = ForceConstantPotential(cs, parameters)
        fcs_hiphive = fcp.get_force_constants(fcs.supercell)
        for order in cs.cutoffs.orders:
            fc_original = fcs.get_fc_array(order=order)
            fc_reconstructed = fcs_hiphive.get_fc_array(order=order)
            rel_error = np.linalg.norm(fc_original-fc_reconstructed) / np.linalg.norm(fc_original)
            print(f'Force constant reconstruction error order {order}: {100*rel_error:9.4f}%')

    return parameters
