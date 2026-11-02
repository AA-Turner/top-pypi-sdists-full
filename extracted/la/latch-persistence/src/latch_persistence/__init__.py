import asyncio
import base64
import hashlib
import math
import mimetypes
import os as _os
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from threading import Semaphore
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union
from urllib.parse import urljoin, urlparse

import httpx
import requests
from requests.adapters import HTTPAdapter, Retry

from latch_persistence._wire_types import (
    CompletedUploadPart,
    EndUploadResponse,
    MultipartStartUploadResponse,
    ObjectExistsResponse,
    RecursiveSignedUrlResponse,
    SignedUrlResponse,
    UploadResult,
    ZeroPartStartUploadResponse,
)


@dataclass
class LatchConfig(object):
    """
    Latch specific configuration values
    """

    endpoint: str = "https://nucleus.latch.bio"
    upload_chunk_size_bytes: int = 10000000

    @classmethod
    def auto(cls, config_file=None) -> "LatchConfig":
        return LatchConfig()


class LatchPersistenceRateLimitError(ValueError):
    status_code = 429

    def __init__(
        self,
        *,
        operation: str,
        remote_path: str,
        response_text: str,
    ) -> None:
        super().__init__(
            f"rate limited during {operation} for `{remote_path}`: {response_text}"
        )
        self.operation = operation
        self.remote_path = remote_path
        self.response_text = response_text


download_part_size = 1024 * 1024 * 100
write_chunk_size = 1024 * 1024
num_concurrent_downloads = 8


def urlretrieve(url: str, start: int, end: int, fd: int):
    attempts = 0
    while True:
        try:
            headers = {"Range": f"bytes={start}-{end}"}
            r = _session.get(url, headers=headers, stream=True, timeout=90)
            if r.status_code != 206:
                raise RuntimeError(
                    "failed to download byte range {}-{}: "
                    "status_code={} error={}".format(
                        start,
                        end,
                        r.status_code,
                        r.content,
                    )
                )

            bytes_written = 0
            for chunk in r.iter_content(write_chunk_size):
                bytes_written += _os.pwrite(fd, chunk, start + bytes_written)

            break
        except requests.exceptions.ConnectionError as e:
            attempts += 1
            if attempts >= 3:
                raise e

        time.sleep(0.1 * 2**attempts)


byte_range_prefix = "bytes 0-0/"


def get(args: Tuple[str, Union[str, Path]]) -> bool:
    url = args[0]
    path = args[1]

    r = _session.get(url, headers={"Range": "bytes=0-0"}, timeout=90)
    if r.status_code == 404:
        return False

    if r.status_code == 416:
        Path(path).write_text("")
        return True

    if r.status_code != 206:
        raise RuntimeError(
            f"failed to get file size for `{url}`: status_code={r.status_code} error={r.content}"
        )

    content_range = r.headers.get("Content-Range")
    if content_range is None or not content_range.startswith(byte_range_prefix):
        raise RuntimeError(f"invalid Content-Range header for `{url}`: {content_range}")

    file_size = int(content_range[len(byte_range_prefix) :])
    num_parts = math.ceil(file_size / download_part_size)

    with open(path, "wb") as output_file:
        futures: list[Future] = []

        with ThreadPoolExecutor(max_workers=num_concurrent_downloads) as executor:
            for i in range(num_parts):
                start = i * download_part_size
                end = min(start + download_part_size - 1, file_size - 1)
                futures.append(
                    executor.submit(urlretrieve, url, start, end, output_file.fileno())
                )

        for future in futures:
            future.result()

    return True


def get_auth_header() -> str:
    internal_execution_id = _os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if internal_execution_id is not None:
        return f"Latch-Execution-Token {internal_execution_id}"

    token_path = Path.home() / ".latch" / "token"
    if token_path.exists():
        return f"Latch-SDK-Token {token_path.read_text().strip()}"

    raise ValueError("no authentication method found")


