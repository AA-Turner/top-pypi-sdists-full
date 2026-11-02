"""Bounded storage GETs using explicit short-lived URLs without platform credentials."""

import errno
import hashlib
import http.client
import os
import shutil
import sys
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from urllib.parse import urlsplit

from labqoat.argument_codec import decode_result
from labqoat.references import AssetRef
from labqoat.worker.scoped_api import ScopedApi
from labqoat.net.transport_trust import TransportTrust
from labqoat.worker.worker_api_error import WorkerApiError


class DirectAssetDownload:
    """Validate an authorized grant, renew expired grants and verify transfers before publication."""

    ATTEMPTS = 3
    RENEWABLE_STATUSES: frozenset[int | None] = frozenset({None, 400, 403})

    @staticmethod
    def acquire(reference: AssetRef, destination: Path, planner: Callable[[AssetRef], Mapping[str, object]]) -> bool:
        """Return false for proxy plans or transfer exactly one verified descriptor, renewing rejected grants."""
        attempt = 1
        while True:
            url = DirectAssetDownload._url(planner(reference), reference)
            if url is None:
                return False
            started = time.monotonic()
            try:
                DirectAssetDownload._attempt(url, destination, reference)
                return True
            except WorkerApiError as error:
                if (
                    attempt >= DirectAssetDownload.ATTEMPTS
                    or error.status not in DirectAssetDownload.RENEWABLE_STATUSES
                ):
                    raise
                DirectAssetDownload._report(attempt, time.monotonic() - started, error)
            attempt += 1

    @staticmethod
    def _report(attempt: int, seconds: float, error: WorkerApiError) -> None:
        """Leave each retried transfer and its cause in the worker's output; a silent retry hides slow starts."""
        message = f"Storage download attempt {attempt} failed after {seconds:.1f}s and is retried: {error}"
        print(message, file=sys.stderr, flush=True)

    @staticmethod
    def _url(document: Mapping[str, object], reference: AssetRef) -> str | None:
        """Require each fresh plan to describe the same immutable asset before using its grant."""
        identity = {
            "id": document["id"],
            "blob_sha256": document["sha256"],
            "byte_size": document["byte_size"],
            "media_type": document["media_type"],
        }
        if decode_result(identity, AssetRef) != reference:
            raise ValueError("Download plan does not match its immutable asset reference")
        url = document["download_url"]
        if url is not None and not isinstance(url, str):
            raise ValueError("Storage download URL must be a string")
        return url

    @staticmethod
    def _attempt(url: str, destination: Path, reference: AssetRef) -> None:
        """Restart into private staging and publish atomically only after size and digest verification."""
        staging = destination.with_name(f".{destination.name}.part")
        DirectAssetDownload._require_space(destination.parent, reference)
        try:
            DirectAssetDownload._download(url, staging, reference)
            os.replace(staging, destination)
        finally:
            staging.unlink(missing_ok=True)

    @staticmethod
    def _download(url: str, destination: Path, reference: AssetRef) -> None:
        """Never follow redirects or attach application, worker, or invocation credentials."""
        parsed = urlsplit(url)
        endpoint = parsed._replace(path="", query="", fragment="").geturl()
        ScopedApi(endpoint, {}, "/")
        if parsed.fragment or not parsed.path.startswith("/"):
            raise ValueError("Storage download requires an absolute URL without a fragment")
        connection = TransportTrust.connection(parsed.scheme, str(parsed.hostname), parsed.port, timeout=180)
        try:
            path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
            connection.request("GET", path, headers={"Accept-Encoding": "identity"})
            response = connection.getresponse()
            if response.status != 200:
                raise WorkerApiError(f"Storage download returned HTTP {response.status}", response.status)
            DirectAssetDownload._copy(response, destination, reference)
        except OSError as error:
            if error.errno == errno.ENOSPC:
                raise
            raise DirectAssetDownload._failure(parsed.hostname, error) from error
        except http.client.HTTPException as error:
            raise DirectAssetDownload._failure(parsed.hostname, error) from error
        finally:
            connection.close()

    @staticmethod
    def _failure(host: str | None, error: Exception) -> WorkerApiError:
        """Name the storage host and the kind of transport failure, never text that could echo the signed grant."""
        kind = type(error).__name__
        number = getattr(error, "errno", None)
        cause = kind if number is None else f"{kind} {number}"
        return WorkerApiError(f"Storage download failed ({host}: {cause})")

    @staticmethod
    def _require_space(directory: Path, reference: AssetRef) -> None:
        """Fail before transfer, without retries, when the asset cannot fit on the destination volume."""
        free = shutil.disk_usage(directory).free
        if free < reference.byte_size:
            message = f"Asset {reference.id} needs {reference.byte_size} bytes but {directory} has {free} free"
            raise OSError(errno.ENOSPC, message)

    @staticmethod
    def _copy(response: http.client.HTTPResponse, destination: Path, reference: AssetRef) -> None:
        """Bound memory, treat truncation as an interrupted transfer and reject excess or corrupt bytes."""
        received = 0
        digest = hashlib.sha256()
        with destination.open("wb") as output:
            while chunk := response.read(min(1024 * 1024, reference.byte_size - received + 1)):
                received += len(chunk)
                if received > reference.byte_size:
                    raise ValueError("Asset download exceeds its declared byte size")
                digest.update(chunk)
                output.write(chunk)
        if received != reference.byte_size:
            raise http.client.IncompleteRead(b"", reference.byte_size - received)
        if digest.hexdigest() != str(reference.blob_sha256):
            raise ValueError("Asset download does not match its declared sha256")
