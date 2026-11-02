from .imports import (
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
    raw_create_dirs,
    mkdirs,
    makedirs,
    get_file_name,
    get_abs_name_of_this,
    sanitize_filename,
    get_base_name,
)
def simple_path_join(path_A:str, path_B:str):
    """
    Join two paths using the appropriate file path separator.

    Args:
        path_A (str): The first path to join.
        path_B (str): The second path to join.
    
    Returns:
        str: The joined path.
    """
    return os.path.join(str(path_A), str(path_B))

def path_join(path_A, path_B=None):
    """
    Joins two paths or a list of paths using the appropriate file path separator.

    Args:
        path_A (str or list): The first path or list of paths to join.
        path_B (str, optional): The second path to join. Defaults to None.
    
    Returns:
        str: The joined path.
    """
    if path_B is not None:  # If path_B is provided, join path_A and path_B
        return simple_path_join(path_A, path_B)
    if isinstance(path_A, list):  # If path_A is a list, join all paths in the list
        path = path_A[0]
        for k in range(1, len(path_A)):
            path = simple_path_join(path, path_A[k])
        return path
def update_global_variable(name: str, value) -> None:
    """Updates the global variable with the provided name and value.

    Args:
        name (str): The name of the global variable.
        value: The value to assign to the global variable.

    Returns:
        None
    """
    globals()[name] = value


def trunc(a: float, x: int) -> float:
    """
    Truncates a float number to a specific number of decimal places.

    Args:
        a (float): The number to truncate.
        x (int): The number of decimal places to retain.

    Returns:
        float: The truncated float number.
    """
    temp = str(a)
    for i in range(len(temp)):
        if temp[i] == '.':
            try:
                return float(temp[:i+x+1])
            except:
                return float(temp)
    return float(temp)




