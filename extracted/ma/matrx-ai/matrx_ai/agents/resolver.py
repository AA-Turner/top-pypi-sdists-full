"""Conversation and Agent config resolution.

Single responsibility: given an ID (or raw config), return a UnifiedConfig
ready for execution. Owns the resolution order — in-memory cache first,
database second — so nothing outside this module needs to know how config
is sourced.

Usage:
    from matrx_ai.conversation_resolver import ConversationResolver, AgentConfigResolver

    # Continuing an existing conversation:
    config = await ConversationResolver.from_conversation_id(
        conversation_id, user_input=request.user_input
    )

    # Starting an agent:
    config = await AgentConfigResolver.from_id(
        agent_id, variables=request.variables, overrides=request.config_overrides
    )
"""

from __future__ import annotations

import traceback
from copy import deepcopy
from typing import Any

from fastapi import HTTPException, status
from matrx_utils import vcprint

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.definition import Agent
from matrx_ai.config import LLMParams, UnifiedConfig


async def _load_unified_config(conversation_id: str) -> UnifiedConfig:
    """History-read seam: a configured ConversationStore (client host) serves
    the stored config dict; otherwise the cx_ tables via cxm (server path).
    cxm is resolved lazily — importing this module must not require DB config.
    """
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is not None:
        config_dict = await store.get_conversation_config(conversation_id)
        return UnifiedConfig.from_dict(config_dict)
    from matrx_ai.db import cxm

    return await cxm.get_conversation_unified_config(conversation_id)


def _pin_system_date(config: Any, conv_row: Any) -> None:
    """Freeze the system-prompt date to the conversation's ``created_at``.

    The "Current date" decoration is pinned ONCE per conversation to an
    immutable, already-persisted anchor so the cacheable system prefix never
    changes — not between loop rounds, not across midnight, not across a DB
    reload. Best-effort: if anything is missing we leave ``date_anchor`` unset
    and SystemInstruction falls back to a single memoized ``now()``.
    """
    si = getattr(config, "system_instruction", None)
    if si is None or getattr(si, "date_anchor", None):
        return
    created = getattr(conv_row, "created_at", None)
    if created is None:
        return
    if isinstance(created, str):
        # Persisted ISO timestamp — the date is the leading 10 chars.
        anchor = created[:10]
    else:
        try:
            anchor = created.strftime("%Y-%m-%d")
        except Exception:
            return
    if len(anchor) == 10:
        si.date_anchor = anchor


# ---------------------------------------------------------------------------
# Conversation resolver
# ---------------------------------------------------------------------------


