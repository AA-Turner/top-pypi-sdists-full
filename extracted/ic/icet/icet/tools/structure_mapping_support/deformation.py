"""
Decomposition of the deformation relating two cells.

The total Biot strain relating two cells mixes the change of the volume with the
change of the shape and discards the rotation. This module separates the three,
which is useful when the parts are to be judged individually, for example when
deciding whether a relaxation changed the shape of a cell or merely its size.
"""

from dataclasses import dataclass, field

import numpy as np
import scipy.linalg
from scipy.spatial.transform import Rotation

STR_WIDTH = 40
"""Width of the string representation."""

ROTATION_ANGLE_TOLERANCE = 1e-9
"""Angle in radians below which a rotation counts as absent and its axis as undefined.

An exact comparison against zero does not do, because the rotation obtained from a
deformation that is free of rotation is the identity only to within numerical
precision. Normalizing the resulting rotation vector would turn that noise into an
arbitrary unit vector."""


def _check_cell_shape(name: str, cell: np.ndarray) -> np.ndarray:
    """Returns the cell as an array of floats, checking that it is a 3x3 matrix.

    Parameters
    ----------
    name
        Name used for the cell in the error message.
    cell
        Cell metric.

    Raises
    ------
    ValueError
        If the cell is not a 3x3 matrix.
    """
    cell = np.asarray(cell, dtype=np.float64)
    if cell.shape != (3, 3):
        raise ValueError('Cell {} is not a 3x3 matrix, its shape is {}.'.format(
            name, cell.shape))
    return cell


