"""
Interpretation of the outcome of a structure mapping.

The functions in this module translate the quantities produced by the mapping into
warning tags and the corresponding human readable messages. They perform no
geometric analysis of their own, but work from the per-atom arrays attached to the
mapped structure, which makes them straightforward to exercise on their own.
"""

import numpy as np
from ase import Atoms

MAX_REPORTED_SITES = 10
"""Largest number of site indices quoted in a warning message."""

DEFAULT_TRIGGER_LEVELS = {'volumetric_strain': 0.25,
                          'anisotropic_strain': 0.1,
                          'maximum_displacement': 1.0,
                          'average_displacement': 0.5,
                          'maximum_displacement_fraction': 0.3,
                          'average_displacement_fraction': 0.15,
                          'ambiguity_tolerance': 1e-6,
                          'ambiguity_ratio': 0.9}
"""Levels at which the warnings concerning a mapped structure are triggered.

* ``volumetric_strain``: absolute volumetric strain.
* ``anisotropic_strain``: difference between the largest and the smallest eigenvalue
  of the strain tensor.
* ``maximum_displacement``: largest distance in Ångstrom between a relaxed position
  and its site.
* ``average_displacement``: average distance in Ångstrom between the relaxed
  positions and their sites.
* ``maximum_displacement_fraction``: the same, as a fraction of the distance between
  two neighboring sites. Whether a displacement is large depends on the lattice, so a
  displacement of half the distance to the next site is reported however large the
  lattice constant happens to be.
* ``average_displacement_fraction``: likewise for the average.
* ``ambiguity_tolerance``: slack in Ångstrom allowed when deciding whether an atom was
  assigned to a site further away than the closest one.
* ``ambiguity_ratio``: an atom counts as almost equally far from its two closest sites
  if the distance to the closest one exceeds this fraction of the distance to the
  second closest one.
"""

DEFAULT_TRIGGER_LEVELS_NO_CELL_RELAXATION = dict(DEFAULT_TRIGGER_LEVELS,
                                                 volumetric_strain=1e-3,
                                                 anisotropic_strain=1e-3)
"""Levels used when no relaxation of the cell is assumed. The levels for the strain
are much tighter, since in that case the input structure is expected to be obtainable
from the reference structure via an integer transformation matrix."""


def get_trigger_levels(assume_no_cell_relaxation: bool = False,
                       trigger_levels: dict[str, float] | None = None) -> dict[str, float]:
    """Returns the levels at which the warnings are triggered.

    Parameters
    ----------
    assume_no_cell_relaxation
        If ``True`` the tighter levels for the strain are used as the starting point.
    trigger_levels
        Levels that deviate from the defaults. Levels that are not given keep their
        default value.

    Raises
    ------
    ValueError
        If :attr:`trigger_levels` contains a key that is not a known trigger level.
    """
    defaults = (DEFAULT_TRIGGER_LEVELS_NO_CELL_RELAXATION if assume_no_cell_relaxation
                else DEFAULT_TRIGGER_LEVELS)
    if trigger_levels is None:
        return dict(defaults)

    unknown = sorted(set(trigger_levels) - set(defaults))
    if unknown:
        raise ValueError('Unknown trigger level(s): {}.\n  Valid trigger levels are: {}.'
                         .format(', '.join(unknown), ', '.join(sorted(defaults))))
    return dict(defaults, **trigger_levels)


def get_displacement_metrics(mapped: Atoms) -> tuple[float, float]:
    """Returns the maximum and the average distance between the relaxed positions and
    the sites they were assigned to.

    Vacant sites carry no displacement and are not counted.

    Parameters
    ----------
    mapped
        Mapped structure, carrying the array of displacement magnitudes.
    """
    magnitudes = mapped.arrays['Displacement_Magnitude']
    occupied = magnitudes[~np.isnan(magnitudes)]
    if len(occupied) == 0:
        return float('nan'), float('nan')
    return float(occupied.max()), float(occupied.mean())


