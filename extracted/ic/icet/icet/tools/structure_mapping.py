import numpy as np
from ase import Atoms

from icet.input_output.logging_tools import logger
from .structure_mapping_support.alignment import (DEFAULT_TOL_CELL, DEFAULT_TOL_POSITIONS,
                                                  get_reference_supercell)
from .structure_mapping_support.candidate_search import get_minimum_site_distance
from .structure_mapping_support.deformation import CellDeformation
from .structure_mapping_support.diagnostics import (DEFAULT_TRIGGER_LEVELS,
                                                    DEFAULT_TRIGGER_LEVELS_NO_CELL_RELAXATION,
                                                    collect_warnings,
                                                    get_displacement_metrics,
                                                    get_trigger_levels)
from .structure_mapping_support.mapping_result import StructureMapping
from .structure_mapping_support.orientation import (calculate_disorientation,
                                                    get_point_group_operations)
from .structure_mapping_support.site_matching import match_positions
from .structure_mapping_support.strain import (calculate_strain_eigenvalues,
                                               calculate_strain_tensor,
                                               calculate_volumetric_strain,
                                               get_periodic_frame,
                                               transfer_positions)

__all__ = ['DEFAULT_TRIGGER_LEVELS', 'DEFAULT_TRIGGER_LEVELS_NO_CELL_RELAXATION',
           'StructureMapping', 'map_structure_to_reference']


