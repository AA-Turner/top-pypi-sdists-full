from pathlib import Path
from .utils import *

def get_shortest_path(*args):
    shortest = None
    args = {arg:str(arg).split('/') for arg in args if arg}
    for path,spl in args.items():
        if shortest is None or (len(spl)<len(shortest[-1])):
            shortest=[path,spl]
    return shortest[0]
def get_common_root(paths):
    """
    Compute the deepest common parent directory of all sysroots.
    """
    paths = [Path(p).resolve() for p in paths]
    common = os.path.commonpath(paths)
    return common

def get_dirs(path):
    """
    Get List of Immediate Subdirectories in a Path

    This function uses the os.walk method to traverse through a directory tree and returns a list of immediate subdirectories
    within the specified path.

    Parameters:
    - path (str): The path for which subdirectories need to be retrieved.

    Returns:
    - subdirectories (list): A list of immediate subdirectories within the specified path.

    Example:
    subdirs = get_dirs("/path/to/directory")
    print("Immediate Subdirectories:", subdirs)
    """
    from os import walk
    for (dirpath, dirnames, filenames) in walk(path):
        return dirnames
def get_directory(file_path: str) -> str:
    """
    Extracts and returns the directory path from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The directory path extracted from the file path.
    """
    return os.path.dirname(file_path)
def if_not_last_child_join(path:str,child:str):
    """
    Adds a child path to the given path if it's not already present at the end.

    Args:
        path (str): The parent path.
        child (str): The child path to add.
    
    Returns:
        str: The updated path.
    """
    if path.endswith(child):
        return path
    return simple_path_join(path, child)
def createFolds(ls: list) -> None:
    """
    Creates multiple directories.

    Args:
        ls (list): The list of directory paths to create.
    """
    for k in range(len(ls)):
        mkdirs(ls[k])
def list_directory_contents(path: str) -> list:
    """Returns a list of directory contents or a list with a single file, if the path is a file.

    Args:
        path (str): The path of the directory or file.

    Returns:
        list: A list of directory contents or a list with a single file path.
    """
    if is_file(path):
        return [path]
    elif is_valid_path(path):
        return os.listdir(path)
    return [path]
def is_string_in_dir(path,strings,**kwargs):
    dirname =  path
    if is_file(path,**kwargs):
        dirname = os.path.dirname(path)
    pieces = [pa for pa in dirname.split('/') if pa and pa in strings]
    if pieces:
        return True
    return False
def raw_create_dirs(*paths):
    """Recursively create all directories along the given path."""
    full_path = os.path.abspath(safe_join(*paths))
    sub_parts = [p for p in full_path.split(os.sep) if p]

    current_path = "/" if full_path.startswith(os.sep) else ""
    for part in sub_parts:
        current_path = safe_join(current_path, part)
        os.makedirs(current_path, exist_ok=True)
    return full_path

mkdirs=raw_create_dirs
makedirs = mkdirs
make_dirs = makedirs
makeAllDirs = raw_create_dirs

