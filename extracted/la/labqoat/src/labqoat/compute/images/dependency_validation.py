"""Bounded immutable package and index inputs for service-owned dependency resolution."""

import re
from urllib.parse import urlsplit

from labqoat.compute.images.image_validation import ImageValidation


class DependencyValidation:
    """Reject floating requirements, option injection and credential-bearing index URLs."""

    @staticmethod
    def python(packages: tuple[str, ...]) -> tuple[str, ...]:
        """Require exact PEP 440 version spellings, optionally with explicitly selected extras."""
        for package in ImageValidation.commands(packages):
            if (
                re.fullmatch(
                    r"[A-Za-z0-9][A-Za-z0-9_.-]*(?:\[[A-Za-z0-9_,.-]+\])?==[A-Za-z0-9][A-Za-z0-9_.+!-]*", package
                )
                is None
            ):
                raise ValueError("Python image packages must use exact name==version requirements")
        return packages

    @staticmethod
    def apt(packages: tuple[str, ...]) -> tuple[str, ...]:
        """Require Debian name=version pins rather than mutable package names."""
        for package in ImageValidation.commands(packages):
            if re.fullmatch(r"[a-z0-9][a-z0-9+.-]*(?::[a-z0-9]+)?=[A-Za-z0-9][A-Za-z0-9.+:~_-]*", package) is None:
                raise ValueError("System image packages must use exact name=version requirements")
        return packages

    @staticmethod
    def index(value: str | None) -> str | None:
        """Permit explicit HTTPS indexes without embedding reusable secrets in a retained recipe."""
        if value is None:
            return None
        ImageValidation.text(value)
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
            raise ValueError("Package indexes must be credential-free HTTPS URLs")
        return value

    @staticmethod
    def names(values: tuple[str, ...]) -> tuple[str, ...]:
        """Validate package, extra and group selectors before converting them to uv arguments."""
        if len(values) > 128 or any(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value) is None for value in values):
            raise ValueError("Invalid uv package, group or extra selection")
        return values
