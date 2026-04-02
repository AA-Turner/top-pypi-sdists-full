import fcntl
import csv
import os


def save_to_csv(data, file_name):
    keys = data[0].keys()
    with open(file_name, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def read_file_with_lock(file_path):
    with open(file_path, "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        try:
            content = file.read()
        finally:
            fcntl.flock(file, fcntl.LOCK_UN)
    return content


def is_binary_file(file_path: str) -> bool:
    """
    Determine if a file should be treated as binary based on its extension or path pattern.

    Args:
        file_path: The path to the file

    Returns:
        True if the file should be treated as binary, False otherwise
    """
    # Binary file extensions
    binary_extensions = {".so", ".dll", ".exe", ".bin", ".pyc", ".pyd"}

    # Check file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() in binary_extensions:
        return True

    # Check for pyarmor runtime files
    if "pyarmor_runtime" in file_path:
        return True

    return False
