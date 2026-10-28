"""Thin adapter over the reused ``storage`` package.

Storage is the one piece the new client reuses as-is (SDK_REDESIGN.md §5.1): the
existing ``StorageApi`` (upload via ``create_revision``, download via
``read_contents``). This adapter gives the facade a small surface over it plus the
``TokenDto`` → ``Token`` conversion the read path needs.

Storage calls do not go through ``_Manager._call``, so this adapter is their error
boundary: it maps generated ``OpenApiException`` (HTTP errors), raw urllib3
transport failures, and storage's own ``ValueError`` (content-hash mismatch /
malformed response) into the ``IstariError`` hierarchy — so callers of
``read_bytes``/``create`` never catch a generated or raw exception.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Callable, TypeVar

import urllib3.exceptions

from istari_digital_client._transfer.errors import (
    MultipartUploadRestartRequiredError,
    TransferError,
)
from istari_digital_client._transfer.events import TransferEvent
from istari_digital_client.sdk._exceptions import (
    APIConnectionError,
    IstariError,
    OpenApiException,
    TransferRetriesExhaustedError,
    map_api_error,
)
from istari_digital_client.sdk._generated.storage_api.api.storage_api import StorageApi
from istari_digital_client.sdk._storage.token import Token

_T = TypeVar("_T")


def _guard(fn: Callable[[], _T], *, token: Token | None = None) -> _T:
    """Run a storage call, mapping its failures into the ``IstariError`` hierarchy."""
    try:
        return fn()
    except OpenApiException as exc:
        error = map_api_error(exc)
        if isinstance(error, TransferRetriesExhaustedError) and error.token is None:
            error.token = token
        raise error from exc
    except urllib3.exceptions.HTTPError as exc:
        raise APIConnectionError(str(exc)) from exc
    except MultipartUploadRestartRequiredError:
        # This terminal completion condition has one public catchable identity.
        raise
    except TransferError as exc:
        # terminal local transfer conditions (cancelled, file changed mid-upload,
        # no valid part plan) — not ValueErrors, so map them explicitly.
        raise IstariError(str(exc)) from exc
    except ValueError as exc:
        # storage raises ValueError on content-hash mismatch and malformed
        # upload/download responses — surface as IstariError, not a bare ValueError.
        raise IstariError(str(exc)) from exc


class StorageHelper:
    """Facade-side handle over the reused ``StorageApi``."""

    def __init__(self, storage_api: StorageApi) -> None:
        """Wrap a configured ``StorageApi`` instance."""
        self._api = storage_api

    def upload(
        self,
        path: str | Path,
        *,
        display_name: str | None = None,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        salt: str | None = None,
        progress: Callable[[TransferEvent], None] | None = None,
        cancel: threading.Event | None = None,
    ) -> Any:
        """Upload a local file and return the resulting ``FileRevision`` (name + tokens).

        ``salt`` keeps an interrupted multipart upload resumable across the caller's
        own retries; ``progress`` and ``cancel`` are optional per-call transfer hooks.
        """
        return _guard(
            lambda: self._api.create_revision(
                file_path=path,
                display_name=display_name,
                description=description,
                version_name=version_name,
                external_identifier=external_identifier,
                salt=salt,
                progress=progress,
                cancel=cancel,
            )
        )

    @staticmethod
    def _token(token_dto: Any) -> Token:
        return Token(
            id=token_dto.id,
            sha=token_dto.sha,
            salt=token_dto.salt,
            created=token_dto.created,
        )

    def read_contents(self, token_dto: Any) -> bytes:
        """Download and return the raw content bytes for a ``TokenDto`` (verified inline)."""
        token = self._token(token_dto)
        return _guard(lambda: self._api.read_contents(token=token), token=token)

    def download_to(
        self,
        token_dto: Any,
        dest: str | Path,
        *,
        progress: Callable[[TransferEvent], None] | None = None,
        cancel: threading.Event | None = None,
    ) -> Path:
        """Download verified content via a temp file and return the destination.

        Retry an exhausted download with the original content and destination; its
        token is content context, not an upload-resume salt workflow.
        """
        token = self._token(token_dto)
        return _guard(
            lambda: self._api.download_to(token, Path(dest), progress=progress, cancel=cancel),
            token=token,
        )
