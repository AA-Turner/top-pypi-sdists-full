# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import os
import pkgutil
import sys
from typing import TYPE_CHECKING
from zlib import crc32

from contrast.utils.decorators import fail_loudly
from contrast.utils.distributions import (
    LightDistribution,
    all_distributions,
    normalize_dist_name,
)
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

logger = logging.getLogger("contrast")


@fail_loudly("Failed to compute application fingerprint", return_value="")
def artifact_fingerprint() -> str:
    """
    Compute a fingerprint of the running code artifact.

    This fingerprint is smudgy. It prefers to be fast and simple over being
    completely accurate.

    It may return an empty string if it fails to compute a meaningful fingerprint.

    The returned fingerprint is based on the installed distribution packages,
    their versions, and the names and sized of the application source files.
    """
    app_root = sys.path[0] if os.path.isdir(sys.path[0]) else "."
    app_ids = app_source_ids(app_root)
    if not app_ids:
        logger.debug("failed to compute fingerprint, no app sources found")
        return ""
    deps_ids = distribution_ids(all_distributions())
    artifact_id = f"app_sources={app_ids};deps={deps_ids}"
    logger.debug(
        "computed fingerprint",
        artifact_id=artifact_id,
        app_sources_count=len(app_ids),
        installed_distributions_count=len(deps_ids),
    )
    return str(crc32(artifact_id.encode()))


def distribution_ids(dists: Iterable[LightDistribution]) -> list[str]:
    return sorted(f"{normalize_dist_name(dist.name)}=={dist.version}" for dist in dists)


def app_source_ids(app_root: str) -> list[str]:
    ids = (
        module_id(info, origin)
        for info, origin in sorted(
            scan_app_modules([app_root], prefix="."), key=lambda x: x[0].name
        )
    )
    return [module_id_ for module_id_ in ids if module_id_ is not None]


def module_id(info: pkgutil.ModuleInfo, origin: str) -> str | None:
    try:
        file_size = os.stat(origin).st_size
    except OSError:
        logger.debug(
            "failed to stat app source module during fingerprinting, skipping it",
            module_name=info.name,
            origin=origin,
            exc_info=True,
        )
        return None
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
