from __future__ import annotations

import asyncio
import json
import signal
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from ..channel import Channel as GrpcChannel
from ..clients.capsule import (
    DataServiceStub,
    GetSecretRequest,
    HeartbeatRequest,
    IngestLogsRequest,
    KeepAliveRequest,
    RecvRequest,
    RegisterRequest,
    RunnerServiceStub,
    SecretServiceStub,
    SessionServiceStub,
    SubmitResultRequest,
    TaskServiceStub,
)
from .shared import (
    _HEARTBEAT_INTERVAL,
    _PORT,
    _SUBMIT_RESULT_WORKERS,
    _log,
    _log_buffer,
    _log_buffer_lock,
)


class RunnerGatewayMixin:
    def _submit(
        self,
        request_id: str,
        text: str,
        done: bool = False,
        session_id: str = "",
        block_json: str = "",
    ) -> None:
        if not self._runner_stub:
            return
        req = SubmitResultRequest(
            request_id=request_id,
            text=text,
            done=done,
            session_id=session_id,
            block_json=block_json,
        )

        def _call() -> None:
            start = time.time()
            try:
                self._runner_stub.submit_result(req)
            except Exception as exc:
                _log(f"submit_result failed: {exc}")
            finally:
                elapsed = time.time() - start
                if elapsed > 1:
                    _log(
                        "submit_result slow: "
                        f"request_id={request_id} session_id={session_id} elapsed={elapsed:.2f}s"
                    )

        executor = getattr(self, "_submit_executor", None)
        if executor is None:
            executor = ThreadPoolExecutor(
                max_workers=max(1, _SUBMIT_RESULT_WORKERS),
                thread_name_prefix="cpsl-submit-result",
            )
            self._submit_executor = executor

        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = self._loop if self._loop and self._loop.is_running() else None

        if loop and loop.is_running():
            loop.run_in_executor(executor, _call)
            return

        try:
            self._runner_stub.submit_result(req)
        except Exception as exc:
            _log(f"submit_result failed: {exc}")

    def _submit_block(self, session_id: str, block_json: str) -> None:
        """Send a structured block as a session-scoped message.

        Blocks are fire-and-forget — no result channel is opened because the
        UI fetches current state from the task/resource directly.
        """
        self._submit(
            request_id=str(uuid.uuid4()),
            text="",
            done=True,
            session_id=session_id,
            block_json=block_json,
        )

    def _submit_widget_update(self, session_id: str, *, reason: str = "data") -> None:
        block_json = json.dumps(
            {
                "id": f"widget_update_{session_id}",
                "type": "widget_update",
                "payload": {"reason": reason, "session_id": session_id},
            }
        )
        self._submit(
            request_id=str(uuid.uuid4()),
            text="",
            done=True,
            session_id=session_id,
            block_json=block_json,
        )

    def _submit_session_data_snapshot(self, session_id: str, data_json: str) -> None:
        block_json = json.dumps(
            {
                "event": "session_data_snapshot",
                "data_json": data_json or "{}",
            }
        )
        self._submit(
            request_id=str(uuid.uuid4()),
            text="",
            done=True,
            session_id=session_id,
            block_json=block_json,
        )

    async def _stream_chunks(self, request_id: str, chunks, session_id: str = "") -> None:
        full = ""
        async for text in chunks:
            if text.startswith(full):
                delta = text[len(full) :]
            else:
                delta = text
            if delta:
                self._submit(request_id, delta, session_id=session_id)
            full += delta
        self._submit(request_id, "", done=True, session_id=session_id)
        self._last_activity = time.time()

    def _connect(self, gw: str, token: str | None) -> None:
        extra_md = []
        if self._version_type:
            extra_md.append(("x-version-type", self._version_type))
        if self._version_id:
            extra_md.append(("x-version-id", self._version_id))
        ch = GrpcChannel(addr=gw, token=token, extra_metadata=extra_md or None)
        self._channel = ch
        self._runner_stub = RunnerServiceStub(ch)
        self._session_stub = SessionServiceStub(ch)
        self._task_stub = TaskServiceStub(ch)
        self._data_stub = DataServiceStub(ch)

        from ..secret import _set_resolver

        _set_resolver(self._fetch_secret)

    def _fetch_secret(self, name: str) -> str:
        stub = SecretServiceStub(self._channel)
        resp = stub.get_secret(GetSecretRequest(name=name))
        if not resp.ok:
            raise ValueError(f"secret '{name}' not found: {resp.err_msg}")
        return resp.value

    def _disconnect(self) -> None:
        ch = self._channel
        self._channel = None
        if ch:
            try:
                ch.close()
            except Exception:
                pass
        executor = getattr(self, "_submit_executor", None)
        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=False)
            self._submit_executor = None
        rpc_executor = getattr(self, "_rpc_executor", None)
        if rpc_executor is not None:
            rpc_executor.shutdown(wait=False, cancel_futures=False)
            self._rpc_executor = None

    def _request_stop(self, sig: signal.Signals | None = None) -> None:
        if sig is not None:
            _log(f"received {sig.name}, shutting down")
        if self._thread_stop:
            self._thread_stop.set()
        self._disconnect()
        if self._stop_event and not self._stop_event.is_set():
            self._stop_event.set()

    def _register(self) -> None:
        self._runner_stub.register(
            RegisterRequest(
                app_id=self._app_id,
                version_id=self._version_id,
                version_type=self._runner_version_type,
            )
        )

    def _flush_log_buffer(self) -> None:
        with _log_buffer_lock:
            if not _log_buffer:
                return
            records = list(_log_buffer)
            _log_buffer.clear()
        if not self._runner_stub or not self._app_id:
            return
        try:
            self._runner_stub.ingest_logs(
                IngestLogsRequest(
                    app_id=self._app_id,
                    records=records,
                    version_id=self._version_id,
                )
            )
        except Exception as exc:
            _log(f"ingest_logs failed ({len(records)} records dropped): {exc}")

    def _heartbeat_loop(self, stop: threading.Event) -> None:
        consecutive_failures = 0
        while not stop.is_set():
            try:
                resp = self._runner_stub.heartbeat(
                    HeartbeatRequest(
                        app_id=self._app_id,
                        version_type=self._runner_version_type,
                    )
                )
                consecutive_failures = 0
                if resp.update and resp.update.sdk_version:
                    self._do_update(resp.update.sdk_version)
                if resp.keep_warm_seconds > 0:
                    self._keep_warm = resp.keep_warm_seconds

                ttl = self._keepalive_ttl()
                if ttl > 0:
                    try:
                        self._runner_stub.keep_alive(
                            KeepAliveRequest(
                                app_id=self._app_id,
                                ttl_seconds=ttl,
                                version_type=self._runner_version_type,
                            )
                        )
                    except Exception as exc:
                        if stop.is_set():
                            return
                        _log(f"keepalive failed: {exc}")
                elif self._keep_warm > 0:
                    _log("keep-warm expired, shutting down")
                    self._request_stop()
                    return
            except Exception as exc:
                if stop.is_set():
                    return
                consecutive_failures += 1
                _log(f"heartbeat failed: {exc}")
                if consecutive_failures >= 3:
                    return

            self._self_ping()
            stop.wait(_HEARTBEAT_INTERVAL)

    def _self_ping(self) -> None:
        """Hit our own /health endpoint to reset idle timeout."""
        try:
            import urllib.request

            urllib.request.urlopen(f"http://127.0.0.1:{_PORT}/health", timeout=2).close()
        except Exception:
            pass

    def _recv_loop(self, stop: threading.Event) -> None:
        import betterproto

        while not stop.is_set():
            try:
                for resp in self._runner_stub.recv(
                    RecvRequest(
                        app_id=self._app_id,
                        version_type=self._runner_version_type,
                    )
                ):
                    if stop.is_set():
                        return

                    field_name, value = betterproto.which_one_of(resp, "payload")

                    if field_name == "message" and value and value.request_id and self._loop:
                        asyncio.run_coroutine_threadsafe(self._handle(value), self._loop)
                    elif field_name == "task" and value and value.task_id and self._loop:
                        asyncio.run_coroutine_threadsafe(self._handle_task(value), self._loop)
                    elif field_name == "schedule" and value and value.schedule_name and self._loop:
                        asyncio.run_coroutine_threadsafe(self._handle_schedule(value), self._loop)
            except Exception as exc:
                if not stop.is_set():
                    _log(f"recv stream error: {exc}")
                return

    def _do_update(self, version: str) -> None:
        _log(f"updating SDK → {version}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", f"cpsl=={version}"],
                stdout=sys.stderr,
                stderr=sys.stderr,
            )
            _log("SDK updated, takes effect on next reconnect")
        except Exception as exc:
            _log(f"update failed: {exc}")
