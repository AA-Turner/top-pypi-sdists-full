"""
Determination of the reference supercell that corresponds to an input structure.

This module decides how the input structure is related to the reference
structure, i.e. which supercell of the reference structure the input structure
is to be mapped onto.
"""

import numpy as np
from ase import Atoms
from ase.build import make_supercell

from icet.input_output.logging_tools import logger
from .candidate_search import (find_transformation_matrix, get_minimum_site_distance,
                               get_position_residuals, get_residual_strain)
from .validation import (check_cell_is_full_rank,
                         check_inert_species,
                         check_matching_boundary_conditions,
                         check_periodicity_is_sufficient,
                         check_structure_is_not_empty,
                         check_tol_cell)

DEFAULT_TOL_CELL = 0.25
"""Default tolerance for the deviation of the cell metric of the input structure
from an integer transformation of the reference cell metric."""

FAST_PATH_MAX_RESIDUAL_FRACTION = 0.15
"""Mean distance between the atoms and the sites, as a fraction of the distance between
neighboring sites, at which a rounded transformation matrix is accepted without more ado.

A structure that is merely strained and rattled sits well inside this, leaving the atoms less
than a tenth of that distance from the sites, whereas the rotated structures that rounding
gets wrong leave them nearly a quarter of it away. Above the bar the search is run as well and
the better of the two kept, which costs time but cannot give a worse answer than either
alone."""

FAST_PATH_REPLACEMENT_MARGIN = 0.9
"""Fraction of the rounded matrix score that the search has to beat before it replaces it.

Several matrices describe the same supercell, so where the two agree the rounded one is kept:
it is the one in the setting of the reference structure, and swapping an equivalent
description in for no gain would make the supercell that is returned depend on which route
happened to be taken."""

DEFAULT_TOL_POSITIONS = 1e-4
"""Default tolerance in Ångstrom applied when scanning for overlapping positions.

Defined here rather than on the public function so that the two cannot diverge."""


def get_periodic_measure(cell: np.ndarray, periodic: np.ndarray) -> float:
    """Returns the volume of the subspace spanned by the periodic cell vectors.

    This is the volume of the cell if all three directions are periodic, the area of the
    base if two are, and a length if one is. It is the quantity that stands in for the
    volume whenever a structure is not periodic along every direction, since the extent of
    the cell along a direction that is not periodic is arbitrary.

    Parameters
    ----------
    cell
        Cell metric (row-major format).
    periodic
        Boolean mask marking the periodic directions.
    """
    rows = np.asarray(cell, dtype=np.float64)[np.asarray(periodic, dtype=bool)]
    return float(np.sqrt(np.linalg.det(np.dot(rows, rows.T))))


def get_volume_scaled_cell(structure: Atoms,
                           reference: Atoms,
                           inert_species: list[str] | None = None) -> np.ndarray:
    """Returns the cell metric of the input structure rescaled such that the measure of
    its periodic subspace per atom matches that of the reference structure.

    That measure is the volume when all three directions are periodic and an area or a
    length otherwise, and only the periodic cell vectors are rescaled. Were the volume used
    for a slab, adding vacuum would change the scaling and with it the transformation matrix
    that is inferred, although nothing about the slab itself had changed.

    Parameters
    ----------
    structure
        Input structure, typically a relaxed structure.
    reference
        Reference structure, which can but need not be the primitive structure.
    inert_species
        List of chemical symbols (e.g., ``['Au', 'Pd']``) that are never
        substituted for a vacancy. If provided, only the sites occupied by
        these species are counted.
    """
    if inert_species is None:
        n_reference = len(reference)
        n_structure = len(structure)
    else:
        symbols_reference = reference.get_chemical_symbols()
        symbols_structure = structure.get_chemical_symbols()
        n_reference = sum([symbols_reference.count(s) for s in inert_species])
        n_structure = sum([symbols_structure.count(s) for s in inert_species])

    periodic = np.asarray(reference.pbc, dtype=bool)
    n_periodic = int(periodic.sum())
    if n_periodic == 0:
        logger.debug('No direction is periodic, so the cell of the input structure is left '
                     'as it is')
        return np.array(structure.cell, dtype=np.float64)

    volume_scaling = get_periodic_measure(reference.cell, periodic) / n_reference
    volume_scaling /= get_periodic_measure(structure.cell, periodic) / n_structure

    logger.debug('Rescaling the cell of the input structure by a factor of {:.6f} along {} '
                 'periodic direction(s), counting {} of {} sites in the reference structure '
                 'and {} of {} atoms in the input structure{}'.format(
                     volume_scaling ** (1 / n_periodic), n_periodic,
                     n_reference, len(reference), n_structure, len(structure),
                     '' if inert_species is None
                     else ' (inert species: {})'.format(', '.join(inert_species))))

    scaled = np.array(structure.cell, dtype=np.float64)
    scaled[periodic] *= volume_scaling ** (1 / n_periodic)
    return scaled


