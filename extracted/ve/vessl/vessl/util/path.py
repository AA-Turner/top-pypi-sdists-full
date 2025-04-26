import os


def ensure_parent_dir_exists(path_to_file: str):
    """
    Given a path to a file, ensure that its parent directory exists,
    creating directories (throughout the hierarchy) if needed.

    Example:
        ensure_parent_dir_exists("./dir1/dir2/file")
        : Ensure that the directory "./dir1/dir2/" exists.

        ensure_parent_dir_exists("/code/mymodel/README.md")
        : Ensure that the directory "/code/mymodel/" exists.

        ensure_parent_dir_exists("path.py")
        : Does nothing.
    """

    dirname = os.path.dirname(path_to_file)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
