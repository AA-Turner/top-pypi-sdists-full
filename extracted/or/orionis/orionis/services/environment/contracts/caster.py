from abc import ABC, abstractmethod

class IEnvironmentCaster(ABC):

    @abstractmethod
    def to(self, type_hint: str):
        """
        Set the type hint for the Type instance.

        Parameters
        ----------
        type_hint : str
            The type hint to assign. Must be one of the valid options defined in OPTIONS.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided type hint is not among the valid options.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Retrieve the value corresponding to the specified type hint.

        Checks the validity of the provided type hint and dispatches the call to the appropriate
        handler for the type. Supported type hints include: 'path:', 'str:', 'int:', 'float:',
        'bool:', 'list:', 'dict:', 'tuple:', and 'set:'.

        Returns
        -------
        Any
            The value converted or processed according to the specified type hint.

        Raises
        ------
        OrionisEnvironmentValueError
            If the type hint is not supported.
        """
        pass
