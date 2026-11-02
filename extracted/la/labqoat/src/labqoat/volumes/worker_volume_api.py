"""A mounted volume reached under the run's own worker credentials."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from urllib.parse import quote, urlencode

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.worker.scoped_api import ScopedApi
from labqoat.worker.worker_api_error import WorkerApiError


class WorkerVolumeApi:
    """Volume operations a worker may perform on the volumes its function mounts.

    A mount of the volume's directory ``subpath`` names its paths relative to that directory, as the workload sees
    them; they are named from the volume's root only on the way to the platform.
    """

    def __init__(self, api: ScopedApi, name: str, subpath: str = "") -> None:
        """Address one mounted volume by name, seen from its directory ``subpath`` when the mount names one."""
        self._api = api
        self._base = f"/api/v1/worker/volumes/{quote(name, safe='')}"
        self._subpath = subpath

    def entries(self, path: str = "", recursive: bool = True) -> tuple[int, list[VolumeEntry]]:
        """The volume's version and its entries at or under ``path``; a mounted directory not made yet holds none."""
        if not self._subpath:
            return self._listed(path, recursive)
        try:
            version, entries = self._listed(self._within(path), recursive)
        except WorkerApiError as error:
            if path or error.code != "no_path":
                raise
            return self._listed("", False)[0], []
        prefix = f"{self._subpath}/"
        return version, [
            replace(entry, path=entry.path.removeprefix(prefix)) for entry in entries if entry.path.startswith(prefix)
        ]

    def _listed(self, path: str, recursive: bool) -> tuple[int, list[VolumeEntry]]:
        """The platform's listing at or under ``path`` named from the volume's root."""
        query = urlencode({"path": path, "recursive": "true" if recursive else "false"})
        document = self._api.json("GET", f"{self._base}/entries?{query}")
        items = JsonDocument.expect_list(document["entries"])
        return JsonDocument.expect_scalar(document["version"], int), [
            VolumeEntry.from_dict(JsonDocument.expect_dict(item)) for item in items
        ]

    def uploads(self, blocks: Sequence[Mapping[str, JsonValue]]) -> list[Mapping[str, JsonValue]]:
        """Signed uploads for the blocks storage does not hold."""
        document = self._api.json("POST", f"{self._base}/blocks", {"blocks": [dict(block) for block in blocks]})
        return [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(document["uploads"])]

    def downloads(self, digests: Sequence[str]) -> dict[str, str]:
        """Signed GET URLs for the given blocks."""
        document = self._api.json("POST", f"{self._base}/downloads", {"digests": list(digests)})
        urls = JsonDocument.expect_dict(document["urls"])
        return {digest: JsonDocument.expect_scalar(url, str) for digest, url in urls.items()}

    def commit(self, document: Mapping[str, JsonValue]) -> int:
        """Merge changed and removed paths and return the version made."""
        committed = self._api.json("POST", f"{self._base}/commits", self._placed(document))
        return JsonDocument.expect_scalar(committed["version"], int)

    def _placed(self, document: Mapping[str, JsonValue]) -> Mapping[str, JsonValue]:
        """The commit with every path named from the volume's root."""
        if not self._subpath:
            return document
        placed = dict(document)
        for key in ("entries", "deletions"):
            items = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(document.get(key, []))]
            rows: list[JsonValue] = [
                {**item, "path": self._within(JsonDocument.expect_scalar(item["path"], str))} for item in items
            ]
            placed[key] = rows
        return placed

    def _within(self, path: str) -> str:
        """A path of the mount named from the volume's root."""
        return f"{self._subpath}/{path}" if path else self._subpath
