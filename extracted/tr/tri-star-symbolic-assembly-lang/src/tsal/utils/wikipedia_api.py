import json
from urllib.parse import quote
from typing import Any

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback
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

API = "https://en.wikipedia.org/w/api.php"
REST = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def search(query: str) -> Any:
    """Search Wikipedia."""
    url = f"{API}?action=query&list=search&format=json&srsearch={quote(query)}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def summary(title: str) -> Any:
    """Return page summary."""
    url = REST + quote(title)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
