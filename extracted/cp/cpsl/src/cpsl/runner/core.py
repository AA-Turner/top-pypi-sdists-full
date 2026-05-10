"""Capsule runner — connects to the gateway, dispatches messages and tasks.

Not a public API. Invoked inside the runtime:

    python -m cpsl.runner module:ClassName
"""

from __future__ import annotations

import asyncio
import importlib
import os
import signal
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from aiohttp import web

from ..channel import Channel as GrpcChannel
from ..clients.capsule import (
    DataServiceStub,
    RunnerServiceStub,
    SessionServiceStub,
    TaskServiceStub,
)
from ..constants import (
    KV_COLLECTION as _KV_COLLECTION,
    SCOPE_APP,
    SETTINGS_COLLECTION,
    SettingDecl,
)
from ..db import (
    Collection,
    CollectionManager,
    DatabaseProxy,
)
from ..decorators import (
    _BOOT_ATTR,
    _SHUTDOWN_ATTR,
    _ENTER_ATTR,
    _EXIT_ATTR,
    _MESSAGE_ATTR,
    _MESSAGE_LABEL_ATTR,
    _MESSAGE_NAME_ATTR,
    _ACTION_ATTR,
    _ACTION_NAME_ATTR,
    _SCHEDULE_ATTR,
)
from ..session import Session
from ..task_types import TaskDescriptor, GlobalTaskQuery
from ..workflow import Workflow
from .gateway import RunnerGatewayMixin
from .routes import RunnerRouteMixin
from .session import RunnerSessionMixin
from .shared import (
    StdoutJsonInterceptor,
    _HOP_HEADERS,
    _MAX_BACKOFF,
    _PORT,
    _RPC_WORKERS,
    _SUBMIT_RESULT_WORKERS,
    _find_hook,
    _log,
    _maybe_await,
)
from .tasks import RunnerTaskMixin


