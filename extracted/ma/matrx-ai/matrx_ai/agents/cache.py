"""
Agent cache — two-tier warm/active design.

- active_cache: 30-min TTL for conversations being actively used.
- warm_cache:   10-min TTL for conversations pre-loaded by warm endpoints.

get()      → checks active first, then warm (auto-promotes warm hits to active).
set()      → always writes to active (full 30-min TTL).
set_warm() → writes to warm only if not already in active (10-min TTL).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from matrx_ai.utils.cache import TTLCache

if TYPE_CHECKING:
    from matrx_ai.agents.definition import Agent

_active_cache: TTLCache[Agent] = TTLCache(ttl_seconds=1800, max_size=200)
_warm_cache: TTLCache[Agent] = TTLCache(ttl_seconds=600, max_size=200)


class AgentCache:
    @classmethod
    def get(cls, conversation_id: str) -> Agent | None:
        agent = _active_cache.get(conversation_id)
        if agent is not None:
            return agent
        # Check warm cache and promote to active on hit
        agent = _warm_cache.get(conversation_id)
        if agent is not None:
            _active_cache.set(conversation_id, agent)
            _warm_cache.remove(conversation_id)
        return agent

    @classmethod
    def set(cls, conversation_id: str, agent: Agent) -> None:
        _active_cache.set(conversation_id, agent)

    @classmethod
    def set_warm(cls, conversation_id: str, agent: Agent) -> None:
        if not _active_cache.exists(conversation_id):
            _warm_cache.set(conversation_id, agent)

    @classmethod
    def remove(cls, conversation_id: str) -> None:
        _active_cache.remove(conversation_id)
        _warm_cache.remove(conversation_id)

    @classmethod
    def exists(cls, conversation_id: str) -> bool:
        return _active_cache.exists(conversation_id) or _warm_cache.exists(
            conversation_id
        )

    @classmethod
    def clear(cls) -> None:
        _active_cache.clear()
        _warm_cache.clear()
