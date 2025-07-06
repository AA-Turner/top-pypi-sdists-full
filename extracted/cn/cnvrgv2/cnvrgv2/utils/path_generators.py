import os
import re
import fnmatch

from cnvrgv2.errors import CnvrgError
from cnvrgv2.utils.validators import validate_directory_name
from cnvrgv2.utils.storage_utils import (
    match_mimetypes,
    path_is_wildcard,
    get_relative_path,
    append_trailing_slash,
    get_files_and_dirs_recursive,
)


def metadata_generator(paths, mime_filters=None, ignore_spec=None, temp_folder=None):
    """
    Duplicates the generator in order to calculate the resulting files metadata like total files and sizes.
    @param paths: [List] List of strings representing paths and wildcards
    @param mime_filters: [List] Array of accepted mime types
    @param ignore_spec: [PathSpec] object, or use build_cnvrgignore_spec
    @param temp_folder: [String] The location of the temporary folder
    @return: [Dict, Generator] The filtered files metadata + the file generator
    """
    counter = multi_path_filter_generator(paths, mime_filters=mime_filters, ignore_spec=ignore_spec)
    generator = multi_path_filter_generator(paths, mime_filters=mime_filters, ignore_spec=ignore_spec)

    if temp_folder is not None and os.path.exists(temp_folder):
        counter = filter_deleted_paths_generator(counter, temp_folder)
        generator = filter_deleted_paths_generator(generator, temp_folder)

    # Count files and their size
    total_size = 0
    total_files = 0
    for path in counter:
        total_files += 1
        if os.path.isfile(path):
            total_size += os.path.getsize(path)

    return {"total_size": total_size, "total_files": total_files}, generator


def filter_deleted_paths_generator(path_generator, temp_folder):
    """
    Receives a path generator and adds a filter on top of it to filter out deleted files.
    @param path_generator: [Generator]
    @param temp_folder: [String] The location of the temporary folder
    @return: [Generator] Returns filtered paths
    """
    # This function should run only if tmp folder exist (sync/download)
    if not os.path.exists(temp_folder):
        raise CnvrgError("Trying to filter paths using a non-existent temp folder")

    # We need to filter out all paths that are under deleted folders
    deleted_folders = get_files_and_dirs_recursive(root_dir=temp_folder, regex=".*deleted/", force=True)

    for path in path_generator:
        deleted_file = "{}/{}.deleted".format(temp_folder, path)

        # Check that the file is not in a deleted folder
        in_deleted_folder = False
        for deleted_folder in deleted_folders:
            matching_path = deleted_folder.replace(".tmp/", "").replace(".deleted", "")
            regex = re.compile("^{}.*".format(matching_path))
            if regex.match(path):
                in_deleted_folder = True

        if os.path.exists(deleted_file) or in_deleted_folder:
            continue

        yield path


def multi_path_filter_generator(paths, mime_filters=None, ignore_spec=None):
    """
    Generates and filters file/folder paths from the given path list
    @param paths: [List] list of string of folder/file/regex
    @param mime_filters: [List] Array of accepted mime types
    @param ignore_spec: [PathSpec] object, or use build_cnvrgignore_spec
    @return: [Generator] Returns filtered paths
    """
    filters = [path for path in paths if path_is_wildcard(path)]
    for path in multi_path_generator(paths=paths):
        # If we want to ignore specific files (for example via .cnvrgignore)
        if ignore_spec and ignore_spec.match_file(path):
            continue

        # Filter out paths using the regex filters
        matches_filter = False if len(filters) > 0 else True
        for regex in filters:
            if fnmatch.fnmatch(path, regex):
                matches_filter = True
        if not matches_filter:
            continue

        # Filter files by mimetype
        if not match_mimetypes(filters=mime_filters, path=path):
            continue

        # Filter special paths
        if path in ["./", ".", "/", "//"]:
            continue

        yield path


def multi_path_generator(paths):
    """
    Generator that yields all file/folder paths from provided path list.
    @param paths: [List] list of string of folder/file/regex
    @return: [Generator] Returns all paths
    """

    # For pattern matching we will yield ALL files from the current working directory
    # Filtering for said files should be performed OUTSIDE of the generator
    folder_patterns_traversed = []

    for target_path in paths:
        is_dir = os.path.isdir(target_path)
        is_file = os.path.isfile(target_path)

        if is_dir:
            validate_directory_name(target_path)
            # For directories we will use os.walk generator to yield files
            yield from folder_path_generator(root_dir=target_path)
        elif is_file:
            # For files we will yield them right away
            yield target_path
        elif path_is_wildcard(target_path):
            # Calculate which folder we should traverse as part of the regex
            if "/" in target_path or ".." in target_path:
                if "*" in target_path:
                    regex_path = target_path.split("*")[0]
                elif "?" in target_path:
                    regex_path = target_path.split("?")[0]
            else:
                regex_path = "."

            # We will traverse only once per folder and leave the filtering to the caller function
            if regex_path in folder_patterns_traversed:
                continue

            folder_patterns_traversed.append(regex_path)
            yield from folder_path_generator(root_dir=regex_path)


def folder_path_generator(root_dir="."):
    """
    Recursively traverse a given directory and get all of the relevant files and folders within
    @param root_dir: [String] The target directory to traverse
    @return: [Generator] returns all files and directories inside a given path
    """

    for root, dirs, files in os.walk(root_dir, topdown=False, followlinks=True):
        for name in files:
            file_path = get_relative_path(os.path.join(root, name))
            yield file_path
        for name in dirs:
            dir_path = get_relative_path(os.path.join(root, name))
            dir_path = append_trailing_slash(dir_path)
            yield dir_path

    # Add the folder itself, if it's an empty one
    if len(os.listdir(root_dir)) == 0:
        dir_path = append_trailing_slash(get_relative_path(root_dir))
        yield dir_path
