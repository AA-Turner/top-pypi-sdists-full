from abc import ABC, abstractmethod

class IEnvironmentCaster(ABC):

    @abstractmethod
    def to(self, type_hint: str):
        """
        Set the type hint for the Type instance.

        Parameters
        ----------
        type_hint : str
            The type hint to set, which must be one of the valid options defined in OPTIONS.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided type hint is not one of the valid options.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Returns the value corresponding to the specified type hint.

        Checks if the provided type hint is valid and then dispatches the call to the appropriate
        method for handling the type.

        Supported type hints include: 'path:', 'str:', 'int:', 'float:', 'bool:', 'list:', 'dict:', 'tuple:', and 'set:'.

        Returns
        -------
        Any
            The value converted or processed according to the specified type hint.

        Raises
        ------
        OrionisEnvironmentValueError
            If the type hint is not one of the supported options.
        """
        pass