def check_transformation_matrix(P: np.ndarray,
                                structure_cell: np.ndarray,
                                reference_cell: np.ndarray,
                                tol_cell: float = DEFAULT_TOL_CELL,
                                pbc: np.ndarray = None) -> None:
    """Checks that an integer transformation matrix reproduces the cell metric of
    the input structure.

    The residual is measured as the largest absolute eigenvalue of the Biot strain
    tensor that relates the transformed reference cell to the cell of the input
    structure, over the subspace spanned by the periodic cell vectors. That measure
    is invariant under a rotation of either cell, it does not depend on the size of
    the cells, and it does not depend on the cell vectors along the directions that
    are not periodic, whose extent is arbitrary.

    Parameters
    ----------
    P
        Integer transformation matrix.
    structure_cell
        Cell metric of the input structure, rescaled if applicable.
    reference_cell
        Cell metric of the reference structure.
    tol_cell
        Largest acceptable residual strain.
    pbc
        Boundary conditions. A direction that is not periodic contributes no strain.

    Raises
    ------
    ValueError
        If the transformation matrix is singular or changes the handedness of the
        cell.
    ValueError
        If the residual strain exceeds :attr:`tol_cell`.
    """
    determinant = np.linalg.det(P)
    if determinant < 0.5:
        msg = ('The transformation matrix relating the input structure to the reference '
               'structure is singular or reverses the handedness of the cell.')
        msg += '\n  transformation matrix:\n' + str(P)
        msg += '\n  determinant: ' + str(determinant)
        raise ValueError(msg)

    residual = get_residual_strain(P, structure_cell, reference_cell, pbc)
    if residual > tol_cell:
        msg = ('The cell metric of the input structure cannot be reconciled with an integer '
               'transformation of the reference cell metric.')
        msg += '\n  largest residual strain: {:.5f}'.format(residual)
        msg += '\n  tol_cell: ' + str(tol_cell)
        msg += '\n  transformation matrix:\n' + str(P)
        msg += ('\n  The input structure may be rotated relative to the reference structure, '
                'or it may not be a supercell of it.')
        msg += '\n  For a strongly strained input structure tol_cell can be increased.'
        raise ValueError(msg)


