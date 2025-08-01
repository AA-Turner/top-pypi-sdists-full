# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import collections
import functools
import hashlib
import itertools
import os
import re
from types import ModuleType

from contrast_vendor.importlib_metadata import (
    Distribution,
    distributions as importlib_distributions,
    _top_level_declared,
    _top_level_inferred,
)
from contrast_vendor.importlib_metadata._meta import PackageMetadata


@functools.cache
def distributions() -> list[Distribution]:
    """
    Get all Distribution instances for the current environment.
    """
    return list(importlib_distributions())


@functools.cache
def packages_distributions() -> dict[str, list[Distribution]]:
    """
    Return a mapping of top-level packages to their distributions.
    """
    pkg_to_dist = collections.defaultdict(list)
    for dist in distributions():
        for pkg in _top_level_declared(dist) or _top_level_inferred(dist):
            if dist not in pkg_to_dist[pkg]:
                pkg_to_dist[pkg].append(dist)
    return dict(pkg_to_dist)


@functools.cache
def namespace_file_to_distribution() -> dict[str, Distribution]:
    namespacepkg_dists = [
        dists for pkg, dists in packages_distributions().items() if len(dists) > 1
    ]
    files_to_dist = {
        str(f): dist
        for dist in itertools.chain.from_iterable(namespacepkg_dists)
        for f in dist.files or []
    }
    return files_to_dist


def get_module_distribution_metadata(module: ModuleType) -> PackageMetadata | None:
    top_level_name = module.__name__.partition(".")[0]
    if dist_meta := _get_simple_regular_package_distribution_metadata(top_level_name):
        return dist_meta
    elif (
        (mod_file := getattr(module, "__file__", None))
        and (file_name := normalize_file_name(mod_file))
        and (dist := namespace_file_to_distribution().get(file_name))
    ):
        return dist.metadata
    return None


@functools.lru_cache
def _get_simple_regular_package_distribution_metadata(
    package_name: str,
) -> PackageMetadata | None:
    """
    Get the distribution metadata for a package that has only one distribution.

    This handles the common case of a regular package (https://docs.python.org/3/glossary.html#term-regular-package).

    This function is separated from get_module_distribution_metadata to allow for caching.
    For packages with many modules, this caching makes a measurable difference in performance
    because Distribution.metadata is a relatively expensive operation, reading from the filesystem
    and parsing files with the standard library's email.parser module.
    """
    dists = packages_distributions().get(package_name)
    if not dists:
        return None
    if len(dists) == 1:
        return dists[0].metadata
    return None


@functools.cache
def get_installed_dist_names():
    return [dist.name for dist in distributions()]


SITE_PACKAGES_DIR = f"{os.sep}site-packages{os.sep}"
DIST_PACKAGES_DIR = f"{os.sep}dist-packages{os.sep}"


def normalize_file_name(file_path: str) -> str | None:
    """
    This function normalizes the file path by removing the leading site-packages or dist-packages portion
    and removing the .pyc suffix if present, returning the resulting .py file path.
    @param file_path: the full path to a Python .pyc or .py file
    @return: the normalized file path ending in .py, or None if prefix not found
    """
    _, match, normalized_file_name = file_path.rpartition(SITE_PACKAGES_DIR)
    if not match:
        _, match, normalized_file_name = file_path.rpartition(DIST_PACKAGES_DIR)
        if not match:
            return None

    if normalized_file_name.endswith(".pyc"):
        normalized_file_name = normalized_file_name.removesuffix("c")
    return normalized_file_name


def normalize_dist_name(name):
    # Normalize the name based on the spec https://packaging.python.org/en/latest/specifications/name-normalization/
    return re.sub(r"[-_.]+", "-", name).lower()


def get_hash(name, version):
    """
    DO NOT ALTER OR REMOVE

    This must match the calculation made by the artifact dependency management database.
    """
    name = normalize_dist_name(name)

    to_hash = name + " " + version

    return hashlib.sha1(to_hash.encode("utf-8")).hexdigest()
