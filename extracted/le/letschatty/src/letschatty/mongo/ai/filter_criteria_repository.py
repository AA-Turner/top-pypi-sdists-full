"""`FilterCriteriaRepository` on the `filter_criterias` collection: a simple catalog (`MongoCatalogWithPreviews`)."""
from __future__ import annotations

from typing import Any, Dict

from ...models.company.assets.filter_criteria import FilterCriteria, FilterCriteriaPreview
from ...services.chatty_assets.collections.filter_criteria_collection import FilterCriteriaCollection
from ..catalog_repository import MongoCatalogWithPreviews


class MongoFilterCriteriaRepository(MongoCatalogWithPreviews[FilterCriteria]):
    """Reuses `FilterCriteriaCollection`, so the stored document has exactly the shape CINTIA reads and writes."""

    collection: FilterCriteriaCollection

    def preview_projection(self) -> Dict[str, Any]:
        return FilterCriteriaPreview.get_projection()
