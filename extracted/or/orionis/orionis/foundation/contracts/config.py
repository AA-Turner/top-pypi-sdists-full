from abc import ABC, abstractmethod

class IConfig(ABC):
    """
    Abstract base class for configuration holders.

    This interface enforces the presence of a `config` attribute in subclasses,
    which must return a dataclass instance containing configuration data.

    Attributes
    ----------
    config : object
        Dataclass instance representing the configuration data.
    """

    @property
    @abstractmethod
    def config(self):
        """
        Get the configuration dataclass instance.

        Returns
        -------
        object
            Dataclass instance containing the configuration data.

        Notes
        -----
        Subclasses must implement this property to provide access to their configuration.
        """
        pass
