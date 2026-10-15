from __future__ import annotations

from typing import TypedDict
from urllib.parse import quote

from bitfab.http import HttpClient

CATEGORIES_PATH = "/api/sdk/categories"


class CategorySummary(TypedDict):
    id: str
    title: str
    description: str


class Category(CategorySummary):
    organizationId: str
    createdAt: str
    updatedAt: str


class CategoriesClient:
    """Organization-scoped groupings for assertions and scenarios."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def save(
        self,
        title: str,
        *,
        id: str | None = None,
        description: str | None = None,
    ) -> Category:
        """Create or update by ID. Omit description to preserve it, or pass an empty string to clear it."""
        payload: dict[str, object] = {"title": title}
        if id is not None:
            payload["id"] = id
        if description is not None:
            payload["description"] = description
        return self._http_client.request(CATEGORIES_PATH, payload)["category"]

    def get(self, id: str) -> Category:
        """Read one category in the API key's organization."""
        return self._http_client.get(f"{CATEGORIES_PATH}/{quote(id, safe='')}")[
            "category"
        ]

    def list(self) -> list[Category]:
        """List the organization's categories ordered by title."""
        return self._http_client.get(CATEGORIES_PATH)["categories"]

    def delete(self, id: str) -> Category:
        """Delete a category and clear its assignments, preserving assertions, scenarios, and verdicts."""
        return self._http_client.request(
            f"{CATEGORIES_PATH}/{quote(id, safe='')}", {}, method="DELETE"
        )["category"]
