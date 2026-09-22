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

from matrx_ai.agents import live_structure
from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.definition import Agent
from matrx_ai.config import LLMParams, UnifiedConfig
from matrx_ai.config.message_config import UnifiedMessage


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


async def _load_persisted_messages(conversation_id: str) -> list[UnifiedMessage]:
    """Load only the canonical rebuilt message projection for a continuation.

    A client-host store remains the authority when configured. Server callers
    use the same cx message/tool/media rebuild funnel as full config loads,
    without recreating unrelated structural configuration on every cache hit.
    """
    from matrx_ai.client_host import get_conversation_store

    store = get_conversation_store()
    if store is not None:
        config_dict = await store.get_conversation_config(conversation_id)
        return list(UnifiedConfig.from_dict(config_dict).messages)

    from matrx_ai.db import cxm

    return await cxm.get_rebuilt_conversation_messages(conversation_id)


# ---------------------------------------------------------------------------
# Conversation resolver
# ---------------------------------------------------------------------------


class ConversationResolver:
    """Resolves a UnifiedConfig from a conversation_id.

    Resolution order:
        1. AgentCache for structural agent configuration (tools, variables,
           runtime settings), plus a durable message-history fence.
        2. Database via cxm for a cold config load and the authoritative
           completed message projection on cached continuations.
        3. HTTP 404 if the persisted conversation cannot be found.

    The in-memory AgentCache stores Agent objects whose ``.config`` has already
    resolved structural agent state (media, tools, and runtime settings). Its
    message list is an optimization only: a cached continuation reloads the
    durable message projection before provider dispatch, so process-local cache
    propagation cannot decide conversation history.
    """

    @staticmethod
    async def from_conversation_id(
        conversation_id: str,
        user_input: str | list[dict[str, Any]] | None = None,
        config_overrides: LLMParams | None = None,
        responder_agent_id: str | None = None,
        responder_is_version: bool = False,
    ) -> UnifiedConfig:
        """Return a UnifiedConfig ready for execution.

        Appends user_input (if provided) and applies config_overrides before
        returning. Updates AgentCache after a cold DB load so subsequent calls
        can reuse structural resolution; cached continuations still fence their
        messages against durable history.

        ``responder_agent_id`` names an agent that supplies the STRUCTURAL
        configuration for this turn — system prompt, model, tools, settings —
        while the conversation still supplies the history. It exists for a
        conversation that has no configuration of its own to resolve: a coding
        session mirrored into AI Matrx is agentless by construction and its
        ``config`` blob is empty, so the ordinary path resolved a config with no
        model and the turn died at the provider. With a responder the SAME send
        boundary, history fence, and override handling below apply — this is not
        a second resolution path, only a different source for the structural
        half. The conversation row is never rewritten: the choice is per turn,
        and the process cache is deliberately NOT primed with it, so a later
        change to that choice takes effect on the very next turn.

        Raises HTTPException(404) if the conversation cannot be found.
        """

        if responder_agent_id:
            responder = await Agent.from_agent(
                responder_agent_id, is_version=responder_is_version, variables={}
            )
            config = deepcopy(responder.config)
            try:
                persisted_messages = await _load_persisted_messages(conversation_id)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation not found: {conversation_id}",
                ) from exc
            config.messages.clear()
            config.messages.extend(deepcopy(persisted_messages))
            return await ConversationResolver._finish(
                config,
                conversation_id=conversation_id,
                user_input=user_input,
                config_overrides=config_overrides,
            )

        agent = AgentCache.get(conversation_id)

        if agent is not None:
            vcprint(f"[ConversationResolver] Cache hit: {conversation_id}", color="green")
            config = deepcopy(agent.config)

            # The cache is allowed to accelerate structural agent resolution,
            # but it is never an authority for turn order.  A second transport
            # task/process can resolve a follow-up after the prior request
            # committed but before this process received that request's cache
            # update.  Reusing the cached messages in that window silently
            # sends an amnesiac provider payload.  Refresh only the durable
            # message projection before appending the new turn: cached tools,
            # variables, and runtime configuration remain intact, while the
            # database remains the completed-turn fence for every caller of
            # this shared resolver (agent, chat, resume, and voice).
            try:
                persisted_messages = await _load_persisted_messages(conversation_id)
            except Exception as exc:
                tb_str = traceback.format_exc()
                vcprint(
                    f"[ConversationResolver] history fence FAILED for {conversation_id}\n"
                    f"  Exception type : {type(exc).__name__}\n"
                    f"  Exception      : {exc}\n"
                    f"  Traceback:\n{tb_str}",
                    color="red",
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation not found: {conversation_id}",
                ) from exc
            config.messages.clear()
            config.messages.extend(deepcopy(persisted_messages))
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

        # ── A ROW THAT NAMES AN AGENT BUT NEVER RAN ONE ──────────────────
        # `system_instruction` on the conversation row is written by the turn
        # that adopted an agent's structure. A conversation created by a DOOR
        # — a Personal Staff thread minted so a text, a call and the in-app
        # page continue ONE conversation — never had such a turn, so the row
        # names its agent in `initial_agent_id` and carries none of that
        # agent's configuration. Every turn on it is a continuation, so
        # without this the agent's system prompt and its whole belt stay in
        # the database forever and the model answers from nothing: on
        # 2026-09-21 a Chief of Staff asked to run a shell command in its
        # owner's box printed a plausible hostname it had read in its briefing
        # and called no tool at all.
        #
        # Done HERE rather than in one caller because three continuation
        # surfaces share this resolver — the agent route, `/conversations/{id}`,
        # and crash recovery — and a fix in one of them leaves a person's staff
        # amnesiac on the other two. It costs one extra read, and only on a
        # conversation that is already in this state.
        #
        # TWO SYMPTOMS, ONE STATE. A row that never adopted an agent has no
        # frozen prompt; a row whose adoption was interrupted (a crash-recovery
        # turn rewrote its config blob from a turn that had nothing) keeps the
        # prompt and loses the belt — and a staff thread with a prompt but no
        # tools is the fabricating agent again, this time politely. Either
        # symptom means the same thing: the row is not carrying the agent it
        # names. The tool read costs one primary-key lookup and happens only on
        # a conversation that carries no tools at all, which on a tool-using
        # platform is the anomaly, not the norm.
        #
        # A THIRD STATE, AND THE ONE THE OTHER TWO KEPT COMING BACK FROM: the
        # row is MANDATE-HELD. Its structural half never belonged to it — it
        # belongs to whoever holds the mandate right now — so a frozen prompt
        # and a frozen belt on such a row are not evidence of adoption, they
        # are last week's Holder. `chat.conversation.config` is rewritten
        # wholesale at the end of every turn, so the in-app door's repair
        # (`personal_staff/thread_row.py`) held for exactly one turn and only
        # on the surface that opened the door; the SMS worker, the voice
        # ingress, crash recovery and the deferred-result inbox driver ran the
        # stale belt. The marker and the rule live in `agents/live_structure.py`
        # — read it before changing this branch.
        _structureless = not str(getattr(config, "system_instruction", None) or "").strip() or not (
            getattr(config, "tools", None) or getattr(config, "custom_tools", None)
        )
        source = None
        if not responder_agent_id:
            source = await live_structure.read_structure_source(conversation_id)

        if source is not None and source.is_live:
            live_agent, live_is_version = await live_structure.resolve_live_structure_agent(
                source
            )
            if live_agent:
                vcprint(
                    f"[ConversationResolver] {conversation_id} is mandate-held"
                    + (f" ({source.mandate_key})" if source.mandate_key else "")
                    + f" — resolving the structural half (prompt, model, tools, "
                    f"settings) LIVE from Holder {live_agent} while the conversation "
                    f"supplies the history. The row's own config is never the "
                    f"authority here.",
                    color="cyan",
                )
                return await ConversationResolver.from_conversation_id(
                    conversation_id,
                    user_input=user_input,
                    config_overrides=config_overrides,
                    responder_agent_id=live_agent,
                    responder_is_version=live_is_version,
                )
            vcprint(
                f"[ConversationResolver] {conversation_id} is marked mandate-held but "
                f"no Holder could be resolved for it. This turn runs with the "
                f"conversation's own configuration, which on a mandate-held row is "
                f"whatever a previous Holder left behind.",
                color="red",
            )

        if not responder_agent_id and _structureless:
            named = source.named_agent_id if source is not None else None
            named_is_version = source.named_is_version if source is not None else False
            if named and str(getattr(config, "system_instruction", None) or "").strip():
                # The prompt is already frozen, so the only thing worth taking
                # from the agent is a belt it actually has. Without this an
                # agent that legitimately carries no tools would have its
                # conversation re-resolved from the live definition on every
                # turn — quietly unfreezing a prompt the person's first turn
                # deliberately froze.
                try:
                    probe = await Agent.from_agent(
                        named, is_version=named_is_version, variables={}
                    )
                except Exception:  # noqa: BLE001 — a probe never fails a turn
                    named = None
                else:
                    if not (probe.config.tools or probe.config.custom_tools):
                        named = None
            if named:
                vcprint(
                    f"[ConversationResolver] {conversation_id} has no frozen system "
                    f"instruction and names agent {named} — resolving the structural "
                    f"half (prompt, model, tools, settings) from that agent while the "
                    f"conversation supplies the history.",
                    color="yellow",
                )
                return await ConversationResolver.from_conversation_id(
                    conversation_id,
                    user_input=user_input,
                    config_overrides=config_overrides,
                    responder_agent_id=named,
                    responder_is_version=named_is_version,
                )

        return await ConversationResolver._finish(
            config,
            conversation_id=conversation_id,
            user_input=user_input,
            config_overrides=config_overrides,
        )

    @staticmethod
    async def _finish(
        config: UnifiedConfig,
        *,
        conversation_id: str,
        user_input: str | list[dict[str, Any]] | None,
        config_overrides: LLMParams | None,
    ) -> UnifiedConfig:
        """Overrides, the new user turn, and THE SEND BOUNDARY — for every source
        of the structural config, so a responder turn can never skip them."""
        if config_overrides is not None:
            config.apply_overrides(config_overrides)

        if user_input:
            config.append_or_extend_user_input(user_input)

        # THE SEND BOUNDARY. Every prompt-shaping mutation between here and the
        # provider call goes through ``prepare_for_send`` — the system-date pin
        # (so the cacheable system prefix never wobbles) and the cache-gated
        # in-memory context trim (old, large tool-result blocks collapsed to a
        # compact preview so the model isn't re-reading stale 30KB JSON every
        # turn). The DB stays untouched; the trim is purely a transformation on
        # the in-memory UnifiedConfig about to be handed to the executor.
        # Never call trim_messages_context (or any other shaping step) directly
        # — see config/send_boundary.py for the law and the guard that enforces it.
        # Imported BEFORE the try: the except clause below names it, and a name
        # bound inside the try would not exist if the import itself failed.
        from matrx_ai.config.context_preflight import PromptTooLargeError

        try:
            from matrx_ai.config.send_boundary import STAGE_RESOLVE, prepare_for_send

            # Load the conversation row for BOTH the date pin and the Phase-2
            # cache_state the trim gate reads. ALWAYS load it: the old path
            # raised when a client-host conversation store was configured, which
            # skipped the pin entirely — resume then re-memoized datetime.now()
            # and busted the prompt cache across midnight / TZ boundaries.
            conv_row = None
            cache_state_dict: dict[str, Any] | None = None
            try:
                from matrx_ai.client_host import get_conversation_store
                from matrx_ai.db import cxm

                conv_row = await cxm.conversation.load_conversation_by_id(conversation_id)
                if conv_row is not None and get_conversation_store() is None:
                    # cx_ cache_state is only meaningful on the host DB path.
                    cache_state_dict = getattr(conv_row, "cache_state", None) or None
            except Exception:
                conv_row = None
                cache_state_dict = None

            await prepare_for_send(
                config,
                stage=STAGE_RESOLVE,
                conversation_id=conversation_id,
                conversation_row=conv_row,
                cache_state=cache_state_dict,
                user_input=user_input,
                config_overrides=config_overrides,
            )
        except PromptTooLargeError:
            # NOT a shaping failure: the prompt provably cannot fit the model's
            # window. Refusing here is the whole point — swallowing it would
            # hand the same prompt to the provider a moment later and lose the
            # step, the numbers and the remedy.
            raise
        except Exception as prep_exc:
            # Prompt shaping is an optimisation — never let it break the run.
            vcprint(
                f"[ConversationResolver] send-boundary prep failed (ignored): {prep_exc}",
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
