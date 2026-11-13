from __future__ import annotations

import asyncio
import inspect
import logging
import math
import threading
import time
from collections.abc import Awaitable, Callable
from concurrent.futures import Future as ThreadFuture
from concurrent.futures import TimeoutError as FutureTimeoutError
from contextlib import suppress
from dataclasses import dataclass
from numbers import Number
from typing import Any

from typing_extensions import TypeAliasType

from dreamscale import errors
from dreamscale.config import load_config
from dreamscale.control import ControlPlaneClient, Session
from dreamscale.policy.config import OptimizationConfig
from dreamscale.policy.types import (
    ProviderPreference,
    RegionPreference,
    SpeedPreference,
    TransportMode,
    TransportPreference,
)
from dreamscale.region_probe import (
    create_session_with_rtt_region_order,
    pins_region,
    validate_provider_selection,
    validate_speed_selection,
)
from dreamscale.sessions import Heartbeat, region_label, wait_until_ready
from dreamscale.terminal import describe_resolved_policy
from dreamscale.transport_selection import REPORT_TRANSPORT_TIMEOUT_S, connect_selected_transport

DEFAULT_CONNECT_IDLE_TIMEOUT_S = 3600
MAX_KEEP_WARM_S = 3600
# A release moving a deployment onto a new serving image refuses its connects
# (deployment_requalifying) until the deployment passes its check on the new image, usually
# within a minute or two: connect waits that out, this long at most, asking again every
# REQUALIFYING_POLL_S (or the server's Retry-After).
REQUALIFYING_WAIT_S = 300.0
REQUALIFYING_POLL_S = 30.0
# Connect waits this long for a Modal session's punched QUIC, then lets it finish in the
# background. The upgrade measured about 300 ms at p50, so most sessions still send their
# first observation over QUIC, and a punch that fails costs this instead of its timeouts.
MODAL_QUIC_STARTUP_WAIT_S = 1.5
# A switch to the WebSocket is said only once it has lasted this long. A session whose server
# stopped loses QUIC and then the WebSocket within a moment, and the policy then says the
# server stopped (not that QUIC was lost); a path the re-punch heals at once is no news.
QUIC_LOST_NOTICE_S = 3.0
# The control plane's names for a punched-QUIC fallback (the transport keeps the detail).
_MODAL_FALLBACK_REASONS = {
    "quic_punch_failed": "quic_punch_failed",
    "quic_path_timeout": "quic_path_timeout",
    "quic_send_failed": "quic_send_failed",
    "quic_closed": "quic_closed",
    "quic_lost": "quic_closed",
}

log = logging.getLogger(__name__)

TransportConnect = TypeAliasType(
    "TransportConnect",
    Callable[..., Awaitable[Any]],
)


def _validate_startup_timeout(startup_timeout: float | None) -> float | None:
    if startup_timeout is None:
        return None
    if isinstance(startup_timeout, bool) or not isinstance(startup_timeout, Number):
        raise ValueError("startup_timeout must be a finite positive number")
    try:
        timeout_s = float(startup_timeout)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("startup_timeout must be a finite positive number") from exc
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ValueError("startup_timeout must be a finite positive number")
    return timeout_s


def _validate_keep_warm(keep_warm: int) -> int:
    if isinstance(keep_warm, bool) or not isinstance(keep_warm, int):
        raise ValueError("keep_warm must be an integer from 0 to 3600 seconds")
    if keep_warm < 0 or keep_warm > MAX_KEEP_WARM_S:
        raise ValueError("keep_warm must be an integer from 0 to 3600 seconds")
    return keep_warm


