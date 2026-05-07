"""Capsule runner — connects to the gateway, dispatches messages and tasks.

Not a public API. Invoked inside the runtime:

    python -m cpsl.runner module:ClassName
"""

from __future__ import annotations

import asyncio
import contextvars
import importlib
import inspect
import io
import json
import os
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import uuid
from typing import Any

from aiohttp import web

from .channel import Channel as GrpcChannel
from .integration import IntegrationCredentials, KNOWN_SECRET_INTEGRATIONS
from .session import SessionChannel
from .clients.capsule import (
    ClaimTaskRequest,
    CompleteTaskRequest,
    DataServiceStub,
    GetCollectionSchemaRequest,
    GetSecretRequest,
    GetSessionRequest,
    GetUserIntegrationsRequest,
    HeartbeatRequest,
    InboundMessage,
    IngestLogsRequest,
    IntegrationCredential,
    KeepAliveRequest,
    LogRecord,
    NotifySessionRequest,
    RecvRequest,
    RegisterRequest,
    RunnerServiceStub,
    SaveSessionDataRequest,
    SecretServiceStub,
    SessionServiceStub,
    SubmitResultRequest,
    TaskDelivery,
    TaskHeartbeatRequest,
    TaskServiceStub,
    TaskStatus,
)
from .constants import (
    ACCESS_AUTHENTICATED,
    ACCESS_PUBLIC,
    CollectionDecl,
    DEFAULT_CHANNEL_TYPE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_TOKEN_TYPE,
    HEADER_AUTHENTICATED,
    HEADER_EMAIL,
    HEADER_ORG_ID,
    HEADER_SESSION_ID,
    HEADER_USER_ID,
    HISTORY_FETCH_COUNT,
    KV_COLLECTION as _KV_COLLECTION,
    MAX_PAGE_SIZE,
    PAGE_TYPE_REACT,
    SCOPE_APP,
    SETTINGS_COLLECTION,
    SETTINGS_KEY_FIELD,
    SettingDecl,
    _TYPE_TO_STR,
)
from .app import _ACCESS_ATTR
from .db import (
    Collection,
    CollectionManager,
    DatabaseProxy,
    ScopedDatabaseProxy,
    reset_active_identity,
    set_active_identity,
)
from .decorators import (
    _BOOT_ATTR,
    _SHUTDOWN_ATTR,
    _ENTER_ATTR,
    _EXIT_ATTR,
    _MESSAGE_ATTR,
    _SCHEDULE_ATTR,
    _ENDPOINT_ATTR,
    _ASGI_ATTR,
)
from .msg import Message
from .home import HomeContext, serialize_suggestions
from .session import ReplyStream, RequestContext, Session, UserInfo, _track_data_value
from .task_types import TaskDescriptor, GlobalTaskQuery
from .task_exec import _retry_on_errors, run_task_subprocess
from .workflow import Workflow, WorkflowInput

_PORT = 8080
_HEARTBEAT_INTERVAL = 10
_MAX_BACKOFF = 5
_GRPC_RETRY_TRIES = 4
_SUBMIT_RESULT_WORKERS = int(os.environ.get("CAPSULE_SUBMIT_RESULT_WORKERS", "1"))
_RPC_WORKERS = int(os.environ.get("CAPSULE_RPC_WORKERS", "16"))

# Query keys reserved by the gateway for routing/identity; strip before
# handing off to user-defined data sources so they don't collide with kwargs.
_RESERVED_QUERY_KEYS = frozenset({"version_id", "session_id"})
_GRPC_RETRY_DELAY = 2
_BRANDING_LOGO_ROUTE = "/branding/logo"

_current_task_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "_current_task_id", default=""
)

_log_buffer: list[LogRecord] = []
_log_buffer_lock = threading.Lock()
_LOG_BUFFER_MAX = 500
_ASSET_MAX_BYTES = 512 * 1024  # 512 KB — skip data-URI for huge files


def _asset_to_data_uri(path: str) -> str | None:
    """Read a local asset file and return a data URI, or None if unreadable."""
    import base64
    import mimetypes

    full = os.path.join(os.getcwd(), path)
    if not os.path.isfile(full):
        _log(f"theme asset not found: {full}")
        return None
    if os.path.getsize(full) > _ASSET_MAX_BYTES:
        _log(f"theme asset too large for inline: {full}")
        return None
    ct = mimetypes.guess_type(full)[0] or "application/octet-stream"
    data = open(full, "rb").read()
    return f"data:{ct};base64,{base64.b64encode(data).decode()}"


def _serialize_collection_columns(columns) -> list | None:
    if not columns:
        return None
    has_types = any(
        getattr(c, "type", "text") != "text"
        or getattr(c, "label", None)
        or getattr(c, "format", None)
        for c in columns
    )
    if has_types:
        return [
            {k: v for k, v in {
                "key": c.key,
                "type": getattr(c, "type", "text") or "text",
                "label": getattr(c, "label", None),
                "format": getattr(c, "format", None),
            }.items() if v is not None}
            for c in columns
        ]
    return [c.key for c in columns]


def _parse_integration_credential(ic: IntegrationCredential) -> IntegrationCredentials:
    """Build an IntegrationCredentials from a protobuf IntegrationCredential.

    For secret-based integrations the gateway JSON-encodes the field map
    into ``access_token``. We unpack it here so ``cred.fields`` is populated.
    """
    is_secret = ic.type in KNOWN_SECRET_INTEGRATIONS
    secret_fields: dict[str, str] = {}
    if is_secret and ic.access_token:
        try:
            parsed = json.loads(ic.access_token)
            if isinstance(parsed, dict):
                secret_fields = parsed
        except (json.JSONDecodeError, TypeError):
            pass

    return IntegrationCredentials(
        access_token="" if secret_fields else ic.access_token,
        token_type=ic.token_type or DEFAULT_TOKEN_TYPE,
        scopes=list(ic.scopes),
        expires_at=ic.expires_at,
        fields=secret_fields,
    )


