from __future__ import annotations

import asyncio
import json
import time
import uuid
from typing import Any


from ..clients.capsule import (
    ClaimTaskRequest,
    CompleteTaskRequest,
    NotifySessionRequest,
    TaskDelivery,
    TaskHeartbeatRequest,
    TaskStatus,
)
from ..constants import (
    DEFAULT_CHANNEL_TYPE,
)
from ..msg import Message
from ..session import ReplyStream, Session, SessionChannel, UserInfo
from ..task_exec import _retry_on_errors, run_task_subprocess
from .shared import (
    _GRPC_RETRY_DELAY,
    _GRPC_RETRY_TRIES,
    _current_task_id,
    _log,
    _maybe_await,
)


class RunnerTaskMixin:
    async def _get_task_session(self, session_id: str) -> Session:
        """Build a fully wired Session for use inside a task.

        Always refreshes history/data from the session service so the task
        sees the latest conversation state.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(
                id=session_id,
                user=UserInfo(id="", email=None),
                channel=SessionChannel(type=DEFAULT_CHANNEL_TYPE),
                history=[],
                data={},
            )
        session = self._sessions[session_id]

        await self._hydrate_session(session)

        async def _notify_task_session(
            request_id: str,
            *,
            text: str = "",
            block_json: str = "",
            external_delivery: bool = True,
        ) -> None:
            if self._session_stub and hasattr(self._session_stub, "notify_session"):
                await self._run_rpc(
                    self._session_stub.notify_session,
                    NotifySessionRequest(
                        app_id=self._app_id,
                        session_id=session_id,
                        request_id=request_id,
                        text=text,
                        block_json=block_json,
                        external_delivery=external_delivery,
                    ),
                )
                return
            self._submit(
                request_id,
                text,
                done=True,
                session_id=session_id,
                block_json=block_json,
            )

        async def _task_reply(msg: Message) -> None:
            await _notify_task_session(str(uuid.uuid4()), text=msg.text)

        async def _task_block(block_json: str) -> None:
            await _notify_task_session(
                str(uuid.uuid4()),
                block_json=block_json,
                external_delivery=False,
            )

        async def _task_stream(chunks) -> None:
            full = ""
            async for chunk in chunks:
                full += chunk or ""
            if full:
                await _task_reply(
                    Message(text=full, sender="app", channel_type=session.channel.type)
                )

        def _task_stream_reply() -> Any:
            request_id = str(uuid.uuid4())

            def _write(text: str) -> None:
                return None

            def _done() -> None:
                if reply.text:
                    asyncio.ensure_future(
                        _notify_task_session(
                            request_id,
                            text=reply.text,
                        )
                    )

            reply = ReplyStream(_write, session.history, session.channel.type, done_cb=_done)
            return reply

        session._reply_callback = _task_reply
        session._stream_callback = _task_stream
        session._stream_reply_factory = _task_stream_reply
        session._stream_write_callback = None
        session._block_callback = _task_block
        self._bind_session_db(session)
        session._runner = self
        session._runner_stub = self._runner_stub
        session._session_stub = self._session_stub
        session._app_id = self._app_id
        return session

    async def _handle_task(self, delivery: TaskDelivery) -> None:
        await self._track_start()
        task_id = delivery.task_id
        task_name = delivery.task_name
        started = time.time()
        token = _current_task_id.set(task_id)
        session = None

        _log(f"task received: name={task_name} task_id={task_id} session_id={delivery.session_id}")

        try:
            delivery_version_id = getattr(delivery, "version_id", "")
            if not delivery_version_id and self._version_type == "serve":
                _log(
                    "stale task skipped: "
                    f"name={task_name} task_id={task_id} "
                    f"missing task_version_id runner_version_id={self._version_id}"
                )
                return
            if delivery_version_id and self._version_id and delivery_version_id != self._version_id:
                _log(
                    "stale task skipped: "
                    f"name={task_name} task_id={task_id} "
                    f"task_version_id={delivery_version_id} runner_version_id={self._version_id}"
                )
                return

            claim_started = time.time()
            if not await self._claim_task(task_id):
                return
            claim_elapsed = time.time() - claim_started
            if claim_elapsed > 1:
                _log(f"task claim slow: task_id={task_id} elapsed={claim_elapsed:.2f}s")

            desc = self._tasks.get(task_name)
            if desc is None:
                _log(f"unknown task: {task_name}")
                await self._complete_task(task_id, TaskStatus.FAILED, f"unknown task: {task_name}")
                return

            kwargs = json.loads(delivery.kwargs_json) if delivery.kwargs_json else {}
            timeout = delivery.timeout or desc._timeout or 0
            current_task = asyncio.current_task()
            hb = asyncio.ensure_future(self._task_heartbeat_loop(task_id, current_task))

            try:
                if desc._process:
                    kwargs_json = (
                        delivery.kwargs_json.decode()
                        if isinstance(delivery.kwargs_json, bytes)
                        else (delivery.kwargs_json or "{}")
                    )
                    _log(f"task {task_name} spawning subprocess (process=True)")
                    status, detail = await self._run_task_subprocess(
                        task_name,
                        delivery.session_id or "",
                        kwargs_json,
                        timeout,
                    )
                    elapsed = time.time() - started

                    if status == "ok":
                        await self._complete_task(task_id, TaskStatus.COMPLETED, duration=elapsed)
                        if desc._callback_url:
                            self._fire_callback(desc._callback_url, task_id, "completed", elapsed)
                    elif status == "timeout":
                        _log(f"task {task_name} subprocess timed out after {timeout}s")
                        await self._complete_task(task_id, TaskStatus.TIMEOUT, detail, elapsed)
                        if desc._callback_url:
                            self._fire_callback(
                                desc._callback_url, task_id, "timeout", elapsed, detail
                            )
                    elif status == "killed":
                        _log(f"task {task_name} subprocess killed: {detail}")
                        await self._complete_task(task_id, TaskStatus.RETRY, detail, elapsed)
                        if desc._callback_url:
                            self._fire_callback(
                                desc._callback_url, task_id, "failed", elapsed, detail
                            )
                    else:
                        _log(f"task {task_name} subprocess failed: {detail}")
                        if _retry_on_errors(desc._retry_for, RuntimeError(detail)):
                            await self._complete_task(task_id, TaskStatus.RETRY, detail, elapsed)
                        elif desc._retry_for:
                            await self._complete_task(task_id, TaskStatus.FAILED, detail, elapsed)
                        else:
                            await self._complete_task(task_id, TaskStatus.RETRY, detail, elapsed)
                        if desc._callback_url:
                            self._fire_callback(
                                desc._callback_url, task_id, "failed", elapsed, detail
                            )
                else:
                    session = None
                    runtime_session = None
                    if delivery.session_id:
                        hydrate_started = time.time()
                        session = await self._get_task_session(delivery.session_id)
                        runtime_session = session
                        hydrate_elapsed = time.time() - hydrate_started
                        if hydrate_elapsed > 1:
                            _log(
                                "task session hydrate slow: "
                                f"task_id={task_id} session_id={delivery.session_id} "
                                f"elapsed={hydrate_elapsed:.2f}s"
                            )
                    else:
                        runtime_session = await self._build_runtime_session()
                        if desc._wants_session:
                            session = runtime_session

                    identity_token = (
                        self._set_session_on_refs(runtime_session) if runtime_session else None
                    )
                    try:
                        _log(
                            f"task handler starting: name={task_name} task_id={task_id} "
                            f"elapsed_since_delivery={time.time() - started:.2f}s"
                        )
                        call_kwargs = dict(kwargs)
                        if session is not None and desc._session_param_name:
                            call_kwargs.setdefault(desc._session_param_name, session)
                        coro = desc(**call_kwargs)
                        if timeout > 0:
                            await asyncio.wait_for(coro, timeout=timeout)
                        else:
                            await coro
                    finally:
                        if identity_token is not None:
                            self._clear_session_on_refs(identity_token)

                    elapsed = time.time() - started
                    await self._complete_task(task_id, TaskStatus.COMPLETED, duration=elapsed)
                    if desc._callback_url:
                        self._fire_callback(desc._callback_url, task_id, "completed", elapsed)

            except asyncio.TimeoutError:
                elapsed = time.time() - started
                _log(f"task {task_name} timed out after {timeout}s")
                await self._complete_task(task_id, TaskStatus.TIMEOUT, "timeout", elapsed)
                if desc._callback_url:
                    self._fire_callback(desc._callback_url, task_id, "timeout", elapsed, "timeout")

            except asyncio.CancelledError:
                elapsed = time.time() - started
                _log(f"task {task_name} cancelled")
                await self._complete_task(task_id, TaskStatus.CANCELLED, "cancelled", elapsed)
                if desc._callback_url:
                    self._fire_callback(
                        desc._callback_url, task_id, "cancelled", elapsed, "cancelled"
                    )

            except BaseException as exc:
                elapsed = time.time() - started
                error_msg = f"{type(exc).__name__}: {exc}"
                _log(f"task {task_name} failed: {error_msg}")

                if _retry_on_errors(desc._retry_for, exc):
                    await self._complete_task(task_id, TaskStatus.RETRY, error_msg, elapsed)
                elif desc._retry_for:
                    await self._complete_task(task_id, TaskStatus.FAILED, error_msg, elapsed)
                else:
                    await self._complete_task(task_id, TaskStatus.RETRY, error_msg, elapsed)

                if desc._callback_url:
                    self._fire_callback(desc._callback_url, task_id, "failed", elapsed, error_msg)
            finally:
                hb.cancel()

        except Exception as exc:
            _log(f"task dispatch error task_id={task_id}: {exc}")
            await self._complete_task(task_id, TaskStatus.FAILED, f"dispatch error: {exc}")
        finally:
            _current_task_id.reset(token)
            drain = getattr(self, "_drain_submit_results", None)
            if drain:
                await drain()
            await self._track_end()
            if session is not None and session.id:
                asyncio.ensure_future(self._persist(session))

    async def _build_runtime_session(self) -> Session:
        """Build a synthetic session from the runtime's owner context.

        Used for handlers that don't receive a persisted chat/API session
        (e.g. schedules and owner-scoped background tasks).
        """
        owner_id = self._user_id
        session = Session(
            id="",
            user=UserInfo(
                id=owner_id,
                email=None,
                org_id=UserInfo.org_id_from_owner_id(owner_id),
            ),
            channel=SessionChannel(type=DEFAULT_CHANNEL_TYPE),
            history=[],
            data={},
            integrations=await self._fetch_integrations(owner_id=owner_id),
        )
        self._bind_session_db(session)
        session._runner = self
        session._runner_stub = self._runner_stub
        session._session_stub = self._session_stub
        session._app_id = self._app_id
        return session

    async def _handle_schedule(self, delivery) -> None:
        name = delivery.schedule_name
        handler = self._schedules.get(name)
        if handler is None:
            _log(f"unknown schedule: {name}")
            return

        lock = self._schedule_locks.get(name)
        if lock and lock.locked():
            _log(f"schedule {name} still running from previous tick, skipping")
            return

        runtime_session = await self._build_runtime_session()
        token = self._set_session_on_refs(runtime_session)
        await self._track_start()
        try:
            async with lock:
                _log(f"running schedule: {name}")
                await _maybe_await(handler())
        except Exception as exc:
            _log(f"schedule error {name}: {exc}")
        finally:
            self._clear_session_on_refs(token)
            await self._track_end()

    def _fire_callback(
        self, url: str, task_id: str, status: str, duration: float, error: str = ""
    ) -> None:
        try:
            import urllib.request

            payload = json.dumps(
                {"task_id": task_id, "status": status, "duration": duration, "error": error}
            ).encode()
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception as exc:
            _log(f"callback {url} failed: {exc}")

    async def _claim_task(self, task_id: str) -> bool:
        if not self._task_stub:
            _log(f"claim_task skipped: task_stub not connected (task_id={task_id})")
            return False
        try:
            resp = await self._run_rpc(
                self._task_stub.claim_task,
                ClaimTaskRequest(
                    task_id=task_id, runner_id=self._app_id, version_id=self._version_id
                ),
            )
            if not getattr(resp, "ok", False):
                _log(f"claim_task rejected: task_id={task_id}")
                return False
            return True
        except Exception as exc:
            _log(f"claim_task failed: task_id={task_id} err={exc}")
            return False

    async def _complete_task(
        self, task_id: str, status: TaskStatus, error: str = "", duration: float = 0
    ) -> None:
        if not self._task_stub:
            _log(f"complete_task skipped: task_stub not connected (task_id={task_id})")
            return
        for attempt in range(_GRPC_RETRY_TRIES):
            try:
                await self._run_rpc(
                    self._task_stub.complete_task,
                    CompleteTaskRequest(
                        task_id=task_id,
                        status=status,
                        error=error,
                        duration_seconds=duration,
                        version_id=self._version_id,
                    ),
                )
                return
            except Exception as exc:
                if attempt < _GRPC_RETRY_TRIES - 1:
                    await asyncio.sleep(_GRPC_RETRY_DELAY * (2**attempt))
                else:
                    _log(
                        f"complete_task failed after {_GRPC_RETRY_TRIES} attempts: "
                        f"task_id={task_id} status={status} err={exc}"
                    )

    async def _task_heartbeat_loop(
        self, task_id: str, owner_task: asyncio.Task | None = None
    ) -> None:
        while True:
            await asyncio.sleep(10)
            try:
                resp = await self._run_rpc(
                    self._task_stub.task_heartbeat,
                    TaskHeartbeatRequest(task_id=task_id, version_id=self._version_id),
                )
                if getattr(resp, "cancelled", False):
                    _log(f"task cancellation requested: {task_id}")
                    if owner_task and not owner_task.done():
                        owner_task.cancel()
                    return
            except asyncio.CancelledError:
                return
            except Exception as exc:
                if self._stop_event and self._stop_event.is_set():
                    return
                _log(f"task heartbeat failed: {task_id}: {exc}")

    async def _run_task_subprocess(
        self, task_name: str, session_id: str, kwargs_json: str, timeout: int
    ) -> tuple[str, str]:
        """Spawn the task in a child process and wait for it to finish."""
        return await run_task_subprocess(
            self.module_path,
            self.class_name,
            task_name,
            session_id,
            kwargs_json,
            timeout,
        )
