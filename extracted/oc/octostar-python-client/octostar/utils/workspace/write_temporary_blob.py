from typing import Union
from io import BytesIO
import logging
import os
import httpx
from urllib import parse as urllib_parse

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


DEFAULT_TIMEOUT = 120


def _is_dev_mode() -> bool:
    return f"{os.getenv('OS_DEV_MODE')}".lower() == "true"


def _upload_api_url(client: Client, filename: str) -> str:
    """Build the blob upload API endpoint URL."""
    base = client.get_base_url_v1()
    return f"{base}/api/v1/files/upload-blob/{filename}"


def _resolve_url(client: Client, path: str, use_external: bool) -> str:
    """Resolve a presigned URL, joining with base URL in external/dev mode."""
    if use_external:
        return urllib_parse.urljoin(client.get_base_url_v1(), path)
    return path


def _get_upload_info_sync(
    api_url: str, headers: dict, filename: str, client: Client
) -> dict:
    """Fetch presigned upload URL and fields from the API."""
    use_external = _is_dev_mode()
    params = {"external_url": use_external}
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = http_client.get(api_url, headers=headers, params=params)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("write_temporary_blob", response, client)
    result = response.json()
    url = result.get("url")
    if not url:
        raise ValueError(f"write_temporary_blob: no upload url returned for {filename}")
    return {
        "url": _resolve_url(client, url, use_external),
        "fields": result.get("fields", {}),
    }


async def _get_upload_info_async(
    api_url: str, headers: dict, filename: str, client: Client
) -> dict:
    """Fetch presigned upload URL and fields from the API (async)."""
    use_external = _is_dev_mode()
    params = {"external_url": use_external}
    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.get(
                        api_url, headers=headers, params=params
                    )
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("write_temporary_blob", response, client)
    result = response.json()
    url = result.get("url")
    if not url:
        raise ValueError(f"write_temporary_blob: no upload url returned for {filename}")
    return {
        "url": _resolve_url(client, url, use_external),
        "fields": result.get("fields", {}),
    }


def sync(
    filename: str,
    file: Union[str, bytes, BytesIO],
    client: Client = None,
):
    """
    # Write a temporary blob to the user's temp bucket

    Uploads a file to the authenticated user's temporary S3 bucket.
    This is useful for temporary file storage before processing or importing into workspaces.
    The blob is not associated with any workspace entity — use write_file() for that.

    ## Arguments
    - `filename`: The name for the file in the temp bucket
    - `file`: The file contents — a local file path (str), bytes, or BytesIO
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    None on success

    ## Raises
    - `ApiConnectionError`: If requesting the presigned upload URL failed
    - `ConnectionError`: If the upload to S3 failed
    """
    if not client:
        client = get_default_client()

    api_url = _upload_api_url(client, filename)
    auth_headers = dict(client.get_headers())
    upload_info = _get_upload_info_sync(api_url, auth_headers, filename, client)
    upload_url = upload_info["url"]
    upload_fields = upload_info["fields"]

    should_close = False
    if isinstance(file, str):
        file_obj = open(file, "rb")
        should_close = True
    elif isinstance(file, bytes):
        file_obj = BytesIO(file)
    else:
        file_obj = file

    try:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    if hasattr(file_obj, "seek"):
                        file_obj.seek(0)
                    with httpx.Client() as http_client:
                        response = http_client.post(
                            upload_url,
                            data=upload_fields,
                            files={"file": (filename, file_obj)},
                            timeout=DEFAULT_TIMEOUT,
                        )
                        response.raise_for_status()
        except Exception:
            raise ConnectionError(
                f"write_temporary_blob: upload failed for {filename}"
                + (f" — {response.status_code}: {response.text}" if response else "")
            )
    finally:
        if should_close:
            file_obj.close()


async def asyncio(
    filename: str,
    file: Union[str, bytes, BytesIO],
    client: Client = None,
):
    """
    # Write a temporary blob to the user's temp bucket (async)

    Uploads a file to the authenticated user's temporary S3 bucket.
    This is useful for temporary file storage before processing or importing into workspaces.
    The blob is not associated with any workspace entity — use write_file() for that.

    ## Arguments
    - `filename`: The name for the file in the temp bucket
    - `file`: The file contents — a local file path (str), bytes, or BytesIO
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Returns
    None on success

    ## Raises
    - `ApiConnectionError`: If requesting the presigned upload URL failed
    - `ConnectionError`: If the upload to S3 failed
    """
    if not client:
        client = get_default_client()

    api_url = _upload_api_url(client, filename)
    auth_headers = dict(client.get_headers())
    upload_info = await _get_upload_info_async(api_url, auth_headers, filename, client)
    upload_url = upload_info["url"]
    upload_fields = upload_info["fields"]

    should_close = False
    if isinstance(file, str):
        file_obj = open(file, "rb")
        should_close = True
    elif isinstance(file, bytes):
        file_obj = BytesIO(file)
    else:
        file_obj = file

    try:
        response = None
        try:
            for attempt in network_retry_strategy():
                with attempt:
                    if hasattr(file_obj, "seek"):
                        file_obj.seek(0)
                    async with httpx.AsyncClient() as http_client:
                        response = await http_client.post(
                            upload_url,
                            data=upload_fields,
                            files={"file": (filename, file_obj)},
                            timeout=DEFAULT_TIMEOUT,
                        )
                        response.raise_for_status()
        except Exception:
            raise ConnectionError(
                f"write_temporary_blob: upload failed for {filename}"
                + (f" — {response.status_code}: {response.text}" if response else "")
            )
    finally:
        if should_close:
            file_obj.close()
