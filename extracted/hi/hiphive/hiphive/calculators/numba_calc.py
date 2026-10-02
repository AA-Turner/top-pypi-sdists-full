import numba
import numpy as np


@numba.jit(nopython=True)
def _get_forces(clusters, force_constants,
                atom_indices_list, atom_positions_list, atom_counts_list,
                prefactors_list,
                nbody, order,
                forces, E,
                displacements):
    fc_tmp = np.zeros(3**order)
    fc = np.zeros(3**order)
    forces_tmp = np.zeros(forces.shape)
    f = np.zeros(3)
    for i in range(len(clusters)):
        cluster = clusters[i]
        fc[:] = force_constants[i].flat
        atom_positions = atom_positions_list[i]
        prefactors = prefactors_list[i]
        cluster_force_contribution(atom_positions, prefactors, nbody,
                                   fc_tmp, fc, order,
                                   displacements,
                                   cluster, f, forces_tmp)
    forces += forces_tmp
    E_tmp = 0
    for atom_index in range(len(forces_tmp)):
        E_tmp += np.dot(forces_tmp[atom_index], displacements[atom_index])
    E -= E_tmp / order


def cluster_force_contribution_einsum(positions, prefactors, numbers,
                                      fc_tmp, fc, order,
                                      disps,
                                      cluster, f, F):
    fc = fc.reshape((3,)*order)
    for p, pf in zip(positions, prefactors):
        t = [fc, list(range(order))]
        for i, a in enumerate(cluster):
            if i == p:
                continue
            t.append(disps[a])
            t.append([i])
        F[cluster[p], :] += pf * np.einsum(*t)


try:
    import numba

    @numba.jit(nopython=True)
    def tvl(fc, v, order):
        """Contracts a 3-dim tensor of rank n with a 3-dim vector from the left
        """
        t = 3**(order-1)
        fc[0:t] *= v[0]
        fc[t:2*t] *= v[1]
        fc[2*t:3*t] *= v[2]
        fc[0:t] = fc[0:t] + fc[t:2*t] + fc[2*t:3*t]

    @numba.jit(nopython=True)
    def tvr(fc, v, order):
        for i in range(3**(order-1)):
            t = 3*i
            fc[i] = fc[t]*v[0]+fc[t+1]*v[1]+fc[t+2]*v[2]

    @numba.jit(nopython=True)
    def contraction(fc, d, cluster, pos, order, prefac, f):
        i = 0
        for m in range(pos):
            v = d[cluster[m], :]
            tvl(fc, v, order - i)
            i += 1
        for r in range(order - pos - 1):
            v = d[cluster[order - r - 1], :]
            tvr(fc, v, order - i)
            i += 1
        f[0] = fc[0] * prefac
        f[1] = fc[1] * prefac
        f[2] = fc[2] * prefac

    @numba.jit(nopython=True)
    def cluster_force_contribution_numba(positions, prefactors, numbers,
                                         fc_tmp, fc, order,
                                         disps,
                                         cluster, f, F):
        for i in range(numbers):
            pos = positions[i]
            prefac = prefactors[i]
            for j in range(3**order):
                fc_tmp[j] = fc[j]
            contraction(fc_tmp, disps,
                        cluster, pos, order, prefac, f)
            a = cluster[pos]
            F[a, 0] += f[0]
            F[a, 1] += f[1]
            F[a, 2] += f[2]

    @numba.jit(nopython=True)
    def clusters_force_contribution_numba(positions, prefactors, numbers,
                                          fc_tmp, fc, order,
                                          disps,
                                          clusters, f, F):
        for i in range(clusters.shape[0]):
            cluster = clusters[i, :]
            cluster_force_contribution_numba(positions, prefactors, numbers,
                                             fc_tmp, fc, order,
                                             disps,
                                             cluster, f, F)

    cluster_force_contribution = cluster_force_contribution_numba
    clusters_force_contribution = clusters_force_contribution_numba

except ImportError:

    cluster_force_contribution = cluster_force_contribution_einsum
