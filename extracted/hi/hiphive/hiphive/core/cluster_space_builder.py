import itertools
import numpy as np
import spglib as spg
from collections import Counter
from ase.neighborlist import NeighborList

from .atoms import Atom, Atoms
from .clusters import get_clusters
from .orbits import get_orbits
from ..input_output.logging_tools import logger
from .eigentensors import create_eigentensors as _create_eigentensors
from .tensors import rotate_tensor_precalc, rotation_tensor_as_matrix
from .translational_constraints import create_constraint_map as _create_constraint_map
from .utilities import BiMap, ase_atoms_to_spglib_tuple


# TODO: Add longer description of each step
# TODO: Be careful with side effects
# TODO: Preferably the functions should not take the cs as input
def build_cluster_space(cluster_space, prototype_structure):

    """ The permutation list is an indexed fast lookup table for permutation
    vectors.
    """
    logger.debug('Populate permutation list')
    _create_permutations(cluster_space)

    """ The primitive cell is calcualted by spglib and contains the cell
    metric, basis and atomic numbers. After this the prototype structure is
    disposed.
    """
    logger.debug('Get primitive cell')
    _create_primitive_cell(cluster_space, prototype_structure)

    """ The symmetries are calculated by spglib and the main information is the
    rotation matrices and translation vectors for each symmetry in scaled
    coordinates.
    """
    logger.debug('Get symmetries')
    _create_symmetry_dataset(cluster_space)

    """ The neigbor atoms to the center cell are stored in an indexed list. The
    list contains all atoms within the maximum cutoff specified.
    """
    logger.debug('Find neighbors')
    _create_atom_list(cluster_space)

    """ Clusters are generated as combinations of the indices of the atoms in
    the atom_list. If the cluster is to be included or not depends on the
    specification of valid clusters in the cutoffs object. Often all atoms must
    be within some distance from each other which may depend on both expansion
    order and number of atoms in the cluster
    """
    logger.debug('Starting generating clusters')
    _create_cluster_list(cluster_space)
    logger.debug('Finished generating clusters')

    """ The clusters are categorized into orbits and the eigensymmetries are
    stored in each orbit.
    """
    logger.debug('Starting categorizing clusters')
    _create_orbits(cluster_space)
    logger.debug('Finished categorizing clusters')

    """ The eigensymmetries from the previous step is used to generate valid
    eigentensors
    """
    logger.debug('Starting finding eigentensors')
    _create_eigentensors(cluster_space)
    logger.debug('Finished finding eigentensors')

    """ If some orbits can't have a force constant due to symmetry they are
    dropped from the _orbits attribute but kept in a separate list named
    _dropped_orbits
    """
    logger.debug('Dropping orbits...')
    _drop_orbits(cluster_space)

    """ Each orientation family gets populated with its rotated version of the
    orbits eigentensors.
    """
    logger.debug('Rotating eigentensors into ofs...')
    _populate_ofs_with_ets(cluster_space)

    """ The matrix describing the mapping which preserves the global symmetries
    is created (translational and rotational symmetry).
    """
    logger.debug('Constructing constraint map')
    _create_constraint_map(cluster_space)
    logger.info('Constraints:')
    logger.info('    Acoustic: {}'.format(cluster_space.acoustic_sum_rules))
    ndofs_by_order = {o: cluster_space.get_n_dofs_by_order(o) for o in cluster_space.cutoffs.orders}
    logger.info('    Number of degrees of freedom: {}'.format(ndofs_by_order))
    for order, count in ndofs_by_order.items():
        if count == 0:
            logger.warning('    Warning: No degrees of freedom exists for order {}'.format(order))
    logger.info('    Total number of degrees of freedom: {}'.format(cluster_space.n_dofs))

    """  The eigentensors are rescaled depending on order to create a more well
    behaved system for fitting. NOTE! In here the constratints are rescaled too
    """
    logger.debug('Rescale eigentensors')
    _rescale_eigentensors(cluster_space)

    logger.debug('Normalize constraints')
    _normalize_constraint_vectors(cluster_space)

    logger.debug('Rotate tensors to Carteesian coordinates')
    _rotate_eigentensors(cluster_space)


