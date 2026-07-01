import asyncio
import logging
from typing import Any, ClassVar, Coroutine, Literal, Optional, Self

import aiohttp
from openreward.api._session.http import (
    RetryPolicy,
    _finalize_session,
    request_retryable,
    resumable_sse,
    set_retry_policy,
)
from openreward.api._session.ping import (
    _MAX_CONSECUTIVE_PING_FAILURES,
    ErrorResponse,
    ping,
    ping_thread,
)
# Defined in openreward.api.errors.
from openreward.api.errors import SessionTerminatedError


logger = logging.getLogger(__name__)


SessionKind = Literal["environment", "sandbox"]


class BaseAsyncSession:
    # Subclasses must override to identify the session kind in error messages
    # and start-up logs.
    _session_kind: ClassVar[SessionKind]
    # Retry policy applied to HTTP calls this session makes on behalf of
    # the user. Default "api" is safe for the platform API; env-bearing
    # subclasses (AsyncSession) override to "env-server" so 500s from
    # ErrorHandlingMiddleware don't get re-executed.
    _retry_policy: ClassVar[RetryPolicy] = "api"


    def __init__(
        self,
        base_url: str,
        api_key: Optional[str],
        creation_endpoint: str,
        creation_payload: dict[str, Any],
        creation_timeout: int = 60 * 30,
        deployment: Optional[str] = None,
        client: Optional[aiohttp.ClientSession] = None,
        default_headers: Optional[dict[str, str]] = None,
        creation_headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self._creation_endpoint = creation_endpoint
        self._creation_payload = creation_payload
        self.creation_timeout = creation_timeout
        self.deployment = deployment
        self._default_headers = default_headers
        self._creation_headers = creation_headers

        # External client: we don't own it, don't close it
        self._external_client = client
        # Our own client + connector, created in __aenter__ if no external client
        self._own_connector: Optional[aiohttp.TCPConnector] = None
        self._own_client: Optional[aiohttp.ClientSession] = None

        self.sid: Optional[str] = None
        self._pending_task_id: Optional[str] = None

        self._ping_task: asyncio.Task[None] | None = None
        self._dead = asyncio.Event()
        self._dead_exception: Optional[SessionTerminatedError] = None

    @property
    def client(self) -> aiohttp.ClientSession:
        c = self._external_client or self._own_client
        if c is None:
            raise RuntimeError("Session not started. Use as async context manager.")
        return c

    def _mark_dead(self, exc: ErrorResponse):
        if self._dead_exception is None:
            self._dead_exception = SessionTerminatedError(
                exc.message, sid=self.sid, kind=self._session_kind
            )
            self._dead.set()
            # Kick off server-side teardown eagerly so we don't keep
            # burning resources (sandbox compute, etc.) until __aexit__
            # or the server's 900s reaper. Idempotent with __aexit__'s
            # later cleanup — server's /delete is a no-op once the
            # session is gone.
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No running loop — nothing to schedule. __aexit__ will
                # still tear down whenever the caller exits.
                return
            loop.create_task(self._teardown_dead_session())

    async def _teardown_dead_session(self) -> None:
        """Best-effort server-side teardown after _mark_dead.

        Mirrors __aexit__'s `/delete` POST but leaves ping/client cleanup
        to __aexit__ — the handle is still alive and the caller may yet
        finalize it. Swallows all errors; this is fire-and-forget.
        """
        try:
            await self._pre_delete()
        except Exception as e:
            logger.debug(
                "eager_teardown_failed sid=%s kind=%s error=%s",
                self.sid, self._session_kind, e,
            )

    def _ensure_alive(self):
        if self._dead_exception is not None:
            raise self._dead_exception

    async def _run_or_die(self, coro: Coroutine[Any, Any, Any]) -> Any:
        """Run a coroutine until completion or until the session dies."""
        if self._dead_exception is not None:
            raise self._dead_exception

        task = asyncio.create_task(coro)
        stopper = asyncio.create_task(self._dead.wait())
        try:
            done, pending = await asyncio.wait(
                {task, stopper},
                return_when=asyncio.FIRST_COMPLETED,
            )

            if self._dead.is_set() and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                if self._dead_exception:
                    raise self._dead_exception

            return await task

        except SessionTerminatedError as e:
            # Any SessionTerminatedError propagating through here (e.g. a
            # 410 from resumable_sse) means the session is gone on the
            # server. Poison the local handle and fire eager teardown so
            # subsequent calls short-circuit and any server-side state is
            # released promptly. Idempotent — _mark_dead is a no-op if the
            # handle is already poisoned.
            self._mark_dead(ErrorResponse(type="error", message=str(e)))
            raise
        except Exception as e:
            raise self._annotate_error(e) from e.__cause__

        finally:
            stopper.cancel()
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    def _annotate_error(self, e: Exception) -> Exception:
        """Attach session context to *e* without changing its type.

        Where possible, splice the session prefix into ``e.args[0]`` so
        ``str(e)`` carries the sid (preserving the legacy format that
        callers may grep for). For exceptions with overridden ``__str__``
        or non-string args (e.g. aiohttp.ClientResponseError), fall back
        to ``add_note`` so we still capture the context without mangling
        their structured fields.

        Avoids the old approach of reconstructing via ``type(e)(msg)``,
        which silently downgraded any exception whose constructor didn't
        accept a single string (ClientResponseError, HeartbeatTimeoutError)
        to RuntimeError.
        """
        prefix = f"({self._session_kind} session sid={self.sid})"
        if (
            len(e.args) == 1
            and isinstance(e.args[0], str)
            and type(e).__str__ is BaseException.__str__
        ):
            e.args = (f"{prefix} {e.args[0]}",)
        else:
            e.add_note(prefix)
        return e

    async def _post_create(self) -> None:
        """Subclass hook called after SID is obtained. No-op in base."""
        pass

    async def _pre_delete(self) -> None:
        """Subclass hook called before session deletion. No-op in base."""
        pass

    async def _run_ping(
        self,
        url: str,
        sid: str,
        api_key: Optional[str],
        sleep_time: float,
        deployment: Optional[str],
        max_consecutive_failures: int = _MAX_CONSECUTIVE_PING_FAILURES,
    ) -> None:
        """Keepalive loop on a dedicated thread.

        Marks the session dead on:
          (a) a definitive server signal — `SessionTerminatedError`
              raised through the wrapped future; or
          (b) `max_consecutive_failures` (default 5) consecutive ping
              failures of any other kind.

        Single transient failures (timeouts, intermittent 5xx, network
        blips) are logged and retried — they no longer kill the session
        on the first error. The dedicated-thread design (see #1721) is
        preserved; only the failure-handling policy changes.
        """
        consecutive_failures = 0
        while True:
            future = ping_thread.schedule(
                url, sid, api_key, sleep_time, deployment,
            )
            try:
                await asyncio.wrap_future(future)
                # ping() loops forever internally. If it returns, treat
                # as a transient end-of-loop and reschedule.
                consecutive_failures = 0
            except SessionTerminatedError as e:
                # Definitive server-side termination. Mark dead immediately
                # — same behaviour as the original code for this case.
                self._mark_dead(ErrorResponse(type="error", message=str(e)))
                return
            except Exception as e:
                consecutive_failures += 1
                logger.warning(
                    "Ping failed sid=%s (%d/%d): %s: %s",
                    sid, consecutive_failures, max_consecutive_failures,
                    type(e).__name__, e,
                )
                if consecutive_failures >= max_consecutive_failures:
                    logger.error(
                        "Ping failed %d consecutive times for sid=%s; "
                        "marking session dead",
                        consecutive_failures, sid,
                    )
                    self._mark_dead(ErrorResponse(
                        type="error",
                        message=(
                            f"{consecutive_failures} consecutive ping "
                            f"failures: {type(e).__name__}: {e}"
                        ),
                    ))
                    return
            await asyncio.sleep(sleep_time)

    async def __aenter__(self) -> Self:
        # Create client if not provided externally
        if self._external_client is None:
            self._own_connector = aiohttp.TCPConnector(limit=1_000_000)
            self._own_client = aiohttp.ClientSession(
                base_url=self.base_url,
                connector=self._own_connector,
                headers=self._default_headers,
                trust_env=True,
            )
            set_retry_policy(self._own_client, self._retry_policy)

        def on_event(event: str, data: str) -> None:
            if event == "task_id":
                self._pending_task_id = data.strip()

        try:
            res = await resumable_sse(
                self.client,
                self._creation_endpoint,
                token=self.api_key,
                json=self._creation_payload,
                deployment=self.deployment,
                max_retries=3,
                timeout=self.creation_timeout,
                on_event=on_event,
                extra_headers=self._creation_headers,
            )
        except Exception as e:
            raise self._annotate_error(e) from e.__cause__

        # Extract SID from SSE response
        if res and isinstance(res, dict):
            self.sid = res.get("sid")
        if self.sid is None:
            self.sid = self._pending_task_id
        self._pending_task_id = None

        assert self.sid is not None, "No SID returned from creation endpoint"

        try:
            await self._post_create()
        except Exception as e:
            raise self._annotate_error(e) from e.__cause__

        # Start ping as an asyncio task
        self._ping_task = asyncio.create_task(self._run_ping(
            url=f"{self.base_url}/ping",
            sid=self.sid,
            api_key=self.api_key,
            sleep_time=10,
            deployment=self.deployment,
        ))

        return self

    async def __aexit__(self, *exc):
        # Stop ping
        if self._ping_task is not None:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass
            self._ping_task = None

        # Subclass hook (e.g. environment teardown)
        try:
            await self._pre_delete()
        except Exception:
            pass

        # Fast cleanup: pending task from interrupted creation
        if self._pending_task_id is not None:
            try:
                await request_retryable(
                    self.client, "POST", "/delete_session",
                    expect_json=False, token=self.api_key,
                    sid=self._pending_task_id,
                )
            except Exception:
                pass
            self._pending_task_id = None

        # Main cleanup: delete session
        if self.sid is not None:
            try:
                await request_retryable(
                    self.client, "POST", "/delete_session",
                    expect_json=False, token=self.api_key,
                    sid=self.sid,
                )
            except:
                pass

        # Close client if we own it
        if self._own_client is not None and not self._own_client.closed:
            await self._own_client.close()

    def __del__(self):
        own_client = getattr(self, "_own_client", None)
        if own_client is not None:
            _finalize_session(own_client)
