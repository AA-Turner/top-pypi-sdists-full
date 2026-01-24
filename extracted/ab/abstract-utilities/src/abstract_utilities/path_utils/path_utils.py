"""
path_utils.py

This module provides a collection of utility functions related to file and directory path management. 
Its features include, but are not limited to:

Usage:
    import abstract_utilities.path_utils as path_utils

- Determining appropriate file path separators based on the operating system.
- Joining paths using the correct file path separator.
- Fetching the current working directory and user's home folder.
- Checking if a path corresponds to a file or directory and if they exist.
- Fetching file sizes and determining the size of directories.
- Creating multiple nested directories if they do not exist.
- Retrieving creation time of files.
- Converting sizes to GB with options for truncation.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
from functools import lru_cache
from pathlib import Path
from .imports import *


def get_files(directory):
    file_list = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root,file))
    return file_list

def get_folders(directory):
    directory_list = []
    for root,dirs,files in os.walk(directory):
        for folder in dirs:
            directory_list.append(os.path.join(root,folder))
    return directory_list

def break_down_find_existing(path):
    slash = get_slash()
    test_path=''
    found_path=None
    for part in path.split(slash):
        test_path=os.path.join(test_path,part)
        if not os.path.exists(test_path):
            return found_path
        found_path = test_path
    return found_path

def get_directory_items(directory):
    if not os.path.isdir(directory):
        return []
    return os.listdir(directory)

def get_directory_files(directory):
    if not os.path.isdir(directory):
        return []
    return get_files(directory)

def get_all_item_paths(directory):
    directory_items = get_directory_items(directory)
    item_paths = [os.path.join(directory,item) for item in directory_items if item]
    return item_paths

def get_all_file_paths(directory):
    item_paths = get_directory_files(directory) 
    return item_paths

def get_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory,exist_ok=True)
    return directory

def create_directory(directory,path):
    directory = os.path.join(directory,path)
    return get_directory(directory)


def initialize_file(directory,basename):
    directory = get_directory(directory)
    file_path = create_directory(directory,basename)
    return get_file_path(file_path)

def join_path(directory,basename):
    file_path = os.path.join(directory,basename)
    return file_path

def is_last_itter(i,*itters):
    itter_len = len(itters)
    if i+1 == itter_len:
        return True
    return False

def path_join(*paths, isfile=False):
    final_path = os.path.join(*paths)
    paths_len = len(paths)
    for i, path in enumerate(paths):
        if i == 0:
            final_path = path  # Note: Fixed bug; original code had `final_path = paths`
        else:
            final_path = os.path.join(final_path, path)
        if isfile and is_last_itter(i, paths_len):  # Note: `is_last_itter` is undefined; assuming it checks if last iteration
            break
        os.makedirs(final_path, exist_ok=True)      
    return final_path


def get_all_directories(directory):
    dir_list = os.listdir(directory)
    directory_list = [item for item in dir_list if is_dir(directory,item)]
    return directory_list

def get_all_files(directory=None):
    directory = directory or os.getcwd()
    dir_list = os.listdir(directory)
    file_list = [item for item in dir_list if is_file(directory,item)]
    return file_list

def get_all_items(directory):
    dir_list = os.listdir(directory)
    file_list = [item for item in dir_list if is_exists(directory,item)]
    return file_list


def get_dirlist(directory):
    path = get_directory(directory)
    if not path:
        return path
    dir_list=[]
    if is_dir(path):
        dir_list = os.listdir(path)
    elif is_file(path):
        dir_list = [os.path.basename(path)]
    return dir_list


def is_directory_in_paths(path,directory):
    return directory in path 

def remove_directory(directory,paths=None):
    paths = make_list_it(paths)
    shutil.rmtree(audio_dir)
    for path in paths:
        remove_path(path=path)
def remove_path(path=None):
    if path and os.path.exists(path):
        if os.path.isdir(path):
            remove_directory(path)
        else:
            os.remove(path)
def get_safe_dirname(path=None):
    if path:
        path_str = str(path)
        return os.path.dirname(path_str)
def get_safe_basename(path=None):
    if path:
        path_str = str(path)
        return os.path.basename(path_str)
def get_safe_splitext(path=None,basename=None):
    basename = basename or get_safe_basename(path=path)
    if basename:
        basename_str = str(basename)
        filename,ext = os.path.splitext(basename_str)
        return filename,ext
    return None,None
def get_safe_filename(path=None,basename=None):
    filename,_ = get_safe_splitext(path=path,basename=basename)
    return filename
def get_safe_ext(path=None,basename=None):
    _,ext = get_safe_splitext(path=path,basename=basename)
    return ext
def raw_create_dirs(*paths):
    """Recursively create all directories along the given path."""
    full_path = os.path.abspath(safe_join(*paths))
    sub_parts = [p for p in full_path.split(os.sep) if p]

    current_path = "/" if full_path.startswith(os.sep) else ""
    for part in sub_parts:
        current_path = safe_join(current_path, part)
        os.makedirs(current_path, exist_ok=True)
    return full_path


def create_dirs(directory, child=None):
    """Create directory and optional child path safely."""
    full_path = os.path.abspath(safe_join(directory, child))
    if not os.path.exists(full_path):
        raw_create_dirs(full_path)
    return full_path


def get_base_dir(directory=None):
    """Return given directory or _BASE_DIR fallback."""
    return directory or _BASE_DIR


def create_base_path(directory=None, child=None):
    """Join base dir with child."""
    directory = get_base_dir(directory)
    return safe_join(directory, child)


def create_base_dir(directory=None, child=None):
    """Ensure existence of base directory path."""
    full_path = create_base_path(directory, child)
    if not os.path.exists(full_path):
        raw_create_dirs(full_path)
    return full_path




def get_abs_path(path: str, i=None) -> str:
    abs_dir = get_initial_caller_dir()

    if not abs_dir:
        raise RuntimeError(
            "get_abs_path(): could not determine caller directory. "
            "This usually means the code is running from a virtual, "
            "GVFS, or dynamically loaded context."
        )

    return os.path.join(abs_dir, path)


    return root / name


def get_file_parts(path):
    if path:
        path= str(path) 
        basename = get_safe_basename(path)
        filename, ext = get_safe_splitext(basename=basename)

        dirname = get_safe_dirname(path)
        dirbase = get_safe_basename(dirname)
        
        parent_dirname = get_safe_dirname(dirname)
        parent_dirbase = get_safe_basename(parent_dirname)
        
        super_dirname = get_safe_dirname(parent_dirname)
        super_dirbase = get_safe_basename(super_dirname)

        return {"file_path":path,
                "dirname": dirname,
                "basename": basename,
                "filename": filename,
                "ext": ext,
                "dirbase":dirbase,
                "parent_dirname":parent_dirname,
                "parent_dirbase":parent_dirbase,
                "super_dirname":super_dirname,
                "super_dirbase":super_dirbase
                }

