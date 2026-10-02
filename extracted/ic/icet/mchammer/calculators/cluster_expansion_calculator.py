
import numpy as np

from _icet import _ClusterExpansionCalculator
from icet.input_output.logging_tools import logger
from ase import Atoms
from icet import ClusterExpansion
from icet.core.structure import structure_to_arrays
from icet.core.sublattices import Sublattices
from mchammer.calculators.base_calculator import BaseCalculator


class ClusterExpansionCalculator(BaseCalculator):
    """A :class:`ClusterExpansionCalculator` object enables the efficient
    calculation of properties described by a cluster expansion. It is
    specific for a particular (supercell) structure and commonly
    employed when setting up a Monte Carlo simulation, see
    :ref:`ensembles`.

    Cluster expansions, e.g., of the energy, typically yield property
    values *per site*. When running a Monte Carlo simulation one,
    however, considers changes in the *total* energy of the
    system. The default behavior is therefore to multiply the output
    of the cluster expansion by the number of sites. This behavior can
    be changed via the :attr:`scaling` keyword parameter.

    The calculator holds the occupations of its supercell and evaluates
    property changes against them.
    They are taken from the structure it is constructed with, so every site of
    that structure has to carry a species the cluster expansion defines.
    The synchronization contract with the ensemble machinery is that the
    held occupations change only through an explicit accept: the ensemble
    calls :func:`set_occupations` once at setup and :func:`accept_change`
    for every accepted move, and :func:`calculate_change` is guaranteed to
    leave the held occupations untouched, including when it raises.
    The compiled calculator behind this class, reachable as
    :attr:`cpp_calc`, states its thread contract in its own docstring.

    Parameters
    ----------
    structure
        Structure for which to set up the calculator.
    cluster_expansion
        Cluster expansion from which to build calculator.
    name
        Human-readable identifier for this calculator.
    scaling
        Scaling factor applied to the property value predicted by the
        cluster expansion.
    use_local_energy_calculator
        Evaluate energy changes using only the local environment; this method
        is generally *much* faster. Unless you know what you are doing do *not*
        set this option to ``False``.
    """

    def __init__(self,
                 structure: Atoms, cluster_expansion: ClusterExpansion,
                 name: str = 'Cluster Expansion Calculator',
                 scaling: float | None = None,
                 use_local_energy_calculator: bool = True) -> None:
        super().__init__(name=name)

        structure_cpy = structure.copy()

        self.use_local_energy_calculator = use_local_energy_calculator

        # The calculator describes a model of its own, so that pruning it
        # reaches nothing the caller holds.
        self._cluster_expansion = cluster_expansion.copy()
        self._cluster_expansion.prune()

        # The compiled calculator takes a snapshot of the cluster space it is
        # given, which is why it is built after the prune.
        self.cpp_calc = _ClusterExpansionCalculator(
            cluster_space=self._cluster_expansion._cluster_space,
            **structure_to_arrays(structure_cpy),
            fractional_position_tolerance=self._cluster_expansion.fractional_position_tolerance)

        if self.cpp_calc.is_self_interacting:
            logger.warning('The ClusterExpansionCalculator self-interacts, '
                           'which may lead to erroneous results. To avoid '
                           'self-interaction, use a larger supercell or a '
                           'cluster space with shorter cutoffs.')

        # The parameter vector is the one the cluster expansion above holds, so
        # that this calculator evaluates exactly the model it reports.
        self._parameters = self._cluster_expansion._parameters

        if scaling is None:
            self._property_scaling = len(structure)
        else:
            self._property_scaling = scaling

        self._sublattices = self._cluster_expansion._cluster_space.get_sublattices(structure)

    @property
    def cluster_expansion(self) -> ClusterExpansion:
        """ Cluster expansion this calculator evaluates (copy).

        The orbits whose parameters are all zero are left out of it, see
        :func:`ClusterExpansion.prune`.

        It is handed out as a copy, so the calculator cannot be steered through
        it. Editing its parameters, pruning it, or editing a value nested in
        its metadata changes neither what the calculator computes nor what the
        next read of this property reports.
        """
        return self._cluster_expansion.copy()

    def calculate_total(self, *, occupations: list[int]) -> float:
        """
        Calculates and returns the total property value of the current
        configuration.

        Parameters
        ----------
        occupations
            The entire occupation vector (i.e., list of atomic species).
        """

        cv = self.cpp_calc.get_cluster_vector(occupations)
        return np.dot(cv, self._parameters) * self._property_scaling

    def set_occupations(self, occupations: list[int]) -> None:
        """
        Sets the configuration this calculator describes.
        An ensemble calls this once at setup and keeps the calculator in
        step afterwards through :func:`accept_change`; see the class
        docstring for the synchronization contract.

        Parameters
        ----------
        occupations
            The entire occupation vector (atomic numbers).
        """
        self.cpp_calc.set_occupations(occupations)

    def accept_change(self, *, sites: list[int] | None = None,
                      species: list[int] | None = None) -> None:
        """
        Advances the configuration this calculator describes through an
        accepted change, which is the only way it moves during a
        simulation.

        Calling this method without stating which change was accepted
        raises rather than doing nothing, because silently not advancing
        would leave the calculator evaluating every subsequent change
        against a stale configuration, with no error anywhere.
        An empty list of sites is a legitimate empty change and does
        nothing.

        Parameters
        ----------
        sites
            Indices of the sites whose occupations changed.
        species
            New occupations (atomic numbers) on those sites.
        """
        if sites is None or species is None:
            raise TypeError('accept_change requires the sites and species of the '
                            'accepted change, since this calculator holds the '
                            'configuration and advances it only through accepted '
                            'changes.')
        if len(sites) != len(species):
            raise ValueError('sites and species must have the same length.')
        if len(sites) == 0:
            return
        self.cpp_calc.apply_moves([[(int(site), int(occupation))
                                    for site, occupation in zip(sites, species)]])

    def calculate_change(self, *, sites: list[int],
                         current_occupations: list[int],
                         new_site_occupations: list[int]) -> float:
        """
        Calculates and returns the sum of the contributions to the property
        due to the sites specified in :attr:`sites`.

        The local calculation evaluates the change against the occupations
        this calculator holds, which the ensemble machinery keeps equal to
        :attr:`current_occupations` through :func:`set_occupations` and
        :func:`accept_change`; when calling this method outside an
        ensemble, call :func:`set_occupations` first.

        Parameters
        ----------
        sites
            Indices of sites at which occupations will be changed.
        current_occupations
            Entire occupation vector (atomic numbers) before change.
            The local calculation does not read it; it exists for the
            calculator interface and for the fallback path below.
        new_site_occupations
            Atomic numbers after change at the sites defined by :attr:`sites`.

        Raises
        ------
        ValueError
            If :attr:`sites` and :attr:`new_site_occupations` differ in length.
        """
        if len(sites) != len(new_site_occupations):
            raise ValueError('sites and new_site_occupations must have the same'
                             ' length, not {} and {}.'
                             .format(len(sites), len(new_site_occupations)))

        if not self.use_local_energy_calculator:
            occupations = np.array(current_occupations)
            e_before = self.calculate_total(occupations=occupations)
            occupations[sites] = np.array(new_site_occupations)
            e_after = self.calculate_total(occupations=occupations)
            return e_after - e_before

        # The trial move is one move: an ordered sequence of
        # (site, new occupation) pairs, evaluated sequentially by the
        # batched entry point against the held occupations.
        # Errors from the evaluation are raised as they are rather than
        # rewritten as a suggestion to evaluate the whole supercell instead.
        # They report an invalid site or a species the model does not define,
        # which the full evaluation would reject in the same way.
        move = [(int(site), int(occupation))
                for site, occupation in zip(sites, new_site_occupations)]
        changes = self.cpp_calc.get_cluster_vector_changes([move])
        change = np.dot(changes[0], self._parameters)
        return change * self._property_scaling

    @property
    def sublattices(self) -> Sublattices:
        """ Sublattices of the calculator structure. """
        return self._sublattices
