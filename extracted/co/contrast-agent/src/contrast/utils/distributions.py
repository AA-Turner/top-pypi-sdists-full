# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import collections
import functools
import hashlib
import itertools
import os
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from contrast_vendor import importlib_metadata
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from types import ModuleType

logger = logging.getLogger("contrast")

# General note:
# Talking about a "package" in python is a delicate matter. This module is generally
# referring to "distribution packages", ie the things you install from pypi. See:
# https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/


@dataclass(frozen=True)
class LightDistribution:
    """
    A wrapper around importlib-metadata's Distribution that's less useful but faster.
    Requires minimal metadata parsing to be initialized.

    It's easy to accidentally perform slow operations with a Distribution object,
    because it has many properties that perform a surprising amount of work involving
    reading and parsing files from the disk. Controlling access to this object makes it
    less likely for us to accidentally write slow code.
    """

    _dist: importlib_metadata.Distribution
    name: str
    version: str

    @functools.cached_property
    def files(self):
        return self._dist.files


@functools.lru_cache
def distribution_from_dist_name(name: str) -> LightDistribution | None:
    """
    Look up a distribution by its name and return a LightDistribution. This requires a
    distribution name, not an import name!
    """
    try:
        heavy_dist = importlib_metadata.distribution(name)
    except importlib_metadata.PackageNotFoundError:
        return None

    return _read_core_metadata(heavy_dist)


@functools.cache
def all_distributions() -> list[LightDistribution]:
    """
    Get all available distributions in the current environment as LightDistributions.

    Deduplicates by package name to avoid reporting inaccessible packages. This does a
    lot of work when first called, particularly in python environments containing many
    distribution packages.
    """
    seen_names = set()
    distributions = []
    for dist in importlib_metadata.distributions():
        light_dist = _read_core_metadata(dist)
        if (
            light_dist
            and (norm_name := normalize_dist_name(light_dist.name)) not in seen_names
        ):
            seen_names.add(norm_name)
            distributions.append(light_dist)

    return distributions


def _read_core_metadata(
    dist: importlib_metadata.Distribution,
) -> LightDistribution | None:
    """
    Read the agent's wanted metadata fields from a distribution.

    Uses a fast targeted parser for the common case (a METADATA/PKG-INFO file with a
    standard header block), falling back to importlib_metadata's full email-based parser
    for any distribution whose layout the fast path can't handle. Returns `None` if no
    usable metadata is available.
    """
    text = dist.read_text("METADATA") or dist.read_text("PKG-INFO")
    if text is not None:
        fields = _parse_core_metadata(text)
        if "name" in fields and "version" in fields:
            # This is the happy path. Everything else here is just extensive error
            # handling so we can hopefully figure out why we're not on the happy path.
            return LightDistribution(
                dist,
                name=fields["name"],
                version=fields["version"],
            )
        else:
            logger.debug(
                "WARNING: failed to fast-parse distribution metadata."
                " Falling back to the default parser."
            )
    else:
        logger.debug(
            "WARNING: failed to find metadata file for a distribution."
            " Falling back to the default parser."
        )

    try:
        metadata = dist.metadata
    except importlib_metadata.MetadataNotFound:
        logger.debug(
            "WARNING: failed to find dist metadata even with the default parser"
        )
        return None

    if (name := metadata.get("Name")) is None:
        logger.debug(
            "WARNING: failed to find name for dist requiring fall-back parsing"
        )
        return None

    if (version := metadata.get("Version")) is None:
        logger.debug(
            "WARNING: failed to find version for dist requiring fall-back parsing",
            dist_name=name,
        )
        return None

    logger.debug(
        "WARNING: found dist with fall-back parser that failed fast-parsing",
        dist_name=name,
        dist_version=version,
    )

    return LightDistribution(
        dist,
        name=name,
        version=version,
    )


_WANTED_METADATA_FIELDS = frozenset({"name", "version"})


def _parse_core_metadata(text: str) -> dict[str, str]:
    """
    Extract the agent's wanted fields from raw core metadata text.

    This is a deliberately narrow RFC 5322-style parser: it scans only the leading
    header block (up to the first blank line, which separates headers from the
    description body) and pulls out the agent's required headers.

    Returns a dict that contains field names -> field values for desired fields only.
    If any wanted fields are missing, they won't be present in the return value.
    """
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if not line:
            # A blank line terminates the header block.
            break
        if line[0] in " \t":
            # Folded continuation line. Ignored as a heuristic to improve performance.
            # If we discover that the agent requires header values that are sometimes
            # folded across multiple lines, we'll need to account for this complexity.
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key = key.strip().lower()
        if key in _WANTED_METADATA_FIELDS:
            fields[key] = value.strip()
        if len(fields) == len(_WANTED_METADATA_FIELDS):
            # found everything, can exit early
            break

    return fields


