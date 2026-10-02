import hashlib
import json
import random
import numpy as np
from ase import Atoms
from icet.core.sublattices import Sublattices
from icet.tools.geometry import atomic_number_to_chemical_symbol


class SwapNotPossibleError(Exception):
    pass


# Atomic number that ASE assigns to the vacancy species 'X'. A site is
# considered occupied when its occupation differs from this value.
VACANCY_ATOMIC_NUMBER = 0


def get_constraint_hash(neighbor_sites_to_avoid: dict[int, list[int]]) -> str:
    """Returns a short digest that identifies a neighbor constraint.

    The digest lets a simulation that is restarted from a data container be
    checked against the constraint the data container was written with, without
    storing a mapping whose size grows with the system.
    It is computed from a canonical form, so that a mapping written in a
    different order gives the same digest. Sites without neighbors are dropped,
    so that two mappings which impose the same rules agree even when one of them
    lists unconstrained sites explicitly.

    Parameters
    ----------
    neighbor_sites_to_avoid
        Sites that must not be occupied simultaneously, keyed by site index.
    """
    canonical = sorted((int(site), sorted(int(n) for n in neighbors))
                       for site, neighbors in neighbor_sites_to_avoid.items() if neighbors)
    return hashlib.sha1(json.dumps(canonical).encode()).hexdigest()[:16]


