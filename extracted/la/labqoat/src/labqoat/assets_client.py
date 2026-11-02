"""Verified asset transfer client."""

from __future__ import annotations

import hashlib
import mimetypes
import os
import tempfile
from collections.abc import Iterator, Mapping
from pathlib import Path

from labqoat._generated.asset_record import AssetRecord
from labqoat._generated.asset_record_page import AssetRecordPage
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.references import AssetRef, ResourceId, Sha256


class AssetsClient(BaseClient):
    """Single and batch asset registration with verified bytes."""

    _CHUNK_SIZE = 1024 * 1024
    _FILE_ATTEMPTS = 3

    def upload(self, path: Path, *, media_type: str | None = None) -> AssetRef:
        """Upload verified file bytes and return an immutable handle suitable for typed compute arguments."""
        record = self.upload_file(path, media_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream")
        return AssetRef(
            id=ResourceId.parse(record.id),
            blob_sha256=Sha256(record.sha256),
            byte_size=record.byte_size,
            media_type=record.media_type,
        )

    def register(
        self,
        sha: str,
        byte_size: int,
        media_type: str,
        extra: Mapping[str, JsonValue] | None = None,
        *,
        key: str | None = None,
    ) -> AssetRecord:
        """Register an asset identity."""
        payload: dict[str, JsonValue] = {"sha256": sha, "byte_size": byte_size, "media_type": media_type}
        if extra:
            payload.update(extra)
        path = "/api/v1/asset-records" if key is None else f"/api/v1/asset-records?operation_key={self.encode_ref(key)}"
        response = self.send_json("POST", path, payload)
        return self.decode(response, "/api/v1/asset-records", AssetRecord.from_dict)

    def upload_bytes(self, ref: str, data: bytes) -> None:
        """Upload raw bytes for a pending asset."""
        path = f"/api/v1/asset-records/item/content?ref={BaseClient.encode_ref(ref)}"
        self.send_content("PUT", path, data, "application/octet-stream")

    def upload_stream(self, ref: str, chunks: Iterator[bytes], byte_size: int | None = None) -> None:
        """Upload raw byte chunks for a pending asset."""
        path = f"/api/v1/asset-records/item/content?ref={BaseClient.encode_ref(ref)}"
        self.send_content("PUT", path, chunks, "application/octet-stream", content_length=byte_size)

    def upload_path(self, ref: str, path: Path, byte_size: int, attempt: int = 1) -> None:
        """Send a file's bytes for a pending asset, reading the file afresh after an attempt that stalled.

        A connection that pauses for a minute makes the service give up on the body (408), and a dropped one
        loses it; a streamed body cannot be replayed, but the file can be read again.
        """
        try:
            self.upload_stream(ref, AssetsClient.file_chunks(path), byte_size)
        except ApiError as error:
            if attempt >= AssetsClient._FILE_ATTEMPTS or not AssetsClient._stalled(error):
                raise
            self.upload_path(ref, path, byte_size, attempt + 1)

    @staticmethod
    def _stalled(error: ApiError) -> bool:
        """Whether an upload failed because its bytes stopped arriving rather than because they were refused."""
        return isinstance(error, TransportError) or error.status == 408

    def complete(self, ref: str) -> AssetRecord:
        """Complete verification for an uploaded asset."""
        path = f"/api/v1/asset-records/item/complete?ref={BaseClient.encode_ref(ref)}"
        response = self.send_json("POST", path, {})
        return self.decode(response, path, AssetRecord.from_dict)

    def upload_file(
        self, path: Path, media_type: str = "application/octet-stream", *, key: str | None = None
    ) -> AssetRecord:
        """Hash, register, transfer, and verify one file."""
        sha, byte_size = AssetsClient.hash_file(path)
        record = self.register(sha, byte_size, media_type, key=key)
        if key is not None:
            record = self.get(record.id)
        if getattr(record, "availability", "available") != "available":
            self.upload_path(f"sha256:{sha}", path, byte_size)
            record = self.complete(f"sha256:{sha}")
        return record

    def download(self, ref: str) -> bytes:
        """Download verified bytes."""
        path = f"/api/v1/asset-records/item/download?ref={BaseClient.encode_ref(ref)}"
        return self.send("GET", path).content

    def download_plan(self, ref: str) -> JsonDocument:
        """Authorize a short-lived direct storage URL or select the proxy byte endpoint."""
        path = f"/api/v1/asset-records/item/transfer?ref={BaseClient.encode_ref(ref)}"
        return JsonDocument.expect_dict(self.send("GET", path).json())

    def download_to(self, ref: str, destination: Path) -> int:
        """Download, verify, and atomically replace one destination file."""
        from labqoat.storage.client_asset_source import ClientAssetSource

        record = self.get(ref)
        reference = AssetRef(
            id=ResourceId.parse(record.id),
            blob_sha256=Sha256(record.sha256),
            byte_size=record.byte_size,
            media_type=record.media_type,
        )
        descriptor, temporary = AssetsClient.temporary_file(destination)
        os.close(descriptor)
        try:
            ClientAssetSource(self).download_to(reference, temporary)
            digest, byte_size = self.hash_file(temporary)
            if digest != record.sha256 or byte_size != record.byte_size:
                raise ApiError("downloaded asset checksum does not match its catalog record")
            with temporary.open("rb") as received:
                os.fsync(received.fileno())
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
        return byte_size

    def download_chunks(self, ref: str) -> Iterator[bytes]:
        """Yield verified endpoint bytes without whole-response buffering."""
        path = f"/api/v1/asset-records/item/download?ref={BaseClient.encode_ref(ref)}"
        with self.stream_response("GET", path) as response:
            yield from response.iter_bytes()

    @staticmethod
    def hash_file(path: Path) -> tuple[str, int]:
        """Hash one file incrementally and return its size."""
        digest = hashlib.sha256()
        byte_size = 0
        for chunk in AssetsClient.file_chunks(path):
            digest.update(chunk)
            byte_size += len(chunk)
        return digest.hexdigest(), byte_size

    @staticmethod
    def file_chunks(path: Path) -> Iterator[bytes]:
        """Yield bounded chunks from one local file."""
        with path.open("rb") as stream:
            while chunk := stream.read(AssetsClient._CHUNK_SIZE):
                yield chunk

    @staticmethod
    def temporary_file(destination: Path) -> tuple[int, Path]:
        """Create and retain an open private unpredictable sibling file."""
        descriptor, name = tempfile.mkstemp(
            prefix=f".{destination.name}.",
            suffix=".labqoat-download",
            dir=destination.parent,
        )
        return descriptor, Path(name)

    def get(self, ref: str) -> AssetRecord:
        """Read one asset record."""
        path = f"/api/v1/asset-records/item?ref={BaseClient.encode_ref(ref)}"
        return self.decode(self.send("GET", path), path, AssetRecord.from_dict)

    def resolve(self, ref: str) -> AssetRef:
        """Resolve an available asset ID or content digest into an immutable compute input."""
        record = self.get(ref)
        if record.availability != "available":
            raise ApiError("Asset is not available")
        if ref not in (record.id, f"sha256:{record.sha256}"):
            raise ApiError("Resolved asset identity mismatch")
        return AssetRef(
            id=ResourceId.parse(record.id),
            blob_sha256=Sha256.parse(record.sha256),
            byte_size=record.byte_size,
            media_type=record.media_type,
        )

    def list_page(self, limit: int = 20, cursor: str | None = None) -> AssetRecordPage:
        """Read one bounded page."""
        path = f"/api/v1/asset-records?limit={limit}"
        if cursor is not None:
            path += f"&cursor={BaseClient.encode_ref(cursor)}"
        return self.decode(self.send("GET", path), path, AssetRecordPage.from_dict)
