"""A project's volume reached under a person's credentials."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.volumes.volume_entry import VolumeEntry

if TYPE_CHECKING:
    from labqoat.base_client import BaseClient


class ClientVolumeApi:
    """Volume operations through the management API of the client's selected project."""

    def __init__(self, client: BaseClient, name: str) -> None:
        """Address one volume of the selected project by name."""
        self._client = client
        self._base = f"/api/v1/volumes/{client.encode_ref(name)}"

    def entries(self, path: str = "", recursive: bool = True) -> tuple[int, list[VolumeEntry]]:
        """The volume's version and its entries at or under ``path``."""
        query = urlencode({"path": path, "recursive": "true" if recursive else "false"})
        document = self._document(self._client.send("GET", f"{self._base}/entries?{query}").text)
        items = JsonDocument.expect_list(document["entries"])
        return JsonDocument.expect_scalar(document["version"], int), [
            VolumeEntry.from_dict(JsonDocument.expect_dict(item)) for item in items
        ]

    def uploads(self, blocks: Sequence[Mapping[str, JsonValue]]) -> list[Mapping[str, JsonValue]]:
        """Signed uploads for the blocks storage does not hold."""
        requested: list[JsonValue] = [dict(block) for block in blocks]
        response = self._client.send_json("POST", f"{self._base}/blocks", {"blocks": requested})
        return [
            JsonDocument.expect_dict(item)
            for item in JsonDocument.expect_list(self._document(response.text)["uploads"])
        ]

    def downloads(self, digests: Sequence[str]) -> dict[str, str]:
        """Signed GET URLs for the given blocks."""
        requested: list[JsonValue] = list(digests)
        response = self._client.send_json("POST", f"{self._base}/downloads", {"digests": requested})
        urls = JsonDocument.expect_dict(self._document(response.text)["urls"])
        return {digest: JsonDocument.expect_scalar(url, str) for digest, url in urls.items()}

    def commit(self, document: Mapping[str, JsonValue]) -> int:
        """Merge changed and removed paths and return the version made."""
        response = self._client.send_json("POST", f"{self._base}/commits", document)
        return JsonDocument.expect_scalar(self._document(response.text)["version"], int)

    @staticmethod
    def _document(text: str) -> JsonDocument:
        """Decode one JSON object response."""
        return JsonDocument.expect_dict(json.loads(text))