# TODO: Actual input could be just the maximum order
# TODO: No side effects, returns only the permutation BiMap
def _create_permutations(cs):
    orders = cs.cutoffs.orders
    permutations = BiMap()
    for order in orders:
        for permutation in itertools.permutations(range(order)):
            permutations.append(permutation)
    cs._permutations = permutations


# TODO: tolerances must be fixed in a coherent way. Prefarably via a config
# object
# TODO: Does the basis check need to be done? There might not be a problem that
# it is close to 1 instead of 0 anymore. If thats the case it is better to keep
# it as spglib returns it
# TODO: Add good debug
# TODO: Assert spos dot cell == pos. Sometimes the positions can be outside of
# the cell and then there is a mismatch between wath is returned by
# get_sclad_positions, positions and what spos dot cell gives (it should give
# the position
# TODO: Check basis to see if it can be represented by sympy. (in preparation
# for rotational sum rules)
# TODO: general function -> break out into utility function
# TODO: Send the tolerance as a parameter instef of the whole cs.
def _create_primitive_cell(cs, prototype_structure):

    structure_as_tuple = ase_atoms_to_spglib_tuple(prototype_structure)
    spgPrim = spg.standardize_cell(structure_as_tuple, no_idealize=True,
                                   to_primitive=True, symprec=cs.symprec)

    numbers_match = sorted(spgPrim[2]) == sorted(prototype_structure.numbers)
    spg_cell_volume = np.abs(np.linalg.det(spgPrim[0].T))
    prototype_cell_volume = np.abs(np.linalg.det(prototype_structure.cell.T))
    # TODO: is symprec the best tolerance to use for volume check?
    cell_volume_match = np.isclose(spg_cell_volume, prototype_cell_volume, atol=cs.symprec, rtol=0)

    if numbers_match and cell_volume_match:
        prim = Atoms(prototype_structure)
        prim.wrap()
    else:
        basis = spgPrim[1]
        if np.any(basis > (1 - cs.symprec)):
            logger.debug('Found basis close to 1:\n {}'.format(str(basis)))
            basis = basis.round(8) % 1  # TODO
            logger.debug('Wrapping to:\n {}'.format(str(basis)))
        prim = Atoms(cell=spgPrim[0], scaled_positions=basis, numbers=spgPrim[2], pbc=True)

    # log primitive cell information
    logger.info('Primitive cell:')
    logger.info('    Formula: {}'.format(prim.get_chemical_formula()))
    logger.info(('    Cell:' + '\n        [{:9.5f} {:9.5f} {:9.5f}]'*3).format(
        *prim.cell[0], *prim.cell[1], *prim.cell[2]))
    logger.info('    Basis:')
    if len(prim) < 5:
        for symbol, spos in zip(prim.get_chemical_symbols(), prim.basis):
            logger.info('        {:2}  [{:9.5f} {:9.5f} {:9.5f}]'.format(symbol, *spos))
    else:
        for sym, spos in zip(prim[:3].get_chemical_symbols(), prim[:3].basis):
            logger.info('        {:2}  [{:9.5f} {:9.5f} {:9.5f}]'.format(sym, *spos))
        logger.info('        ...')
    logger.info('')
    cs._prim = prim


# TODO: Fix how the tolerance is handled
# TODO: Look over properties to acccess symmetry_dataset. Especially rotation,
# translation and wyckoff
# TODO: Sen prim and symprec as parameters
def _create_symmetry_dataset(cs):

    prim_as_tuple = ase_atoms_to_spglib_tuple(cs.primitive_structure)
    symmetry_dataset = spg.get_symmetry_dataset(prim_as_tuple, symprec=cs.symprec)
    cs._symmetry_dataset = symmetry_dataset

    logger.info('Crystal symmetry:')
    logger.info('    Spacegroup:          {}'.format(cs.spacegroup))
    logger.info('    Unique site:         {}'.format(len(set(cs.wyckoff_sites))))
    logger.info('    Symmetry operations: {}'.format(len(cs.rotation_matrices)))
    logger.info('    symprec:             {:.2e}'.format(cs.symprec))
    logger.info('')