def _enforce_trailing_slash(path: str):
    if path[-1] != "/":
        path += "/"
    return path


_session = requests.Session()

_adapter = HTTPAdapter(
    max_retries=Retry(
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=["GET", "PUT", "POST"],
    ),
    pool_maxsize=100,
    pool_connections=10,
)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)


MAXIMUM_UPLOAD_SIZE = 5 * 2**40  # 5 TiB
MAXIMUM_UPLOAD_PARTS = 10000
MAX_CONCURRENT_CHUNKS = 100
MAX_CONCURRENT_UPLOADS = 100
MAX_CONCURRENT_CALLS = 10

_nucleus_semaphore = Semaphore(MAX_CONCURRENT_CALLS)


def _upload_chunk_plan(file_size: int, default_chunk_size: int) -> Tuple[int, int]:
    chunk_size = max(
        default_chunk_size,
        math.ceil(file_size / MAXIMUM_UPLOAD_PARTS),
    )
    nrof_parts = math.ceil(float(file_size) / chunk_size)
    return chunk_size, nrof_parts


def _accumulate_cache(cache_accum: bytearray, cache: str) -> None:
    digest = hashlib.sha256(cache.encode("utf-8")).digest()
    for idx, digest_byte in enumerate(digest):
        cache_accum[idx] ^= digest_byte


def _combine_upload_caches(results: List[UploadResult]) -> UploadResult:
    cache_accum = bytearray([0] * 32)
    for result in results:
        _accumulate_cache(cache_accum, result["cache"])

    cache = base64.standard_b64encode(bytes(cache_accum)).decode("ascii")
    return {"cache": cache}


def _resolve_recursive_downloads(
    key_to_url_map: Dict[str, str],
    local_path: str,
) -> List[Tuple[str, Path]]:
    destination_root = Path(local_path).resolve()
    downloads: List[Tuple[str, Path]] = []

    for key, url in key_to_url_map.items():
        if key == "":
            raise ValueError("recursive signed URL response contained an empty path")
        if Path(key).is_absolute():
            raise ValueError(
                f"recursive signed URL response contained an absolute path `{key}`"
            )
        if url == "":
            raise ValueError(
                f"recursive signed URL response contained an empty URL for `{key}`"
            )

        local_file_path = destination_root.joinpath(key).resolve()
        try:
            local_file_path.relative_to(destination_root)
        except ValueError:
            raise ValueError(
                f"recursive signed URL response contained an unsafe path `{key}`"
            ) from None

        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        downloads.append((url, local_file_path))

    return downloads


