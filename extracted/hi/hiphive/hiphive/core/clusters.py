# Contains the get_clusters function which generates clusters

import numpy as np
import itertools
from collections import defaultdict

from .utilities import BiMap
from ..input_output.logging_tools import logger

logger = logger.getChild('get_clusters')


# TODO: This function could be made a bit more general
def get_clusters(atoms, cutoffs, nPrim, multiplicity=True,
                 use_geometrical_order=False):
    """Generate a list of all clusters in the atoms object which includes the
    center atoms with positions within the cell metric. The cutoff determines
    up to which order and range clusters should be generated.

    With multiplicity set to True clusters like `[0,0]` and `[3,3,4` etc will
    be generated. This is useful when doing force constants but not so much for
    cluster expansions.

    The geometrical order is the total number of different atoms in the
    cluster. `[0,0,1]` would have geometrical order 2 and `[1,2,3,4]` would
    have order 4. If the key word is True the cutoff criteria will be based on
    the geometrical order of the cluster. This is based on the observation that
    many body interactions decrease fast with cutoff but anharmonic
    interactions can be quite long ranged.

    Parameters
    ----------
    atoms : ase.Atoms
        can be a general atoms object but must have pbc=False.
    cutoffs : dict
        the keys specify the order while the values specify the cutoff radii
    multiplicity : bool
        includes clusters where same atom appears more than once
    geometrical_order : bool
        specifies if the geometrical order should be used as cutoff_order,
        otherwise the normal order of the cluster is used

    Returns
    -------
    list(tuple(int))
        a list of clusters where each entry is a tuple of indices,
        which refer to the atoms in the input supercell
    """

    logger.debug('Generating clusters...')
    cluster_dict = defaultdict(list)
    # Generate all on-site clusters of all orders (1-body)
    for i in range(nPrim):
        for order in cutoffs.orders:
            cluster = (i,) * order
            cluster_dict[order].append(cluster)

    # Generate all 2-body clusters and above in order
    for nbody in cutoffs.nbodies:
        cutoff = cutoffs.max_nbody_cutoff(nbody)
        # Generate all n-body, order n clusters compatible with the cutoff
        nbody_clusters, nbody_cutoffs = generate_geometrical_clusters(atoms, nPrim, cutoff, nbody)
        for order in range(nbody, cutoffs.max_nbody_order(nbody) + 1):
            for cluster, cutoff in zip(nbody_clusters, nbody_cutoffs):
                # If the cutoff of the n-body cluster is compatible with order (order > n) then
                # extend the n-body cluster to higher order (e.g. nbody=3, order=6: ijk -> iijkkk)
                if cutoff < cutoffs.get_cutoff(nbody=nbody, order=order):
                    cluster_dict[order].extend(extend_cluster(cluster, order))

    # The clusters are saved in a BiMap structure which allows for fast lookups
    cluster_list = BiMap()
    for key in sorted(cluster_dict):
        # For each order the clusters are saved in lexicographical order
        for cluster in sorted(cluster_dict[key]):
            cluster_list.append(cluster)
    return cluster_list


def generate_geometrical_clusters(atoms, n_prim, cutoff, order):
    neighbor_matrix, distance_matrix = create_neighbor_matrices(atoms, cutoff)
    clusters, cutoffs = [], []
    i, j = 0, 0
    # The clusters are generated in lexicographical order
    for cluster in itertools.combinations(range(len(atoms)), r=order):
        # If the first atom in the cluster has an index higher or equal to the number of atoms in
        # the primitive cell then no upcoming cluster will have an atom in the primitive cell, thus
        # we can break
        if cluster[0] >= n_prim:
            break
        # if the last cluster failed on index i, j we start by checking this index again to speed
        # things up
        if not neighbor_matrix[cluster[i], cluster[j]]:
            continue
        # loop through all pairs in the cluster and check so that they are neighbors
        for i, j in itertools.combinations(range(order), r=2):
            if not neighbor_matrix[cluster[i], cluster[j]]:
                break
        else:
            clusters.append(cluster)
            # We also note the cutoff each cluster is compatible with
            cutoffs.append(np.max(distance_matrix[cluster, :][:, cluster]))
    return clusters, cutoffs


def create_neighbor_matrices(atoms, cutoff):
    distance_matrix = atoms.get_all_distances(mic=False)  # or True?
    neighbor_matrix = distance_matrix < cutoff
    return neighbor_matrix, distance_matrix


def extend_cluster(cluster, order):
    clusters = []
    cluster = tuple(cluster)
    nbody = len(cluster)
    r = order - nbody
    for tup in itertools.combinations_with_replacement(cluster, r):
        new_cluster = sorted(cluster + tup)
        clusters.append(tuple(new_cluster))
    return clusters