@dataclass(frozen=True, eq=False)
class CellDeformation:
    """Decomposition of the deformation relating a reference cell to a target cell.

    The deformation gradient :math:`F` is written as a change of the volume, a
    change of the shape and a rotation,

    .. math::

        F = R \\, J^{1/3} \\, (E + I),

    where :math:`J` is the volume dilation, :math:`R` is the rotation, and
    :math:`E` is the isochoric Biot strain tensor, which describes the change of
    the shape alone and vanishes if the two cells differ only in size and
    orientation.

    This class is internal to the structure mapping. The quantities it provides are
    reported by :func:`map_structure_to_reference
    <icet.tools.map_structure_to_reference>`, which knows about the atoms as well and
    can therefore say what a rotation means for the structure rather than only for the
    cells.

    Parameters
    ----------
    reference_cell
        Reference cell (row-major format).
    target_cell
        Target cell (row-major format).

    Raises
    ------
    ValueError
        If either cell is not a 3x3 matrix.
    ValueError
        If the cells are of opposite handedness or either one is singular.

    Example
    -------
    A cell that is inflated by two percent has a volume dilation of about six
    percent but no change of shape and no rotation::

        >>> import numpy as np
        >>> from icet.tools.structure_mapping_support.deformation import CellDeformation
        >>> A = np.array([[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]])
        >>> deformation = CellDeformation(A, 1.02 * A)
        >>> round(deformation.volume_dilation, 6)
        1.061208
        >>> round(float(np.abs(deformation.isochoric_strain).max()), 12)
        0.0
        >>> round(deformation.rotation_angle, 12)
        0.0
    """

    reference_cell: np.ndarray
    target_cell: np.ndarray

    _deformation_gradient: np.ndarray = field(init=False, repr=False)
    _volume_dilation: float = field(init=False, repr=False)
    _rotation: np.ndarray = field(init=False, repr=False)
    _isochoric_strain: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        reference_cell = _check_cell_shape('A', self.reference_cell)
        target_cell = _check_cell_shape('B', self.target_cell)

        deformation_gradient = np.linalg.solve(reference_cell, target_cell).T
        volume_dilation = float(np.linalg.det(deformation_gradient))
        if volume_dilation <= 0:
            msg = ('The two cells are of opposite handedness or one of them is singular, so '
                   'they are not related by a rotation and a strain.')
            msg += '\n  determinant of the deformation gradient: ' + str(volume_dilation)
            raise ValueError(msg)

        # the volume-preserving part, whose determinant is one by construction
        rotation, stretch = scipy.linalg.polar(deformation_gradient / np.cbrt(volume_dilation))

        # the class is frozen, so the derived quantities are assigned this way
        for name, value in (('reference_cell', reference_cell),
                            ('target_cell', target_cell),
                            ('_deformation_gradient', deformation_gradient),
                            ('_volume_dilation', volume_dilation),
                            ('_rotation', rotation),
                            ('_isochoric_strain', stretch - np.eye(3))):
            object.__setattr__(self, name, value)

    @property
    def deformation_gradient(self) -> np.ndarray:
        """Deformation gradient in column-major format."""
        return self._deformation_gradient

    @property
    def volume_dilation(self) -> float:
        """Ratio of the volume of the target cell to that of the reference cell."""
        return self._volume_dilation

    @property
    def rotation(self) -> np.ndarray:
        """Rotation relating the two cells, a proper orthogonal matrix."""
        return self._rotation

    @property
    def isochoric_strain(self) -> np.ndarray:
        """Biot strain tensor of the volume-preserving part of the deformation."""
        return self._isochoric_strain

    @property
    def strain_tensor(self) -> np.ndarray:
        """Biot strain tensor of the whole deformation, including the change of volume.

        This is what :func:`calculate_strain_tensor
        <icet.tools.structure_mapping_support.strain.calculate_strain_tensor>` returns.
        """
        scale = np.cbrt(self.volume_dilation)
        return scale * (self.isochoric_strain + np.eye(3)) - np.eye(3)

    @property
    def volumetric_strain(self) -> float:
        """Relative change of the volume, i.e. the volume dilation minus one.

        This is the quantity reported as ``volumetric_strain`` by
        :func:`map_structure_to_reference <icet.tools.map_structure_to_reference>`.
        """
        return self.volume_dilation - 1

    @property
    def isochoric_strain_eigenvalues(self) -> np.ndarray:
        """Eigenvalues of the isochoric strain tensor in ascending order.

        They sum to zero to first order and describe the elongation along the three
        principal directions of the change of shape.
        """
        return np.linalg.eigvalsh(self.isochoric_strain)

    @property
    def eigenstrain_norm(self) -> float:
        """Norm of the eigenvalues of the isochoric strain tensor.

        A single number describing how much the shape of the cell changed.
        """
        return float(np.linalg.norm(self.isochoric_strain_eigenvalues))

    @property
    def eigenstrain_rms(self) -> float:
        """Root mean square of the eigenvalues of the isochoric strain tensor."""
        return self.eigenstrain_norm / np.sqrt(3)

    @property
    def von_mises_strain(self) -> float:
        """Von Mises strain of the isochoric strain tensor.

        This is the conventional measure of the change of shape in the mechanics
        literature. For small strains it is related to :attr:`eigenstrain_norm` by a
        factor of the square root of three halves, from which it departs by a few
        parts per thousand at a strain of twenty percent.
        """
        deviatoric = self.isochoric_strain - np.trace(self.isochoric_strain) / 3 * np.eye(3)
        return float(np.sqrt(2 * (deviatoric ** 2).sum() / 3))

    @property
    def strain_pseudo_angle(self) -> float:
        """Arc tangent of :attr:`eigenstrain_rms` in degrees.

        A measure of the change of shape on a scale of degrees, which saturates rather
        than growing without bound as the strain becomes large.
        """
        return float(np.degrees(np.arctan(self.eigenstrain_rms)))

    @property
    def rotation_angle(self) -> float:
        """Angle of the rotation in degrees, between zero and 180.

        Note that the rotation relating two cells of a crystal is only defined up to a
        symmetry operation of that crystal. See :func:`calculate_disorientation_angle
        <icet.tools.calculate_disorientation_angle>`.
        """
        angle = np.linalg.norm(self._rotation_vector)
        if angle < ROTATION_ANGLE_TOLERANCE:
            return 0.0
        return float(np.degrees(angle))

    @property
    def rotation_axis(self) -> np.ndarray:
        """Axis of the rotation as a unit vector.

        The zero vector is returned if there is no rotation, in which case the axis is
        undefined.
        """
        rotation_vector = self._rotation_vector
        norm = np.linalg.norm(rotation_vector)
        if norm < ROTATION_ANGLE_TOLERANCE:
            return np.zeros(3)
        return rotation_vector / norm

    @property
    def _rotation_vector(self) -> np.ndarray:
        """Rotation vector, whose norm is the angle in radians."""
        return Rotation.from_matrix(self.rotation).as_rotvec()

    def reconstruct_target_cell(self, reference_cell: np.ndarray) -> np.ndarray:
        """Returns the target cell, rebuilt from the parts of the decomposition.

        This is the inverse of :func:`from_cells` and is mainly useful for checking that
        the decomposition is complete.

        Parameters
        ----------
        reference_cell
            Reference cell (row-major format), the one the decomposition was obtained
            with.

        Raises
        ------
        ValueError
            If the cell is not a 3x3 matrix.
        """
        reference_cell = _check_cell_shape('A', reference_cell)
        scale = np.cbrt(self.volume_dilation)
        deformation_gradient = self.rotation @ (scale * (self.isochoric_strain + np.eye(3)))
        return (deformation_gradient @ reference_cell.T).T

    def to_dict(self) -> dict:
        """Returns the decomposition as a dictionary, for writing to a record or a log."""
        return {'deformation_gradient': self.deformation_gradient,
                'volume_dilation': self.volume_dilation,
                'volumetric_strain': self.volumetric_strain,
                'rotation': self.rotation,
                'rotation_angle': self.rotation_angle,
                'rotation_axis': self.rotation_axis,
                'isochoric_strain': self.isochoric_strain,
                'isochoric_strain_eigenvalues': self.isochoric_strain_eigenvalues,
                'eigenstrain_norm': self.eigenstrain_norm,
                'eigenstrain_rms': self.eigenstrain_rms,
                'von_mises_strain': self.von_mises_strain,
                'strain_pseudo_angle': self.strain_pseudo_angle}

    def __str__(self) -> str:
        s = []
        s += ['{s:=^{n}}'.format(s=' Cell Deformation ', n=STR_WIDTH)]
        s += [' {:24} : {:.6f}'.format('volume dilation', self.volume_dilation)]
        s += [' {:24} : {:.6f}'.format('volumetric strain', self.volumetric_strain)]
        s += [' {:24} : {:.4f}'.format('rotation angle (deg)', self.rotation_angle)]
        s += [' {:24} : {}'.format('rotation axis', np.round(self.rotation_axis, 4))]
        s += [' {:24} : {}'.format('isochoric eigenstrains',
                                   np.round(self.isochoric_strain_eigenvalues, 6))]
        s += [' {:24} : {:.6f}'.format('eigenstrain norm', self.eigenstrain_norm)]
        s += [' {:24} : {:.6f}'.format('eigenstrain rms', self.eigenstrain_rms)]
        s += [' {:24} : {:.6f}'.format('von Mises strain', self.von_mises_strain)]
        s += [' {:24} : {:.4f}'.format('pseudo angle (deg)', self.strain_pseudo_angle)]
        s += [''.center(STR_WIDTH, '=')]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        """ HTML representation. Used, e.g., in jupyter notebooks. """
        s = ['<h4>Cell Deformation</h4>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>']
        s += ['<tbody>']
        s += ['<tr><td style="text-align: left;">Volume dilation</td>'
              f'<td>{self.volume_dilation:.6f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Volumetric strain</td>'
              f'<td>{self.volumetric_strain:.6f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Rotation angle (deg)</td>'
              f'<td>{self.rotation_angle:.4f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Rotation axis</td>'
              f'<td>{np.round(self.rotation_axis, 4)}</td></tr>']
        s += ['<tr><td style="text-align: left;">Isochoric eigenstrains</td>'
              f'<td>{np.round(self.isochoric_strain_eigenvalues, 6)}</td></tr>']
        s += ['<tr><td style="text-align: left;">Eigenstrain norm</td>'
              f'<td>{self.eigenstrain_norm:.6f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Eigenstrain RMS</td>'
              f'<td>{self.eigenstrain_rms:.6f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Von Mises strain</td>'
              f'<td>{self.von_mises_strain:.6f}</td></tr>']
        s += ['<tr><td style="text-align: left;">Strain pseudo angle (deg)</td>'
              f'<td>{self.strain_pseudo_angle:.4f}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)
