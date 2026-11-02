"""Sales registered on a company's chats: the port every sale store implements.

The entity is `letschatty.models.company.assets.sale.Sale`, unchanged: other services (CINTIA, copilot,
analytics, campaigns) import it, and its rules (lines, derived `product_id`, editing with `con_cambios`)
already are pure. Putting a sale on a chat is a rule of the chat (`ChatService.create_sale`).

Every method takes the company; the repository does not filter by it. Per ADR-007, the use case checks
the company with a shared helper (`of_the_company` in api-chatty), and ENG-10 will be fixed there.
"""
from __future__ import annotations

from typing import List, Protocol

from ...models.company.assets.sale import Sale
from ...models.utils.types import StrObjectId


class SaleRepository(Protocol):
    """Raises `NotFoundError` when the sale does not exist."""

    async def get(self, company_id: StrObjectId, sale_id: StrObjectId) -> Sale:
        """Also a deleted sale."""
        ...

    async def find_live_by_crm_id(self, company_id: StrObjectId, crm_id: str, limit: int) -> List[Sale]:
        """Up to `limit` live sales of the company with exactly this order number (never from a cache)."""
        ...

    async def add(self, sale: Sale) -> Sale: ...

    async def save(self, sale: Sale) -> Sale:
        """Writes the fields `sale` was built with (`Sale.con_cambios` keeps track of them) over what is
        stored now; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, sale_id: StrObjectId) -> None:
        """Marks the sale deleted; the document stays."""
        ...
