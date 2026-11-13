"""
Sandbox Executor API Client

Sync and async Python clients for interacting with the Sandbox Executor API.
"""

import asyncio
import contextlib
import json
import logging
import time
from dataclasses import dataclass
from typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Dict,
    Iterator,
    Optional,
    Sequence,
    Union,
)

import httpx

from .errors import (
    NoSandboxSecretError,
    SandboxError,
    SandboxRequestError,
    SandboxServiceError,
    SandboxTimeoutError,
)

DEFAULT_HTTP_TIMEOUT = 30  # seconds for HTTP requests

# Seconds without progress before a streamed /files call fails. Unlike
# DEFAULT_HTTP_TIMEOUT, which bounds the whole JSON call, this bounds idle
# time only: a transfer that keeps moving is never cut off (executor routes
# v0.0.24+; a 5 GiB transfer must not die at 30 s).
FILES_IDLE_TIMEOUT = 60

# The timeout object for every streamed /files call: idle-bounded, connect
# still capped at the JSON default.
_FILES_TIMEOUT = httpx.Timeout(FILES_IDLE_TIMEOUT, connect=DEFAULT_HTTP_TIMEOUT)

# One warning per handle: pre-v0.0.24 executors make every transfer legacy.
_LEGACY_FILES_WARNING = (
    "Sandbox executor has no streamed /files routes (pre-v0.0.24): "
    "file transfers use the legacy JSON routes"
)


def _probe_verdict(status_code: int) -> bool:
    """A probe reply's status to a routes verdict.

    404: the route does not exist (legacy executor). 400: "path is
    required" — the new executor answering. Anything else (401/403/429...)
    says nothing about the routes: raise, so the caller leaves the probe
    uncached and the next call tries again.
    """
    if status_code == 404:
        return False
    if status_code == 400:
        return True
    raise SandboxError(f"Failed probing /files routes: HTTP {status_code}")


# A request to the executor is retried up to 3 times, after 1, 2, then 4 s.
_MAX_RETRIES = 3
_INITIAL_BACKOFF = 1.0

logger = logging.getLogger(__name__)


def _timeout_seconds(timeout: Union[int, float, httpx.Timeout]) -> float:
    """The read/idle bound a timeout message should name.

    Legacy calls pass plain seconds; the streamed /files routes pass an
    httpx.Timeout whose read timeout is the idle bound.
    """
    if isinstance(timeout, httpx.Timeout):
        return timeout.read or 0.0
    return float(timeout)


def _override_timeout(
    timeout: Optional[float], default: Union[int, float, httpx.Timeout]
) -> Union[int, float, httpx.Timeout]:
    """A /files call's timeout: the per-call override or the default.

    The override keeps the default's shape — the idle bound for streamed
    bodies, the client's total cap for control calls — and connect stays
    at the JSON default either way.
    """
    if timeout is None:
        return default
    return httpx.Timeout(timeout, connect=DEFAULT_HTTP_TIMEOUT)


async def _async_stream(
    content: Union[BinaryIO, Iterator[bytes]]
) -> AsyncIterator[bytes]:
    """Yield sync stream content - a file object or chunk iterator - as
    the async stream httpx requires on an AsyncClient."""
    if hasattr(content, "read"):
        while True:
            chunk = content.read(65536)
            if not chunk:
                return
            yield chunk
    else:
        for chunk in content:
            yield chunk


def _raise_for_status(response: httpx.Response) -> None:
    """Wrap a non-2xx streamed response in the SDK taxonomy.

    The /files routes answer with real status codes and a {"error": ...}
    body; classification into filesystem exceptions happens one layer up.
    """
    if response.status_code >= 500:
        raise SandboxServiceError(
            status_code=response.status_code,
            message=response.text,
        )
    if response.status_code >= 400:
        raise SandboxRequestError(
            status_code=response.status_code,
            body=response.text,
        )


def _retry_delay(attempt: int, expires_at: Optional[float] = None) -> Optional[float]:
    """
    Seconds to wait before retrying a request whose try number attempt
    (0 for the first) failed, or None when it must not be retried: no retry
    left, or the wait would reach expires_at (a time.monotonic() deadline).
    """
    if attempt >= _MAX_RETRIES:
        return None
    delay = _INITIAL_BACKOFF * 2**attempt
    if expires_at is not None and time.monotonic() + delay >= expires_at:
        return None
    return delay


def _command_timed_out(timeout: Optional[float]) -> SandboxTimeoutError:
    """The error raised when a command's timeout runs out."""
    return SandboxTimeoutError(
        f"Command timed out after {timeout:g}s "
        "(pass a larger timeout, or timeout=None for no limit)"
    )


@dataclass
class ConnectionInfo:
    """Information needed to connect to a sandbox"""

    public_url: str
    routing_key: Optional[str]
    secret: Optional[str]

    def __str__(self) -> str:
        return f"ConnectionInfo(public_url={self.public_url}, routing_key={self.routing_key}, secret={'********' if self.secret else 'None'})"

    def validate(self) -> None:
        if not self.public_url:
            raise ValueError("Unable to get sandbox URL")
        if not self.secret:
            raise NoSandboxSecretError(
                "Sandbox secret not available — this handle is not "
                "executor-connected (e.g. it came from Sandbox.list()); use "
                "Sandbox.get_from_id(<id>) for a connected handle"
            )


def _build_headers(conn_info: ConnectionInfo) -> Dict[str, str]:
    """Build common headers for sandbox client."""
    headers = {
        "Authorization": f"Bearer {conn_info.secret}",
        "Content-Type": "application/json",
    }
    if conn_info.routing_key:
        headers["X-Routing-Key"] = conn_info.routing_key
    return headers


