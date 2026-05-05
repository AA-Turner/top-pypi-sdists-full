"""Subprocess task execution for ``process=True`` tasks.

Extracted from runner.py to keep that module focused on the gRPC
connection loop and message dispatch. Everything here is internal —
the public API lives in task_types.py (TaskDescriptor, TaskHandle).
"""

from __future__ import annotations

import asyncio
import importlib
import json
import multiprocessing
import multiprocessing.connection
import os
import time
import traceback
import uuid
from typing import Any, Type

from .clients.capsule import (
    DataServiceStub,
    GetSessionRequest,
    GetUserIntegrationsRequest,
    NotifySessionRequest,
    RunnerServiceStub,
    SaveSessionDataRequest,
    SessionServiceStub,
)
from .constants import DEFAULT_CHANNEL_TYPE, HISTORY_FETCH_COUNT, KV_COLLECTION
from .db import Collection, CollectionRef, DatabaseProxy, ScopedDatabaseProxy, reset_active_identity, set_active_identity
from .msg import Message
from .task_types import TaskDescriptor


def _retry_on_errors(retry_for: list[Type[Exception]], exc: BaseException) -> bool:
    """True when *exc* is an exact-type match for any entry in *retry_for*."""
    if not retry_for:
        return False
    return any(type(exc) is err for err in retry_for)


def _parse_integration_credential(ic: Any) -> Any:
    """Re-import helper to avoid circular dep on runner.py at module level."""
    from .integration import IntegrationCredentials, KNOWN_SECRET_INTEGRATIONS

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
        token_type=ic.token_type or "bearer",
        scopes=list(ic.scopes),
        expires_at=ic.expires_at,
        fields=secret_fields,
    )


# ---------------------------------------------------------------------------
# Child process entrypoint
# ---------------------------------------------------------------------------

