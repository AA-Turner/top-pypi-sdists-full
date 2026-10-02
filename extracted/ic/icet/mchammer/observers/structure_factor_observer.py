from collections.abc import Sequence
import numpy as np
from ase import Atoms
from ase.data import atomic_numbers, chemical_symbols
from mchammer.observers.base_observer import BaseObserver
from icet.input_output.logging_tools import logger
logger = logger.getChild('structure_factor_observer')

# Tolerance on the indices that identify a q-point as commensurate with the
# supercell, in units of the reciprocal lattice vectors of the supercell. It has
# to absorb the rounding error incurred when a q-point is specified through the
# lattice parameters rather than through the cell metric, which is a relative
# error of a few units in the last place. It is far too tight to absorb the
# difference between a nominal lattice parameter and the one of a relaxed
# supercell, which is a much larger deviation and is meant to be rejected.
# A q-point that passes is snapped onto the exact reciprocal lattice point, so
# the tolerance decides what is accepted and never how accurate the result is.
_COMMENSURABILITY_TOLERANCE = 1e-6


class StructureFactorObserver(BaseObserver):
    r"""This class represents a structure factor observer.

    This observer allows one to compute structure factors along the
    trajectory sampled by a Monte Carlo (MC) simulation. Structure
    factors are convenient for monitoring long-range order. The
    `structure factor <https://en.wikipedia.org/wiki/Structure_factor>`_
    is defined as:

    .. math::

        S(\vec{q}) = \frac{1}{\sum_{j=1}^N f_j^2}
                 \sum_{j,k}^N e^{-i \vec{q} \cdot (\vec{R}_k - \vec{R}_j)}

    In addition to this "total" structure factor, this observer
    calculates pair-specific structure factors, which correspond to parts
    of the summation defined above, with the summation restricted to pairs
    of specific types, e.g., Au-Au, Au-Cu and Cu-Cu in the example below.

    Parameters
    ----------
    structure
        Prototype for the structures for which the structure factor will
        be computed later. The supercell size (but not its decoration)
        must be identical. This structure is also used to determine the
        the possible pairs if :attr:`symbol_pairs=None`.
    q_points
        Array of q-points at which to evaluate the structure factor.
        The q-points must be commensurate with the supercell, see the
        notes below.
    symbol_pairs
        List of symbol pairs for which structure factors will be computed,
        e.g., ``[('Al', 'Cu'), ('Al', 'Al')]``. If ``None`` (default) use all
        pairs possible based on the input structure.
    form_factors
        Form factors for each atom type. This can be used to
        (coarsely) simulate X-ray or neutron spectra. Note that in
        general the form factors are q-dependent, see, e.g., `here
        <https://dynasor.materialsmodeling.org/reference/post_processing.html>`__.
        By default (``None``) all form factors are set to 1.
    interval
        Observation interval. Defaults to ``None`` meaning that if the
        observer is used in a Monte Carlo simulation, the :class:`Ensemble` object
        will determine the interval.

    Raises
    ------
    ValueError
        If a q-point is not commensurate with the supercell, if the q-points are
        not given as three-dimensional vectors, if no pair is defined, if a
        symbol is not a valid chemical species, if a form factor is missing for
        one of the requested species, or if a form factor is zero.

    Notes
    -----
    A q-point has to be commensurate with the supercell, meaning that
    :math:`\vec{q} \cdot \vec{a}_k` is an integer multiple of :math:`2\pi` for
    every periodic cell vector :math:`\vec{a}_k`, in other words that the
    q-point is a reciprocal lattice vector of the supercell.
    The reason is that a periodic structure fixes its sites only up to a cell
    vector.
    Moving a site by :math:`\vec{a}_k` multiplies its phase by
    :math:`e^{-i \vec{q} \cdot \vec{a}_k}`, which equals one only for a
    commensurate q-point, so for any other q-point the structure factor would
    depend on which periodic image happens to represent each site.
    Commensurate q-points are also the ones for which the structure factor of a
    finite supercell approximates the structure factor of the corresponding
    infinite crystal.
    A direction along which the structure is not periodic imposes no condition,
    since it admits no such shift.

    A q-point is accepted if its indices with respect to the reciprocal lattice
    of the supercell are integers to within a small tolerance, and is then
    snapped onto the exact reciprocal lattice point along the periodic
    directions, so that the phases are those of the q-point that was meant.
    The tolerance applies to the indices themselves, which is what bounds the
    error of a phase, so a high order reflection is held to a tighter relative
    accuracy than a low order one.
    A q-point computed from a lattice parameter that differs slightly from the
    one of the supercell can therefore be accepted at low order and rejected at
    high order.

    Independently of all this, the double sum above factorizes into a product of
    two single sums over the sites, which is what makes the observer cheap.
    It stores one phase per site rather than one phase per pair of sites, so
    that both its setup and its evaluation scale linearly with the number of
    atoms.

    Example
    -------
    The following snippet illustrates how to use the structure factor
    observer in a simulated annealing run of dummy Cu-Au model to
    observe the emergence of a long-range ordered :math:`L1_2` structure::

        >>> import numpy as np
        >>> from ase.build import bulk
        >>> from icet import ClusterSpace, ClusterExpansion
        >>> from mchammer.calculators import ClusterExpansionCalculator
        >>> from mchammer.ensembles import CanonicalAnnealing
        >>> from mchammer.observers import StructureFactorObserver

        >>> # parameters
        >>> size = 3
        >>> alat = 4.0
        >>> symbols = ['Cu', 'Au']

        >>> # setup
        >>> prim = bulk('Cu', a=alat, cubic=True)
        >>> cs = ClusterSpace(prim, [0.9*alat], symbols)
        >>> ce = ClusterExpansion(cs, [0, 0, 0.2])

        >>> # make supercell
        >>> supercell = prim.repeat(size)
        >>> ns = int(0.25 * len(supercell))
        >>> supercell.symbols[0:ns] = 'Au'
        >>> np.random.shuffle(supercell.symbols)

        >>> # define q-points to sample
        >>> q_points = []
        >>> q_points.append(2 * np.pi / alat * np.array([1, 0, 0]))
        >>> q_points.append(2 * np.pi / alat * np.array([0, 1, 0]))
        >>> q_points.append(2 * np.pi / alat * np.array([0, 0, 1]))

        >>> # set up structure factor observer
        >>> sfo = StructureFactorObserver(supercell, q_points)

        >>> # run simulation
        >>> calc = ClusterExpansionCalculator(supercell, ce)
        >>> mc = CanonicalAnnealing(supercell, calc,
        ...          T_start=900, T_stop=500, cooling_function='linear',
        ...          n_steps=400*len(supercell))
        >>> mc.attach_observer(sfo)
        >>> mc.run()

    After having run this snippet, one can access the structure factors via the data
    container::

        >>> dc = mc.data_container
        >>> print(dc.data)

    The emergence of the ordered low-temperature structure can be monitored by
    following the temperature dependence of any of the pair-specific structure
    factors.

    """

    def __init__(self,
                 structure: Atoms,
                 q_points: list[Sequence],
                 symbol_pairs: list[tuple[str, str]] | None = None,
                 form_factors: dict[str, float] | None = None,
                 interval: int | None = None) -> None:
        super().__init__(interval=interval, return_type=dict, tag='StructureFactorObserver')

        self._original_structure = structure.copy()
        self._q_points = list(q_points)

        if symbol_pairs is not None:
            self._pairs = symbol_pairs
        else:
            self._pairs = [(e1, e2)
                           for e1 in set(structure.symbols)
                           for e2 in set(structure.symbols)]
        self._pairs = sorted(set([tuple(sorted(p)) for p in self._pairs]))
        if len(self._pairs) == 0:
            raise ValueError('The StructureFactorObserver requires '
                             'at least one pair to be defined')
        if len(self._pairs) == 1 and self._pairs[0][0] == self._pairs[0][1]:
            logger.warning(f'Only one pair requested {self._pairs[0]}; '
                           'use either a structure occupied by more than '
                           'one species or use the symbol_pairs argument '
                           'to specify more pairs.')

        self._unique_symbols = tuple(sorted({s for p in self._pairs for s in p}))
        self._symbol_indices = {s: k for k, s in enumerate(self._unique_symbols)}
        if form_factors is not None:
            self._form_factors = form_factors
        else:
            self._form_factors = {s: 1 for s in self._unique_symbols}
        self._form_factors = dict(sorted(self._form_factors.items()))

        for symbol in self._unique_symbols:
            if symbol not in chemical_symbols:
                raise ValueError(f'Unknown species {symbol}')
            if symbol not in self._form_factors:
                raise ValueError(f'Form factor missing for {symbol}')

        for symbol, ff in self._form_factors.items():
            if ff == 0:
                raise ValueError(f'Form factor for {symbol} is zero')

        self._form_factor_vector = np.array(
            [self._form_factors[s] for s in self._unique_symbols], dtype=float)
        # the occupations are resolved by atomic number rather than by symbol,
        # since the symbols of a structure come as a list of strings that would
        # have to be turned into an array on every observation
        self._unique_numbers = np.array(
            [atomic_numbers[s] for s in self._unique_symbols])

        self._site_phases = self._get_site_phases(structure, q_points)

    def _get_site_phases(self,
                         structure: Atoms,
                         q_points: list[Sequence]) -> np.ndarray:
        """Returns the phase :math:`e^{-i \\vec{q} \\cdot \\vec{R}}` of every site
        for every q-point, which is all the geometric information needed to
        evaluate the structure factor of a commensurate q-point.
        """
        q_array = np.array(q_points, dtype=float)
        if q_array.size == 0:
            q_array = q_array.reshape(0, 3)
        if q_array.ndim != 2 or q_array.shape[1] != 3:
            raise ValueError('q_points must be a sequence of three-dimensional vectors, '
                             f'but an array of shape {q_array.shape} was given')
        self._check_cell(structure)
        self._check_commensurability(structure, q_array)
        q_array = self._snap_to_reciprocal_lattice(structure, q_array)
        # wrapping the positions into the cell leaves the phases of a
        # commensurate q-point unchanged and keeps their arguments small
        positions = structure.get_positions(wrap=True)
        return np.exp(-1j * (positions @ q_array.T))

    def _check_cell(self,
                    structure: Atoms) -> None:
        """Checks that the reciprocal lattice of the supercell is defined, which
        requires the cell vectors along the periodic directions to be linearly
        independent. A cell that does not meet this is reported here rather than
        through the failure it would otherwise cause when the positions are
        wrapped.
        """
        periodic = np.array(structure.pbc)
        if not np.any(periodic):
            return
        cell = np.array(structure.cell)
        if np.linalg.matrix_rank(cell[periodic]) < int(np.sum(periodic)):
            raise ValueError(
                'The cell vectors along the periodic directions have to be linearly '
                'independent, since the reciprocal lattice of the supercell is otherwise '
                'undefined. The cell is\n'
                f'{np.array2string(cell, precision=6)}\n'
                f'with periodic boundary conditions {tuple(bool(p) for p in periodic)}')

    def _snap_to_reciprocal_lattice(self,
                                    structure: Atoms,
                                    q_points: np.ndarray) -> np.ndarray:
        """Returns the q-points with their component along the periodic
        directions replaced by the nearest reciprocal lattice vector of the
        supercell.

        A q-point is accepted with a finite tolerance, so its indices can deviate
        from integers by a small amount, which would leave a phase drift growing
        with the distance from the origin and make the result depend on the
        periodic image that represents a site. The correction is the shortest one
        that fixes the indices, so it lies in the span of the periodic cell
        vectors and leaves the rest of the q-point alone.
        """
        periodic = np.array(structure.pbc)
        if not np.any(periodic):
            return q_points
        cell = np.array(structure.cell)[periodic]
        indices = cell @ q_points.T / (2 * np.pi)
        residuals = indices - np.round(indices)
        return q_points - 2 * np.pi * (np.linalg.pinv(cell) @ residuals).T

    def _check_commensurability(self,
                                structure: Atoms,
                                q_points: np.ndarray) -> None:
        """Checks that every q-point is a reciprocal lattice vector of the
        supercell and raises otherwise. Directions along which the structure is
        not periodic impose no condition.
        """
        indices = np.array(structure.cell) @ q_points.T / (2 * np.pi)
        residuals = np.abs(indices - np.round(indices))
        residuals[~structure.pbc] = 0.0
        offending = np.flatnonzero(np.any(residuals >= _COMMENSURABILITY_TOLERANCE, axis=0))
        if len(offending) == 0:
            return
        lines = ['The following q-points are not commensurate with the supercell,',
                 'meaning that their indices with respect to the reciprocal lattice',
                 'of the supercell are not integers:']
        for k in offending:
            lines.append(f'  q-point {k}: {np.array2string(q_points[k], precision=6)}'
                         f'  indices: {np.array2string(indices[:, k], precision=6)}')
        raise ValueError('\n'.join(lines))

    def _get_occupation_matrix(self,
                               structure: Atoms) -> np.ndarray:
        """Returns a matrix with one row per species that occurs in the requested
        pairs and one column per site, which is one where the site is occupied by
        that species and zero elsewhere. Species that occur in none of the
        requested pairs are not represented and hence do not contribute.
        """
        numbers = structure.get_atomic_numbers()
        occupations = np.zeros((len(self._unique_numbers), len(numbers)), dtype=np.complex128)
        for k, number in enumerate(self._unique_numbers):
            occupations[k] = numbers == number
        return occupations

    def _compute_structure_factor(self,
                                  structure: Atoms) -> dict[tuple[str, str], float]:
        occupations = self._get_occupation_matrix(structure)
        counts = occupations.real.sum(axis=1)
        norm = np.sum(self._form_factor_vector ** 2 * counts)
        if norm <= 0:
            prefactor = 0.0  # occurs if none of the specified atom types are present
        else:
            prefactor = 1 / norm

        # one single sum per species, from which the double sum over pairs of
        # sites is assembled below as a product of two of them
        amplitudes = occupations @ self._site_phases

        Sq_dict = dict()
        for sym1, sym2 in self._pairs:
            scale = prefactor * self._form_factors[sym1] * self._form_factors[sym2]
            Sq = amplitudes[self._symbol_indices[sym1]].conj() \
                * amplitudes[self._symbol_indices[sym2]] * scale
            if sym1 == sym2:
                # the imaginary part must be zero because both ij and ji appear in the sum
                Sq_dict[(sym1, sym2)] = Sq.real
            else:
                # since we only consider A-B (not B-A; see __init__) we explicitly add ij and ji,
                # which comes down to adding the complex conjugate
                Sq_dict[(sym1, sym2)] = 2 * Sq.real
        return Sq_dict

    def get_observable(self,
                       structure: Atoms) -> dict[str, float]:
        """Returns the structure factors for a given atomic configuration.

        Parameters
        ----------
        structure
            Input atomic structure.

        Raises
        ------
        ValueError
            If the input structure is incompatible with structure used
            for initialization of the :class:`StructureFactorObserver`.
        """
        if len(structure) != len(self._original_structure):
            raise ValueError('Input structure incompatible with structure used for initialization\n'
                             f'  n_input: {len(structure)}\n'
                             f'  n_original: {len(self._original_structure)}')
        Sq_dict = self._compute_structure_factor(structure)
        return_dict = dict()
        for pair, Sq in Sq_dict.items():
            for i in range(len(Sq)):
                tag = 'sfo_{}_{}_q{}'.format(*pair, i)
                return_dict[tag] = Sq[i]
                return_dict[f'total_q{i}'] = return_dict.get(f'total_q{i}', 0) + Sq[i]
        return_dict = dict(sorted(return_dict.items()))
        return return_dict

    @property
    def form_factors(self) -> dict[str, float]:
        """ Form factors used in structure factor calculation. """
        return self._form_factors.copy()

    @property
    def q_points(self) -> list[np.ndarray]:
        """q-points for which structure factor is calculated, as they were
        requested. The phases are computed from the reciprocal lattice points
        these were snapped onto, which differ by at most the acceptance
        tolerance.
        """
        return self._q_points.copy()

    def __str__(self) -> str:
        """ String representation of observer object. """
        width = 60
        name = self.__class__.__name__
        s = [' {} '.format(name).center(width, '=')]

        fmt = '{:15} : {}'
        s += [fmt.format('tag', self.tag)]
        s += [fmt.format('return_type', self.return_type)]
        s += [fmt.format('interval', self.interval)]
        s += [fmt.format('pairs', self._pairs)]
        s += [fmt.format('form_factors', self.form_factors)]
        for k, qpt in enumerate(self.q_points):
            s += [fmt.format(f'q-point{k}', qpt)]
        return '\n'.join(s)
