"""
spotilyzer path utilities
"""

# system imports
import os
import pathlib

# exported constants
SEEDS_FILE = 'seeds.json'

# constants
_DATA_DIR = 'data'
_USER_DIR = '.spotilyzer'


def get_package_datadir():
    """
    Get the package data directory.
    :return: path to package data directory
    """
    return os.path.normpath(os.path.join(os.path.dirname(__file__),
                                         os.path.pardir, os.path.pardir,
                                         _DATA_DIR))


def get_user_datadir():
    """
    Get the user's data directory.
    :return: path to user's data directory
    """
    return os.path.join(pathlib.Path.home(), _USER_DIR)


def find_seeds_file():
    """
    Determine location of seeds.json using spotilyzer precedence. Raise
    exception if not found.
    :return: path to seeds.json
    """
    seeds_file = os.path.join(get_user_datadir(), SEEDS_FILE)
    if os.path.exists(seeds_file):
        return seeds_file
    seeds_file = os.path.join(get_package_datadir(), SEEDS_FILE)
    if os.path.exists(seeds_file):
        return seeds_file
    raise FileNotFoundError("seeds file not found")
