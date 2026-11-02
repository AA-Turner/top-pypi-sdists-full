"""Scoped dataset transport dependency used by worker materialization."""

from typing import Protocol

from labqoat.json_document import JsonValue
from labqoat.references import AssetRef


class DatasetRequester(Protocol):
    """Supply manifest metadata and bytes only for authorized dataset inputs."""

    def authorize(self, reference: AssetRef) -> None:
        """Recheck live read authority even when the selected file is already cached."""
        ...

    def dataset_request(self, action: str, body: dict[str, JsonValue]) -> object:
        """Execute one pinned manifest or file download request."""
        ...
