"""
Search for the integer transformation matrix relating an input structure to a
reference structure.

The cell metric of the input structure is related to that of the reference
structure by an integer transformation matrix, a symmetric stretch and a
rotation. Rounding the real transformation matrix to the nearest integer one
only recovers the correct matrix if the rotation is small. This module
determines the matrix without that restriction.

The search proceeds entirely in terms of the metric tensors of the two cells,
which are invariant under a rotation, and it is therefore blind to the
orientation of the input structure. Since several matrices can reproduce the
metric tensor of the input structure, a criterion based on the positions is
needed in addition. That criterion is evaluated in reduced coordinates, in which
neither the rotation nor a homogeneous strain appears.
"""

import numpy as np
from ase import Atoms

from icet.input_output.logging_tools import logger
from .orientation import get_symmetry_rotations
from .strain import calculate_maximum_biot_strains, get_periodic_frame

MAX_CANDIDATE_PAIRS = 8_000_000
"""Largest number of pairs of cell vectors that is considered before the search
is abandoned."""

MAX_LATTICE_POINTS = 5_000_000
"""Largest number of lattice points of the reference structure that is collected before the
search is abandoned.

The bound on each index follows from the inverse of the metric tensor, so the number of
points grows without limit as the cell of the reference structure approaches degeneracy,
which a cell of full rank does not preclude. The number is therefore compared against this
limit before the points are generated, so that such a cell is reported rather than exhausting
the memory of the machine."""

RESIDUAL_TIE_WINDOW = 0.02
"""Difference in Ångstrom below which two mappings are considered to reproduce the
positions equally well, so that the species decide between them."""

TRANSLATION_MAX_RESIDUAL_FRACTION = 0.15
"""Largest mean distance between the atoms and the sites, as a fraction of the shortest
lattice vector of the reference structure, for which a rigid offset is applied.

Requiring only that an offset improve on using none at all is not enough. If the
positions do not correspond to the sites in the first place, as happens when a structure
is distorted rather than translated, some offset among those tried will improve the fit by
any given factor and thereby hide the fact that the mapping is poor. An offset is
therefore only applied if the result is good in absolute terms as well.

The scale is the distance between neighboring sites that the atoms can occupy. Counting every
site instead lets an interstitial sublattice that the input structure does not populate set the
scale: a reference with an interstitial half a bond length from its host then leaves a gate too
tight for any relaxation to pass, and the offset of a structure that plainly has one is
discarded. Counting the lattice vectors instead is too generous, and lets an offset through for
a structure whose positions do not correspond to the sites at all."""


def get_minimum_site_distance(reference: Atoms) -> float:
    """Returns the shortest distance between two distinct sites of the reference
    structure, or the shortest lattice vector if it contains only one site.
    """
    if len(reference) > 1:
        distances = reference.get_all_distances(mic=True)
        distances = distances[~np.eye(len(reference), dtype=bool)]
        shortest_pair = float(distances.min())
    else:
        shortest_pair = np.inf
    shortest_vector = float(np.linalg.norm(np.asarray(reference.cell), axis=1).min())
    return min(shortest_pair, shortest_vector)


def get_minimum_occupiable_site_distance(reference: Atoms, structure: Atoms) -> float:
    """Returns the shortest distance between two sites of the reference structure carrying a
    species that occurs in the input structure.

    This is the spacing of the sites that the atoms can be assigned to, which is the scale a
    residual has to be judged against. Every site of the reference structure taken together
    gives a different scale whenever part of the reference structure is a sublattice that the
    input structure does not populate, an interstitial sublattice in particular.

    Parameters
    ----------
    reference
        Reference structure, which provides the sites.
    structure
        Input structure, which provides the species that occur.
    """
    present = set(structure.get_chemical_symbols())
    occupiable = [index for index, symbol in enumerate(reference.get_chemical_symbols())
                  if symbol in present]
    if not occupiable:
        return get_minimum_site_distance(reference)
    # a single occupiable site leaves no pair, and the shortest lattice vector is then the
    # spacing of that sublattice, which is what get_minimum_site_distance falls back to
    return get_minimum_site_distance(reference[occupiable])


