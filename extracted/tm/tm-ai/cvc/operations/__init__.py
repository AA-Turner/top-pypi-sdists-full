"""
cvc.operations — engine-level operations and the COGNOME substrate.
"""

from cvc.operations.cognome import (
    CognomeCompiler,
    CompiledEngram,
    Noeme,
    estimate_tokens,
)
from cvc.operations.cognome_manager import (
    CognomeAuditEntry,
    CognomeManager,
    CognomeStatus,
)
from cvc.operations.cognome_runtime import CognomeRuntime
from cvc.operations.engram_injectors import (
    AnthropicEngramInjector,
    EngramInjector,
    GoogleEngramInjector,
    OllamaEngramInjector,
    select_injector,
)
from cvc.operations.handoff import DEFAULT_FILENAME, HandoffPackage, HandoffTurn
from cvc.operations.session_scratchpad import SessionScratchpad, list_sessions

__all__ = [
    "CognomeCompiler",
    "CompiledEngram",
    "Noeme",
    "estimate_tokens",
    "CognomeAuditEntry",
    "CognomeManager",
    "CognomeStatus",
    "CognomeRuntime",
    "EngramInjector",
    "AnthropicEngramInjector",
    "GoogleEngramInjector",
    "OllamaEngramInjector",
    "select_injector",
    "SessionScratchpad",
    "list_sessions",
    "HandoffPackage",
    "HandoffTurn",
    "DEFAULT_FILENAME",
]
