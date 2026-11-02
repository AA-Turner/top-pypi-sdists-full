"""`MetaTemplateRepository` on the `meta_templates` collection: a simple catalog (`MongoCatalogWithPreviews`) plus the
reads by Meta's id, the duplicate key as `MetaTemplateKeyTaken` and the move to another WABA."""
from __future__ import annotations

from typing import Any, Dict, Optional

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from ...domain.messaging.meta_templates import MetaTemplateKeyTaken
from ...models.messages.message_templates.meta_template import MetaTemplate
from ...models.utils.types import StrObjectId
from ..catalog_repository import MongoCatalogWithPreviews


class MongoMetaTemplateRepository(MongoCatalogWithPreviews[MetaTemplate]):
    """Reuses the asset collection of the legacy `MetaTemplates` service, so the stored document keeps exactly the
    shape (and the types: `last_synced_at` as a string) the lambdas read."""

    def preview_projection(self) -> Dict[str, Any]:
        return MetaTemplate.preview_class.get_projection()

    async def add(self, item: MetaTemplate) -> MetaTemplate:
        # The module's own: Mongo's duplicate key is a domain fact for the use case, not a driver error.
        try:
            return await super().add(item)
        except DuplicateKeyError as exc:
            raise MetaTemplateKeyTaken(item.company_id, item.meta_template_id) from exc

    async def get_live(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        rows = await self.collection.get_docs(
            query={"meta_template_id": meta_template_id, "deleted_at": None}, company_id=company_id)
        return rows[0] if rows else None

    async def get_any(self, company_id: StrObjectId, meta_template_id: str) -> Optional[MetaTemplate]:
        rows = await self.collection.get_docs(query={"meta_template_id": meta_template_id}, company_id=company_id)
        return rows[0] if rows else None

    async def move_to_waba(self, template_id: StrObjectId, waba_id: str) -> None:
        row_id = ObjectId(template_id) if ObjectId.is_valid(str(template_id)) else template_id
        await self.collection.collection.update_one({"_id": row_id}, {"$set": {"waba_id": waba_id}})
