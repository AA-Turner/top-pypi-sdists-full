from orionis.support.standard.contracts.std import IStdClass
from orionis.support.standard.exceptions import OrionisStdValueException

class StdClass(IStdClass):
    """
    A dynamic class for storing arbitrary attributes, similar to PHP's stdClass.

    Attributes
    ----------
    Any attribute can be dynamically set via keyword arguments or the `update` method.
    """

    def __init__(self, **kwargs):
        """
        Initialize a StdClass instance with optional attributes.

        Parameters
        ----------
        **kwargs : dict, optional
            Arbitrary keyword arguments to set as attributes.
        """
        self.update(**kwargs)

    def __repr__(self):
        """
        Return an unambiguous string representation of the object.

        Returns
        -------
        str
            String representation suitable for debugging.
        """
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self):
        """
        Return a readable string representation of the object.

        Returns
        -------
        str
            String showing the object's attributes.
        """
        return str(self.__dict__)

    def __eq__(self, other):
        """
        Compare two StdClass objects for equality based on their attributes.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if both objects have the same attributes and values, False otherwise.
        """
        if not isinstance(other, StdClass):
            return False
        return self.__dict__ == other.__dict__

    def toDict(self):
        """
        Convert the object's attributes to a dictionary.

        Returns
        -------
        dict
            A shallow copy of the object's attributes.
        """
        # Return a copy to avoid external modifications
        return self.__dict__.copy()

    def update(self, **kwargs):
        """
        Update the object's attributes dynamically.

        Parameters
        ----------
        **kwargs : dict
            Key-value pairs to update or add as attributes.

        Raises
        ------
        OrionisStdValueException
            If an attribute name is reserved or conflicts with a class method.
        """
        for key, value in kwargs.items():
            if key.startswith('__') and key.endswith('__'):
                raise OrionisStdValueException(f"Cannot set attribute with reserved name: {key}")
            if hasattr(self.__class__, key):
                raise OrionisStdValueException(f"Cannot set attribute '{key}' as it conflicts with a class method")
            setattr(self, key, value)

    def remove(self, *attributes):
        """
        Remove one or more attributes from the object.

        Parameters
        ----------
        *attributes : str
            Names of the attributes to remove.

        Raises
        ------
        AttributeError
            If any of the specified attributes do not exist.
        """
        for attr in attributes:
            if not hasattr(self, attr):
                raise AttributeError(f"Attribute '{attr}' not found")
            delattr(self, attr)

    @classmethod
    def fromDict(cls, dictionary):
        """
        Create a StdClass instance from a dictionary.

        Parameters
        ----------
        dictionary : dict
            Dictionary containing attribute names and values.

        Returns
        -------
        StdClass
            A new StdClass instance with attributes set from the dictionary.
        """
        return cls(**dictionary)