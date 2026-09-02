"""
CX_ Database Layer — Singleton manager instances for conversation exchange tables.

Usage:
    from matrx_ai.db import cxm, rebuild_conversation_messages
    from matrx_ai.db import ensure_conversation_exists, ensure_user_request_exists

Names are resolved LAZILY (PEP 562 ``__getattr__``). The submodules below pull in
the heavy config/orm chain, and the lightweight ``matrx_ai.db._registry``
(``get_model`` / ``get_base`` — imported at module top by many small modules)
lives *under this package*. An eager ``__init__`` therefore made even
``from matrx_ai.db._registry import get_model`` run the whole
``conversation_gate`` → ``cx_managers`` → ``unified_config`` import, which formed
a ``config`` ↔ ``db`` cycle that broke cold deep-imports (e.g. importing a
submodule before ``configure()``). Deferring resolution to first attribute
access keeps importing ``_registry`` cheap and breaks the cycle, while
``from matrx_ai.db import cxm`` behaves exactly as before (loads on first use).
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # import-time only for type checkers; never at runtime
    from .conversation_gate import (
        ConversationGateError,
        ConversationRunInFlightError,
        create_new_conversation,
        create_pending_user_request,
        ensure_conversation_exists,
        ensure_user_request_exists,
        launch_conversation_gate,
        mark_conversation_known,
        update_conversation_status,
        update_user_request_status,
        verify_existing_conversation,
    )
    from .conversation_rebuild import rebuild_conversation_messages
    from .cx_managers import (
        CxAgentMemoryManager,
        CxConversationManager,
        CxManagers,
        CxMediaManager,
        CxMessageManager,
        CxRequestManager,
        CxToolCallManager,
        CxUserRequestManager,
        cxm,
    )

# Public name → defining submodule. Resolved on first access so importing this
# package (and thus the lightweight _registry under it) never eagerly imports the
# heavy manager/gate chain.
_LAZY_EXPORTS = {
    "ConversationGateError": "conversation_gate",
    "ConversationRunInFlightError": "conversation_gate",
    "release_conversation_start_claim": "conversation_gate",
    "release_pending_start_claim": "conversation_gate",
    "create_new_conversation": "conversation_gate",
    "create_pending_user_request": "conversation_gate",
    "ensure_conversation_exists": "conversation_gate",
    "ensure_user_request_exists": "conversation_gate",
    "launch_conversation_gate": "conversation_gate",
    "mark_conversation_known": "conversation_gate",
    "update_conversation_status": "conversation_gate",
    "update_user_request_status": "conversation_gate",
    "verify_existing_conversation": "conversation_gate",
    "rebuild_conversation_messages": "conversation_rebuild",
    "CxAgentMemoryManager": "cx_managers",
    "CxConversationManager": "cx_managers",
    "CxManagers": "cx_managers",
    "CxMediaManager": "cx_managers",
    "CxMessageManager": "cx_managers",
    "CxRequestManager": "cx_managers",
    "CxToolCallManager": "cx_managers",
    "CxUserRequestManager": "cx_managers",
    "cxm": "cx_managers",
}

__all__ = [
    "ConversationGateError",
    "ConversationRunInFlightError",
    "release_conversation_start_claim",
    "release_pending_start_claim",
    "CxAgentMemoryManager",
    "CxConversationManager",
    "CxManagers",
    "CxMediaManager",
    "CxMessageManager",
    "CxRequestManager",
    "CxToolCallManager",
    "CxUserRequestManager",
    "create_new_conversation",
    "create_pending_user_request",
    "cxm",
    "ensure_conversation_exists",
    "ensure_user_request_exists",
    "launch_conversation_gate",
    "mark_conversation_known",
    "rebuild_conversation_messages",
    "update_conversation_status",
    "update_user_request_status",
    "verify_existing_conversation",
]


def __getattr__(name: str):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module = importlib.import_module(f".{module_name}", __name__)
    value = getattr(module, name)
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    return sorted(__all__)
