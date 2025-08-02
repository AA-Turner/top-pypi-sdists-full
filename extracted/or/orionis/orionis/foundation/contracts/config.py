from abc import ABC, abstractmethod

class IConfig(ABC):
    """
    An abstract base class that defines an interface for classes that must have
    a `config` attribute.

    The subclass is required to implement the `config` attribute, which should be
    a dataclass instance representing the configuration data.

    Attributes
    ----------
    config : object
        A dataclass instance representing the configuration.
    """

    @property
    @abstractmethod
    def config(self):
        """
        Should return a dataclass instance representing the configuration.
        """
        pass