class _LoopRunner:
    """Daemon asyncio loop for sync policy facades that hold async resources."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._closed = False
        self._state_lock = threading.Lock()
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="dreamscale-policy-loop",
        )
        self._thread.start()

    def _run(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def run(self, coro):
        return self._run_task(coro, cancel_on_interrupt=True)

    def run_cleanup(self, coro):
        return self._run_task(coro, cancel_on_interrupt=False)

    def _run_task(self, coro, *, cancel_on_interrupt: bool):
        task_ready: ThreadFuture = ThreadFuture()
        result_future: ThreadFuture = ThreadFuture()
        cancel_requested = threading.Event()
        started_lock = threading.Lock()
        started = False
        schedule_returned = False

        async def run_once() -> Any:
            nonlocal started
            with started_lock:
                if started:
                    return None
                started = True
            try:
                result = await coro
            except asyncio.CancelledError:
                if not result_future.done():
                    result_future.cancel()
                raise
            except BaseException as exc:
                _set_future_exception(result_future, exc)
                raise
            else:
                if not result_future.done():
                    result_future.set_result(result)
                return result

        def create_task() -> None:
            # Interrupt recovery may schedule this callback twice. Only the
            # original task may resolve the shared result after its cleanup.
            if task_ready.done():
                return
            try:
                task = self._loop.create_task(run_once())
                task.add_done_callback(lambda done_task: on_task_done(done_task))
                if not task_ready.done():
                    task_ready.set_result(task)
                if cancel_requested.is_set():
                    task.cancel()
            except BaseException as exc:
                _set_future_exception(task_ready, exc)
                _set_future_exception(result_future, exc)

        def on_task_done(task: asyncio.Task) -> None:
            if task.cancelled():
                with started_lock:
                    has_started = started
                if not has_started:
                    _close_unstarted_awaitable(coro)
                if not result_future.done():
                    result_future.cancel()
                return
            task.exception()

        try:
            with self._state_lock:
                self._raise_if_closed_locked(coro)
                try:
                    # A signal can land inside call_soon_threadsafe. Treat that
                    # as "maybe scheduled" and resolve via task_ready below.
                    self._loop.call_soon_threadsafe(create_task)
                    schedule_returned = True
                except RuntimeError as exc:
                    _close_unstarted_awaitable(coro)
                    raise RuntimeError("dreamscale policy loop is closed") from exc
            task = _future_result(task_ready, timeout=5)
            return _future_result(result_future)
        except FutureTimeoutError as exc:
            # FutureTimeoutError is the builtin TimeoutError, so this also matches
            # a timeout raised by the coroutine itself (a step deadline). Only the
            # scheduling wait above means the loop is gone.
            if result_future.done() and not result_future.cancelled():
                if result_future.exception() is exc:
                    raise
            _close_unstarted_awaitable(coro)
            raise RuntimeError("dreamscale policy loop is closed") from exc
        except BaseException as original:
            if result_future.done():
                raise
            if cancel_on_interrupt:
                cancel_requested.set()
                try:
                    if not schedule_returned:
                        raise FutureTimeoutError()
                    task = _future_result(task_ready, timeout=5)
                except FutureTimeoutError:
                    if not _ensure_task_scheduled(self._loop, create_task):
                        _close_unstarted_awaitable(coro)
                        raise original from None
                    try:
                        task = _future_result(task_ready, timeout=5)
                    except FutureTimeoutError:
                        _close_unstarted_awaitable(coro)
                        raise original from None
                with suppress(RuntimeError):
                    self._loop.call_soon_threadsafe(task.cancel)
                _wait_for_interrupted_cleanup(result_future)
            else:
                try:
                    if not schedule_returned:
                        raise FutureTimeoutError()
                    _future_result(task_ready, timeout=5)
                except FutureTimeoutError:
                    if not _ensure_task_scheduled(self._loop, create_task):
                        _close_unstarted_awaitable(coro)
                        raise original from None
                    try:
                        _future_result(task_ready, timeout=5)
                    except FutureTimeoutError:
                        _close_unstarted_awaitable(coro)
                        raise original from None
                _wait_for_interrupted_cleanup(result_future)
            raise original

    def submit(self, coro):
        with self._state_lock:
            self._raise_if_closed_locked(coro)
            try:
                return asyncio.run_coroutine_threadsafe(coro, self._loop)
            except RuntimeError as exc:
                _close_unstarted_awaitable(coro)
                raise RuntimeError("dreamscale policy loop is closed") from exc

    def shutdown(self) -> None:
        with self._state_lock:
            if self._closed:
                return
            self._closed = True
            loop_is_closed = self._loop.is_closed()
            thread_is_alive = self._thread.is_alive()
        if loop_is_closed:
            return
        if thread_is_alive:
            try:
                future = asyncio.run_coroutine_threadsafe(_cancel_pending_tasks(), self._loop)
                future.result(timeout=5)
            except FutureTimeoutError:
                log.debug("timed out draining policy loop tasks before shutdown")
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join(timeout=5)
        self._loop.close()

    def _raise_if_closed_locked(self, coro=None) -> None:
        if self._closed or self._loop.is_closed() or not self._thread.is_alive():
            _close_unstarted_awaitable(coro)
            raise RuntimeError("dreamscale policy loop is closed")


@dataclass
class PolicyConnection:
    client: Any
    session: Session
    transport: Any
    heartbeat: Heartbeat
    transport_mode: TransportMode
    keep_warm: int = 0
    on_progress: Callable[[str], None] | None = None
    allow_runtime_fallback: bool = False
    diagnostic_timing_monotonic: dict[str, float] | None = None
    closed: bool = False
    release_status: str | None = None
    # A Modal session's punched-QUIC upgrade still running after connect, and the reports
    # that follow its path.
    quic_upgrade: asyncio.Task[Any] | None = None
    transport_reports: ModalTransportReports | None = None

    async def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        first_error: Exception | None = None

        async def attempt(cleanup: Awaitable[Any]) -> None:
            nonlocal first_error
            try:
                await cleanup
            except Exception as exc:  # noqa: BLE001 - preserve first cleanup failure.
                if first_error is None:
                    first_error = exc

        if self.quic_upgrade is not None:
            self.quic_upgrade.cancel()
            await asyncio.gather(self.quic_upgrade, return_exceptions=True)
        await attempt(self.heartbeat.stop())
        await attempt(self.transport.close())
        if self.transport_reports is not None:
            await self.transport_reports.aclose()

        async def release() -> None:
            if self.keep_warm:
                response = await self.client.detach_session(self.session.session_id)
                if isinstance(response, dict):
                    self.release_status = response.get("status")
            else:
                await _stop_policy_session(self.client, self.session.session_id)
                self.release_status = "closed"

        await attempt(release())
        await attempt(self.client.close())

        if first_error is not None:
            raise first_error


async def default_transport_connect(
    addr: str,
    port: int,
    *,
    cert_fingerprint: str,
    session_id: str,
    session_token: str,
    upload: str = "standard",
    profile: Any = None,
) -> Any:
    from dreamscale_transport import QuicClient

    return await QuicClient.connect(
        addr,
        port,
        cert_fingerprint=cert_fingerprint,
        session_id=session_id,
        session_token=session_token,
        upload=upload,
        profile=profile,
    )


def session_transport_profile(session: Session) -> Any:
    """The transport v2 profile the control plane named for this session, or None."""
    raw = getattr(session, "transport_profile", None)
    if not raw:
        return None
    from dreamscale_transport.profiles import resolve

    return resolve(raw.get("name"), raw.get("levers_off") or ())


async def pin_connect(transport_connect: TransportConnect, session: Session) -> Any:
    # Only a Steady Upload session passes `upload`, so injected connectors
    # without that keyword keep working for standard sessions.
    upload: dict[str, Any] = {"upload": "steady"} if session.upload == "steady" else {}
    profile = session_transport_profile(session)
    if profile is not None:  # likewise only when the control plane names one
        upload["profile"] = profile
    try:
        return await transport_connect(
            session.worker_addr,
            session.port,
            cert_fingerprint=session.cert_fingerprint,
            session_id=session.session_id,
            session_token=session.session_token,
            **upload,
        )
    except errors.DreamscaleError:
        raise
    except Exception as exc:
        text = str(exc).lower()
        if "fingerprint" in text or "pin" in text:
            raise errors.catalog("cert_fingerprint_mismatch") from exc
        raise


def compatible_diagnose_udp(preflight_fn: Callable[..., Any]) -> Callable[..., Any]:
    async def diagnose(addr: str, port: int, **kwargs: Any) -> Any:
        call_kwargs = _accepted_preflight_kwargs(preflight_fn, kwargs)
        result = preflight_fn(addr, port, **call_kwargs)
        if inspect.isawaitable(result):
            result = await result
        return _as_udp_reachability_report(result)

    return diagnose


def _accepted_preflight_kwargs(
    preflight_fn: Callable[..., Any],
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    try:
        params = inspect.signature(preflight_fn).parameters
    except (TypeError, ValueError):
        return kwargs
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values()):
        return kwargs
    return {key: value for key, value in kwargs.items() if key in params}


def _as_udp_reachability_report(result: Any) -> Any:
    if hasattr(result, "ok") and hasattr(result, "worker"):
        return result
    if not hasattr(result, "status"):
        return result

    from dreamscale_transport import PreflightResult, UdpReachabilityReport

    status = result.status
    remediation = getattr(result, "remediation", "")
    reason = "ok"
    if status == "udp_blocked":
        reason = "udp_refused"
    elif status != "ok":
        reason = "data_plane_unreachable"
    return UdpReachabilityReport(
        worker=PreflightResult(status=status, remediation=remediation),
        diagnostic=None,
        reason=reason,
        remediation="" if status == "ok" else remediation,
    )


class _RequalifyingWait:
    """Waits out ``deployment_requalifying`` refusals for REQUALIFYING_WAIT_S at most from the
    start of the connect (or the caller's startup timeout, if shorter), saying so once, then
    about once a minute. It gives up before a wait would pass that bound, so what the caller
    sees is the server's own problem and fix, not a timeout."""

    def __init__(self, progress, sleep, clock, limit_s: float | None) -> None:
        self.progress, self.sleep, self.clock = progress, sleep, clock
        self.started: float | None = None  # the first create (open_policy_connection)
        self.limit_s = min(REQUALIFYING_WAIT_S, limit_s or REQUALIFYING_WAIT_S)
        self.said_at: float | None = None

    def attempt(self, at: float) -> None:
        if self.started is None:
            self.started = at

    async def wait(self, error: errors.DreamscaleError) -> None:
        now = self.clock()
        started = now if self.started is None else self.started
        retry_after = getattr(error, "retry_after_s", None)
        if (
            not isinstance(retry_after, int | float)
            or not math.isfinite(retry_after)
            or retry_after <= 0
        ):
            retry_after = REQUALIFYING_POLL_S
        pause = min(max(float(retry_after), 1.0), REQUALIFYING_POLL_S * 2)
        if started + self.limit_s - now <= pause:
            raise error
        if self.said_at is None:
            self.said_at = now
            limit = (
                f"{self.limit_s / 60:.0f} min" if self.limit_s >= 120 else f"{self.limit_s:.0f} s"
            )
            self.progress(f"{str(error).rstrip('.')}. Waiting for it (up to {limit})…")
        elif now - self.said_at >= 60:
            self.said_at = now
            self.progress(
                f"Still moving to the new serving image ({(now - started) / 60:.0f} min "
                "so far)…"
            )
        await self.sleep(pause)


async def open_policy_connection(
    *,
    model: str,
    region: RegionPreference = "auto",
    region_fallback: bool | None = None,
    engine: str | None = None,
    provider: ProviderPreference | None = None,
    speed: SpeedPreference | None = None,
    idle_timeout: int = DEFAULT_CONNECT_IDLE_TIMEOUT_S,
    keep_warm: int = 0,
    startup_timeout: float | None = None,
    transport: TransportPreference = "auto",
    optimization_config: OptimizationConfig | None = None,
    checkpoint: str | None = None,
    api_key: str | None = None,
    on_progress: Callable[[str], None] | None = print,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    transport_connect: TransportConnect = default_transport_connect,
    preflight_fn: Callable[..., Any] | None = None,
    relay_connect: Callable[..., Awaitable[Any]] | None = None,
    sleep: Callable[..., Any] = asyncio.sleep,
    clock: Callable[[], float] = time.monotonic,
    on_session_status: Callable[[Session], None] | None = None,
) -> PolicyConnection:
    validate_provider_selection(model, provider, region)
    region = validate_speed_selection(model, speed, provider, region)
    if (provider == "modal" or speed == "fast") and transport != "auto":
        raise ValueError("Modal requires transport='auto'")
    startup_timeout = _validate_startup_timeout(startup_timeout)
    keep_warm = _validate_keep_warm(keep_warm)
    if transport not in ("auto", "quic", "relay"):
        raise ValueError('transport must be "auto", "quic", or "relay"')

    config = load_config()
    if api_key is not None:
        config.api_key = api_key.strip() or None
    if not config.api_key:
        raise errors.catalog("not_configured")

    progress = on_progress or _ignore_progress
    client = None
    session: Session | None = None
    selected_transport = None
    heartbeat: Heartbeat | None = None
    quic_upgrade: asyncio.Task[Any] | None = None
    transport_reports: ModalTransportReports | None = None
    diagnostic_timing: dict[str, float] = {}
    try:
        client = client_factory(config.control_plane_url, config.api_key)
        moving = _RequalifyingWait(progress, sleep, clock, startup_timeout)

        async def create() -> Session:
            nonlocal session
            session = await create_session_with_rtt_region_order(
                client,
                model,
                region=region,
                **({"region_fallback": region_fallback} if region_fallback is not None else {}),
                **({"engine": engine} if engine is not None else {}),
                **({"provider": provider} if provider is not None else {}),
                **({"speed": speed} if speed == "fast" else {}),
                idle_timeout=idle_timeout,
                keep_warm=keep_warm,
                optimization_config=optimization_config or OptimizationConfig(),
                **({"checkpoint": checkpoint} if checkpoint is not None else {}),
            )
            return session

        while True:
            try:
                diagnostic_timing["session_create_started_at"] = clock()
                moving.attempt(diagnostic_timing["session_create_started_at"])
                created = await create()
                diagnostic_timing["session_id_received_at"] = clock()
                session = created
                session = await wait_until_ready(
                    client,
                    session,
                    on_progress=progress,
                    sleep=sleep,
                    timeout_s=startup_timeout,
                    on_status=on_session_status,
                    restart_session=create,
                )
                break
            except errors.DreamscaleError as error:
                if error.code != "deployment_requalifying":
                    raise
                session = None  # refused, or failed while queued: nothing to close
                await moving.wait(error)
        if provider is not None and (
            session.requested_provider != provider or session.provider != provider
            or (region_fallback is not True and not pins_region(region, session.region))
        ):
            raise RuntimeError("ready session violates the requested provider or region")
        if speed == "fast" and session.speed != "fast":
            raise RuntimeError('ready session does not run at speed="fast"')
        diagnostic_timing["session_ready_at"] = clock()
        progress(_worker_allocated_line(session))

        if session.data_plane is not None:
            if transport != "auto":
                raise ValueError(
                    "session-scoped WebSocket compute requires transport='auto'"
                )
            connect_data_plane = getattr(client, "connect_data_plane", None)
            if not callable(connect_data_plane):
                raise RuntimeError("control-plane client cannot connect the assigned data plane")
            selected_transport = await connect_data_plane(session)
            selected_transport.mode = "wss_tunnel"
            transport_reports = ModalTransportReports(
                getattr(client, "report_transport", None), session.session_id, progress
            )
            quic_upgrade = await _start_modal_quic(session, selected_transport, transport_reports)

        async def quic_connect(ready_session: Session) -> Any:
            return await pin_connect(transport_connect, ready_session)

        async def relay_connect_for_session(ready_session: Session) -> Any:
            connect = relay_connect or getattr(client, "connect_relay", None)
            if connect is None:
                raise errors.catalog("relay_unavailable")
            return await connect(ready_session)

        if selected_transport is not None:
            pass
        elif transport == "relay":
            selected_transport = await relay_connect_for_session(session)
            selected_transport.mode = getattr(selected_transport, "mode", "relay")
            selected_transport.fallback_reason = None
            selected_transport.primary_preflight_status = None
            selected_transport.diagnostic_preflight_status = None
            await _report_transport_best_effort(
                getattr(client, "report_transport", None),
                session.session_id,
                transport_protocol="relay",
                fallback_used=False,
                fallback_reason=None,
                primary_preflight_status=None,
                diagnostic_preflight_status=None,
            )
        else:
            diagnose_udp_fn = _select_preflight(preflight_fn)
            selected_transport = await connect_selected_transport(
                session,
                diagnose_udp_fn=diagnose_udp_fn,
                quic_connect=quic_connect,
                relay_connect=relay_connect_for_session,
                allow_fallback=transport == "auto",
                on_line=progress,
                notice_style="sdk",
                report_transport_fn=getattr(client, "report_transport", None),
            )

        diagnostic_timing["transport_connected_at"] = clock()
        heartbeat = Heartbeat(client, session.session_id, sleep=sleep)
        heartbeat.start()
        progress(_transport_connected_line(selected_transport))
        # A robot with a camera codec device names its camera stream (and why, on JPEG), and
        # its terminal hears every later change, each JPEG request and the run's tally.
        camera_stream = getattr(selected_transport, "camera_stream_notice", None)
        if isinstance(camera_stream, str):
            progress(camera_stream)
            codec = getattr(selected_transport, "codec_settings", None)
            if codec is not None:
                codec.on_status = progress
        progress(
            f"Runtime selected: {describe_resolved_policy(session.resolved_optimization_config)}"
        )
        if session.resolved_optimization_config.calibration == "off":
            progress("Policy is ready for inference.")
        return PolicyConnection(
            client=client,
            session=session,
            transport=selected_transport,
            heartbeat=heartbeat,
            transport_mode=getattr(selected_transport, "mode", transport),
            keep_warm=keep_warm,
            on_progress=progress,
            diagnostic_timing_monotonic=diagnostic_timing,
            allow_runtime_fallback=(
                transport == "auto"
                and getattr(selected_transport, "mode", None) == "quic"
            ),
            quic_upgrade=quic_upgrade,
            transport_reports=transport_reports,
        )
    except BaseException:
        if quic_upgrade is not None:
            quic_upgrade.cancel()
            await asyncio.gather(quic_upgrade, return_exceptions=True)
        if transport_reports is not None:
            await transport_reports.cancel()
        await _cleanup_connect_failure(
            client=client,
            session=session,
            transport=selected_transport,
            heartbeat=heartbeat,
        )
        raise


def _select_preflight(preflight_fn: Callable[..., Any] | None) -> Callable[..., Any]:
    if preflight_fn is None:
        from dreamscale_transport import diagnose_udp as preflight_fn
    return compatible_diagnose_udp(preflight_fn)


def _ignore_progress(_line: str) -> None:
    return None


def _worker_allocated_line(session: Session) -> str:
    region = session.routed_region or session.region
    if region:
        return f"Compute is ready in {region_label(region)}."
    return "Compute is ready."


def _transport_connected_line(transport: Any) -> str:
    mode = getattr(transport, "mode", None)
    if mode == "relay":
        return "Connected through HTTPS fallback."
    if mode == "wss_tunnel":
        return "Connected to session-scoped compute."
    return "Connected to compute."


def modal_fallback_reason(detail: str | None) -> str | None:
    """The control plane's name for why a Modal session is on the WebSocket."""
    if detail is None:
        return None
    return _MODAL_FALLBACK_REASONS.get(detail.split(":", 1)[0], "quic_closed")


class ModalTransportReports:
    """Tells the control plane which path a Modal session is on, in order, at each switch."""

    def __init__(
        self,
        report_fn: Callable[..., Awaitable[None]] | None,
        session_id: str,
        on_progress: Callable[[str], None],
    ) -> None:
        self._report_fn = report_fn
        self._session_id = session_id
        self._on_progress = on_progress
        self._lock = asyncio.Lock()
        self._tasks: set[asyncio.Task[None]] = set()
        self._fell_back = False
        self._notice: asyncio.TimerHandle | None = None
        self._muted = False
        self.started = False

    def report(self, mode: str, detail: str | None) -> asyncio.Task[None]:
        task = asyncio.create_task(self._send(mode, detail))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def _send(self, mode: str, detail: str | None) -> None:
        reason = None if mode == "quic_punch" else modal_fallback_reason(detail)
        async with self._lock:  # FIFO: the last report the control plane gets is the latest
            await _report_transport_best_effort(
                self._report_fn,
                self._session_id,
                transport_protocol="quic" if mode == "quic_punch" else "wss_tunnel",
                fallback_used=reason is not None,
                fallback_reason=reason,
                primary_preflight_status=None,
                diagnostic_preflight_status=None,
            )

    def changed(self, mode: str, detail: str | None) -> None:
        """The transport's ``on_transport_change``: a switch after connect. Every switch is
        reported; the robot's terminal hears of a fallback only once it lasts
        (``QUIC_LOST_NOTICE_S``), and of the return only if it heard of the fallback."""
        if mode == "wss_tunnel":
            if self._notice is None and not self._muted:
                self._notice = asyncio.get_running_loop().call_later(
                    QUIC_LOST_NOTICE_S, self._say_lost
                )
        elif self._notice is not None:  # healed before it was news
            self._notice.cancel()
            self._notice = None
        elif self._fell_back and not self._muted:
            self._fell_back = False
            self._on_progress("Reconnected over QUIC.")
        self.report(mode, detail)

    def _say_lost(self) -> None:
        self._notice = None
        if not self._muted:
            self._fell_back = True
            self._on_progress("QUIC path lost; continuing over WebSocket until it reconnects.")

    def mute(self) -> None:
        """The session is going away (its link is lost, or it closes): no more path lines,
        including a fallback not yet said. Reports still go out."""
        self._muted = True
        if self._notice is not None:
            self._notice.cancel()
            self._notice = None

    async def aclose(self) -> None:
        """Let the reports already queued finish (each is bounded by its timeout)."""
        self.mute()
        if self._tasks:
            await asyncio.gather(*tuple(self._tasks), return_exceptions=True)

    async def cancel(self) -> None:
        """Drop the reports still queued: the session is going away unused."""
        self.mute()
        tasks = tuple(self._tasks)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def _start_modal_quic(
    session: Session, transport: Any, reports: ModalTransportReports
) -> asyncio.Task[Any] | None:
    """Start the punched-QUIC upgrade a Modal session's control plane and worker offer:
    wait up to ``MODAL_QUIC_STARTUP_WAIT_S``, then let it finish in the background.
    Reports the path now and at every later switch. Returns the upgrade if still running."""
    upgrade: asyncio.Task[Any] | None = None
    try:
        if session.modal_quic and callable(getattr(transport, "upgrade_quic", None)):
            upgrade = asyncio.create_task(_upgrade_modal_quic(session, transport, reports))
            await asyncio.wait((upgrade,), timeout=MODAL_QUIC_STARTUP_WAIT_S)
        # No await between reading the path and hooking its changes: none is missed.
        first = reports.report(
            getattr(transport, "mode", "wss_tunnel"), getattr(transport, "fallback_reason", None)
        )
        transport.on_transport_change = reports.changed
        reports.started = True
        await first
    except BaseException:
        if upgrade is not None:
            upgrade.cancel()
            await asyncio.gather(upgrade, return_exceptions=True)
        raise
    return None if upgrade is None or upgrade.done() else upgrade


async def _upgrade_modal_quic(
    session: Session, transport: Any, reports: ModalTransportReports | None = None
) -> str | None:
    """Move a Modal session onto punched QUIC, in the upload mode the control plane
    names, when the worker offers it. Returns the fallback reason, if any; the
    WebSocket tunnel keeps serving the session either way (and the transport keeps
    trying the punch in the background)."""
    from dreamscale_transport.punch import PunchNotOffered

    upgrade = getattr(transport, "upgrade_quic", None)
    if not session.modal_quic or not callable(upgrade):
        return None
    try:
        profile = session_transport_profile(session)
        if profile is None:
            await upgrade(upload=session.modal_quic)
        else:
            await upgrade(upload=session.modal_quic, profile=profile)
    except PunchNotOffered:
        return None  # this session does not use punched QUIC: not a fallback
    except Exception as exc:  # noqa: BLE001 - never fail a session over QUIC
        reason = f"quic_punch_failed:{type(exc).__name__}"
        transport.fallback_reason = reason
        if reports is not None and reports.started:
            reports.report("wss_tunnel", reason)
        return reason
    return None


async def _report_transport_best_effort(
    report_transport_fn: Callable[..., Awaitable[None]] | None,
    session_id: str,
    **metadata: Any,
) -> None:
    if report_transport_fn is None:
        return
    try:
        await asyncio.wait_for(
            report_transport_fn(session_id, **metadata),
            timeout=REPORT_TRANSPORT_TIMEOUT_S,
        )
    except Exception:
        log.debug("failed to report selected transport", exc_info=True)


async def _cleanup_connect_failure(
    *,
    client: Any,
    session: Session | None,
    transport: Any,
    heartbeat: Heartbeat | None,
) -> None:
    if heartbeat is not None:
        with suppress(Exception):
            await heartbeat.stop()
    if transport is not None:
        with suppress(Exception):
            await transport.close()
    if client is not None and session is not None:
        with suppress(Exception):
            await _stop_policy_session(client, session.session_id)
    if client is not None:
        with suppress(Exception):
            await client.close()


async def _stop_policy_session(control: Any, session_id: str) -> None:
    await control.delete_session(session_id)


def _wait_for_interrupted_cleanup(future) -> None:
    while True:
        try:
            future.result()
            return
        except BaseException:
            if future.done():
                return


def _future_result(future, timeout=None):
    if timeout is None:
        return future.result()
    return future.result(timeout=timeout)


def _set_future_exception(future: ThreadFuture, exc: BaseException) -> None:
    if not future.done():
        future.set_exception(exc)


def _ensure_task_scheduled(loop: asyncio.AbstractEventLoop, callback: Callable[[], None]) -> bool:
    try:
        loop.call_soon_threadsafe(callback)
    except BaseException:
        return False
    return True


async def _cancel_pending_tasks() -> None:
    current = asyncio.current_task()
    pending = [
        task
        for task in asyncio.all_tasks()
        if task is not current and not task.done()
    ]
    if not pending:
        return
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


def _close_unstarted_awaitable(awaitable) -> None:
    close = getattr(awaitable, "close", None)
    if callable(close):
        close()
