from icet.tools import ConstituentStrain
from icet import ClusterExpansion
from mchammer.calculators import ClusterExpansionCalculator
import numpy as np


class ConstituentStrainCalculator(ClusterExpansionCalculator):
    """
    Calculator for handling cluster expansions with strain.

    Parameters
    ----------
    constituent_strain
        :class:`ConstituentStrain` object defining the strain energy
        properties of the system. The supercell used to
        create this object should correspond to the one
        used when running Monte Carlo simulations with this
        calculator
    cluster_expansion
        Cluster expansion based on which to set up :class:`ClusterExpansionCalculator`.
    name
        Human-readable identifier for this calculator.
    scaling
        Scaling factor applied to the property value predicted by the
        cluster expansion.
    """

    def __init__(self, constituent_strain: ConstituentStrain,
                 cluster_expansion: ClusterExpansion,
                 name: str = 'Constituent Strain Calculator',
                 scaling: float | None = None):
        self.constituent_strain = constituent_strain
        super().__init__(structure=constituent_strain.supercell,
                         cluster_expansion=cluster_expansion,
                         name=name,
                         scaling=scaling)

    def set_occupations(self, occupations: list[int]) -> None:
        """
        Sets the configuration this calculator describes, both for the
        underlying cluster expansion calculator and for the
        :class:`ConstituentStrain` object.

        Parameters
        ----------
        occupations
            The entire occupation vector (atomic numbers).
        """
        super().set_occupations(occupations)
        # The structure factor stored for each k-point describes one
        # configuration, and the change evaluation reads it as the value
        # before the change rather than recomputing it from the occupations
        # it is given. Moving to a configuration that is not reachable from
        # the stored one through accepted changes therefore has to rebuild it,
        # which a total evaluation does for every k-point.
        self.constituent_strain.get_constituent_strain(np.asarray(occupations))

    def calculate_total(self, *, occupations: np.ndarray) -> float:
        """
        Calculates and returns the total property value of the current
        configuration.

        Parameters
        ----------
        occupations
            The entire occupation vector (i.e., an array of atomic numbers as integers).
        """
        e = super().calculate_total(occupations=occupations)
        # The structure factors are left where they are, since a total
        # evaluation scores the occupations it is given and must not move the
        # configuration the next change is evaluated against.
        e += len(occupations) * \
            self.constituent_strain.get_constituent_strain(
                occupations, update_structure_factors=False)
        return e

    def calculate_change(self, *, sites: list[int],
                         current_occupations: list[int],
                         new_site_occupations: list[int]) -> float:
        """
        Calculates and returns the sum of the contributions to the property
        due to the sites specified in :attr:`sites`.

        Parameters
        ----------
        sites
            Indices of sites at which occupations will be changed.
        current_occupations
            Entire occupation vector (atomic numbers) before change.
        new_site_occupations
            Atomic numbers after change at the sites defined by :attr:`sites`.
        """
        if len(new_site_occupations) > 1:
            raise NotImplementedError('Only single flips are currently allowed in '
                                      'conjunction with the constituent strain calculator.')
        e = super().calculate_change(sites=sites,
                                     current_occupations=current_occupations,
                                     new_site_occupations=new_site_occupations)
        de_cs = self.constituent_strain.get_constituent_strain_change(current_occupations,
                                                                      sites[0])
        e += len(current_occupations) * de_cs
        return e

    def accept_change(self, *, sites: list[int] | None = None,
                      species: list[int] | None = None) -> None:
        """Advances the configuration held by the underlying cluster
        expansion calculator and informs the :class:`ConstituentStrain`
        object that the most recent change was accepted, such that the new
        structure factor can be stored.

        Parameters
        ----------
        sites
            Indices of the sites whose occupations changed.
        species
            New occupations (atomic numbers) on those sites.
        """
        super().accept_change(sites=sites, species=species)
        # An empty change advances nothing, so the structure factors must not
        # advance either. Forwarding it would commit the candidate the last
        # change evaluation staged, which is the trial that was rejected.
        if len(sites) == 0:
            return
        self.constituent_strain.accept_change()
