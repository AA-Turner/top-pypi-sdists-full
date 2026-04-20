"""save_memory tool — AI-initiated durable memory candidates (#217).

The tool delegates to :func:`memory_promotion.propose_candidate` with
``proposer="agent"`` so every agent-proposed fact enters the governed
review queue shipped in #920 rather than writing to disk directly.

Phase 1 restricts ``scope`` to ``user`` and ``local``. Project-scoped
memories are deferred until a reliable ``project_slug`` surface exists
on the active-space dict; attempts to use ``scope="project"`` return a
typed error so the LLM stops retrying.

The handler follows the repo's tool contract:
- Accepts underscore-prefixed context kwargs (``_db``, ``_conversation_id``,
  ``_config``, ``_user_id``) injected by :func:`tools.ToolRegistry.call_tool`.
- Returns ``{"error": ..., "retry_hint"?: ...}`` payloads on every
  failure path — never raises.
"""

from __future__ import annotations

import logging
import sqlite3
from typing import Any

from ..services import memory_promotion
from ..services.memory_promotion import (
    PromotionAgentDisabledError,
    PromotionError,
    PromotionRateLimitError,
)

logger = logging.getLogger(__name__)

_CATEGORIES = ("preference", "project_fact", "decision", "workflow_hint")
_SCOPES_PHASE_1 = ("user", "local")
_MAX_CONTENT_CHARS = 500


DEFINITION: dict[str, Any] = {
    "name": "save_memory",
    "description": (
        "Propose a durable fact worth remembering across sessions. The fact "
        "enters the user's review queue as a candidate and only becomes "
        "active after explicit approval (unless the install has enabled "
        "memory.promotion.local_auto_approve). Under the default approval "
        "mode (ask_for_writes) the user is prompted before the candidate "
        "is queued — that prompt IS the first review step."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "minLength": 1,
                "maxLength": _MAX_CONTENT_CHARS,
                "description": "The fact to remember (1-500 characters).",
            },
            "category": {
                "type": "string",
                "enum": list(_CATEGORIES),
                "description": ("Kind of fact: preference, project_fact, decision, or workflow_hint."),
            },
            "scope": {
                "type": "string",
                "enum": list(_SCOPES_PHASE_1),
                "default": "user",
                "description": (
                    "Where the memory applies. Phase 1: 'user' (cross-project) "
                    "or 'local' (this machine only). 'project' scope is not yet supported."
                ),
            },
        },
        "required": ["content", "category"],
    },
}


async def handle(
    content: str,
    category: str,
    scope: str = "user",
    *,
    _db: Any = None,
    _conversation_id: str | None = None,
    _config: Any = None,
    _user_id: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Propose a memory candidate through the governed promotion pipeline."""

    if _db is None or _config is None:
        return {"error": "save_memory is unavailable in this context"}

    if not isinstance(content, str):
        return {"error": "content must be 1–500 characters"}
    stripped = content.strip()
    if not stripped or len(stripped) > _MAX_CONTENT_CHARS:
        return {"error": "content must be 1–500 characters"}

    if scope == "project":
        return {
            "error": ("save_memory scope='project' is not yet supported. Use 'user' or 'local'."),
        }
    if scope not in _SCOPES_PHASE_1:
        return {"error": f"Invalid memory scope: {scope!r}. Use 'user' or 'local'."}

    # Defense-in-depth: the JSON-schema enum is advisory; guard here too so a
    # caller that bypasses the schema (fuzzer, compromised sub-agent) still hits
    # the allowlist without a DB round-trip.
    if category not in _CATEGORIES:
        return {"error": f"Invalid memory category: {category!r}"}

    try:
        promo_config = _config.memory.promotion
    except AttributeError:
        return {"error": "save_memory is unavailable in this context"}

    provenance: dict[str, str | None] = {}
    if _conversation_id:
        provenance["conversation_id"] = _conversation_id

    try:
        artifact = memory_promotion.propose_candidate(
            _db,
            content=stripped,
            scope=scope,
            category=category,
            proposer="agent",
            proposer_id=_user_id,
            provenance=provenance or None,
            config=promo_config,
        )
    except PromotionAgentDisabledError as exc:
        return {"error": str(exc)}
    except PromotionRateLimitError as exc:
        return {
            "error": str(exc),
            "retry_hint": (
                "Review existing candidates first via /memory candidates; approve or reject them to free a slot."
            ),
        }
    except ValueError as exc:
        return {"error": str(exc)}
    except sqlite3.IntegrityError:
        return {"error": "A memory with this auto-generated FQN already exists"}
    except PromotionError as exc:
        return {"error": f"Failed to save memory: {exc}"}
    except Exception as exc:
        logger.exception("save_memory failed unexpectedly: %s", exc)
        return {"error": f"Failed to save memory: {type(exc).__name__}"}

    metadata = artifact.get("metadata") or {}
    return {
        "fqn": artifact.get("fqn", ""),
        "memory_status": metadata.get("memory_status", "candidate"),
        "category": metadata.get("memory_category", category),
        "scope": metadata.get("memory_scope", scope),
    }