def _get_lattice_points(reference_cell: np.ndarray,
                        radius: float) -> np.ndarray:
    r"""Returns all integer triplets whose corresponding lattice vector is no
    longer than :attr:`radius`.

    The bound on each index follows from maximizing :math:`|p_k|` subject to
    :math:`p G p^T \le r^2`, which gives :math:`r \sqrt{(G^{-1})_{kk}}`.

    Raises
    ------
    ValueError
        If more than :data:`MAX_LATTICE_POINTS` points would be needed.
    """
    metric = np.dot(reference_cell, reference_cell.T)
    bounds = np.ceil(radius * np.sqrt(np.diag(np.linalg.inv(metric)))).astype(int)

    # count the points before generating them, using integers of arbitrary size so that the
    # count itself cannot overflow
    n_points = 1
    for bound in bounds:
        n_points *= 2 * int(bound) + 1
    if n_points > MAX_LATTICE_POINTS:
        raise ValueError(
            'The search for the transformation matrix relating the input structure to the '
            'reference structure was abandoned, since it would require {} lattice points of '
            'the reference structure.'.format(n_points)
            + '\n  bounds on the indices: ' + str(bounds)
            + '\n  Reducing tol_cell narrows the search. A cell of the reference structure '
              'whose vectors are nearly parallel widens it, in which case a different setting '
              'of the same lattice is cheaper to search.')

    ranges = [np.arange(-bound, bound + 1) for bound in bounds]
    return np.stack(np.meshgrid(*ranges, indexing='ij'), axis=-1).reshape(-1, 3)


def find_candidate_transformation_matrices(structure_cell: np.ndarray,
                                           reference_cell: np.ndarray,
                                           n_cells: int,
                                           pbc: np.ndarray,
                                           tol_cell: float) -> np.ndarray:
    """Returns the integer matrices that reproduce the cell metric of the input
    structure up to a rotation.

    Two cells are related by a rotation if and only if their metric tensors
    agree, so only the metric tensors enter here. Rows along a direction that is
    not periodic are not searched over, since the extent of the cell along such a
    direction is arbitrary.

    Parameters
    ----------
    structure_cell
        Cell metric of the input structure, rescaled if applicable.
    reference_cell
        Cell metric of the reference structure.
    n_cells
        Number of reference cells that the input structure is expected to contain.
    pbc
        Periodic boundary conditions of the two structures.
    tol_cell
        Relative tolerance for the agreement of the metric tensors.

    Returns
    -------
        Array of shape ``(N, 3, 3)`` holding the candidate matrices, which may be
        empty.
    """
    structure_cell = np.asarray(structure_cell, dtype=np.float64)
    reference_cell = np.asarray(reference_cell, dtype=np.float64)
    metric_reference = np.dot(reference_cell, reference_cell.T)
    metric_structure = np.dot(structure_cell, structure_cell.T)
    target_lengths_squared = np.diag(metric_structure)

    # A matrix is accepted if the eigenvalues of the stretch relating the transformed
    # reference cell to the cell of the input structure lie within tol_cell of unity.
    # Writing the metric tensor of the input structure as a_i C a_j for the rows a_i of the
    # transformed reference cell, C being the square of that stretch, gives
    # |a_i C a_j - a_i a_j| <= metric_tolerance |a_i| |a_j|, from which the bounds below
    # follow. They are derived this way so that no matrix that would be accepted is
    # discarded before the criterion that decides acceptance is evaluated.
    metric_tolerance = 2 * tol_cell + tol_cell ** 2
    smallest_factor = 1 / (1 + tol_cell) ** 2
    largest_factor = 1 / (1 - tol_cell) ** 2

    radius = np.sqrt(largest_factor * target_lengths_squared.max())
    points = _get_lattice_points(reference_cell, radius)
    lengths_squared = np.einsum('ni,ij,nj->n', points, metric_reference, points)

    # the admissible rows for each direction along with their squared lengths; a direction
    # that is not periodic is fixed, since the extent of the cell along it is arbitrary
    shells, shell_lengths = [], []
    for direction in range(3):
        if not pbc[direction]:
            shells.append(np.eye(3, dtype=int)[direction][None, :])
            shell_lengths.append(np.array([metric_reference[direction, direction]]))
            continue
        target = target_lengths_squared[direction]
        mask = ((lengths_squared >= smallest_factor * target)
                & (lengths_squared <= largest_factor * target))
        shells.append(points[mask])
        shell_lengths.append(lengths_squared[mask])
    logger.debug('Sizes of the shells of candidate cell vectors: {}'.format(
        [len(shell) for shell in shells]))

    if any(len(shell) == 0 for shell in shells):
        return np.zeros((0, 3, 3), dtype=int)

    n_pairs = max(len(shells[0]) * len(shells[1]), len(shells[1]) * len(shells[2]))
    if n_pairs > MAX_CANDIDATE_PAIRS:
        raise ValueError(
            'The search for the transformation matrix relating the input structure to the '
            'reference structure was abandoned, since it would require considering {} pairs '
            'of cell vectors.\n  Reducing tol_cell narrows the search.'.format(n_pairs))

    candidates = []
    for first_row, first_length in zip(shells[0], shell_lengths[0]):
        second_rows, second_lengths = _filter_on_metric_element(
            shells[1], shell_lengths[1], first_row, first_length, metric_reference,
            metric_structure[0, 1], metric_tolerance, pbc[0] and pbc[1])
        if len(second_rows) == 0:
            continue
        third_rows, third_lengths = _filter_on_metric_element(
            shells[2], shell_lengths[2], first_row, first_length, metric_reference,
            metric_structure[0, 2], metric_tolerance, pbc[0] and pbc[2])
        if len(third_rows) == 0:
            continue

        # the remaining element of the metric tensor couples the second and the third row
        if pbc[1] and pbc[2]:
            inner = second_rows @ metric_reference @ third_rows.T
            bound = metric_tolerance * np.sqrt(np.outer(second_lengths, third_lengths))
            pairs = np.argwhere(np.abs(inner - metric_structure[1, 2]) <= bound)
        else:
            pairs = np.stack(np.meshgrid(np.arange(len(second_rows)),
                                         np.arange(len(third_rows)),
                                         indexing='ij'), axis=-1).reshape(-1, 2)
        if len(pairs) == 0:
            continue

        block = np.empty((len(pairs), 3, 3), dtype=int)
        block[:, 0, :] = first_row
        block[:, 1, :] = second_rows[pairs[:, 0]]
        block[:, 2, :] = third_rows[pairs[:, 1]]
        candidates.append(block[_get_determinants(block) == n_cells])

    candidates = [block for block in candidates if len(block)]
    if not candidates:
        return np.zeros((0, 3, 3), dtype=int)

    candidates = np.concatenate(candidates, axis=0)
    # keep only the matrices whose residual strain is within the tolerance, evaluated for
    # the whole set at once since the bounds above admit a great many matrices
    residuals = calculate_maximum_biot_strains(
        candidates.astype(np.float64) @ reference_cell, structure_cell, pbc)
    candidates = candidates[residuals <= tol_cell]
    logger.debug('Number of candidate transformation matrices: {}'.format(len(candidates)))
    return candidates