class LatchPersistence:
    PROTOCOL = "latch://"

    def __init__(self, default_prefix: Optional[str] = None, data_config=None):
        self._name = "latch"
        self._default_prefix = default_prefix
        default_latch_config = data_config.latch if data_config else LatchConfig.auto()

        latch_endpoint = _os.environ.get("LATCH_AUTHENTICATION_ENDPOINT")
        if latch_endpoint is None:
            latch_endpoint = default_latch_config.endpoint
        if latch_endpoint is None:
            raise ValueError("LATCH_AUTHENTICATION_ENDPOINT must be set")

        self._latch_endpoint = latch_endpoint

        self._default_chunk_size = default_latch_config.upload_chunk_size_bytes
        if self._default_chunk_size is None:
            raise ValueError("S3_UPLOAD_CHUNK_SIZE_BYTES must be set")

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_prefix(self) -> Optional[str]:
        return self._default_prefix

    @staticmethod
    def _split_s3_path_to_key(path: str) -> str:
        """
        :param str path:
        :rtype: str
        """
        url = urlparse(path)
        return url.path

    def exists(self, remote_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :rtype bool: whether the s3 file exists or not
        """
        if not remote_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {remote_path}")

        attempts = 0
        while True:
            try:
                r = _session.post(
                    urljoin(self._latch_endpoint, "/api/object-exists-at-url"),
                    json={
                        "object_url": remote_path,
                        "execution_name": _os.environ.get(
                            "FLYTE_INTERNAL_EXECUTION_ID"
                        ),
                    },
                    timeout=90,
                )
                break
            except requests.exceptions.ConnectionError as e:
                attempts += 1
                if attempts >= 3:
                    raise e
                time.sleep(0.1 * 2**attempts)

        if r.status_code != 200:
            raise ValueError(
                "failed to check if object exists at url `{}`".format(remote_path)
            )

        return r.json()["exists"]

    def download_directory(self, remote_path: str, local_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :param str local_path: directory to copy to
        :return: whether every presigned object existed and was downloaded
        """

        auth_headers = {"Authorization": get_auth_header()}
        r = _session.post(
            urljoin(self._latch_endpoint, "/ldata/get-signed-urls-recursive"),
            json={
                "path": remote_path,
            },
            headers=auth_headers,
            timeout=90,
        )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(f"failed to get presigned urls for `{remote_path}`")

        key_to_url_map = RecursiveSignedUrlResponse.model_validate(res_data).data.urls
        task_tuples = _resolve_recursive_downloads(key_to_url_map, local_path)

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures: List[Future[bool]] = [
                executor.submit(get, task) for task in task_tuples
            ]
            results = [future.result() for future in futures]

        return all(results)

    def download(self, remote_path: str, local_path: str) -> bool:
        """
        :param str remote_path: remote latch:// path
        :param str local_path: directory to copy to
        """

        auth_headers = {"Authorization": get_auth_header()}
        r = _session.post(
            urljoin(self._latch_endpoint, "/ldata/get-signed-url"),
            json={
                "path": remote_path,
            },
            headers=auth_headers,
            timeout=90,
        )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(f"failed to get presigned url for `{remote_path}`")

        url = res_data["data"]["url"]
        return get((url, local_path))

    @staticmethod
    def _upload_chunk(
        file_path: str, chunk_size: int, offset: int, url: str, part_num: int
    ):
        with open(file_path, "rb") as f:
            chunk = _os.pread(f.fileno(), chunk_size, offset)
            r = _session.put(url, data=chunk, timeout=90)
            if r.status_code != 200:
                raise RuntimeError(f"Failed to upload chunk: {r.status_code} {r.text}")
            return {"ETag": r.headers["ETag"], "PartNumber": part_num}

    @staticmethod
    def _upload_chunks(
        file_path: str,
        presigned_urls: List[str],
        chunk_size: int,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        managed_executor = executor is None
        if managed_executor:
            executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_CHUNKS)

        try:
            futures: List[Future] = []
            for idx, url in enumerate(presigned_urls):
                offset = idx * chunk_size
                futures.append(
                    executor.submit(
                        LatchPersistence._upload_chunk,
                        file_path,
                        chunk_size,
                        offset,
                        url,
                        idx + 1,
                    )
                )

            parts = []
            for future in futures:
                parts.append(future.result())
        finally:
            if managed_executor:
                executor.shutdown()

        return sorted(parts, key=lambda x: x["PartNumber"])

    @staticmethod
    def _upload(
        file_path: str,
        to_path: str,
        default_chunk_size: int,
        endpoint: str,
        executor: Optional[ThreadPoolExecutor] = None,
    ) -> UploadResult:
        file_size = _os.path.getsize(file_path)
        if file_size > MAXIMUM_UPLOAD_SIZE:
            raise ValueError(
                f"File {file_path} is {file_size} bytes which exceeds the maximum upload size (5TiB)"
            )

        chunk_size, nrof_parts = _upload_chunk_plan(file_size, default_chunk_size)
        content_type = mimetypes.guess_type(file_path)[0]
        if content_type is None:
            content_type = "application/octet-stream"

        auth_headers = {"Authorization": get_auth_header()}

        with _nucleus_semaphore:
            r = _session.post(
                urljoin(endpoint, "/ldata/start-upload"),
                json={
                    "path": to_path,
                    "part_count": nrof_parts,
                    "content_type": content_type,
                },
                headers=auth_headers,
                timeout=90,
            )

        res_data = r.json()
        if r.status_code != 200:
            raise ValueError(
                f"failed to get presigned upload urls for `{to_path}`: {res_data['error']}"
            )

        data = res_data["data"]

        if nrof_parts == 0:
            return {"cache": data["version_id"]}

        presigned_urls = data["urls"]
        upload_id = data["upload_id"]

        parts = LatchPersistence._upload_chunks(
            file_path, presigned_urls, chunk_size, executor
        )

        with _nucleus_semaphore:
            r = _session.post(
                urljoin(endpoint, "/ldata/end-upload"),
                json={
                    "upload_id": upload_id,
                    "parts": parts,
                    "path": to_path,
                },
                headers=auth_headers,
                timeout=90,
            )

        res_data = r.json()
        if r.status_code != 200:
            raise RuntimeError(
                f"failed to complete upload for `{to_path}`: {res_data['error']}"
            )

        data = res_data["data"]
        return {"cache": data["version_id"]}

    def upload(self, file_path: str, to_path: str) -> UploadResult:
        """
        :param str file_path:
        :param str to_path:
        """
        return LatchPersistence._upload(
            file_path, to_path, self._default_chunk_size, self._latch_endpoint
        )

    def upload_directory(self, local_path: str, remote_path: str) -> UploadResult:
        """
        :param str local_path:
        :param str remote_path:
        """
        if remote_path == "latch://":
            remote_path = "latch:///"

        # ensure formatting
        local_path = _enforce_trailing_slash(local_path)
        remote_path = _enforce_trailing_slash(remote_path)

        files_to_upload = [
            _os.path.join(dp, f)
            for dp, __, filenames in _os.walk(local_path)
            for f in filenames
        ]

        results: List[UploadResult] = []

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_UPLOADS) as outer_executor:
            futures: List[Future[UploadResult]] = []

            with ThreadPoolExecutor(
                max_workers=MAX_CONCURRENT_CHUNKS
            ) as inner_executor:
                for file_path in files_to_upload:
                    relative_name = file_path.replace(local_path, "", 1)
                    if relative_name.startswith("/"):
                        relative_name = relative_name[1:]

                    futures.append(
                        outer_executor.submit(
                            self._upload,
                            file_path,
                            remote_path + relative_name,
                            self._default_chunk_size,
                            self._latch_endpoint,
                            inner_executor,
                        )
                    )

                for future in futures:
                    results.append(future.result())

        return _combine_upload_caches(results)

    def construct_path(self, add_protocol: bool, add_prefix: bool, *args: str) -> str:
        paths = list(args)  # make type check happy
        if add_prefix and self.default_prefix is not None:
            paths.insert(0, self.default_prefix)
        path = "/".join(paths)
        if add_protocol:
            return f"{self.PROTOCOL}{path}"
        return path

    def get(self, from_path: str, to_path: str, recursive: bool = False):
        if not from_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {from_path}")

        if recursive:
            return self.download_directory(from_path, to_path)

        return self.download(from_path, to_path)

    def put(self, from_path: str, to_path: str, recursive: bool = False):
        if not to_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {to_path}")

        if recursive:
            return self.upload_directory(from_path, to_path)

        return self.upload(from_path, to_path)


