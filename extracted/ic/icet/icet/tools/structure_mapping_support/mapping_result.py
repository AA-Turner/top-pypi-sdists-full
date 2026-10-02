"""
The result of mapping a structure onto a reference structure.
"""

from dataclasses import dataclass, fields
from collections.abc import Iterator, Mapping

import numpy as np

STR_WIDTH = 54
"""Width of the string representation."""


@dataclass(frozen=True, eq=False)
class StructureMapping(Mapping):
    """Supplementary information about a mapping of a structure onto a reference
    structure, as returned by :func:`map_structure_to_reference
    <icet.tools.map_structure_to_reference>`.

    The quantities are reached as attributes, which is the intended form. The class is at
    the same time a read-only mapping, so ``result['drmax']``, ``result.get('drmax')``,
    ``result.keys()``, ``result.items()``, ``result.values()``, ``'drmax' in result`` and
    ``len(result)`` all behave as they do for a dictionary. That is there so that code
    written against the dictionary that this class replaces continues to work.

    Nothing can be assigned to, and neither can the contents of what is handed out: the
    arrays are not writeable and the sequences are tuples. Instances are therefore not
    hashable, as a mapping is not.

    Attributes
    ----------
    drmax
        Largest distance in Ångstrom between a position of the input structure and the
        site it was assigned to.
    dravg
        Average of that distance over the atoms. Both are taken over the atoms that are
        present rather than over the sites, so vacancies do not dilute them.
    transformation_matrix
        Integer matrix relating the cell of the reference structure to that of the
        returned supercell.
    translation
        Rigid offset in Ångstrom that was removed from the input structure, which
        vanishes if none was removed.
    ambiguous_sites
        Sites whose assignment is ambiguous, either because the atom was assigned past a
        closer site or because it is almost equally far from two sites.
    warnings
        Tags of the warnings that were triggered, reported whether or not they were
        printed.
    strain_tensor
        Biot strain tensor of the input structure relative to the returned supercell.
    strain_tensor_eigenvalues
        Its three eigenvalues in ascending order.
    volumetric_strain
        Relative change of the volume.
    volume_dilation
        Ratio of the volumes, i.e. the volumetric strain plus one.
    isochoric_strain
        Biot strain tensor of the volume-preserving part of the deformation, which
        describes the change of shape alone.
    isochoric_strain_eigenvalues
        Its three eigenvalues in ascending order.
    eigenstrain_norm
        Norm of those eigenvalues, a single measure of the change of shape.
    eigenstrain_rms
        Root mean square of those eigenvalues.
    von_mises_strain
        Von Mises strain of the isochoric strain, the conventional measure of the change
        of shape. For small strains it is the eigenstrain norm divided by the square root
        of three halves.
    disorientation_angle
        Angle of the rotation in degrees, reduced over the symmetry of the reference
        structure. A supercell related to the returned one by a symmetry operation
        describes the same crystal, so this is the smallest angle among the descriptions
        that the structure cannot tell apart, and it is the rotation that is meaningful on
        its own.
    disorientation_axis
        Unit vector in Cartesian coordinates that the disorientation is taken about. It
        belongs to the same description as :attr:`disorientation_angle`, so the two
        together give that rotation, and it is not the axis of :attr:`rotation`. It
        vanishes if the angle does, since a vanishing rotation has no axis, and it is not
        determined by the crystal if the misorientation lies on a symmetry element, in
        which case one of the equivalent axes is reported.
    rotation
        Rotation relating the returned supercell to the cell of the input structure. It
        describes the cells and is defined only up to a symmetry operation of the
        reference structure, so its angle can be much larger than
        :attr:`disorientation_angle`; a misorientation of twenty degrees can appear here
        as one hundred and seventy two.
    """

    drmax: float
    dravg: float
    transformation_matrix: np.ndarray
    translation: np.ndarray
    ambiguous_sites: tuple
    warnings: tuple
    strain_tensor: np.ndarray
    strain_tensor_eigenvalues: np.ndarray
    volumetric_strain: float
    volume_dilation: float
    isochoric_strain: np.ndarray
    isochoric_strain_eigenvalues: np.ndarray
    eigenstrain_norm: float
    eigenstrain_rms: float
    von_mises_strain: float
    disorientation_angle: float
    disorientation_axis: np.ndarray
    rotation: np.ndarray

    def __post_init__(self) -> None:
        """Makes the quantities read-only.

        Freezing the dataclass only prevents a field from being assigned to, so an array or
        a list handed out could still be modified in place, which would alter what is
        reported for a mapping after the fact. The arrays are copied and marked as not
        writeable, and the sequences are stored as tuples.
        """
        for entry in fields(self):
            value = getattr(self, entry.name)
            if isinstance(value, np.ndarray):
                frozen = np.array(value)
                frozen.flags.writeable = False
                object.__setattr__(self, entry.name, frozen)
            elif isinstance(value, list):
                object.__setattr__(self, entry.name, tuple(value))

    def __getitem__(self, key: str):
        """Returns a quantity by name, for compatibility with the dictionary that this
        class replaces. Prefer attribute access."""
        # the names are taken from the fields rather than from keys(), since the view that
        # keys() returns tests membership through this method and would recurse
        names = [entry.name for entry in fields(self)]
        if key not in names:
            raise KeyError('{} is not among the quantities reported for a mapping; '
                           'the available ones are {}.'.format(key, ', '.join(names)))
        return getattr(self, key)

    def __iter__(self) -> Iterator[str]:
        return (entry.name for entry in fields(self))

    def __len__(self) -> int:
        return len(fields(self))

    def __eq__(self, other) -> bool:
        """Returns whether two results report the same quantities throughout.

        Defined here because the comparison that a mapping provides comes down to comparing
        two dictionaries, which is ambiguous for the fields that are arrays.
        """
        if not isinstance(other, StructureMapping):
            return NotImplemented
        for name in self:
            mine, theirs = self[name], other[name]
            if isinstance(mine, np.ndarray) or isinstance(theirs, np.ndarray):
                if not np.array_equal(mine, theirs):
                    return False
            elif mine != theirs:
                return False
        return True

    def __str__(self) -> str:
        s = []
        s += ['{s:=^{n}}'.format(s=' Structure Mapping ', n=STR_WIDTH)]
        s += [' {:32} : {:.5f}'.format('maximum relaxation distance', self.drmax)]
        s += [' {:32} : {:.5f}'.format('average relaxation distance', self.dravg)]
        s += [' {:32} : {}'.format('translation', np.round(self.translation, 4))]
        s += [' {:32} : {:.5f}'.format('volume dilation', self.volume_dilation)]
        s += [' {:32} : {:.5f}'.format('volumetric strain', self.volumetric_strain)]
        s += [' {:32} : {}'.format('strain eigenvalues',
                                   np.round(self.strain_tensor_eigenvalues, 5))]
        s += [' {:32} : {}'.format('isochoric eigenstrains',
                                   np.round(self.isochoric_strain_eigenvalues, 5))]
        s += [' {:32} : {:.5f}'.format('eigenstrain norm', self.eigenstrain_norm)]
        s += [' {:32} : {:.5f}'.format('von Mises strain', self.von_mises_strain)]
        s += [' {:32} : {:.4f}'.format('disorientation angle (deg)', self.disorientation_angle)]
        s += [' {:32} : {}'.format('disorientation axis',
                                   np.round(self.disorientation_axis, 4))]
        s += [' {:32} : {}'.format('number of ambiguous sites', len(self.ambiguous_sites))]
        s += [' {:32} : {}'.format('warnings', ', '.join(self.warnings) or 'none')]
        s += [''.center(STR_WIDTH, '=')]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        """ HTML representation. Used, e.g., in jupyter notebooks. """
        rows = [('Maximum relaxation distance', '{:.5f}'.format(self.drmax)),
                ('Average relaxation distance', '{:.5f}'.format(self.dravg)),
                ('Translation', str(np.round(self.translation, 4))),
                ('Volume dilation', '{:.5f}'.format(self.volume_dilation)),
                ('Volumetric strain', '{:.5f}'.format(self.volumetric_strain)),
                ('Strain eigenvalues', str(np.round(self.strain_tensor_eigenvalues, 5))),
                ('Isochoric eigenstrains',
                 str(np.round(self.isochoric_strain_eigenvalues, 5))),
                ('Eigenstrain norm', '{:.5f}'.format(self.eigenstrain_norm)),
                ('Von Mises strain', '{:.5f}'.format(self.von_mises_strain)),
                ('Disorientation angle (deg)', '{:.4f}'.format(self.disorientation_angle)),
                ('Disorientation axis', str(np.round(self.disorientation_axis, 4))),
                ('Number of ambiguous sites', str(len(self.ambiguous_sites))),
                ('Warnings', ', '.join(self.warnings) or 'none')]

        s = ['<h4>Structure Mapping</h4>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>']
        s += ['<tbody>']
        for label, value in rows:
            s += ['<tr><td style="text-align: left;">{}</td><td>{}</td></tr>'.format(
                label, value)]
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)
