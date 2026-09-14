import os

from .imports import (
    imports,
    os,
    load_dotenv,
    is_file,
    eatAll,
    eatInner,
    eatOuter,
    safe_split,
    line_contains,
    is_list,
    is_bool,
    get_slash,
    path_join,
    if_not_last_child_join,
    get_home_folder,
    simple_path_join,
    DEFAULT_FILE_NAME,
    DEFAULT_KEY,
    find_and_read_env_file,
    search_for_env_key,
    check_env_file,
    safe_env_load,
    get_env_value,
    split_eq,
    dotenv_load,
)
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
