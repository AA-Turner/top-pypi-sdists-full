"""
read_write_utils.py

This module, 'read_write_utils.py', provides utility functions for reading and writing to files.
These include functions to:

Usage:
    import abstract_utilities.read_write_utils as read_write_utils

1. Write content to a file.
2. Read content from a file.
3. Check if a string has a file extension.
4. Read from or write to a file depending on the number of arguments.
5. Create a file if it does not exist, then read from it.

Each function includes a docstring to further explain its purpose, input parameters, and return values.
import os

# File and Directory Operations
os.rename(src, dst)            # Rename a file or directory
os.remove(path)               # Remove a file
os.unlink(path)               # Alias for os.remove()
os.rmdir(path)                # Remove an empty directory
os.makedirs(path)             # Create directories recursively
os.makedirs(path, exist_ok=True)  # Create directories, ignore if exists
os.mkdir(path)                # Create a single directory
os.listdir(path)              # List files and directories in a path
os.chdir(path)                # Change current working directory
os.getcwd()                   # Get current working directory
os.stat(path)                 # Get file/directory information
os.lstat(path)                # Get symbolic link information
os.symlink(src, dst)          # Create a symbolic link
os.readlink(path)             # Read the target of a symbolic link
os.getcwd()                   # Get current working directory
os.chdir(path)                # Change current working directory

# File and Directory Information
os.path.exists(path)          # Check if a path exists
os.path.isfile(path)          # Check if a path points to a file
os.path.isdir(path)           # Check if a path points to a directory
os.path.islink(path)          # Check if a path points to a symbolic link
os.path.abspath(path)         # Get the absolute path of a file/directory
os.path.basename(path)        # Get the base name of a path
os.path.dirname(path)         # Get the directory name of a path
os.path.join(path1, path2, ...)  # Join path components into a single path

# File Permissions
os.chmod(path, mode)          # Change file permissions
os.access(path, mode)         # Check if a file is accessible with given mode

# File Times
os.path.getatime(path)        # Get last access time of a file
os.path.getmtime(path)        # Get last modification time of a file
os.path.getctime(path)        # Get creation time of a file
os.utime(path, times)         # Set access and modification times

# Working with Paths
os.path.split(path)           # Split a path into (head, tail)
os.path.splitext(path)        # Split a path into (root, ext)
os.path.normpath(path)        # Normalize a path (e.g., convert slashes)

# Other
os.path.samefile(path1, path2)  # Check if two paths refer to the same file

# Directory Traversal
for root, dirs, files in os.walk(top, topdown=True):
    # Traverse a directory tree, yielding root, dirs, and files lists

# Temporary Files and Directories
import tempfile
tempfile.mkstemp()            # Create a temporary file
tempfile.mkdtemp()            # Create a temporary directory
tempfile.TemporaryFile()      # Create a temporary file object

# Environment Variables
os.environ                    # Dictionary of environment variables
os.environ['VAR_NAME']        # Access an environment variable
os.environ.get('VAR_NAME')    # Access an environment variable (with default)

# Path Manipulation
os.path.abspath(path)         # Convert relative path to absolute path
os.path.join(path1, path2, ...)  # Join paths together
os.path.split(path)           # Split a path into directory and filename
os.path.dirname(path)         # Get the directory part of a path
os.path.basename(path)        # Get the filename part of a path
os.path.exists(path)          # Check if a path exists
os.path.isfile(path)          # Check if a path points to a file
os.path.isdir(path)           # Check if a path points to a directory

# File Permissions
os.chmod(path, mode)          # Change file permissions

# Miscellaneous
os.getpid()                   # Get the current process ID
os.getlogin()                 # Get the name of the logged-in user

"""
import os
def break_down_find_existing(path):
    test_path = ''
    for part in path.split(os.sep):
        test_path = os.path.join(test_path, part)
        if not os.path.exists(test_path):
            return test_path if test_path else None
    return test_path

def string_in_keys(strings, kwargs):
    return next((key for key in kwargs if any(s.lower() in key.lower() for s in strings)), None)

def get_path(paths):
    for path in paths:
        if isinstance(path,str):
            if os.path.isfile(path):
                return path
            dirname = os.path.dirname(path)
            if os.path.exists(dirname):
                return path
    return None

def check_read_write_params(*args, **kwargs):
    file_path = kwargs.get('file_path', None)
    contents = kwargs.get('contents', None)
    if contents is None:
        contents = kwargs.get('data', None)

    # Handle positional arguments
    if file_path is None and len(args) > 0:
        file_path = args[0]
    if contents is None and len(args) > 1:
        contents = args[1]
    elif contents is None and len(args) > 0 and file_path != args[0]:
        contents = args[0]

    if file_path is None or contents is None:
        raise ValueError("Both 'file_path' and 'contents' (or 'data') are required.")

    return file_path, contents

def write_to_file(file_path=None, contents=None,*args,  **kwargs):
    """
    Write contents to a file. If the file does not exist, it is created.

    Args:
        file_path: The path of the file to write to.
        contents: The content to write to the file.
        
    Returns:
        The contents that were written to the file.
    """
    params = check_read_write_params(file_path=file_path, contents=contents,*args,  **kwargs)
    if params:
        with open(params[0], 'w', encoding='UTF-8') as f:
            f.write(params[1])
        return contents


def read_from_file(file_path) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: The path of the file to read from.
        
    Returns:
        The contents of the file.
    """
    with open(file_path, 'r', encoding='UTF-8') as f:
        return f.read()

def create_and_read_file(file_path=None, contents:str='',*args,  **kwargs) -> str:
    """
    Create a file if it does not exist, then read from it.
    
    Args:
        file_path: The path of the file to create and read from.
        contents: The content to write to the file if it does not exist.
        
    Returns:
        The contents of the file.
    """
    if not os.path.isfile(file_path):
        write_to_file(contents, file_path)
    return read_from_file(file_path)
def is_file_extension(obj: str) -> bool:
    """
    Check if a string has a file extension.
    
    Args:
        obj: The string to check.
        
    Returns:
        True if the string has a file extension, False otherwise.
    """
    return len(obj) >= 4 and '.' in obj[-4:-3]

def delete_file(file_path: str):
    if os.path.isfile(file_path):
        os.remove(file_path)

