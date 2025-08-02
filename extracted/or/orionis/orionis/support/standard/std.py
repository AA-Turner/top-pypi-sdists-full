from orionis.support.standard.contracts.std import IStdClass
from orionis.support.standard.exceptions import OrionisStdValueException

class StdClass(IStdClass):
    """
    A dynamic class that allows setting arbitrary attributes,
    similar to PHP's stdClass.
    """

    def __init__(self, **kwargs):
        """
        Initializes the StdClass with optional keyword arguments.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to set as attributes.
        """
        self.update(**kwargs)

    def __repr__(self):
        """
        Returns an unambiguous string representation of the object.

        Returns
        -------
        str
            A string that could be used to recreate the object.
        """
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self):
        """
        Returns a readable string representation of the object.

        Returns
        -------
        str
            A user-friendly string showing the object's attributes.
        """
        return str(self.__dict__)

    def __eq__(self, other):
        """
        Compares two StdClass objects for equality based on their attributes.

        Parameters
        ----------
        other : object
            The object to compare with.

        Returns
        -------
        bool
            True if both objects have the same attributes and values.
        """
        if not isinstance(other, StdClass):
            return False
        return self.__dict__ == other.__dict__

    def toDict(self):
        """
        Converts the object's attributes to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the object's attributes.
        """

        # Return a copy to avoid external modifications
        return self.__dict__.copy()

    def update(self, **kwargs):
        """
        Updates the object's attributes dynamically.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to update attributes.

        Raises
        ------
        OrionisStdValueException
            If an attribute name is invalid or conflicts with existing methods.
        """
        for key, value in kwargs.items():
            if key.startswith('__') and key.endswith('__'):
                raise OrionisStdValueException(f"Cannot set attribute with reserved name: {key}")
            if hasattr(self.__class__, key):
                raise OrionisStdValueException(f"Cannot set attribute '{key}' as it conflicts with a class method")
            setattr(self, key, value)

    def remove(self, *attributes):
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
        for attr in attributes:
            if not hasattr(self, attr):
                raise AttributeError(f"Attribute '{attr}' not found")
            delattr(self, attr)

    @classmethod
    def fromDict(cls, dictionary):
        """
        Creates a StdClass instance from a dictionary.

        Parameters
        ----------
        dictionary : dict
            Dictionary to create the object from.

        Returns
        -------
        StdClass
            A new StdClass instance with the dictionary's key-value pairs as attributes.
        """
        return cls(**dictionary)