class StdoutJsonInterceptor(io.TextIOBase):
    """Intercepts stdout/stderr and writes structured JSON lines to the original stream.

    The Go side (serve controller) tails the process output, parses JSON lines,
    and routes them to S2. For deploy-type apps the runner also flushes buffered
    records to the gateway via IngestLogs gRPC (see _flush_log_buffer).
    """

    def __init__(self, stream=sys.__stdout__):
        self._stream = stream

    def write(self, buf: str) -> int:
        if not buf:
            return 0
        try:
            task_id = _current_task_id.get("")
            for line in buf.splitlines():
                if not line:
                    continue
                record = {"message": line, "stream": "stdout"}
                if task_id:
                    record["task_id"] = task_id
                self._stream.write(json.dumps(record) + "\n")
                with _log_buffer_lock:
                    if len(_log_buffer) < _LOG_BUFFER_MAX:
                        _log_buffer.append(LogRecord(stream="stdout", text=line, task_id=task_id))
            self._stream.flush()
        except Exception:
            self._stream.write(buf)
            self._stream.flush()
        return len(buf)

    def flush(self) -> None:
        self._stream.flush()

    def fileno(self) -> int:
        try:
            return self._stream.fileno()
        except (AttributeError, io.UnsupportedOperation):
            return -1

    def isatty(self) -> bool:
        return False

    def writable(self) -> bool:
        return True


_HOP_HEADERS = frozenset(
    (
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
        "host",
    )
)


def _log(msg: str) -> None:
    print(f"[cpsl] {msg}", flush=True)


def _find_hook(instance: object, attr: str):
    for name in dir(instance):
        fn = getattr(instance, name, None)
        if callable(fn) and getattr(fn, attr, False):
            return fn
    return None


async def _maybe_await(result):
    if asyncio.iscoroutine(result):
        return await result
    return result


def _wants_request_context(fn) -> bool:
    """True if fn's first parameter is named 'ctx' or type-hinted as a context object."""
    try:
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        if not params:
            return False
        first = params[0]
        if first.name == "ctx":
            return True
        hint = first.annotation
        if hint is inspect.Parameter.empty:
            return False
        return hint in (RequestContext, HomeContext) or (
            isinstance(hint, str) and ("RequestContext" in hint or "HomeContext" in hint)
        )
    except (ValueError, TypeError):
        return False


def _wants_session(fn) -> bool:
    """True if fn declares a parameter named 'session' or type-hinted as Session."""
    try:
        sig = inspect.signature(fn)
        for param in sig.parameters.values():
            if param.name == "session":
                return True
            hint = param.annotation
            if hint is inspect.Parameter.empty:
                continue
            if hint is Session or (isinstance(hint, str) and "Session" in hint):
                return True
    except (ValueError, TypeError):
        return False
    return False