def find_ambiguous_sites(mapped: Atoms,
                         trigger_levels: dict[str, float]) -> tuple[list[int], list[int]]:
    """Returns the sites whose assignment is ambiguous.

    Two situations are distinguished. An atom can be assigned to a site that is
    further away than the closest site, which happens when the closest site is
    already occupied by another atom. An atom can also be almost equally far from
    its two closest sites, in which case a small change of the positions would
    change the assignment.

    Both are decided from the arrays attached to the mapped structure, since the
    magnitude of the displacement of an atom and the distances to the sites closest
    to it are recorded there.

    Parameters
    ----------
    mapped
        Mapped structure, carrying the arrays of displacement magnitudes and of
        minimum distances.
    trigger_levels
        Levels at which the warnings are triggered.

    Returns
    -------
        The sites at which an atom was assigned past its closest site, and the sites
        at which an atom was almost equally far from two sites.
    """
    magnitudes = mapped.arrays['Displacement_Magnitude']
    minimum_distances = mapped.arrays['Minimum_Distances']
    tolerance = trigger_levels['ambiguity_tolerance']
    ratio = trigger_levels['ambiguity_ratio']

    assigned_past_closest = []
    close_alternative = []
    for site in range(len(mapped)):
        if np.isnan(magnitudes[site]):
            continue
        closest = minimum_distances[site][0]
        if magnitudes[site] > closest + tolerance:
            assigned_past_closest.append(site)
        elif len(minimum_distances[site]) > 1 and not np.isnan(minimum_distances[site][1]):
            if closest > ratio * minimum_distances[site][1]:
                close_alternative.append(site)

    return assigned_past_closest, close_alternative


def _describe_sites(sites: list[int]) -> str:
    """Returns a description of the number of sites affected and of their indices."""
    quoted = ', '.join(str(site) for site in sites[:MAX_REPORTED_SITES])
    if len(sites) > MAX_REPORTED_SITES:
        quoted += ', ...'
    return 'Number of sites affected: {} ({}).'.format(len(sites), quoted)


def collect_warnings(mapped: Atoms,
                     volumetric_strain: float,
                     eigenvalues: np.ndarray,
                     drmax: float,
                     dravg: float,
                     trigger_levels: dict[str, float],
                     minimum_site_distance: float) -> tuple[list[tuple[str, str]], list[int]]:
    """Returns the warnings triggered by the outcome of a structure mapping, together
    with the sites whose assignment is ambiguous.

    The warnings are returned as a list of tuples, the first element of which is a tag
    identifying the warning and the second element of which is the corresponding
    message. Each reason is reported once, with the number of sites affected, rather
    than once per site.

    Parameters
    ----------
    mapped
        Mapped structure.
    volumetric_strain
        Volumetric strain of the input structure relative to the reference structure.
    eigenvalues
        Eigenvalues of the strain tensor.
    drmax
        Maximum distance between a relaxed position and its site.
    dravg
        Average distance between the relaxed positions and their sites.
    trigger_levels
        Levels at which the warnings are triggered.
    minimum_site_distance
        Distance between two neighboring sites of the reference structure, against which
        the relaxation distances are judged in addition to the absolute levels.
    """
    s = 'Consider excluding this structure when training a cluster expansion.'
    warnings = []

    assigned_past_closest, close_alternative = find_ambiguous_sites(mapped, trigger_levels)
    if assigned_past_closest:
        warnings.append(('possible_ambiguity_in_mapping',
                         'An atom was mapped to a site that was further away than the '
                         'closest site (that site was already occupied by another atom). '
                         + _describe_sites(assigned_past_closest)))
    if close_alternative:
        warnings.append(('possible_ambiguity_in_mapping',
                         'An atom was approximately equally far from its two closest '
                         'sites. ' + _describe_sites(close_alternative)))

    if abs(volumetric_strain) > trigger_levels['volumetric_strain']:
        warnings.append(('high_volumetric_strain',
                         'High volumetric strain ({:.2f} %). {}'.format(
                             100 * volumetric_strain, s)))

    eigenvalue_diff = max(eigenvalues) - min(eigenvalues)
    if eigenvalue_diff > trigger_levels['anisotropic_strain']:
        warnings.append(('high_anisotropic_strain',
                         'High anisotropic strain (the difference between '
                         'largest and smallest eigenvalues of strain tensor is '
                         '{:.5f}). {}'.format(eigenvalue_diff, s)))

    # a displacement counts as large either in absolute terms or relative to the
    # distance between neighboring sites, since what is large depends on the lattice
    maximum_fraction = drmax / minimum_site_distance
    if (drmax > trigger_levels['maximum_displacement']
            or maximum_fraction > trigger_levels['maximum_displacement_fraction']):
        warnings.append(('large_maximum_relaxation_distance',
                         'Large maximum relaxation distance ({:.5f} Angstrom, {:.0f} % of '
                         'the distance to the next site). {}'.format(
                             drmax, 100 * maximum_fraction, s)))

    average_fraction = dravg / minimum_site_distance
    if (dravg > trigger_levels['average_displacement']
            or average_fraction > trigger_levels['average_displacement_fraction']):
        warnings.append(('large_average_relaxation_distance',
                         'Large average relaxation distance ({:.5f} Angstrom, {:.0f} % of '
                         'the distance to the next site). {}'.format(
                             dravg, 100 * average_fraction, s)))

    return warnings, sorted(set(assigned_past_closest + close_alternative))