def _subprocess_entry(
    module_path: str,
    target_name: str,
    task_name: str,
    session_id: str,
    kwargs_json: str,
    result_conn: multiprocessing.connection.Connection,
) -> None:
    """Child process entrypoint for ``process=True`` tasks.

    Runs in a fresh Python interpreter (``spawn`` context). Creates its own
    gRPC channel, re-imports the user module, hydrates the session from the
    gateway, and executes the task function. The result — ``("ok", None)``
    or ``("error", "<traceback>")`` — is sent back to the parent via *pipe*.
    """
    try:
        from .app import App
        from .channel import Channel as _GrpcChannel
        from .session import Session, SessionChannel, UserInfo

        gw = os.environ.get("CAPSULE_GATEWAY_HOST", "localhost:1980")
        token = os.environ.get("CAPSULE_RUNNER_TOKEN") or None
        version_type = os.environ.get("CAPSULE_VERSION_TYPE", "")
        env_type = os.environ.get("CAPSULE_ENV_TYPE", "")
        app_id = os.environ.get("CAPSULE_APP_ID", "")
        user_id = os.environ.get("CAPSULE_USER_ID", "")
        canonical_type = env_type or version_type

        extra_md = []
        if canonical_type:
            extra_md.append(("x-version-type", canonical_type))
        ch = _GrpcChannel(addr=gw, token=token, extra_metadata=extra_md or None)

        runner_stub = RunnerServiceStub(ch)
        session_stub = SessionServiceStub(ch)
        data_stub = DataServiceStub(ch)

        # Expose stubs to session methods (prompt_file, prompt_integration,
        # show_image) which locate them via Runner._instance_ref.
        from .runner import Runner
        _shim = object.__new__(Runner)
        _shim._runner_stub = runner_stub
        _shim._session_stub = session_stub
        _shim._app_id = app_id
        Runner._instance_ref = _shim

        data_app_id = f"{app_id}_dev" if canonical_type == "serve" else app_id

        mod = importlib.import_module(module_path)
        obj = getattr(mod, target_name)
        instance = None

        if isinstance(obj, App):
            obj._finalize_config()
            desc = getattr(obj, task_name, None)
        else:
            instance = obj()
            desc = None
            for name in dir(instance):
                attr = getattr(instance, name, None)
                if isinstance(attr, TaskDescriptor) and attr._name == task_name:
                    desc = attr
                    break

        if desc is None:
            result_conn.send(("error", f"task '{task_name}' not found on {target_name}"))
            return

        def _bind_collection_refs() -> None:
            if not data_stub:
                return
            from .app import _REGISTERED_CLASSES

            db = DatabaseProxy(data_stub, data_app_id)
            for reg in _REGISTERED_CLASSES:
                for ref in reg.get("collection_refs", []):
                    if isinstance(ref, CollectionRef):
                        ref._bound = getattr(db, ref.name)
            if isinstance(obj, App):
                obj._kv = Collection(data_stub, data_app_id, KV_COLLECTION)
            elif instance is not None:
                setattr(instance, "db", db)

        _bind_collection_refs()

        kwargs = json.loads(kwargs_json) if kwargs_json else {}

        def _bind_runtime_session(session: Session) -> Session:
            session._runner_stub = runner_stub
            session._session_stub = session_stub
            session._app_id = app_id
            if data_stub:
                session._db_proxy = ScopedDatabaseProxy(
                    data_stub,
                    data_app_id,
                    user_id=session.user.id,
                    owner_id=session.user.owner_id,
                    session_id=session.id,
                    collection_scopes={},
                )
            return session

        def _fetch_runtime_integrations(owner_id: str) -> dict[str, Any]:
            if not owner_id:
                return {}
            try:
                resp = session_stub.get_user_integrations(
                    GetUserIntegrationsRequest(
                        app_id=app_id,
                        owner_id=owner_id,
                        env=canonical_type,
                    )
                )
                return {
                    ic.type: _parse_integration_credential(ic)
                    for ic in resp.integrations
                }
            except Exception:
                return {}

        def _build_runtime_session() -> Session:
            owner_id = user_id
            return _bind_runtime_session(
                Session(
                    id="",
                    user=UserInfo(
                        id=owner_id,
                        email=None,
                        org_id=UserInfo.org_id_from_owner_id(owner_id),
                    ),
                    channel=SessionChannel(type=DEFAULT_CHANNEL_TYPE),
                    history=[],
                    data={},
                    integrations=_fetch_runtime_integrations(owner_id),
                )
            )

        async def _run() -> None:
            session = None
            runtime_session = None
            if session_id:
                session = Session(
                    id=session_id,
                    user=UserInfo(id=user_id, email=None),
                    channel=SessionChannel(type=DEFAULT_CHANNEL_TYPE),
                    history=[],
                    data={},
                )

                resp = session_stub.get_session(
                    GetSessionRequest(
                        session_id=session_id,
                        history_count=HISTORY_FETCH_COUNT,
                    )
                )
                if resp.user_id:
                    session.user = UserInfo(
                        id=resp.user_id,
                        email=resp.user_email or None,
                        org_id=resp.org_id or None,
                    )
                if resp.channel_type:
                    session.channel = SessionChannel(type=resp.channel_type)
                if resp.data_json:
                    from .session import _track_data_value
                    session.data = _track_data_value(json.loads(resp.data_json), session._notify_data_changed)

                raw = [
                    Message(text=e.text, sender=e.sender, channel_type=e.channel_type)
                    for e in resp.history
                ]
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
                session.history = history

                if resp.integrations:
                    session.integrations = {
                        ic.type: _parse_integration_credential(ic)
                        for ic in resp.integrations
                    }

                async def _task_reply(msg: Message) -> None:
                    rid = str(uuid.uuid4())
                    session_stub.notify_session(
                        NotifySessionRequest(
                            app_id=app_id,
                            session_id=session_id,
                            request_id=rid,
                            text=msg.text,
                            external_delivery=True,
                        )
                    )

                async def _task_block(block_json: str) -> None:
                    rid = str(uuid.uuid4())
                    session_stub.notify_session(
                        NotifySessionRequest(
                            app_id=app_id,
                            session_id=session_id,
                            request_id=rid,
                            block_json=block_json,
                            external_delivery=False,
                        )
                    )

                def _task_data_changed() -> None:
                    session_stub.save_session_data(
                        SaveSessionDataRequest(
                            session_id=session_id,
                            data_json=json.dumps(session.data),
                        )
                    )
                    rid = str(uuid.uuid4())
                    session_stub.notify_session(
                        NotifySessionRequest(
                            app_id=app_id,
                            session_id=session_id,
                            request_id=rid,
                            block_json=json.dumps({
                                "id": f"widget_update_{session_id}",
                                "type": "widget_update",
                                "payload": {"reason": "data", "session_id": session_id},
                            }),
                            external_delivery=False,
                        )
                    )

                session._reply_callback = _task_reply
                session._block_callback = _task_block
                session._data_change_callback = _task_data_changed
                _bind_runtime_session(session)
                runtime_session = session
            else:
                runtime_session = _build_runtime_session()
                if desc._wants_session:
                    session = runtime_session

            identity_token = set_active_identity(runtime_session) if runtime_session else None
            try:
                fn = desc._fn
                is_async = desc._is_async
                is_functional = desc._functional

                call_kwargs = dict(kwargs)
                if session is not None and desc._session_param_name:
                    call_kwargs.setdefault(desc._session_param_name, session)
                if is_functional:
                    result = fn(**call_kwargs)
                else:
                    inst = getattr(desc, "_instance", None) or instance
                    result = fn(inst, **call_kwargs)

                if is_async:
                    await result
            finally:
                if identity_token is not None:
                    reset_active_identity(identity_token)

            if session and session.id:
                session_stub.save_session_data(
                    SaveSessionDataRequest(
                        session_id=session.id,
                        data_json=json.dumps(session.data),
                    )
                )

        asyncio.run(_run())
        result_conn.send(("ok", None))

    except BaseException:
        result_conn.send(("error", traceback.format_exc()))
    finally:
        result_conn.close()


