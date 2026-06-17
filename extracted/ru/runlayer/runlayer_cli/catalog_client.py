"""MCP catalog client surface, split out of ``api.py``.

Keeps the catalog models + the single ``GET /api/v1/catalog/`` call in one
small module instead of growing the already-large shared ``api.py``.
``RunlayerClient`` mixes in :class:`CatalogClientMixin`, so callers still use
``client.list_catalog_connectors()`` (thin delegate, no behavior change).

Raw ``_meta`` is preserved on :class:`CatalogConnector`; flattening lives in
``runlayer_cli.catalog_enrichment`` so meta parsing has one home.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
from pydantic import BaseModel, ConfigDict, Field

_CATALOG_API_TIMEOUT = 30.0


class CatalogResponseError(RuntimeError):
    """Raised when the catalog endpoint returns an unexpected response shape."""


class CatalogTransport(BaseModel):
    """Transport block nested under a catalog package."""

    model_config = ConfigDict(populate_by_name=True)

    type: str | None = None
    url: str | None = None


class CatalogPackage(BaseModel):
    """Installable package entry on a catalog connector."""

    model_config = ConfigDict(populate_by_name=True)

    identifier: str | None = None
    registry_type: str | None = Field(default=None, validation_alias="registryType")
    transport: CatalogTransport | None = None


class CatalogRemote(BaseModel):
    """Remote endpoint entry on a catalog connector."""

    model_config = ConfigDict(populate_by_name=True)

    type: str | None = None
    url: str | None = None


class CatalogConnector(BaseModel):
    """Raw MCP catalog connector entry for CLI display.

    `meta` keeps the raw `_meta` blob untouched; flattened/derived fields
    (deployment mode, beta, transports, oauth vendor, ...) are produced once by
    ``runlayer_cli.catalog_enrichment.enrich_connector`` so meta parsing lives in
    a single place that mirrors the backend ``_catalog_entry_helpers``.
    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    title: str | None = None
    description: str | None = None
    version: str | None = None
    status: str | None = None
    packages: list[CatalogPackage] = []
    remotes: list[CatalogRemote] = []
    repository: dict[str, Any] | None = None
    website_url: str | None = Field(default=None, validation_alias="websiteUrl")
    mcp_fingerprint: str | None = Field(default=None, validation_alias="mcpFingerprint")
    version_fingerprint: str | None = Field(
        default=None, validation_alias="versionFingerprint"
    )
    meta: dict[str, Any] = Field(default_factory=dict, validation_alias="_meta")


class CatalogClientMixin:
    """Catalog reads for ``RunlayerClient`` (the host supplies the HTTP plumbing)."""

    if TYPE_CHECKING:
        base_url: str

        def _client(self, **kwargs: Any) -> httpx.Client: ...

        def _get_with_retries(
            self,
            client: httpx.Client,
            url: str,
            *,
            params: dict[str, Any] | None = None,
        ) -> httpx.Response: ...

    def list_catalog_connectors(self) -> list[CatalogConnector]:
        """List installable MCP catalog connectors."""
        with self._client(timeout=_CATALOG_API_TIMEOUT) as client:
            response = self._get_with_retries(
                client,
                f"{self.base_url}/api/v1/catalog/",
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise CatalogResponseError(
                    "Expected a JSON array from /api/v1/catalog/, got "
                    f"{type(data).__name__}"
                )
            return [CatalogConnector.model_validate(item) for item in data]
