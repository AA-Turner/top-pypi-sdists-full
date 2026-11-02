"""the error every desktop-app update step raises: its message is the step's `error`."""

from __future__ import annotations


class InstallError(Exception):
    """A step that failed: its message is the step's `error`."""
