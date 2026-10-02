# TODO: Docstring all functions
""" This module aims to collect debug functions for various parts of the core

"""
from ase.build import bulk
from ase.calculators.emt import EMT
from ase.neighborlist import NeighborList

from matplotlib import pyplot as plt
import itertools
import numpy as np
import spglib as spg


from .atoms import Atom
from .get_clusters import get_clusters
from ..force_constant_model import ForceConstantModel
from ..cluster_space import ClusterSpace
from .utilities import BiMap
from .tensors import rotation_to_cart_coord, rotate_tensor


def debug_fcm_clusters(fcm, atoms, cutoffs):
    fcm_cluster_list = fcm.cluster_list
    debug_cluster_list = get_clusters(atoms, cutoffs, len(atoms))
#    assert len(fcm_cluster_list) == len(debug_cluster_list), \
#            (len(fcm_cluster_list), len(debug_cluster_list))
    for i, c_fcm in enumerate(fcm_cluster_list):
        c_fcm = sorted(c_fcm)
        if c_fcm not in debug_cluster_list:
            assert False, str(c_fcm) + ' not in debug list'
        for j, c_fcm2 in enumerate(fcm_cluster_list):
            c_fcm2 = sorted(c_fcm2)
            if i == j:
                continue
            assert c_fcm != c_fcm2, (i, j)
    print('All clusters seem to be found!')


def simple_test():
    prim = bulk('Al')
    cs = ClusterSpace(prim, [5, 5])
    atoms = bulk('Al', cubic=True).repeat(3)
    fcm = ForceConstantModel(atoms=atoms, cs=cs)
    atoms.calc = EMT()
    pos = atoms.positions.copy()
    atoms.rattle(0.01)
    disps = atoms.positions - pos
    F = atoms.get_forces().flatten()
    M = fcm.get_fit_matrix(disps)
    a = np.linalg.lstsq(M, F)[0]
    plt.plot(F, np.dot(M, a),  '.')
    plt.savefig('test.pdf')
    return (prim, cs, atoms, fcm)


