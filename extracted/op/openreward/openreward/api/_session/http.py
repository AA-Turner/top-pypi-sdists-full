import asyncio
import json as json_lib
from typing import Any, AsyncGenerator, Callable, Literal, Optional, Tuple

import aiohttp
from openreward._version import USER_AGENT
from openreward.log_utils import get_logger
from tenacity import (retry, retry_if_exception, stop_after_attempt,
                      wait_exponential)

logger = get_logger("openreward-session-client")


# RetryPolicy controls how aggressively we retry HTTP failures, scoped by
# what we know about the destination:
#
# - "api": broad. Retries any 5xx and 429. Used for calls into the
#   OpenReward API (api.openreward.ai), where a 500 might be a transient
#   downstream blip (DB, provisioner, etc.) and a retry can legitimately
#   succeed.
#
# - "env-server": narrow. Retries only the intermediary-class 5xx
#   ({429, 502, 503, 504}). A 500 from the env server means
#   ErrorHandlingMiddleware caught an unhandled exception in user code —
#   retrying just re-executes the same code path with the same outcome.
RetryPolicy = Literal["api", "env-server"]


_ENV_SERVER_RETRY_STATUSES = frozenset({429, 502, 503, 504})

# Per-ClientSession retry policy, looked up by identity. WeakKeyDictionary
# so we don't keep dead clients alive. Untagged clients (anything not
# explicitly registered) get the "api" default — which means bare
# MagicMock test clients also behave correctly without per-test setup.
import weakref as _weakref
_client_retry_policies: "_weakref.WeakKeyDictionary[Any, RetryPolicy]" = _weakref.WeakKeyDictionary()


def set_retry_policy(client: aiohttp.ClientSession, policy: RetryPolicy) -> None:
    """Set the default retry policy for *client*.

    Call once at construction time. resumable_sse / request_retryable
    will pick this up for every request made through the session.
    """
    _client_retry_policies[client] = policy


def _resolve_policy(client: aiohttp.ClientSession) -> RetryPolicy:
    return _client_retry_policies.get(client, "api")


def _is_retryable_http_error(
    exception: BaseException,
    policy: RetryPolicy = "api",
) -> bool:
    # Check ClientResponseError first — it's a subclass of ClientError, so
    # the broader isinstance check below would otherwise swallow it before
    # we can apply the policy-specific status check.
    if isinstance(exception, aiohttp.ClientResponseError):
        if policy == "env-server":
            return exception.status in _ENV_SERVER_RETRY_STATUSES
        # "api": broad retry on any 5xx + 429.
        return exception.status >= 500 or exception.status == 429
    if isinstance(exception, (aiohttp.ClientError, asyncio.TimeoutError)):
        return True  # Network/timeout errors (conn reset, DNS, payload, etc.)
    return False


class AuthenticationError(Exception):
    """Raised when API authentication fails (401 Unauthorized)"""
    pass


def _rebuild_response_error(status: int, message: str) -> "SessionResponseError":
    # request_info/history are dropped on pickle; None is accepted at runtime.
    return SessionResponseError(None, (), status=status, message=message)  # type: ignore[arg-type]


class SessionResponseError(aiohttp.ClientResponseError):
    """A ClientResponseError that survives pickling across a process/Ray boundary.

    aiohttp's ClientResponseError stores request_info/history/headers, which hold
    CIMultiDictProxy objects that cloudpickle cannot serialize. When an env 5xx/4xx
    is raised inside a Ray RolloutActor and propagates to the driver, cloudpickle
    raises a *secondary* ``TypeError: can't pickle
    multidict._multidict.CIMultiDictProxy``, masking the real HTTP status and
    turning a retryable env hiccup into a hard rollout failure. The live object
    stays fully populated (retry logic / logging still see the headers); only the
    *pickled* form is reduced to the picklable status + message.
    """
    def __reduce__(self):
        return (_rebuild_response_error, (self.status, self.message))


