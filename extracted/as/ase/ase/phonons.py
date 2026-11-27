"""Module for calculating phonons of periodic systems."""

import warnings
from math import pi, sqrt
from pathlib import Path

import numpy as np
import numpy.fft as fft
import numpy.linalg as la

from ase import Atoms, units
from ase.dft import monkhorst_pack
from ase.io.trajectory import Trajectory
from ase.parallel import world
from ase.utils import deprecated
from ase.utils.filecache import MultiFileJSONCache


class Displacement:
    """Abstract base class for phonon and el-ph supercell calculations.

    Both phonons and the electron-phonon interaction in periodic systems can be
    calculated with the so-called finite-displacement method where the
    derivatives of the total energy and effective potential are obtained from
    finite-difference approximations, i.e. by displacing the atoms. This class
    provides the required functionality for carrying out the calculations for
    the different displacements in its ``run`` member function.

    Derived classes must overwrite the ``__call__`` member function which is
    called for each atomic displacement.

    """

    def __init__(
        self,
        atoms: Atoms,
        calc,
        supercell: tuple[int, int, int],
        select_atoms: list[str] | list[int] | None,
        name: str,
        delta: float,
        center_refcell: bool,
        comm,
    ):
        # Store atoms and calculator
        self.atoms = atoms
        self.natoms = len(atoms)
        self.calc = calc

        # Specify indices of which atoms to vibrate
        self.set_atoms(select_atoms, _warn=False)

        self.name = name
        self.delta = delta

        assert len(supercell) == 3
        self.supercell = supercell
        self.ncells = np.prod(supercell)
        if not center_refcell:
            self.refcell_offset = 0
        else:
            self.refcell_offset = (
                supercell[0] // 2 * (supercell[1] * supercell[2])
                + supercell[1] // 2 * supercell[2]
                + supercell[2] // 2
            )

        self.lattice_vectors_array = self.get_lattice_vectors()

        if comm is None:
            comm = world
        self.comm = comm

        self.cache = MultiFileJSONCache(self.name, comm=comm)

    @deprecated('Please use get_lattice_vectors() instead')
    def compute_lattice_vectors(self):
        """Deprecated version of get_lattice_vectors,
        can safely be removed by summer 2027"""
        return self.get_lattice_vectors().T

    def get_lattice_vectors(self):
        """Return lattice vectors for cells in the supercell.

        These are the integer indices of each cell within the supercell.
        The ordering is as illustrated in Phonons class docstring"""

        # First, lattice vectors relevative to the corner unit cell
        R_Nc = np.indices(self.supercell).reshape(3, self.ncells).T

        N_c = np.array(self.supercell)
        if self.refcell_offset == 0:
            R_Nc += N_c // 2
            R_Nc %= N_c
        R_Nc -= N_c // 2

        return R_Nc

    def __call__(self, *args, **kwargs):
        """Member function called in the ``run`` function."""

        raise NotImplementedError('Implement in derived classes!.')

    def set_atoms(
        self, select_atoms: list[str] | list[int] | None, _warn: bool = True
    ):
        """Specify which atoms to vibrate.

        Parameters
        ----------
        select_atoms:
            List of atomic indices or atomic types.
            If None, all atoms are set to vibrate.

        """

        if _warn:
            warnings.warn(
                'Please specify which atoms to vibrate using the select_atoms '
                'keyword during initialization instead of using '
                'Displacements.set_atoms(...)',
                FutureWarning,
            )
        # This method can safely be moved inside the __init__ and deleted
        # roughly by summer 2027.

        atoms = self.atoms

        match select_atoms:
            case None:
                self.nindices = len(atoms)
                self.indices = np.arange(self.nindices)
            case [*atomlist]:
                indices: list[int]
                assert len(atomlist) == len(set(atomlist))
                assert len(atomlist) <= len(atoms)
                assert all(type(atom) is type(atomlist[0]) for atom in atomlist)
                if isinstance(atomlist[0], str):
                    indices = atoms.symbols.search(atomlist)
                elif isinstance(atomlist[0], int):
                    indices = atomlist
                self.indices = np.array(indices)
                self.nindices = len(indices)
            case _:
                raise TypeError(
                    'Bad input type for keyword "select_atoms"; '
                    'should be either list[str] or list[int]!'
                )

    def _eq_disp(self):
        return self._disp(0, 0, 0)

    def _disp(self, a, i: int, step):
        from ase.vibrations.vibrations import Displacement as VDisplacement

        return VDisplacement(a, i, np.sign(step), abs(step), self)

    def run(self):
        """Run the calculations for the required displacements.

        This will do a calculation for 6 displacements per atom, +-x, +-y, and
        +-z. Only those calculations that are not already done will be
        started. Be aware that an interrupted calculation may produce an empty
        file (ending with .json), which must be deleted before restarting the
        job. Otherwise the calculation for that displacement will not be done.

        """

        # Atoms in the supercell -- repeated in the lattice vector directions
        # beginning with the last
        atoms_N = self.atoms * self.supercell

        # Set calculator if provided
        assert self.calc is not None, 'Provide calculator in __init__ method'
        atoms_N.calc = self.calc

        # Do calculation on equilibrium structure
        eq_disp = self._eq_disp()
        with self.cache.lock(eq_disp.name) as handle:
            if handle is not None:
                output = self.calculate(atoms_N, eq_disp)
                handle.save(output)

        # Positions of atoms to be displaced in the reference cell
        natoms = len(self.atoms)
        offset = natoms * self.refcell_offset
        pos_av = atoms_N.positions[offset : offset + natoms].copy()

        # Loop over all displacements
        for a in self.indices:
            for i in range(3):
                for sign in [-1, 1]:
                    disp = self._disp(a, i, sign)
                    with self.cache.lock(disp.name) as handle:
                        if handle is None:
                            continue
                        try:
                            atoms_N.positions[offset + a, i] = (
                                pos_av[a, i] + sign * self.delta
                            )

                            result = self.calculate(atoms_N, disp)
                            handle.save(result)
                        finally:
                            # Return to initial positions
                            atoms_N.positions[offset + a, i] = pos_av[a, i]

        self.comm.barrier()

    def clean(self):
        """Delete generated files."""
        if self.comm.rank == 0:
            nfiles = self._clean()
        else:
            nfiles = 0
        self.comm.barrier()
        return nfiles

    def _clean(self):
        name = Path(self.name)

        nfiles = 0
        if name.is_dir():
            for fname in name.iterdir():
                fname.unlink()
                nfiles += 1
            name.rmdir()
        return nfiles


