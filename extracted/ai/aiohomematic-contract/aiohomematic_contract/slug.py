# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Shared slug rule for hub data-point names.

aiohomematic builds the ``unique_id`` of hub data points (system variables,
programs, connectivity, metrics, …) as
``generate_unique_id(address=..., parameter=hub_slug(legacy_name))``, where the
slug is produced by **python-slugify with default settings** (dash separator,
Unicode transliteration, lowercased).

This is a contract landmine: a naive ``replace(":"/"-"/" ", "_").lower()``
cleaner diverges from python-slugify on any non-ASCII name — e.g.
``"Außen Temperatur"`` slugifies to ``"aussen-temperatur"`` (ä→a, ß→ss) but a
naive cleaner yields ``"außen_temperatur"``. Different slug ⇒ different
``unique_id`` ⇒ lost Home Assistant entities/history on cutover. Any
alternative backend MUST reproduce this exact rule.

Note: ``generate_unique_id`` folds ``-`` to ``_`` only in the *address*, not in
the *parameter*, so the dash from the slug survives into the final id
(``ccu3_sysvar_aussen-temperatur``).
"""

from slugify import slugify

__all__ = ["hub_slug"]


def hub_slug(name: str) -> str:
    """Slugify a hub data-point name exactly as aiohomematic does."""
    return slugify(name)
