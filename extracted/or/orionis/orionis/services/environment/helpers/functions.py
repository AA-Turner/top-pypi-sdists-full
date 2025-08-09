from typing import Any
from orionis.services.environment.core.dot_env import DotEnv

def env(key: str, default: Any = None) -> Any:
    """
    Retrieves the value of an environment variable.

    Parameters
    ----------
    key : str
        The name of the environment variable to retrieve.
    default : Any, optional
        The value to return if the environment variable is not found. Defaults to None.

    Returns
    -------
    Any
        The value of the environment variable if it exists, otherwise the specified default value.
    """

    # Instantiate DotEnv and retrieve the environment variable by key
    return DotEnv().get(key, default)