from .imports import (
    imports,
    os,
    Path,
    safe_join,
    is_file,
)
from .name_utils import (
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
    get_shortest_path,
    get_common_root,
    get_dirs,
    get_directory,
    if_not_last_child_join,
    createFolds,
    list_directory_contents,
    is_string_in_dir,
    raw_create_dirs,
    mkdirs,
    makedirs,
    make_dirs,
    makeAllDirs,
    get_file_name,
    get_abs_name_of_this,
    sanitize_filename,
    get_base_name,
)
def get_os_info():
    """
    Get Operating System Information

    This function retrieves information about the current operating system, including its name and bit size.

    Returns:
    - os_info (dict): A dictionary containing the operating system information.
                      Keys:
                      - "operating_system" (str): The name of the operating system (e.g., "Windows", "Linux", "Darwin").
                      - "bit_size" (str): The bit size of the operating system (e.g., "32bit", "64bit").

    Example:
    os_info = get_os_info()
    print("Operating System:", os_info["operating_system"])
    print("Bit Size:", os_info["bit_size"])
    """
    os_name = platform.system()
    bit_size = platform.architecture()[0]
    return {"operating_system": os_name, "bit_size": bit_size}
def mkGb(k) -> float:
    """
    Converts a value to Gigabytes (GB).

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB.
    """
    return float(float(k)*(10**9))

def mkGbTrunk(k) -> float:
    """
    Converts a value to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (float): The value to convert to GB.

    Returns:
        float: The value converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(k), 5)

def mkGbTrunFroPathTot(k) -> float:
    """
    Fetches the file size from a path, converts it to Gigabytes (GB) and truncates the result to five decimal places.

    Args:
        k (str): The file path.

    Returns:
        float: The file size converted to GB and truncated to five decimal places.
    """
    return trunc(mkGb(s.path.getsize(k)), 5)
