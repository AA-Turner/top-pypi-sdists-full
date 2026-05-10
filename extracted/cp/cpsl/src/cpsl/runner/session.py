from __future__ import annotations

import asyncio
import json
import time
import uuid
from types import SimpleNamespace
from typing import Any

from aiohttp import web

from ..clients.capsule import (
    GetSessionRequest,
    GetUserIntegrationsRequest,
    InboundMessage,
    NotifySessionRequest,
    SaveSessionDataRequest,
)
from ..constants import (
    CollectionDecl,
    DEFAULT_CHANNEL_TYPE,
    HEADER_AUTHENTICATED,
    HEADER_EMAIL,
    HEADER_ORG_ID,
    HEADER_SESSION_ID,
    HEADER_USER_ID,
    HISTORY_FETCH_COUNT,
    KV_COLLECTION as _KV_COLLECTION,
)
from ..db import (
    Collection,
    CollectionManager,
    ScopedDatabaseProxy,
    reset_active_identity,
    set_active_identity,
)
from ..decorators import (
    _ENTER_ATTR,
    _MESSAGE_ATTR,
)
from ..home import HomeContext
from ..integration import IntegrationCredentials
from ..msg import Event, Message
from ..session import RequestContext, Session, SessionChannel, UserInfo, _track_data_value
from ..workflow import WorkflowInput
from .shared import (
    _HEARTBEAT_INTERVAL,
    _log,
    _maybe_await,
    _parse_integration_credential,
    _resolve_message_handler,
)


class RunnerSessionMixin:
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
                session.data = _track_data_value(
                    json.loads(resp.data_json), session._notify_data_changed
                )

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
        from ..app import _REGISTERED_CLASSES

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
            identity_parts = []
            if email:
                identity_parts.append(f"email={email}")
            if owner_id:
                identity_parts.append(f"owner_id={owner_id}")
            identity = " ".join(identity_parts)
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
        integrations = (
            await self._fetch_integrations(email=email, owner_id=owner_id)
            if email or owner_id
            else {}
        )

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
                integrations=(
                    await self._fetch_integrations(email=email, owner_id=owner_id)
                    if email or owner_id
                    else {}
                ),
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
        from ..app import _REGISTERED_CLASSES

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
            if item.initial_data_json and is_new:
                try:
                    initial_data = json.loads(item.initial_data_json)
                    if isinstance(initial_data, dict):
                        session.data.update(initial_data)
                except (json.JSONDecodeError, TypeError):
                    pass
            if item.chat_name:
                session.data.setdefault("__chat_name__", item.chat_name)

            if is_new and self._hooks.get(_ENTER_ATTR):
                await _maybe_await(self._hooks[_ENTER_ATTR](session))

            att_list = None
            if item.attachments:
                from ..msg import Attachment as MsgAttachment

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
                if item.action_name:
                    if item.action_name == "__session_init__":
                        payload = {}
                        if item.action_payload_json:
                            parsed = json.loads(item.action_payload_json)
                            if isinstance(parsed, dict):
                                payload = parsed
                        session_name = str(payload.get("name") or item.chat_name or "")
                        handler = self._session_handlers.get(session_name)
                        if handler:
                            await _maybe_await(handler(session))
                    else:
                        handler = self._action_handlers.get(item.action_name)
                        if handler is None:
                            available = ", ".join(sorted(self._action_handlers))
                            suffix = f" Available actions: {available}." if available else ""
                            raise RuntimeError(f"Unknown action {item.action_name!r}.{suffix}")
                        payload = {}
                        if item.action_payload_json:
                            parsed = json.loads(item.action_payload_json)
                            if isinstance(parsed, dict):
                                payload = parsed
                        await _maybe_await(
                            handler(session, Event(name=item.action_name, payload=payload))
                        )
                elif not await self._try_workflow_dispatch(
                    session, item.text, _reply, _stream, _block, _stream_write, rid, sid
                ):
                    chat_name = item.chat_name or session.data.get("__chat_name__", "")
                    handler = _resolve_message_handler(
                        self._message_handlers,
                        self._hooks.get(_MESSAGE_ATTR),
                        chat_name,
                    )
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
        self,
        session: Session,
        text: str,
        reply_cb,
        stream_cb,
        block_cb,
        stream_write_cb,
        rid: str,
        sid: str,
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