# TODO: Fix how the tolerance is handled
# TODO: Refactor the two runs of finding the neighbors
# TODO: The bug that the cutoff is exactly on a shell might be a non issue.
# TODO: It is possible to check that the clusters map out the orbits completely
# TODO: Send in prim, cutoff and config and return atom_list instead
def _create_atom_list(cs):

    tol = cs.symprec
    atom_list = BiMap()

    # Populating the atom list with the center atoms
    for i in range(len(cs._prim)):
        atom_list.append(Atom(i, [0, 0, 0]))

    logger.info('Cutoffs:')
    logger.info('    Maximum cutoff: {}'.format(cs.cutoffs.max_cutoff))

    # Find all the atoms which is neighbors to the atoms in the center cell
    # The pair cutoff should be larger or equal than the others
    cutoffs = [(cs.cutoffs.max_cutoff - tol) / 2] * len(cs._prim)
    nl = NeighborList(cutoffs=cutoffs, skin=0, self_interaction=True, bothways=True)
    nl.update(cs._prim)
    for i in range(len(cs._prim)):
        for index, offset in zip(*nl.get_neighbors(i)):
            atom = Atom(index, offset)
            if atom not in atom_list:
                atom_list.append(atom)

    nl = NeighborList(
        cutoffs=[(cs.cutoffs.max_cutoff + tol) / 2] * len(cs._prim),
        skin=0, self_interaction=True, bothways=True)
    nl.update(cs._prim)
    distance_from_cutoff = tol
    for i in range(len(cs._prim)):
        for index, offset in zip(*nl.get_neighbors(i)):
            atom = Atom(index, offset)
            # ... and check that no new atom is found
            if atom not in atom_list:
                pos = atom.pos(cs._prim.basis, cs._prim.cell)
                distance = min(np.linalg.norm(pos - atom.position)
                               for atom in cs._prim) - cs.cutoffs.max_cutoff
                distance_from_cutoff = min(distance, distance_from_cutoff)

    if distance_from_cutoff != tol:
        raise Exception('Maximum cutoff close to neighbor shell, change cutoff')

    msg = '    Found {} center atom{} with {} images totaling {} atoms'.format(
        len(cs._prim), 's' if len(cs._prim) > 1 else '',
        len(atom_list) - len(cs._prim), len(atom_list))
    logger.info(msg)
    logger.info('')

    cs._atom_list = atom_list


# TODO: add atoms property to cs
# TODO: Only inputs are prim, atom_list and cutoffs
def _create_cluster_list(cs):

    # Convert the atom list from site/offset to scaled positions
    spos = [a.spos(cs._prim.basis) for a in cs._atom_list]
    numbers = [cs._prim.numbers[a.site] for a in cs._atom_list]

    # Make an atoms object out of the scaled positions
    atoms = Atoms(cell=cs._prim.cell, scaled_positions=spos, numbers=numbers, pbc=False)

    cs._cluster_filter.setup(atoms)
    cs._cluster_list = get_clusters(atoms, cs.cutoffs, len(cs._prim))

    logger.info('Clusters:')
    counter = Counter(len(c) for c in cs._cluster_list)
    logger.info('    Clusters: {}'.format(dict(counter)))
    logger.info('    Total number of clusters: {}\n'.format(sum(counter.values())))


def _create_orbits(cs):
    # TODO: Check scaled/cart
    cs._orbits = get_orbits(cs._cluster_list,
                            cs._atom_list,
                            cs.rotation_matrices,
                            cs.translation_vectors,
                            cs.permutations,
                            cs._prim,
                            cs.symprec)
    orbits_to_drop = []
    for i, orbit in enumerate(cs.orbits):
        if not cs._cluster_filter(cs._cluster_list[orbit.prototype_index]):
            orbits_to_drop.append(i)

    reduced_orbits = []
    cs._dropped_orbits = []
    for i in range(len(cs.orbits)):
        if i in orbits_to_drop:
            cs._dropped_orbits.append(cs.orbits[i])
        else:
            reduced_orbits.append(cs.orbits[i])
    cs._orbits = reduced_orbits

    counter = Counter(orb.order for orb in cs._orbits)
    logger.info('Orbits:')
    logger.info('    Orbits: {}'.format(dict(counter)))
    logger.info('    Total number of orbits: {}\n'.format(sum(counter.values())))


