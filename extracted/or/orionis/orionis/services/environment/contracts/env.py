from typing import Any, Dict
from abc import ABC, abstractmethod

class IEnv(ABC):

    @staticmethod
    @abstractmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Retrieves the value of the specified environment variable.

        Parameters
        ----------
        key : str
            The name of the environment variable to retrieve.
        default : Any, optional
            The value to return if the environment variable is not found. Defaults to None.

        Returns
        -------
        Any
            The value of the environment variable if it exists, otherwise the default value.
        """
        pass

    @staticmethod
    @abstractmethod
    def set(key: str, value: str, type: str = None) -> bool:
        """
        Sets the value of an environment variable in the .env file.

        Parameters
        ----------
        key : str
            The name of the environment variable to set.
        value : str
            The value to assign to the environment variable.
        type : str, optional
            The type of the environment variable (e.g., 'str', 'int'). Defaults to None.

        Returns
        -------
        bool
            True if the environment variable was set successfully, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def unset(key: str) -> bool:
        """
        Removes the specified environment variable from the .env file.

        Parameters
        ----------
        key : str
            The name of the environment variable to remove.

        Returns
        -------
        bool
            True if the environment variable was removed successfully, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def all() -> Dict[str, Any]:
        """
        Retrieves all environment variables as a dictionary.

        Returns
        -------
        dict of str to Any
            A dictionary containing all environment variables loaded by DotEnv.
        """
        pass