@functools.lru_cache
def distribution_from_module(module: ModuleType) -> LightDistribution | None:
    """
    Get the LightDistribution that the provided module is a member of.

    Note that if caches are not yet warm, this does a fair amount of work.
    """
    top_level_name = module.__name__.partition(".")[0]

    possible_dists = _distributions_by_top_level_import().get(top_level_name, set())
    if len(possible_dists) == 1:
        # If there's only one available dist corresponding to this module's top-level
        # import name, return that.
        return next(iter(possible_dists))

    if (
        (mod_file := getattr(module, "__file__", None))
        and (file_name := normalize_file_name(mod_file))
        and (dist := _namespace_distributions_by_filename().get(file_name))
    ):
        # Otherwise, if there's ambiguity in the top-level import name, use the filename
        # to determine this module's particular distribution package.
        return dist

    return None


@functools.cache
def _distributions_by_top_level_import() -> dict[str, set[LightDistribution]]:
    """
    Return a mapping of top-level import package names to their LightDistribution.
    Approximately a reimplementation of `importlib_metadata.packages_distributions` with
    LightDistribution.

    Most commonly, each top-level import corresponds to a single distribution package.
    For example, the top-level import `django` corresponds to the `django` distribution
    package. Top-level imports do not necessarily share a name with their dist package;
    an example of this is `import yaml` -> `pyyaml`.

    Consider the following example: you installed `google-cloud-aiplatform` in the
    current python environment. This distribution package depends on several other
    google-* distribution packages, all of which are available in python under the
    top-level `google` import package name.

    This results in something like the following entry in this function's return value:
    {
        ...
        'google': {
            <LightDistribution google-cloud-resource-manager>,
            <LightDistribution google-cloud-aiplatform>,
            <LightDistribution google-cloud-core>,
            ...
        },
        ...
    }
    """
    pkg_to_dist = collections.defaultdict(set)
    for dist in all_distributions():
        for pkg in importlib_metadata._top_level_declared(
            dist._dist,
        ) or importlib_metadata._top_level_inferred(
            dist._dist,
        ):
            pkg_to_dist[pkg].add(dist)
    return dict(pkg_to_dist)


@functools.cache
def _namespace_distributions_by_filename() -> dict[str, LightDistribution]:
    """
    Construct a map from normalized filename -> LightDistribution for distributions
    whose top-level import names are ambiguous (e.g. `google`).
    """
    namespacepkg_dists = [
        dists
        for dists in _distributions_by_top_level_import().values()
        if len(dists) > 1
    ]
    files_to_dist = {
        str(f): dist
        for dist in itertools.chain.from_iterable(namespacepkg_dists)
        for f in dist.files or []
    }
    return files_to_dist


SITE_PACKAGES_DIR = f"{os.sep}site-packages{os.sep}"
DIST_PACKAGES_DIR = f"{os.sep}dist-packages{os.sep}"


def normalize_file_name(file_path: str) -> str | None:
    """Normalize a module file path to a stable path relative to site-packages.

    Removes the leading site-packages or dist-packages portion and removes the .pyc
    suffix if present, returning the resulting .py file path.

    Returns None if the path does not appear to be within site-packages/dist-packages.
    """
    file_path = _normalize_separators(file_path)

    _, match, normalized_file_name = file_path.rpartition(SITE_PACKAGES_DIR)
    if not match:
        _, match, normalized_file_name = file_path.rpartition(DIST_PACKAGES_DIR)
        if not match:
            return None

    if normalized_file_name.endswith(".pyc"):
        normalized_file_name = normalized_file_name.removesuffix("c")

    # Normalize to forward slashes for stable reporting across platforms.
    return normalized_file_name.replace(os.sep, "/")


def _normalize_separators(path: str) -> str:
    """Normalize to the current platform separator.

    On Windows, paths can contain either '\\' or '/' depending on the source.
    This helps make matching logic consistent.
    """
    if os.altsep:
        path = path.replace(os.altsep, os.sep)
    return path


def normalize_dist_name(name: str) -> str:
    # Normalize the name based on the spec:
    # https://packaging.python.org/en/latest/specifications/name-normalization/
    return re.sub(r"[-_.]+", "-", name).lower()


def get_hash(name: str, version: str) -> str:
    """
    DO NOT ALTER OR REMOVE

    This must match the calculation made by the artifact dependency management database.
    """
    name = normalize_dist_name(name)

    to_hash = name + " " + version

    return hashlib.sha1(to_hash.encode("utf-8")).hexdigest()