def _get_determinants(blocks: np.ndarray) -> np.ndarray:
    """Returns the determinant of each of a stack of 3x3 integer matrices.

    Writing the expression out keeps the result exact, since the matrices are integer, and
    is considerably faster than a general purpose routine for the many small matrices that
    the search generates.
    """
    return (blocks[:, 0, 0] * (blocks[:, 1, 1] * blocks[:, 2, 2]
                               - blocks[:, 1, 2] * blocks[:, 2, 1])
            - blocks[:, 0, 1] * (blocks[:, 1, 0] * blocks[:, 2, 2]
                                 - blocks[:, 1, 2] * blocks[:, 2, 0])
            + blocks[:, 0, 2] * (blocks[:, 1, 0] * blocks[:, 2, 1]
                                 - blocks[:, 1, 1] * blocks[:, 2, 0]))


def _filter_on_metric_element(rows: np.ndarray,
                              lengths_squared: np.ndarray,
                              other_row: np.ndarray,
                              other_length_squared: float,
                              metric_reference: np.ndarray,
                              target: float,
                              metric_tolerance: float,
                              constrained: bool) -> tuple[np.ndarray, np.ndarray]:
    """Returns the rows whose inner product with :attr:`other_row` agrees with
    :attr:`target`, together with their squared lengths.

    The bound follows from the tolerance on the stretch, so a row that can still lead to an
    accepted transformation matrix is never discarded. If either of the two directions is not
    periodic the rows are returned unchanged, since the corresponding element of the metric
    tensor of the input structure then carries no information.
    """
    if not constrained:
        return rows, lengths_squared
    inner = rows @ metric_reference @ other_row
    bound = metric_tolerance * np.sqrt(other_length_squared * lengths_squared)
    keep = np.abs(inner - target) <= bound
    return rows[keep], lengths_squared[keep]