def validate_cs(cs):

    # Use spglib to try to find a primitive cell
    spg_prim = spg.standardize_cell(cs.primitive_structure, no_idealize=True,
                                    to_primitive=True, symprec=cs.symprec)

    # is the cell a valid cell?
    det = np.linalg.det(cs.primitive_structure.cell.T)
    assert det > 1e-12

    # is the cell the same size as spglibs?
    assert np.isclose(det, np.linalg.det(spg_prim[0].T))

    # is the basis compatible?
    assert sorted(cs.primitive_structure.numbers) == sorted(spg_prim[2])

    assert cs.spacegroup == spg.get_spacegroup(cs.primitive_structure,
                                               symprec=cs.symprec)

    # Is the prim spos within prim cell?
    for spos in cs.primitive_structure.basis:
        for s in spos:
            assert s >= 0 and s < 1-1e-4

    # Did the cs find the correct amount of atoms?
    cutoff = cs.cutoffs.max_cutoff
    nl = NeighborList([cutoff / 2] * len(cs.primitive_structure), skin=0,
                      self_interaction=True, bothways=True)
    nl.update(cs.primitive_structure)
    atom_list = BiMap()
    for i in range(len(cs.primitive_structure)):
        for site, offset in zip(*nl.get_neighbors(i)):
            atom = Atom(site, *offset)
            if atom not in atom_list:
                atom_list.append(atom)
    assert len(cs.atom_list) == len(atom_list)
    for atom in atom_list:
        assert atom in cs.atom_list
    for atom in cs.atom_list:
        assert atom in atom_list

    # Is the first atoms in the atom list the center atoms?
    for i in range(len(cs.primitive_structure)):
        atom = cs.atom_list[i]
        assert atom.site == i and tuple(atom.offset) == (0, 0, 0)

    # Does all clusters contain any of the center atoms?
    prim_set = set(range(len(cs.primitive_structure)))
    for cluster in cs.cluster_list:
        assert not prim_set.isdisjoint(cluster)

    # Does the clusters obey the cutoff
    spos = [atom.spos(cs.primitive_structure.basis) for atom in cs.atom_list]
    pos = [np.dot(spos, cs.primitive_structure.cell) for sp in spos]
    for cluster in cs.cluster_list:
        order = len(cluster)
        nbody = len(set(cluster))
        if nbody == 1:
            continue
        cutoff = cs.cutoffs.get_cutoff(order=order, nbody=nbody)
        for i, j in itertools.combinations(set(cluster), r=2):
            assert np.linalg.norm(pos[i] - pos[j]) < cutoff

    for orbit in cs.orbits:
        prototype_index = orbit.prototype_index
        assert (orbit.orientation_families[0].cluster_indices[0] ==
                prototype_index)
        perm = orbit.orientation_families[0].permutation_indices[0]
        assert cs.permutations[perm] == tuple(range(orbit.order))
        prototype_cluster = cs.cluster_list[prototype_index]
        order = len(prototype_cluster)
        assert orbit.order == order
        prototype_distances = []
        for i, j in itertools.combinations(set(prototype_cluster), r=2):
            distance = np.linalg.norm(pos[i] - pos[j])
            assert distance < orbit.maximum_distance
            prototype_distances.append(distance)
        prototype_distances = sorted(prototype_distances)
        for of in orbit.orientation_families:
            cluster_index = of.cluster_indices[0]
            cluster = cs.cluster_list[cluster_index]
            order = len(cluster)
            assert orbit.order == order
            distances = []
            for i, j in itertools.combinations(set(cluster), r=2):
                distance = np.linalg.norm(pos[i] - pos[j])
                assert distance < orbit.maximum_distance
                distances.append(distance)
            distances = sorted(distances)
            assert np.allclose(distances, prototype_distances)

    for orbit in cs.orbits:
        prototype = cs.cluster_list[orbit.prototype_index]
        assert sorted(prototype) == list(prototype)
        values, positions, counts = np.unique(prototype, return_index=True,
                                              return_counts=True)
        for p, c in zip(positions, counts):
            perm = list(range(len(prototype)))
            for tmp in itertools.permutations(perm[p:p+c]):
                perm = list(range(len(prototype)))
                perm[p:p+c] = tmp
                for et in orbit.eigentensors:
                    assert np.allclose(et, et.transpose(perm))

    for orbit in cs.orbits:
        for ri, pi in orbit.eigensymmetries:
            R_scaled = cs.rotation_matrices[ri]
            R = rotation_to_cart_coord(R_scaled, cs.primitive_structure.cell)
            R_inv = np.linalg.inv(R)
            perm = cs.permutations[pi]
            for et in orbit.eigentensors:
                assert np.allclose(rotate_tensor(et, R_inv).transpose(perm),
                                   et)

    nirred = cs._cvs.shape[1]
    irred = np.random.random(nirred)
    params = cs._map_parameters(irred)
    i = 0
    for orb in cs.orbits:
        for of in orb.orientation_families:
            fc = np.zeros([3]*orb.order)
            for j, et in enumerate(of.eigentensors):
                fc += et * params[i+j]
            of.force_constant = fc
        i += len(orb.eigentensors)

    lookup = dict()
    for orbit in cs.orbits:
        for of in orbit.orientation_families:
            fc = of.force_constant
            for ci, pi in zip(of.cluster_indices, of.permutation_indices):
                cluster = cs.cluster_list[ci]
                perm = cs.permutations[pi]
                lookup[tuple(cluster)] = fc.transpose(perm)

#    previous_cluster_prefix = None
    for order in cs.cutoffs.orders:
        for pre in range(len(cs.primitive_structure)):
            for body in itertools.combinations_with_replacement(
                    range(pre, len(cs.atom_list)), r=order-2):
                cluster = [pre] + list(body) + [None]
                FC = np.zeros([3]*order)
                for i in range(len(cs.atom_list)):
                    cluster[-1] = i
                    inv_perm = np.argsort(np.argsort(cluster))
                    fc = lookup.get(tuple(sorted(cluster)))
                    if fc is None:
                        continue
                    FC += fc.transpose(inv_perm)
                assert np.allclose(FC, 0), FC.round(8)

    for orbit in cs.orbits:
        prototype = cs.cluster_list[orbit.prototype_index]
        FC = lookup[tuple(prototype)]
        for of in orbit.orientation_families:
            R_scaled = cs.rotation_matrices[of.symmetry_index]
            R = rotation_to_cart_coord(R_scaled, cs.primitive_structure.cell)
            R_inv = np.linalg.inv(R)
            assert np.allclose(rotate_tensor(FC, R_inv), of.force_constant)
