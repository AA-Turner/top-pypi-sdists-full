from .imports import (
    imports,
    os,
    Path,
    safe_join,
    is_file,
)
from .directory_utils import (
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
)
def get_file_name(file_path: str) -> str:
    """
    Retrieves and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file (without extension).
    """
    return split_text(get_base_name(file_path))[0]
def get_abs_name_of_this():
    """
    Returns the absolute name of the current module.

    Returns:
        Path: The absolute name of the current module.
    """
    return os.path.abspath(__name__)
def sanitize_filename(name: str):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
    name (str): Filename to sanitize.
    
    Returns:
    str: Sanitized filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)
def get_base_name(file_path: str) -> str:
    """
    Extracts and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file.
    """
    return os.path.basename(file_path)