def get_residual_strain(P: np.ndarray,
                        structure_cell: np.ndarray,
                        reference_cell: np.ndarray,
                        pbc: np.ndarray = None) -> float:
    """Returns the largest absolute eigenvalue of the Biot strain tensor relating
    the transformed reference cell to the cell of the input structure.

    The measure is invariant under a rotation of either cell and it does not
    depend on the size of the cells. It is taken over the subspace spanned by the periodic
    cell vectors, so that the cell vectors along the other directions, whose extent is
    arbitrary, do not enter even when they are not orthogonal to that subspace.
    """
    transformed = np.dot(np.asarray(P, dtype=np.float64), reference_cell)
    return float(calculate_maximum_biot_strains(
        transformed[None, :, :], structure_cell, pbc)[0])


def get_relevant_images(reference_cell: np.ndarray,
                        periodic: np.ndarray) -> np.ndarray:
    """Returns the image offsets that can shorten a difference already reduced into the box
    of reduced coordinates.

    Reducing a difference componentwise puts every component between minus and plus one half,
    which is the closest image only for a cell whose box in reduced coordinates is its own
    Wigner-Seitz cell. An oblique cell is not such a cell, and for the primitive face centered
    cubic cell the componentwise reduction overstates a distance by as much as 73 per cent.
    The offsets that can do better are collected once here and tried alongside the reduced
    difference.

    An offset :math:`n` beats the origin for a difference :math:`d` exactly when
    :math:`2 d G n > n G n` for the metric tensor :math:`G`, and the left hand side is largest
    at a corner of the box, so testing the corners settles it. A cell for which no offset
    qualifies, such as any orthogonal cell, yields the zero offset alone and costs nothing.

    Parameters
    ----------
    reference_cell
        Cell metric of the reference structure (row-major format).
    periodic
        Boolean mask marking the periodic directions.

    Returns
    -------
        Array of shape ``(N, 3)`` whose first row is zero.
    """
    reference_cell = np.asarray(reference_cell, dtype=np.float64)
    ranges = [np.arange(-1, 2) if flag else np.zeros(1, dtype=int) for flag in periodic]
    offsets = np.stack(np.meshgrid(*ranges, indexing='ij'), axis=-1).reshape(-1, 3)
    corners = np.stack(np.meshgrid(*([np.array([-0.5, 0.5])] * 3), indexing='ij'),
                       axis=-1).reshape(-1, 3)

    plain = np.linalg.norm(corners @ reference_cell, axis=1)
    relevant = [np.zeros(3)]
    for offset in offsets:
        if not offset.any():
            continue
        if np.any(np.linalg.norm((corners - offset) @ reference_cell, axis=1) < plain - 1e-12):
            relevant.append(offset.astype(np.float64))
    return np.array(relevant)