def _drop_orbits(cs):
    orbits_to_drop = []
    for i, orbit in enumerate(cs.orbits):
        if not orbit.eigentensors:
            orbits_to_drop.append(i)

    reduced_orbits = []

    for i in range(len(cs.orbits)):
        if i in orbits_to_drop:
            cs._dropped_orbits.append(cs.orbits[i])
        else:
            reduced_orbits.append(cs.orbits[i])
    cs._orbits = reduced_orbits

    logger.info('Eigentensors:')
    n_ets = dict()
    for order in cs.cutoffs.orders:
        n_ets[order] = sum(len(orb.eigentensors) for orb in cs.orbits if orb.order == order)
    logger.info('    Eigentensors: {}'.format(n_ets))
    logger.info('    Total number of parameters: {}'.format(sum(n_ets.values())))
    if len(cs._dropped_orbits) > 0:
        logger.info('    Discarded orbits:')
        for orb in cs._dropped_orbits:
            logger.info('        {}'.format(cs.cluster_list[orb.prototype_index]))
    counter = Counter(orb.order for orb in cs._orbits)
    for order in cs.cutoffs.orders:
        if counter[order] == 0:
            logger.warning('    Warning: No orbits exists for order {}'.format(order))
    logger.info('')


def _populate_ofs_with_ets(cs):

    R_inv_lookup = dict()
    for orbit_index, orbit in enumerate(cs.orbits):
        for of in orbit.orientation_families:
            R_inv_lookup_index = (of.symmetry_index, orbit.order)
            R_inv = R_inv_lookup.get(R_inv_lookup_index, None)
            if R_inv is None:
                R = cs.rotation_matrices[of.symmetry_index]
                R_inv_tmp = np.linalg.inv(R)
                R_inv = R_inv_tmp.astype(np.int64)
                assert np.allclose(R_inv, R_inv_tmp), (R_inv, R_inv_tmp)
                R_inv = rotation_tensor_as_matrix(R_inv, orbit.order)
                R_inv_lookup[R_inv_lookup_index] = R_inv
            of.eigentensors = []
            for et in orbit.eigentensors:
                rotated_et = rotate_tensor_precalc(et, R_inv)
                assert rotated_et.dtype == np.int64
                of.eigentensors.append(rotated_et)


def _rotate_eigentensors(cs):
    V_invT = np.linalg.inv(cs._prim.cell.T)
    lookup = dict()
    for orb in cs.orbits:
        V_invT_tensormatrix = lookup.get(orb.order, None)
        if V_invT_tensormatrix is None:
            V_invT_tensormatrix = rotation_tensor_as_matrix(V_invT, orb.order)
            lookup[orb.order] = V_invT_tensormatrix
        orb.eigentensors = [rotate_tensor_precalc(et, V_invT_tensormatrix) for et in orb.eigentensors]  # noqa
        for of in orb.orientation_families:
            of.eigentensors = [rotate_tensor_precalc(et, V_invT_tensormatrix) for et in of.eigentensors]  # noqa


def _normalize_constraint_vectors(cs):
    M = cs._cvs
    norms = np.zeros(M.shape[1])
    for c, v in zip(M.col, M.data):
        norms[c] += v**2
    for i in range(len(norms)):
        norms[i] = np.sqrt(norms[i])
    for i, c in enumerate(M.col):
        M.data[i] /= norms[c]


def _rescale_eigentensors(cs):
    for orbit in cs.orbits:
        norm = cs.length_scale**orbit.order
        ets = orbit.eigentensors
        for i, et in enumerate(ets):
            ets[i] = et.astype(np.float64)
            ets[i] /= norm
        for of in orbit.orientation_families:
            ets = of.eigentensors
            for i, et in enumerate(ets):
                ets[i] = et.astype(np.float64)
                ets[i] /= norm

    orders = []
    for orbit in cs.orbits:
        for et in orbit.eigentensors:
            orders.append(orbit.order)

    M = cs._cvs
    for i, r in enumerate(M.row):
        M.data[i] *= cs.length_scale**orders[r]
