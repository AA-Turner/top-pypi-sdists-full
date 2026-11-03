"""AI agents of a company (`ai_agents`): the port every agent store implements.

The entity is `letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent.ChattyAIAgent`, unchanged: cintia-lambdas,
onboarding-intelligence and polls-lambda read and write the same documents straight to Mongo.

Every method takes the company first (the one the caller asks from); the repository reads by id and does not filter
by it, as `main` did. Per ADR-007 the use case checks the company where `main` did (nowhere today: ENG-10). `None` is
the company of the reads of any company (`GetAiAgent.any_company`, ADR-010 §3): the readers of the agent of a chat.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Tuple

from ...models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from ...models.utils.types import StrObjectId


class AiAgentRepository(Protocol):
    """Raises `NotFoundError` when no agent has that id (deleted ones are read)."""

    async def get(self, company_id: Optional[StrObjectId], agent_id: StrObjectId) -> ChattyAIAgent:
        """By id, through the cache."""
        ...

    async def get_fresh(self, company_id: Optional[StrObjectId], agent_id: StrObjectId) -> ChattyAIAgent:
        """By id from the store now, leaving it in the cache."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live agents of the company, as JSON-ready preview dicts."""
        ...

    async def add(self, agent: ChattyAIAgent) -> ChattyAIAgent: ...

    async def update(self, company_id: StrObjectId, agent_id: StrObjectId, changes: ChattyAIAgent) -> ChattyAIAgent:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...

    async def stored_updated_at(self, company_id: StrObjectId, agent_id: StrObjectId) -> Tuple[bool, Any]:
        """Whether it is stored, and its `updated_at` exactly as stored (raw: the compare-and-set compares that value)."""
        ...

    async def replace_if_unchanged(self, company_id: StrObjectId, agent: ChattyAIAgent, stored_updated_at: Any) -> bool:
        """Writes the whole `agent` (all but `_id`) only if the stored `updated_at` is still `stored_updated_at`.
        False when another write got there first."""
        ...

    async def delete(self, company_id: StrObjectId, agent_id: StrObjectId) -> ChattyAIAgent:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...

    async def company_ids_with_calendar(self, calendar_email: str) -> List[Any]:
        """The `company_id` of every agent, of any company and deleted ones too, whose `calendars` has that email,
        as stored (text or ObjectId), in the store's order (the lookup of every company, ADR-010 §3)."""
        ...
