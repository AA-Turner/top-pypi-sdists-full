# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
import pkgutil
import sys
from collections.abc import Generator, Iterable
from zlib import crc32

from contrast.utils.libraries import distributions, normalize_dist_name, Distribution
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


def artifact_fingerprint() -> str:
    """
    Compute a fingerprint of the running code artifact.

    This fingerprint is smudgy. It prefers to be fast and simple over being
    completely accurate.

    It may return an empty string if it fails to compute a meaningful fingerprint.

    The returned fingerprint is based on the installed distribution packages,
    their versions, and the names and sized of the application source files.
    """
    app_root = sys.path[0] or "."
    app_ids = app_source_ids(app_root)
    if not app_ids:
        logger.debug("failed to compute fingerprint, no app sources found")
        return ""
    deps_ids = distribution_ids(distributions())
    artifact_id = f"app_sources={app_ids};deps={deps_ids}"
    logger.debug(
        "computed fingerprint",
        artifact_id=artifact_id,
        app_sources_count=len(app_ids),
        installed_distributions_count=len(deps_ids),
    )
    return str(crc32(artifact_id.encode()))


def distribution_ids(dists: Iterable[Distribution]) -> list[str]:
    return sorted(
        [
            f"{normalize_dist_name(dist_meta['Name'])}=={dist_meta['Version']}"
            for dist_meta in (dist.metadata for dist in dists)
        ]
    )


def app_source_ids(app_root: str) -> list[str]:
    return [
        module_id(info, origin)
        for info, origin in sorted(
            scan_app_modules([app_root], prefix="."), key=lambda x: x[0].name
        )
    ]


def module_id(info: pkgutil.ModuleInfo, origin: str):
    file_size = os.stat(origin).st_size
    return f"{info.name}:{file_size}"


def scan_app_modules(
    search_locations: list[str] | None, prefix=""
) -> Generator[tuple[pkgutil.ModuleInfo, str], None, None]:
    if not search_locations:
        return
    for mod_info in pkgutil.iter_modules(search_locations, prefix):
        spec = mod_info.module_finder.find_spec(mod_info.name)
        if not spec or not spec.origin:
            continue
        yield mod_info, spec.origin
        yield from scan_app_modules(
            spec.submodule_search_locations, prefix=f"{mod_info.name}."
        )
