"""Products of a company's catalog: the port every product store implements.

The entity is `letschatty.models.company.assets.product.Product`, unchanged: other services (CINTIA,
copilot, products-lambda) import it. Putting a product on a chat is a rule of the chat
(`ChatService.add_product`), not of the catalog.

Every method takes the company; the repository does not filter by it. Per ADR-007, the use case checks
the company with a shared helper (`of_the_company` in api-chatty), and ENG-10 will be fixed there.
"""
from __future__ import annotations

from typing import Any, Dict, List, Protocol

from ...models.company.assets.product import Product
from ...models.utils.types import StrObjectId


class ProductRepository(Protocol):
    """Raises `NotFoundError` when the product does not exist."""

    async def get(self, company_id: StrObjectId, product_id: StrObjectId) -> Product:
        """Also a deleted product (REQ-CRM-111)."""
        ...

    async def list_previews(self, company_id: StrObjectId) -> List[Dict[str, Any]]:
        """Live products of the company, newest first, as JSON-ready preview dicts."""
        ...

    async def add(self, product: Product) -> Product: ...

    async def update(self, company_id: StrObjectId, product_id: StrObjectId, changes: Product) -> Product:
        """Writes only the fields `changes` was built with; the rest stays as stored."""
        ...

    async def delete(self, company_id: StrObjectId, product_id: StrObjectId) -> Product:
        """Marks the product deleted (the document stays) and returns it as it was before."""
        ...
