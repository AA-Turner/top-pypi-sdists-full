from ase.calculators.calculator import Calculator, all_changes
from ase.neighborlist import NeighborList
import numpy as np

import numba
from numba.typed import List


alpha = 1 / 137.035999046  # no unit
hbar = 6.582119569e-16  # eV * s
c = 299792458 * 1e10  # m/s * A/m
prefactor = alpha * hbar * c  # eV * A


@numba.njit
def a(Z_i, Z_j):
    return 0.46850 / (Z_i**0.23 + Z_j**0.23)


@numba.njit
def phi(x):
    return (0.18175 * np.exp(-3.19980 * x)
            + 0.50986 * np.exp(-0.94229 * x)
            + 0.28022 * np.exp(-0.40290 * x)
            + 0.02817 * np.exp(-0.20162 * x))


@numba.njit
def phi_derivative(x):
    return (- 3.19980 * 0.18175 * np.exp(-3.19980 * x)
            - 0.94229 * 0.50986 * np.exp(-0.94229 * x)
            - 0.40290 * 0.28022 * np.exp(-0.40290 * x)
            - 0.20162 * 0.02817 * np.exp(-0.20162 * x))


@numba.njit
def zbl_energy(Z_i, Z_j, r_ij):
    return prefactor * Z_i * Z_j / r_ij * phi(r_ij / a(Z_i, Z_j))


@numba.njit
def zbl_force(Z_i, Z_j, r_ij):
    return (-prefactor
            * (Z_i * Z_j)
            * (phi_derivative(r_ij / a(Z_i, Z_j)) / (r_ij * a(Z_i, Z_j))
               - phi(r_ij / a(Z_i, Z_j)) / r_ij**2))


@numba.njit
def np_linalg_norm_axis1(mat):
    norm = np.empty(len(mat), dtype=np.float64)
    for i in range(len(mat)):
        norm[i] = np.linalg.norm(mat[i])
    return norm


@numba.njit
def inner_loop(ai, positions, cell, offsets, neighbors, forces, energy, numbers):
    cells = np.dot(offsets, cell)
    v_ij = positions[neighbors] + cells - positions[ai]
    r_ij = np_linalg_norm_axis1(v_ij)
    for aj, v, r in zip(neighbors, v_ij, r_ij):
        energy[0] += zbl_energy(numbers[ai], numbers[aj], r)
        force_j = v / r * zbl_force(numbers[ai], numbers[aj], r)
        forces[aj] += force_j
        forces[ai] -= force_j


@numba.njit
def outer_loop(positions, cell, offsets_list, neighbors_list, forces, energy, numbers):
    for ai in range(len(positions)):
        neighbors = neighbors_list[ai]
        offsets = offsets_list[ai]
        inner_loop(ai, positions, cell, offsets, neighbors, forces, energy, numbers)


class ZBLCalculator(Calculator):
    implemented_properties = ['energy', 'forces']

    def __init__(self, cutoff, skin=1.0, **kwargs):
        self._cutoff = cutoff
        self._skin = skin
        super().__init__(**kwargs)

    def calculate(self, atoms=None, properties=['energy'],
                  system_changes=all_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

        if not ('forces' in properties or 'energy' in properties):
            return

        n_atoms = len(self.atoms)

        if 'numbers' in system_changes:
            self.nl = NeighborList([self._cutoff / 2] * n_atoms,
                                   self_interaction=False,
                                   skin=self._skin)

        self.nl.update(self.atoms)

        positions = self.atoms.positions
        numbers = self.atoms.numbers
        cell = self.atoms.cell.array

        neighbors_list, offsets_list = List(), List()
        for ai in range(n_atoms):
            neighbors, offsets = self.nl.get_neighbors(ai)
            neighbors_list.append(neighbors)
            offsets_list.append(offsets.astype(np.float64))

        energy = np.array([0.0])
        forces = np.zeros((n_atoms, 3))

        outer_loop(positions, cell, offsets_list, neighbors_list, forces, energy, numbers)

        self.results['energy'] = energy[0]
        self.results['forces'] = forces
