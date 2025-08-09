from abc import ABC, abstractmethod
from typing import Any, Dict

class IStdClass(ABC):
    """
    Abstract base class for a dynamic object that allows arbitrary attribute assignment,
    similar to PHP's stdClass.

    Implementations must support dynamic attribute management and provide methods for
    representation, comparison, serialization, and attribute manipulation.
    """

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the object with optional attributes.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to set as initial attributes.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the object.

        Returns
        -------
        str
            String representation suitable for debugging and object recreation.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a readable string representation of the object.

        Returns
        -------
        str
            Human-readable string displaying the object's attributes.
        """
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """
        Compare this object with another for equality based on attributes.

        Parameters
        ----------
        other : Any
            Object to compare against.

        Returns
        -------
        bool
            True if both objects have identical attributes and values, False otherwise.
        """
        pass

    @abstractmethod
    def toDict(self) -> Dict[str, Any]:
        """
        Convert the object's attributes to a dictionary.

        Returns
        -------
        dict of str to Any
            Dictionary containing the object's attribute names and values.
        """
        pass

    @abstractmethod
    def update(self, **kwargs: Any) -> None:
        """
        Update the object's attributes with the provided key-value pairs.

        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to update or add as attributes.

        Raises
        ------
        ValueError
            If an attribute name is invalid or conflicts with existing methods.
        """
        pass

    @abstractmethod
    def remove(self, *attributes: str) -> None:
        """
        Remove one or more attributes from the object.

        Parameters
        ----------
        *attributes : str
            Names of the attributes to remove.

        Raises
        ------
        AttributeError
            If any specified attribute does not exist.
        """
        pass

    @classmethod
    @abstractmethod
    def fromDict(cls, dictionary: Dict[str, Any]) -> 'IStdClass':
        """
        Create an instance from a dictionary of attributes.

        Parameters
        ----------
        dictionary : dict of str to Any
            Dictionary containing attribute names and values.

        Returns
        -------
        IStdClass
            New instance with attributes set from the dictionary.
        """
        pass