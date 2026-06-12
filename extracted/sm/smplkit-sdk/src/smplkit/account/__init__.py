"""Smpl Account — account-level settings on ``client.account``.

``client.account`` exposes the authenticated account's own configuration:

- ``client.account.settings.*``

The :class:`AccountClient` / :class:`AsyncAccountClient` classes are
re-exported from the top-level :mod:`smplkit` package (the established
convention that clients re-export from ``smplkit`` only). This package
exports the customer-facing account-settings models.
"""

from __future__ import annotations

from smplkit.account.models import AccountSettings, AsyncAccountSettings

__all__ = [
    "AccountSettings",
    "AsyncAccountSettings",
]
