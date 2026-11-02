"""Filter criteria («casos» of the AI agents): the port every filter-criteria store implements.

The entity is `letschatty.models.company.assets.filter_criteria.FilterCriteria`, unchanged: CINTIA writes the
same documents straight to Mongo. Matching a chat against criteria is `services.filter_criteria_service`.

Every method takes the company; the repository does not filter by it. Per ADR-007, the use case checks
the company with a shared helper (`of_the_company` in api-chatty), and ENG-10 will be fixed there.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ...models.company.assets.filter_criteria import FilterCriteria
from ...models.utils.types import StrObjectId


class FilterCriteriaRepository(Protocol):
    """Raises `NotFoundError` when the filter criteria does not exist."""

    async def get(self, company_id: StrObjectId, filter_criteria_id: StrObjectId) -> FilterCriteria: ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live filter criteria of the company, global or not, as JSON-ready preview dicts."""
        ...

    async def add(self, filter_criteria: FilterCriteria) -> FilterCriteria: ...

    async def update(self, company_id: StrObjectId, filter_criteria_id: StrObjectId,
                     changes: FilterCriteria) -> FilterCriteria:
        """Writes only the fields `changes` was built with; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, filter_criteria_id: StrObjectId) -> FilterCriteria:
        """Marks it deleted (the document stays) and returns it as it was before."""
        ...
