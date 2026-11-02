"""Value object for resolved API credentials."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    """Username and password for one API origin."""

    username: str
    password: str