def _get_transformation_matrix(structure: Atoms,
                               reference: Atoms,
                               scaled_structure_cell: np.ndarray,
                               tol_cell: float,
                               symprec: float) -> tuple[np.ndarray, np.ndarray]:
    """Returns the integer transformation matrix relating the input structure to
    the reference structure, together with the rigid offset in reduced coordinates
    that brings the positions closest to the sites.

    Rounding the real transformation matrix is tried first, which is sufficient
    unless the input structure is strongly rotated relative to the reference
    structure. Only if that fails is the matrix searched for, which is more
    expensive.
    """
    reference_cell = np.asarray(reference.cell, dtype=np.float64)
    periodic = np.asarray(reference.pbc, dtype=bool)
    P = np.around(np.dot(scaled_structure_cell, np.linalg.inv(reference_cell)))
    # a direction that is not periodic is fixed rather than rounded, as it is in the search.
    # Rounding it makes the matrix follow the extent of the cell along that direction, so
    # that adding vacuum to a slab repeats it instead of leaving it alone
    P[~periodic] = np.eye(3)[~periodic]

    # the number of cells is taken from the periodic subspace for the same reason, while its
    # sign comes from the determinant, which is what reveals a cell of reversed handedness
    determinant_ratio = np.linalg.det(scaled_structure_cell) / np.linalg.det(reference_cell)
    n_cells = int(round(np.sign(determinant_ratio)
                        * get_periodic_measure(scaled_structure_cell, periodic)
                        / get_periodic_measure(reference_cell, periodic)))

    # Rounding is a shortcut around the search, and it is only a shortcut where it is
    # certain. Between roughly twelve and thirty degrees of rotation the rounded matrix is
    # already wrong while its residual strain is still inside tol_cell and its atoms are
    # still within a quarter of the distance between sites, so accepting it on those grounds
    # alone returns a wrong supercell where the search would have returned an exact one.
    # It is therefore taken without question only when the atoms sit essentially on the
    # sites; otherwise the search runs as well and the better of the two is kept.
    rounded_score, rounded_translation = _score_rounded_matrix(
        P, structure, reference, scaled_structure_cell, tol_cell)
    site_distance = get_minimum_site_distance(reference)
    if (rounded_score is not None
            and rounded_score <= FAST_PATH_MAX_RESIDUAL_FRACTION * site_distance):
        logger.debug('Transformation matrix obtained by rounding, which leaves the atoms '
                     '{:.5f} Angstrom from the sites:\n{}'.format(rounded_score, P))
        return P, rounded_translation

    if n_cells < 1:
        # nothing to search for; report the degenerate matrix instead. This is checked
        # before the number of cells is corrected below, since a cell metric that is
        # mirrored or singular is not a matter of how many cells to look for
        check_transformation_matrix(P, scaled_structure_cell, reference_cell, tol_cell,
                                    reference.pbc)

    # the number of cells follows from the volume per atom, which underestimates it when
    # the input structure contains vacancies and no inert species are given, since the
    # missing atoms make the volume per atom of the input structure too large. A supercell
    # with fewer sites than the input structure has atoms cannot accommodate it under any
    # circumstances, so the search is given at least the smallest size that can
    minimum_cells = int(np.ceil(len(structure) / len(reference)))
    if n_cells < minimum_cells:
        logger.debug('The volume per atom gives {} reference cells, which provide fewer '
                     'sites than the input structure has atoms, so {} cells are sought '
                     'instead'.format(n_cells, minimum_cells))
        n_cells = minimum_cells

    logger.debug('Rounding the transformation matrix did not settle it, searching for it as '
                 'well ({} reference cells sought)'.format(n_cells))
    try:
        searched, searched_translation = find_transformation_matrix(
            structure, reference, scaled_structure_cell, n_cells, tol_cell, symprec)
    except ValueError:
        # the search covers a different set of matrices than the rounding, so it can come up
        # empty where the rounding did not; the rounded matrix then stands
        if rounded_score is None:
            raise
        logger.debug('The search found no candidate, so the rounded matrix stands')
        return P, rounded_translation

    check_transformation_matrix(searched, scaled_structure_cell, reference_cell, tol_cell,
                                reference.pbc)
    if rounded_score is None:
        return searched.astype(float), searched_translation

    searched_score = get_position_residuals(np.array([searched]), structure, reference)[0][0]
    if searched_score < FAST_PATH_REPLACEMENT_MARGIN * rounded_score:
        logger.debug('The search improves on the rounded matrix, {:.5f} against {:.5f} '
                     'Angstrom'.format(searched_score, rounded_score))
        return searched.astype(float), searched_translation
    logger.debug('The search does not improve on the rounded matrix, {:.5f} against {:.5f} '
                 'Angstrom, which therefore stands'.format(searched_score, rounded_score))
    return P, rounded_translation


