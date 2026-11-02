"""`FriendlyCodeRepository` on the `friendly_codes` collection. Only Mongo: the cache is a decorator (ADR-001).

Not a catalog (ADR-010 of api-chatty): a code is looked up by its source or by its text, never listed nor deleted.
Each lookup runs the asset service's `get_by_query` (`collection.get_docs(query, company_id)`), unchanged."""
from __future__ import annotations

from typing import Dict, List, Optional

from ...models.analytics.smart_messages.friendly_code_for_source import FriendlyCodeForSource
from ...models.utils.types import StrObjectId


class MongoFriendlyCodeRepository:
    """Reuses the asset collection of the legacy service, so the stored document keeps its shape."""

    def __init__(self, collection):
        self.collection = collection

    async def records_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> List[FriendlyCodeForSource]:
        return await self.collection.get_docs(query={"source_id": source_id}, company_id=company_id)

    async def code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        records = await self.records_of_source(company_id, source_id)
        return records[0].friendly_code if records else None

    async def stored_code_of_source(self, company_id: StrObjectId, source_id: StrObjectId) -> Optional[str]:
        return await self.code_of_source(company_id, source_id)

    async def source_of_code(self, company_id: StrObjectId, code: str) -> Optional[str]:
        records = await self.collection.get_docs(query={"friendly_code": code}, company_id=company_id)
        return str(records[0].source_id) if records else None

    async def known_codes(self, company_id: StrObjectId, source_ids: List[str]) -> Dict[str, str]:
        return {}

    async def add(self, record: FriendlyCodeForSource) -> FriendlyCodeForSource:
        await self.collection.insert(record)
        return record

    async def update(self, record_id: StrObjectId, changes: FriendlyCodeForSource) -> FriendlyCodeForSource:
        # The asset service's `update`: merged onto Mongo now, writing only what was sent.
        existing = await self.collection.get_by_id(record_id)
        merged, sent_fields = existing.merge(changes)
        await self.collection.update_fields(merged, sent_fields)
        return merged