def _parse_sse_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a Server-Sent Events line into an event dict."""
    if not line or not line.startswith("data:"):
        return None
    data = line[5:].strip()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {"error": f"Failed to parse event data: {data}"}


class SandboxClient:
    """Client for the Sandbox Executor API."""

    def __init__(
        self, conn_info: ConnectionInfo, timeout: float = DEFAULT_HTTP_TIMEOUT
    ):
        """
        Initialize the Sandbox Client.

        Args:
            conn_info: The parameters needed to connect to the sandbox
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = conn_info.public_url.rstrip("/")
        self.secret = conn_info.secret
        self.timeout = timeout
        self.headers = _build_headers(conn_info)
        self._client = httpx.Client(headers=self.headers, trust_env=True)
        self._closed = False
        # Cached result of has_files_routes(): None = not probed yet.
        self._files_routes: Optional[bool] = None

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        if not getattr(self, "_closed", True) and hasattr(self, "_client"):
            self._client.close()
            self._closed = True

    def __enter__(self):
        """Context manager entry - returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - automatically closes the client."""
        self.close()

    def __del__(self):
        """Clean up client on deletion (fallback, not guaranteed to run)."""
        if not getattr(self, "_closed", True):
            self.close()

    def _request_with_retry(
        self,
        method: str,
        url: str,
        idempotent: bool = True,
        **kwargs,
    ) -> httpx.Response:
        """
        Make an HTTP request with retry logic for transient failures.

        Retries all 5xx responses and network errors (httpx.RequestError,
        excluding timeouts) with exponential backoff. 4xx responses are
        wrapped as SandboxRequestError; 5xx that persist after retries are
        wrapped as SandboxServiceError.

        A non-idempotent request (one that runs a command) is retried only
        when the connection failed, so it never reached the executor: a 5xx
        or a dropped connection may come after the command ran (e.g. the
        gateway's 504 on a long /run), and a retry would run it again.

        Args:
            method: HTTP method (e.g., 'GET', 'POST')
            url: The URL to request
            idempotent: False for requests that must not run twice
            **kwargs: Additional arguments to pass to httpx

        Returns:
            Response object

        Raises:
            SandboxRequestError: On a non-retryable HTTP error (4xx)
            SandboxServiceError: On an HTTP 5xx error after retries are exhausted
            SandboxTimeoutError: On request timeout
            SandboxError: On network errors after retries are exhausted
        """
        # Set default timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        for attempt in range(_MAX_RETRIES + 1):
            delay = _retry_delay(attempt)  # None on the last attempt
            try:
                response = self._client.request(method, url, **kwargs)

                # Retry transient server errors (5xx) with backoff
                if response.status_code >= 500 and idempotent and delay is not None:
                    logger.debug(
                        f"Received {response.status_code} error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1})"
                    )
                    time.sleep(delay)
                    continue

                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and idempotent and delay is not None:
                    logger.debug(
                        f"Received {e.response.status_code} error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1})"
                    )
                    time.sleep(delay)
                    continue
                if e.response.status_code >= 500:
                    raise SandboxServiceError(
                        status_code=e.response.status_code,
                        message=e.response.text,
                    ) from e
                raise SandboxRequestError(
                    status_code=e.response.status_code,
                    body=e.response.text,
                ) from e
            except httpx.TimeoutException as e:
                raise SandboxTimeoutError(
                    f"Request timed out after "
                    f"{_timeout_seconds(kwargs.get('timeout', self.timeout)):g}s"
                ) from e
            except httpx.RequestError as e:
                # Transient network errors (connection refused, reset, ...)
                # are retried with the same backoff as server errors.
                retryable = idempotent or isinstance(e, httpx.ConnectError)
                if retryable and delay is not None:
                    logger.debug(
                        f"Network error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1}): {e}"
                    )
                    time.sleep(delay)
                    continue
                logger.warning(f"Request failed after {attempt} retries: {e}")
                raise SandboxError(f"Request to sandbox executor failed: {e}") from e

        # Unreachable in practice: every terminal path returns or raises.
        raise SandboxError(f"Request to {url} failed after {_MAX_RETRIES} retries")

    @contextlib.contextmanager
    def _open_stream(
        self,
        request: httpx.Request,
        expires_at: Optional[float],
    ) -> Iterator[httpx.Response]:
        """
        Send a streaming request, retrying only a failed connect.

        A failed connect never reached the executor, so the command did not
        start and can be sent again, with the same backoff as
        _request_with_retry. Nothing is retried once a response has come back,
        nor past expires_at (a time.monotonic() deadline).
        """
        attempt = 0
        while True:
            try:
                response = self._client.send(request, stream=True)
                break
            except httpx.ConnectError as e:
                delay = _retry_delay(attempt, expires_at)
                if delay is None:
                    raise
                attempt += 1
                logger.debug(
                    f"Connect failed, retrying... "
                    f"(attempt {attempt}/{_MAX_RETRIES + 1}): {e}"
                )
                time.sleep(delay)
        try:
            yield response
        finally:
            response.close()

    def health(self) -> Dict[str, str]:
        """
        Check the health status of the server.

        Uses a short timeout and no retries since callers (wait_ready)
        already handle polling with backoff.

        Returns:
            Dict with status information

        Raises:
            httpx.HTTPStatusError: If the health check fails
            httpx.TimeoutException: If the health check times out
        """
        response = self._client.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        return response.json()

    def run(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a shell command in the sandbox.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional timeout in seconds for the request, or an
                httpx.Timeout (httpx.Timeout(None) for no limit). Defaults to
                the client's timeout

        Returns:
            Dict containing stdout, stderr, error (if any), and exit code
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        request_timeout = timeout if timeout is not None else self.timeout
        response = self._request_with_retry(
            "POST",
            f"{self.base_url}/run",
            json=payload,
            timeout=request_timeout,
            idempotent=False,
        )
        return response.json()

    def run_streaming(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        connect_timeout: float = 10.0,
    ) -> Iterator[Dict[str, Any]]:
        """
        Execute a shell command in the sandbox and stream the output in real-time.

        This method uses Server-Sent Events (SSE) to stream command output line-by-line
        as it's produced. Use this for long-running commands where you want real-time
        output. For simple commands where buffered output is acceptable, use run() instead.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional time budget in seconds for the whole stream. Once
                it has passed, the stream is closed and SandboxTimeoutError is
                raised. Whether the command then stops is up to the executor.
                The budget is checked whenever a line arrives, keepalives
                (every 10 s) included, so the error can come up to one keepalive
                interval late. Without it, the stream runs until the command
                ends, and only a read silent for the client's timeout fails.
            connect_timeout: Timeout in seconds for connecting to the executor,
                10 by default and never more than timeout

        Yields:
            Dict events with the following types:

            - output events (as command produces output):
              {"stream": "stdout"|"stderr", "data": "line of output"}

            - complete event (when command finishes):
              {"code": <exit_code>, "error": false}

            - error event (if command fails to start):
              {"error": "error message"}

        Raises:
            SandboxTimeoutError: If connecting, a read or the timeout budget times out

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> for event in client.run_streaming("echo 'Hello'; sleep 1; echo 'World'"):
            ...     if "stream" in event:
            ...         print(f"{event['stream']}: {event['data']}")
            ...     elif "code" in event:
            ...         print(f"Exit code: {event['code']}")
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        # The executor sends a keepalive every 10 s, so the per-read timeout
        # only catches a dead connection: timeout is enforced as a deadline.
        read_timeout = timeout if timeout is not None else self.timeout
        if timeout is not None:
            connect_timeout = min(connect_timeout, timeout)
        request_timeout = httpx.Timeout(read_timeout, connect=connect_timeout)
        expires_at = time.monotonic() + timeout if timeout is not None else None
        request = self._client.build_request(
            "POST",
            f"{self.base_url}/run_streaming",
            json=payload,
            timeout=request_timeout,
        )
        try:
            with self._open_stream(request, expires_at) as response:
                if response.status_code >= 500:
                    response.read()
                    raise SandboxServiceError(
                        status_code=response.status_code,
                        message=response.text,
                    )
                response.raise_for_status()
                for line in response.iter_lines():
                    if expires_at is not None and time.monotonic() >= expires_at:
                        raise _command_timed_out(timeout)
                    event = _parse_sse_line(line)
                    if event is not None:
                        yield event
        except httpx.ConnectTimeout as e:
            raise SandboxTimeoutError(
                f"Connection timed out after {connect_timeout}s"
            ) from e
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(f"Request timed out after {read_timeout}s") from e
        except httpx.RequestError as e:
            # E.g. the instance is torn down mid-stream during a redeployment.
            raise SandboxError(f"Connection to sandbox lost: {e}") from e

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.

        Args:
            path: The file path to write to
            content: The content to write

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path, "content": content}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/write_file", json=payload
        )
        return response.json()

    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read content from a file.

        Args:
            path: The file path to read from

        Returns:
            Dict with file content and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/read_file", json=payload
        )
        return response.json()

    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            path: The file path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/delete_file", json=payload
        )
        return response.json()

    def make_dir(self, path: str) -> Dict[str, Any]:
        """
        Create a directory (including parent directories).

        Args:
            path: The directory path to create

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/make_dir", json=payload
        )
        return response.json()

    def delete_dir(self, path: str) -> Dict[str, Any]:
        """
        Recursively delete a directory and all its contents.

        Args:
            path: The directory path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/delete_dir", json=payload
        )
        return response.json()

    def list_dir(self, path: str) -> Dict[str, Any]:
        """
        List the contents of a directory.

        Args:
            path: The directory path to list

        Returns:
            Dict with entries list and error if any
        """
        payload = {"path": path}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/list_dir", json=payload
        )
        return response.json()

    def files_stat(self, path: str, hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Stat a file on the streamed /files routes (executor v0.0.24+).

        Args:
            path: The file path to stat
            hash: "sha256" to add the file's digest to the reply (regular
                files only; the executor answers 400 otherwise)

        Returns:
            FileEntry dict: type (file|dir|symlink|other), size, mode (octal
            string), mtime (RFC 3339 UTC, nanoseconds), sha256 when asked
        """
        params: Dict[str, Any] = {"path": path}
        if hash is not None:
            params["hash"] = hash
        response = self._request_with_retry(
            "GET",
            f"{self.base_url}/files/stat",
            params=params,
        )
        return response.json()

    def files_put(
        self,
        path: str,
        content: Union[bytes, Iterator[bytes], BinaryIO],
        mode: Optional[str] = None,
        parents: bool = False,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Stream content to a file through PUT /files (executor v0.0.24+).

        The executor writes to a temp file and renames it into place: readers
        never see a partial file and a failed upload leaves the destination
        as it was. The timeout bounds idle time (FILES_IDLE_TIMEOUT), not
        total transfer time. Not retried on network errors mid-stream: a
        streamed body cannot be replayed; only a connect-time failure (the
        request never left) is retried.

        Args:
            path: The destination path
            content: The bytes to write, streamed (constant memory)
            mode: Octal permission string, e.g. "0644"; the existing
                destination's mode is kept when omitted
            parents: Create missing parent directories
            sha256: Expected content digest; the executor verifies it while
                streaming and fails with 400 on mismatch
            timeout: Seconds without progress before the call fails
                (default FILES_IDLE_TIMEOUT)

        Returns:
            {"size": received bytes, "sha256": content digest}
        """
        params: Dict[str, Any] = {"path": path}
        if mode is not None:
            params["mode"] = mode
        if parents:
            params["parents"] = "1"
        headers = {"Content-Type": "application/octet-stream"}
        if sha256:
            headers["X-Content-SHA256"] = sha256
        response = self._request_with_retry(
            "PUT",
            f"{self.base_url}/files",
            params=params,
            content=content,
            headers=headers,
            idempotent=False,
            timeout=_override_timeout(timeout, _FILES_TIMEOUT),
        )
        return response.json()

    def files_read(
        self, path: str, chunk_size: int = 65536, timeout: Optional[float] = None
    ) -> Iterator[bytes]:
        """
        Stream a file's bytes from GET /files (executor v0.0.24+).

        The executor serves Range requests; this stream is the whole file,
        chunk by chunk, constant memory on both sides. The timeout bounds
        idle time, not total download time. No retry: a broken stream is
        the fs layer's to resume.

        Args:
            path: The file path to read
            chunk_size: Bytes per yielded chunk
            timeout: Seconds without progress before the stream fails
                (default FILES_IDLE_TIMEOUT)

        Yields:
            File content chunks
        """
        bound = _override_timeout(timeout, _FILES_TIMEOUT)
        try:
            with self._client.stream(
                "GET",
                f"{self.base_url}/files",
                params={"path": path},
                timeout=bound,
            ) as response:
                if response.status_code >= 400:
                    response.read()
                    _raise_for_status(response)
                for chunk in response.iter_bytes(chunk_size):
                    yield chunk
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(bound):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    def has_files_routes(self) -> bool:
        """
        Whether this sandbox's executor serves the streamed /files routes.

        Probes once per handle with a body-less GET /files/stat: the legacy
        executor (pre-v0.0.24) has no such route and answers 404, the new one
        answers 400 ("path is required"). The result is cached for the
        client's lifetime, so every handle warns at most once.

        Never inferred from a failed transfer: an early 404 on a large PUT
        can surface as a Cloudflare 502 on Nomad.

        Returns:
            True if the streamed /files routes are available
        """
        if self._files_routes is None:
            try:
                self._request_with_retry("GET", f"{self.base_url}/files/stat")
            except SandboxRequestError as e:
                verdict = _probe_verdict(e.status_code)
                if not verdict:
                    logger.warning(_LEGACY_FILES_WARNING)
                self._files_routes = verdict
            else:
                self._files_routes = True
        return self._files_routes

    def files_list(
        self, path: str, recursive: bool = False
    ) -> Iterator[Dict[str, Any]]:
        """
        Stream a directory listing from GET /files/list (executor v0.0.24+).

        One JSON entry per line, yielded as the walk goes: a large tree is
        never held in memory. An entry the executor could not read carries
        an "error" field and the listing goes on. The timeout bounds idle
        time, not total listing time.

        Args:
            path: The directory to list
            recursive: Walk into subdirectories (a flat listing skips them)

        Yields:
            FileEntry dicts: path (relative, /-separated), type, size,
            mode (octal string), mtime (RFC 3339 UTC, nanoseconds)
        """
        params: Dict[str, Any] = {"path": path}
        if recursive:
            params["recursive"] = "1"
        try:
            with self._client.stream(
                "GET",
                f"{self.base_url}/files/list",
                params=params,
                timeout=_FILES_TIMEOUT,
            ) as response:
                if response.status_code >= 400:
                    response.read()
                    _raise_for_status(response)
                for line in response.iter_lines():
                    if line.strip():
                        yield json.loads(line)
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(_FILES_TIMEOUT):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    def files_archive_get(
        self, path: str, exclude: Sequence[str] = ()
    ) -> Iterator[bytes]:
        """
        Stream a directory as a gzip'd tar from GET /files/archive
        (executor v0.0.24+).

        The root itself is not an entry; symlinks are archived as links and
        special files are skipped. The timeout bounds idle time, not total
        archive time.

        Args:
            path: The directory to archive
            exclude: Glob patterns; a matching path (or any /-separated
                suffix of it) is left out, a matching directory whole

        Yields:
            The archive's gzip bytes, chunk by chunk
        """
        params: Dict[str, Any] = {"path": path}
        excludes = list(exclude)
        if excludes:
            params["exclude"] = excludes
        try:
            with self._client.stream(
                "GET",
                f"{self.base_url}/files/archive",
                params=params,
                timeout=_FILES_TIMEOUT,
            ) as response:
                if response.status_code >= 400:
                    response.read()
                    _raise_for_status(response)
                for chunk in response.iter_bytes(65536):
                    yield chunk
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(_FILES_TIMEOUT):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    def files_archive_put(
        self,
        path: str,
        content: Union[bytes, Iterator[bytes], BinaryIO],
    ) -> Dict[str, Any]:
        """
        Extract a gzip'd tar into the directory at path (executor v0.0.24+).

        The executor creates the directory when missing and refuses
        members that escape it (absolute paths, '..', links leaving the
        root). Entries already extracted stay in place when the stream
        ends short. Not retried on network errors mid-stream: a streamed
        body cannot be replayed; only a connect-time failure (the request
        never left) is retried.

        Args:
            path: The destination directory
            content: The archive's gzip bytes, streamed (constant memory)

        Returns:
            {"files": extracted file count, "bytes": extracted file bytes}
        """
        response = self._request_with_retry(
            "PUT",
            f"{self.base_url}/files/archive",
            params={"path": path},
            content=content,
            headers={"Content-Type": "application/octet-stream"},
            idempotent=False,
            timeout=_FILES_TIMEOUT,
        )
        return response.json()

    def files_upload_open(
        self,
        path: str,
        size: int,
        mode: Optional[str] = None,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Open a multipart upload session (executor v0.0.24+).

        A file too large for one request uploads as offset-addressed parts:
        the executor truncates a temp file to `size` up front, so parts land
        in any order, in parallel, and a retried part overwrites the same
        bytes. Sessions live in memory — an executor restart or an idle hour
        loses them, and the upload starts over.

        Args:
            path: The destination path
            size: The final size in bytes
            mode: Octal permission string, e.g. "0644" (the existing
                destination's mode is kept when omitted)
            sha256: Expected whole-file digest, checked once at complete
            timeout: Seconds without progress before this call fails
                (default DEFAULT_HTTP_TIMEOUT — a control call)

        Returns:
            {"upload_id", "max_part_size"} — the cap for every part
        """
        payload: Dict[str, Any] = {"path": path, "size": size}
        if mode is not None:
            payload["mode"] = mode
        if sha256:
            payload["sha256"] = sha256
        response = self._request_with_retry(
            "POST",
            f"{self.base_url}/files/uploads",
            json=payload,
            idempotent=False,
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    def files_upload_part(
        self,
        upload_id: str,
        offset: int,
        content: bytes,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """
        Write one part at its offset (executor v0.0.24+).

        The timeout bounds idle time, not the part's total time. A part is
        idempotent at the executor (a WriteAt of the same bytes), so
        transient network errors retry — the bytes must be replayable:
        callers pass the part's bytes, never a consumed stream.

        Args:
            upload_id: The session from files_upload_open
            offset: The part's position in the final file
            content: The part's bytes
            sha256: The part's digest, verified while streaming
            timeout: Seconds without progress before the part fails
                (default FILES_IDLE_TIMEOUT)
        """
        headers = {"Content-Type": "application/octet-stream"}
        if sha256:
            headers["X-Content-SHA256"] = sha256
        self._request_with_retry(
            "PUT",
            f"{self.base_url}/files/uploads/{upload_id}",
            params={"offset": offset},
            content=content,
            headers=headers,
            idempotent=True,
            timeout=_override_timeout(timeout, _FILES_TIMEOUT),
        )

    def files_upload_status(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        The ranges received so far (executor v0.0.24+): half-open
        [start, end) spans, sorted and coalesced, so a live session can
        resume by sending what is missing.

        Args:
            upload_id: The session to inspect

        Returns:
            {"size", "ranges": [{"start", "end"}, ...]}
        """
        response = self._request_with_retry(
            "GET",
            f"{self.base_url}/files/uploads/{upload_id}",
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    def files_upload_complete(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Check coverage and commit (executor v0.0.24+).

        A 409 carries the missing ranges in the error body — the session
        stays live, so the caller can fill the gaps and complete again. On
        success the temp file is fsynced and renamed onto the destination;
        the whole-file sha256 from files_upload_open is checked here.

        Args:
            upload_id: The session to complete

        Returns:
            {"size", "sha256"?}
        """
        response = self._request_with_retry(
            "POST",
            f"{self.base_url}/files/uploads/{upload_id}/complete",
            idempotent=False,
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    def files_upload_abort(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> None:
        """
        Abort the session and remove its temp file (executor v0.0.24+).

        Args:
            upload_id: The session to abort
            timeout: Seconds without progress before this call fails
                (default DEFAULT_HTTP_TIMEOUT — a control call)
        """
        self._request_with_retry(
            "DELETE",
            f"{self.base_url}/files/uploads/{upload_id}",
            timeout=_override_timeout(timeout, self.timeout),
        )

    def bind_port(self, port: int) -> Dict[str, Any]:
        """
        Bind a port to the TCP proxy for external access.

        Configures the TCP proxy to forward traffic to the specified port inside the sandbox.
        This allows you to expose services running inside the sandbox to external connections.

        Args:
            port: The port number to bind to (must be a valid port number)

        Returns:
            Dict with success status, message, and port information

        Notes:
            - Only one port can be bound at a time
            - Binding a new port will override the previous binding
            - The port must be available and accessible within the sandbox environment
        """
        payload = {"port": str(port)}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/bind_port", json=payload
        )
        return response.json()

    def unbind_port(self, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Unbind a port from the TCP proxy.

        Removes the TCP proxy port binding, stopping traffic forwarding to the previously bound port.

        Args:
            port: Optional port number to unbind. If provided, it must match the currently bound port.
                If not provided, any existing binding will be removed.

        Returns:
            Dict with success status and message

        Notes:
            - If a port is specified and doesn't match the currently bound port, the request will fail
            - After unbinding, the TCP proxy will no longer forward traffic
        """
        payload: Dict[str, Any] = {}
        if port is not None:
            payload["port"] = str(port)
        response = self._request_with_retry(
            "POST", f"{self.base_url}/unbind_port", json=payload
        )
        return response.json()

    def start_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Start a background process in the sandbox.

        Starts a long-running background process that continues executing even after
        the API call completes. Use this for servers, workers, or other long-running tasks.

        Args:
            cmd: The shell command to execute as a background process
            cwd: Optional working directory for the process
            env: Optional environment variables to set/override for the process

        Returns:
            Dict with process id and success status:
                - id: The unique process ID (UUID string)
                - success: True if the process was started successfully

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.start_process("python -u server.py")
            >>> process_id = result["id"]
            >>> print(f"Started process: {process_id}")
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env
        response = self._request_with_retry(
            "POST", f"{self.base_url}/start_process", json=payload, idempotent=False
        )
        return response.json()

    def kill_process(self, process_id: str) -> Dict[str, Any]:
        """
        Kill a background process by its ID.

        Terminates a running background process. This sends a SIGTERM signal to the process,
        allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
        it will be forcefully killed with SIGKILL.

        Args:
            process_id: The unique process ID (UUID string) to kill

        Returns:
            Dict with success status and error message if any

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.kill_process("550e8400-e29b-41d4-a716-446655440000")
            >>> if result.get("success"):
            ...     print("Process killed successfully")
        """
        payload = {"id": process_id}
        response = self._request_with_retry(
            "POST", f"{self.base_url}/kill_process", json=payload
        )
        return response.json()

    def list_processes(self) -> Dict[str, Any]:
        """
        List all background processes.

        Returns information about all currently running and recently completed background
        processes. This includes both active processes and processes that have completed
        (which remain in memory until server restart).

        Returns:
            Dict with a list of processes:
                - processes: List of process objects, each containing:
                    - id: Process ID (UUID string)
                    - command: The command that was executed
                    - status: Process status (e.g., "running", "completed")
                    - pid: OS process ID (if running)
                    - exit_code: Exit code (if completed)
                    - started_at: ISO 8601 timestamp when process started
                    - completed_at: ISO 8601 timestamp when process completed (if applicable)

        Example:
            >>> client = SandboxClient("http://localhost:8080", "secret")
            >>> result = client.list_processes()
            >>> for process in result.get("processes", []):
            ...     print(f"{process['id']}: {process['command']} - {process['status']}")
        """
        response = self._request_with_retry("GET", f"{self.base_url}/list_processes")
        return response.json()


class AsyncSandboxClient:
    """Async client for the Sandbox Executor API using httpx."""

    def __init__(
        self, conn_info: ConnectionInfo, timeout: float = DEFAULT_HTTP_TIMEOUT
    ):
        """
        Initialize the Async Sandbox Client.

        Args:
            conn_info: The parameters needed to connect to the sandbox
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = conn_info.public_url.rstrip("/")
        self.secret = conn_info.secret
        self.timeout = timeout
        self.headers = _build_headers(conn_info)
        self._client = httpx.AsyncClient(headers=self.headers, trust_env=True)
        self._closed = False
        # Cached result of has_files_routes(): None = not probed yet.
        self._files_routes: Optional[bool] = None

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        if not getattr(self, "_closed", True) and hasattr(self, "_client"):
            await self._client.aclose()
            self._closed = True

    async def __aenter__(self):
        """Async context manager entry - returns self."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - automatically closes the client."""
        await self.close()

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        idempotent: bool = True,
        **kwargs,
    ) -> httpx.Response:
        """
        Make an HTTP request with retry logic for transient failures.

        Retries all 5xx responses and network errors (httpx.RequestError,
        excluding timeouts) with exponential backoff. 4xx responses are
        wrapped as SandboxRequestError; 5xx that persist after retries are
        wrapped as SandboxServiceError.

        A non-idempotent request (one that runs a command) is retried only
        when the connection failed, so it never reached the executor: a 5xx
        or a dropped connection may come after the command ran (e.g. the
        gateway's 504 on a long /run), and a retry would run it again.

        Args:
            method: HTTP method (e.g., 'GET', 'POST')
            url: The URL to request
            idempotent: False for requests that must not run twice
            **kwargs: Additional arguments to pass to httpx

        Returns:
            Response object

        Raises:
            SandboxRequestError: On a non-retryable HTTP error (4xx)
            SandboxServiceError: On an HTTP 5xx error after retries are exhausted
            SandboxTimeoutError: On request timeout
            SandboxError: On network errors after retries are exhausted
        """
        # Set default timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        for attempt in range(_MAX_RETRIES + 1):
            delay = _retry_delay(attempt)  # None on the last attempt
            try:
                response = await self._client.request(method, url, **kwargs)

                # Retry transient server errors (5xx) with backoff
                if response.status_code >= 500 and idempotent and delay is not None:
                    logger.debug(
                        f"Received {response.status_code} error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1})"
                    )
                    await asyncio.sleep(delay)
                    continue

                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and idempotent and delay is not None:
                    logger.debug(
                        f"Received {e.response.status_code} error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1})"
                    )
                    await asyncio.sleep(delay)
                    continue
                if e.response.status_code >= 500:
                    raise SandboxServiceError(
                        status_code=e.response.status_code,
                        message=e.response.text,
                    ) from e
                raise SandboxRequestError(
                    status_code=e.response.status_code,
                    body=e.response.text,
                ) from e
            except httpx.TimeoutException as e:
                raise SandboxTimeoutError(
                    f"Request timed out after "
                    f"{_timeout_seconds(kwargs.get('timeout', self.timeout)):g}s"
                ) from e
            except httpx.RequestError as e:
                # Transient network errors (connection refused, reset, ...)
                # are retried with the same backoff as server errors.
                retryable = idempotent or isinstance(e, httpx.ConnectError)
                if retryable and delay is not None:
                    logger.debug(
                        f"Network error, retrying... "
                        f"(attempt {attempt + 1}/{_MAX_RETRIES + 1}): {e}"
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.warning(f"Request failed after {attempt} retries: {e}")
                raise SandboxError(f"Request to sandbox executor failed: {e}") from e

        # Unreachable in practice: every terminal path returns or raises.
        raise SandboxError(f"Request to {url} failed after {_MAX_RETRIES} retries")

    @contextlib.asynccontextmanager
    async def _open_stream(
        self,
        request: httpx.Request,
        expires_at: Optional[float],
    ) -> AsyncIterator[httpx.Response]:
        """
        Send a streaming request, retrying only a failed connect.

        A failed connect never reached the executor, so the command did not
        start and can be sent again, with the same backoff as
        _request_with_retry. Nothing is retried once a response has come back,
        nor past expires_at (a time.monotonic() deadline).
        """
        attempt = 0
        while True:
            try:
                response = await self._client.send(request, stream=True)
                break
            except httpx.ConnectError as e:
                delay = _retry_delay(attempt, expires_at)
                if delay is None:
                    raise
                attempt += 1
                logger.debug(
                    f"Connect failed, retrying... "
                    f"(attempt {attempt}/{_MAX_RETRIES + 1}): {e}"
                )
                await asyncio.sleep(delay)
        try:
            yield response
        finally:
            await response.aclose()

    async def health(self) -> Dict[str, str]:
        """
        Check the health status of the server.

        Uses a short timeout and no retries since callers (wait_ready)
        already handle polling with backoff.

        Returns:
            Dict with status information

        Raises:
            httpx.HTTPStatusError: If the health check fails
            httpx.TimeoutException: If the health check times out
        """
        response = await self._client.get(f"{self.base_url}/health", timeout=5)
        response.raise_for_status()
        return response.json()

    async def run(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a shell command in the sandbox.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional timeout in seconds for the request, or an
                httpx.Timeout (httpx.Timeout(None) for no limit). Defaults to
                the client's timeout

        Returns:
            Dict containing stdout, stderr, error (if any), and exit code
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        request_timeout = timeout if timeout is not None else self.timeout
        response = await self._request_with_retry(
            "POST",
            f"{self.base_url}/run",
            json=payload,
            timeout=request_timeout,
            idempotent=False,
        )
        return response.json()

    async def run_streaming(
        self,
        cmd: str,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        connect_timeout: float = 10.0,
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Execute a shell command in the sandbox and stream the output in real-time.

        This method uses Server-Sent Events (SSE) to stream command output line-by-line
        as it's produced. Use this for long-running commands where you want real-time
        output. For simple commands where buffered output is acceptable, use run() instead.

        Args:
            cmd: The shell command to execute
            cwd: Optional working directory for command execution
            env: Optional environment variables to set/override
            timeout: Optional time budget in seconds for the whole stream. Once
                it has passed, the stream is closed and SandboxTimeoutError is
                raised. Whether the command then stops is up to the executor.
                Without it, the stream runs until the command ends, and only a
                read silent for the client's timeout fails.
            connect_timeout: Timeout in seconds for connecting to the executor,
                10 by default and never more than timeout

        Yields:
            Dict events with the following types:

            - output events (as command produces output):
              {"stream": "stdout"|"stderr", "data": "line of output"}

            - complete event (when command finishes):
              {"code": <exit_code>, "error": false}

            - error event (if command fails to start):
              {"error": "error message"}

        Raises:
            SandboxTimeoutError: If connecting, a read or the timeout budget times out

        Example:
            >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
            >>> async for event in client.run_streaming("echo 'Hello'; sleep 1; echo 'World'"):
            ...     if "stream" in event:
            ...         print(f"{event['stream']}: {event['data']}")
            ...     elif "code" in event:
            ...         print(f"Exit code: {event['code']}")
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env

        # The executor sends a keepalive every 10 s, so the per-read timeout
        # only catches a dead connection: timeout is enforced as a deadline.
        read_timeout = timeout if timeout is not None else self.timeout
        if timeout is not None:
            connect_timeout = min(connect_timeout, timeout)
        request_timeout = httpx.Timeout(read_timeout, connect=connect_timeout)
        expires_at = time.monotonic() + timeout if timeout is not None else None
        request = self._client.build_request(
            "POST",
            f"{self.base_url}/run_streaming",
            json=payload,
            timeout=request_timeout,
        )
        try:
            async with self._open_stream(request, expires_at) as response:
                if response.status_code >= 500:
                    await response.aread()
                    raise SandboxServiceError(
                        status_code=response.status_code,
                        message=response.text,
                    )
                response.raise_for_status()
                lines = response.aiter_lines()
                while True:
                    try:
                        if expires_at is None:
                            line = await lines.__anext__()
                        else:
                            line = await asyncio.wait_for(
                                lines.__anext__(), expires_at - time.monotonic()
                            )
                    except StopAsyncIteration:
                        break
                    except asyncio.TimeoutError as e:
                        raise _command_timed_out(timeout) from e
                    event = _parse_sse_line(line)
                    if event is not None:
                        yield event
        except httpx.ConnectTimeout as e:
            raise SandboxTimeoutError(
                f"Connection timed out after {connect_timeout}s"
            ) from e
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(f"Request timed out after {read_timeout}s") from e
        except httpx.RequestError as e:
            # E.g. the instance is torn down mid-stream during a redeployment.
            raise SandboxError(f"Connection to sandbox lost: {e}") from e

    async def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.

        Args:
            path: The file path to write to
            content: The content to write

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path, "content": content}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/write_file", json=payload
        )
        return response.json()

    async def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read content from a file.

        Args:
            path: The file path to read from

        Returns:
            Dict with file content and error if any
        """
        payload = {"path": path}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/read_file", json=payload
        )
        return response.json()

    async def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            path: The file path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/delete_file", json=payload
        )
        return response.json()

    async def make_dir(self, path: str) -> Dict[str, Any]:
        """
        Create a directory (including parent directories).

        Args:
            path: The directory path to create

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/make_dir", json=payload
        )
        return response.json()

    async def delete_dir(self, path: str) -> Dict[str, Any]:
        """
        Recursively delete a directory and all its contents.

        Args:
            path: The directory path to delete

        Returns:
            Dict with success status and error if any
        """
        payload = {"path": path}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/delete_dir", json=payload
        )
        return response.json()

    async def list_dir(self, path: str) -> Dict[str, Any]:
        """
        List the contents of a directory.

        Args:
            path: The directory path to list

        Returns:
            Dict with entries list and error if any
        """
        payload = {"path": path}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/list_dir", json=payload
        )
        return response.json()

    async def files_stat(self, path: str, hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Stat a file on the streamed /files routes (executor v0.0.24+).

        Args:
            path: The file path to stat
            hash: "sha256" to add the file's digest to the reply (regular
                files only; the executor answers 400 otherwise)

        Returns:
            FileEntry dict: type (file|dir|symlink|other), size, mode (octal
            string), mtime (RFC 3339 UTC, nanoseconds), sha256 when asked
        """
        params: Dict[str, Any] = {"path": path}
        if hash is not None:
            params["hash"] = hash
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/files/stat",
            params=params,
        )
        return response.json()

    async def files_put(
        self,
        path: str,
        content: Union[bytes, AsyncIterator[bytes], Iterator[bytes], BinaryIO],
        mode: Optional[str] = None,
        parents: bool = False,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Stream content to a file through PUT /files (executor v0.0.24+).

        The executor writes to a temp file and renames it into place: readers
        never see a partial file and a failed upload leaves the destination
        as it was. The timeout bounds idle time (FILES_IDLE_TIMEOUT), not
        total transfer time. Not retried on network errors mid-stream: a
        streamed body cannot be replayed; only a connect-time failure (the
        request never left) is retried.

        Args:
            path: The destination path
            content: The bytes to write, streamed (constant memory)
            mode: Octal permission string, e.g. "0644"; the existing
                destination's mode is kept when omitted
            parents: Create missing parent directories
            sha256: Expected content digest; the executor verifies it while
                streaming and fails with 400 on mismatch
            timeout: Seconds without progress before the call fails
                (default FILES_IDLE_TIMEOUT)

        Returns:
            {"size": received bytes, "sha256": content digest}
        """
        params: Dict[str, Any] = {"path": path}
        if mode is not None:
            params["mode"] = mode
        if parents:
            params["parents"] = "1"
        headers = {"Content-Type": "application/octet-stream"}
        if sha256:
            headers["X-Content-SHA256"] = sha256
        if isinstance(content, (bytes, bytearray, str)) or hasattr(
            content, "__aiter__"
        ):
            body = content
        else:
            body = _async_stream(content)
        response = await self._request_with_retry(
            "PUT",
            f"{self.base_url}/files",
            params=params,
            content=body,
            headers=headers,
            idempotent=False,
            timeout=_override_timeout(timeout, _FILES_TIMEOUT),
        )
        return response.json()

    async def files_read(
        self, path: str, chunk_size: int = 65536, timeout: Optional[float] = None
    ) -> AsyncIterator[bytes]:
        """
        Stream a file's bytes from GET /files (executor v0.0.24+).

        The executor serves Range requests; this stream is the whole file,
        chunk by chunk, constant memory on both sides. The timeout bounds
        idle time, not total download time. No retry: a broken stream is
        the fs layer's to resume.

        Args:
            path: The file path to read
            chunk_size: Bytes per yielded chunk
            timeout: Seconds without progress before the stream fails
                (default FILES_IDLE_TIMEOUT)

        Yields:
            File content chunks
        """
        bound = _override_timeout(timeout, _FILES_TIMEOUT)
        try:
            async with self._client.stream(
                "GET",
                f"{self.base_url}/files",
                params={"path": path},
                timeout=bound,
            ) as response:
                if response.status_code >= 400:
                    await response.aread()
                    _raise_for_status(response)
                async for chunk in response.aiter_bytes(chunk_size):
                    yield chunk
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(bound):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    async def has_files_routes(self) -> bool:
        """
        Whether this sandbox's executor serves the streamed /files routes.

        Probes once per handle with a body-less GET /files/stat: the legacy
        executor (pre-v0.0.24) has no such route and answers 404, the new one
        answers 400 ("path is required"). The result is cached for the
        client's lifetime, so every handle warns at most once.

        Never inferred from a failed transfer: an early 404 on a large PUT
        can surface as a Cloudflare 502 on Nomad.

        Returns:
            True if the streamed /files routes are available
        """
        if self._files_routes is None:
            try:
                await self._request_with_retry("GET", f"{self.base_url}/files/stat")
            except SandboxRequestError as e:
                verdict = _probe_verdict(e.status_code)
                if not verdict:
                    logger.warning(_LEGACY_FILES_WARNING)
                self._files_routes = verdict
            else:
                self._files_routes = True
        return self._files_routes

    async def files_list(
        self, path: str, recursive: bool = False
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Stream a directory listing from GET /files/list (executor v0.0.24+).

        One JSON entry per line, yielded as the walk goes: a large tree is
        never held in memory. An entry the executor could not read carries
        an "error" field and the listing goes on. The timeout bounds idle
        time, not total listing time.

        Args:
            path: The directory to list
            recursive: Walk into subdirectories (a flat listing skips them)

        Yields:
            FileEntry dicts: path (relative, /-separated), type, size,
            mode (octal string), mtime (RFC 3339 UTC, nanoseconds)
        """
        params: Dict[str, Any] = {"path": path}
        if recursive:
            params["recursive"] = "1"
        try:
            async with self._client.stream(
                "GET",
                f"{self.base_url}/files/list",
                params=params,
                timeout=_FILES_TIMEOUT,
            ) as response:
                if response.status_code >= 400:
                    await response.aread()
                    _raise_for_status(response)
                async for line in response.aiter_lines():
                    if line.strip():
                        yield json.loads(line)
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(_FILES_TIMEOUT):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    async def files_archive_get(
        self, path: str, exclude: Sequence[str] = ()
    ) -> AsyncIterator[bytes]:
        """
        Stream a directory as a gzip'd tar from GET /files/archive
        (executor v0.0.24+).

        The root itself is not an entry; symlinks are archived as links and
        special files are skipped. The timeout bounds idle time, not total
        archive time.

        Args:
            path: The directory to archive
            exclude: Glob patterns; a matching path (or any /-separated
                suffix of it) is left out, a matching directory whole

        Yields:
            The archive's gzip bytes, chunk by chunk
        """
        params: Dict[str, Any] = {"path": path}
        excludes = list(exclude)
        if excludes:
            params["exclude"] = excludes
        try:
            async with self._client.stream(
                "GET",
                f"{self.base_url}/files/archive",
                params=params,
                timeout=_FILES_TIMEOUT,
            ) as response:
                if response.status_code >= 400:
                    await response.aread()
                    _raise_for_status(response)
                async for chunk in response.aiter_bytes(65536):
                    yield chunk
        except httpx.TimeoutException as e:
            raise SandboxTimeoutError(
                f"Request timed out after {_timeout_seconds(_FILES_TIMEOUT):g}s"
            ) from e
        except httpx.RequestError as e:
            raise SandboxError(f"Request to sandbox executor failed: {e}") from e

    async def files_archive_put(
        self,
        path: str,
        content: Union[bytes, AsyncIterator[bytes], Iterator[bytes], BinaryIO],
    ) -> Dict[str, Any]:
        """
        Extract a gzip'd tar into the directory at path (executor v0.0.24+).

        The executor creates the directory when missing and refuses
        members that escape it (absolute paths, '..', links leaving the
        root). Entries already extracted stay in place when the stream
        ends short. Not retried on network errors mid-stream: a streamed
        body cannot be replayed; only a connect-time failure (the request
        never left) is retried.

        Args:
            path: The destination directory
            content: The archive's gzip bytes, streamed (constant memory)

        Returns:
            {"files": extracted file count, "bytes": extracted file bytes}
        """
        if isinstance(content, (bytes, bytearray, str)) or hasattr(
            content, "__aiter__"
        ):
            body = content
        else:
            body = _async_stream(content)
        response = await self._request_with_retry(
            "PUT",
            f"{self.base_url}/files/archive",
            params={"path": path},
            content=body,
            headers={"Content-Type": "application/octet-stream"},
            idempotent=False,
            timeout=_FILES_TIMEOUT,
        )
        return response.json()

    async def files_upload_open(
        self,
        path: str,
        size: int,
        mode: Optional[str] = None,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Open a multipart upload session (executor v0.0.24+).

        A file too large for one request uploads as offset-addressed parts:
        the executor truncates a temp file to `size` up front, so parts land
        in any order, in parallel, and a retried part overwrites the same
        bytes. Sessions live in memory — an executor restart or an idle hour
        loses them, and the upload starts over.

        Args:
            path: The destination path
            size: The final size in bytes
            mode: Octal permission string, e.g. "0644" (the existing
                destination's mode is kept when omitted)
            sha256: Expected whole-file digest, checked once at complete
            timeout: Seconds without progress before this call fails
                (default DEFAULT_HTTP_TIMEOUT — a control call)

        Returns:
            {"upload_id", "max_part_size"} — the cap for every part
        """
        payload: Dict[str, Any] = {"path": path, "size": size}
        if mode is not None:
            payload["mode"] = mode
        if sha256:
            payload["sha256"] = sha256
        response = await self._request_with_retry(
            "POST",
            f"{self.base_url}/files/uploads",
            json=payload,
            idempotent=False,
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    async def files_upload_part(
        self,
        upload_id: str,
        offset: int,
        content: bytes,
        sha256: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """
        Write one part at its offset (executor v0.0.24+).

        The timeout bounds idle time, not the part's total time. A part is
        idempotent at the executor (a WriteAt of the same bytes), so
        transient network errors retry — the bytes must be replayable:
        callers pass the part's bytes, never a consumed stream.

        Args:
            upload_id: The session from files_upload_open
            offset: The part's position in the final file
            content: The part's bytes
            sha256: The part's digest, verified while streaming
            timeout: Seconds without progress before the part fails
                (default FILES_IDLE_TIMEOUT)
        """
        headers = {"Content-Type": "application/octet-stream"}
        if sha256:
            headers["X-Content-SHA256"] = sha256
        await self._request_with_retry(
            "PUT",
            f"{self.base_url}/files/uploads/{upload_id}",
            params={"offset": offset},
            content=content,
            headers=headers,
            idempotent=True,
            timeout=_override_timeout(timeout, _FILES_TIMEOUT),
        )

    async def files_upload_status(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        The ranges received so far (executor v0.0.24+): half-open
        [start, end) spans, sorted and coalesced, so a live session can
        resume by sending what is missing.

        Args:
            upload_id: The session to inspect

        Returns:
            {"size", "ranges": [{"start", "end"}, ...]}
        """
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/files/uploads/{upload_id}",
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    async def files_upload_complete(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Check coverage and commit (executor v0.0.24+).

        A 409 carries the missing ranges in the error body — the session
        stays live, so the caller can fill the gaps and complete again. On
        success the temp file is fsynced and renamed onto the destination;
        the whole-file sha256 from files_upload_open is checked here.

        Args:
            upload_id: The session to complete

        Returns:
            {"size", "sha256"?}
        """
        response = await self._request_with_retry(
            "POST",
            f"{self.base_url}/files/uploads/{upload_id}/complete",
            idempotent=False,
            timeout=_override_timeout(timeout, self.timeout),
        )
        return response.json()

    async def files_upload_abort(
        self, upload_id: str, timeout: Optional[float] = None
    ) -> None:
        """
        Abort the session and remove its temp file (executor v0.0.24+).

        Args:
            upload_id: The session to abort
            timeout: Seconds without progress before this call fails
                (default DEFAULT_HTTP_TIMEOUT — a control call)
        """
        await self._request_with_retry(
            "DELETE",
            f"{self.base_url}/files/uploads/{upload_id}",
            timeout=_override_timeout(timeout, self.timeout),
        )

    async def bind_port(self, port: int) -> Dict[str, Any]:
        """
        Bind a port to the TCP proxy for external access.

        Configures the TCP proxy to forward traffic to the specified port inside the sandbox.
        This allows you to expose services running inside the sandbox to external connections.

        Args:
            port: The port number to bind to (must be a valid port number)

        Returns:
            Dict with success status, message, and port information

        Notes:
            - Only one port can be bound at a time
            - Binding a new port will override the previous binding
            - The port must be available and accessible within the sandbox environment
        """
        payload = {"port": str(port)}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/bind_port", json=payload
        )
        return response.json()

    async def unbind_port(self, port: Optional[int] = None) -> Dict[str, Any]:
        """
        Unbind a port from the TCP proxy.

        Removes the TCP proxy port binding, stopping traffic forwarding to the previously bound port.

        Args:
            port: Optional port number to unbind. If provided, it must match the currently bound port.
                If not provided, any existing binding will be removed.

        Returns:
            Dict with success status and message

        Notes:
            - If a port is specified and doesn't match the currently bound port, the request will fail
            - After unbinding, the TCP proxy will no longer forward traffic
        """
        payload: Dict[str, Any] = {}
        if port is not None:
            payload["port"] = str(port)
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/unbind_port", json=payload
        )
        return response.json()

    async def start_process(
        self, cmd: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Start a background process in the sandbox.

        Starts a long-running background process that continues executing even after
        the API call completes. Use this for servers, workers, or other long-running tasks.

        Args:
            cmd: The shell command to execute as a background process
            cwd: Optional working directory for the process
            env: Optional environment variables to set/override for the process

        Returns:
            Dict with process id and success status:
                - id: The unique process ID (UUID string)
                - success: True if the process was started successfully

        Example:
            >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
            >>> result = await client.start_process("python -u server.py")
            >>> process_id = result["id"]
            >>> print(f"Started process: {process_id}")
        """
        payload: Dict[str, Any] = {"cmd": cmd}
        if cwd is not None:
            payload["cwd"] = cwd
        if env is not None:
            payload["env"] = env
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/start_process", json=payload, idempotent=False
        )
        return response.json()

    async def kill_process(self, process_id: str) -> Dict[str, Any]:
        """
        Kill a background process by its ID.

        Terminates a running background process. This sends a SIGTERM signal to the process,
        allowing it to clean up gracefully. If the process doesn't terminate within a timeout,
        it will be forcefully killed with SIGKILL.

        Args:
            process_id: The unique process ID (UUID string) to kill

        Returns:
            Dict with success status and error message if any

        Example:
            >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
            >>> result = await client.kill_process("550e8400-e29b-41d4-a716-446655440000")
            >>> if result.get("success"):
            ...     print("Process killed successfully")
        """
        payload = {"id": process_id}
        response = await self._request_with_retry(
            "POST", f"{self.base_url}/kill_process", json=payload
        )
        return response.json()

    async def list_processes(self) -> Dict[str, Any]:
        """
        List all background processes.

        Returns information about all currently running and recently completed background
        processes. This includes both active processes and processes that have completed
        (which remain in memory until server restart).

        Returns:
            Dict with a list of processes:
                - processes: List of process objects, each containing:
                    - id: Process ID (UUID string)
                    - command: The command that was executed
                    - status: Process status (e.g., "running", "completed")
                    - pid: OS process ID (if running)
                    - exit_code: Exit code (if completed)
                    - started_at: ISO 8601 timestamp when process started
                    - completed_at: ISO 8601 timestamp when process completed (if applicable)

        Example:
            >>> client = AsyncSandboxClient("http://localhost:8080", "secret")
            >>> result = await client.list_processes()
            >>> for process in result.get("processes", []):
            ...     print(f"{process['id']}: {process['command']} - {process['status']}")
        """
        response = await self._request_with_retry(
            "GET", f"{self.base_url}/list_processes"
        )
        return response.json()
