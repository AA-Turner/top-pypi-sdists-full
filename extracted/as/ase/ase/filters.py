"""Filters"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Never
from warnings import warn

import numpy as np
import numpy.typing as npt

from ase.calculators.calculator import PropertyNotImplementedError
from ase.stress import full_3x3_to_voigt_6_stress, voigt_6_to_full_3x3_stress
from ase.utils import deprecated
from ase.utils.abc import Optimizable

if TYPE_CHECKING:
    from ase import Atom, Atoms
    from ase.calculators.calculator import BaseCalculator
    from ase.cell import Cell
    from ase.constraints.constraint import FixConstraint


__all__ = [
    'Filter',
    'StrainFilter',
    'UnitCellFilter',
    'FrechetCellFilter',
    'ExpCellFilter',
]


class OptimizableFilter(Optimizable):
    def __init__(self, filterobj: Filter) -> None:
        self.filterobj = filterobj

    def get_x(self) -> npt.NDArray[np.floating]:
        return self.filterobj.get_positions().ravel()

    def set_x(self, x: npt.NDArray[np.floating]) -> None:
        self.filterobj.set_positions(x.reshape(-1, 3))

    def get_gradient(self) -> np.ndarray:
        return -self.filterobj.get_forces().ravel()

    @cached_property
    def _use_force_consistent_energy(self) -> bool:
        # This boolean is in principle invalidated if the
        # calculator changes.  This can lead to weird things
        # in multi-step optimizations.
        try:
            self.filterobj.get_potential_energy(force_consistent=True)
        except PropertyNotImplementedError:
            return False
        else:
            return True

    def get_value(self) -> float:
        force_consistent = self._use_force_consistent_energy
        return self.filterobj.get_potential_energy(
            force_consistent=force_consistent
        )

    def ndofs(self) -> int:
        return 3 * len(self.filterobj)

    def iterimages(self) -> Atoms:
        return self.filterobj.iterimages()


class Filter:
    def __init__(
        self,
        atoms: Atoms,
        indices=None,
        mask: np.ndarray | None = None,
    ):
        """Filter "hiding" specified atoms.

        This filter "hides" some atoms in the ASE :class:`~ase.Atoms` object
        and thus fixes their positions during structure optimization.

        This can be used as an alternative to the
        :class:`~ase.constraints.FixAtoms` constraint.

        Parameters
        ----------
        atoms : :class:`~ase.Atoms`
            ASE :class:`~ase.Atoms` object.
        indices : list[int] | None, default: None
           Indices for of the atoms that should remain visible.
        mask : np.ndarray | None, default: None
           One boolean per atom indicating if the atom should remain
           visible or not.

        Notes
        -----
        You must supply either ``indices`` or ``mask``.

        If :class:`~ase.io.Trajectory` tries to save this object,
        it will instead save the underlying :class:`~ase.Atoms` object.
        To prevent this, override the :meth:`~Filter.iterimages` method.

        Examples
        --------
        >>> from ase.build import molecule
        >>> from ase.filters import Filter
        >>> atoms=molecule('H2O')
        >>> list(atoms.symbols)
        ['O', 'H', 'H']
        >>> atoms.get_positions()
        array([[ 0.      ,  0.      ,  0.119262],
               [ 0.      ,  0.763239, -0.477047],
               [ 0.      , -0.763239, -0.477047]])
        >>> f1 = Filter(atoms, indices=[1, 2])
        >>> f2 = Filter(atoms, mask=[0, 1, 1])
        >>> f3 = Filter(atoms, mask=[a.z == 1 for a in atoms])
        >>> f1.get_positions()
        array([[ 0.      ,  0.763239, -0.477047],
               [ 0.      , -0.763239, -0.477047]])

        In all three filters, only the hydrogen atoms are made visible.
        When asking for the positions, only the positions of the hydrogen atoms
        are returned.

        """

        self.atoms = atoms
        self.constraints: list[FixConstraint] = []
        # Make self.info a reference to the underlying atoms' info dictionary.
        self.info = self.atoms.info

        if indices is None and mask is None:
            raise ValueError('Use "indices" or "mask".')
        if indices is not None and mask is not None:
            raise ValueError('Use only one of "indices" and "mask".')

        if mask is not None:
            self.index = np.asarray(mask, bool)
            self.n = self.index.sum()
        else:
            self.index = np.asarray(indices, int)
            self.n = len(self.index)

    def iterimages(self) -> Atoms:
        # Present the real atoms object to Trajectory and friends
        return self.atoms.iterimages()

    def get_cell(self) -> Cell:
        """Returns the computational cell.

        The computational cell is the same as for the original system.
        """
        return self.atoms.get_cell()

    def get_pbc(self) -> npt.NDArray[np.bool_]:
        """Returns the periodic boundary conditions.

        The boundary conditions are the same as for the original system.
        """
        return self.atoms.get_pbc()

    def get_positions(self):
        "Return the positions of the visible atoms."
        return self.atoms.get_positions()[self.index]

    def set_positions(self, positions, **kwargs):
        "Set the positions of the visible atoms."
        pos = self.atoms.get_positions()
        pos[self.index] = positions
        self.atoms.set_positions(pos, **kwargs)

    positions = property(
        get_positions, set_positions, doc='Positions of the atoms'
    )

    def get_momenta(self) -> npt.NDArray[np.floating]:
        "Return the momenta of the visible atoms."
        return self.atoms.get_momenta()[self.index]

    def set_momenta(self, momenta: npt.NDArray[np.floating], **kwargs) -> None:
        "Set the momenta of the visible atoms."
        mom = self.atoms.get_momenta()
        mom[self.index] = momenta
        self.atoms.set_momenta(mom, **kwargs)

    def get_atomic_numbers(self) -> npt.NDArray[np.integer]:
        "Return the atomic numbers of the visible atoms."
        return self.atoms.get_atomic_numbers()[self.index]

    def set_atomic_numbers(
        self,
        atomic_numbers: npt.NDArray[np.integer],
    ) -> None:
        "Set the atomic numbers of the visible atoms."
        z = self.atoms.get_atomic_numbers()
        z[self.index] = atomic_numbers
        self.atoms.set_atomic_numbers(z)

    def get_tags(self) -> npt.NDArray[np.integer]:
        "Return the tags of the visible atoms."
        return self.atoms.get_tags()[self.index]

    def set_tags(self, tags: npt.NDArray[np.integer]) -> None:
        "Set the tags of the visible atoms."
        tg = self.atoms.get_tags()
        tg[self.index] = tags
        self.atoms.set_tags(tg)

    def get_forces(self, *args, **kwargs):
        return self.atoms.get_forces(*args, **kwargs)[self.index]

    def get_stress(self, *args, **kwargs) -> npt.NDArray[np.floating]:
        return self.atoms.get_stress(*args, **kwargs)

    def get_stresses(self, *args, **kwargs) -> npt.NDArray[np.floating]:
        return self.atoms.get_stresses(*args, **kwargs)[self.index]

    def get_masses(self) -> npt.NDArray[np.floating]:
        return self.atoms.get_masses()[self.index]

    def get_potential_energy(self, **kwargs):
        """Calculate potential energy.

        Returns the potential energy of the full system.
        """
        return self.atoms.get_potential_energy(**kwargs)

    def get_chemical_symbols(self) -> list[str]:
        return self.atoms.get_chemical_symbols()

    def get_initial_magnetic_moments(self) -> npt.NDArray[np.floating]:
        return self.atoms.get_initial_magnetic_moments()

    def get_calculator(self) -> BaseCalculator:
        """Returns the calculator.

        WARNING: The calculator is unaware of this filter, and sees a
        different number of atoms.
        """
        return self.atoms.calc

    @property
    def calc(self) -> BaseCalculator:
        return self.atoms.calc

    def get_celldisp(self) -> npt.NDArray[np.floating]:
        return self.atoms.get_celldisp()

    def has(self, name: str) -> bool:
        "Check for existence of array."
        return self.atoms.has(name)

    def __len__(self) -> int:
        "Return the number of movable atoms."
        return self.n

    def __getitem__(self, i: int) -> Atom:
        "Return an atom."
        return self.atoms[self.index[i]]

    def __ase_optimizable__(self) -> OptimizableFilter:
        return OptimizableFilter(self)


class StrainFilter(Filter):
    def __init__(
        self,
        atoms: Atoms,
        mask: np.ndarray | None = None,
        include_ideal_gas: bool = False,
    ) -> None:
        """Filter applying a homogeneous strain to a list of atoms.

        This class is used together with an ASE optimizer in order to optimize
        the cell shape with minimizing the stress while keeping the scaled
        positions fixed.

        This class regards the strain of the cell as the generalized positions
        and the global stress tensor (times the volume) as the generalized
        force.

        The stress and strain are presented as 6-vectors, the order of the
        components follow the standard engineering practice:
        ``xx``, ``yy``, ``zz``, ``yz``, ``xz``, ``xy``.

        Parameters
        ----------
        atoms : :class:`~ase.Atoms`
            ASE :class:`~ase.Atoms` object.
        mask : np.ndarray | None, default: None
            Array of six booleans, indicating which of the six independent
            components of the strain that are allowed to become non-zero.
            The default (:obj:`None`) relaxes all the six components, i.e.,
            ``[True, True, True, True, True, True]``.
        include_ideal_gas : bool, default: False
            If True, the kinetic contribution of the stress is also considered.

        Notes
        -----
        If this filter is used together with :class:`~ase.optimize.MDMin`,
        the timestep (``dt``) to be used depends on the system size.
        0.01/x where x is a typical dimension seems like a good choice.

        """

        self.strain = np.zeros(6)
        self.include_ideal_gas = include_ideal_gas

        if mask is None:
            mask = np.ones(6)
        else:
            mask = np.array(mask)

        Filter.__init__(self, atoms=atoms, mask=mask)
        self.mask = mask
        self.origcell = atoms.get_cell()

    def get_positions(self):
        return self.strain.reshape((2, 3)).copy()

    def set_positions(self, new):
        new = new.ravel() * self.mask
        eps = np.array(
            [
                [1.0 + new[0], 0.5 * new[5], 0.5 * new[4]],
                [0.5 * new[5], 1.0 + new[1], 0.5 * new[3]],
                [0.5 * new[4], 0.5 * new[3], 1.0 + new[2]],
            ]
        )

        self.atoms.set_cell(np.dot(self.origcell, eps), scale_atoms=True)
        self.strain[:] = new

    def get_forces(self, **kwargs):
        stress = self.atoms.get_stress(include_ideal_gas=self.include_ideal_gas)
        return -self.atoms.get_volume() * (stress * self.mask).reshape((2, 3))

    def has(self, x: str) -> bool:
        return self.atoms.has(x)

    def __len__(self) -> int:
        return 2


class UnitCellFilter(Filter):
    def __init__(
        self,
        atoms: Atoms,
        mask: np.ndarray | None = None,
        cell_factor: float | None = None,
        hydrostatic_strain: bool = False,
        constant_volume: bool = False,
        orig_cell: np.ndarray | None = None,
        scalar_pressure: float = 0.0,
    ) -> None:
        r"""Filter returning the atomic forces and the cell stresses together.

        This class is used together with an ASE optimizer in order to minimize
        both the atomic forces and the cell stresses simultaneously.

        Degrees of freedom are the positions in the original undeformed cell,
        plus the deformation gradient :math:`\mathbf{F}` (extra 3 "atoms").
        If :math:`\mathbf{r}_i` denotes a Cartesian atomic position, the
        corresponding atomic degree of freedom is

        .. math::
            \mathbf{q}_i = \mathbf{F}^{-1}\mathbf{r}_i.

        Thus, when :math:`\mathbf{F}` changes while :math:`\mathbf{q}_i` is
        kept fixed, the atoms follow the cell deformation affinely,
        :math:`\mathbf{r}_i = \mathbf{F}\mathbf{q}_i`.  This separates
        homogeneous cell deformation from internal atomic displacements.
        The cell forces are the negative derivatives of the energy with
        respect to :math:`\mathbf{F}`.
        For full details, see [1]_.

        .. [1]
            E. B. Tadmor, G. S. Smith, N. Bernstein, and E. Kaxiras,
            Phys. Rev. B 59, 235 (1999).
            :doi:`10.1103/PhysRevB.59.235`

        Parameters
        ----------
        atoms : :class:`~ase.Atoms`
            ASE :class:`~ase.Atoms` object.
        mask : np.ndarray | None, default: None
            Mask indicating which of the six independent components of the
            strain are relaxed.

            - :obj:`True`: relax to zero
            - :obj:`False`: fixed, ignore this component

        cell_factor: float, default: float(len(atoms))
            Factor by which deformation gradient is multiplied to put
            it on the same scale as the positions when assembling
            the combined position/cell vector. The stress contribution to
            the forces is scaled down by the same factor. This can be thought
            of as a very simple preconditioners. Default is number of atoms
            which gives approximately the correct scaling.

        hydrostatic_strain: bool, default: False
            Constrain the cell by only allowing hydrostatic deformation.
            The virial tensor is replaced by `np.diag([np.trace(virial)] * 3)`.

            .. versionadded:: 3.17.0

        constant_volume: bool, default: False
            Project out the diagonal elements of the virial tensor to allow
            relaxations at constant volume, e.g. for mapping out an
            energy-volume curve. Note: this only approximately conserves
            the volume and breaks energy/force consistency so can only be
            used with optimizers that do require do a line minimisation
            (e.g. :class:`~ase.optimize.FIRE`).

            .. versionadded:: 3.17.0

        scalar_pressure: float, default: 0.0
            Applied pressure in eV/Å3 to use for enthalpy pV term.
            (Note: 1 eV/Å3 ≈ 160.2 GPa).
            For example, set ``1.0 * ase.units.GPa`` to provide 1 GPa.
            As above, this breaks energy/force consistency.

            .. versionadded:: 3.17.0

        Notes
        -----
        :class:`FrechetCellFilter` will probably perform better.

        Examples
        --------
        You can still use constraints on the atoms, e.g.
        :class:`~ase.constraints.FixAtoms`, to control
        the relaxation of the atoms.

        >>> from ase.build import bulk
        >>> from ase.constraints import FixAtoms
        >>> atoms = bulk('BN', 'wurtzite', a=2.55, c=4.23)
        >>> # this should be equivalent to the StrainFilter
        >>> atoms.set_constraint(FixAtoms(mask=[True for atom in atoms]))
        >>> ucf = UnitCellFilter(atoms)
        """

        from ase._4.optimize.cellutil import CellUtility

        Filter.__init__(self, atoms=atoms, indices=range(len(atoms)))
        self.atoms = atoms

        if orig_cell is None:
            orig_cell = atoms.get_cell()
        else:
            orig_cell = orig_cell

        self._utility = CellUtility(
            orig_cell.copy(),
            mask=mask,
            scalar_pressure=scalar_pressure,
            constant_volume=constant_volume,
            hydrostatic_strain=hydrostatic_strain,
        )

        self.stress = None

        if cell_factor is None:
            cell_factor = float(len(atoms))
        self.cell_factor = cell_factor
        self.copy = self.atoms.copy
        self.arrays = self.atoms.arrays

    @property
    def hydrostatic_strain(self) -> bool:
        return self._utility.hydrostatic_strain

    @hydrostatic_strain.setter
    def hydrostatic_strain(self, value: bool) -> None:
        # Probably we do not need these setters but at least one precon
        # test unwisely does hasattr() magic with these.
        self._utility.hydrostatic_strain = value

    @property
    def constant_volume(self) -> bool:
        return self._utility.constant_volume

    @constant_volume.setter
    def constant_volume(self, value: bool) -> None:
        self._utility.constant_volume = value

    @property
    def scalar_pressure(self) -> float:
        return self._utility.scalar_pressure

    @scalar_pressure.setter
    def scalar_pressure(self, value: float) -> None:
        self._utility.scalar_pressure = value

    @property
    def mask(self) -> np.ndarray:
        return self._utility.mask3x3

    @property
    def orig_cell(self) -> npt.NDArray[np.floating]:
        return self._utility.orig_cell

    @orig_cell.setter
    def orig_cell(self, value: npt.NDArray[np.floating]) -> None:
        self._utility.orig_cell[:] = value

    def deform_grad(self) -> npt.NDArray[np.floating]:
        return self._utility.deform_grad(self.atoms.cell)

    def get_positions(self):
        """
        this returns an array with shape (natoms + 3,3).

        the first natoms rows are the positions of the atoms, the last
        three rows are the deformation tensor associated with the unit cell,
        scaled by self.cell_factor.
        """
        return self._utility.get_positions_unitcellfilter(
            self.atoms.positions, self.atoms.cell, self.cell_factor
        )

    def set_positions(self, new, **kwargs):
        """
        new is an array with shape (natoms+3,3).

        the first natoms rows are the positions of the atoms, the last
        three rows are the deformation tensor used to change the cell shape.

        the new cell is first set from original cell transformed by the new
        deformation gradient, then the positions are set with respect to the
        current cell by transforming them with the same deformation gradient
        """
        self._utility.set_positions_unitcellfilter(
            new, self.atoms, self.cell_factor, **kwargs
        )

    def get_potential_energy(self, force_consistent=True):
        """
        returns potential energy including enthalpy PV term.
        """
        return self._utility.get_energy(self.atoms, force_consistent)

    def get_forces(self, **kwargs):
        """
        returns an array with shape (natoms+3,3) of the atomic forces
        and unit cell stresses.

        the first natoms rows are the forces on the atoms, the last
        three rows are the forces on the unit cell, which are
        computed from the stress tensor.
        """
        stress = self.atoms.get_stress(**kwargs)
        atoms_forces = self.atoms.get_forces(**kwargs)

        forces, modified_stress = self._utility.get_forces_unitcellfilter(
            atoms_forces,
            stress,
            cell=self.atoms.cell,
            cell_factor=self.cell_factor,
        )
        self.stress = modified_stress  # XXX what's this doing here?
        return forces

    def get_stress(self) -> Never:
        raise PropertyNotImplementedError

    def has(self, x: str) -> bool:
        return self.atoms.has(x)

    def __len__(self) -> int:
        return len(self.atoms) + 3


class FrechetCellFilter(UnitCellFilter):
    def __init__(
        self,
        atoms,
        mask=None,
        exp_cell_factor=None,
        *args,
        **kwargs,
    ):
        r"""Filter returning the atomic forces and the cell stresses together.

        This class is used together with an ASE optimizer in order to minimize
        both the atomic forces and the cell stresses simultaneously.

        .. versionadded:: 3.23.0

        Degrees of freedom are the positions in the original undeformed cell,
        plus the matrix logarithm :math:`\mathbf{U} = \log(\mathbf{F})` of the
        deformation gradient (extra 3 "atoms"). The cell forces are computed
        using the Fréchet derivative of the matrix exponential, giving the
        negative derivatives of the energy with respect to :math:`\mathbf{U}`.

        Parameters
        ----------
        exp_cell_factor : float, default: float(len(atoms))
            Scaling factor for cell variables. The cell gradients in
            :meth:`~ase.filters.FrechetCellFilter.get_forces()` is divided by
            ``exp_cell_factor``.
            By default, set the number of atoms. We recommend to set
            an extensive value for this parameter.
        *args, **kwargs
            Additional arguments passed to :class:`~ase.filters.UnitCellFilter`.

        Notes
        -----
        The original :class:`ExpCellFilter` implementation also uses the
        matrix logarithm of the deformation gradient as the cell variable,
        but its cell forces are not in general consistent with numerical
        energy derivatives. :class:`FrechetCellFilter` instead evaluates the
        required Fréchet derivatives explicitly.
        If you would like to keep the previous behavior, please use
        :class:`ExpCellFilter`.

        The derivation of gradients of energy w.r.t positions and the log of the
        deformation tensor is given in
        https://github.com/lan496/lan496.github.io/blob/main/notes/cell_grad.pdf
        """

        Filter.__init__(self, atoms=atoms, indices=range(len(atoms)))
        UnitCellFilter.__init__(
            self,
            atoms=atoms,
            mask=mask,
            *args,
            **kwargs,
        )

        # We defer the scipy import to avoid high immediate import overhead
        from scipy.linalg import expm, expm_frechet, logm

        self.expm = expm
        self.logm = logm
        self.expm_frechet = expm_frechet

        # Scaling factor for cell gradients
        if exp_cell_factor is None:
            exp_cell_factor = float(len(atoms))
        self.exp_cell_factor = exp_cell_factor

    def get_positions(self):
        return self._utility.get_positions_frechet(
            self.atoms.get_positions(),
            self.atoms.get_cell(),
            cell_factor=self.cell_factor,
            exp_cell_factor=self.exp_cell_factor,
        )

    def set_positions(self, new, **kwargs):
        self._utility.set_positions_frechet(
            new,
            self.atoms,
            cell_factor=self.cell_factor,
            exp_cell_factor=self.exp_cell_factor,
            **kwargs,
        )

    def get_forces(self, **kwargs):
        # forces on atoms are same as UnitCellFilter, we just
        # need to modify the stress contribution
        stress = self.atoms.get_stress(**kwargs)
        atoms_forces = self.atoms.get_forces(**kwargs)

        forces, convergence_crit_stress = self._utility.get_forces_frechet(
            atoms_forces=atoms_forces,
            stress=stress,
            cell=self.atoms.get_cell(),
            exp_cell_factor=self.exp_cell_factor,
        )

        self.stress = full_3x3_to_voigt_6_stress(convergence_crit_stress)
        return forces


class ExpCellFilter(UnitCellFilter):
    @deprecated(
        DeprecationWarning(
            'Use FrechetCellFilter for better convergence w.r.t. '
            'cell variables.'
        )
    )
    def __init__(
        self,
        atoms,
        mask=None,
        cell_factor=None,
        *args,
        **kwargs,
    ):
        r"""Filter returning the atomic forces and the cell stresses together.

        .. versionadded:: 3.17.0

        .. deprecated:: 3.23.0
            Use :class:`~ase.filters.FrechetCellFilter` for better convergence
            w.r.t. cell variables.

        This class is used together with an ASE optimizer in order to minimize
        both the atomic forces and the cell stresses simultaneously.

        Degrees of freedom are the positions in the original undeformed cell,
        plus the log of the deformation tensor (extra 3 "atoms").

        Parameters
        ----------
        cell_factor : float(DEPRECATED)
            Retained for backwards compatibility, but no longer used.

            .. deprecated:: 3.23.0

        *args, **kwargs
            Additional arguments passed to :class:`~ase.filters.UnitCellFilter`.

        Notes
        -----
        The implementation is based on that of Christoph Ortner in JuLIP.jl:
        https://github.com/libAtoms/JuLIP.jl/blob/expcell/src/Constraints.jl#L244

        In :class:`ExpCellFilter`, we express the deformation gradient
        :math:`\mathbf{F} \in \mathbb{R}^{3 \times 3}` as

        .. math::
            \mathbf{F} = \exp(\mathbf{U}),

        where :math:`\mathbf{U} = \log(\mathbf{F})` is used as the cell
        optimization variable.

        For a perturbation
        :math:`\mathbf{V} \in \mathbb{R}^{3 \times 3}` of
        :math:`\mathbf{U}`, the corresponding first-order change of
        :math:`\mathbf{F}` is given by the Fréchet derivative of the
        matrix exponential,

        .. math::
            L_{\exp}(\mathbf{U}, \mathbf{V})
            \equiv
            \left.
            \frac{\mathrm{d}}{\mathrm{d}t}
            \exp(\mathbf{U} + t\mathbf{V})
            \right|_{t=0}.

        Let :math:`\mathbf{S}` denote the virial tensor, defined here as
        :math:`\mathbf{S} = -\Omega \boldsymbol\sigma`, where :math:`\Omega` is
        the current cell volume and :math:`\boldsymbol\sigma` is the Cauchy
        stress tensor. Since the energy gradient with respect to
        :math:`\mathbf{F}` is :math:`-\mathbf{S}\mathbf{F}^{-\top}`,
        the directional derivative of the energy with respect to
        :math:`\mathbf{U}` is

        .. math::
            \left.
            \frac{\mathrm{d}}{\mathrm{d}t}
            E(\mathbf{U} + t\mathbf{V})
            \right|_{t=0}
            =
            [-\mathbf{S}\exp(-\mathbf{U}^{\top})]
            :
            L_{\exp}(\mathbf{U},\mathbf{V}).

        Here :math:`:` denotes the Frobenius inner product,
        :math:`\mathbf{A}:\mathbf{B}
        = \operatorname{tr}(\mathbf{A}^{\!\top}\mathbf{B})`.

        Using the integral representation of the Fréchet derivative
        and the cyclic property of the trace, this can be rewritten as

        .. math::
            [-\mathbf{S}\exp(-\mathbf{U}^{\top})]
            :
            L_{\exp}(\mathbf{U},\mathbf{V})
            =
            L_{\exp}\left(
                \mathbf{U}^{\top},
                -\mathbf{S}\exp(-\mathbf{U}^{\top})
            \right)
            :
            \mathbf{V}.

        Therefore,

        .. math::
            \left.
            \frac{\mathrm{d}}{\mathrm{d}t}
            E(\mathbf{U} + t\mathbf{V})
            \right|_{t=0}
            =
            L_{\exp}\left(
                \mathbf{U}^{\top},
                -\mathbf{S}\exp(-\mathbf{U}^{\top})
            \right)
            :
            \mathbf{V}.

        If :math:`\mathbf{U}` is symmetric, an assumption that does not hold
        in general, this reduces to

        .. math::
            \left.
            \frac{\mathrm{d}}{\mathrm{d}t}
            E(\mathbf{U} + t\mathbf{V})
            \right|_{t=0}
            =
            L_{\exp}\left(
                \mathbf{U},
                -\mathbf{S}\exp(-\mathbf{U})
            \right)
            :
            \mathbf{V}.

        Thus, under this assumption, the generalized cell force with respect to
        :math:`\mathbf{U}`, i.e. the negative energy gradient, is

        .. math::

            -\frac{\partial E}{\partial \mathbf{U}}
            = -L_{\exp}\left(\mathbf{U}, -\mathbf{S}\exp(-\mathbf{U})\right).

        """
        Filter.__init__(self, atoms=atoms, indices=range(len(atoms)))
        UnitCellFilter.__init__(
            self,
            atoms=atoms,
            mask=mask,
            cell_factor=cell_factor,
            *args,
            **kwargs,
        )
        if cell_factor is not None:
            # cell_factor used in UnitCellFilter does not affect on gradients of
            # ExpCellFilter.
            warn('cell_factor is deprecated')
        self.cell_factor = 1.0

        # We defer the scipy import to avoid high immediate import overhead
        from scipy.linalg import expm, logm

        self.expm = expm
        self.logm = logm

    def get_forces(self, **kwargs):
        forces = UnitCellFilter.get_forces(self, **kwargs)

        # forces on atoms are same as UnitCellFilter, we just
        # need to modify the stress contribution
        stress = self.atoms.get_stress(**kwargs)
        volume = self.atoms.get_volume()
        virial = -volume * (
            voigt_6_to_full_3x3_stress(stress)
            + np.diag([self.scalar_pressure] * 3)
        )

        cur_deform_grad = self.deform_grad()
        cur_deform_grad_log = self.logm(cur_deform_grad)

        if self.hydrostatic_strain:
            vtr = virial.trace()
            virial = np.diag([vtr / 3.0, vtr / 3.0, vtr / 3.0])

        # Zero out components corresponding to fixed lattice elements
        if (self.mask != 1.0).any():
            virial *= self.mask

        deform_grad_log_force_naive = virial.copy()
        Y = np.zeros((6, 6))
        Y[0:3, 0:3] = cur_deform_grad_log
        Y[3:6, 3:6] = cur_deform_grad_log
        Y[0:3, 3:6] = -virial @ self.expm(-cur_deform_grad_log)
        deform_grad_log_force = -self.expm(Y)[0:3, 3:6]
        for i1, i2 in [(0, 1), (0, 2), (1, 2)]:
            ff = 0.5 * (
                deform_grad_log_force[i1, i2] + deform_grad_log_force[i2, i1]
            )
            deform_grad_log_force[i1, i2] = ff
            deform_grad_log_force[i2, i1] = ff

        # check for reasonable alignment between naive and
        # exact search directions
        all_are_equal = np.all(
            np.isclose(deform_grad_log_force, deform_grad_log_force_naive)
        )
        if all_are_equal or (
            np.sum(deform_grad_log_force * deform_grad_log_force_naive)
            / np.sqrt(
                np.sum(deform_grad_log_force**2)
                * np.sum(deform_grad_log_force_naive**2)
            )
            > 0.8
        ):
            deform_grad_log_force = deform_grad_log_force_naive

        # Cauchy stress used for convergence testing
        convergence_crit_stress = -(virial / volume)
        if self.constant_volume:
            # apply constraint to force
            dglf_trace = deform_grad_log_force.trace()
            np.fill_diagonal(
                deform_grad_log_force,
                np.diag(deform_grad_log_force) - dglf_trace / 3.0,
            )
            # apply constraint to Cauchy stress used for convergence testing
            ccs_trace = convergence_crit_stress.trace()
            np.fill_diagonal(
                convergence_crit_stress,
                np.diag(convergence_crit_stress) - ccs_trace / 3.0,
            )

        # pack gradients into vector
        natoms = len(self.atoms)
        forces[natoms:] = deform_grad_log_force
        self.stress = full_3x3_to_voigt_6_stress(convergence_crit_stress)
        return forces
