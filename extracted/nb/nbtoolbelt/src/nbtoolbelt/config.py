"""
Configuration file handling

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.

Configuration files use JSON to make it easier to move the Jupyter configuration file mechanism in the future.

There is a top-level entry for global options with the package name as key.
Each tool has a tool-specific entry with key 'nb' + tool name; e.g. 'nbrun'.

The top-level configuration is loaded first; typically it has options that apply to multiple tools.
Then the tool-specific configuration is loaded on top of that (using dict update).

TODO: First the embedded configuration file is loaded (these are defaults).

TODO: Then a configuration file in the home directory is loaded, if present.

Finally configuration files mentioned on the command line are loaded.
These are processed during argument parsing.
"""

import json
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, Union

from ._version import package_name
from .printing import print_namespace

TEST = False

CONFIG_FILE_NAME = package_name + '.json'


def config_path() -> Path:
    """Return path to embedded config file.

    :return: path to embedded config file
    """
    return Path(__file__).resolve().parent / 'data' / CONFIG_FILE_NAME


def load_config_file(tool: str = package_name,
                     ns: Namespace = None,
                     file_path: Union[str, Path] = config_path(),
                     verbose: bool = False) -> Namespace:
    """Load configuration for tool from file and return update namespace.
    Silently ignores file if it does not exist.

    .. note:: **Modifies**: ``ns``

    :param tool: tool for which to load a configuration file
    :param ns: namespace to load configuration into
    :param file_path: file path to load configuration from
    :param verbose: whether to print some diagnostic info
    :return: updated ns
    """
    if ns is None:
        ns = Namespace()  # create a fresh one
        # NOTE: in an earlier version, ns had default parameter value Namespace()
        # But that default is created once, and shared by all subsequent tools.
        # And that hurts during testing.

    if type(file_path) is str:
        file_path = Path(file_path)  # TODO can this raise an exception?

    if file_path.exists():
        try:
            with file_path.open(encoding='utf-8') as config_file:
                config_all = json.load(config_file)  # type: Dict[str, Dict[str, Any]]
        except Exception as e:
            print('Could not load configuration for {} in: {}'.format(tool, file_path), file=sys.stderr)
            print('{}: {}'.format(type(e).__name__, e), file=sys.stderr)
            sys.exit(1)  # TODO do this more graciously (but it may have been called from tool constructor)
        if verbose:
            print('Loading configuration for {} from: {}'.format(tool, file_path))
        if TEST:
            print('load_config_file(tool={}, fp={})'.format(tool, file_path))
            print('[load_config_file] config_all=\n{}'.format(json.dumps(config_all, indent=2)))
        if package_name in config_all:
            # copy the loaded configuration to the namespace
            for key, value in config_all[package_name].items():
                setattr(ns, key, value)  # overwrite or create the key-value pair
        if tool in config_all:
            # copy the loaded configuration to the namespace; unnecessary when tool == package_name
            for key, value in config_all[tool].items():
                setattr(ns, key, value)  # overwrite or create the key-value pair
        if TEST:
            print_namespace(ns, '[load_config_file] config for ' + tool)
    else:
        if verbose:
            print('Skipping configuration in: {} (not present)'.format(file_path))

    return ns


def load_config(tool: str = package_name, verbose: bool = False) -> Namespace:
    """Load configuration for tool.

    Successively load configuration files (if present) in:

    * the package itself (see src/nbtoolbelt/data/CONFIG_FILE_NAME)
    * /etc/CONFIG_FILE_NAME
    * ~/.CONFIG_FILE_NAME (a dot file in the home directory)

    .. note:: **Modifies**: ``ns``

    :param tool: tool for which to load a configuration file (default: top-level)
    :param verbose: whether to print some diagnostic info
    :return: updated ns
    """
    ns = load_config_file(tool, verbose=verbose)

    fp_etc = Path('/etc') / CONFIG_FILE_NAME
    load_config_file(tool, ns, fp_etc, verbose)

    fp_home = Path.home() / ('.' + CONFIG_FILE_NAME)
    load_config_file(tool, ns, fp_home, verbose)

    if verbose:
        print_namespace(ns, 'Configuration accumulated for ' + tool)

    return ns
