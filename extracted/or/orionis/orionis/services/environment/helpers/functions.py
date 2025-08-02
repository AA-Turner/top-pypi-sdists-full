from typing import Any
from orionis.services.environment.core.dot_env import DotEnv

def env(key: str, default: Any = None) -> Any:
    """
    Retrieve the value of an environment variable.

    Parameters
    ----------
    key : str
        The name of the environment variable to retrieve.
    default : Any, optional
        The value to return if the environment variable is not found. Default is None.

    Returns
    -------
    Any
        The value of the environment variable if it exists, otherwise the default value.
    """
    return DotEnv().get(key, default)