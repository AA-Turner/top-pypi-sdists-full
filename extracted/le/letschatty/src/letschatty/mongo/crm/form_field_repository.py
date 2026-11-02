"""`FormFieldRepository` on the `form_fields` collection. A simple catalog; only Mongo: the cache is a decorator (ADR-001)."""
from __future__ import annotations

from ...models.company.form_field import FormField
from ...models.utils.types import StrObjectId
from ...services.chatty_assets.collections.form_field_collection import FormFieldCollection
from ..catalog_repository import MongoCatalogRepository


class MongoFormFieldRepository(MongoCatalogRepository[FormField]):
    """Reuses `FormFieldCollection`, so the stored document has exactly the shape CINTIA reads. A simple catalog
    (`MongoCatalogRepository`) listed whole, plus the customizations of the system fields."""

    collection: FormFieldCollection

    async def add_customization(self, customization: FormField) -> None:
        await self.collection.insert(customization)

    async def replace_customization(self, customization: FormField) -> None:
        await self.collection.update(customization)

    async def remove_customization(self, company_id: StrObjectId, customization_id: StrObjectId) -> None:
        # ENG-61: `delete` takes `doc_id`, so this raises TypeError and nothing is removed. Kept as it was.
        await self.collection.delete(id=customization_id)