class Phonons(Displacement):
    r"""Class for calculating phonon modes using the finite displacement method.

    The matrix of force constants is calculated from the finite difference
    approximation to the first-order derivative of the atomic forces as::

                            2             nbj   nbj
                nbj        d E           F-  - F+
               C     = ------------ ~  -------------  ,
                mai     dR   dR          2 * delta
                          mai  nbj

    where F+/F- denotes the force in direction j on atom nb when atom ma is
    displaced in direction +i/-i. The force constants are related by various
    symmetry relations. From the definition of the force constants it must
    be symmetric in the three indices mai::

                nbj    mai         bj        ai
               C    = C      ->   C  (R ) = C  (-R )  .
                mai    nbj         ai  n     bj   n

    As the force constants can only depend on the difference between the m and
    n indices, this symmetry is more conveniently expressed as shown on the
    right hand-side.

    The acoustic sum-rule::

                           _ _
                aj         \    bj
               C  (R ) = -  )  C  (R )
                ai  0      /__  ai  m
                          (m, b)
                            !=
                          (0, a)

    Ordering of the unit cells illustrated here for a 1-dimensional system (in
    case ``center_refcell=False`` in constructor!):

    ::

               m = 0        m = 1        m = -2        m = -1
           -----------------------------------------------------
           |            |            |            |            |
           |        * b |        *   |        *   |        *   |
           |            |            |            |            |
           |   * a      |   *        |   *        |   *        |
           |            |            |            |            |
           -----------------------------------------------------

    Examples
    --------
    >>> from ase.build import bulk
    >>> from ase.phonons import Phonons
    >>> from ase.calculators.emt import EMT

    >>> atoms = bulk('Al', 'fcc', a=4.05)
    >>> calc = EMT()
    >>> ph = Phonons(
    ...     atoms,
    ...     calc,
    ...     supercell=(5, 5, 5),
    ...     delta=0.05,
    ...     use_mean_minimum_images=True
    ... )
    >>> ph.run()
    >>> ph.read()
    >>> path = atoms.cell.bandpath('GXULGK', npoints=100)
    >>> bs = ph.get_band_structure(path, verbose=False)
    >>> dos = ph.get_dos(kpts=(12, 12, 12)).sample_grid(npts=100, width=1e-3)

    """

    def __init__(
        self,
        atoms: Atoms,
        calc=None,
        supercell: tuple[int, int, int] = (1, 1, 1),
        select_atoms: list[int] | list[str] | None = None,
        name: str = 'phonon',
        delta: float = 0.01,
        center_refcell: bool = False,
        use_mean_minimum_images: bool | None = None,
        minimum_image_tol: float = 1e-5,
        comm=None,
    ):
        """Init with an instance of :class:`~ase.Atoms` and a calculator.

        Parameters
        ----------
        atoms:
            The atoms to work on.
        calc:
            Calculator for the supercell calculation.
        supercell:
            Size of supercell given by the number of repetitions (n1, n2, n3) of
            the small unit cell in each direction.
        select_atoms:
            Select which atoms to generate displacements for.
            By default, displacements are generated for all atoms.
        name:
            Base name to use for files.
        delta:
            Magnitude of displacement in Ang.
        center_refcell:
            Reference cell in which the atoms will be displaced. If False, then
            corner cell in supercell is used. If True, then cell in the center
            of the supercell is used.
        use_mean_minimum_images:
            Use averaged phase factor of all the shortest atom-to-atom image
            vectors.  This will be the default in the future and is strongly
            recommended as it requires smaller supercells to converge
            the phonon energies.
        minimum_image_tol:
            Tolerance (in Å) for finding equivalent atoms when using
            mean minimum image phase factors.
        comm:
            MPI communicator for the phonon calculation.
            Default is to use world.
        """

        super().__init__(
            atoms=atoms,
            calc=calc,
            supercell=supercell,
            select_atoms=select_atoms,
            name=name,
            delta=delta,
            center_refcell=center_refcell,
            comm=comm,
        )

        if use_mean_minimum_images is None:
            warnings.warn(
                'The "use_mean_minimum_images" parameter is new to the '
                'Phonons class and in the future it will be True by default. '
                'For now, it will be set to False to ensure consistency with '
                'previous behaviour. Please explicitly set the '
                '"use_mean_minimum_images" keyword to True / False '
                'to ensure consistent behaviour with future versions.',
                FutureWarning,
            )
            use_mean_minimum_images = False

        self.use_mean_minimum_images = use_mean_minimum_images
        self.atom2atom_vectors = self._get_atom2atom_vectors(minimum_image_tol)

        self.C_avNav: np.ndarray | None = None  # in units of eV / Ang**2

    def __call__(self, atoms_N: Atoms):
        """Calculate forces on atoms in supercell."""
        return atoms_N.get_forces()

    def calculate(self, atoms_N: Atoms, disp) -> dict[str, np.ndarray]:
        forces = self(atoms_N)
        return {'forces': forces}

    def check_eq_forces(self):
        """Check maximum size of forces in the equilibrium structure."""

        eq_disp = self._eq_disp()
        feq_av = self.cache[eq_disp.name]['forces']

        fmin = feq_av.min()
        fmax = feq_av.max()
        i_min = np.where(feq_av == fmin)
        i_max = np.where(feq_av == fmax)

        return fmin, fmax, i_min, i_max

    def _get_atom2atom_vectors(self, minimum_image_tol: float) -> np.ndarray:
        """Calculate all atom-to-atom vectors, i.e. all vectors that go from
        atom a1 in the reference unit cell to atom a2 in cell N in the
        supercell.

        If the phonons class was initialized with use_mean_minimum_images=True,
        all the shortest atom-to-atom vectors are calculated by also checking
        the periodic images of atom2 in cell N. Furthermore, the keyword
        minimum_image_tol can be supplied to the Phonons class which controls
        the tolerance when detecting minimum image vectors.
        """

        R_Nc = self.lattice_vectors_array
        relpos_ac = self.atoms.get_scaled_positions(wrap=True)[self.indices]
        vectors_aNac = (
            relpos_ac[np.newaxis, np.newaxis]
            + R_Nc[np.newaxis, :, np.newaxis]
            - relpos_ac[:, np.newaxis, np.newaxis]
        )

        if not self.use_mean_minimum_images:
            return vectors_aNac

        supercellshifts_Sc = (
            np.indices((3, 3, 3)).reshape(3, -1).T - 1
        ) * self.supercell
        bools_L = np.logical_or(supercellshifts_Sc == 0, self.atoms.pbc).all(
            axis=1
        )
        supercellshifts_Sc = supercellshifts_Sc[bools_L]
        cell_cv = self.atoms.cell.array

        vectors_aNaSc = np.empty(vectors_aNac.shape[0:3], dtype=object)

        for a1, vectors_Nac in enumerate(vectors_aNac):
            for N, vectors_ac in enumerate(vectors_Nac):
                for a2, vector_c in enumerate(vectors_ac):
                    images_Sc = vector_c + supercellshifts_Sc
                    lengths_S = np.linalg.norm(images_Sc @ cell_cv, axis=1)
                    bools_S = np.isclose(
                        lengths_S,
                        lengths_S.min(),
                        rtol=0.0,
                        atol=minimum_image_tol,
                    )
                    vectors_aNaSc[a1, N, a2] = images_Sc[bools_S]

        return vectors_aNaSc

    @deprecated(
        'Implementation of non-analytical correction has remained untested '
        'for many years and was likely incorrect, see '
        'https://gitlab.com/ase/ase/-/work_items/941   '
    )
    def read_born_charges(self, name='born', neutrality=True):
        r"""Read Born charges and dieletric tensor from JSON file.

        The charge neutrality sum-rule::

                   _ _
                   \    a
                    )  Z   = 0
                   /__  ij
                    a

        .. deprecated:: 3.22.1
            Current implementation of non-analytical correction is likely
            incorrect, see :issue:`941`

        Parameters
        ----------

        neutrality: bool
            Restore charge neutrality condition on calculated Born effective
            charges.
        name: str
            Key used to identify the file with Born charges for the unit cell
            in the JSON cache.
        """

        # Load file with Born charges and dielectric tensor for atoms in the
        # unit cell
        Z_avv, eps_vv = self.cache[name]

        # Neutrality sum-rule
        if neutrality:
            Z_mean = Z_avv.sum(0) / len(Z_avv)
            Z_avv -= Z_mean

        self.Z_avv = Z_avv[self.indices]
        self.eps_vv = eps_vv

    def read(
        self,
        method: str = 'Frederiksen',
        symmetrize: int = 3,
        acoustic: bool = True,
        cutoff: float | None = None,
    ):
        """Read forces from json files and calculate force constants.

        Parameters
        ----------
        method:
            Specify method for evaluating the atomic forces,
            method='Frederiksen' imposes momentum conservation.
        symmetrize:
            Symmetrize force constants (see doc string at top) when
            ``symmetrize != 0`` (default: 3). Since restoring the acoustic sum
            rule breaks the symmetry, the symmetrization must be repeated a few
            times until the changes a insignificant. The integer gives the
            number of iterations that will be carried out.
        acoustic:
            Restore the acoustic sum rule on the force constants.
        cutoff:
            Zero elements in the dynamical matrix between atoms with an
            interatomic distance larger than the cutoff.
        """

        method = method.lower()
        assert method in ['standard', 'frederiksen']
        if cutoff is not None:
            cutoff = float(cutoff)

        cache = self.cache
        natoms = self.natoms
        nindices = self.nindices
        ncells = self.ncells
        refcell_offset = self.refcell_offset
        # Matrix of force constants in units eV / Ang**2 with five
        # indices (a1, v1) and (N, a2, v2), i.e. these constants
        # couple the harmonic motion of atom a1 in the reference
        # unit cell moving along Cartesian direction v1 with the
        # force on atom a2 in unit cell N pointing along direction v2.
        C_avNav = np.empty((nindices, 3, ncells, nindices, 3), dtype=float)

        # Loop over all atomic displacements and calculate force constants
        for a, C_vNav in zip(self.indices, C_avNav):
            for v, C_Nav in zip('xyz', C_vNav):
                # Atomic forces for a displacement of atom a in direction v
                # basename = '%s.%d%s' % (self.name, a, v)
                basename = f'{a}{v}'
                C_raw_Nav = (
                    cache[basename + '-']['forces']
                    - cache[basename + '+']['forces']
                ).reshape(ncells, natoms, 3)
                C_raw_Nav /= 2 * self.delta

                if method == 'frederiksen':
                    C_raw_Nav[refcell_offset, a] -= C_raw_Nav.sum((0, 1))

                # Slice out included atoms
                C_Nav[:] = C_raw_Nav[:, self.indices]

        # Apply cutoff before symmetry and acoustic sum rule are imposed
        if cutoff is not None:
            self.apply_cutoff(C_avNav, cutoff)

        # Symmetrize force constants
        if symmetrize:
            for _ in range(symmetrize):
                # Symmetrize
                C_avNav = self.symmetrize(C_avNav)
                # Restore acoustic sum-rule
                if acoustic:
                    self.acoustic(C_avNav)
                else:
                    break

        # Store force constants
        self.C_avNav = C_avNav

    def symmetrize(self, C_avNav: np.ndarray) -> np.ndarray:
        """Symmetrize force constant matrix."""

        supercell = self.supercell
        nindices = self.nindices
        ncells = self.ncells

        C_Navav = np.moveaxis(C_avNav, (0, 1, 2), (1, 2, 0))

        # Reshape force constants to (n, n, n) cell indices
        C_nnnXX = C_Navav.reshape(supercell + (3 * nindices, 3 * nindices))

        # Shift reference cell to center index (if it isn't already)
        if self.refcell_offset == 0:
            C_nnnXX = fft.fftshift(C_nnnXX, axes=(0, 1, 2)).copy()
        # Make force constants symmetric in indices -- in case of an even
        # number of unit cells don't include the first cell
        n1, n2, n3 = 1 - np.asarray(supercell) % 2
        C_nnnXX[n1:, n2:, n3:] *= 0.5
        C_nnnXX[n1:, n2:, n3:] += (
            (C_nnnXX[n1:, n2:, n3:][::-1, ::-1, ::-1])
            .transpose(0, 1, 2, 4, 3)
            .copy()
        )
        if self.refcell_offset == 0:
            C_nnnXX = fft.ifftshift(C_nnnXX, axes=(0, 1, 2)).copy()

        # Change to single unit cell index shape
        C_Navav = C_nnnXX.reshape((ncells, nindices, 3, nindices, 3))

        return np.moveaxis(C_Navav, (0, 1, 2), (2, 0, 1))

    def acoustic(self, C_avNav: np.ndarray) -> None:
        """Restore acoustic sumrule on force constants."""
        # There may be better performing methods for
        # restoring the acoustic sum rule

        for a, C_vNav in enumerate(C_avNav):
            for C_Nav in C_vNav:
                C_Nav[self.refcell_offset, a] -= C_Nav.sum(axis=(0, 1))

    def apply_cutoff(self, C_avNav: np.ndarray, r_c: float) -> None:
        """Zero elements for interatomic distances larger than the cutoff.

        Parameters
        ----------
        C_avNav: ndarray
            Matrix of force constants.
        r_c: float
            Cutoff radius in Ångstrom.
        """

        R_Nc = self.lattice_vectors_array
        cell_cv = self.atoms.cell
        R_Nv = R_Nc @ cell_cv
        pos_av = self.atoms.get_positions()[self.indices]

        # Maybe calculate mean minimum image vector here instead..
        vectors_aNav = (
            pos_av[np.newaxis, np.newaxis]
            + R_Nv[np.newaxis, :, np.newaxis]
            - pos_av[:, np.newaxis, np.newaxis]
        )

        dist_aNa = np.linalg.norm(vectors_aNav, axis=-1)
        bools_aNa = dist_aNa <= r_c

        C_avNav *= bools_aNa[:, np.newaxis, :, :, np.newaxis]

    @deprecated('Please use get_force_constants() instead')
    def get_force_constant(self) -> np.ndarray:
        """Deprecated version of get_force_constants,
        can safely be removed by summer 2027

        .. note::
           Please use get_force_constants().

        """

        C_avNav = self.get_force_constants()
        C_Navav = np.moveaxis(C_avNav, (0, 1, 2), (1, 2, 0))
        return C_Navav.reshape(
            (C_Navav.shape[0],) + (3 * self.nindices, 3 * self.nindices)
        )

    def get_force_constants(self) -> np.ndarray:
        """Return matrix of force constants."""

        assert self.C_avNav is not None
        return self.C_avNav

    def get_band_structure(
        self,
        path,
        modes: bool = False,
        verbose: bool = True,
    ):
        r"""Calculate and return the phonon band structure.

        This method computes the phonon band structure for a given path
        in reciprocal space. It is a wrapper around the internal
        :meth:`~Phonons.band_structure` method of the :class:`Phonons` class.
        The method can optionally calculate and return phonon modes.

        Frequencies and modes are in units of eV and
        :math:`1/\sqrt{\mathrm{amu}}`, respectively.

        Parameters
        ----------
        path : BandPath object
            The BandPath object defining the path in the reciprocal
            space over which the phonon band structure is calculated.
        modes : bool, optional
            If True, phonon modes will also be calculated and returned.
            Defaults to False.
        verbose : bool, optional
            If True, enables verbose output during the calculation.
            Defaults to True.

        Returns
        -------
        BandStructure or tuple of (BandStructure, ndarray)
            If ``modes`` is False, returns a ``BandStructure`` object
            containing the phonon band structure. If ``modes`` is True,
            returns a tuple, where the first element is the
            ``BandStructure`` object and the second element is an ndarray
            of phonon modes.

            If modes are returned, the array is of shape
            (k-point, bands, atoms, 3) and the norm-squared of the mode
            is `1 / m_{eff}`, where `m_{eff}` is the effective mass of the
            mode.

        """
        result = self.band_structure(path.kpts, modes=modes, verbose=verbose)
        if modes:
            omega_kl, omega_modes = result
        else:
            omega_kl = result

        from ase.spectrum.band_structure import BandStructure

        bs = BandStructure(path, energies=omega_kl[None])

        # Return based on the modes flag
        return (bs, omega_modes) if modes else bs

    @deprecated('Please use calculate_dynamical_matrix() instead')
    def compute_dynamical_matrix(
        self, q_scaled: np.ndarray, D_N: np.ndarray
    ) -> np.ndarray:
        """Computation of the dynamical matrix in momentum space D_ab(q).
        This is a Fourier transform from real-space dynamical matrix D_N
        for a given momentum vector q.

        .. note::
           Deprecated. Please use calculate_dynamical_matrix().

        Parameters
        ----------
        q_scaled : np.ndarray
            q vector in scaled coordinates.
        D_N : np.ndarray
            Dynamical matrix in real-space.

        Returns
        -------
        D_q : np.ndarray
            2D complex-valued array D(q) with shape=(3 * natoms, 3 * natoms).

        """

        # Evaluate fourier sum
        R_cN = self.compute_lattice_vectors()
        phase_N = np.exp(-2.0j * pi * np.dot(q_scaled, R_cN))
        D_q = np.sum(phase_N[:, np.newaxis, np.newaxis] * D_N, axis=0)
        return D_q

    def calculate_dynamical_matrix(
        self, q_c: np.ndarray, D_avNav: np.ndarray
    ) -> np.ndarray:
        """Computation of the dynamical matrix in momentum space D_XX(q).
        This is a Fourier transform from real-space force constants
        for a given momentum vector q.

        If the phonons class was initialized with use_mean_minimum_images=True,
        the q-dependent phase factor for a given set of atoms a1 and (N, a2) is
        averaged over all the shortest atom-to-atom vectors from atom1 to a
        periodic image of atom (N, a2).

        Parameters
        ----------
        q_c:
            Phonon wave vector in scaled coordinates.
        D_avNav:
            Force constant matrix scaled by atom masses.

        Returns
        -------
        D_XX: np.ndarray
            Dynamical matrix, a complex-valued array D(q)
            with shape=(3 * natoms, 3 * natoms).
        """

        if not self.use_mean_minimum_images:
            atom2atom_aNac = self.atom2atom_vectors
            phase_aNa = np.exp(2.0j * np.pi * np.dot(atom2atom_aNac, q_c))
        else:
            atom2atom_aNaSc = self.atom2atom_vectors
            # In this case, atom2atom is an ndarray with 3 indexes of ndarrays
            # with 2 indexes so some code might look unintuitive
            phase_aNa = np.zeros(atom2atom_aNaSc.shape, dtype=complex)
            for (a1, N, a2), atom2atom_Sc in np.ndenumerate(atom2atom_aNaSc):
                phase_aNa[a1, N, a2] = np.exp(
                    2.0j * np.pi * np.dot(atom2atom_Sc, q_c)
                ).mean()

        D_avav = np.einsum('avNbw,aNb->avbw', D_avNav, phase_aNa)

        return D_avav.reshape(3 * self.nindices, 3 * self.nindices)

    def band_structure(self, path_kc, modes=False, verbose=True):
        """Calculate phonon dispersion along a path in the Brillouin zone.

        The dynamical matrix at arbitrary q-vectors is obtained by Fourier
        transforming the real-space force constants. In case of negative
        eigenvalues (squared frequency), the corresponding negative frequency
        is returned.

        Frequencies and modes are in units of eV and 1/sqrt(amu),
        respectively.

        Parameters
        ----------
        path_kc: ndarray
            List of k-point coordinates (in units of the reciprocal lattice
            vectors) specifying the path in the Brillouin zone for which the
            dynamical matrix will be calculated.
        modes: bool
            Returns both frequencies and modes when True.
        verbose: bool
            Print warnings when imaginary frequncies are detected.

        Returns
        -------
        omega_kl: np.ndarray
            Phonon band energies.
        u_klav: np.ndarray
            Eigenvectors (only when ``modes`` is ``True``).
        """

        nindices = self.nindices

        # Force constant matrices
        assert self.C_avNav is not None, print(
            'Make sure you have .read() your force constant matrices!'
        )
        C_avNav = self.C_avNav

        # Multiply by mass prefactor
        m_inv_a = self.atoms.get_masses()[self.indices] ** -0.5
        m_inv_aa = np.outer(m_inv_a, m_inv_a)

        D_avNav = C_avNav * m_inv_aa[:, np.newaxis, np.newaxis, :, np.newaxis]

        # Lists for frequencies and modes along path
        nk = path_kc.shape[0]
        omega_kl = np.zeros((nk, 3 * nindices))
        u_klav = np.zeros((nk, 3 * nindices, nindices, 3), dtype=complex)

        for q_index, q_c in enumerate(path_kc):
            # Evaluate Fourier sum
            D_XX = self.calculate_dynamical_matrix(q_c, D_avNav)

            if modes:
                omega2_l, u_Xl = la.eigh(D_XX, UPLO='U')
                # Sort eigenmodes according to eigenvalues and reshape
                u_lav = u_Xl.T[omega2_l.argsort()].reshape(
                    3 * nindices, nindices, 3
                )
                # Multiply with mass prefactor. This gives the eigenmode
                # (which is now not normalized!) in units of 1/sqrt(amu).
                u_klav[q_index] = u_lav * m_inv_a[np.newaxis, :, np.newaxis]
            else:
                omega2_l = la.eigvalsh(D_XX, UPLO='U')

            # Sort eigenvalues in increasing order
            omega2_l.sort()
            # Use dtype=complex to handle negative eigenvalues
            omega_l = np.sqrt(omega2_l.astype(complex))

            # Take care of imaginary frequencies
            if not np.all(omega2_l >= 0.0):
                complex_indices = np.where(omega2_l < 0)[0]

                if verbose:
                    print(
                        'WARNING, %i imaginary frequencies at '
                        'q = (% 5.2f, % 5.2f, % 5.2f) ; (omega_q =% 5.3e*i)'
                        % (
                            len(complex_indices),
                            q_c[0],
                            q_c[1],
                            q_c[2],
                            omega_l[complex_indices][0].imag,
                        )
                    )

                omega_l[complex_indices] = -1 * np.sqrt(
                    np.abs(omega2_l[complex_indices].real)
                )

            omega_kl[q_index] = omega_l.real

        # Conversion factor: sqrt(eV / Ang^2 / amu) -> eV
        omega_kl *= units._hbar * 1e10 / sqrt(units._e * units._amu)

        if modes:
            return omega_kl, u_klav
        return omega_kl

    def get_dos(
        self,
        kpts: tuple[int, int, int] = (10, 10, 10),
        indices: list | None = None,
        verbose: bool = True,
    ):
        """Return a phonon density of states.

        Parameters
        ----------
        kpts: tuple
            Shape of Monkhorst-Pack grid for sampling the Brillouin zone.
        indices: list
            If indices is not None, the amplitude-weighted atomic-partial
            DOS for the specified atoms will be calculated.
        verbose: bool
            Print warnings when imaginary frequncies are detected.

        Returns
        -------
        RawDOSData
            Density of states.

        """
        from ase.spectrum.dosdata import RawDOSData

        # dos = self.dos(kpts, npts, delta, indices)
        kpts_kc = monkhorst_pack(kpts)
        if indices is None:
            # Return the total DOS
            omega_w = self.band_structure(kpts_kc, verbose=verbose)
            assert omega_w.ndim == 2
            n_kpt = omega_w.shape[0]
            omega_w = omega_w.ravel()
            dos = RawDOSData(omega_w, np.ones_like(omega_w) / n_kpt)
        else:
            # Return a partial DOS
            omegas, amplitudes = self.band_structure(
                kpts_kc, modes=True, verbose=verbose
            )
            # omegas.shape = (k-points, bands)
            # amplitudes.shape = (k-points, bands, atoms, 3)
            ampl_sq = (np.abs(amplitudes) ** 2).sum(axis=3)
            assert ampl_sq.ndim == 3
            assert ampl_sq.shape == omegas.shape + (len(self.indices),)
            weights = ampl_sq[:, :, indices].sum(axis=2) / ampl_sq.sum(axis=2)
            dos = RawDOSData(omegas.ravel(), weights.ravel() / omegas.shape[0])
        return dos

    def write_modes(
        self,
        q_c,
        branches=0,
        kT: float = units.kB * 300,
        repeat: tuple[int, int, int] = (1, 1, 1),
        nimages: int = 30,
        center: bool = False,
    ) -> None:
        """Write modes to trajectory file.

        .. note::
           To exaggerate the amplitudes for better visualization, multiply
           kT by the square of the desired factor.

        Parameters
        ----------
        q_c: ndarray of shape (3,)
            q-vector of the modes.
        branches: int or list
            Branch index of modes.
        kT: float
            Temperature in units of eV. Determines the amplitude of the atomic
            displacements in the modes.
        repeat: tuple
            Repeat atoms (l, m, n) times in the directions of the lattice
            vectors. Displacements of atoms in repeated cells carry a Bloch
            phase factor given by the q-vector and the cell lattice vector R_m.
        nimages: int
            Number of images in an oscillation.
        center: bool
            Center atoms in unit cell if True (default: False).
        """

        if isinstance(branches, int):
            branch_l = [branches]
        else:
            branch_l = list(branches)

        # Calculate modes
        omega_l, u_l = self.band_structure(
            q_c[np.newaxis, :],
            modes=True,
        )
        # Repeat atoms
        atoms = self.atoms * repeat
        # Center
        if center:
            atoms.center()

        # Here ``Na`` refers to a composite unit cell/atom dimension
        pos_Nav = atoms.get_positions()
        # Total number of unit cells
        N = np.prod(repeat)

        # Corresponding lattice vectors R_m
        R_cN = np.indices(repeat).reshape(3, -1)
        # Bloch phase
        phase_N = np.exp(2.0j * pi * np.dot(q_c, R_cN))
        phase_Na = phase_N.repeat(len(self.atoms))

        hbar = units._hbar * units.J * units.second
        for lval in branch_l:
            omega = omega_l[0, lval]
            u_av = u_l[0, lval]
            assert u_av.ndim == 2

            # For a classical harmonic oscillator, <x^2> = k T / m omega^2
            # and <x^2> = 1/2 u^2 where u is the amplitude and m is the
            # effective mass of the mode.
            # The reciprocal mass is already included in the normalization
            # of the modes.  The variable omega is actually hbar*omega (it
            # is in eV, not reciprocal ASE time units).
            u_av *= hbar * sqrt(2 * kT) / abs(omega)

            mode_av = np.zeros((len(self.atoms), 3), dtype=complex)
            # Insert slice with atomic displacements for the included atoms
            mode_av[self.indices] = u_av
            # Repeat and multiply by Bloch phase factor
            mode_Nav = np.vstack(N * [mode_av]) * phase_Na[:, np.newaxis]

            with Trajectory('%s.mode.%d.traj' % (self.name, lval), 'w') as traj:
                for x in np.linspace(0, 2 * pi, nimages, endpoint=False):
                    atoms.set_positions(
                        (pos_Nav + np.exp(1.0j * x) * mode_Nav).real
                    )
                    traj.write(atoms)
