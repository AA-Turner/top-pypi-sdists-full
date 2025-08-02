from abc import ABC, abstractmethod
from typing import Any, Dict

class IStdClass(ABC):
    """
    Interface for a dynamic class that allows setting arbitrary attributes,
    similar to PHP's stdClass.

    Implementations should provide dynamic attribute access and management.
    """

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the object with optional attributes.

        Parameters
        ----------
        kwargs : Any
            Key-value pairs to set as initial attributes.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the object.

        Returns
        -------
        str
            A string that could be used to recreate the object.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a readable string representation of the object.

        Returns
        -------
        str
            A user-friendly string showing the object's attributes.
        """
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """
        Compares two objects for equality based on their attributes.

        Parameters
        ----------
        other : Any
            The object to compare with.

        Returns
        -------
        bool
            True if both objects have the same attributes and values.
        """
        pass

    @abstractmethod
    def toDict(self) -> Dict[str, Any]:
        """
        Converts the object's attributes to a dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the object's attributes.
        """
        pass

    @abstractmethod
    def update(self, **kwargs: Any) -> None:
        """
        Updates the object's attributes dynamically.

        Parameters
        ----------
        kwargs : Any
            Key-value pairs to update attributes.

        Raises
        ------
        ValueError
            If an attribute name is invalid or conflicts with existing methods.
        """
        pass

    @abstractmethod
    def remove(self, *attributes: str) -> None:
        """
        Removes one or more attributes from the object.

        Parameters
        ----------
        *attributes : str
            Names of the attributes to remove.

        Raises
        ------
        AttributeError
            If any of the attributes doesn't exist.
        """
        pass

    @classmethod
    @abstractmethod
    def fromDict(cls, dictionary: Dict[str, Any]) -> 'IStdClass':
        """
        Creates an instance from a dictionary.

        Parameters
        ----------
        dictionary : Dict[str, Any]
            Dictionary to create the object from.

        Returns
        -------
        IStdClass
            A new instance with the dictionary's key-value pairs as attributes.
        """
        pass