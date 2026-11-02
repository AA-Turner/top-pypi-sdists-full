"""Migration tooling for the AdCP SDK.

Run via ``python -m adcp.migrate <migration> <path>``.

Migrations are one-shot code rewriters for spec major-version bumps.
They are *not* a runtime compatibility layer — the removed types are
gone. The migrations turn a 2-3 day sed hunt into an afternoon by
doing the mechanical renames automatically and reporting what the
seller still has to fix by hand.

Supported migrations:

* ``v3-to-v4`` — 3.x → 4.0 rename + removal report. Renames the 9
  ``<Type>Asset`` → ``<Type>Content`` classes and flags usages of
  removed types (``BrandManifest``, ``DeliverTo``, ``Pricing``, etc.)
  and of numbered ``Assets<N>`` direct imports that aren't stable.
"""

from __future__ import annotations

__all__ = ["v3_to_v4"]

from adcp.migrate import v3_to_v4
