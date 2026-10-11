"""
Site Backups API operations for DealCloud.

The API provides four operations (per swagger):
- request_backup: POST /api/rest/v4/backups/request
- list_backups: GET /api/rest/v4/backups (items have name, link per GetBackupsResponse)
- download_backup: primary use is ``download_link`` (blob/SAS URL); optional ``file_name`` for
  list lookup or GET /api/rest/v4/backups/{fileName} when no link is supplied
- delete_backup: POST /api/rest/v4/backups/delete/{fileName}

Backup identifier is the backup file name (API: fileName).
On failure, plain-text error responses are normalized to a dict on ``HttpError.response_body``
(see ``dealcloud_sdk.http.DealCloudRestClient``).
See: https://api.docs.dealcloud.com/docs - Site Backups API
"""

from typing import Any, Callable, List, Optional

from ..publications.dealcloud_publications import DealCloudPublications
from ..storage import StreamingStorageBackend


def _backup_rows_from_list_response(raw: Any) -> List[dict]:
    """
    Normalize GET /backups ApiResult (or a bare list) to ``{"name", "link"}`` dicts.

    Strips the ApiResult envelope; drops extra per-row keys. Rows missing ``name`` or
    ``link`` are omitted.
    """
    if raw is None:
        return []
    rows: List[dict] = []
    if isinstance(raw, list):
        rows = [r for r in raw if isinstance(r, dict)]
    elif isinstance(raw, dict):
        model = raw.get("model")
        if isinstance(model, list):
            rows = [r for r in model if isinstance(r, dict)]
    else:
        return []

    keys = ("name", "link")
    out: List[dict] = []
    for r in rows:
        item = {k: r.get(k) for k in keys}
        if item["name"] is None or item["link"] is None:
            continue
        out.append(item)
    return out


