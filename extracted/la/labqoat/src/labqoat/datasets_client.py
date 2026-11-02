"""Dataset repository, immutable publication, revision and tag client."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TypeVar

from labqoat._generated.dataset_publication import DatasetPublication
from labqoat._generated.dataset_import import DatasetImport
from labqoat._generated.dataset_import_event import DatasetImportEvent
from labqoat._generated.hugging_face_source import HuggingFaceSource
from labqoat._generated.hugging_face_preview import HuggingFacePreview
from labqoat._generated.new_dataset_import import NewDatasetImport
from labqoat._generated.dataset_publication_event import DatasetPublicationEvent
from labqoat._generated.dataset_repository import DatasetRepository
from labqoat._generated.dataset_revision_files import DatasetRevisionFiles
from labqoat._generated.dataset_tag import DatasetTag
from labqoat.base_client import BaseClient
from labqoat.compute.published_dataset import PublishedDataset
from labqoat.dataset import Dataset
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument
from labqoat.sse_client import SseClient

T = TypeVar("T")


class DatasetsClient(BaseClient):
    """Dataset publication and inspection."""

    def preview_hugging_face(self, source: HuggingFaceSource) -> HuggingFacePreview:
        """Resolve a public source and inspect an advisory sample without creating a dataset."""
        path = "/api/v1/dataset-imports/huggingface/preview"
        return self.decode(self.send_json("POST", path, source.to_dict()), path, HuggingFacePreview.from_dict)

    def import_hugging_face(self, request: NewDatasetImport, *, idempotency_key: str) -> DatasetImport:
        """Durably accept a source selection for backend-owned download and publication."""
        path = "/api/v1/dataset-imports"
        response = self.send_json("POST", path, request.to_dict(), idempotency_key=idempotency_key)
        return self.decode(response, path, DatasetImport.from_dict)

    def get_import(self, import_id: str) -> DatasetImport:
        """Read retained source identity, failure evidence and resulting revision."""
        path = f"/api/v1/dataset-imports/{BaseClient.encode_ref(import_id)}"
        return self.decode(self.send("GET", path), path, DatasetImport.from_dict)

    def import_events(self, import_id: str) -> Iterator[DatasetImportEvent]:
        """Wait for durable preparation completion before following revision publication."""
        path = f"/api/v1/dataset-imports/{BaseClient.encode_ref(import_id)}/events"
        with self.stream_response("GET", path, event_stream=True) as response:
            for event in SseClient.parse_events(response.iter_bytes()):
                try:
                    yield DatasetImportEvent.from_dict(event)
                except (KeyError, TypeError, ValueError) as error:
                    raise ApiError("Malformed import event.") from error

    def wait_import(self, import_id: str, *, max_reconnects: int = 5) -> DatasetPublication:
        """Follow import handoff then the existing publication stream through ready or failure."""
        from labqoat.datasets.import_waiter import ImportWaiter

        return ImportWaiter(self, import_id, max_reconnects).run()

    def create_repository(self, name: str) -> DatasetRepository:
        """Create a repository."""
        response = self.send_json("POST", "/api/v1/dataset-repositories", {"name": name})
        return self.decode(response, "/api/v1/dataset-repositories", DatasetRepository.from_dict)

    def get_revision(self, revision_id: str) -> DatasetPublication:
        """Read immutable captured identity and current publication progress."""
        path = f"/api/v1/dataset-revisions/{BaseClient.encode_ref(revision_id)}"
        return self.decode(self.send("GET", path), path, DatasetPublication.from_dict)

    def resolve(self, ref: str, *, row_type: type[T]) -> Dataset[T]:
        """Resolve a mutable name once and bind the exact ready revision to its declared row type."""
        path = f"/api/v1/datasets/resolve?ref={BaseClient.encode_ref(ref)}"
        publication = self.decode(self.send("GET", path), path, DatasetPublication.from_dict)
        return PublishedDataset.capture(publication, row_type)

    def events(
        self, revision_id: str, *, cursor: str | None = None, follow: bool = True
    ) -> Iterator[DatasetPublicationEvent]:
        """Replay retained publication events and follow commit-driven progress."""
        path = f"/api/v1/dataset-revisions/{BaseClient.encode_ref(revision_id)}/events?follow={str(follow).lower()}"
        if cursor is not None:
            path += f"&cursor={BaseClient.encode_ref(cursor)}"
        with self.stream_response("GET", path, event_stream=True) as response:
            for event in SseClient.parse_events(response.iter_bytes()):
                try:
                    yield DatasetPublicationEvent.from_dict(event)
                except (KeyError, TypeError, ValueError) as error:
                    raise ApiError("Malformed publication event.") from error

    def wait(self, revision_id: str, *, max_reconnects: int = 5) -> DatasetPublication:
        """Follow terminal publication evidence and reread authoritative state."""
        from labqoat.datasets.publication_waiter import PublicationWaiter

        return PublicationWaiter(self, revision_id, max_reconnects).run()

    def revision_files(self, ref: str) -> DatasetRevisionFiles:
        """Resolve ready output files with immutable manifest and layout identities."""
        path = f"/api/v1/dataset-revisions/files?ref={BaseClient.encode_ref(ref)}"
        return self.decode(self.send("GET", path), path, DatasetRevisionFiles.from_dict)

    def create_tag(self, repository_ref: str, tag: str, revision_ref: str) -> DatasetTag:
        """Create an immutable tag."""
        payload = {"repository_ref": repository_ref, "tag": tag, "revision_ref": revision_ref}
        response = self.send_json("POST", "/api/v1/dataset-tags", payload)
        return self.decode(response, "/api/v1/dataset-tags", DatasetTag.from_dict)

    def delete_revision(self, ref: str) -> JsonDocument:
        """Delete an eligible revision."""
        path = f"/api/v1/dataset-revisions/item?ref={BaseClient.encode_ref(ref)}"
        return JsonDocument.expect_dict(self.send("DELETE", path).json())