ASYNC_RETRY_STATUS_CODES = frozenset([429, 500, 502, 503, 504])
ASYNC_MAX_ATTEMPTS = 3
ASYNC_TIMEOUT_SECONDS = 90.0
ASYNC_NUCLEUS_CONCURRENCY = MAX_CONCURRENT_CALLS
ASYNC_UPLOAD_PART_CONCURRENCY = MAX_CONCURRENT_CHUNKS
ASYNC_UPLOAD_FILE_CONCURRENCY = MAX_CONCURRENT_UPLOADS
ASYNC_DOWNLOAD_RANGE_CONCURRENCY = num_concurrent_downloads
ASYNC_DOWNLOAD_FILE_CONCURRENCY = 20
ASYNC_MAX_KEEPALIVE_CONNECTIONS = 20
ASYNC_MAX_CONNECTIONS = (
    ASYNC_NUCLEUS_CONCURRENCY
    + ASYNC_UPLOAD_PART_CONCURRENCY
    + ASYNC_UPLOAD_FILE_CONCURRENCY
    + ASYNC_DOWNLOAD_RANGE_CONCURRENCY
    + ASYNC_DOWNLOAD_FILE_CONCURRENCY
)

_TaskT = TypeVar("_TaskT")


async def _async_retry_sleep(attempt: int) -> None:
    await asyncio.sleep(0.1 * 2**attempt)


