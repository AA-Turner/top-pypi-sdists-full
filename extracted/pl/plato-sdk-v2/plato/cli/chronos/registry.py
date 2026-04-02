"""Registry utilities for parsing package strings."""

from __future__ import annotations


def parse_package_string(package_string: str) -> tuple[str, str | None]:
    """Parse package:version string into (package, version) tuple.

    Args:
        package_string: Package string like "plato-world-foo:0.1.0" or just "plato-world-foo"

    Returns:
        Tuple of (package_name, version) where version may be None
    """
    if ":" in package_string:
        name, version = package_string.split(":", 1)
        if not version or version == "latest":
            return name, None
        return name, version
    return package_string, None
