import os,glob
from typing import *
from abstract_utilities import read_from_file,make_list
def glob_search(path, pattern, ext=None):
    """Search for files matching pattern in path."""
    import glob
    files = glob.glob(os.path.join(path, pattern))
    if ext:
        return [f for f in files if f.endswith(ext)]
    return files
