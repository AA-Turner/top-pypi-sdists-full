"""
Consistency checks shared by the steps of the structure mapping algorithm.

Each check raises :class:`ValueError` with a message that names the offending
quantity for both structures involved.
"""

import numpy as np
from ase import Atoms


def check_matching_boundary_conditions(reference: Atoms,
                                       structure: Atoms,
                                       structure_name: str = 'input') -> None:
    """Checks that the periodic boundary conditions of the two structures agree.

    Parameters
    ----------
    reference
        Structure with idealized positions.
    structure
        Structure to compare with the reference structure.
    structure_name
        Name used for :attr:`structure` in the error message.

    Raises
    ------
    ValueError
        If the boundary conditions of the two structures do not match.
    """
    if not np.all(reference.pbc == structure.pbc):
        msg = ('The boundary conditions of reference and {} structures do not '
               'match.'.format(structure_name))
        msg += '\n  reference: ' + str(reference.pbc)
        msg += '\n  {}: '.format(structure_name) + str(structure.pbc)
        raise ValueError(msg)


def check_matching_cell_metrics(reference: Atoms, structure: Atoms) -> None:
    """Checks that the cell metrics of the two structures agree.

    Parameters
    ----------
    reference
        Structure with idealized positions.
    structure
        Structure with relaxed positions.

    Raises
    ------
    ValueError
        If the cell metrics of the two structures do not match.
    """
    if not np.all(np.isclose(reference.cell, structure.cell)):
        msg = 'The cell metrics of reference and relaxed structures do not match.'
        msg += '\n  reference: ' + str(reference.cell)
        msg += '\n  relaxed: ' + str(structure.cell)
        raise ValueError(msg)


def check_cell_is_full_rank(structure: Atoms, structure_name: str = 'input') -> None:
    """Checks that the cell of a structure spans three dimensions.

    The criterion is the rank of the cell rather than the boundary conditions, since a
    slab or a wire with vacuum along the non-periodic directions has a cell of full
    rank and can be mapped.

    Parameters
    ----------
    structure
        Structure whose cell is checked.
    structure_name
        Name used for :attr:`structure` in the error message.

    Raises
    ------
    ValueError
        If the cell does not span three dimensions.
    """
    if structure.cell.rank < 3:
        msg = ('The cell of the {} structure does not span three dimensions, so the '
               'volume and the transformation matrix are undefined.'.format(structure_name))
        msg += '\n  cell:\n' + str(structure.cell)
        msg += ('\n  A structure that is not periodic along one or more directions has to be '
                'given a cell with vacuum along those directions.')
        raise ValueError(msg)


def check_structure_is_not_empty(structure: Atoms, structure_name: str = 'input') -> None:
    """Checks that a structure contains at least one atom.

    Parameters
    ----------
    structure
        Structure that is checked.
    structure_name
        Name used for :attr:`structure` in the error message.

    Raises
    ------
    ValueError
        If the structure contains no atoms.
    """
    if len(structure) == 0:
        raise ValueError('The {} structure contains no atoms.'.format(structure_name))


def check_tol_cell(tol_cell: float) -> None:
    """Checks that the tolerance on the cell metric lies between zero and one.

    The bounds within which candidate transformation matrices are sought scale as
    ``1 / (1 - tol_cell)``, which is the largest factor by which a cell vector of the
    reference structure can be stretched, so the search is only defined below unity. A
    tolerance of one would admit a cell vector of any length.

    Parameters
    ----------
    tol_cell
        Tolerance for the deviation of the cell metric of the input structure from an
        integer transformation of the reference cell metric.

    Raises
    ------
    ValueError
        If the tolerance does not lie between zero and one.
    """
    if not 0 < tol_cell < 1:
        raise ValueError('tol_cell has to lie between zero and one, it is {}.'.format(tol_cell))


