"""Built-in structured item types agents can emit during a run.

An *item* is a typed, session-traceable record (a finding, an asset, …) that an
agent reports back to the platform via the single ``report_item`` tool
(``item_type`` is a parameter, so one tool covers every type). The platform
ships ``Finding`` and ``Asset``; capabilities enable built-ins and declare their
own types via the ``produces`` manifest entry.

These models mirror the platform-side validators in
``packages/api/app/items/schemas.py`` — keep them in sync.
"""

from dreadnode.items.models import Asset, Finding, ItemSeverity

__all__ = ["Asset", "Finding", "ItemSeverity"]
