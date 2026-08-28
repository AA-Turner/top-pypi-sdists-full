"""Primitive state: one protocol, one implementation, one key grammar.

``_contracts/09-tobe-engine-architecture.md`` §4 -- the durability seam (**D6**).

    from matrice_analytics.engine.state import InMemoryStateStore, Lifetime, StateStore

App authors only ever see ``StateStore``, handed to their ``__init__``; the runtime owns
which implementation it is and what scope it is pointed at.

* :mod:`~matrice_analytics.engine.state.store` -- the protocol, the key grammar
  (``<camera_id>/<app_id>/<zone>/<primitive>/<name>``) and :class:`Lifetime`.
* :mod:`~matrice_analytics.engine.state.memory` -- the only implementation for now.

This package has no dependency on ``matrice_analytics.post_processing`` or
``matrice_analytics.analytics``, and none on the wire format.
"""

from __future__ import annotations

from matrice_analytics.engine.state.memory import InMemoryStateStore
from matrice_analytics.engine.state.store import (
    KEY_SEPARATOR,
    Lifetime,
    StateKeyError,
    StateLifetimeError,
    StateStore,
    escape_component,
    make_key,
    scope_key,
    stable_namespace,
)

__all__ = [
    "KEY_SEPARATOR",
    "InMemoryStateStore",
    "Lifetime",
    "StateKeyError",
    "StateLifetimeError",
    "StateStore",
    "escape_component",
    "make_key",
    "scope_key",
    "stable_namespace",
]
