"""Chain of thought (the reasoning of the AI on a chat): the port of the standalone `chain_of_thoughts` collection.

The entity is `letschatty.models.company.assets.ai_agents_v2.chain_of_thought_in_chat.ChainOfThoughtInChat`,
unchanged. Since April 2026 the chains live nested in `chatty_ai_agents_in_chat`; this collection is only read, by id,
as a fallback, and nobody writes it any more.

Not async on purpose: `main` called it without `await` and its callers depend on that (api-chatty
`docs/ia/cadena-de-pensamientos.md`, ENG-126). It reads by id alone, of any company, as `main` (ADR-007: the caller
checks whose it is).
"""
from __future__ import annotations

from typing import Protocol

from ...models.company.assets.ai_agents_v2.chain_of_thought_in_chat import ChainOfThoughtInChat
from ...models.utils.types import StrObjectId


class ChainOfThoughtRepository(Protocol):
    def get(self, chain_of_thought_id: StrObjectId) -> ChainOfThoughtInChat:
        """By id, of any company. `bson.errors.InvalidId` when the id is not one. ENG-126: the Mongo adapter never
        awaits its read, so for every valid id it raises `TypeError` and never returns (nor raises `NotFoundError`)."""
        ...
