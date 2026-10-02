from abc import ABC, abstractmethod


class BaseCalculator(ABC):
    """
    Base class for calculators.

    Attributes
    ----------
    name : str
        Human-readable calculator name.
    """

    def __init__(self, name='BaseCalculator'):
        self.name = name

    @abstractmethod
    def calculate_total(self):
        pass

    @abstractmethod
    def calculate_change(self):
        pass

    def set_occupations(self, occupations: list[int]) -> None:
        """
        Sets the configuration a stateful calculator describes.
        Calculators that hold no configuration state ignore this.

        Parameters
        ----------
        occupations
            The entire occupation vector (atomic numbers).
        """
        pass

    def accept_change(self, *, sites: list[int] | None = None,
                      species: list[int] | None = None) -> None:
        """
        Some calculators depend on the state of the occupations, in which
        case they need to be informed when an accepted change advances the
        configuration.

        Parameters
        ----------
        sites
            Indices of the sites whose occupations changed.
        species
            New occupations (atomic numbers) on those sites.
        """
        pass

    @property
    def sublattices(self):
        raise NotImplementedError()
