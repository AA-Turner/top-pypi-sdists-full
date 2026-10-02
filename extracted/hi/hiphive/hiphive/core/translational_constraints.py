"""
Functionality for enforcing translational sum rules
"""

import sympy
from scipy.sparse import coo_matrix
import numpy as np

from ..input_output.logging_tools import logger
from .utilities import SparseMatrix, BiMap
from .orbits import get_orbits


logger = logger.getChild('sum_rules')


def create_constraint_map(cs):

    # First we need to know the global index of a eigentensor given which
    # orbit it belongs to.
    params = []
    n = 0
    for orbit_index, orbit in enumerate(cs.orbits):
        nParams_in_orbit = len(orbit.eigentensors)
        params.append(list(range(n, n + nParams_in_orbit)))
        n += nParams_in_orbit

    # If we dont want the sum rules an eye matrix is created instead.
    if not cs.acoustic_sum_rules:
        row = list(range(n))
        col = list(range(n))
        data = [1.0]*n
        cs._cvs = coo_matrix((data, (row, col)), shape=(n, n))
        return None

    M = get_translational_constraint_matrix(cs)

    nullspace = M.nullspace()
    logger.debug('Assembling solutions...')
    row = []
    col = []
    data = []
    for c, vec in enumerate(nullspace):
        for r, _, v in vec.row_list():
            row.append(r)
            col.append(c)
            data.append(np.float64(v))

    # sanity check that there are orbits still present
    if len(nullspace) == 0:
        raise ValueError('There are no degrees of freedom, error!')

    # This is the final product, the constraint map (or constraint vectors)
    cs._cvs = coo_matrix((data, (row, col)), shape=(len(vec), len(nullspace)))

    logger.debug('{} degrees of freedom'.format(cs._cvs.shape[1]))
    logger.debug('Finished constructing constraint vectors')


def get_translational_constraint_matrix(cs):
    logger.debug('Starting constructing constraint matrices')

    # First we need to know the global index of a eigentensor given which
    # orbit it belongs to.
    params = []
    n = 0
    for orbit_index, orbit in enumerate(cs.orbits):
        nParams_in_orbit = len(orbit.eigentensors)
        params.append(list(range(n, n + nParams_in_orbit)))
        n += nParams_in_orbit

    # The lookup is a fast way to get the eigentensors given a cluster Also the
    # orbit index is bundled to quickly find the correct parameter indices
    lookup = {}
    for orbit_index, orbit in enumerate(cs.orbits):
        for of in orbit.orientation_families:
            for cluster_index, perm_index in zip(of.cluster_indices,
                                                 of.permutation_indices):
                cluster = cs._cluster_list[cluster_index]
                perm = cs._permutations[perm_index]
                lookup[tuple(cluster)] = [et.transpose(perm) for et in
                                          of.eigentensors], orbit_index

    # Init just one row to be able to stack. n is the total number of
    # eigentensors
    M = SparseMatrix(1, n, 0)  # This is the constraint matrix
    for order in cs.cutoffs.orders:
        logger.debug('Order {}: '.format(order))

        # Find which minimal amount of prefixes that is needed
        # Essentially they are all the prototypes of order one less still
        # compatible with the cutoff.
        prefix_list = []
        if order == 2:
            for i in np.unique(cs.wyckoff_sites):
                prefix_list.append((i,))
        else:
            tmp_cluster_set = set()
            for cluster in cs._cluster_list:
                if len(cluster) != order:
                    continue
                for i in range(order):
                    c = tuple(cluster[:i]) + tuple(cluster[i+1:])
                    if c[0] < len(cs._prim):
                        tmp_cluster_set.add(c)
            tmp_cluster_list = BiMap()
            for c in tmp_cluster_set:
                tmp_cluster_list.append(c)
            orbits = get_orbits(tmp_cluster_list, cs._atom_list,
                                cs.rotation_matrices, cs.translation_vectors,
                                cs.permutations, cs._prim, cs.symprec)
            for orb in orbits:
                prefix_list.append(tmp_cluster_list[orb.prototype_index])

        m = SparseMatrix(3**order, M.shape[1], 0)  # intermediate matrix
        # Now loop over the prefix and add the last atom index
        for prefix in prefix_list:
            m *= 0
            cluster = list(prefix) + [None]
            for i in range(len(cs._atom_list)):
                cluster[-1] = i
                tmp = lookup.get(tuple(sorted(cluster)))
                if tmp is None:
                    continue
                ets, orbit_index = tmp
                inv_argsort = np.argsort(np.argsort(cluster))
                ets = [et.transpose(inv_argsort) for et in ets]
                for et, col in zip(ets, params[orbit_index]):
                    et_flat = et.flatten()
                    for j in et_flat.nonzero()[0]:
                        m[j, col] += sympy.nsimplify(et_flat[j])
            M = SparseMatrix.vstack(M, m)
            # only compress if there are very many elements
            if M.nnz() > cs._config['max_number_constraint_elements']:
                M = SparseMatrix.rref(M)[0]

    logger.debug('Finished constructing constraint matrices')
    logger.debug('Starting constructing constraint vectors')
    return M
