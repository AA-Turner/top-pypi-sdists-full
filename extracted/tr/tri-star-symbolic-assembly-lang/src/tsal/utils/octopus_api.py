import json
from typing import Dict, Any, Optional

try:  # optional dependency
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback used in CI
    import urllib.request

    class _Response:
        def __init__(self, text: str, status: int = 200) -> None:
            self.text = text
            self.status_code = status

        def json(self) -> Any:
            return json.loads(self.text)

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"status {self.status_code}")

    class requests:
        @staticmethod
        def get(url: str) -> _Response:
            with urllib.request.urlopen(url) as resp:
                text = resp.read().decode()
            return _Response(text, resp.getcode())

BASE = "https://api.octopus.energy/v1/"


def get(endpoint: str) -> Any:
    """Return JSON from Kraken API endpoint."""
    url = BASE + endpoint.lstrip("/")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_products() -> Any:
    """List available products."""
    return get("products/")


def get_electricity_tariffs(product_code: str) -> Any:
    """Return tariffs for a product."""
    return get(f"products/{product_code}/electricity-tariffs/")