async def _raise_for_status(resp: aiohttp.ClientResponse) -> None:
    """Raise ClientResponseError with server's detail message if available."""
    if resp.ok:
        return
    text = await resp.text()
    try:
        detail = json_lib.loads(text).get("detail", text)
        if 'Deployment not found.' in detail:
            detail = 'Deployment not found. Environment name is case-sensitive, is it correct?'
    except Exception:
        detail = text
    # SessionResponseError (a ClientResponseError subclass) so this survives
    # cloudpickle when a Ray actor propagates it to the driver — see its docstring.
    raise SessionResponseError(
        resp.request_info, resp.history,
        status=resp.status,
        message=detail,
        headers=resp.headers,
    )


async def _raise_for_status_with_auth(resp: aiohttp.ClientResponse) -> None:
    """Like _raise_for_status but with a friendly message for 401s."""
    if resp.ok:
        return
    if resp.status == 401:
        text = await resp.text()
        RED = "\033[38;2;247;230;204m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
        raise AuthenticationError(
            f"\n\n{RED}{BOLD}"
            "═══════════════════════════════════════════════════════════════\n"
            "  Authentication Failed: Missing or Invalid API Key\n"
            "═══════════════════════════════════════════════════════════════"
            f"{RESET}\n\n"
            "Your request was rejected because:\n"
            f"  • {text}\n\n"
            "To fix this:\n"
            "  1. Get your API key from: https://openreward.ai/keys\n"
            "  2. Set it as an environment variable:\n"
            "     export OPENREWARD_API_KEY='your-api-key-here'\n"
            "  3. Or pass it directly to the client:\n"
            "     client = AsyncOpenReward(api_key='your-api-key-here')\n"
        )
    await _raise_for_status(resp)


async def _do_request(
    client: aiohttp.ClientSession,
    method: str,
    path: str,
    expect_json: bool,
    token: Optional[str],
    json: Optional[dict[str, Any]] = None,
    sid: Optional[str] = None,
    deployment: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
) -> Any:
    headers: dict[str, str] = {"User-Agent": USER_AGENT}
    if token is not None:
        headers["X-API-Key"] = token
    if sid:
        headers["X-Session-ID"] = sid
    if deployment:
        headers["X-Deployment"] = deployment
    if extra_headers:
        headers.update(extra_headers)

    async with client.request(method, path, headers=headers, json=json) as response:
        await _raise_for_status_with_auth(response)
        return await response.json() if expect_json else None


# Two policy-specific retry wrappers built up-front. tenacity's @retry
# binds the retry predicate at decoration time, so we can't make it
# dynamic — we dispatch to the right wrapper based on the client's tag.

_request_retryable_api = retry(
    retry=retry_if_exception(lambda e: _is_retryable_http_error(e, "api")),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)(_do_request)

_request_retryable_env_server = retry(
    retry=retry_if_exception(lambda e: _is_retryable_http_error(e, "env-server")),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)(_do_request)


async def request_retryable(
    client: aiohttp.ClientSession,
    method: str,
    path: str,
    expect_json: bool,
    token: Optional[str],
    json: Optional[dict[str, Any]] = None,
    sid: Optional[str] = None,
    deployment: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
) -> Any:
    """Perform an HTTP request with retry. Retry policy is read from the
    client (set via :func:`set_retry_policy` at construction time).
    Defaults to the "api" policy if untagged.
    """
    impl = (
        _request_retryable_env_server
        if _resolve_policy(client) == "env-server"
        else _request_retryable_api
    )
    return await impl(
        client, method, path, expect_json, token,
        json=json, sid=sid, deployment=deployment, extra_headers=extra_headers,
    )


# Defined in openreward.api.errors; re-exported here so existing imports of
# `from openreward.api._session.http import MaxRetriesError` keep working.
from openreward.api.errors import (
    HeartbeatTimeoutError,
    MaxRetriesError,
    SessionTerminatedError,
)


class _RemoteSSEError(RuntimeError):
    """Internal: server emitted an SSE ``error`` event mid-stream.

    Subclasses ``RuntimeError`` so any caller that catches RuntimeError
    (e.g. sandboxes' resumable-task helper at client.py:16) keeps
    working. New code should catch this class directly to distinguish a
    remote tool failure from other transient runtime errors.
    """


