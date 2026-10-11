"""
DealCloud-specific RestClient.

Some v4 endpoints (e.g. Site Backups) return plain-text bodies on 4xx/5xx instead of JSON.
The generic ``intapp_rest_client.RestClient`` stores those as ``str`` on ``HttpError.response_body``.
This subclass normalizes non-JSON error bodies to an ``ApiResult``-like dict (swagger
``DealCloud.Web.Utils.Net.WebApi.ApiResult``): ``statusCode``, ``message``, and ``error``
(same text as ``message`` for callers that expect ``{ "error": "..." }``).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, BinaryIO, Callable, Dict, Optional, Union

import fsspec
import httpx
from intapp_rest_client import RestClient
from intapp_rest_client.exceptions import HttpError


def normalize_plain_text_error_body(response: httpx.Response) -> Dict[str, Any]:
    """
    Build an ApiResult-like dict from a response body that is not JSON.

    Used when ``response.json()`` fails so ``HttpError.response_body`` stays a mapping.
    """
    raw = response.text or ""
    text = raw.strip()
    status = response.status_code
    body: Dict[str, Any] = {
        "statusCode": status,
        "message": text if text else None,
    }
    if text:
        body["error"] = text
    return body


class DealCloudRestClient(RestClient):
    """
    RestClient for the DealCloud Python SDK.

    Overrides error handling only: non-JSON error responses become structured dicts.
    Successful responses and JSON error bodies are unchanged.
    """

    def _handle_error_response(self, response: httpx.Response, request_id: Optional[str] = None) -> None:
        try:
            body = response.json()
        except httpx.ResponseNotRead:
            # httpx.stream / async stream: body is not loaded until read/aread.
            # intapp-rest-client download paths read before calling this; keep this
            # for older clients or other streaming callers using sync read().
            response.read()
            try:
                body = response.json()
            except json.JSONDecodeError:
                body = normalize_plain_text_error_body(response)
        except json.JSONDecodeError:
            body = normalize_plain_text_error_body(response)

        status = response.status_code
        headers = dict(response.headers)

        self.logger.debug(
            f"HTTP error response - Status: {status}, "
            f"Body: {body}, "
            f"Headers: {self._sanitize_headers(headers)}, "
            f"Request-ID: {request_id}"
        )

        messages = {
            400: "Bad request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
            429: "Rate limit exceeded",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable",
            504: "Gateway timeout",
        }

        message = messages.get(status, f"HTTP error {status}")
        raise HttpError(status, message, body, headers, request_id=request_id)

    def download_file(
        self,
        endpoint: str,
        destination: Union[str, Path, BinaryIO],
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
        skip_auth: bool = False,
        **kwargs: Any,
    ) -> int:
        """
        Stream a GET to disk or a binary buffer.

        **String / path destinations** (local paths and URIs such as ``s3://``) always open
        via **fsspec** and stream through this class's ``_download_file_to_stream`` (SDK
        behavior).

        **BinaryIO** destinations: if ``intapp_rest_client.RestClient`` defines
        ``download_file``, that implementation is used; otherwise the same
        ``_download_file_to_stream`` path applies (e.g. older wheels without ``download_file``).
        """
        if isinstance(destination, (str, Path)):
            dest_str = str(destination)
            if "://" not in dest_str:
                fsspec.filesystem("file").makedirs(str(Path(dest_str).parent), exist_ok=True)
            with fsspec.open(dest_str, "wb") as file_obj:
                return self._download_file_to_stream(
                    endpoint,
                    file_obj,
                    params=params,
                    headers=headers,
                    chunk_size=chunk_size,
                    timeout=timeout,
                    progress_callback=progress_callback,
                    skip_auth=skip_auth,
                    **kwargs,
                )

        sup = super(DealCloudRestClient, self)
        base_dl = getattr(sup, "download_file", None)
        if base_dl is not None:
            return base_dl(
                endpoint,
                destination,
                params=params,
                headers=headers,
                chunk_size=chunk_size,
                timeout=timeout,
                progress_callback=progress_callback,
                skip_auth=skip_auth,
                **kwargs,
            )
        return self._download_file_to_stream(
            endpoint,
            destination,
            params=params,
            headers=headers,
            chunk_size=chunk_size,
            timeout=timeout,
            progress_callback=progress_callback,
            skip_auth=skip_auth,
            **kwargs,
        )

    def _download_file_to_stream(
        self,
        endpoint: str,
        destination: BinaryIO,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        chunk_size: int = 8192,
        timeout: Optional[float] = None,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
        skip_auth: bool = False,
        **kwargs: Any,
    ) -> int:
        """Streaming download into an open binary stream (used for fsspec and BinaryIO)."""
        url = self._build_url(endpoint)
        if skip_auth:
            request_headers = {**self.default_headers, **(headers or {})}
            all_params = dict(params or {})
            stream_auth: Optional[Any] = None
        else:
            auth_headers_fn = getattr(self, "_get_auth_headers_sync", None)
            auth_params_fn = getattr(self, "_get_auth_params_sync", None)
            request_headers = {
                **self.default_headers,
                **(auth_headers_fn() if auth_headers_fn else {}),
                **(headers or {}),
            }
            params_extra = auth_params_fn() if auth_params_fn else {}
            all_params = {**(params or {}), **params_extra}
            stream_auth = getattr(self, "_httpx_auth", None)

        effective_timeout = timeout if timeout is not None else self.timeout
        file_obj = destination

        with httpx.stream(
            "GET",
            url,
            params=all_params if all_params else None,
            headers=request_headers,
            timeout=effective_timeout,
            auth=stream_auth,
            **kwargs,
        ) as response:
            if not response.is_success:
                response.read()
                self._handle_error_response(response)

            total_size = None
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    total_size = int(content_length)
                except ValueError:
                    pass

            downloaded = 0
            for chunk in response.iter_bytes(chunk_size):
                file_obj.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    try:
                        progress_callback(downloaded, total_size)
                    except Exception as e:
                        self.logger.warning(f"Progress callback failed: {e}")

            return downloaded
