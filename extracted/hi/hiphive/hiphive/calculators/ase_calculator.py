"""Contains a calculator which given an arbitrary list of clusters and
associated force constants can calculate the energy and forces of a displaced
system
"""
import math
from collections import defaultdict as dd
from typing import List, Tuple

import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from hiphive.force_constants import SortedForceConstants
from hiphive.utilities import get_displacements
from .numba_calc import _get_forces


class ForceConstantCalculator(Calculator):
    """This class provides an ASE calculator that can be used in conjunction
    with integrators and optimizers with the `atomic simulation environment
    (ASE) <https://wiki.fysik.dtu.dk/ase/index.html>`_. To initialize an object
    of this class one must provide the ideal atomic configuration along with a
    compatible force constant model.

    Parameters
    -----------
    fcs : ForceConstants
        the force constants instance must include the atomic configuration
    max_disp : float
        maximum allowed displacement before calculator raises ValueError
    """

    implemented_properties = ['energy', 'forces']

    def __init__(self, fcs: SortedForceConstants, max_disp: float = 3.0):
        Calculator.__init__(self)

        if not isinstance(fcs, SortedForceConstants):
            raise TypeError('The FC calculator requires sorted FCs.')
        self.atoms_ideal = fcs.supercell.copy()

        # Nearest neighbor distance used as maximum displacement allowed,
        # stops exploding MD simulations.
        self.max_allowed_disp = max_disp

        self.clusters = dd(list)
        self.force_constants = dd(list)
        self.atom_indices = dd(list)
        self.atom_positions = dd(list)
        self.atom_counts = dd(list)
        self.prefactors = dd(list)
        # The main idea is to precompute the prefactor and multiplicities of
        # belonging to each cluster
        for cluster, fc in fcs.get_fc_dict().items():
            argsort = np.argsort(cluster)  # TODO: is already True?
            cluster = np.array(sorted(cluster))
            nbody = len(set(cluster))
            order = len(cluster)
            key = (nbody, order)
            self.clusters[key].append(cluster)
            assert fc.shape == (3,) * order
            self.force_constants[key].append(fc.transpose(argsort))
            unique = np.unique(cluster, return_index=True, return_counts=True)
            self.atom_indices[key].append(unique[0])
            self.atom_positions[key].append(unique[1])
            self.atom_counts[key].append(unique[2])
            prefac = [-count/np.prod(list(map(math.factorial, unique[2]))) for count in unique[2]]
            self.prefactors[key].append(prefac)
        for d in [self.clusters,
                  self.force_constants,
                  self.atom_indices,
                  self.atom_positions,
                  self.atom_counts,
                  self.prefactors,
                  ]:
            for k, v in d.items():
                d[k] = np.array(v)

    def calculate(self, atoms: Atoms = None,
                  properties: List[str] = ['energy'],
                  system_changes: List[str] = all_changes) -> None:
        Calculator.calculate(self, atoms, properties, system_changes)
        self._check_atoms()
        self._compute_displacements()

        if 'forces' in properties or 'energy' in properties:
            E, forces = self.compute_energy_and_forces()
            self.results['forces'] = forces
            self.results['energy'] = E

    def _check_atoms(self) -> None:
        """Checks that the atomic configuration, with which the calculator is
        associated, is compatible with the ideal configuration provided during
        initialization."""
        if len(self.atoms) != len(self.atoms_ideal):
            raise ValueError('Length of atoms does not match reference structure')
        if not all(self.atoms.numbers == self.atoms_ideal.numbers):
            raise ValueError('Atomic numbers do not match reference structure')

    def _compute_displacements(self) -> None:
        """Evaluates the atomic displacements between the current and the ideal
        (reference) configuration."""
        self.displacements = get_displacements(self.atoms, self.atoms_ideal)

        # sanity check that displacements are not too large
        max_disp = np.max(np.linalg.norm(self.displacements, axis=1))
        if max_disp > self.max_allowed_disp:
            msg = 'Displacement {:.5f} larger than maximum allowed displacement {:.5f}'
            raise ValueError(msg.format(max_disp, self.max_allowed_disp))

    def compute_energy_and_forces(self) -> Tuple[float, list]:
        """Computes energy and forces.

        Returns
        -------
        float, list(list(float))
            energy and forces
        """
        E = np.zeros(1)
        forces = np.zeros((len(self.atoms), 3))

        for key in self.clusters.keys():
            nbody = key[0]
            order = key[1]
            _get_forces(self.clusters[key],
                        self.force_constants[key],
                        self.atom_indices[key],
                        self.atom_positions[key],
                        self.atom_counts[key],
                        self.prefactors[key],
                        nbody, order,
                        forces, E, self.displacements)
        return float(E[0]), forces

    def __repr__(self) -> str:
        fc_dict_str = '{{{}: {}, ...}}'.format(self.clusters[0], self.force_constants[0])
        fcs_str = 'ForceConstants(fc_dict={}, atoms={!r})'.format(fc_dict_str, self.atoms_ideal)
        return 'ForceConstantCalculator({})'.format(fcs_str)