async def _async_request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    redact_transport_error: Optional[str] = None,
    **kwargs: Any,
) -> httpx.Response:
    attempts = 0
    while True:
        try:
            response = await client.request(
                method,
                url,
                timeout=ASYNC_TIMEOUT_SECONDS,
                follow_redirects=True,
                **kwargs,
            )
        except httpx.TransportError:
            attempts += 1
            if attempts >= ASYNC_MAX_ATTEMPTS:
                if redact_transport_error is not None:
                    raise RuntimeError(redact_transport_error) from None
                raise
            await _async_retry_sleep(attempts)
            continue

        if response.status_code not in ASYNC_RETRY_STATUS_CODES:
            return response

        attempts += 1
        if attempts >= ASYNC_MAX_ATTEMPTS:
            return response

        await _async_retry_sleep(attempts)


async def _gather_or_cancel(tasks: List[asyncio.Task[_TaskT]]) -> List[_TaskT]:
    try:
        return list(await asyncio.gather(*tasks))
    except BaseException:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise


class AsyncLatchPersistence:
    PROTOCOL = LatchPersistence.PROTOCOL

    def __init__(
        self,
        default_prefix: Optional[str] = None,
        data_config=None,
        client: Optional[httpx.AsyncClient] = None,
    ):
        self._name = "latch"
        self._default_prefix = default_prefix
        default_latch_config = data_config.latch if data_config else LatchConfig.auto()

        latch_endpoint = _os.environ.get("LATCH_AUTHENTICATION_ENDPOINT")
        if latch_endpoint is None:
            latch_endpoint = default_latch_config.endpoint
        if latch_endpoint is None:
            raise ValueError("LATCH_AUTHENTICATION_ENDPOINT must be set")

        self._latch_endpoint = latch_endpoint

        self._default_chunk_size = default_latch_config.upload_chunk_size_bytes
        if self._default_chunk_size is None:
            raise ValueError("S3_UPLOAD_CHUNK_SIZE_BYTES must be set")

        self._client = client
        self._owns_client = client is None
        self._nucleus_semaphore = asyncio.Semaphore(ASYNC_NUCLEUS_CONCURRENCY)
        self._upload_part_semaphore = asyncio.Semaphore(ASYNC_UPLOAD_PART_CONCURRENCY)
        self._upload_file_semaphore = asyncio.Semaphore(ASYNC_UPLOAD_FILE_CONCURRENCY)
        self._download_range_semaphore = asyncio.Semaphore(
            ASYNC_DOWNLOAD_RANGE_CONCURRENCY
        )
        self._download_file_semaphore = asyncio.Semaphore(
            ASYNC_DOWNLOAD_FILE_CONCURRENCY
        )

    async def __aenter__(self) -> "AsyncLatchPersistence":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
            self._client = None

    def _http_client(self) -> httpx.AsyncClient:
        if self._client is None:
            limits = httpx.Limits(
                max_keepalive_connections=ASYNC_MAX_KEEPALIVE_CONNECTIONS,
                max_connections=ASYNC_MAX_CONNECTIONS,
            )
            self._client = httpx.AsyncClient(
                timeout=ASYNC_TIMEOUT_SECONDS,
                limits=limits,
                follow_redirects=True,
            )
        return self._client

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_prefix(self) -> Optional[str]:
        return self._default_prefix

    async def exists(self, remote_path: str) -> bool:
        if not remote_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {remote_path}")

        response = await _async_request(
            self._http_client(),
            "POST",
            urljoin(self._latch_endpoint, "/api/object-exists-at-url"),
            json={
                "object_url": remote_path,
                "execution_name": _os.environ.get("FLYTE_INTERNAL_EXECUTION_ID"),
            },
        )

        if response.status_code != 200:
            raise ValueError(f"failed to check if object exists at url `{remote_path}`")

        return ObjectExistsResponse.model_validate_json(response.content).exists

    async def _download_part(
        self,
        url: str,
        start: int,
        end: int,
        fd: int,
    ) -> None:
        attempts = 0
        headers = {"Range": f"bytes={start}-{end}"}

        while True:
            try:
                async with self._download_range_semaphore:
                    async with self._http_client().stream(
                        "GET",
                        url,
                        headers=headers,
                        timeout=ASYNC_TIMEOUT_SECONDS,
                        follow_redirects=True,
                    ) as response:
                        if response.status_code in ASYNC_RETRY_STATUS_CODES:
                            attempts += 1
                            content = await response.aread()
                            if attempts >= ASYNC_MAX_ATTEMPTS:
                                raise RuntimeError(
                                    "failed to download byte range {}-{}: "
                                    "status_code={} error={}".format(
                                        start,
                                        end,
                                        response.status_code,
                                        content,
                                    )
                                )

                        elif response.status_code != 206:
                            content = await response.aread()
                            raise RuntimeError(
                                "failed to download byte range {}-{}: "
                                "status_code={} error={}".format(
                                    start,
                                    end,
                                    response.status_code,
                                    content,
                                )
                            )

                        else:
                            bytes_written = 0
                            async for chunk in response.aiter_bytes(write_chunk_size):
                                if len(chunk) == 0:
                                    continue
                                bytes_written += await asyncio.to_thread(
                                    _os.pwrite,
                                    fd,
                                    chunk,
                                    start + bytes_written,
                                )
                            return
            except httpx.TransportError:
                attempts += 1
                if attempts >= ASYNC_MAX_ATTEMPTS:
                    raise RuntimeError(
                        f"failed to download byte range {start}-{end}"
                    ) from None

            await _async_retry_sleep(attempts)

    async def _download_presigned_url(self, url: str, path: str) -> bool:
        async with self._download_file_semaphore:
            response = await _async_request(
                self._http_client(),
                "GET",
                url,
                headers={"Range": "bytes=0-0"},
                redact_transport_error="failed to get file size from presigned URL",
            )
            if response.status_code == 404:
                return False

            if response.status_code == 416:
                await asyncio.to_thread(Path(path).write_text, "")
                return True

            if response.status_code != 206:
                raise RuntimeError(
                    "failed to get file size from presigned URL: "
                    f"status_code={response.status_code} error={response.content}"
                )

            content_range = response.headers.get("Content-Range")
            if content_range is None or not content_range.startswith(byte_range_prefix):
                raise RuntimeError(f"invalid Content-Range header: {content_range}")

            file_size = int(content_range[len(byte_range_prefix) :])
            num_parts = math.ceil(file_size / download_part_size)

            with open(path, "wb") as output_file:
                tasks: List[asyncio.Task[None]] = []
                for i in range(num_parts):
                    start = i * download_part_size
                    end = min(start + download_part_size - 1, file_size - 1)
                    tasks.append(
                        asyncio.create_task(
                            self._download_part(
                                url,
                                start,
                                end,
                                output_file.fileno(),
                            )
                        )
                    )

                await _gather_or_cancel(tasks)

            return True

    async def download_directory(self, remote_path: str, local_path: str) -> bool:
        """Download a directory and return whether every presigned object existed."""
        response = await _async_request(
            self._http_client(),
            "POST",
            urljoin(self._latch_endpoint, "/ldata/get-signed-urls-recursive"),
            json={"path": remote_path},
            headers={"Authorization": get_auth_header()},
        )

        if response.status_code != 200:
            raise ValueError(f"failed to get presigned urls for `{remote_path}`")

        key_to_url_map = RecursiveSignedUrlResponse.model_validate_json(
            response.content
        ).data.urls

        tasks: List[asyncio.Task[bool]] = []
        for url, local_file_path in _resolve_recursive_downloads(
            key_to_url_map, local_path
        ):
            tasks.append(
                asyncio.create_task(
                    self._download_presigned_url(url, str(local_file_path))
                )
            )

        return all(await _gather_or_cancel(tasks))

    async def download(self, remote_path: str, local_path: str) -> bool:
        response = await _async_request(
            self._http_client(),
            "POST",
            urljoin(self._latch_endpoint, "/ldata/get-signed-url"),
            json={"path": remote_path},
            headers={"Authorization": get_auth_header()},
        )

        if response.status_code != 200:
            raise ValueError(f"failed to get presigned url for `{remote_path}`")

        url = SignedUrlResponse.model_validate_json(response.content).data.url
        if url == "":
            raise ValueError("signed URL response data.url was empty")

        return await self._download_presigned_url(url, local_path)

    async def _upload_chunk(
        self,
        file_path: str,
        chunk_size: int,
        offset: int,
        url: str,
        part_num: int,
    ) -> CompletedUploadPart:
        async with self._upload_part_semaphore:
            with open(file_path, "rb") as f:
                chunk = await asyncio.to_thread(
                    _os.pread, f.fileno(), chunk_size, offset
                )

            response = await _async_request(
                self._http_client(),
                "PUT",
                url,
                content=chunk,
                redact_transport_error="failed to upload chunk to presigned URL",
            )
            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to upload chunk: {response.status_code} {response.text}"
                )

            etag = response.headers.get("ETag")
            if etag is None or etag == "":
                raise RuntimeError("uploaded chunk response is missing `ETag` header")

            return {"ETag": etag, "PartNumber": part_num}

    async def _upload_chunks(
        self,
        file_path: str,
        presigned_urls: List[str],
        chunk_size: int,
    ) -> List[CompletedUploadPart]:
        tasks: List[asyncio.Task[CompletedUploadPart]] = []
        for idx, url in enumerate(presigned_urls):
            offset = idx * chunk_size
            tasks.append(
                asyncio.create_task(
                    self._upload_chunk(file_path, chunk_size, offset, url, idx + 1)
                )
            )

        parts = await _gather_or_cancel(tasks)
        return sorted(parts, key=lambda part: part["PartNumber"])

    async def _upload(
        self,
        file_path: str,
        to_path: str,
    ) -> UploadResult:
        async with self._upload_file_semaphore:
            file_size = await asyncio.to_thread(_os.path.getsize, file_path)
            if file_size > MAXIMUM_UPLOAD_SIZE:
                raise ValueError(
                    f"File {file_path} is {file_size} bytes which exceeds "
                    "the maximum upload size (5TiB)"
                )

            chunk_size, nrof_parts = _upload_chunk_plan(
                file_size, self._default_chunk_size
            )
            content_type = mimetypes.guess_type(file_path)[0]
            if content_type is None:
                content_type = "application/octet-stream"

            auth_headers = {"Authorization": get_auth_header()}
            async with self._nucleus_semaphore:
                response = await _async_request(
                    self._http_client(),
                    "POST",
                    urljoin(self._latch_endpoint, "/ldata/start-upload"),
                    json={
                        "path": to_path,
                        "part_count": nrof_parts,
                        "content_type": content_type,
                    },
                    headers=auth_headers,
                )

            if response.status_code == LatchPersistenceRateLimitError.status_code:
                raise LatchPersistenceRateLimitError(
                    operation="start-upload",
                    remote_path=to_path,
                    response_text=response.text,
                )

            if response.status_code != 200:
                raise ValueError(
                    f"failed to get presigned upload urls for `{to_path}`: "
                    f"{response.text}"
                )

            if nrof_parts == 0:
                version_id = ZeroPartStartUploadResponse.model_validate_json(
                    response.content
                ).data.version_id
                if version_id == "":
                    raise ValueError(
                        "zero-part start upload response data.version_id was empty"
                    )
                return {"cache": version_id}

            multipart_data = MultipartStartUploadResponse.model_validate_json(
                response.content
            ).data
            presigned_urls = multipart_data.urls
            upload_id = multipart_data.upload_id
            if upload_id == "":
                raise ValueError(
                    "multipart start upload response data.upload_id was empty"
                )
            if len(presigned_urls) != nrof_parts:
                raise ValueError(
                    "multipart start upload response returned "
                    f"{len(presigned_urls)} URLs for {nrof_parts} parts"
                )
            for url in presigned_urls:
                if url == "":
                    raise ValueError(
                        "multipart start upload response contained an empty URL"
                    )

            parts = await self._upload_chunks(file_path, presigned_urls, chunk_size)
            async with self._nucleus_semaphore:
                response = await _async_request(
                    self._http_client(),
                    "POST",
                    urljoin(self._latch_endpoint, "/ldata/end-upload"),
                    json={
                        "upload_id": upload_id,
                        "parts": parts,
                        "path": to_path,
                    },
                    headers=auth_headers,
                )

            if response.status_code == LatchPersistenceRateLimitError.status_code:
                raise LatchPersistenceRateLimitError(
                    operation="end-upload",
                    remote_path=to_path,
                    response_text=response.text,
                )

            if response.status_code != 200:
                raise RuntimeError(
                    f"failed to complete upload for `{to_path}`: {response.text}"
                )

            version_id = EndUploadResponse.model_validate_json(
                response.content
            ).data.version_id
            if version_id == "":
                raise ValueError("end upload response data.version_id was empty")
            return {"cache": version_id}

    async def upload(self, file_path: str, to_path: str) -> UploadResult:
        return await self._upload(file_path, to_path)

    async def upload_directory(self, local_path: str, remote_path: str) -> UploadResult:
        if remote_path == "latch://":
            remote_path = "latch:///"

        local_path = _enforce_trailing_slash(local_path)
        remote_path = _enforce_trailing_slash(remote_path)

        files_to_upload = [
            _os.path.join(dp, f)
            for dp, __, filenames in _os.walk(local_path)
            for f in filenames
        ]

        tasks: List[asyncio.Task[UploadResult]] = []
        for file_path in files_to_upload:
            relative_name = file_path.replace(local_path, "", 1)
            if relative_name.startswith("/"):
                relative_name = relative_name[1:]

            tasks.append(
                asyncio.create_task(
                    self._upload(
                        file_path,
                        remote_path + relative_name,
                    )
                )
            )

        results = await _gather_or_cancel(tasks)
        return _combine_upload_caches(results)

    def construct_path(self, add_protocol: bool, add_prefix: bool, *args: str) -> str:
        paths = list(args)
        if add_prefix and self.default_prefix is not None:
            paths.insert(0, self.default_prefix)
        path = "/".join(paths)
        if add_protocol:
            return f"{self.PROTOCOL}{path}"
        return path

    async def get(self, from_path: str, to_path: str, recursive: bool = False) -> bool:
        if not from_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {from_path}")

        if recursive:
            return await self.download_directory(from_path, to_path)

        return await self.download(from_path, to_path)

    async def put(
        self, from_path: str, to_path: str, recursive: bool = False
    ) -> UploadResult:
        if not to_path.startswith(self.PROTOCOL):
            raise ValueError(f"expected a Latch URL (latch://...): {to_path}")

        if recursive:
            return await self.upload_directory(from_path, to_path)

        return await self.upload(from_path, to_path)