class DealCloudBackups(DealCloudPublications):
    """
    Site Backups API operations. Exposes the four swagger operations:
    request_backup, list_backups, download_backup, delete_backup.
    """

    @property
    def backups_url(self) -> str:
        """
        Backups API base URL (e.g. https://site.dealcloud.com/api/rest/v4/backups).
        Use for custom backup API calls not covered by SDK methods.
        """
        return self._backups_url

    # =========================================================================
    # Backup creation
    # =========================================================================

    def request_backup(
        self,
        ids: Optional[List[int]] = None,
        api_names: Optional[List[str]] = None,
    ) -> dict:
        """
        Request a new site backup.

        API: POST /api/rest/v4/backups/request. Body is BackupRequestVm (ids, apiNames only).

        Args:
            ids: Optional list of object IDs to include.
            api_names: Optional list of object apiNames (e.g. ["Company", "Contact"]).
                Some sites require at least one of ``ids`` or ``api_names``; otherwise
                the API may return 400 (e.g. "select at least one list or binary").

        Returns:
            Response from POST (e.g. 204 No Content; server may return body with backupId).

        Note:
            Uses ``post_no_retry429`` so HTTP 429 (e.g. daily backup quota) is not
            retried by the transport; other retryable statuses keep normal behavior.
        """
        url = f"{self._backups_url}/request"
        payload = {}
        if ids is not None:
            payload["ids"] = ids
        if api_names is not None:
            payload["apiNames"] = api_names
        return self._client.post_no_retry429(url, json=payload)

    # =========================================================================
    # List backups
    # =========================================================================

    def list_backups(self) -> List[dict]:
        """
        List available backups.

        API: GET /api/rest/v4/backups. The wire format is ApiResult JSON with a ``model``
        array of GetBackupsResponse rows (``name``, ``link``) plus ``statusCode`` / ``message``.
        This method strips the envelope and returns a plain list of ``{"name", "link"}``
        dicts only.

        Swagger does not define any query parameters for this endpoint.

        Returns:
            List of ``{"name": str, "link": str}`` items (no ``statusCode`` / ``message``).
        """
        raw = self._client.get(self._backups_url)
        return _backup_rows_from_list_response(raw)

    # =========================================================================
    # Download backup
    # =========================================================================

    def download_backup(
        self,
        output_path: Optional[str] = None,
        file_name: Optional[str] = None,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
        *,
        download_link: Optional[str] = None,
        storage: Optional[StreamingStorageBackend] = None,
        relative_path: Optional[str] = None,
        content_type: str = "application/zip",
    ) -> str:
        """
        Download a backup file (streaming).

        Pass ``download_link`` for a direct blob/SAS URL (typical case): OAuth is skipped so
        the SAS query string stays authoritative. ``file_name`` is optional in that case.

        Without ``download_link``, ``file_name`` is required: the method resolves an ``http(s)``
        ``link`` from ``list_backups()`` for that name, or falls back to
        GET /api/rest/v4/backups/{fileName}.

        Destination: either ``output_path`` (fsspec URI or local path) **or**
        ``storage`` + ``relative_path`` for pluggable streaming storage.

        Args:
            output_path: Path or URI to save the file (fsspec). Required if ``storage`` is omitted.
            file_name: Backup file name (API: fileName). Required when ``download_link`` is
                omitted.
            progress_callback: Optional; invoked while streaming (SDK ``download_file`` / ``_download_file_to_stream``).
            download_link: Absolute ``http`` or ``https`` URL (e.g. SAS); skips list lookup.
            storage: Optional ``StreamingStorageBackend`` (e.g. ``LocalStorage``, ``FsspecStreamingStorage``).
            relative_path: Key within ``storage``; required when ``storage`` is set.
            content_type: MIME type passed to ``storage.open_write`` (default zip).

        Returns:
            Resolved path or URI string for the written object.

        Raises:
            ValueError: If destination or URL arguments are inconsistent.
        """
        if not download_link and not file_name:
            raise ValueError(
                "download_backup requires file_name when download_link is omitted "
                "(needed for list lookup or GET .../backups/{fileName}).",
            )
        if storage is not None:
            if not relative_path:
                raise ValueError("relative_path is required when storage is provided")
            if output_path is not None:
                raise ValueError("pass either output_path or storage, not both")
        elif not output_path:
            raise ValueError("output_path is required when storage is omitted")

        # progress_callback: optional callable ``(bytes_downloaded, total_bytes) -> None`` passed
        # through to the client's streaming download. Invoked as chunks are written; ``total_bytes``
        # may be None when the response has no Content-Length (e.g. chunked transfer).

        url = download_link
        if not url and file_name is not None:
            for row in self.list_backups():
                if row.get("name") != file_name:
                    continue
                link = row.get("link")
                if isinstance(link, str) and link.startswith(("http://", "https://")):
                    url = link
                break

        def _dest_return() -> str:
            if storage is not None and relative_path is not None:
                fp = getattr(storage, "full_path", None)
                if callable(fp):
                    return fp(relative_path)
                return relative_path
            if output_path is None:
                raise RuntimeError("output_path is required when storage is omitted")
            return str(output_path)

        if url:
            if storage is not None:
                if relative_path is None:
                    raise RuntimeError("relative_path is required when storage is set")
                with storage.open_write(relative_path, content_type=content_type) as buf:
                    self._client.download_file(
                        url,
                        destination=buf,
                        progress_callback=progress_callback,
                        skip_auth=True,
                    )
            else:
                self._client.download_file(
                    url,
                    destination=output_path,
                    progress_callback=progress_callback,
                    skip_auth=True,
                )
        else:
            endpoint = f"{self._backups_url}/{file_name}"
            if storage is not None:
                if relative_path is None:
                    raise RuntimeError("relative_path is required when storage is set")
                with storage.open_write(relative_path, content_type=content_type) as buf:
                    self._client.download_file(
                        endpoint,
                        destination=buf,
                        progress_callback=progress_callback,
                    )
            else:
                self._client.download_file(
                    endpoint,
                    destination=output_path,
                    progress_callback=progress_callback,
                )
        out = _dest_return()
        log_label = file_name if file_name else "download_link"
        self._logger.info(f"Downloaded backup {log_label} to {out}")
        return out

    # =========================================================================
    # Delete backup
    # =========================================================================

    def delete_backup(self, file_name: str) -> bool:
        """
        Delete a backup by fileName.

        API: POST /api/rest/v4/backups/delete/{fileName}.

        Args:
            file_name: Backup file name (API: fileName) to delete.

        Returns:
            True if the request succeeded.
        """
        url = f"{self._backups_url}/delete/{file_name}"
        self._client.post(url)
        return True