def map_structure_to_reference(structure: Atoms,
                               reference: Atoms,
                               *,
                               inert_species: list[str] | None = None,
                               tol_positions: float = DEFAULT_TOL_POSITIONS,
                               tol_cell: float = DEFAULT_TOL_CELL,
                               symprec: float = 1e-5,
                               find_translation: bool = True,
                               trigger_levels: dict[str, float] | None = None,
                               suppress_warnings: bool = False,
                               assume_no_cell_relaxation: bool = False) \
        -> tuple[Atoms, StructureMapping]:
    """Maps a structure onto a reference structure.
    This is often desirable when, for example, a structure has been
    relaxed using DFT, and one wants to use it as a training structure
    in a cluster expansion.

    The function returns a tuple comprising the ideal supercell most closely matching the
    input structure and a :class:`StructureMapping <icet.tools.StructureMapping>` carrying
    the supplementary information about the mapping. The latter reports the relaxation
    distances, the transformation matrix, any rigid offset that was removed, the sites
    whose assignment is ambiguous, the warnings that were triggered, the strain and its
    separation into a change of volume and a change of shape, and the rotation. Its
    attributes are documented there.

    The rotation is reported as ``disorientation_angle`` and ``disorientation_axis``,
    reduced over the symmetry of the reference structure, because a supercell related to
    the returned one by a symmetry operation describes the same crystal, so only the
    smallest rotation among those descriptions means anything on its own. Successive
    rotations of a structure are not reported separately, since any number of them compose
    into a single rotation about a single axis.

    The returned Atoms object carries the following per-atom arrays, each with one entry
    per site of the returned supercell rather than per atom of the input structure.

    * ``Displacement``, shape ``(n, 3)``, the displacement in Ångstrom pointing from the
      site to the position of the atom that occupies it,
    * ``Displacement_Magnitude``, shape ``(n,)``, its norm,
    * ``Minimum_Distances``, shape ``(n, 3)``, the distances in Ångstrom to the three
      closest sites, irrespective of whether those sites are occupied, padded if the
      reference structure has fewer than three sites,
    * ``IndexMapping``, shape ``(n,)``, the index of the atom of the input structure that
      occupies the site.

    At a vacant site the three arrays of distances are undefined and ``IndexMapping`` is
    ``-1``.

    Notes
    -----
    Only :attr:`structure` and :attr:`reference` can be given positionally. Everything
    else has to be given by keyword.

    The input structure may be rotated relative to the reference structure. The
    transformation matrix relating the two is then determined by a search, which is
    more expensive than the rounding that suffices when the two structures adhere to
    the same crystallographic setting. The returned structure is always expressed in
    the setting of the reference structure.

    A rigid translation of the input structure relative to the reference structure is
    detected and removed, unless :attr:`find_translation` is set to ``False``.

    The reference structure has to be periodic along at least two directions. A slab is
    therefore mapped, with the amount and the direction of its vacuum having no bearing on the
    outcome, whereas a wire or a molecule is refused: the cell of a structure periodic along
    one direction is unchanged by a rotation about that direction, and a structure periodic
    along none has no cell vector that means anything, so in neither case does the cell
    determine the orientation.

    **Vacancies.** The reference structure provides the sites and the input structure
    provides the atoms. If there are fewer atoms than sites, the sites that no atom is
    assigned to are vacant and come out carrying the species ``X``, which is how a
    vacancy is denoted in :program:`icet`. Which sites end up vacant is decided by the
    assignment and is not under the control of the caller: leaving a site vacant carries
    no direct cost for the underlying Hungarian algorithm, so the vacancies are placed
    wherever they leave the remaining atoms closest to their sites. A vacant site carries
    no displacement, so ``Displacement``, ``Displacement_Magnitude`` and
    ``Minimum_Distances`` are undefined there and ``IndexMapping`` is ``-1``; accordingly
    ``drmax`` and ``dravg`` are taken over the atoms that are present rather than over the
    sites. This is also the reason for :attr:`inert_species`: an input structure with
    vacancies has fewer atoms than the reference structure has sites, so rescaling the
    volume by the total number of atoms would be wrong and only the species that are never
    substituted for a vacancy may be counted.

    **Interstitials.** Interstitials are handled by making the interstitial sites part of
    the reference structure. The sites that are not occupied in a particular input
    structure then come out as vacancies, which is how, for example, hydrogen in a metal
    is treated. The converse is not supported: an input structure cannot contain atoms
    for which the reference structure provides no site, and attempting it raises a
    :class:`ValueError`. There is no mechanism for introducing a site that the reference
    structure does not define.

    Parameters
    ----------
    structure
        Input structure, typically a relaxed structure.
    reference
        Reference structure, which can but need not be the primitive structure.
    inert_species
        List of chemical symbols (e.g., ``['Au', 'Pd']``) that are never
        substituted for a vacancy. The number of inert sites is used to rescale
        the volume of the input structure to match the reference structure.
    tol_positions
        Tolerance factor applied when scanning for overlapping positions in
        Ångstrom (forwarded to :func:`ase.build.make_supercell`).
    tol_cell
        Largest acceptable deviation of the cell metric of the input structure
        from an integer transformation of the reference cell metric, measured as
        the largest absolute eigenvalue of the residual Biot strain tensor. This
        measure is invariant under a rotation of either cell and independent of
        the size of the cells. For a structure that is not periodic along every
        direction it covers the subspace spanned by the periodic cell vectors
        alone, since the extent of the cell along the other directions is
        arbitrary. A strongly strained input structure may require a larger
        value.
    symprec
        Tolerance imposed when analyzing the symmetry of the reference structure
        using :program:`spglib`. The symmetry is used to discard candidate
        transformation matrices that describe the same mapping.
    find_translation
        If ``True`` a rigid offset of the input structure relative to the reference
        structure is removed before the atoms are assigned to the sites. The offset
        is only removed if doing so reduces the average relaxation distance by at
        least a factor of two, so that a structure that is already aligned is left
        alone. The offset that was removed is reported as ``translation``.
    trigger_levels
        Levels at which the warnings are triggered, for those that are to deviate from
        the defaults. Levels that are not given keep their default value, and an
        unknown key raises a :class:`ValueError` that lists the valid ones. The valid
        keys and their default values are

        * ``volumetric_strain`` (0.25), the absolute volumetric strain,
        * ``anisotropic_strain`` (0.1), the difference between the largest and the
          smallest eigenvalue of the strain tensor,
        * ``maximum_displacement`` (1.0 Å), the largest distance between a relaxed
          position and its site,
        * ``average_displacement`` (0.5 Å), the average distance between the relaxed
          positions and their sites,
        * ``maximum_displacement_fraction`` (0.3), the same as a fraction of the distance
          between two neighbouring sites, since whether a displacement is large depends on
          the lattice,
        * ``average_displacement_fraction`` (0.15), likewise for the average,
        * ``ambiguity_tolerance`` (1e-6 Å), the slack allowed when deciding whether an
          atom was assigned to a site further away than the closest one,
        * ``ambiguity_ratio`` (0.9), the fraction of the distance to the second closest
          site beyond which an atom counts as almost equally far from both.

        Setting :attr:`assume_no_cell_relaxation` to ``True`` tightens the defaults for
        ``volumetric_strain`` and ``anisotropic_strain`` to 1e-3, which an entry given
        here then overrides in turn.
    suppress_warnings
        If ``True`` no warnings are printed. They are still reported in the
        supplementary information, so that they can be inspected programmatically.
    assume_no_cell_relaxation
        If ``True`` the volume and cell metric of the input structure are *not*
        rescaled to match the reference structure. Skipping the rescaling can be
        advantageous for some structures, e.g., with many vacancies. Note that the input
        structure must then be obtainable via an *integer* transformation matrix from the
        reference cell metric, i.e. it should not involve relaxations of the volume or of
        the cell metric.

    Raises
    ------
    ValueError
        If the boundary conditions of the two structures do not match.
    ValueError
        If either structure contains no atoms or has a cell of less than full rank.
    ValueError
        If a species given as :attr:`inert_species` occupies no site of one of them.
    ValueError
        If no integer transformation of the reference cell reproduces the input cell.
    ValueError
        If the input structure has more atoms than the reference structure has sites.
    ValueError
        If :attr:`trigger_levels` contains a key that is not a known trigger level.

    Example
    -------
    The following code snippet illustrates the general usage. It first creates
    a primitive FCC cell, which is latter used as reference structure. To
    emulate a relaxed structure obtained from, e.g., a density functional
    theory calculation, the code then creates a 4x4x4 conventional FCC
    supercell, which is populated with two different atom types, has distorted
    cell vectors, and random displacements to the atoms. Finally, the present
    function is used to map the structure back the ideal lattice::

        >>> from ase.build import bulk
        >>> reference = bulk('Au', a=4.09)
        >>> structure = bulk('Au', cubic=True, a=4.09).repeat(4)
        >>> structure.symbols = 10 * ['Ag'] + (len(structure) - 10) * ['Au']
        >>> structure.set_cell(structure.cell * 1.02, scale_atoms=True)
        >>> structure.rattle(0.1, seed=42)
        >>> mapped_structure, info = map_structure_to_reference(structure, reference)
        >>> print('{:.4f}'.format(info['dravg']))
        0.1541
    """

    # Obtain supercell of reference structure that is compatible
    # with relaxed structure
    reference_supercell, P, reduced_translation = get_reference_supercell(
        structure, reference, inert_species=inert_species,
        tol_positions=tol_positions, tol_cell=tol_cell, symprec=symprec,
        assume_no_cell_relaxation=assume_no_cell_relaxation)

    # The strain and its decomposition describe the periodic subspace, the cell vectors
    # along the other directions being replaced by an orthonormal basis of its complement.
    # Reporting them for the cells as they stand would let the amount and the direction of
    # vacuum enter, and a slab whose cell is skewed would appear strained by that alone.
    reference_frame = get_periodic_frame(reference_supercell.cell, reference.pbc)
    structure_frame = get_periodic_frame(structure.cell, reference.pbc)

    # Calculate strain tensor
    strain_tensor = calculate_strain_tensor(reference_frame, structure_frame)

    # Symmetric matrix has real eigenvalues
    eigenvalues = calculate_strain_eigenvalues(strain_tensor)
    volumetric_strain = calculate_volumetric_strain(strain_tensor)
    logger.debug('Eigenvalues of the strain tensor: {}, volumetric strain: {:.6f}'.format(
        np.round(eigenvalues, 6), volumetric_strain))

    # Separate the deformation into its change of volume, change of shape and rotation.
    # The rotation is reduced over the symmetry of the reference structure, since a
    # supercell related to the chosen one by a symmetry operation describes the same
    # crystal and would otherwise give a different angle.
    deformation = CellDeformation(reference_frame, structure_frame)

    # The rotation comes from the periodic cell vectors rather than from the frames above.
    # A frame completes the periodic vectors with a basis of what is left, and that basis is
    # only determined where one direction is left over, so for a structure periodic along a
    # single direction the frames of two cells can differ by a rotation that neither structure
    # has undergone, or agree although one has been turned.
    operations = get_point_group_operations(reference, symprec)
    disorientation_angle, disorientation_axis = calculate_disorientation(
        deformation.rotation, operations)
    logger.debug('Volume dilation {:.6f}, isochoric eigenstrains {}, disorientation {:.4f} '
                 'degrees about {} (from {:.4f} degrees before reducing over {} '
                 'operations)'.format(
                     deformation.volume_dilation,
                     np.round(deformation.isochoric_strain_eigenvalues, 6),
                     disorientation_angle, np.round(disorientation_axis, 4),
                     deformation.rotation_angle, len(operations)))

    # Express the input structure in the cell of the supercell it is mapped onto. The
    # positions follow the periodic cell vectors and keep their Cartesian component along the
    # remaining directions, since the extent of the cell along those is arbitrary and scaling
    # by it would move the atoms.
    structure_scaled = structure.copy()
    structure_scaled.positions = transfer_positions(
        structure.positions, structure_frame, reference_frame)
    structure_scaled.set_cell(reference_supercell.cell, scale_atoms=False)

    # Remove a rigid offset of the input structure relative to the reference
    # structure. The offset is only non-zero if it improves the agreement of the
    # positions substantially, so that a structure that is already aligned is left
    # alone rather than being displaced by a spurious offset.
    translation = np.zeros(3)
    if find_translation and np.abs(reduced_translation).max() > 1e-12:
        # the offset comes back in the coordinates it was sought in, which are those of the
        # frame of the reference structure rather than of its cell
        translation = np.dot(reduced_translation,
                             get_periodic_frame(reference.cell, reference.pbc))
        logger.debug('Removing a rigid offset of {} Angstrom, which is {} in reduced '
                     'coordinates of the reference cell'.format(np.round(translation, 5),
                                                                np.round(reduced_translation, 5)))
        structure_scaled.positions -= translation
        structure_scaled.wrap()

    # Match positions
    mapped_structure = match_positions(structure_scaled, reference_supercell)
    drmax, dravg = get_displacement_metrics(mapped_structure)

    # Collect the warnings unconditionally, so that they are reported in the
    # supplementary information even when they are not printed
    levels = get_trigger_levels(assume_no_cell_relaxation, trigger_levels)
    warnings, ambiguous_sites = collect_warnings(mapped_structure, volumetric_strain,
                                                 eigenvalues, drmax, dravg, levels,
                                                 get_minimum_site_distance(reference))
    n_vacancies = mapped_structure.get_chemical_symbols().count('X')
    logger.debug('Assigned {} atoms to {} sites, leaving {} vacant; maximum relaxation '
                 'distance {:.5f} Angstrom, average {:.5f} Angstrom, {} ambiguous '
                 'site(s)'.format(len(structure), len(mapped_structure), n_vacancies,
                                  drmax, dravg, len(ambiguous_sites)))

    warning_tags = []
    for tag, message in warnings:
        if tag not in warning_tags:
            warning_tags.append(tag)
        if not suppress_warnings:
            logger.warning(message)

    # Populate dictionary with supplementary information
    result = StructureMapping(
        drmax=drmax,
        dravg=dravg,
        transformation_matrix=P,
        translation=translation,
        ambiguous_sites=ambiguous_sites,
        warnings=warning_tags,
        strain_tensor=strain_tensor,
        strain_tensor_eigenvalues=eigenvalues,
        volumetric_strain=volumetric_strain,
        volume_dilation=deformation.volume_dilation,
        isochoric_strain=deformation.isochoric_strain,
        isochoric_strain_eigenvalues=deformation.isochoric_strain_eigenvalues,
        eigenstrain_norm=deformation.eigenstrain_norm,
        eigenstrain_rms=deformation.eigenstrain_rms,
        von_mises_strain=deformation.von_mises_strain,
        disorientation_angle=disorientation_angle,
        disorientation_axis=disorientation_axis,
        rotation=deformation.rotation)

    return mapped_structure, result
