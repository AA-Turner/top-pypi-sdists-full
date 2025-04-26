r"""Contain the definition of the exceptions."""

from __future__ import annotations

__all__ = ["AssetExistsError", "AssetNotFoundError", "SplitNotFoundError"]


class AssetExistsError(Exception):
    r"""Raised when trying to add an asset that already exists."""


class AssetNotFoundError(Exception):
    r"""Raised when trying to access an asset that does not exist."""


class SplitNotFoundError(Exception):
    r"""Raised when trying to access a split that does not exist."""