class ConversationResolver:
    """Resolves a UnifiedConfig from a conversation_id.

    Resolution order:
        1. AgentCache (in-memory, instant — already converted, zero reconstruction)
        2. Database via cxm (auto-cached by the ORM layer)
        3. HTTP 404 if not found

    The in-memory AgentCache is the primary cache. It stores Agent objects
    whose .config is the fully-reconstructed UnifiedConfig (media already
    processed, tool content already rebuilt). Hitting the cache means zero
    DB queries and zero reconstruction work.
    """

    @staticmethod
    async def from_conversation_id(
        conversation_id: str,
        user_input: str | list[dict[str, Any]] | None = None,
        config_overrides: LLMParams | None = None,
    ) -> UnifiedConfig:
        """Return a UnifiedConfig ready for execution.

        Appends user_input (if provided) and applies config_overrides before
        returning. Updates AgentCache after a DB load so subsequent calls
        within the same process are instant.

        Raises HTTPException(404) if the conversation cannot be found.
        """

        agent = AgentCache.get(conversation_id)

        if agent is not None:
            vcprint(f"[ConversationResolver] Cache hit: {conversation_id}", color="green")
            config = deepcopy(agent.config)
        else:
            vcprint(
                f"[ConversationResolver] Cache miss — loading from DB: {conversation_id}",
                color="yellow",
            )
            try:
                config = await _load_unified_config(conversation_id)
            except Exception as exc:
                tb_str = traceback.format_exc()
                vcprint(
                    f"[ConversationResolver] DB load FAILED for {conversation_id}\n"
                    f"  Exception type : {type(exc).__name__}\n"
                    f"  Exception      : {exc}\n"
                    f"  Traceback:\n{tb_str}",
                    color="red",
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation not found: {conversation_id}",
                ) from exc

            agent = Agent(config=deepcopy(config))
            AgentCache.set(conversation_id, agent)

        if config_overrides is not None:
            config.apply_overrides(config_overrides)

        if user_input:
            config.append_or_extend_user_input(user_input)

        # In-memory context-trim pass — collapses old, large tool-result
        # blocks to a compact preview so the model isn't re-reading
        # stale 30KB JSON every turn. DB stays untouched; the trim is
        # purely a transformation on the in-memory UnifiedConfig that's
        # about to be handed to the executor. See context_trim.py for
        # the tier rules and safety guards (image/audio/video skipped).
        #
        # The TrimReport is stashed on AppContext.metadata so persistence
        # can copy it onto cx_request.trim_summary (Phase 1d). The metadata
        # is per-request and cleared by the streaming infrastructure.
        try:
            from matrx_ai.config.context_trim import trim_messages_context
            from matrx_ai.context.app_context import try_get_app_context

            messages_iter = (
                list(config.messages) if not isinstance(config.messages, list) else config.messages
            )

            # Phase 2: load the conversation's cache_state so the trim can
            # protect a live prompt-cache prefix. Best-effort — if the read
            # fails or the row doesn't exist (new conversation), pass None
            # and the trim falls back to its unconditional behaviour.
            cache_state_dict: dict[str, Any] | None = None
            try:
                from matrx_ai.client_host import get_conversation_store
                from matrx_ai.db import cxm

                # ALWAYS load the conversation row so we can pin the system-
                # prompt date to created_at. The old path raised when a
                # client-host conversation store was configured, which skipped
                # the pin entirely — resume then re-memoized datetime.now()
                # and busted the prompt cache across midnight / TZ boundaries.
                conv_row = await cxm.conversation.load_conversation_by_id(conversation_id)
                if conv_row is not None:
                    _pin_system_date(config, conv_row)
                    # cx_ cache_state is only meaningful on the host DB path.
                    if get_conversation_store() is None:
                        cache_state_dict = getattr(conv_row, "cache_state", None) or None
            except Exception:
                cache_state_dict = None

            report = trim_messages_context(messages_iter, cache_state=cache_state_dict)
            ctx = try_get_app_context()
            if ctx is not None:
                ctx.metadata["last_trim_report"] = report.to_dict()
            if report.blocks_rewritten:
                vcprint(
                    f"[ConversationResolver] context-trim rewrote "
                    f"{report.blocks_rewritten} tool-result block(s) "
                    f"(freed {report.freed_chars} chars) for {conversation_id}",
                    color="yellow",
                )
        except Exception as trim_exc:
            # Trim is purely an optimisation — never let a trim bug
            # break the actual agent run.
            vcprint(
                f"[ConversationResolver] context-trim failed (ignored): {trim_exc}",
                color="red",
            )

        return config

    @staticmethod
    async def warm(conversation_id: str) -> bool:
        """Pre-load a conversation into AgentCache. Returns True if newly cached.

        Called by the warm endpoint. Fire-and-forget safe — errors are logged
        but never raised.
        """
        from matrx_ai.agents.cache import AgentCache
        from matrx_ai.agents.definition import Agent

        if AgentCache.exists(conversation_id):
            vcprint(
                f"[ConversationResolver] Already cached: {conversation_id}",
                color="green",
            )
            return False

        try:
            config = await _load_unified_config(conversation_id)
            AgentCache.set_warm(conversation_id, Agent(config=config))
            vcprint(f"[ConversationResolver] Warmed: {conversation_id}", color="green")
            return True
        except Exception as exc:
            vcprint(f"[ConversationResolver] Warm failed: {exc}", color="red")
            return False


