import os

from .imports import *
from .abstractEnv import abstractEnv
def get_env_value(key:str=None,path:str=None,file_name:str=None,deep_scan=False):
    # Process environment takes precedence over the .env file so exported /
    # systemd / container env vars are always honored.
    if key and os.environ.get(key) is not None:
        return os.environ[key]
    abstract_env = abstractEnv(key=key, file_name=file_name, path=path,deep_scan=deep_scan)

    """
    Retrieves the value of a specified environment variable from a .env file.

    Args:
        key (str, optional): The key to search for in the .env file. Defaults to None.
        path (str, optional): The path to the .env file. Defaults to None.
        file_name (str, optional): The name of the .env file. Defaults to None.

    Returns:
        str: The value of the environment variable if found, otherwise None.
    """
    return abstract_env.env_value


def get_env_path(key:str=None,path:str=None,file_name:str=None,deep_scan=False):
    abstract_env = abstractEnv(key=key, file_name=file_name, path=path,deep_scan=deep_scan)
    """
    Retrieves the value of a specified environment variable from a .env file.

    Args:
        key (str, optional): The key to search for in the .env file. Defaults to None.
        path (str, optional): The path to the .env file. Defaults to None.
        file_name (str, optional): The name of the .env file. Defaults to None.

    Returns:
        str: The value of the environment variable if found, otherwise None.
    """
    return abstract_env.env_path
