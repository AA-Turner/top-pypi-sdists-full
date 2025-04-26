r"""Contain the definition of the exceptions."""

from __future__ import annotations

__all__ = ["ShardExistsError", "ShardNotFoundError"]


class ShardExistsError(Exception):
    r"""Raised when trying to add a shard that already exists."""


class ShardNotFoundError(Exception):
    r"""Raised when trying to access a shard that does not exist."""
