# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for various helper functions."""
import json
import collections
from pathlib import Path
from subprocess import getoutput


def get_repo_root():
    """ Return absolute path to repository where script is executed, regardless
        of the current script's location.

        Returns:
            path (str): Absolute, canonical path to the top-level repository.
                        if not a git repository, returns current working dir

    """
    try:
        root = Path(getoutput('git rev-parse --show-toplevel')).resolve()
    except (FileNotFoundError, OSError):
        root = Path.cwd().resolve()
    return str(root)


def create_dir(path: Path):
    """If the directory for a given directory path does not exist, create it.
    Including parent directories.

    Args:
        path (Path): Path to directory.
    Returns:
        path (Path): Path to directory.
    """
    if not path.is_dir():
        path.mkdir(parents=True)
    return path


def merge_dicts(dict1, dict2, handle_collision=lambda a, b: a, merge_recursively=False):
    """Merge two dicts.

    Args:
        dict1 (dict): dict to merge
        dict2 (dict): dict to merge
        handle_collision (function(arg1, arg2)): function to resolve key collisions,
            default keeps original value in dict1
        merge_recursively (bool): if set to True it merges nested dicts recursively with handle_collision
            resolving collisions with non-dict types.
    Returns:
        dict: the result of the two merged dicts
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key not in result:
            result.update({key: value})
        elif isinstance(result[key], dict) and \
                isinstance(value, dict) and \
                merge_recursively:
            result[key] = merge_dicts(result[key], value, handle_collision, merge_recursively)
        else:
            result[key] = handle_collision(result[key], value)
    return result


def deep_dict_update(base, add):
    """Recursively update a dict that may contain sub-dicts.

    Args:
        base (dict): The base dict will be updated with the contents
                     of the add dict
        add (dict): This dict will be added to the base dict

    Returns:
        dict: the updated base dict is returned

    """
    for key, value in add.items():
        if key not in base:
            base[key] = value
        elif isinstance(value, dict):
            deep_dict_update(base[key], value)
    return base


def deep_json_update(json_file, dict_to_merge):
    """ Recursively update a json file with the content of a dict.

    Args:
        json_file (path): json file.
        dict_to_merge (dict): Dictionary that will be merged into json file, overwriting values and adding keys.
    """
    with open(json_file, 'r', encoding="utf-8") as fle:
        json_dict = json.load(fle)
    merged_dict = merge_dicts(
        json_dict,
        dict_to_merge,
        handle_collision=lambda a, b: b,
        merge_recursively=True
    )
    with open(json_file, 'w', encoding="utf-8") as fle:
        json.dump(merged_dict, fle, indent=2)


def recursive_default_dict():
    """Returns recursively defined default dict. This allows people to insert
       arbitrarily complex nested data into the dict without getting KeyErrors.

    Returns:
        defaultdict(self): A new defaultdict instance, recursively defined.
    """
    return collections.defaultdict(recursive_default_dict)


def to_normal_dict(weird_dict):
    """Converts nested dict to normal, suitable for YAML/JSON dumping.

    Args:
        weird_dict (dict): Any dict-like item that can be converted to a dict.
    Returns:
        dict(nested): An identical nested dict structure, but using real dicts.
    """
    for key, value in weird_dict.items():
        if isinstance(value, dict):
            weird_dict[key] = to_normal_dict(value)
    return dict(weird_dict)
