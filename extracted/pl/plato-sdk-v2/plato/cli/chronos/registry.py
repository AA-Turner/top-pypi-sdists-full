"""Registry utilities for parsing package strings."""

from __future__ import annotations


def parse_package_string(package_string: str) -> tuple[str, str | None]:
    """Parse a ``name:version`` reference into ``(name, version | None)``.

    Works for any package-like reference: world packages, agent packages,
    and Docker image URLs (after stripping the registry prefix).

    ``"latest"``, empty strings, and missing versions all normalise to
    ``None`` so callers never have to special-case the sentinel value.

    Args:
        package_string: e.g. ``"plato-world-foo:0.1.0"``, ``"claude-code:latest"``,
            or just ``"plato-world-foo"``

    Returns:
        ``(package_name, version)`` where *version* is ``None`` when
        unspecified or ``"latest"``.
    """
    if ":" in package_string:
        name, version = package_string.split(":", 1)
        version = version.strip()
        if not version or version == "latest":
            return name, None
        return name, version
    return package_string, None


def parse_image_url(image: str) -> tuple[str, str | None]:
    """Extract package name and version from a Docker image URL.

    Strips the registry/repo prefix (everything before the last ``/``)
    and parses the remaining ``name:tag`` with :func:`parse_package_string`.
    """
    last_part = image.split("/")[-1]
    return parse_package_string(last_part)
