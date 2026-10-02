from __future__ import annotations

from typing import TypedDict
from urllib.parse import quote

from bitfab.http import HttpClient

CATEGORIES_PATH = "/api/sdk/assertionCategories"


class AssertionCategorySummary(TypedDict):
    id: str
    title: str
    description: str


class AssertionCategory(AssertionCategorySummary):
    organizationId: str
    createdAt: str
    updatedAt: str


class AssertionCategoriesClient:
    """Organization-scoped groupings for assertions."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def save(
        self,
        title: str,
        *,
        id: str | None = None,
        description: str | None = None,
    ) -> AssertionCategory:
        """Create or update by ID. Omit description to preserve it, or pass an empty string to clear it."""
        payload: dict[str, object] = {"title": title}
        if id is not None:
            payload["id"] = id
        if description is not None:
            payload["description"] = description
        return self._http_client.request(CATEGORIES_PATH, payload)["category"]

    def get(self, id: str) -> AssertionCategory:
        """Read one category in the API key's organization."""
        return self._http_client.get(f"{CATEGORIES_PATH}/{quote(id, safe='')}")[
            "category"
        ]

    def list(self) -> list[AssertionCategory]:
        """List the organization's categories ordered by title."""
        return self._http_client.get(CATEGORIES_PATH)["categories"]

    def delete(self, id: str) -> AssertionCategory:
        """Delete a category and clear its assignments, preserving assertions and verdicts."""
        return self._http_client.request(
            f"{CATEGORIES_PATH}/{quote(id, safe='')}", {}, method="DELETE"
        )["category"]