def _score_rounded_matrix(P: np.ndarray,
                          structure: Atoms,
                          reference: Atoms,
                          scaled_structure_cell: np.ndarray,
                          tol_cell: float) -> tuple[float, np.ndarray]:
    """Returns how well a rounded transformation matrix reproduces the positions of the input
    structure, along with the corresponding rigid offset in reduced coordinates.

    The score is the mean distance between the atoms and the sites they are assigned to. It is
    ``None`` where the matrix is not usable at all, which is where it reverses the handedness
    of the cell, where its residual strain exceeds :attr:`tol_cell`, or where it leaves the
    atoms further from the sites than a quarter of the distance between them.
    """
    reference_cell = np.asarray(reference.cell, dtype=np.float64)
    if np.linalg.det(P) < 0.5:
        return None, np.zeros(3)
    # the determinant is deliberately not compared against the number of cells
    # obtained from the volume per atom; the latter can be off when the input
    # structure contains vacancies and no inert species are specified, whereas the
    # residual strain constrains the volume directly
    if get_residual_strain(P, scaled_structure_cell, reference_cell, reference.pbc) > tol_cell:
        return None, np.zeros(3)
    scores, translations, _ = get_position_residuals(np.array([P]), structure, reference)
    if scores[0] >= 0.25 * get_minimum_site_distance(reference):
        return None, np.zeros(3)
    return float(scores[0]), translations[0]


def get_reference_supercell(structure: Atoms,
                            reference: Atoms,
                            inert_species: list[str] | None = None,
                            tol_positions: float = DEFAULT_TOL_POSITIONS,
                            tol_cell: float = DEFAULT_TOL_CELL,
                            symprec: float = 1e-5,
                            assume_no_cell_relaxation: bool = False
                            ) -> tuple[Atoms, np.ndarray, np.ndarray]:
    """
    Returns a tuple comprising a supercell of the reference structure that is compatible with the
    cell metric of the input structure, the transformation matrix that maps from the
    primitive to the supercell structure, and the rigid offset in reduced coordinates that brings
    the positions of the input structure closest to the sites of the supercell.

    See :func:`map_structure_to_reference
    <icet.tools.map_structure_to_reference>` for a description of the
    parameters.

    Raises
    ------
    ValueError
        If the boundary conditions of the reference and the input structure
        do not match.
    ValueError
        If either structure contains no atoms, or if its cell does not span three
        dimensions.
    ValueError
        If a species given as inert does not occur in one of the structures.
    ValueError
        If the reference structure is periodic along fewer than two directions.
    ValueError
        If tol_cell does not lie between zero and one.
    ValueError
        If the cell metric of the input structure deviates too strongly from an
        integer transformation of the reference cell metric.
    """

    check_matching_boundary_conditions(reference, structure, 'input')
    check_periodicity_is_sufficient(reference)
    check_tol_cell(tol_cell)
    # these guards come first, so that the volume, the inverse of the cell and the
    # relaxation distances further down cannot be computed from degenerate input
    check_structure_is_not_empty(reference, 'reference')
    check_structure_is_not_empty(structure, 'input')
    check_cell_is_full_rank(reference, 'reference')
    check_cell_is_full_rank(structure, 'input')
    if inert_species is not None:
        check_inert_species(structure, reference, inert_species)

    # Step 1:
    # rescale cell metric of relaxed cell to match volume per atom of reference cell
    if not assume_no_cell_relaxation:
        scaled_structure_cell = get_volume_scaled_cell(structure, reference, inert_species)
    else:
        scaled_structure_cell = structure.cell

    # Step 2:
    # get transformation matrix, by rounding the real one if that is sufficient
    # and by searching for it otherwise
    P, translation = _get_transformation_matrix(structure, reference, scaled_structure_cell,
                                                tol_cell, symprec)

    # Step 3:
    # generate supercell of reference structure
    reference_supercell = make_supercell(reference, P, tol=tol_positions)

    # The supercell keeps the cell vectors of the reference structure along the directions
    # that are not periodic. Neither the length of such a vector nor its direction says
    # anything about the structure, both being a choice of how much empty space to carry, so
    # there is nothing in them to adopt. What the input structure does determine is where its
    # atoms sit along those directions, and that is carried across when the positions are
    # brought into this cell.
    return reference_supercell, P, translation
