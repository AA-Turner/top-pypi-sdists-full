import numpy as np
from itertools import permutations, product


def write_fcs_gpumd(fname_fc: str,
                    fname_clusters: str,
                    fcs,
                    order: int,
                    tol: float = 1e-10):
    """
    Writes force constants of given order in GPUMD format.

    Parameters
    ----------
    fname_fc
        name of file which contains the lookup force constants
    fname_clusters
        name of file which contains the clusters and the force constant lookup index
    fcs
        force constants
    order
        force constants for this order will be written to file
    tol
        if the norm of a force constant term is less than this value it will be excluded
        from the output;
        if two force-constants differ by this value or less, they are considered equal.
    """
    cluster_lookup, fc_lookup = _get_lookup_data_smart(fcs, order, tol)
    _write_clusters(fname_clusters, cluster_lookup, order)
    _write_fc_lookup(fname_fc, fc_lookup, order)


def _write_fc_lookup(fname, fc_lookup, order):
    """ Writes the lookup force constants to file """
    fmt = '{}' + ' {}'*order
    with open(fname, 'w') as f:
        f.write(str(len(fc_lookup)) + '\n\n')
        for fc in fc_lookup:
            for xyz in product(range(3), repeat=order):
                f.write(fmt.format(*xyz, fc[xyz])+'\n')
            f.write('\n')


def _write_clusters(fname, cluster_lookup, order):
    """ Writes the cluster lookup to file """
    fmt = '{}' + ' {}'*order
    with open(fname, 'w') as f:
        f.write(str(len(cluster_lookup)) + '\n\n')
        for c, i in cluster_lookup.items():
            line = fmt.format(*c, i) + '\n'
            f.write(line)


def _get_clusters(fcs,
                  order: int,
                  tol: float):
    """ Collect all relevant clusters; for 2nd and 3rd-order force constants
    all permutations are included.
    """
    if order in [2, 3]:
        clusters = []
        for c in fcs._fc_dict.keys():
            if len(c) == order and np.linalg.norm(fcs[c]) > tol:
                for ci in permutations(c):
                    clusters.append(ci)
        clusters = list(sorted(set(clusters)))
    else:
        clusters = [c for c in fcs._fc_dict.keys() if len(c) == order and np.linalg.norm(fcs[c]) > tol]  # noqa
    return clusters


def _get_lookup_data_naive(fcs,
                           order: int,
                           tol: float):
    """ Groups force constants for a given order into groups for which the
    force constant is identical. """
    fc_lookup = []
    cluster_lookup = dict()

    clusters = _get_clusters(fcs, order, tol)

    for c in clusters:
        fc1 = fcs[c]
        if np.linalg.norm(fc1) < tol:
            continue
        for i, fc2 in enumerate(fc_lookup):
            if np.linalg.norm(fc1 - fc2) < tol:
                cluster_lookup[c] = i
                break
        else:
            cluster_lookup[c] = len(fc_lookup)
            fc_lookup.append(fc1)
    return cluster_lookup, fc_lookup


def _get_lookup_data_smart(fcs,
                           order: int,
                           tol: float):
    """ Groups force constants for a given order into groups for which the
    force constant is identical. """
    fc_lookup = []
    cluster_lookup = dict()
    axis = tuple(range(1, order+1))

    clusters = _get_clusters(fcs, order, tol)
    fc_all = np.array([fcs[c] for c in clusters])

    indices = list(range(len(clusters)))
    while len(indices) > 0:
        i = indices[0]
        delta = fc_all[indices] - fc_all[i]
        delta_norm = np.sqrt(np.sum(delta**2, axis=axis))

        inds_to_del = [indices[x] for x in np.where(delta_norm < tol)[0]]
        assert i in inds_to_del

        fc_lookup.append(fc_all[i])
        for j in inds_to_del:
            indices.remove(j)
            cluster_lookup[clusters[j]] = len(fc_lookup)-1
    return cluster_lookup, fc_lookup


def write_fcp_txt(fname: str,
                  path: str,
                  n_types: int,
                  max_order: int,
                  heat_current_order: int = 2):
    """ Write driver potential file for GPUMD.

    Parameters
    ----------
    fname
        file name
    path
        path to directory with force constant file
    n_types
        number of atom types
    max_order
        maximum order of the force constant potential
    heat_current_order
        heat current order used in thermal conductivity


    Format is a simple file containing the following

    fcp number_of_atom_types
    highest_force_order heat_current_order
    path_to_force_constant_files

    which in practice for a binary system with a sixth order model,
    consider third-order heat-currents, would mean

    fcp 2
    6 3
    /path/to/your/folder
    """

    with open(fname, 'w') as f:
        f.write('fcp {}\n'.format(n_types))
        f.write('{} {}\n'.format(max_order, heat_current_order))
        f.write('{}'.format(path.rstrip('/')))  # without a trailing '/'


def write_r0(fname, atoms):
    """
    Write GPUMD r0 file, with reference atomic positions.

    Parameters
    ----------
    fname : str
        name of file to which to write the atomic positions
    atoms : ase.Atoms
        input structure

    """
    line = '{} {} {}\n'
    with open(fname, 'w') as f:
        for a in atoms:
            f.write(line.format(*a.position))
