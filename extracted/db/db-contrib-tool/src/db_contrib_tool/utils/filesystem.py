"""Filesystem-related helper functions."""

import os
import tempfile
from typing import Any, Dict, Optional

import yaml


def mkdtemp_in_build_dir() -> str:
    """
    Use build/ as the temp directory since it's mapped to an EBS volume on Evergreen hosts.

    :return: Temporary directory path.
    """
    build_tmp_dir = os.path.join("build", "tmp")
    os.makedirs(build_tmp_dir, exist_ok=True)

    return tempfile.mkdtemp(dir=build_tmp_dir)


def build_bin_path(parent: str) -> Optional[str]:
    """
    Find the first bin directory recursively in the parent directory.

    :param parent: Path to parent directory.
    :return: Bin directory path.
    """
    for path, dirs, _ in os.walk(parent):
        if "bin" in dirs:
            return os.path.join(path, "bin")
    return None


def read_yaml_file(path: str) -> Dict[str, Any]:
    """
    Read the yaml file at the given path and return the contents.

    :param path: Path to file to read.
    :return: Contents of given file.
    """
    with open(path) as file_handle:
        return yaml.safe_load(file_handle)
