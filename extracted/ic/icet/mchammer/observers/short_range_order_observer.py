import warnings
from itertools import combinations

import numpy as np

from ase import Atoms
from ase.data import atomic_numbers, chemical_symbols
from icet import ClusterSpace
from icet.core.local_orbit_list_generator import LocalOrbitListGenerator
from icet.core.structure import structure_to_arrays
from mchammer.observers.base_observer import BaseObserver


class ShortRangeOrderObserver(BaseObserver):
    r"""
    This class represents a Warren-Cowley short-range order (SRO) observer for
    systems with an arbitrary number of species.

    A shell is one pair orbit of the cluster space, meaning one set of pairs
    that are equivalent under the symmetry of the lattice.
    Shells are numbered by increasing radius, starting from one.
    Two shells can share a radius without being the same shell, since pairs at
    the same distance need not be related by symmetry.
    An example is hexagonal close packing at the ideal axial ratio, where the
    six neighbors within the basal plane and the six neighbors outside it lie
    at the same distance but form two shells.

    For a system with a single sublattice, a pair of species :math:`A` and
    :math:`B` and a shell :math:`m`, the SRO parameter is

    .. math::

        \alpha^{(m)}_{AB} = 1 - \frac{P^{(m)}_{B|A}}{c_B},

    where :math:`P^{(m)}_{B|A}` is the probability of finding a :math:`B` atom
    in shell :math:`m` around an :math:`A` atom and :math:`c_B` is the
    concentration of species :math:`B`.
    The form that is evaluated here is

    .. math::

        \alpha^{(m)}_{AB} = 1 - \frac{N^{(m)}_{AB}}
        {\langle N^{(m)}_{AB}\rangle_\mathrm{rnd}},

    where :math:`N^{(m)}_{AB}` is the number of :math:`A`-:math:`B` pairs in
    shell :math:`m` and :math:`\langle\cdot\rangle_\mathrm{rnd}` is the number
    of such pairs expected when the species are distributed at random over each
    sublattice, at the concentrations of the structure at hand.
    On a single sublattice the two expressions agree.
    The parameter is negative if :math:`A`-:math:`B` pairs are more common than
    in a random alloy and positive if they are less common.
    It is symmetric under exchange of :math:`A` and :math:`B` and bounded from
    above by one, which is reached when the shell contains no
    :math:`A`-:math:`B` pairs at all.
    The value is ``nan`` if one of the species is absent from a sublattice that
    the shell connects, since the parameter is undefined in that case.

    For a system with several sublattices the second expression is a
    generalization of the first rather than a rewriting of it.
    The reference is conditioned on the sublattices that the shell connects and
    is built from the concentration of each of them separately, whereas the
    textbook expression uses the concentration of the system as a whole.
    The two therefore differ whenever the sublattices differ in composition.
    The quantity reported here measures the correlation that remains once the
    composition of each sublattice is accounted for, which is the useful
    quantity for an ordered compound with mixing on its sublattices.

    A shell that connects two different sublattices distinguishes the two
    orientations of a pair, since :math:`A` on the first sublattice next to
    :math:`B` on the second is a different correlation from :math:`B` on the
    first next to :math:`A` on the second.
    The observer reports one parameter per pair and therefore rejects a pair
    whose two species are both allowed on both of the sublattices that such a
    shell connects, rather than averaging the two orientations into a single
    number.

    On a single sublattice with :math:`n` species the parameters of a shell
    obey the :math:`n` sum rules :math:`\sum_B c_B \alpha^{(m)}_{AB} = 0`, one
    per species :math:`A`, which leaves :math:`n(n-1)/2` independent parameters
    per shell.
    The parameters for unlike pairs form such an independent set and are
    therefore the ones that are reported by default.
    These sum rules do not carry over to a shell that connects two different
    sublattices, where the number of independent parameters is set by the
    number of species allowed on either side.

    A random alloy gives zero in the thermodynamic limit.
    A cell that holds a fixed number of atoms of each species retains a finite
    size offset, because the reference treats the sites as independent while
    the neighbors of a site are in fact drawn without replacement.
    The offset is :math:`-1/(N-1)` for an unlike pair on a sublattice of
    :math:`N` sites, so a cell of 8 sites averages :math:`-1/7` rather than
    zero.

    Shells that touch a sublattice with only one allowed species are not part
    of the cluster space and are hence not reported.
    Their parameters would be identically zero, since that species occupies
    every site of the sublattice in question.

    Parameters
    ----------
    cluster_space
        Cluster space used for initialization.
        Only the primitive structure and the chemical species are taken from
        it, since the shells to be analyzed are set by the ``radius``
        parameter.
    structure
        Defines the lattice which the observer will work on.
        The shells and the sublattices are determined once, at initialization,
        hence :func:`get_observable` accepts only structures with the same cell
        and the same positions, in the same order.
    radius
        Cutoff that selects the neighbor shells to be analyzed, given as the
        largest interatomic distance of a pair that is still included, in
        Ångstrom.
    pairs
        Pairs of species for which to compute the SRO parameters.
        Defaults to ``None``, which implies all pairs of distinct species that
        can occur in at least one of the shells considered.
        Pass explicit pairs in order to restrict the output, or in order to
        include like pairs such as ``('Au', 'Au')``, which are not included by
        default.
        The two species of a pair are reported in alphabetical order, since the
        parameter is symmetric, hence ``('Pd', 'Ag')`` and ``('Ag', 'Pd')`` both
        give keys of the form ``sro_Ag_Pd_m``.
    interval
        Observation interval. Defaults to ``None`` meaning that if the
        observer is used in a Monte Carlo simulations, then the :class:`Ensemble` object
        will determine the interval.

    Example
    -------
    The following snippet illustrates how to use the short-range order (SRO)
    observer in a Monte Carlo simulation of a bulk supercell. Here, the
    parameters of the cluster expansion are set to emulate a simple Ising model
    in order to obtain an example that can be run without modification. In
    practice, one should of course use a proper cluster expansion::

        >>> from ase.build import bulk
        >>> from icet import ClusterExpansion, ClusterSpace
        >>> from mchammer.calculators import ClusterExpansionCalculator
        >>> from mchammer.ensembles import CanonicalEnsemble
        >>> from mchammer.observers import ShortRangeOrderObserver

        >>> # prepare cluster expansion
        >>> # the setup emulates a nearest-neighbor Ising model for a ternary
        >>> # system; note that the shells analyzed by the observer are set by
        >>> # its radius parameter and are independent of the cutoffs of the
        >>> # cluster expansion
        >>> prim = bulk('Au')
        >>> cs = ClusterSpace(prim, cutoffs=[3.0], chemical_symbols=['Ag', 'Au', 'Pd'])
        >>> ce = ClusterExpansion(cs, [0, 0, 0, 0.1, 0.05, -0.02])

        >>> # prepare initial configuration
        >>> structure = prim.repeat(3)
        >>> structure.symbols = 9 * ['Ag'] + 9 * ['Au'] + 9 * ['Pd']

        >>> # set up MC simulation
        >>> calc = ClusterExpansionCalculator(structure, ce)
        >>> mc = CanonicalEnsemble(structure=structure, calculator=calc,
        ...                        temperature=600, dc_filename='myrun_sro.dc')

        >>> # set up observer and attach it to the MC simulation
        >>> sro = ShortRangeOrderObserver(
        ...           cs, structure, interval=len(structure), radius=4.3)
        >>> mc.attach_observer(sro)

        >>> # run 1000 trial steps
        >>> mc.run(1000)

    After having run this snippet one can access the SRO parameters via the
    data container::

        >>> print(mc.data_container.data)

    The parameters are reported under keys of the form ``sro_Ag_Pd_2``, where
    the last field is the shell index. In order to follow only the Ag-Pd
    correlation one would set up the observer as::

        >>> sro = ShortRangeOrderObserver(
        ...           cs, structure, interval=len(structure), radius=4.3,
        ...           pairs=[('Ag', 'Pd')])
    """

    def __init__(self,
                 cluster_space: ClusterSpace,
                 structure: Atoms,
                 radius: float,
                 pairs: list[tuple[str, str]] | None = None,
                 interval: int | None = None) -> None:
        super().__init__(interval=interval, return_type=dict,
                         tag='ShortRangeOrderObserver')

        # The tolerances are carried over, since they decide which pairs are
        # equivalent and hence how the shells come out.
        self._cluster_space = ClusterSpace(
            structure=cluster_space.primitive_structure,
            cutoffs=[radius],
            chemical_symbols=cluster_space.chemical_symbols,
            symprec=cluster_space.symprec,
            position_tolerance=cluster_space.position_tolerance)
        self._number_of_sites = len(structure)
        self._reference_cell = np.array(structure.cell)
        self._reference_positions = structure.get_positions()

        if self._cluster_space.is_supercell_self_interacting(structure):
            warnings.warn('The supercell is self-interacting for a cutoff of'
                          f' {radius}, meaning that a site is a neighbor of itself'
                          ' or of a periodic image of another site in at least one'
                          ' shell. This biases the short-range order parameters,'
                          ' since the reference treats the two sites of a pair as'
                          ' independent. Use a larger supercell or a smaller'
                          ' radius.')

        local_orbit_list_generator = LocalOrbitListGenerator(
            orbit_list=self._cluster_space.orbit_list,
            **structure_to_arrays(structure),
            fractional_position_tolerance=self._cluster_space.fractional_position_tolerance)
        full_orbit_list = local_orbit_list_generator.generate_full_orbit_list()
        sublattices = self._cluster_space.get_sublattices(structure)

        # Collect the pair orbits together with the sublattices that the two
        # sites of their clusters belong to.
        # The orbits are ordered by increasing radius, which makes the position
        # in this list the shell index.
        pair_orbits = []
        for orbit_index in range(len(full_orbit_list)):
            orbit = full_orbit_list.get_orbit(orbit_index)
            if orbit.order != 2:
                continue
            sublattice_indices = tuple(
                sublattices.get_sublattice_index_from_site_index(site.index)
                for site in orbit.representative_cluster.lattice_sites)
            pair_orbits.append((orbit, sublattice_indices))
        if len(pair_orbits) == 0:
            raise ValueError(f'There are no pair orbits within the radius {radius},'
                             ' and hence no shells to analyze')

        # A species can be allowed on more than one sublattice, hence the
        # species of all sublattices involved are collected in a single list
        # that provides the indices into the pair count matrix below.
        self._allowed_species = [set(sublattice.chemical_symbols)
                                 for sublattice in sublattices]
        self._sublattice_symbols = [sublattice.symbol for sublattice in sublattices]
        self._species = sorted(set().union(
            *(self._allowed_species[index]
              for _, sublattice_indices in pair_orbits
              for index in sublattice_indices)))
        self._species_numbers = np.array([atomic_numbers[symbol]
                                          for symbol in self._species])
        self._species_index = {number: index
                               for index, number in enumerate(self._species_numbers)}
        self._pairs = self._validate_pairs(pairs, pair_orbits)
        self._reject_merged_orientations(pair_orbits)

        # The concentrations that define the random reference are those of the
        # sublattices, and only the sublattices that a pair orbit touches are
        # needed for them.
        used_sublattices = sorted({index
                                   for _, sublattice_indices in pair_orbits
                                   for index in sublattice_indices})
        self._sublattices = sublattices
        self._sublattice_sites = [np.array(sublattices[index].indices, dtype=int)
                                  for index in used_sublattices]
        self._sublattice_species_numbers = [
            np.array(sorted(sublattices[index].atomic_numbers))
            for index in used_sublattices]
        position_of_sublattice = {index: position
                                  for position, index in enumerate(used_sublattices)}

        # Precompute, for every shell, the pairs that can occur in it together
        # with the keys under which they are reported, so that an observation
        # amounts to counting and arithmetic only.
        self._shells = []
        self._shell_information = []
        for shell_index, (orbit, sublattice_indices) in enumerate(pair_orbits, start=1):
            shell_pairs = [(symbol_a, symbol_b)
                           for symbol_a, symbol_b in self._pairs
                           if self._pair_can_occur(symbol_a, symbol_b, sublattice_indices)]
            self._shell_information.append(dict(
                index=shell_index,
                radius=orbit.radius,
                sublattices=tuple(sublattices[index].symbol
                                  for index in sublattice_indices),
                pairs=shell_pairs))
            if len(shell_pairs) == 0:
                continue
            targets = [(f'sro_{symbol_a}_{symbol_b}_{shell_index}',
                        self._species_index[atomic_numbers[symbol_a]],
                        self._species_index[atomic_numbers[symbol_b]])
                       for symbol_a, symbol_b in shell_pairs]
            self._shells.append((orbit,
                                 position_of_sublattice[sublattice_indices[0]],
                                 position_of_sublattice[sublattice_indices[1]],
                                 targets))

        # Scratch space reused across observations in order to keep the
        # observation itself free of allocations.
        self._counts = np.zeros((len(self._species), len(self._species)))
        self._concentrations = np.zeros((len(self._sublattice_sites), len(self._species)))
        self._bincount_length = self._species_numbers.max() + 1

    def _reject_merged_orientations(self, pair_orbits: list) -> None:
        """Raises if a pair would mix the two orientations of a shell.

        Parameters
        ----------
        pair_orbits
            The pair orbits together with the sublattices that the two sites of
            their clusters belong to.
        """
        for shell_index, (_, sublattice_indices) in enumerate(pair_orbits, start=1):
            if sublattice_indices[0] == sublattice_indices[1]:
                continue
            first, second = (self._allowed_species[index]
                             for index in sublattice_indices)
            for symbol_a, symbol_b in self._pairs:
                if symbol_a == symbol_b:
                    continue
                if {symbol_a, symbol_b} <= first and {symbol_a, symbol_b} <= second:
                    symbols = [self._sublattice_symbols[index]
                               for index in sublattice_indices]
                    raise ValueError(
                        f'Both {symbol_a} and {symbol_b} are allowed on sublattice'
                        f' {symbols[0]} as well as on sublattice {symbols[1]}, which'
                        f' shell {shell_index} connects. That shell therefore holds'
                        ' two distinct correlations, one per orientation of the pair,'
                        ' which a single parameter cannot represent. Leave this pair'
                        ' out of the pairs argument.')

    def _assert_structure_matches(self, structure: Atoms) -> None:
        """Raises if a structure does not match the one used at initialization.

        The shells and the sublattices are worked out once and are tied to the
        cell, to the positions and to the order of the sites, so applying them
        to any other geometry would silently produce wrong numbers.

        Parameters
        ----------
        structure
            The structure to be checked.
        """
        if len(structure) != self._number_of_sites:
            raise ValueError(
                f'The structure has {len(structure)} sites, whereas this observer'
                f' was set up for {self._number_of_sites}.')
        # The common case is the very same geometry, which an exact comparison
        # settles for a tenth of the cost of a comparison with a tolerance.
        # The tolerance is nevertheless needed, since the structure of a data
        # container has been through a file and need not agree bit for bit.
        cell = structure.cell.array
        positions = structure.positions
        if (np.array_equal(cell, self._reference_cell)
                and np.array_equal(positions, self._reference_positions)):
            return
        tolerance = self._cluster_space.position_tolerance
        if (np.abs(cell - self._reference_cell).max() <= tolerance
                and np.abs(positions - self._reference_positions).max() <= tolerance):
            return
        raise ValueError(
            'The cell or the positions of the structure differ from those of the'
            ' structure that this observer was set up for. The shells and the'
            ' sublattices are determined at initialization, hence only the'
            ' occupations may differ.')

    def _raise_for_disallowed_occupation(self, structure: Atoms) -> None:
        """Raises a description of the site whose species its sublattice does
        not allow.

        This runs only once a cheaper test has established that there is such a
        site, hence it is free to walk the structure.

        Parameters
        ----------
        structure
            The structure whose occupations break the sublattices.
        """
        self._sublattices.assert_occupation_is_allowed(structure.get_chemical_symbols())
        raise ValueError('The occupations of the structure do not obey the sublattices'
                         ' of the cluster space.')

    def _pair_can_occur(self,
                        symbol_a: str,
                        symbol_b: str,
                        sublattice_indices: tuple[int, int]) -> bool:
        """Returns ``True`` if two species can occupy the two sites of a pair
        cluster.

        Parameters
        ----------
        symbol_a
            First species.
        symbol_b
            Second species.
        sublattice_indices
            The sublattices that the two sites of the cluster belong to.
        """
        first, second = (self._allowed_species[index] for index in sublattice_indices)
        return ((symbol_a in first and symbol_b in second)
                or (symbol_b in first and symbol_a in second))

    def _validate_pairs(self,
                        pairs: list[tuple[str, str]] | None,
                        pair_orbits: list) -> list[tuple[str, str]]:
        """ Returns the pairs of species to analyze, after checking them.

        Parameters
        ----------
        pairs
            Pairs requested by the user, or ``None`` for the default, which
            comprises all pairs of distinct species that can occur.
            The species of a pair are sorted, since the parameter is symmetric
            and the two orders therefore name the same quantity.
        pair_orbits
            The pair orbits together with the sublattices that the two sites of
            their clusters belong to.
        """
        def can_occur(symbol_a, symbol_b):
            return any(self._pair_can_occur(symbol_a, symbol_b, sublattice_indices)
                       for _, sublattice_indices in pair_orbits)

        if pairs is None:
            return [(symbol_a, symbol_b)
                    for symbol_a, symbol_b in combinations(self._species, 2)
                    if can_occur(symbol_a, symbol_b)]

        if len(pairs) == 0:
            raise ValueError('The pairs argument is empty, hence the observer would'
                             ' report nothing. Leave it out in order to analyze all'
                             ' pairs of distinct species.')

        validated = []
        seen = set()
        for pair in pairs:
            if len(pair) != 2:
                raise ValueError(f'Each pair must comprise two species, not {pair}')
            symbol_a, symbol_b = sorted(pair)
            for symbol in pair:
                if symbol not in self._species:
                    raise ValueError(f'Species {symbol} is not allowed on any sublattice'
                                     f' that the shells connect; available species:'
                                     f' {self._species}')
            if not can_occur(symbol_a, symbol_b):
                raise ValueError(f'The species {symbol_a} and {symbol_b} cannot occupy the'
                                 ' two sites of any of the shells considered, since they'
                                 ' are confined to sublattices that these shells do not'
                                 ' connect')
            if frozenset(pair) in seen:
                raise ValueError(f'The pair {symbol_a}-{symbol_b} occurs more than once')
            seen.add(frozenset(pair))
            validated.append((symbol_a, symbol_b))
        return validated

    @property
    def pairs(self) -> list[tuple[str, str]]:
        """Pairs of species for which the SRO parameters are computed.

        The two species of a pair appear in alphabetical order, which is the
        order in which they appear in the keys of the observable as well.
        """
        return list(self._pairs)

    @property
    def shells(self) -> list[dict]:
        """Shells that the observer analyzes, ordered by increasing radius.

        Each entry is a dictionary with the keys ``index``, which is the shell
        index that appears in the keys of the observable, ``radius``, which
        follows the convention of :class:`ClusterSpace <icet.ClusterSpace>` and
        is therefore half the interatomic distance of the pair,
        ``sublattices``, which holds the symbols of the sublattices that the
        two sites of the shell belong to, and ``pairs``, which lists the pairs
        of species reported for the shell.
        A shell with an empty list of pairs does not contribute to the
        observable, which is why the shell indices in the observable can have
        gaps for a system with several sublattices.
        """
        return [dict(information, pairs=list(information['pairs']))
                for information in self._shell_information]

    def get_observable(self, structure: Atoms) -> dict[str, float]:
        """Returns the Warren-Cowley short-range order parameters for a given
        atomic configuration.

        The keys of the dictionary are of the form ``sro_A_B_m``, where ``A``
        and ``B`` are the two species and ``m`` is the shell index, counted
        from one in order of increasing radius.

        The observer holds one buffer for the counts of a shell, which it
        reuses, hence a single instance cannot be used from several threads at
        the same time.

        Parameters
        ----------
        structure
            Input atomic structure.
            It has to have the same cell and the same positions, in the same
            order, as the structure that the observer was initialized with.
            Only the occupations may differ, and they have to obey the
            sublattices of the cluster space.
        """
        self._assert_structure_matches(structure)
        occupations = structure.get_atomic_numbers()

        concentrations = self._concentrations
        for position, sites in enumerate(self._sublattice_sites):
            counts = np.bincount(occupations[sites], minlength=self._bincount_length)
            # Counting the species that the sublattice allows and comparing
            # against the number of its sites establishes that every site holds
            # one of them, which comes for free next to the concentrations and
            # costs a fraction of a percent of an observation, whereas
            # Sublattices.assert_occupation_is_allowed walks every site in
            # Python and would triple the cost.
            if counts[self._sublattice_species_numbers[position]].sum() != len(sites):
                self._raise_for_disallowed_occupation(structure)
            concentrations[position] = counts[self._species_numbers] / len(sites)

        sro_parameters = {}
        for orbit, first, second, targets in self._shells:
            counts = self._counts
            counts.fill(0)
            for species, count in orbit.get_cluster_counts(occupations).items():
                try:
                    first_index = self._species_index[species[0]]
                    second_index = self._species_index[species[1]]
                except KeyError:
                    raise ValueError(
                        f'The structure contains {chemical_symbols[species[0]]}'
                        f' or {chemical_symbols[species[1]]} on a site where the'
                        ' cluster space does not allow it; the species available'
                        f' to this observer are {self._species}.') from None
                counts[first_index, second_index] = count

            # Both orders of the two sites of a cluster contribute, which makes
            # the result symmetric and covers like pairs as well as shells that
            # connect two different sublattices.
            # The clusters of an orbit place the two sublattices on the same two
            # sites throughout, so the two concentrations below belong to the
            # two sites in that order. Symmetrizing makes the result independent
            # of this, which an oriented parameter would not be.
            expected = counts.sum() * np.outer(concentrations[first], concentrations[second])
            observed = counts + counts.T
            expected = expected + expected.T
            with np.errstate(divide='ignore', invalid='ignore'):
                alpha = 1 - observed / expected

            for key, index_a, index_b in targets:
                sro_parameters[key] = float(alpha[index_a, index_b])
        return sro_parameters
