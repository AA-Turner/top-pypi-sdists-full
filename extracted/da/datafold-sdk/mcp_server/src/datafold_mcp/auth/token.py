"""Token-based authentication for Datafold API."""

from dataclasses import dataclass

import httpx


@dataclass
class DatafoldAuth:
    """Datafold API key authentication handler."""

    api_key: str

    @property
    def headers(self) -> dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
        }

    def apply_to_client(self, client: httpx.AsyncClient) -> None:
        """Apply authentication to an httpx client."""
        client.headers.update(self.headers)
