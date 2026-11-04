"""The AI assigned to a chat, as cintia-lambdas keeps it: two read-only ports (ADR-012 §2).

`chatty_ai_agents_in_chat` (one document per chat: the agent, its mode, whether it waits for a human) and
`cintia_executions` (each run of CINTIA) are written by cintia-lambdas, which treats them as the source of truth;
api-chatty only reads them, without cache, as `main` did (`company/assets/chatty_ai_agents_in_chat.py`). The chat's
own mirror (`chats.chatty_ai_agent_in_chat_status`) is the chat aggregate's, not these.

Every read goes by the id of the chat or of the execution, of any company: `main`'s filters have no `company_id`, and
the caller already read the chat (ADR-007: whose it is, the caller's).
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Protocol

from ...models.chat.preview import ChattyAiAgentStatus
from ...models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChat
from ...models.company.assets.ai_agents_v2.chatty_ai_agent_in_chat import ChattyAIAgentInChat
from ...models.utils.types import StrObjectId


class AiAgentInChatRepository(Protocol):
    async def of_chat(self, chat_id: StrObjectId) -> Optional[ChattyAIAgentInChat]:
        """The live one (`deleted_at` null or absent), without its chains of thought nor its events; `None` if there
        is none."""
        ...

    async def status_for_preview(self, chat_id: StrObjectId, projection: Dict[str, int]) -> Optional[ChattyAiAgentStatus]:
        """`ESCALATED` / `ASSIGNED` of the live one read with `projection` as `main` took it; `None` without one or
        without an agent. No caller (ENG-156)."""
        ...

    async def chains_of_thought(self, chat_id: StrObjectId) -> List[dict]:
        """The nested chains of the live one as previews dumped to JSON; `[]` without one. No caller and no document
        has the field in prod (ENG-156)."""
        ...

    async def chain_of_thought(self, chat_id: StrObjectId, chain_of_thought_id: StrObjectId) -> Optional[ChainOfThoughtInChat]:
        """One nested chain of the live one, by its id; `None` if it is not there (ENG-156: no document has them)."""
        ...


class CintiaExecutionRepository(Protocol):
    async def has_active(self, chat_id: StrObjectId) -> bool:
        """Whether CINTIA runs anything for the chat: an execution not finished and not held for lack of credit."""
        ...

    async def agents_of(self, cintia_ids: Iterable[str]) -> Dict[str, str]:
        """`{execution id: ai_agent_id}` of those executions, in one query; ids that are not one and executions that
        are not there (or have no agent) are left out; with no valid id, no query."""
        ...
