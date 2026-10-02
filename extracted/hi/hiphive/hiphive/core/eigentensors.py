import numpy as np
import itertools
import sympy
from .tensors import rotate_tensor
from ..input_output.logging_tools import logger
from .utilities import SparseMatrix


logger = logger.getChild('eigensymmetries')


def create_eigentensors(cs):

    for orbit in cs.orbits:
        prototype_cluster = cs._cluster_list[orbit.prototype_index]

        # The first round of eigentensors are created from the atom label
        # permutation condition
        ets = init_ets_from_label_symmetry(prototype_cluster)

        # Loop over the symmetries and apply them iteratively to reduce the
        # number of eigentensors
        for rotation_index, permutation_index in orbit.eigensymmetries:

            # Rotation amtrix in scaled coordinates
            R = cs.rotation_matrices[rotation_index]
            p = cs._permutations[permutation_index]  # permutation vector

            # Skip if the symmetry is the trivial identity operation
            if np.allclose(R, np.eye(3)) and p == tuple(range(orbit.order)):
                continue

            p_inv = np.argsort(p)

            # Create the intermediate constraint matrix and populate it
            M = SparseMatrix.zeros(3**orbit.order, len(ets))
            populate_constraint_matrix(M, ets, R, p_inv)

            nullspace = M.nullspace()

            new_ets = []
            for solution in nullspace:
                # Normalize the solution vector so it is inly integers
                # Done by multiplying with the greatest common multiple of the
                # denominators present
                solution = renormalize_to_integer(solution)
                # From the solution vector and the old eigentensors a new et is
                # created
                new_ets.append(assemble_new_eigentensor(ets, solution))
            ets = new_ets

            # If the force constant is forbidden by symmetry, break early
            if len(ets) == 0:
                break

        orbit.eigentensors = ets


def populate_constraint_matrix(M, ets, R, p_inv):
    for et_index, et in enumerate(ets):
        tmp = rotate_tensor(et.transpose(p_inv), R)
        tmp = tmp - et
        for element_index, v in enumerate(tmp.flat):
            if v != 0:
                M[element_index, et_index] = v


def init_ets_from_label_symmetry(cluster):
    """ This function creates eigentensor which fulfill the atom label
    symmetry. The only information needed is the corresponding cluster
    """
    order = len(cluster)
    assert sorted(cluster) == list(cluster)
    multiplicities = np.unique(cluster, return_counts=True)[1]
    ets = {}
    # Loop over all elements, represented by multi indices
    for multi_index in itertools.product([0, 1, 2], repeat=order):
        # Sort the multi index based on the multiplicities
        # e.g. cluster [1 1 2]
        # -> [z y x] == [y z x]
        sorted_multi_index = []
        j = 0
        for m in multiplicities:
            sorted_multi_index.extend(sorted(multi_index[j:j + m]))
            j += m
        sorted_multi_index = tuple(sorted_multi_index)
        if sorted_multi_index not in ets:
            ets[sorted_multi_index] = np.zeros([3]*order, dtype=np.int64)
        ets[sorted_multi_index][multi_index] = 1
    return list(ets.values())


def assemble_new_eigentensor(eigentensors, solution):
    new_eigentensor = np.zeros(eigentensors[0].shape, dtype=np.int64)
    for parameter, eigentensor in zip(solution, eigentensors):
        new_eigentensor += np.int64(parameter) * eigentensor
    return new_eigentensor


def renormalize_to_integer(vector):
    gcm = 1  # greates common multiple
    for v in vector:
        if v.is_Integer:
            continue
        den = v.q  # Denomonator
        gcd = sympy.gcd(gcm, den)  # greates common divisor
        tmp = den / gcd
        gcm = gcm * tmp
    # Now all elements should be smallest possible integers
    vector = vector * gcm
    return vector
