"""The state of a workflow in a chat (`chat_flow_states`, ADR-012 §6 of api-chatty): its own aggregate, one document per
(chat, workflow) under the unique index `uniq_chat_flow`. copilot_v2 runs it and edits it by compare-and-set on
`last_call`/`next_call`. The chat keeps the reference `chats.flow_ids`, which this port never writes: api-chatty writes
it through its `ChatRepository`, after the state on a link and after the delete on an unlink.

`company_id` comes first and does not enter any filter: the states are read and written by `_id` or by
(`chat_id`, `flow_id`), as before. No cache. Waking the states when the chat changes (`mark_chat_changed`) is a write of
the chat over this aggregate and stays in `ChatFlowStateCollection` (ADR-012 §7).
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Mapping, Optional, Protocol, Sequence

from ...models.chat.flow_link_state import FlowStateAssignedToChat


class ChatFlowStateRepository(Protocol):
    async def insert(self, company_id: str, state: FlowStateAssignedToChat) -> None:
        """Stores the state as `FlowStateAssignedToChat.to_document()` dumps it (dates as dates, `_id` an ObjectId),
        after looking for one of the same chat and workflow. Raises `AssetAlreadyAssigned` when there is one (also when
        the unique index refuses it: two links at once)."""
        ...

    async def delete(self, company_id: str, chat_id: str, workflow_id: str) -> bool:
        """Deletes the state of that chat and workflow. True if there was one."""
        ...

    async def update(self, company_id: str, state_id: str, state: FlowStateAssignedToChat, fields: Sequence[str],
                     expected: Optional[Mapping[str, Optional[datetime]]] = None) -> bool:
        """`$set` of `fields` with the values `state` stores, never the whole state. With `expected` (field → value as
        stored, `last_call`/`next_call`) it is a compare-and-set: it writes only while those fields are still that. True
        if a document matched."""
        ...

    async def get(self, company_id: str, state_id: str) -> Optional[FlowStateAssignedToChat]:
        """The state with that id, or None."""
        ...

    async def of_chat(self, company_id: str, chat_id: str) -> List[FlowStateAssignedToChat]:
        """The chat's states, with `should_execute` computed for now."""
        ...