# ---------------------------------------------------------------------------
# Parent-side subprocess driver
# ---------------------------------------------------------------------------

async def run_task_subprocess(
    module_path: str,
    target_name: str,
    task_name: str,
    session_id: str,
    kwargs_json: str,
    timeout: int,
) -> tuple[str, str]:
    """Spawn the task in a child process and wait for it to finish.

    Returns ``(status, error_msg)`` where *status* is one of
    ``"ok"``, ``"error"``, ``"timeout"``, or ``"killed"``.
    """
    ctx = multiprocessing.get_context("spawn")
    parent_conn, child_conn = ctx.Pipe(duplex=False)

    proc = ctx.Process(
        target=_subprocess_entry,
        args=(module_path, target_name, task_name, session_id, kwargs_json, child_conn),
        daemon=True,
    )
    proc.start()
    child_conn.close()

    deadline = (time.time() + timeout) if timeout > 0 else None

    try:
        while proc.is_alive():
            if deadline and time.time() > deadline:
                proc.kill()
                proc.join(timeout=5)
                return "timeout", f"process killed after {timeout}s timeout"
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        if proc.is_alive():
            proc.kill()
            proc.join(timeout=5)
        parent_conn.close()
        raise

    proc.join(timeout=5)

    if parent_conn.poll(timeout=1):
        status, detail = parent_conn.recv()
    else:
        status, detail = "error", "no result from child process"
    parent_conn.close()

    exit_code = proc.exitcode
    if exit_code is not None and exit_code < 0:
        sig_num = -exit_code
        return "killed", f"process killed by signal {sig_num}"
    if exit_code is not None and exit_code != 0 and status == "ok":
        return "error", f"process exited with code {exit_code}"

    return status, detail or ""