def _score_offset(transformed: np.ndarray,
                  site_fractional: np.ndarray,
                  reference_cell: np.ndarray,
                  offset: np.ndarray,
                  periodic: np.ndarray,
                  images: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """Returns the mean distance to the closest site for a given offset, together
    with the index of the closest site for each atom and the mean residual in
    reduced coordinates.

    The mean residual is used to refine the offset. An offset obtained from a single
    atom carries the relaxation of that atom, which the refinement removes.

    Only the directions marked in :attr:`periodic` are wrapped, and the offsets in
    :attr:`images`, as returned by :func:`get_relevant_images`, are tried alongside the
    reduced difference so that the distance is to the closest image.
    """
    difference = transformed[:, None, :] - offset - site_fractional[None, :, :]
    # only a periodic direction may be wrapped; along a direction that is not periodic two
    # positions separated by a lattice vector are distinct, which is how the final site
    # matching, applying the boundary conditions of the reference structure, treats them
    difference[..., periodic] -= np.rint(difference[..., periodic])

    # the conversion to Cartesian coordinates is the expensive step, so it is done once and
    # the images are subtracted from the result rather than from the reduced difference
    cartesian = difference @ reference_cell
    distances = np.linalg.norm(cartesian, axis=2)
    if len(images) > 1:
        # an oblique cell needs the neighbouring images as well, since the componentwise
        # reduction above does not by itself give the closest one. The running minimum keeps
        # the whole stack of images out of memory.
        image_cartesian = images @ reference_cell
        chosen = np.zeros(distances.shape, dtype=np.int8)
        for index in range(1, len(images)):
            lengths = np.linalg.norm(cartesian - image_cartesian[index], axis=2)
            closer = lengths < distances
            distances = np.where(closer, lengths, distances)
            chosen = np.where(closer, index, chosen)
        difference = difference - images[chosen]

    closest = np.argmin(distances, axis=1)
    rows = np.arange(len(transformed))
    score = float(distances[rows, closest].mean())
    mean_residual = difference[rows, closest].mean(axis=0)
    return score, closest, mean_residual


def get_position_residuals(candidates: np.ndarray,
                           structure: Atoms,
                           reference: Atoms,
                           n_anchors: int = 3,
                           acceptance_margin: float = 0.8
                           ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns, for each candidate transformation matrix, how well the positions
    of the input structure agree with the sites of the corresponding reference
    supercell.

    The reduced coordinates of the input structure with respect to the reference
    cell are :math:`g = f P`, where :math:`f` are the reduced coordinates with
    respect to the cell of the input structure. Neither the rotation nor a
    homogeneous strain enters this relation, so the residual reflects only the
    relaxation of the positions and a rigid offset.

    A rigid offset is determined along with the residual. Since the sites of the
    ideal supercell are invariant, modulo the lattice of the reference structure,
    under a translation by a lattice vector of the reference structure, every
    offset is equivalent to the difference between the reduced coordinates of one
    atom and those of one reference site.

    Parameters
    ----------
    candidates
        Candidate transformation matrices, of shape ``(N, 3, 3)``.
    structure
        Input structure.
    reference
        Reference structure.
    n_anchors
        Number of atoms used to generate the candidate offsets. More than one is
        used so that a single badly relaxed atom cannot spoil the result.
    acceptance_margin
        An offset is only reported if it reduces the mean distance to at most this fraction
        of what using no offset at all leaves. A structure that is already aligned is thereby
        reported with a vanishing offset. The fraction is not the whole of the criterion, and
        deliberately not the strict half it once was: a structure that is rattled as much as
        it is displaced improves by less than a factor of two, so requiring one discards the
        offset of a structure that plainly has one. Rejecting a distorted structure is left to
        the absolute gate, which is what it exists for.

    Returns
    -------
        The smallest mean distance in Ångstrom between an atom and the closest site,
        the corresponding offset in reduced coordinates, and the fraction of atoms
        whose species matches that of the closest site, for each candidate.
    """
    reference_cell = np.asarray(reference.cell, dtype=np.float64)
    periodic = np.asarray(reference.pbc, dtype=bool)
    # distances are measured in the frame the coordinates below are expressed in, which is the
    # reference cell itself where every direction is periodic
    reference_frame = get_periodic_frame(reference_cell, periodic)
    structure_frame = get_periodic_frame(structure.cell, periodic)
    images = get_relevant_images(reference_frame, periodic)

    # The reduced coordinates are taken with respect to the periodic cell vectors of the input
    # structure, completed along the remaining directions by a basis of what is left, which is
    # what get_periodic_frame builds. Along those directions the coordinate is then a Cartesian
    # length rather than a fraction of an arbitrary extent, so an atom that has not moved keeps
    # its coordinate however much vacuum surrounds it and however that vacuum is directed.
    # This is the same frame that the positions are carried into once the supercell is known,
    # so the offset is sought in the frame it is applied in.
    fractional = np.linalg.solve(structure_frame.T, structure.positions.T).T

    site_fractional = np.linalg.solve(reference_frame.T, reference.get_positions().T).T
    structure_numbers = structure.get_atomic_numbers()
    site_numbers = reference.get_atomic_numbers()
    comparable = np.isin(structure_numbers, site_numbers)
    max_mean_residual = (TRANSLATION_MAX_RESIDUAL_FRACTION
                         * get_minimum_occupiable_site_distance(reference, structure))

    scores = np.zeros(len(candidates))
    translations = np.zeros((len(candidates), 3))
    agreements = np.zeros(len(candidates))

    anchors = range(min(n_anchors, len(structure)))
    for index, P in enumerate(candidates):
        transformed = fractional @ P
        offsets = [np.zeros(3)]
        for anchor in anchors:
            for site in range(len(reference)):
                offsets.append(transformed[anchor] - site_fractional[site])

        # using no offset at all is the reference against which any offset has to
        # prove itself, and it is deliberately not refined
        baseline = _score_offset(transformed, site_fractional, reference_cell,
                                 np.zeros(3), periodic, images)
        baseline_score, baseline_closest, _ = baseline
        baseline_agreement = _get_species_agreement(site_numbers[baseline_closest],
                                                    structure_numbers, comparable)

        evaluated = []
        for offset in offsets[1:]:
            score, closest, mean_residual = _score_offset(
                transformed, site_fractional, reference_frame, offset, periodic, images)
            # refine the offset, which removes the relaxation of the anchor atom
            refined = offset + mean_residual
            refined_score, refined_closest, _ = _score_offset(
                transformed, site_fractional, reference_frame, refined, periodic, images)
            if refined_score < score:
                score, offset, closest = refined_score, refined, refined_closest
            agreement = _get_species_agreement(site_numbers[closest], structure_numbers,
                                               comparable)
            evaluated.append((score, offset, agreement))

        best_score, best_offset, best_agreement = baseline_score, np.zeros(3), baseline_agreement
        if evaluated:
            # An offset that maps the sites of one sublattice onto those of another
            # can reproduce the positions just as well as the correct one, so among
            # the offsets that are equally good the species have to decide.
            smallest = min(entry[0] for entry in evaluated)
            tied = [entry for entry in evaluated if entry[0] <= smallest + RESIDUAL_TIE_WINDOW]
            candidate = max(tied, key=lambda entry: entry[2])
            # An offset is applied if it improves the agreement of the positions
            # substantially without worsening that of the species, or if it improves the
            # agreement of the species without worsening that of the positions. The second
            # of these is what corrects an origin sitting on the wrong sublattice: the
            # positions are then reproduced perfectly whichever sublattice the atoms are
            # assigned to, so only the species tell the two apart, and requiring an
            # improvement in the positions asks for something that cannot happen.
            # Either way the atoms have to end up close to the sites in absolute terms,
            # which is what keeps a structure whose positions do not correspond to the sites
            # at all from being made to look mapped by an offset that merely fits it better.
            improves_positions = (candidate[0] < acceptance_margin * baseline_score
                                  and candidate[2] >= baseline_agreement)
            improves_species = (candidate[2] > baseline_agreement
                                and candidate[0] <= baseline_score + RESIDUAL_TIE_WINDOW)
            if (improves_positions or improves_species) and candidate[0] <= max_mean_residual:
                best_score, best_offset, best_agreement = candidate
            elif improves_positions or improves_species:
                logger.debug('An offset of {} in reduced coordinates was not applied, since '
                             'the mean distance of {:.5f} Angstrom that it leaves exceeds '
                             '{:.5f} Angstrom'.format(np.round(candidate[1], 5), candidate[0],
                                                      max_mean_residual))

        scores[index] = best_score
        translations[index] = best_offset
        agreements[index] = best_agreement

    return scores, translations, agreements


def _get_species_agreement(site_numbers: np.ndarray,
                           structure_numbers: np.ndarray,
                           comparable: np.ndarray) -> float:
    """Returns the fraction of atoms that sit on a site of their own species.

    Only the atoms whose species also occurs in the reference structure are counted.
    A species that occurs in the input structure but not in the reference structure,
    such as a substituting species, can never match and would otherwise dilute the
    measure until it carries no information.
    """
    if not comparable.any():
        return 0.0
    return float(np.mean(site_numbers[comparable] == structure_numbers[comparable]))


def reduce_candidates_by_symmetry(candidates: np.ndarray,
                                  reference: Atoms,
                                  symprec: float = 1e-5) -> np.ndarray:
    """Returns the candidate transformation matrices that are inequivalent under
    the symmetry of the reference structure.

    Two matrices describe the same mapping if they differ by a rotation of the
    reference structure. A rotation :math:`W` in reduced coordinates acts on the
    rows of the transformation matrix as :math:`P \\rightarrow P W^T`.

    Parameters
    ----------
    candidates
        Candidate transformation matrices, of shape ``(N, 3, 3)``.
    reference
        Reference structure, whose symmetry operations are used.
    symprec
        Tolerance passed to :program:`spglib`.
    """
    if len(candidates) <= 1:
        return candidates

    rotations = {tuple(rotation.flatten())
                 for rotation in get_symmetry_rotations(reference, symprec)}

    kept = []
    for P in candidates:
        duplicate = False
        for previous in kept:
            # P = previous W^T, so the transformation sought is previous^-1 P
            transformation = np.linalg.solve(previous.astype(float), P.astype(float))
            rounded = np.rint(transformation)
            if not np.allclose(transformation, rounded, atol=1e-6):
                continue
            if tuple(rounded.T.astype(int).flatten()) in rotations:
                duplicate = True
                break
        if not duplicate:
            kept.append(P)

    logger.debug('Number of symmetry inequivalent transformation matrices: {}'.format(len(kept)))
    return np.array(kept, dtype=int)


def find_transformation_matrix(structure: Atoms,
                               reference: Atoms,
                               structure_cell: np.ndarray,
                               n_cells: int,
                               tol_cell: float,
                               symprec: float = 1e-5) -> tuple[np.ndarray, np.ndarray]:
    """Returns the integer transformation matrix relating the input structure to
    the reference structure, along with the rigid offset in reduced coordinates.

    The cell metric alone does not determine the matrix, because several matrices
    reproduce it. The positions are therefore used to select among the candidates,
    and the symmetry of the reference structure is used to discard the candidates
    that describe the same mapping. Should more than one distinct mapping remain,
    the one for which the species of the atoms agree best with the species of the
    sites is chosen.

    Parameters
    ----------
    structure
        Input structure.
    reference
        Reference structure.
    structure_cell
        Cell metric of the input structure, rescaled if applicable.
    n_cells
        Number of reference cells that the input structure is expected to contain.
    tol_cell
        Relative tolerance for the agreement of the metric tensors.
    symprec
        Tolerance passed to :program:`spglib`.

    Raises
    ------
    ValueError
        If no transformation matrix reproduces the cell metric of the input
        structure.
    """
    candidates = find_candidate_transformation_matrices(
        structure_cell, np.asarray(reference.cell, dtype=np.float64), n_cells,
        reference.pbc, tol_cell)

    if len(candidates) == 0:
        msg = ('Could not find a supercell of the reference structure whose cell metric '
               'matches that of the input structure.')
        msg += '\n  tol_cell: ' + str(tol_cell)
        msg += '\n  number of reference cells sought: ' + str(n_cells)
        msg += ('\n  The input structure may not be a supercell of the reference structure, '
                'or it may be too strongly strained.')
        raise ValueError(msg)

    scores, translations, agreements = get_position_residuals(candidates, structure, reference)

    # discard the candidates that clearly do not reproduce the positions before
    # comparing the remaining ones, which are often related by symmetry
    threshold = max(1.5 * scores.min(), scores.min() + 1e-3)
    selected = scores <= threshold
    candidates, scores = candidates[selected], scores[selected]
    translations, agreements = translations[selected], agreements[selected]
    logger.debug('Number of candidates reproducing the positions: {} of {}'.format(
        len(candidates), len(selected)))

    representatives = reduce_candidates_by_symmetry(candidates, reference, symprec)

    # among the inequivalent representatives prefer the one that reproduces the
    # positions best. Mappings that do so equally well within RESIDUAL_TIE_WINDOW are
    # separated by the agreement of the species, which is the more reliable criterion when
    # the lattice is more symmetric than the crystal, then by how compact the matrix is, so
    # that the supercell stays as close to the setting of the reference structure as the
    # candidates allow, and finally by the matrix itself so that the outcome is reproducible
    indices = [int(np.argmin(np.abs(candidates - P).sum(axis=(1, 2)))) for P in representatives]
    smallest = min(scores[index] for index in indices)
    tied = [index for index in indices
            if scores[index] <= smallest + RESIDUAL_TIE_WINDOW]
    if len(tied) > 1:
        logger.debug('{} mappings reproduce the positions equally well; deciding on the '
                     'agreement of the species'.format(len(tied)))
    best_index = max(tied, key=lambda index: (agreements[index],
                                              -np.square(candidates[index]).sum(),
                                              tuple(-value for value in
                                                    candidates[index].flatten())))

    logger.debug('Transformation matrix:\n{}\n  residual {:.5f}, species agreement {:.2f}'.format(
        candidates[best_index], scores[best_index], agreements[best_index]))
    return candidates[best_index], translations[best_index]
