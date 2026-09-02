"""matrx_ai.client_host — the seams that let matrx-ai run in a CLIENT host.

A "client host" is an install with no Postgres and no matrx-orm wiring — the
matrx-local desktop app is the reference host. Instead of the 0.1.26
``client_mode`` package (a parallel mode switch), 0.3.0 expresses every
client-host need as an individually-optional ``configure()`` seam on the
``_ext`` registry:

* ``conversation_store``  — :class:`~matrx_ai.client_host.store.ConversationStore`;
  conversation/tool-call persistence delegates to the host (SQLite, memory, …).
* ``model_catalog``       — see ``matrx_ai.catalog.host_catalog``; model
  lookup + routing without the ORM.
* ``api_key_resolver``    — see ``matrx_ai.providers.keys``; provider keys
  from the host's secure store instead of os.environ.
* ``tool_source``         — see ``matrx_ai.tools.tool_source``; tool
  definitions without the ORM (checked BEFORE the ORM path by
  ``ToolRegistry.load_from_database``).
* ``get_jwt`` / ``server_url`` / ``source_app`` — server-backed features in
  a desktop install. With ``server_url`` + ``source_app`` set and no
  explicit ``tool_source``, the registry derives a ``ServerToolSource``
  that fetches ``{server_url}/ai-tools/app/{source_app}/all`` with the
  current JWT.

``validate_client_host_config()`` (called from ``configure()``) checks the
combination all-errors-at-once — the 0.1.26 ``ClientModeConfigError`` UX.
"""

from __future__ import annotations

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.client_host.store import (
    CONVERSATION_STORE_KEY,
    ConversationStore,
    missing_store_methods,
)


def get_conversation_store() -> ConversationStore | None:
    """Return the host-injected ConversationStore, or None when unset.

    The store-first dispatch sites (conversation gate, persistence, tool
    logger, conversation resolver) all check this; None means the server/ORM
    path runs unchanged.
    """
    if not has_ext(CONVERSATION_STORE_KEY):
        return None
    store = get_ext(CONVERSATION_STORE_KEY)
    if store is None:
        return None
    return store


__all__ = [
    "CONVERSATION_STORE_KEY",
    "ConversationStore",
    "get_conversation_store",
    "missing_store_methods",
]