def check_periodicity_is_sufficient(reference: Atoms) -> None:
    """Checks that the reference structure is periodic along at least two directions.

    Fewer than two periodic directions leave the orientation of a structure undetermined by its
    cell. A structure periodic along one direction only is unchanged, as far as its cell is
    concerned, by a rotation about that direction: the periodic cell vector is invariant under
    such a rotation and the other two describe empty space. A structure periodic along no
    direction has no cell vector that means anything at all. There is then no rotation to
    reduce over the symmetry of the reference structure and no way to bring the atoms into the
    frame of the sites, so such a structure is rejected rather than mapped on terms that cannot
    be met.

    Parameters
    ----------
    reference
        Reference structure, which sets the boundary conditions for the mapping.

    Raises
    ------
    ValueError
        If fewer than two directions are periodic.
    """
    n_periodic = int(np.count_nonzero(reference.pbc))
    if n_periodic < 2:
        msg = ('A structure has to be periodic along at least two directions to be mapped, '
               'and this one is periodic along {}.'.format(n_periodic))
        msg += '\n  boundary conditions: ' + str(reference.pbc)
        msg += ('\n  With fewer the cell does not determine the orientation of the structure, '
                'since a rotation that only moves the directions that are not periodic leaves '
                'the cell as it was.')
        raise ValueError(msg)


def check_inert_species(structure: Atoms,
                        reference: Atoms,
                        inert_species: list[str]) -> None:
    """Checks that the species that are never substituted for a vacancy can be counted in
    both structures.

    The number of sites occupied by these species is used to rescale the volume, so each of
    the two structures has to contain at least one of them, or the scaling factor would
    follow from a division by zero. An individual species may be absent from one of the two,
    which is what allows a species that substitutes for another, as in an alloy, to be given
    as inert. A species that occurs in neither structure is a mistake rather than a choice
    and is reported as one.

    Parameters
    ----------
    structure
        Input structure.
    reference
        Reference structure.
    inert_species
        Chemical symbols that are never substituted for a vacancy.

    Raises
    ------
    ValueError
        If none of the species occurs in one of the structures, or if a species occurs in
        neither of them.
    """
    symbols_structure = structure.get_chemical_symbols()
    symbols_reference = reference.get_chemical_symbols()

    unknown = [species for species in inert_species
               if species not in symbols_structure and species not in symbols_reference]
    if unknown:
        msg = ('The following species given as inert do not occur in either structure: '
               '{}.'.format(', '.join(unknown)))
        msg += '\n  species in the input structure: ' + ', '.join(sorted(set(symbols_structure)))
        msg += '\n  species in the reference structure: ' + ', '.join(
            sorted(set(symbols_reference)))
        raise ValueError(msg)

    for symbols, name in ((symbols_reference, 'reference'), (symbols_structure, 'input')):
        if not any(symbols.count(species) for species in inert_species):
            msg = ('None of the species given as inert occurs in the {} structure, so the '
                   'volume cannot be rescaled.'.format(name))
            msg += '\n  inert species: ' + ', '.join(inert_species)
            msg += '\n  species in the {} structure: '.format(name)
            msg += ', '.join(sorted(set(symbols)))
            raise ValueError(msg)


def check_number_of_atoms(reference: Atoms, structure: Atoms) -> None:
    """Checks that the relaxed structure does not contain more atoms than there
    are sites in the reference structure.

    Parameters
    ----------
    reference
        Structure with idealized positions.
    structure
        Structure with relaxed positions.

    Raises
    ------
    ValueError
        If the relaxed structure contains more atoms than the reference
        structure.
    """
    if len(structure) > len(reference):
        msg = 'The relaxed structure contains more atoms than the reference structure.'
        msg += '\n  reference: ' + str(len(reference))
        msg += '\n  relaxed: ' + str(len(structure))
        msg += ('\n  There is no site for every atom. If the input structure contains '
                'vacancies, the size of the reference supercell cannot be determined from '
                'the volume per atom alone, and inert_species has to be given, or '
                'assume_no_cell_relaxation set if there is no sublattice without vacancies.')
        msg += ('\n  If the input structure instead contains interstitial atoms, the '
                'interstitial sites have to be part of the reference structure; sites that '
                'are not occupied then come out as vacancies.')
        raise ValueError(msg)
