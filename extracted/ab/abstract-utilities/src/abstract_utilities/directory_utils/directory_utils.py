from .utils import (
    imports,
    os,
    Path,
    safe_join,
    is_file,
    split_text,
    get_ext,
    get_slash,
    get_current_path,
    get_home_folder,
    simple_path_join,
    path_join,
    update_global_variable,
    trunc,
    raw_create_dirs,
    mkdirs,
    makedirs,
    get_file_name,
    get_abs_name_of_this,
    sanitize_filename,
    get_base_name,
)

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
make_dirs = makedirs
makeAllDirs = raw_create_dirs

