"""Sends to Meta's Conversions API («envíos a la Conversions API»): the read-only port of `meta_notification_logs`.

The conversions lambda writes one document per call to the CAPI, with Meta's answer; api-chatty only reads a company's
newest ones to show, on a chat's contact points, what Meta did with each conversion. No cache, no writes, no events.

A send is read lazily on purpose (api-chatty `docs/fuentes/envios-a-meta.md`): `main` read the documents inside its
best effort and each field outside it, and only the answer of a send that matched the chat. So each property reads its
field when it is asked for, and a stored shape that is not an object raises `AttributeError` there, as in `main`.
"""
from __future__ import annotations

from typing import Any, List, Optional, Protocol


class ConversionsApiSend(Protocol):
    @property
    def ctwa_clid(self) -> Optional[str]:
        """`ctwa_clid` of the first event's `user_data`; None when the send has no payload, events or user data."""
        ...

    @property
    def external_id(self) -> Optional[str]:
        """`external_id` of the first event's `user_data` (the sha256 of the chat id); None as `ctwa_clid`."""
        ...

    @property
    def event_type(self) -> Any:
        ...

    @property
    def response_status(self) -> Any:
        ...

    @property
    def created_at(self) -> Any:
        ...

    @property
    def fbtrace_id(self) -> Any:
        """Top level of Meta's answer: a 400 keeps it nested in `error`, so it is None there."""
        ...

    @property
    def events_received(self) -> Any:
        ...

    @property
    def warnings(self) -> List[Any]:
        """Meta's `messages` (warnings it gives even on a 200); `[]` when there are none."""
        ...


class ConversionsApiSendRepository(Protocol):
    async def latest_of_company(self, company_id: str, limit: int) -> List[ConversionsApiSend]:
        """The company's sends (stored with `company_id` as text), newest `created_at` first, `limit` at most."""
        ...