class Runner(RunnerSessionMixin, RunnerTaskMixin, RunnerGatewayMixin, RunnerRouteMixin):
    # Latest Runner instance for this process. Task subprocess shims reuse this
    # slot to attach gateway stubs to helper APIs that run outside the main
    # event loop.
    _instance_ref: "Runner | None" = None

    def set_preview_port(self, port: int | None) -> None:
        self._preview_port = port

    def __init__(self, module_path: str, target_name: str) -> None:
        Runner._instance_ref = self
        self.module_path = module_path
        self.class_name = target_name

        from ..app import App

        obj = getattr(importlib.import_module(module_path), target_name)
        if isinstance(obj, App):
            obj._finalize_config()
            self._cls = None
            self._app_obj: App | None = obj
            self._app_name = obj.name
        else:
            self._cls = obj
            self._app_obj = None
            self._app_name = getattr(obj, "_cpsl_config", {}).get("app_name", target_name)

        self._instance: Any = None
        self._hooks: dict[str, Any] = {}
        self._message_handlers: dict[str, Callable] = {}
        self._message_handler_labels: dict[str, str] = {}
        self._session_handlers: dict[str, Callable] = {}
        self._action_handlers: dict[str, Callable] = {}
        self._tasks: dict[str, TaskDescriptor] = {}
        self._schedules: dict[str, Any] = {}
        self._schedule_locks: dict[str, asyncio.Lock] = {}
        self._sessions: dict[str, Session] = {}
        self._session_locks: dict[str, asyncio.Lock] = {}
        self._workflows: dict[str, Workflow] = {}
        self._home_suggestions_cache: dict[str, tuple[float, list[dict[str, Any]]]] = {}

        self._runner_stub: RunnerServiceStub | None = None
        self._session_stub: SessionServiceStub | None = None
        self._task_stub: TaskServiceStub | None = None
        self._data_stub: DataServiceStub | None = None
        self._channel: GrpcChannel | None = None

        self._app_id: str = ""
        self._user_id: str = ""
        self._version_id: str = ""
        self._version_type: str = ""
        self._runner_version_type: str = ""
        self._data_app_id: str = ""
        self._retries: int = 0
        self._loop: asyncio.AbstractEventLoop | None = None
        self._stop_event: asyncio.Event | None = None
        self._thread_stop: threading.Event | None = None
        self._keep_warm: int = int(os.environ.get("CAPSULE_KEEP_WARM_SECONDS", "0"))
        self._last_activity: float = time.time()
        self._active_count: int = 0
        self._preview_port: int | None = None
        self._active_lock = asyncio.Lock()
        self._submit_executor = ThreadPoolExecutor(
            max_workers=max(1, _SUBMIT_RESULT_WORKERS),
            thread_name_prefix="cpsl-submit-result",
        )
        self._rpc_executor = ThreadPoolExecutor(
            max_workers=max(1, _RPC_WORKERS),
            thread_name_prefix="cpsl-rpc",
        )

    def _ensure_rpc_executor(self) -> ThreadPoolExecutor:
        executor = getattr(self, "_rpc_executor", None)
        if executor is None:
            executor = ThreadPoolExecutor(
                max_workers=max(1, _RPC_WORKERS),
                thread_name_prefix="cpsl-rpc",
            )
            self._rpc_executor = executor
        return executor

    async def _run_rpc(self, fn, *args):
        return await asyncio.get_running_loop().run_in_executor(
            self._ensure_rpc_executor(),
            fn,
            *args,
        )

    async def _proxy_to_localhost(self, request: web.Request, port: int, path: str) -> web.Response:
        import aiohttp as _aiohttp

        url = f"http://localhost:{port}/{path}"
        if request.query_string:
            url += f"?{request.query_string}"

        fwd = {k: v for k, v in request.headers.items() if k.lower() not in _HOP_HEADERS}
        fwd["Host"] = f"localhost:{port}"

        try:
            async with _aiohttp.ClientSession() as s:
                resp = await s.request(
                    request.method,
                    url,
                    headers=fwd,
                    data=await request.read() if request.can_read_body else None,
                )
                body = await resp.read()
                hdrs = {k: v for k, v in resp.headers.items() if k.lower() not in _HOP_HEADERS}
                return web.Response(status=resp.status, body=body, headers=hdrs)
        except _aiohttp.ClientConnectorError:
            return web.json_response({"error": "port_not_ready", "port": port}, status=503)

    async def _handle_preview(self, request: web.Request) -> web.Response:
        port = int(request.match_info["port"])
        path = request.match_info.get("path", "")
        return await self._proxy_to_localhost(request, port, path)

    async def _handle_preview_fallback(self, request: web.Request) -> web.Response:
        if self._preview_port is None:
            raise web.HTTPNotFound()
        path = request.match_info.get("path_info", "").lstrip("/")
        return await self._proxy_to_localhost(request, self._preview_port, path)

    async def boot(self) -> None:
        if self._app_obj is not None:
            self._instance = self._app_obj
        else:
            self._instance = self._cls()
        for key in (_BOOT_ATTR, _SHUTDOWN_ATTR, _ENTER_ATTR, _EXIT_ATTR):
            self._hooks[key] = _find_hook(self._instance, key)

        self._message_handlers = {}
        self._message_handler_labels = {}
        if self._app_obj is not None:
            self._message_handlers = dict(self._app_obj._message_handlers)
            self._message_handler_labels = dict(self._app_obj._message_handler_labels)
            self._session_handlers = dict(self._app_obj._session_handlers)
            self._action_handlers = dict(self._app_obj._action_handlers)
        else:
            for name in dir(self._instance):
                fn = getattr(self._instance, name, None)
                if not callable(fn):
                    continue
                if getattr(fn, _MESSAGE_ATTR, False):
                    msg_name = getattr(fn, _MESSAGE_NAME_ATTR, "")
                    if msg_name in self._message_handlers:
                        label = "default" if msg_name == "" else msg_name
                        raise RuntimeError(f"Duplicate @cpsl.message handler for {label!r}")
                    self._message_handlers[msg_name] = fn
                    if msg_name:
                        self._message_handler_labels[msg_name] = (
                            getattr(fn, _MESSAGE_LABEL_ATTR, "") or msg_name
                        )
                if getattr(fn, _ACTION_ATTR, False):
                    self._action_handlers[getattr(fn, _ACTION_NAME_ATTR, name)] = fn
        self._hooks[_MESSAGE_ATTR] = self._message_handlers.get("")

        for name in dir(self._instance):
            attr = getattr(self._instance, name, None)
            if isinstance(attr, TaskDescriptor):
                attr._bind(self._instance, self)
                self._tasks[name] = attr
            cron = getattr(attr, _SCHEDULE_ATTR, None)
            if cron and isinstance(cron, str):
                self._schedules[name] = attr
                self._schedule_locks[name] = asyncio.Lock()

        if self._app_obj is not None:
            for wf in self._app_obj._workflows:
                self._workflows[wf.name] = wf

        self._rebind_services()

        if self._hooks[_BOOT_ATTR]:
            await _maybe_await(self._hooks[_BOOT_ATTR]())
        self._last_activity = time.time()

    def _rebind_services(self) -> None:
        if self._instance is None:
            return
        if self._data_stub:
            db = DatabaseProxy(self._data_stub, self._data_app_id)
            self._instance.db = db
            scopes = {name: decl.scope for name, decl in self._get_all_collections().items()}
            self._instance.collections = CollectionManager(
                self._data_stub,
                self._data_app_id,
                default_scope=SCOPE_APP,
                collection_scopes=scopes,
            )
            self._bind_collection_refs(db)
            self._bind_settings_accessor()
            self._bind_app_kv()
        if self._task_stub:
            self._instance.tasks = GlobalTaskQuery(self)
            for desc in self._tasks.values():
                desc._runner = self

    def _bind_collection_refs(self, db: DatabaseProxy) -> None:
        """Wire each ``CollectionRef`` to its live ``Collection`` proxy."""
        from ..app import _REGISTERED_CLASSES
        from ..db import CollectionRef

        refs: list[CollectionRef] = []
        for reg in _REGISTERED_CLASSES:
            for ref in reg.get("collection_refs", []):
                if isinstance(ref, CollectionRef):
                    ref._bound = getattr(db, ref.name)
                    refs.append(ref)
        self._collection_refs = refs

    def _bind_settings_accessor(self) -> None:
        """Wire the SettingsAccessor to the _settings Mongo collection."""
        if not self._data_stub:
            return
        app = self._app_obj
        if app is None:
            return
        if not app._settings:
            return
        settings_col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)
        app.settings._bind(settings_col)

    def _bind_app_kv(self) -> None:
        if not self._data_stub:
            return
        app = self._app_obj
        if app is None:
            return
        app._kv = Collection(self._data_stub, self._data_app_id, _KV_COLLECTION)

    def _get_all_settings(self) -> dict[str, SettingDecl]:
        """Collect all SettingDecl from registered classes."""
        from ..app import _REGISTERED_CLASSES
        from ..constants import _STR_TO_TYPE

        settings: dict[str, SettingDecl] = {}
        for reg in _REGISTERED_CLASSES:
            for s in reg.get("settings", []):
                if isinstance(s, dict):
                    settings[s["name"]] = SettingDecl(
                        name=s["name"],
                        scope=s.get("scope", "app"),
                        type=_STR_TO_TYPE.get(s.get("type", "str"), str),
                        default=s.get("default"),
                        options=tuple(s["options"]) if s.get("options") else None,
                        label=s.get("label"),
                    )
                elif isinstance(s, SettingDecl):
                    settings[s.name] = s
        return settings

    async def shutdown(self) -> None:
        if self._hooks.get(_SHUTDOWN_ATTR):
            await _maybe_await(self._hooks[_SHUTDOWN_ATTR]())

    async def serve(self) -> None:
        gw = os.environ.get("CAPSULE_GATEWAY_HOST", "localhost:1980")
        self._app_id = os.environ.get("CAPSULE_APP_ID", "")
        self._user_id = os.environ.get("CAPSULE_USER_ID", "")
        self._version_id = os.environ.get("CAPSULE_VERSION_ID", "")
        raw_version_type = os.environ.get("CAPSULE_VERSION_TYPE", "")
        env_version_type = os.environ.get("CAPSULE_ENV_TYPE", "")
        self._version_type = self._canonical_env_type(env_version_type or raw_version_type)
        self._runner_version_type = (
            os.environ.get("CAPSULE_RUNNER_VERSION_TYPE", "")
            or raw_version_type
            or self._version_type
        )
        self._data_app_id = f"{self._app_id}_dev" if self._version_type == "serve" else self._app_id
        token = os.environ.get("CAPSULE_RUNNER_TOKEN") or None
        self._loop = asyncio.get_running_loop()

        _log(f"connecting → {gw} (keep_warm={self._keep_warm}s)")

        http_app = web.Application()
        http_app.router.add_get("/health", lambda _: web.json_response({"ok": True}))
        http_app.router.add_route("*", "/_capsule/preview/{port}/{path:.*}", self._handle_preview)
        self._mount_endpoints(http_app)
        http_app.router.add_route("*", "/{path_info:.*}", self._handle_preview_fallback)
        http_runner = web.AppRunner(http_app)
        await http_runner.setup()
        try:
            await web.TCPSite(http_runner, "0.0.0.0", _PORT, reuse_address=True).start()
        except OSError:
            _log(f"port {_PORT} in use, skipping http")

        stop = asyncio.Event()
        self._stop_event = stop
        for sig in (signal.SIGTERM, signal.SIGINT):
            self._loop.add_signal_handler(sig, lambda s=sig: self._request_stop(s))

        while not stop.is_set():
            self._disconnect()
            self._connect(gw, token)

            try:
                self._register()
                self._retries = 0
                _log(f"connected app_id={self._app_id}")

                self._rebind_services()

                thread_stop = threading.Event()
                self._thread_stop = thread_stop
                hb_thread = threading.Thread(
                    target=self._heartbeat_loop, args=(thread_stop,), daemon=True
                )
                rx_thread = threading.Thread(
                    target=self._recv_loop, args=(thread_stop,), daemon=True
                )
                hb_thread.start()
                rx_thread.start()

                while not stop.is_set() and hb_thread.is_alive() and rx_thread.is_alive():
                    await asyncio.sleep(1)

                thread_stop.set()
                self._disconnect()
                join_timeout = 0.5 if stop.is_set() else 2
                hb_thread.join(timeout=join_timeout)
                rx_thread.join(timeout=join_timeout)
                self._thread_stop = None

                if stop.is_set():
                    break

            except Exception as exc:
                _log(f"connection error: {exc}")

            backoff = min(2**self._retries, _MAX_BACKOFF)
            self._retries += 1
            _log(f"reconnecting in {backoff}s (attempt {self._retries})")
            try:
                await asyncio.wait_for(stop.wait(), timeout=backoff)
                break
            except asyncio.TimeoutError:
                pass

        self._disconnect()
        self._thread_stop = None
        self._stop_event = None

        try:
            await asyncio.wait_for(self.shutdown(), timeout=5)
        except asyncio.TimeoutError:
            _log("shutdown hook timed out")

        try:
            await asyncio.wait_for(http_runner.cleanup(), timeout=3)
        except asyncio.TimeoutError:
            _log("http cleanup timed out")


def main() -> None:
    if len(sys.argv) != 2 or ":" not in sys.argv[1]:
        print("Usage: python -m cpsl.runner <module>:<name>", file=sys.stderr)
        sys.exit(1)

    mod, cls = sys.argv[1].rsplit(":", 1)

    sys.stdout = StdoutJsonInterceptor(sys.__stdout__)
    sys.stderr = StdoutJsonInterceptor(sys.__stdout__)

    async def _run():
        r = Runner(mod, cls)
        await r.boot()
        await r.serve()

    asyncio.run(_run())


if __name__ == "__main__":
    main()