# ---------------------------------------------------------------------------
# Agent config resolver
# ---------------------------------------------------------------------------


class AgentConfigResolver:
    """Resolves a UnifiedConfig from an agent_id.

    Loads the agent definition from agx (via Agent.from_agent), applies
    variables and config overrides, and returns the resulting UnifiedConfig.
    """

    @staticmethod
    async def from_id_with_metadata(agent_id: str) -> dict[str, Any]:
        """Return lightweight agent metadata (name, description) without building full config.

        Used by the agent router to capture agent identity for labeling.
        Fire-and-forget safe — returns empty dict on failure.
        """
        try:
            from matrx_ai.db.agx_manager import agx

            row = await agx.agx_agent.load_item_or_none(id=agent_id)
            if row is None:
                row = await agx.agx_version.load_item_or_none(id=agent_id)
            if row is None:
                return {}
            return {
                "name": getattr(row, "name", "") or "",
                "description": getattr(row, "description", "") or "",
            }
        except Exception as exc:
            vcprint(
                f"[AgentConfigResolver] Metadata load failed for {agent_id!r}: {exc}",
                color="yellow",
            )
            return {}

    @staticmethod
    async def from_id(
        agent_id: str,
        variables: dict[str, Any] | None = None,
        overrides: LLMParams | dict[str, Any] | None = None,
        source: str | None = None,
    ) -> UnifiedConfig:
        """Return a UnifiedConfig for the given agent prompt ID.

        When ``source`` is provided (e.g. "prompt_version"), the lookup goes
        directly to the correct table — no fallback chain.

        Raises HTTPException(404) if the agent cannot be found.
        """
        from matrx_ai.agents.definition import Agent

        try:
            agent = await Agent.from_id(
                agent_id, variables=variables, config_overrides=overrides, source=source
            )
        except Exception as exc:
            vcprint(
                f"[AgentConfigResolver] Load failed for {agent_id!r}: {exc}",
                color="red",
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent not found: {agent_id}",
            ) from exc

        return agent.config

    @staticmethod
    async def from_id_with_mandates(
        agent_id: str,
        variables: dict[str, Any] | None = None,
        overrides: LLMParams | dict[str, Any] | None = None,
        source: str | None = None,
    ) -> tuple[UnifiedConfig, list[dict[str, Any]], bool]:
        """Return (UnifiedConfig, context_policies, auto_context_disabled).

        ``context_policies`` is the agent-defined list of ContextPolicy descriptors
        used by the deferred context system. ``auto_context_disabled`` is the
        agent's context kill switch, returned alongside them because a caller
        that applies the policies without honouring the switch would silently
        deliver context the agent declared it does not want. Raises
        HTTPException(404) if the agent cannot be found.
        """
        from matrx_ai.agents.definition import Agent

        try:
            agent = await Agent.from_id(
                agent_id, variables=variables, config_overrides=overrides, source=source
            )
        except Exception as exc:
            vcprint(
                f"[AgentConfigResolver] Load failed for {agent_id!r}: {exc}",
                color="red",
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent not found: {agent_id}",
            ) from exc

        return agent.config, agent.context_policies, agent.auto_context_disabled

    @staticmethod
    async def warm(agent_id: str, source: str | None = None) -> bool:
        """Pre-load an agent definition into cache. Returns True if loaded.

        Fire-and-forget safe — errors are logged but never raised.
        """
        from matrx_ai.agents.definition import Agent

        try:
            is_version = source in ("prompt_version", "builtin_version")
            await Agent.from_agent(agent_id, is_version=is_version)
            vcprint(
                f"[AgentConfigResolver] Warmed: {agent_id} (source={source})",
                color="green",
            )
            return True
        except Exception as exc:
            vcprint(
                f"[AgentConfigResolver] Warm failed for {agent_id!r}: {exc}",
                color="red",
            )
            return False
