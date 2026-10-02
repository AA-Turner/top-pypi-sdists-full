"""
Assignment of the atoms in an input structure to the sites of a reference structure.
"""

import numpy as np
from ase import Atoms
from ase.geometry import get_distances
from scipy.optimize import linear_sum_assignment

from .validation import (check_matching_boundary_conditions,
                         check_matching_cell_metrics,
                         check_number_of_atoms)

N_MINIMUM_DISTANCES = 3
"""Number of distances to the closest sites that is recorded for each atom. The array
always has this width, so that it does not depend on the size of the reference
structure."""

VACANCY_INDEX = -1
"""Value recorded in the index mapping for a site that no atom was assigned to."""


def match_positions(structure: Atoms, reference: Atoms) -> Atoms:
    """Matches the atoms in the input :attr:`structure` to the sites in the
    :attr:`reference` structure and returns a copy of the :attr:`reference` structure
    in which the chemical species are assigned to comply with the :attr:`structure`.

    Sites to which no atom is assigned are vacant and carry the species ``X``.

    The returned structure carries the supplementary per-atom arrays
    ``Displacement``, ``Displacement_Magnitude``, ``Minimum_Distances`` and
    ``IndexMapping``. Everything that is derived from the mapping, such as the
    relaxation distances and the ambiguities in the assignment, is obtained from those
    arrays by the functions in :mod:`diagnostics`, so this function neither computes
    nor reports it.

    The ``Displacement`` array attached to the returned structure points from the
    ideal reference site to the position of the atom, i.e. it is the displacement
    that the atom underwent relative to the reference site.

    A vacant site carries no displacement and no distances, so ``Displacement``,
    ``Displacement_Magnitude`` and ``Minimum_Distances`` are ``NaN`` there, and
    ``IndexMapping`` is ``-1`` rather than an index into the input structure.

    Parameters
    ----------
    structure
        Structure with relaxed positions.
    reference
        Structure with idealized positions.

    Raises
    ------
    ValueError
        If the periodic boundary conditions of the two input structures do not match.
    ValueError
        If the input structure contains more atoms than the reference structure.
    ValueError
        If the cell metrics of the two input structures do not match.
    """

    check_matching_boundary_conditions(reference, structure, 'relaxed')
    check_number_of_atoms(reference, structure)
    check_matching_cell_metrics(reference, structure)

    # compute displacement vectors and distances between reference and relaxed
    # positions; dvecs[i][j] is the vector from reference site i to atom j
    dvecs, dists = get_distances(reference.positions, structure.positions,
                                 cell=reference.cell, pbc=reference.pbc)
    # pad matrix with zeros to obtain square matrix
    n, m = dists.shape
    cost_matrix = np.pad(dists, ((0, 0), (0, n - m)),
                         mode='constant', constant_values=0)
    # find optimal mapping using Kuhn-Munkres (Hungarian) algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # compile new configuration with supplementary information
    mapped = reference.copy()
    displacement_magnitudes = []
    displacements = []
    minimum_distances = []
    index_mapping = []
    for i, j in zip(row_ind, col_ind):
        atom = mapped[i]
        if j >= len(structure):
            # vacant site in reference structure
            atom.symbol = 'X'
            index_mapping.append(VACANCY_INDEX)
            displacement_magnitudes.append(None)
            displacements.append(3 * [None])
            minimum_distances.append(N_MINIMUM_DISTANCES * [None])
        else:
            atom.symbol = structure[j].symbol
            index_mapping.append(j)
            displacement_magnitudes.append(dists[i, j])
            displacements.append(dvecs[i, j])
            # distances to the three closest sites, irrespective of whether those
            # sites are occupied; padded if the reference has fewer than three sites,
            # so that the array always has the same width
            closest = sorted(dists[:, j])[:N_MINIMUM_DISTANCES]
            closest += [None] * (N_MINIMUM_DISTANCES - len(closest))
            minimum_distances.append(closest)

    # set_array rather than new_array, so that a structure that already carries these
    # arrays, such as one that has been mapped before, can be mapped again
    displacement_magnitudes = np.array(displacement_magnitudes, dtype=np.float64)
    mapped.set_array('Displacement', np.array(displacements, dtype=np.float64),
                     float, shape=(3, ))
    mapped.set_array('Displacement_Magnitude', displacement_magnitudes, float)
    mapped.set_array('Minimum_Distances', np.array(minimum_distances, dtype=np.float64),
                     float, shape=(N_MINIMUM_DISTANCES,))
    mapped.set_array('IndexMapping', np.array(index_mapping, dtype=int), int)

    return mapped