async def _parse_sse_events(
    response: aiohttp.ClientResponse,
) -> AsyncGenerator[Tuple[str, str], None]:
    """Parses an aiohttp response stream and yields SSE events."""
    event = None
    data_lines: list[str] = []
    async for raw_line in response.content:
        line = raw_line.decode("utf-8", "ignore").rstrip("\r\n")

        if not line:
            if event:
                yield event, "\n".join(data_lines)
            event = None
            data_lines = []
            continue

        if line.startswith(":"):
            continue

        field, value = line.split(":", 1)
        value = value.lstrip()

        if field == "event":
            event = value
        elif field == "data":
            data_lines.append(value)


async def resumable_sse(
    client: aiohttp.ClientSession,
    path: str,
    token: Optional[str],
    *,
    json: Optional[dict[str, Any]] = None,
    sid: Optional[str] = None,
    deployment: Optional[str] = None,
    task_id: Optional[str] = None,
    max_retries: Optional[int] = None,
    backoff_base: float = 0.5,
    backoff_max: float = 10.0,
    timeout: Optional[float] = None,
    heartbeat_timeout: int = 30,
    on_event: Callable[[str, str], None] = lambda _event, _data: None,
    extra_headers: Optional[dict[str, str]] = None,
) -> Any:
    """Stream an SSE response with retry. Retry policy is read from the
    client (set via :func:`set_retry_policy` at construction time).
    Defaults to the "api" policy if untagged.
    """

    retry_policy = _resolve_policy(client)
    client_timeout = aiohttp.ClientTimeout(total=None, sock_read=heartbeat_timeout)
    payload = dict(json or {})
    headers: dict[str, str] = {
        "Accept": "text/event-stream",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["X-API-Key"] = token
    if sid:
        headers["X-Session-ID"] = sid
    if deployment:
        headers["X-Deployment"] = deployment
    if extra_headers:
        headers.update(extra_headers)

    async def _execute_with_retries():
        nonlocal task_id, payload
        attempt = 0
        retry_errors: list[Exception] = []
        while True:
            if task_id:
                payload["task_id"] = task_id

            try:
                async with client.post(path, headers=headers, json=payload, timeout=client_timeout) as resp:
                    await _raise_for_status_with_auth(resp)
                    attempt = 0

                    chunks = []
                    async for event, data in _parse_sse_events(resp):
                        on_event(event, data)
                        if event == "task_id":
                            task_id = data.strip()
                        elif event == "chunk":
                            chunks.append(data)
                        elif event == "end":
                            chunks.append(data)
                            final_result = "".join(chunks)
                            if not final_result:
                                return None
                            return json_lib.loads(final_result)
                        elif event == "error":
                            raise _RemoteSSEError(data or "Unknown SSE error")

                    raise aiohttp.ClientPayloadError("Stream ended unexpectedly")

            except aiohttp.ClientResponseError as e:
                if not _is_retryable_http_error(e, retry_policy):
                    # 410 Gone on a session-bearing request: the server
                    # is unambiguously telling us the session has been
                    # deleted. Surface as SessionTerminatedError so the
                    # caller can distinguish it from a generic 4xx.
                    # 404 is intentionally NOT mapped here — it's
                    # ambiguous (could be wrong path / unknown env /
                    # missing session) and the caller is better placed
                    # to interpret it.
                    if sid is not None and e.status == 410:
                        raise SessionTerminatedError(
                            f"server returned 410: {e.message}",
                            sid=sid,
                        ) from e
                    raise e
                retry_errors.append(e)

            except aiohttp.ClientError as e:
                logger.debug("client_error: %s", e)
                retry_errors.append(e)

            except _RemoteSSEError:
                raise

            except asyncio.TimeoutError:
                raise HeartbeatTimeoutError()

            attempt += 1
            if max_retries is not None and attempt > max_retries:
                raise MaxRetriesError(
                    f"Exceeded {max_retries} retries for {path}",
                    errors=retry_errors,
                )

            delay = min(backoff_max, backoff_base * (2 ** (attempt - 1)))
            await asyncio.sleep(delay)

    try:
        return await asyncio.wait_for(_execute_with_retries(), timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Total operation timed out after {timeout} seconds.") from None


def _finalize_session(session: aiohttp.ClientSession):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        try:
            asyncio.run(session.close())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(session.close())
            loop.close()
    else:
        if not session.closed:
            loop.create_task(session.close())
