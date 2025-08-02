from typing import Any, Dict
from abc import ABC, abstractmethod

class IEnv(ABC):

    @staticmethod
    @abstractmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Retrieve the value of an environment variable by key.

        Parameters
        ----------
        key : str
            The name of the environment variable to retrieve.
        default : Any, optional
            The value to return if the key is not found. Default is None.

        Returns
        -------
        Any
            The value of the environment variable if found, otherwise the default value.
        """
        pass

    @staticmethod
    @abstractmethod
    def set(key: str, value: str, type: str = None) -> bool:
        """
        Set an environment variable in the .env file.

        Parameters
        ----------
        key : str
            The name of the environment variable to set.
        value : str
            The value to assign to the environment variable.
        type : str, optional
            The type of the environment variable (e.g., 'str', 'int'). Default is None.

        Returns
        -------
        bool
            True if the variable was set successfully, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def unset(key: str) -> bool:
        """
        Remove the specified environment variable from the .env file.

        Parameters
        ----------
        key : str
            The name of the environment variable to remove.

        Returns
        -------
        bool
            True if the variable was successfully removed, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def all() -> Dict[str, Any]:
        """
        Retrieve all environment variables as a dictionary.

        Returns
        -------
        dict of str to Any
            A dictionary containing all environment variables loaded by DotEnv.
        """
        pass