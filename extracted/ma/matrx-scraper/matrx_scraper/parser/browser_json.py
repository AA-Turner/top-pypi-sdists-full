"""Decode a JSON document displayed in a browser's native preformatted viewer."""
from __future__ import annotations

import json

from bs4 import BeautifulSoup
from pydantic import JsonValue


def decode_browser_json_document(html: str) -> JsonValue:
    """Reject challenge/error HTML instead of treating it as an API response."""
    document = BeautifulSoup(html, "html.parser")
    blocks = document.find_all("pre")
    if len(blocks) != 1:
        raise ValueError("browser did not render one JSON document")
    return json.loads(blocks[0].get_text())