class ConfigurationManager(object):
    """
    The ConfigurationManager owns and handles information pertaining to a
    configuration being sampled in a Monte Carlo simulation.

    Note
    ----
    As a user you will usually not interact directly with objects of this type.

    Parameters
    ----------
    structure : Atoms
        Configuration to be handled.
    sublattices : :class:`Sublattices <icet.core.sublattices.Sublattices>`
        Sublattices used to define allowed occupations and handle related information.
    """

    def __init__(self, structure: Atoms, sublattices: Sublattices) -> None:
        self._structure = structure.copy()
        self._occupations = self._structure.numbers
        self._sublattices = sublattices
        self._sites_by_species = self._get_sites_by_species()
        self._neighbor_sites_to_avoid: dict[int, list[int]] | None = None

    def _get_sites_by_species(self) -> list[dict[int, list[int]]]:
        """Returns the sites that are occupied for each species.  Each
        dictionary represents one sublattice where the key is the
        species (by atomic number) and the value is the list of sites
        occupied by said species in the respective sublattice.
        """
        sites_by_species = []
        for sl in self._sublattices:
            species_dict = {key: [] for key in sl.atomic_numbers}
            for site in sl.indices:
                species_dict[self._occupations[site]].append(site)
            sites_by_species.append(species_dict)
        return sites_by_species

    @property
    def occupations(self) -> np.ndarray:
        """ Occupation vector of the configuration (copy). """
        return self._occupations.copy()

    @property
    def sublattices(self) -> Sublattices:
        """ Sublattices of the configuration. """
        return self._sublattices

    @property
    def structure(self) -> Atoms:
        """ Atomic structure associated with configuration (copy). """
        structure = self._structure.copy()
        structure.set_atomic_numbers(self.occupations)
        return structure

    def get_occupations_on_sublattice(self, sublattice_index: int) -> list[int]:
        """
        Returns the occupations on one sublattice.

        Parameters
        ---------
        sublattice_index
            Sublattice by index for which the occupations should be returned.
        """
        sl = self.sublattices[sublattice_index]
        return list(self.occupations[sl.indices])

    def is_swap_possible(self, sublattice_index: int,
                         allowed_species: list[int] | None = None) -> bool:
        """ Checks if a swap trial move is possible on a specific sublattice.

        Parameters
        ----------
        sublattice_index
            Index of sublattice to be checked.
        allowed_species
            List of atomic numbers for allowed species.
         """
        sl = self.sublattices[sublattice_index]
        if allowed_species is None:
            swap_symbols = set(self.occupations[sl.indices])
        else:
            swap_symbols = set([o for o in self.occupations[sl.indices] if o in
                                allowed_species])
        return len(swap_symbols) > 1

    def get_swapped_state(self, sublattice_index: int,
                          allowed_species: list[int] | None = None,
                          allowed_sites: list[int] | None = None
                          ) -> tuple[list[int], list[int]]:
        """Returns two random sites (first element of tuple) and their
        occupation after a swap (second element of tuple).  The new
        configuration will obey the occupation constraints associated
        with the :class:`ConfigurationManager` object.

        Parameters
        ----------
        sublattice_index
            Sublattice by index from which to pick sites.
        allowed_species
            List of atomic numbers for allowed species.
        allowed_sites
            List of indices for allowed sites.
        """
        # pick the first site
        if allowed_species is None:
            available_sites = self.sublattices[sublattice_index].indices
        else:
            available_sites = [
                s for Z in allowed_species for s in
                self._get_sites_by_species()[sublattice_index][Z]]

        # only include allowed sites
        if allowed_sites is not None:
            available_sites = list(set(available_sites).intersection(allowed_sites))

        try:
            site1 = random.choice(available_sites)
        except IndexError:
            raise SwapNotPossibleError(f'Sublattice {sublattice_index} is empty.')

        # pick the second site
        if allowed_species is None:
            possible_swap_species = \
                set(self._sublattices.get_allowed_numbers_on_site(site1)) - \
                set([self._occupations[site1]])
        else:
            possible_swap_species = \
                set(allowed_species) - set([self._occupations[site1]])
        possible_swap_sites = []
        for Z in possible_swap_species:
            possible_swap_sites.extend(self._sites_by_species[sublattice_index][Z])

        # only include allowed sites
        if allowed_sites is not None:
            possible_swap_sites = list(set(possible_swap_sites).intersection(allowed_sites))

        possible_swap_sites = np.array(possible_swap_sites)

        try:
            site2 = random.choice(possible_swap_sites)
        except IndexError:
            raise SwapNotPossibleError(
                'Cannot swap on sublattice {} since it is full of {} species .'
                .format(sublattice_index,
                        atomic_number_to_chemical_symbol([self._occupations[site1]])[0]))

        return ([site1, site2], [self._occupations[site2], self._occupations[site1]])

    def get_flip_state(
            self,
            sublattice_index: int,
            allowed_species: list[int] | None = None,
            allowed_sites: list[int] | None = None
            ) -> tuple[int, int]:
        """
        Returns a site index and a new species for the site.

        Parameters
        ----------
        sublattice_index
            Index of sublattice from which to pick a site.
        allowed_species
            List of atomic numbers for allowed species.
        allowed_sites
            List of indices for allowed sites.
        """
        if allowed_species is None:
            available_sites = self._sublattices[sublattice_index].indices
        else:
            available_sites = [s for Z in allowed_species for s in
                               self._get_sites_by_species()[sublattice_index][Z]]

        # only include allowed sites
        if allowed_sites is not None:
            available_sites = list(set(available_sites).intersection(allowed_sites))

        site = random.choice(available_sites)
        if allowed_species is not None:
            species = random.choice(list(
                set(allowed_species) - set([self._occupations[site]])))
        else:
            species = random.choice(list(
                set(self._sublattices[sublattice_index].atomic_numbers) -
                set([self._occupations[site]])))
        return site, species

    def update_occupations(self, sites: list[int], species: list[int]) -> None:
        """
        Updates the occupation vector of the configuration being sampled.
        This will change the state in both the configuration in the calculator
        and the configuration manager.

        Parameters
        ----------
        sites
            Indices of sites of the configuration to change.
        species
            New occupations by atomic number.
        """

        # The whole update is checked before any of it is applied, so a
        # rejected update leaves the occupations and the sites by species in
        # the state they were in. Applying as we go would leave the two
        # disagreeing about every site the loop had already reached.
        if len(sites) != len(species):
            raise ValueError('sites and species must have the same length.')
        if len(set(sites)) != len(sites):
            raise ValueError('The same site must not appear more than once'
                             ' in an update: {}'.format(sites))

        for site, new_Z in zip(sites, species):
            if site < 0 or site >= len(self._occupations):
                raise ValueError('Site {} is not a valid site index'.format(site))
            sublattice_index = self.sublattices.get_sublattice_index_from_site_index(site)
            if new_Z not in self.sublattices[sublattice_index].atomic_numbers:
                raise ValueError('Invalid new species {} on site {}'.format(new_Z, site))

        for site, new_Z in zip(sites, species):
            old_Z = self._occupations[site]
            sublattice_index = self.sublattices.get_sublattice_index_from_site_index(site)
            # Move the site from the list of sites for the old species to the
            # list for the new one.
            self._sites_by_species[sublattice_index][old_Z].remove(site)
            self._sites_by_species[sublattice_index][new_Z].append(site)

        # Update occupation vector itself
        self._occupations[sites] = species

    def set_occupations(self, occupations: list[int]) -> None:
        """
        Replaces the occupations of the whole configuration.

        This is the absolute counterpart of :func:`update_occupations`, which
        expresses a change relative to the current configuration. It is what a
        restart needs, since restoring a saved configuration is not the
        acceptance of a move.

        The occupations are checked before anything changes, so a rejected
        input leaves the configuration as it was.

        Parameters
        ----------
        occupations
            New occupations by atomic number, one per site of the configuration.

        Raises
        ------
        ValueError
            If the length does not match the configuration, or if a species is
            not allowed on the site it is given for.
        """
        if len(occupations) != len(self._occupations):
            raise ValueError('occupations must have length {}, not {}'
                             .format(len(self._occupations), len(occupations)))
        for site, new_Z in enumerate(occupations):
            sublattice_index = self.sublattices.get_sublattice_index_from_site_index(site)
            if new_Z not in self.sublattices[sublattice_index].atomic_numbers:
                raise ValueError('Invalid new species {} on site {}'.format(new_Z, site))

        # Assign in place, since the occupations are the atomic numbers of the
        # structure this manager was built from.
        self._occupations[:] = occupations
        self._sites_by_species = self._get_sites_by_species()

    @property
    def neighbor_sites_to_avoid(self) -> dict[int, list[int]] | None:
        """ Sites that must not be occupied simultaneously, keyed by site index (copy). """
        if self._neighbor_sites_to_avoid is None:
            return None
        return {site: list(neighbors)
                for site, neighbors in self._neighbor_sites_to_avoid.items()}

    def set_neighbor_sites_to_avoid(self,
                                    neighbor_sites_to_avoid: dict[int, list[int]] | None
                                    ) -> None:
        """Sets the neighbor constraint that trial moves have to respect.

        The constraint belongs to the configuration rather than to an individual
        trial move, so that it cannot apply to some moves and not to others.
        It governs the trial steps of :class:`ThermodynamicBaseEnsemble
        <mchammer.ensembles.ThermodynamicBaseEnsemble>` that carry out a swap, an
        SGC flip or a VCSGC flip. Thermodynamic integration, Wang-Landau sampling
        and target cluster vector annealing generate their trial moves
        differently and are not subject to it.

        Rejecting a trial move leaves the proposal unchanged and therefore
        symmetric, so the acceptance criterion stays exact and the constraint
        introduces no bias of its own. That alone does not guarantee that the whole
        constrained space is sampled: a restrictive mapping can leave the allowed
        configurations disconnected under the available trial moves, in which case
        the simulation only reaches the part it starts in.

        Parameters
        ----------
        neighbor_sites_to_avoid
            Sites that must not be occupied simultaneously, keyed by site index.
            Sites that are absent from the mapping are unconstrained. ``None``
            removes the constraint. The mapping is copied, so changing it
            afterwards does not change the constraint.

        Raises
        ------
        ValueError
            If the constraint is not usable, see :func:`validate_constraint`.
        """
        if neighbor_sites_to_avoid is None:
            self._neighbor_sites_to_avoid = None
            return
        # a copy, so that mutating the mapping afterwards cannot get around the
        # validation below; the indices are normalized on the way in, which also
        # accepts the numpy integers that a neighbor list produces
        constraint = {int(site): [int(n) for n in neighbors]
                      for site, neighbors in neighbor_sites_to_avoid.items()}
        self.validate_constraint(constraint)
        self._neighbor_sites_to_avoid = constraint

    def is_constraint_violated(self, sites: list[int], species: list[int]) -> bool:
        """Checks whether a trial move would violate the neighbor constraint.

        The constraint forbids two sites that appear in each other's avoid list
        from being occupied at the same time, where a site counts as occupied
        when it is not held by a vacancy.
        Provided that the current configuration satisfies the constraint, only
        the sites touched by the trial move can introduce a violation, which is
        what allows this check to be local.

        Parameters
        ----------
        sites
            Indices of the sites that the trial move would change.
        species
            Occupations by atomic number that the trial move would assign to
            :attr:`sites`.

        Returns
        -------
        ``True`` if applying the trial move would place occupants on two sites
        that appear in each other's avoid list, ``False`` otherwise. Always
        ``False`` when no constraint is set.
        """
        if self._neighbor_sites_to_avoid is None:
            return False
        trial_occupations = dict(zip(sites, species))
        for site, new_species in trial_occupations.items():
            if new_species == VACANCY_ATOMIC_NUMBER:
                continue
            for neighbor in self._neighbor_sites_to_avoid.get(site, ()):
                # a neighbor that the trial move also touches must be evaluated
                # in its trial state rather than its current one
                occupant = trial_occupations.get(neighbor, self._occupations[neighbor])
                if occupant != VACANCY_ATOMIC_NUMBER:
                    return True
        return False

    def validate_constraint(self, neighbor_sites_to_avoid: dict[int, list[int]]) -> None:
        """Checks that a neighbor constraint is usable for the current configuration.

        The configuration has to satisfy the constraint already. Each trial move
        is only checked against the sites it touches, which assumes that the rest
        of the configuration satisfies the constraint. A violating configuration
        is not stuck, since emptying an offending site is never rejected, but the
        sampling is biased until the violations happen to be cleared.

        Parameters
        ----------
        neighbor_sites_to_avoid
            Sites that must not be occupied simultaneously, keyed by site index.
            Sites that are absent from the mapping are unconstrained.

        Raises
        ------
        ValueError
            If the constraint refers to a site that does not exist, if a site is
            listed against itself, if it is not symmetric, or if the current
            configuration already violates it.
        """
        n_sites = len(self._occupations)
        for site, neighbors in neighbor_sites_to_avoid.items():
            for index in (site, *neighbors):
                if not 0 <= index < n_sites:
                    raise ValueError(
                        f'neighbor_sites_to_avoid refers to site {index}, which does not'
                        f' exist in a configuration with {n_sites} sites.')
            if site in neighbors:
                raise ValueError(
                    f'neighbor_sites_to_avoid lists site {site} against itself, which'
                    ' would leave it permanently unoccupiable.')
            for neighbor in neighbors:
                if site not in neighbor_sites_to_avoid.get(neighbor, ()):
                    raise ValueError(
                        'neighbor_sites_to_avoid must be symmetric: site'
                        f' {site} lists {neighbor}, but {neighbor} does not list {site}.')

        for site, neighbors in neighbor_sites_to_avoid.items():
            if self._occupations[site] == VACANCY_ATOMIC_NUMBER:
                continue
            for neighbor in neighbors:
                if self._occupations[neighbor] != VACANCY_ATOMIC_NUMBER:
                    raise ValueError(
                        'The configuration already violates neighbor_sites_to_avoid:'
                        f' sites {site} and {neighbor} are both occupied. Each trial'
                        ' move is only checked against the sites it touches, which'
                        ' assumes that the rest of the configuration satisfies the'
                        ' constraint, so starting here would sample a biased transient.')
