"""Package names as manifests and scripts write them: ``library/package``."""

from __future__ import annotations


def split_package_name(name: str) -> tuple[str, str]:
    """Return ``(library, package)`` from ``library/package``; anything else is a ValueError."""
    parts = name.split("/")
    if len(parts) != 2 or any(
        part in ("", ".", "..") or "\\" in part for part in parts
    ):
        raise ValueError(f"{name!r} is not a package name such as library/package")
    return parts[0], parts[1]
