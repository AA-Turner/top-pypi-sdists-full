"""Represent versions and introspect on corvic version."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Version:
    """A version."""

    major: int
    minor: int
    patch: int
    unparsed: str | None = None

    def less_than(self, other: Version) -> bool:
        """Return true if this version is less than other."""
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )


def parse_version(semver: str) -> Version:
    """Parse a version string into its components."""
    unparsed = None
    patch = 0

    parts_itr = iter(semver.split(".", maxsplit=2))
    major = int(next(parts_itr, 0))
    minor = int(next(parts_itr, 0))
    patchish = next(parts_itr, "")

    if patchish:
        m = re.match(r"(\d+)(.*)?", patchish)
        if m and m.group(1):
            patch = int(m.group(1))
        unparsed = None
        if m and m.group(2):
            unparsed = m.group(2)

    return Version(major, minor, patch, unparsed)
