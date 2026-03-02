"""Session-based context provider system.

This module provides an extensible system for extracting and managing
contextual information during agent sessions.

Example usage:
    from emdash_core.context import ContextService

    # Create service
    service = ContextService()

    # Get terminal ID (creates one if not exists)
    terminal_id = ContextService.get_terminal_id()

    # Update context after changes
    service.update_context(terminal_id)

    # Get formatted context for LLM
    context_prompt = service.get_context_prompt(terminal_id)

Adding new providers:
    1. Create a new provider class inheriting from ContextProvider
    2. Implement extract_context() method
    3. Register with ContextProviderRegistry.register("name", MyProvider)
    4. Add to CONTEXT_PROVIDERS env var
"""

from .models import ContextItem, ContextProviderSpec, SessionContext
from .reranker import get_rerank_scores, rerank_context_items
from .registry import ContextProviderRegistry, get_provider
from .service import ContextService
from .session import SessionContextManager

# Import providers to trigger registration
from .providers import explored_areas, touched_areas  # noqa: F401

__all__ = [
    # Models
    "ContextItem",
    "ContextProviderSpec",
    "SessionContext",
    # Registry
    "ContextProviderRegistry",
    "get_provider",
    # Reranker
    "rerank_context_items",
    "get_rerank_scores",
    # Service
    "ContextService",
    # Session
    "SessionContextManager",
]
