"""Friendly codes of smart-message sources («códigos amigables»): the port every store of them implements.

A friendly code is a record of its own (collection `friendly_codes`, entity
`letschatty.models.analytics.smart_messages.friendly_code_for_source.FriendlyCodeForSource`, unchanged): four lowercase
letters that stand for one source of a company in a short link (`{base}/{alias}/{code}`). The code ↔ source pair never
changes once written (only the source merger moves a code to the winning source), so a cache may remember it forever.

Every lookup is scoped to the company, compared exactly as stored text (`company_id`, `source_id` and the code). A
lookup that finds several records takes the first one Mongo returns, unsorted.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Protocol

from ...models.analytics.smart_messages.friendly_code_for_source import FriendlyCodeForSource
from ...models.utils.types import StrObjectId


class FriendlyCodeRepository(Protocol):
    async def code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        """The code of the source, remembered or stored; None when it has none."""
        ...

    async def stored_code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        """The code of the source as the store has it now, never a remembered one: the creation that lost a race reads
        the winner's."""
        ...

    async def source_of_code(self, company_id: StrObjectId, code: str) -> Optional[str]:
        """The source id a code stands for, remembered or stored; None when the company has no such code."""
        ...

    async def known_codes(self, company_id: StrObjectId, source_ids: List[str]) -> Dict[str, str]:
        """The codes already remembered for these sources, in one read, without asking the store; a source not in the
        answer goes through `code_of_source`. A store without memory knows none."""
        ...

    async def records_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> List[FriendlyCodeForSource]:
        """Every record of the source, from the store."""
        ...

    async def add(self, record: FriendlyCodeForSource) -> FriendlyCodeForSource:
        """Raises the store's error when a unique index refuses it (its text names the field: `friendly_code` or
        `source_id`)."""
        ...

    async def update(self, record_id: StrObjectId, changes: FriendlyCodeForSource) -> FriendlyCodeForSource:
        """Writes only the fields `changes` was built with, merged onto what is in the store now."""
        ...