class Runner:
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

        from .app import App

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
            self._ensure_rpc_executor(), fn, *args,
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
        for key in (_BOOT_ATTR, _SHUTDOWN_ATTR, _ENTER_ATTR, _EXIT_ATTR, _MESSAGE_ATTR):
            self._hooks[key] = _find_hook(self._instance, key)

        msg_handlers = [
            name
            for name in dir(self._instance)
            if callable(getattr(self._instance, name, None))
            and getattr(getattr(self._instance, name, None), _MESSAGE_ATTR, False)
        ]
        if len(msg_handlers) > 1:
            raise RuntimeError(
                f"Only one @cpsl.message() handler allowed per app, "
                f"found {len(msg_handlers)}: {', '.join(sorted(msg_handlers))}"
            )

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
        from .app import _REGISTERED_CLASSES
        from .db import CollectionRef

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
        from .app import _REGISTERED_CLASSES
        from .constants import _STR_TO_TYPE

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

    @staticmethod
    def _set_session_on_refs(session: object | None):
        return set_active_identity(session)

    @staticmethod
    def _clear_session_on_refs(token) -> None:
        reset_active_identity(token)

    @staticmethod
    def _build_request_identity(request: web.Request) -> object:
        owner_id = request.headers.get(HEADER_ORG_ID, "")
        return SimpleNamespace(
            id=request.headers.get(HEADER_SESSION_ID, ""),
            user=UserInfo(
                id=request.headers.get(HEADER_USER_ID, ""),
                email=request.headers.get(HEADER_EMAIL, "") or None,
                org_id=UserInfo.org_id_from_owner_id(owner_id),
            ),
        )

    async def shutdown(self) -> None:
        if self._hooks.get(_SHUTDOWN_ATTR):
            await _maybe_await(self._hooks[_SHUTDOWN_ATTR]())

    async def _track_start(self) -> None:
        async with self._active_lock:
            self._active_count += 1
            self._last_activity = time.time()

    async def _track_end(self) -> None:
        async with self._active_lock:
            self._active_count = max(0, self._active_count - 1)
            self._last_activity = time.time()

    def _keepalive_ttl(self) -> int:
        if self._active_count > 0:
            return max(self._keep_warm, _HEARTBEAT_INTERVAL) + 10
        idle = time.time() - self._last_activity
        if self._keep_warm > 0 and idle < self._keep_warm:
            return self._keep_warm + 10
        return 0

    async def _hydrate_session(
        self, session: Session, *, strip_last_user_text: str | None = None
    ) -> None:
        """Populate a session from the session service. Single path for all callers."""
        if not self._session_stub:
            return
        try:
            resp = await self._run_rpc(
                self._session_stub.get_session,
                GetSessionRequest(session_id=session.id, history_count=HISTORY_FETCH_COUNT),
            )
            if resp.user_id:
                session.user = UserInfo(
                    id=resp.user_id,
                    email=resp.user_email or None,
                    org_id=resp.org_id or UserInfo.org_id_from_owner_id(resp.owner_id),
                )
            if resp.channel_type:
                session.channel = SessionChannel(type=resp.channel_type)
            if resp.data_json:
                session.data = _track_data_value(json.loads(resp.data_json), session._notify_data_changed)

            raw = [
                Message(text=e.text, sender=e.sender, channel_type=e.channel_type)
                for e in resp.history
            ]

            # Merge consecutive same-sender messages. Streaming replies are
            # persisted as one entry now, but older sessions may still have
            # fragmented chunks from before the gateway-side fix.
            history: list[Message] = []
            for m in raw:
                if history and history[-1].sender == m.sender:
                    history[-1] = Message(
                        text=history[-1].text + m.text,
                        sender=m.sender,
                        channel_type=m.channel_type,
                    )
                else:
                    history.append(m)

            if (
                strip_last_user_text is not None
                and history
                and history[-1].sender == "user"
                and history[-1].text == strip_last_user_text
            ):
                history.pop()
            session.history = history

            if resp.integrations:
                session.integrations = {
                    ic.type: _parse_integration_credential(ic) for ic in resp.integrations
                }
        except Exception as exc:
            _log(f"hydrate_session failed: {exc}")

    async def _get_session(self, msg: InboundMessage) -> tuple[Session, bool]:
        is_new = msg.session_id not in self._sessions

        if is_new:
            session = Session(
                id=msg.session_id,
                user=UserInfo(
                    id=msg.user_id,
                    email=msg.user_email or None,
                    org_id=msg.org_id or UserInfo.org_id_from_owner_id(msg.owner_id),
                ),
                channel=SessionChannel(type=msg.channel_type or DEFAULT_CHANNEL_TYPE),
                history=[],
                data={},
            )
            self._sessions[msg.session_id] = session
        else:
            session = self._sessions[msg.session_id]

        await self._hydrate_session(session, strip_last_user_text=msg.text)
        self._bind_session_db(session)
        session._runner = self
        session._runner_stub = self._runner_stub
        session._session_stub = self._session_stub
        session._app_id = self._app_id
        return session, is_new

    @staticmethod
    def _get_all_collections() -> dict[str, CollectionDecl]:
        from .app import _REGISTERED_CLASSES

        result: dict[str, CollectionDecl] = {}
        for reg in _REGISTERED_CLASSES:
            for raw in reg.get("collections", []):
                decl = CollectionDecl.from_dict(raw) if isinstance(raw, dict) else raw
                result[decl.name] = decl
        return result

    @staticmethod
    def _canonical_env_type(version_type: str) -> str:
        return "serve" if version_type == "serve" else "deploy"

    def _bind_session_db(self, session: Session) -> None:
        if self._data_stub:
            collections = self._get_all_collections()
            scopes = {name: decl.scope for name, decl in collections.items()}
            session._db_proxy = ScopedDatabaseProxy(
                self._data_stub,
                self._data_app_id,
                user_id=session.user.id,
                owner_id=session.user.owner_id,
                session_id=session.id,
                collection_scopes=scopes,
            )
            session._collections_proxy = CollectionManager(
                self._data_stub,
                self._data_app_id,
                default_scope="session",
                user_id=session.user.id,
                owner_id=session.user.owner_id,
                session_id=session.id,
                collection_scopes=scopes,
            )
            session._kv = Collection(self._data_stub, self._data_app_id, _KV_COLLECTION)

    async def _fetch_integrations(
        self, *, email: str = "", owner_id: str = ""
    ) -> dict[str, IntegrationCredentials]:
        """Fetch integrations for either a concrete user or runtime owner."""
        if not self._session_stub or (not email and not owner_id):
            return {}
        env = self._version_type or "deploy"
        try:
            resp = await asyncio.get_running_loop().run_in_executor(
                None,
                self._session_stub.get_user_integrations,
                GetUserIntegrationsRequest(
                    app_id=self._app_id,
                    user_email=email,
                    owner_id=owner_id,
                    env=env,
                ),
            )
            integrations = {ic.type: _parse_integration_credential(ic) for ic in resp.integrations}
            return integrations
        except Exception as exc:
            identity = f"email={email}" if email else f"owner_id={owner_id}"
            _log(
                "fetch_integrations failed "
                f"app_id={self._app_id} env={env} {identity} "
                f"error={type(exc).__name__}: {exc}"
            )
            return {}

    async def _build_request_context(self, request: web.Request) -> RequestContext:
        """Build a RequestContext from gateway-forwarded headers + user integrations."""
        email = request.headers.get(HEADER_EMAIL, "")
        user_id = request.headers.get(HEADER_USER_ID, "")
        owner_id = request.headers.get(HEADER_ORG_ID, "")
        authenticated = request.headers.get(HEADER_AUTHENTICATED) == "true"

        user = UserInfo(
            id=user_id,
            email=email or None,
            org_id=UserInfo.org_id_from_owner_id(owner_id),
        )
        integrations = await self._fetch_integrations(email=email) if email else {}

        return RequestContext(
            user=user,
            integrations=integrations,
            authenticated=authenticated,
            request=request,
        )

    async def _build_home_context(self, request: web.Request) -> HomeContext:
        ctx = await self._build_request_context(request)
        return HomeContext(
            user=ctx.user,
            integrations=ctx.integrations,
            authenticated=ctx.authenticated,
            request=request,
            db=getattr(self._instance, "db", None),
            app=self._app_obj,
        )

    async def _build_request_session(self, request: web.Request) -> Session:
        """Build a Session from gateway-forwarded request headers.

        Data handlers use this for ``session: cpsl.Session`` parameters.
        When a real session id is present, hydrate history/data from the
        session service. Otherwise return an identity-only session shell.
        """
        session_id = request.headers.get(HEADER_SESSION_ID, "")
        user_id = request.headers.get(HEADER_USER_ID, "")
        email = request.headers.get(HEADER_EMAIL, "")
        owner_id = request.headers.get(HEADER_ORG_ID, "")

        if session_id and session_id in self._sessions:
            session = self._sessions[session_id]
        else:
            session = Session(
                id=session_id,
                user=UserInfo(
                    id=user_id,
                    email=email or None,
                    org_id=UserInfo.org_id_from_owner_id(owner_id),
                ),
                channel=SessionChannel(type=DEFAULT_CHANNEL_TYPE),
                history=[],
                data={},
                integrations=await self._fetch_integrations(email=email) if email else {},
            )
            if session_id:
                self._sessions[session_id] = session

        if session_id:
            await self._hydrate_session(session)
        self._bind_session_db(session)
        session._runner = self
        session._runner_stub = self._runner_stub
        session._session_stub = self._session_stub
        session._app_id = self._app_id
        return session

    def _registered_home(self) -> dict[str, Any] | None:
        from .app import _REGISTERED_CLASSES

        for reg in _REGISTERED_CLASSES:
            if reg.get("app_name") == self._app_name and reg.get("home"):
                return dict(reg["home"])
        return None

    def _home_cache_key(self, request: web.Request) -> str:
        return "|".join(
            [
                request.headers.get(HEADER_USER_ID, ""),
                request.headers.get(HEADER_ORG_ID, ""),
                request.headers.get(HEADER_AUTHENTICATED, ""),
            ]
        )

    async def _persist(self, session: Session) -> None:
        if not self._session_stub:
            return
        try:
            await asyncio.get_running_loop().run_in_executor(
                None,
                self._session_stub.save_session_data,
                SaveSessionDataRequest(
                    session_id=session.id,
                    data_json=json.dumps(session.data),
                ),
            )
        except Exception as exc:
            if self._stop_event and self._stop_event.is_set():
                return
            _log(f"save_session failed: {exc}")

    async def _handle(self, item: InboundMessage) -> None:
        lock = self._session_locks.setdefault(item.session_id, asyncio.Lock())
        async with lock:
            await self._handle_locked(item)

    async def _handle_locked(self, item: InboundMessage) -> None:
        await self._track_start()
        rid = item.request_id
        sid = item.session_id
        streamed = False
        session: Session | None = None

        try:
            session, is_new = await self._get_session(item)

            if is_new and self._hooks.get(_ENTER_ATTR):
                await _maybe_await(self._hooks[_ENTER_ATTR](session))

            att_list = None
            if item.attachments:
                from .msg import Attachment as MsgAttachment

                att_list = [
                    MsgAttachment(
                        name=a.filename, content_type=a.content_type, url=a.url, size=a.size
                    )
                    for a in item.attachments
                ]
            user_msg = Message(
                text=item.text,
                sender="user",
                channel_type=session.channel.type,
                attachments=att_list,
            )

            replied = False

            async def _reply(m):
                nonlocal replied
                replied = True
                self._submit(rid, m.text, done=False, session_id=sid)

            async def _stream(chunks):
                nonlocal streamed
                streamed = True
                await self._stream_chunks(rid, chunks, session_id=sid)

            async def _block(block_json: str) -> None:
                self._submit_block(sid, block_json)

            async def _data_changed() -> None:
                await self._persist(session)
                self._submit_widget_update(sid, reason="data")

            async def _notify(m):
                if self._session_stub and hasattr(self._session_stub, "notify_session"):
                    await self._run_rpc(
                        self._session_stub.notify_session,
                        NotifySessionRequest(
                            app_id=self._app_id,
                            session_id=sid,
                            request_id=str(uuid.uuid4()),
                            text=m.text,
                            external_delivery=True,
                        ),
                    )
                    return
                self._submit(str(uuid.uuid4()), m.text, done=True, session_id=sid)

            def _stream_write(text: str) -> None:
                self._submit(rid, text, done=False, session_id=sid)

            session._reply_callback = _reply
            session._stream_callback = _stream
            session._stream_write_callback = _stream_write
            session._stream_reply_factory = None
            session._notify_callback = _notify
            session._block_callback = _block
            session._data_change_callback = _data_changed

            identity_token = self._set_session_on_refs(session)
            try:
                wf_handled = await self._try_workflow_dispatch(session, item.text, _reply, _stream, _block, _stream_write, rid, sid)
                if not wf_handled:
                    handler = self._hooks.get(_MESSAGE_ATTR)
                    if handler:
                        await _maybe_await(handler(session, user_msg))
            finally:
                self._clear_session_on_refs(identity_token)

            if not streamed:
                self._submit(rid, "", done=True, session_id=sid)
        except Exception as exc:
            _log(f"handle error request_id={rid}: {exc}")
            if not streamed and rid:
                self._submit(rid, f"Runner error: {exc}", done=True, session_id=sid)
        finally:
            await self._track_end()
            if session is not None:
                asyncio.ensure_future(self._persist(session))

    def _parse_workflow_envelope(self, text: str) -> tuple[str, str, dict] | None:
        """Parse a workflow action envelope from message text.

        Returns (workflow_name, action, payload) or None.
        """
        if not text.startswith("{"):
            return None
        try:
            obj = json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None
        wf_name = obj.get("__workflow__")
        action = obj.get("__action__")
        if not wf_name or not action:
            return None
        payload = obj.get("__payload__", {})
        return wf_name, action, payload

    async def _try_workflow_dispatch(
        self, session: Session, text: str,
        reply_cb, stream_cb, block_cb, stream_write_cb,
        rid: str, sid: str,
    ) -> bool:
        """Attempt to dispatch as a workflow action. Returns True if handled."""
        envelope = self._parse_workflow_envelope(text)
        if envelope:
            wf_name, action, payload = envelope
            wf = self._workflows.get(wf_name)
            if wf is None:
                return False
            wf_input = WorkflowInput(payload)
            if action == "start":
                if wf._start_handler:
                    session.data["__workflow__"] = wf_name
                    await _maybe_await(wf._start_handler(session, wf_input))
                    return True
            else:
                handler = wf._action_handlers.get(action)
                if handler:
                    await _maybe_await(handler(session, wf_input))
                    return True
            return False

        wf_name = session.data.get("__workflow__")
        if wf_name and wf_name in self._workflows:
            wf = self._workflows[wf_name]
            if wf._message_handler:
                msg = Message(text=text, sender="user", channel_type=session.channel.type)
                await _maybe_await(wf._message_handler(session, msg))
                return True
        return False

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
                await _task_reply(Message(text=full, sender="app", channel_type=session.channel.type))

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
                    self._fire_callback(desc._callback_url, task_id, "cancelled", elapsed, "cancelled")

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
            self._runner_stub.submit_result(
                req
            )
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
        block_json = json.dumps({
            "id": f"widget_update_{session_id}",
            "type": "widget_update",
            "payload": {"reason": reason, "session_id": session_id},
        })
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

        from .secret import _set_resolver

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

    def _collect_meta(self) -> dict:
        from .task_types import _TASK_ATTR

        endpoints: list[dict] = []
        tasks: list[dict] = []
        schedules: list[dict] = []
        channels: list[dict] = []

        if self._instance is not None:
            for name in dir(self._instance):
                attr = getattr(self._instance, name, None)
                if attr is None:
                    continue
                ep = getattr(attr, _ENDPOINT_ATTR, None)
                if ep:
                    endpoints.append(
                        {
                            "method": ep["method"].upper(),
                            "path": ep["path"],
                            "name": name,
                            "authorized": ep.get("authorized", True),
                        }
                    )
                if getattr(attr, _TASK_ATTR, False):
                    info: dict = {"name": name}
                    if isinstance(attr, TaskDescriptor):
                        info["retries"] = attr._retries
                        info["timeout"] = attr._timeout
                    tasks.append(info)
                cron = getattr(attr, _SCHEDULE_ATTR, None)
                if cron and isinstance(cron, str):
                    schedules.append({"name": name, "cron": cron})

        from .app import _REGISTERED_CLASSES, _DATA_REGISTRY

        pages: list[dict] = []
        data_sources: list[dict] = []
        theme: dict | None = None
        home: dict | None = None
        chat: dict | None = None
        shell: dict | None = None
        has_message_handler = bool(self._hooks.get(_MESSAGE_ATTR))
        for reg in _REGISTERED_CLASSES:
            has_message_handler = has_message_handler or bool(reg.get("has_message_handler"))
            for ch in reg.get("channels", []):
                channels.append(ch if isinstance(ch, dict) else {"type": str(ch)})
            for p in reg.get("pages", []):
                pages.append(p)
            for ds in reg.get("data_sources", []):
                ds_fn = _DATA_REGISTRY.get(ds)
                ds_access = getattr(ds_fn, _ACCESS_ATTR, ACCESS_PUBLIC) if ds_fn else ACCESS_PUBLIC
                entry = {"name": ds, "access": ds_access}
                if entry not in data_sources:
                    data_sources.append(entry)
            if reg.get("theme"):
                theme = dict(reg["theme"])
                for key in ("logo", "preview_image", "favicon"):
                    asset = theme.get(key)
                    if asset and not asset.startswith(("http://", "https://", "data:")):
                        theme[key] = _asset_to_data_uri(asset)
            if reg.get("home"):
                home = dict(reg["home"])
            if reg.get("chat"):
                chat = dict(reg["chat"])
            if reg.get("shell"):
                shell = dict(reg["shell"])

        collections = self._get_all_collections()
        settings = self._get_all_settings()

        _SETTING_WIDGET_TYPES = frozenset({"toggle", "text_input", "number_input", "select"})

        def _serialize_decl_columns(decl):
            return _serialize_collection_columns(decl.columns)

        def _resolve_widget(node: dict) -> dict:
            if node.get("type") == "table" and "collection_ref" in node:
                ref = node["collection_ref"]
                decl = collections.get(ref)
                resolved: dict = {"type": "table", "collection": ref}
                if decl:
                    cols = _serialize_decl_columns(decl)
                    if cols:
                        resolved["columns"] = cols
                    if decl.sortable:
                        resolved["sortable"] = True
                    if decl.filterable:
                        resolved["filterable"] = True
                    if decl.paginate:
                        resolved["paginate"] = decl.paginate
                    resolved["scope"] = decl.scope
                return resolved
            if node.get("type") == "table" and "collection" in node:
                coll_name = node.get("collection")
                decl = collections.get(coll_name) if coll_name else None
                if decl:
                    node = dict(node)
                    node["scope"] = decl.scope
                return node
            if node.get("type") in _SETTING_WIDGET_TYPES and "setting" in node:
                sname = node["setting"]
                sdecl = settings.get(sname)
                if sdecl:
                    node = dict(node)
                    node["setting_scope"] = sdecl.scope
                    node["setting_type"] = _TYPE_TO_STR.get(sdecl.type, "str")
                    if sdecl.default is not None:
                        node["setting_default"] = sdecl.default
                    if sdecl.options:
                        node["options"] = list(sdecl.options)
                return node
            if "children" in node and isinstance(node["children"], list):
                node = dict(node)
                node["children"] = [_resolve_widget(c) for c in node["children"]]
            return node

        for p in pages:
            if p.get("widget_tree"):
                p["widget_tree"] = _resolve_widget(p["widget_tree"])

        workflows: list[dict] = []
        for reg in _REGISTERED_CLASSES:
            for w in reg.get("workflows", []):
                wf_dict = dict(w) if isinstance(w, dict) else w
                if wf_dict.get("widget_tree"):
                    wf_dict["widget_tree"] = _resolve_widget(wf_dict["widget_tree"])
                workflows.append(wf_dict)

        if home and home.get("widget_tree"):
            home["widget_tree"] = _resolve_widget(home["widget_tree"])
        if chat and chat.get("widget_tree"):
            chat["widget_tree"] = _resolve_widget(chat["widget_tree"])

        meta: dict = {
            "endpoints": endpoints,
            "tasks": tasks,
            "schedules": schedules,
            "channels": channels,
            "pages": pages,
            "workflows": workflows,
            "data_sources": data_sources,
            "collections": [d.to_dict() for d in collections.values()],
            "settings": [s.to_dict() for s in settings.values()],
            "has_message_handler": has_message_handler,
        }
        if theme:
            meta["theme"] = theme
        if home:
            meta["home"] = home
        if chat:
            meta["chat"] = chat
        if shell:
            meta["shell"] = shell
        return meta

    def _mount_endpoints(self, app: web.Application) -> None:
        meta = self._collect_meta()

        def _handle_meta(_req: web.Request) -> web.Response:
            self._last_activity = time.time()
            return web.json_response(meta)

        app.router.add_get("/_meta", _handle_meta)

        from .app import _DATA_REGISTRY

        for ds_name, ds_fn in _DATA_REGISTRY.items():
            app.router.add_get(f"/data/{ds_name}", self._wrap_data_source(ds_fn))
            _log(f"data source mounted: GET /data/{ds_name}")

        app.router.add_get("/collection/{name}", self._wrap_collection_query())
        _log("collection query mounted: GET /collection/{name}")

        if self._get_all_settings():
            app.router.add_get("/settings", self._handle_settings_list())
            app.router.add_get("/settings/{name}", self._handle_settings_get())
            app.router.add_put("/settings/{name}", self._handle_settings_put())
            _log("settings routes mounted: GET/PUT /settings/{name}")

        for page in meta.get("pages", []):
            if page.get("type") == PAGE_TYPE_REACT and page.get("component"):
                pname = page["name"]
                component = page["component"]
                app.router.add_get(
                    f"/pages/{pname}/source",
                    self._wrap_page_source(component),
                )
                _log(f"page source mounted: GET /pages/{pname}/source")

        from .app import _REGISTERED_CLASSES

        for reg in _REGISTERED_CLASSES:
            theme = reg.get("theme")
            if theme and theme.get("logo"):
                logo_path = theme["logo"]
                if not logo_path.startswith(("http://", "https://")):
                    app.router.add_get(_BRANDING_LOGO_ROUTE, self._wrap_logo(logo_path))
                    _log(f"branding logo mounted: GET {_BRANDING_LOGO_ROUTE} → {logo_path}")
                    break

        from .app import _HOME_SUGGESTIONS_REGISTRY

        if self._app_name in _HOME_SUGGESTIONS_REGISTRY:
            app.router.add_get("/_home/suggestions", self._handle_home_suggestions())
            _log("home suggestions mounted: GET /_home/suggestions")

        if self._instance is None:
            return

        for name in dir(self._instance):
            attr = getattr(self._instance, name, None)
            if attr is None:
                continue

            ep = getattr(attr, _ENDPOINT_ATTR, None)
            if ep:
                method = ep["method"].upper()
                path = ep["path"]
                auth = ep.get("authorized", True)
                app.router.add_route(method, path, self._wrap_endpoint(attr, authorized=auth))
                _log(f"endpoint mounted: {method} {path} → {name} (authorized={auth})")

            asgi = getattr(attr, _ASGI_ATTR, None)
            if asgi:
                prefix = asgi["path"].rstrip("/")
                self._mount_asgi(app, prefix, attr(), name)

    def _handle_home_suggestions(self):
        from .app import _HOME_SUGGESTIONS_REGISTRY

        fn = _HOME_SUGGESTIONS_REGISTRY.get(self._app_name)
        home = self._registered_home() or {}
        access = home.get("dynamic_suggestions_access", ACCESS_PUBLIC)
        ttl = int(home.get("dynamic_suggestions_ttl") or 0)
        wants_ctx = _wants_request_context(fn) if fn is not None else False

        async def handler(request: web.Request) -> web.Response:
            if fn is None:
                return web.json_response({"suggestions": []}, status=404)
            if access == ACCESS_AUTHENTICATED and request.headers.get(HEADER_AUTHENTICATED) != "true":
                return web.json_response({"error": "authentication_required"}, status=401)

            now = time.time()
            cache_key = self._home_cache_key(request)
            if ttl > 0:
                cached = self._home_suggestions_cache.get(cache_key)
                if cached and cached[0] > now:
                    return web.json_response({"suggestions": cached[1], "cached": True})

            identity_token = self._set_session_on_refs(self._build_request_identity(request))
            try:
                async def call_handler():
                    if wants_ctx:
                        ctx = await self._build_home_context(request)
                        return await _maybe_await(fn(ctx))
                    return await _maybe_await(fn())

                result = await asyncio.wait_for(call_handler(), timeout=10)
                suggestions = serialize_suggestions(result)
                if ttl > 0:
                    self._home_suggestions_cache[cache_key] = (now + ttl, suggestions)
                return web.json_response({"suggestions": suggestions})
            except asyncio.TimeoutError:
                return web.json_response({"error": "home suggestions timed out"}, status=504)
            except Exception as exc:
                _log(f"home suggestions error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_endpoint(self, fn, *, authorized: bool = True):
        needs_ctx = _wants_request_context(fn)

        async def handler(request: web.Request) -> web.Response:
            if authorized and request.headers.get(HEADER_AUTHENTICATED) != "true":
                return web.json_response({"error": "unauthorized"}, status=401)
            identity_token = self._set_session_on_refs(self._build_request_identity(request))
            try:
                if needs_ctx:
                    ctx = await self._build_request_context(request)
                    result = await _maybe_await(fn(ctx))
                else:
                    result = await _maybe_await(fn(request))
                if isinstance(result, web.Response):
                    return result
                if isinstance(result, dict):
                    return web.json_response(result)
                return web.Response(text=str(result))
            except Exception as exc:
                _log(f"endpoint error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_data_source(self, fn):
        access = getattr(fn, _ACCESS_ATTR, ACCESS_PUBLIC)
        needs_ctx = _wants_request_context(fn)
        needs_session = _wants_session(fn)

        async def handler(request: web.Request) -> web.Response:
            if (
                access == ACCESS_AUTHENTICATED
                and request.headers.get(HEADER_AUTHENTICATED) != "true"
            ):
                return web.json_response({"error": "authentication_required"}, status=401)
            session = await self._build_request_session(request) if needs_session else None
            identity_token = self._set_session_on_refs(
                session if session is not None else self._build_request_identity(request)
            )
            try:
                kwargs = {k: v for k, v in request.query.items() if k not in _RESERVED_QUERY_KEYS}
                if needs_session:
                    kwargs.setdefault("session", session)
                if needs_ctx:
                    ctx = await self._build_request_context(request)
                    result = await _maybe_await(fn(ctx, **kwargs))
                else:
                    result = (
                        await _maybe_await(fn(**kwargs)) if kwargs else await _maybe_await(fn())
                    )
                return web.json_response(result)
            except Exception as exc:
                _log(f"data source error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)
            finally:
                self._clear_session_on_refs(identity_token)

        return handler

    def _wrap_collection_query(self):
        async def handler(request: web.Request) -> web.Response:
            name = request.match_info["name"]
            try:
                db = getattr(self._instance, "db", None)
                if db is None:
                    return web.json_response({"error": "database not available"}, status=503)

                col = getattr(db, name)
                page = int(request.query.get("page", "1"))
                per_page = min(
                    int(request.query.get("per_page", str(DEFAULT_PAGE_SIZE))), MAX_PAGE_SIZE
                )
                sort_field = request.query.get("sort")
                sort_dir = request.query.get("sort_dir", "asc")
                filter_raw = request.query.get("filter")

                query_filter: dict = {}
                if filter_raw:
                    try:
                        parsed = json.loads(filter_raw)
                        if isinstance(parsed, dict):
                            query_filter = parsed
                    except (json.JSONDecodeError, ValueError):
                        pass

                collections = self._get_all_collections()
                decl = collections.get(name)
                scope = request.query.get("scope") or (decl.scope if decl else SCOPE_APP)
                user_id = request.headers.get(HEADER_USER_ID, "")
                owner_id = request.headers.get(HEADER_ORG_ID, "")
                session_id = request.headers.get(HEADER_SESSION_ID, "")
                if scope != SCOPE_APP:
                    scope_decl = decl or CollectionDecl(name=name, scope=scope)
                    sf = scope_decl.scope_filter(
                        user_id=user_id,
                        owner_id=owner_id,
                        session_id=session_id,
                    )
                    query_filter.update(sf)

                dynamic_columns = None
                if self._data_stub:
                    try:
                        schema_resp = await self._run_rpc(
                            self._data_stub.get_collection_schema,
                            GetCollectionSchemaRequest(
                                app_id=self._data_app_id,
                                name=name,
                                scope=scope,
                                user_id=user_id,
                                owner_id=owner_id,
                                session_id=session_id,
                            ),
                        )
                        if schema_resp.found and schema_resp.schema:
                            dynamic_columns = _serialize_collection_columns(schema_resp.schema.columns)
                    except Exception as exc:
                        _log(f"collection schema lookup failed for {name}: {exc}")

                sort_spec = None
                if sort_field:
                    sort_spec = {sort_field: 1 if sort_dir == "asc" else -1}

                skip = (page - 1) * per_page
                data = await col.find(
                    filter=query_filter,
                    sort=sort_spec,
                    skip=skip,
                    limit=per_page,
                )
                total = await col.count(filter=query_filter)

                response = {
                    "data": data,
                    "total": total,
                    "page": page,
                    "per_page": per_page,
                }
                columns = dynamic_columns
                if columns is None and decl:
                    columns = _serialize_collection_columns(decl.columns)
                if columns:
                    response["columns"] = columns
                return web.json_response(response)
            except Exception as exc:
                _log(f"collection query error: {exc}")
                return web.json_response({"error": str(exc)}, status=500)

        return handler

    def _handle_settings_list(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            db = getattr(self._instance, "db", None)
            if db is None:
                return web.json_response({"error": "database not available"}, status=503)

            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            result: dict[str, Any] = {}
            for name, decl in settings.items():
                sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
                filt = {SETTINGS_KEY_FIELD: name, **sf}
                doc = await col.find_one(filt)
                result[name] = doc.get("value", decl.default) if doc else decl.default

            return web.json_response(result)

        return handler

    def _handle_settings_get(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            name = request.match_info["name"]
            decl = settings.get(name)
            if decl is None:
                return web.json_response({"error": f"unknown setting: {name}"}, status=404)

            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
            filt = {SETTINGS_KEY_FIELD: name, **sf}
            doc = await col.find_one(filt)
            value = doc.get("value", decl.default) if doc else decl.default

            return web.json_response({"name": name, "value": value})

        return handler

    def _handle_settings_put(self):
        settings = self._get_all_settings()

        async def handler(request: web.Request) -> web.Response:
            self._last_activity = time.time()
            name = request.match_info["name"]
            decl = settings.get(name)
            if decl is None:
                return web.json_response({"error": f"unknown setting: {name}"}, status=404)

            try:
                body = await request.json()
            except Exception:
                return web.json_response({"error": "invalid JSON body"}, status=400)

            if "value" not in body:
                return web.json_response({"error": "missing 'value' field"}, status=400)

            value = body["value"]
            user_id = request.headers.get(HEADER_USER_ID, "")
            owner_id = request.headers.get(HEADER_ORG_ID, "")
            col = Collection(self._data_stub, self._data_app_id, SETTINGS_COLLECTION)

            sf = decl.scope_filter(user_id=user_id, owner_id=owner_id)
            filt = {SETTINGS_KEY_FIELD: name, **sf}
            existing = await col.find_one(filt)
            if existing:
                await col.update_one(filt, {"$set": {"value": value}})
            else:
                await col.insert_one({**filt, "value": value})

            return web.json_response({"ok": True, "name": name, "value": value})

        return handler

    def _wrap_page_source(self, component_path: str):
        async def handler(request: web.Request) -> web.Response:
            import os

            full_path = os.path.join(os.getcwd(), component_path)
            if not os.path.isfile(full_path):
                return web.json_response({"error": "not found"}, status=404)
            return web.FileResponse(
                full_path,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                    "Cache-Control": "no-cache",
                },
            )

        return handler

    def _wrap_logo(self, logo_path: str):
        import mimetypes

        async def handler(request: web.Request) -> web.Response:
            import os

            full_path = os.path.join(os.getcwd(), logo_path)
            if not os.path.isfile(full_path):
                return web.json_response({"error": "not found"}, status=404)
            ct = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
            return web.FileResponse(
                full_path,
                headers={
                    "Content-Type": ct,
                    "Cache-Control": "public, max-age=3600",
                },
            )

        return handler

    def _mount_asgi(self, app: web.Application, prefix: str, asgi_app, name: str) -> None:
        try:
            from aiohttp_asgi import ASGIApplicationServer

            subapp = ASGIApplicationServer(asgi_app).make_aiohttp_app()
            app.add_subapp(prefix, subapp)
            _log(f"asgi mounted: {prefix}/* → {name}")
        except ImportError:

            async def handler(request: web.Request) -> web.Response:
                try:
                    scope = {
                        "type": "http",
                        "asgi": {"version": "3.0"},
                        "http_version": "1.1",
                        "method": request.method,
                        "path": request.path[len(prefix) :] or "/",
                        "query_string": request.query_string.encode(),
                        "headers": [
                            (k.lower().encode(), v.encode()) for k, v in request.headers.items()
                        ],
                    }
                    body = await request.read()
                    status_code = 200
                    resp_headers: list[tuple[str, str]] = []
                    resp_body = bytearray()

                    async def receive():
                        return {"type": "http.request", "body": body}

                    async def send(message):
                        nonlocal status_code, resp_headers
                        if message["type"] == "http.response.start":
                            status_code = message["status"]
                            resp_headers = [
                                (k.decode(), v.decode()) for k, v in message.get("headers", [])
                            ]
                        elif message["type"] == "http.response.body":
                            resp_body.extend(message.get("body", b""))

                    await asgi_app(scope, receive, send)
                    resp = web.Response(body=bytes(resp_body), status=status_code)
                    for k, v in resp_headers:
                        resp.headers[k] = v
                    return resp
                except Exception as exc:
                    _log(f"asgi error: {exc}")
                    return web.json_response({"error": str(exc)}, status=500)

            app.router.add_route("*", prefix + "/{path:.*}", handler)
            app.router.add_route("*", prefix, handler)
            _log(f"asgi mounted (fallback): {prefix}/* → {name}")

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
