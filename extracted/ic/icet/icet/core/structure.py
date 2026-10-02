"""
This module provides the helpers through which structures cross the boundary
to the compiled core.
The core does not expose a structure class.
A structure enters a binding as plain arrays, namely positions, atomic
numbers, cell metric, and periodic boundary conditions, and comes back as a
dictionary of the same arrays.
"""
import numpy as np
from ase import Atoms

import _icet
from .lattice_site import LatticeSite


def structure_to_arrays(structure: Atoms) -> dict:
    """
    Returns the plain arrays that describe a structure, keyed as the bindings
    of the compiled core name them, so that a call site can unpack them as
    keyword arguments.

    Parameters
    ----------
    structure
        Atomic configuration.
    """
    return dict(positions=np.array(structure.positions, dtype=float),
                atomic_numbers=structure.get_atomic_numbers(),
                cell=np.array(structure.cell),
                pbc=structure.pbc.tolist())


def atoms_from_structure_data(data: dict) -> Atoms:
    """
    Returns the structure described by a dictionary of plain arrays, as
    returned by the bindings of the compiled core, as an
    :class:`Atoms <ase.Atoms>` object.

    Parameters
    ----------
    data
        Dictionary with the keys ``positions``, ``atomic_numbers``, ``cell``,
        and ``pbc``.
    """
    return Atoms(positions=data['positions'],
                 numbers=data['atomic_numbers'],
                 cell=data['cell'],
                 pbc=data['pbc'])


def find_lattice_sites_by_positions(structure: Atoms,
                                    positions: list,
                                    fractional_position_tolerance: float) -> list[LatticeSite]:
    """
    Returns the lattice sites of a structure that match the given positions.
    Each lattice site pairs the index of a site of the structure with the
    offset of the unit cell in which the matched position sits.

    Parameters
    ----------
    structure
        Atomic configuration, typically a primitive structure.
    positions
        Positions to match, in Cartesian coordinates.
    fractional_position_tolerance
        Tolerance applied when comparing positions in fractional coordinates.
    """
    return _icet.find_lattice_sites_by_positions(
        positions=np.array(structure.positions, dtype=float),
        cell=np.array(structure.cell),
        pbc=structure.pbc.tolist(),
        query_positions=np.reshape(positions, (-1, 3)),
        fractional_position_tolerance=fractional_position_tolerance)
