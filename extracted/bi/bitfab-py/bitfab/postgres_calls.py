from __future__ import annotations

import contextlib
import functools
import importlib
import re
import sys
import threading
from collections.abc import Awaitable, Callable, Iterator, Mapping
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from bitfab.constants import _replay_context
from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta
from bitfab.postgres_sql import (
    PASSED_THROUGH_VERBS,
    is_read_verb,
    is_system_table,
    statement_table,
    statement_verb,
)
from bitfab.sandbox import (
    POSTGRES_SANDBOX_NAME,
    SANDBOX_SESSION_KEY,
    LiveSandbox,
    SandboxSession,
    SandboxStartCtx,
)
from bitfab.serialize import to_json_safe
from bitfab.warn_once import warn_once

NEON_BRANCH = "neon-branch"
POSTGRES_KEY_PREFIX = "postgres."
ROW_LIMIT = 200
PARAM_SETS_LIMIT = 200

_TRAILING_COUNT = re.compile(r"(\d+)\s*$")


@dataclass(frozen=True)
class _Statement:
    send: Callable[[], Any]
    view: Callable[[Any], Any]


@dataclass(frozen=True)
class _Planned:
    session: SandboxSession
    sql: str
    verb: str


@dataclass(frozen=True)
class _PlannedCall:
    planned: _Planned
    params: Any
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


_current: ContextVar[_Statement | None] = ContextVar(
    "bitfab_current_postgres_statement", default=None
)
_recording: ContextVar[bool] = ContextVar(
    "bitfab_recording_postgres_statement", default=False
)
_opening_statement_span: ContextVar[bool] = ContextVar(
    "bitfab_opening_postgres_statement_span", default=False
)
_traced: dict[tuple[int, str, bool], Any] = {}
_install_lock = threading.Lock()
_installed: set[str] = set()


def _verb_of_key(call: MockOverrideCtx) -> str:
    return call.node.trace_function_key[len(POSTGRES_KEY_PREFIX) :]


def _sql_of(call: MockOverrideCtx) -> str:
    sql = call.kwargs.get("sql")
    return sql if isinstance(sql, str) else ""


def _is_postgres_call(node: SpanNodeMeta) -> bool:
    return _opening_statement_span.get() and node.trace_function_key.startswith(
        POSTGRES_KEY_PREFIX
    )


def is_postgres_write(call: MockOverrideCtx) -> bool:
    return not is_read_verb(_verb_of_key(call))


def postgres_accessed_object(call: MockOverrideCtx) -> str | None:
    return statement_table(_sql_of(call))


def _add_sorted(names: list[str], name: str) -> None:
    if name not in names:
        names.append(name)
        names.sort()


def _handle(state: Any, call: MockOverrideCtx) -> None:
    table = statement_table(_sql_of(call))
    if table is None:
        return
    key = "tablesWritten" if is_postgres_write(call) else "tablesRead"
    _add_sorted(state[key], table)


def postgres_live_sandbox(lease: Mapping[str, Any]) -> LiveSandbox:
    def start(_ctx: SandboxStartCtx) -> dict[str, Any]:
        return {
            "neonBranchId": lease.get("neonBranchId"),
            "snapshotTimestamp": lease.get("snapshotTimestamp"),
            "tablesRead": [],
            "tablesWritten": [],
        }

    return LiveSandbox(
        name=POSTGRES_SANDBOX_NAME,
        match=_is_postgres_call,
        handle=_handle,
        start=start,
        mode=NEON_BRANCH,
        is_write=is_postgres_write,
        accessed_object=postgres_accessed_object,
    )


def _normal_host(host: str) -> str:
    return host.strip().lower().replace("-pooler", "")


def _lease_host(lease: Mapping[str, Any]) -> str | None:
    url = lease.get("databaseUrl")
    if not isinstance(url, str):
        return None
    return urlsplit(url).hostname


def _is_network_host(host: str | None) -> bool:
    return bool(host) and not str(host).startswith("/")


def _points_at_lease(
    host: str | None, lease: Mapping[str, Any], ctx: Mapping[str, Any]
) -> bool:
    expected = _lease_host(lease)
    if host is None or not _is_network_host(host) or not expected:
        return ctx.get("db_snapshot_accessed") is True
    if _normal_host(host) == _normal_host(expected):
        return True
    warn_once(
        f"postgres-sandbox-other-host:{host}",
        f"a Postgres statement during replay went to {host}, not the Postgres "
        "sandbox, so it was not recorded on the replay trace. Build the "
        "connection from postgres_sandbox_url() so it runs against the "
        "sandbox's copy of your database.",
    )
    return False


def _inside_trace() -> bool:
    from_client = sys.modules.get("bitfab.client")
    return from_client is not None and bool(from_client._get_span_stack())


def _render(query: Any, context: Any) -> str:
    if isinstance(query, str):
        return query
    if isinstance(query, (bytes, bytearray, memoryview)):
        return bytes(query).decode("utf-8", errors="replace")
    as_string = getattr(query, "as_string", None)
    if callable(as_string):
        try:
            rendered = as_string(context)
            if isinstance(rendered, bytes):
                return rendered.decode("utf-8", errors="replace")
            return str(rendered)
        except Exception:
            pass
    return str(query)


def _plan(
    query: Any, host_of: Callable[[], str | None], context: Any
) -> _Planned | None:
    ctx = _replay_context.get()
    if not ctx or _recording.get():
        return None
    lease = ctx.get("db_branch_lease")
    if not lease:
        return None
    try:
        session = ctx.get(SANDBOX_SESSION_KEY)
        if not isinstance(session, SandboxSession) or session.client is None:
            return None
        if session.find_named(POSTGRES_SANDBOX_NAME) is None or not _inside_trace():
            return None
        sql = _render(query, context)
        verb = statement_verb(sql)
        if not verb or verb in PASSED_THROUGH_VERBS:
            return None
        if is_system_table(statement_table(sql)):
            return None
        if not _points_at_lease(_safe_host(host_of), lease, ctx):
            return None
        return _Planned(session=session, sql=sql, verb=verb)
    except Exception:
        return None


def _safe_host(host_of: Callable[[], str | None]) -> str | None:
    try:
        host = host_of()
    except Exception:
        return None
    if isinstance(host, (tuple, list)) and host:
        host = host[0]
    return host if isinstance(host, str) else None


def _view_current(result: Any) -> Any:
    statement = _current.get()
    if statement is None:
        return None
    return statement.view(result)


def _send_current() -> Any:
    statement = _current.get()
    if statement is None:
        raise RuntimeError("Bitfab could not find the Postgres statement to run.")
    return statement.send()


@contextlib.contextmanager
def _statement_scope(
    send: Callable[[], Any], view: Callable[[Any], Any]
) -> Iterator[None]:
    tokens = (
        _current.set(_Statement(send, view)),
        _recording.set(True),
        _opening_statement_span.set(True),
    )
    try:
        yield
    finally:
        _opening_statement_span.reset(tokens[2])
        _recording.reset(tokens[1])
        _current.reset(tokens[0])


@contextlib.contextmanager
def _driver_scope() -> Iterator[None]:
    token = _opening_statement_span.set(False)
    try:
        yield
    finally:
        _opening_statement_span.reset(token)


def _traced_runner(client: Any, verb: str, is_async: bool) -> Any:
    key = (id(client), verb, is_async)
    traced = _traced.get(key)
    if traced is not None:
        return traced
    name = f"{POSTGRES_KEY_PREFIX}{verb}"
    runner: Callable[..., Any]
    if is_async:

        async def send_async(**_inputs: Any) -> Any:
            with _driver_scope():
                return await _send_current()

        runner = send_async
    else:

        def send(**_inputs: Any) -> Any:
            with _driver_scope():
                return _send_current()

        runner = send
    runner.__name__ = name.replace(".", "_")
    runner.__qualname__ = runner.__name__
    traced = client.get_function(name).span(
        name=name, type="function", finalize=_view_current
    )(runner)
    _traced[key] = traced
    return traced


def _inputs(sql: str, params: Any, many: bool) -> dict[str, Any]:
    if not many:
        return {"sql": sql, "params": None if params is None else to_json_safe(params)}
    sets = list(params or [])
    inputs: dict[str, Any] = {
        "sql": sql,
        "params": to_json_safe(sets[:PARAM_SETS_LIMIT]),
    }
    if len(sets) > PARAM_SETS_LIMIT:
        inputs["paramsOmitted"] = len(sets) - PARAM_SETS_LIMIT
    return inputs


def _run(
    planned: _Planned,
    params: Any,
    many: bool,
    send: Callable[[], Any],
    view: Callable[[Any], Any],
) -> Any:
    traced = _traced_runner(planned.session.client, planned.verb, False)
    with _statement_scope(send, view):
        return traced(**_inputs(planned.sql, params, many))


async def _run_async(
    planned: _Planned,
    params: Any,
    many: bool,
    send: Callable[[], Awaitable[Any]],
    view: Callable[[Any], Any],
) -> Any:
    traced = _traced_runner(planned.session.client, planned.verb, True)
    with _statement_scope(send, view):
        return await traced(**_inputs(planned.sql, params, many))


def _row_count(value: Any) -> int | None:
    return value if isinstance(value, int) and value >= 0 else None


def _status_count(status: Any) -> int | None:
    found = _TRAILING_COUNT.search(status) if isinstance(status, str) else None
    return int(found.group(1)) if found else None


def _json_row(row: Any) -> Any:
    if isinstance(row, Mapping):
        return to_json_safe(dict(row))
    items = getattr(row, "items", None)
    if callable(items) and not isinstance(row, (tuple, list)):
        try:
            return to_json_safe(dict(items()))
        except Exception:
            pass
    return to_json_safe(row)


def _output(
    command: str,
    row_count: int | None,
    rows: list[Any] | None = None,
    total: int | None = None,
) -> dict[str, Any]:
    output: dict[str, Any] = {"command": command, "rowCount": row_count}
    if rows is None:
        return output
    kept = rows[:ROW_LIMIT]
    output["rows"] = [_json_row(row) for row in kept]
    omitted = (len(rows) if total is None else total) - len(kept)
    if omitted > 0:
        output["rowsOmitted"] = omitted
    return output


def _command(cursor: Any, verb: str) -> str:
    status = getattr(cursor, "statusmessage", None)
    return status if isinstance(status, str) and status else verb.upper()


def _held_row_total(cursor: Any) -> int | None:
    pgresult = getattr(cursor, "pgresult", None)
    tuples = getattr(pgresult, "ntuples", None)
    if isinstance(tuples, int):
        return tuples
    return _row_count(getattr(cursor, "rowcount", None))


def _cursor_output(
    cursor: Any,
    verb: str,
    row_count: int | None,
    peeked: tuple[list[Any] | None, int | None],
) -> dict[str, Any]:
    rows, total = peeked
    return _output(_command(cursor, verb), row_count, rows, total)


def _cursor_view(cursor: Any, verb: str, read_rows: bool) -> Callable[[Any], Any]:
    def view(_result: Any) -> dict[str, Any]:
        row_count = _row_count(getattr(cursor, "rowcount", None))
        peeked = _peek_rows(cursor) if read_rows else (None, None)
        return _cursor_output(cursor, verb, row_count, peeked)

    return view


def _async_cursor_view(
    cursor: Any, verb: str, read_rows: bool
) -> Callable[[Any], Awaitable[Any]]:
    async def view(_result: Any) -> dict[str, Any]:
        row_count = _row_count(getattr(cursor, "rowcount", None))
        peeked = await _peek_rows_async(cursor) if read_rows else (None, None)
        return _cursor_output(cursor, verb, row_count, peeked)

    return view


_NOT_PEEKED: tuple[None, None] = (None, None)


def _peek_start(cursor: Any) -> tuple[int, int] | None:
    if getattr(cursor, "description", None) is None:
        return None
    position = getattr(cursor, "rownumber", None)
    total = _held_row_total(cursor)
    if not isinstance(position, int) or total is None:
        return None
    return position, total


def _peeked(
    rows: list[Any] | None, position: int, total: int
) -> tuple[list[Any] | None, int | None]:
    return _NOT_PEEKED if rows is None else (rows, total - position)


def _peek_rows(cursor: Any) -> tuple[list[Any] | None, int | None]:
    start = _peek_start(cursor)
    if start is None:
        return _NOT_PEEKED
    position, total = start
    if position >= total:
        return [], 0
    try:
        cursor.scroll(position, mode="absolute")
    except Exception:
        return _NOT_PEEKED
    rows: list[Any] | None
    try:
        rows = list(cursor.fetchmany(ROW_LIMIT))
    except Exception:
        rows = None
    try:
        cursor.scroll(position, mode="absolute")
    except Exception:
        return _NOT_PEEKED
    return _peeked(rows, position, total)


async def _peek_rows_async(cursor: Any) -> tuple[list[Any] | None, int | None]:
    start = _peek_start(cursor)
    if start is None:
        return _NOT_PEEKED
    position, total = start
    if position >= total:
        return [], 0
    try:
        await cursor.scroll(position, mode="absolute")
    except Exception:
        return _NOT_PEEKED
    rows: list[Any] | None
    try:
        rows = list(await cursor.fetchmany(ROW_LIMIT))
    except Exception:
        rows = None
    try:
        await cursor.scroll(position, mode="absolute")
    except Exception:
        return _NOT_PEEKED
    return _peeked(rows, position, total)


def _query_and_params(
    args: tuple[Any, ...], kwargs: dict[str, Any], query_name: str, params_name: str
) -> tuple[Any, Any]:
    query = args[0] if args else kwargs.get(query_name)
    params = args[1] if len(args) > 1 else kwargs.get(params_name)
    return query, params


def _listed_param_sets(
    args: tuple[Any, ...], kwargs: dict[str, Any], params_name: str, at: int
) -> tuple[list[Any], tuple[Any, ...], dict[str, Any]]:
    if len(args) > at:
        sets = list(args[at] or [])
        return sets, (*args[:at], sets, *args[at + 1 :]), kwargs
    sets = list(kwargs.get(params_name) or [])
    if params_name in kwargs:
        kwargs = {**kwargs, params_name: sets}
    return sets, args, kwargs


def _connection_host(connection: Any) -> str | None:
    info = getattr(connection, "info", None)
    host = getattr(info, "host", None)
    if isinstance(host, str):
        return host
    parameters = getattr(connection, "get_dsn_parameters", None)
    if callable(parameters):
        found = parameters().get("host")
        return found if isinstance(found, str) else None
    return None


def _psycopg_plan(
    cursor: Any, args: tuple[Any, ...], kwargs: dict[str, Any], many: bool
) -> _PlannedCall | None:
    if _is_server_cursor(cursor):
        return None
    params_name = "params_seq" if many else "params"
    query, params = _query_and_params(args, kwargs, "query", params_name)
    planned = _plan(query, lambda: _connection_host(cursor.connection), cursor)
    if planned is None:
        return None
    if many:
        params, args, kwargs = _listed_param_sets(args, kwargs, params_name, 1)
    return _PlannedCall(planned, params, args, kwargs)


def _psycopg_execute(original: Callable[..., Any], many: bool) -> Callable[..., Any]:
    @functools.wraps(original)
    def execute(self: Any, *args: Any, **kwargs: Any) -> Any:
        call = _psycopg_plan(self, args, kwargs, many)
        if call is None:
            return original(self, *args, **kwargs)
        return _run(
            call.planned,
            call.params,
            many,
            lambda: original(self, *call.args, **call.kwargs),
            _cursor_view(self, call.planned.verb, not many),
        )

    execute._bitfab_postgres = True  # type: ignore[attr-defined]
    return execute


def _psycopg_execute_async(
    original: Callable[..., Any], many: bool
) -> Callable[..., Any]:
    @functools.wraps(original)
    async def execute(self: Any, *args: Any, **kwargs: Any) -> Any:
        call = _psycopg_plan(self, args, kwargs, many)
        if call is None:
            return await original(self, *args, **kwargs)
        return await _run_async(
            call.planned,
            call.params,
            many,
            lambda: original(self, *call.args, **call.kwargs),
            _async_cursor_view(self, call.planned.verb, not many),
        )

    execute._bitfab_postgres = True  # type: ignore[attr-defined]
    return execute


_server_cursor_classes: tuple[type, ...] = ()


def _is_server_cursor(cursor: Any) -> bool:
    return bool(_server_cursor_classes) and isinstance(cursor, _server_cursor_classes)


def _patch(owner: Any, name: str, build: Callable[[Callable[..., Any]], Any]) -> None:
    original = getattr(owner, name, None)
    if original is None or getattr(original, "_bitfab_postgres", False):
        return
    setattr(owner, name, build(original))


def _install_psycopg() -> None:
    global _server_cursor_classes
    psycopg = importlib.import_module("psycopg")
    _server_cursor_classes = (psycopg.ServerCursor, psycopg.AsyncServerCursor)
    _patch(psycopg.Cursor, "execute", lambda o: _psycopg_execute(o, False))
    _patch(psycopg.Cursor, "executemany", lambda o: _psycopg_execute(o, True))
    _patch(psycopg.AsyncCursor, "execute", lambda o: _psycopg_execute_async(o, False))
    _patch(
        psycopg.AsyncCursor, "executemany", lambda o: _psycopg_execute_async(o, True)
    )


class _Psycopg2RecordingCursor:
    def execute(self, query: Any, vars: Any = None) -> Any:
        planned = _plan(query, lambda: _connection_host(self.connection), self)  # type: ignore[attr-defined]
        if planned is None:
            return super().execute(query, vars)  # type: ignore[misc]
        return _run(
            planned,
            vars,
            False,
            lambda: super(_Psycopg2RecordingCursor, self).execute(query, vars),  # type: ignore[misc]
            _cursor_view(self, planned.verb, True),
        )

    def executemany(self, query: Any, vars_list: Any) -> Any:
        planned = _plan(query, lambda: _connection_host(self.connection), self)  # type: ignore[attr-defined]
        if planned is None:
            return super().executemany(query, vars_list)  # type: ignore[misc]
        sets = list(vars_list)
        return _run(
            planned,
            sets,
            True,
            lambda: super(_Psycopg2RecordingCursor, self).executemany(query, sets),  # type: ignore[misc]
            _cursor_view(self, planned.verb, False),
        )


_PSYCOPG2_CURSOR_PARAMETERS = ("name", "cursor_factory", "withhold", "scrollable")


class _Psycopg2RecordingConnection:
    def cursor(self, *args: Any, **kwargs: Any) -> Any:
        parent = super()
        recording = _recording_cursor_arguments(self, args, kwargs)
        if recording is not None:
            try:
                return parent.cursor(**recording)  # type: ignore[attr-defined]
            except Exception:
                pass
        return parent.cursor(*args, **kwargs)  # type: ignore[attr-defined]


def _recording_cursor_arguments(
    connection: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> dict[str, Any] | None:
    try:
        if len(args) > len(_PSYCOPG2_CURSOR_PARAMETERS):
            return None
        chosen = dict(zip(_PSYCOPG2_CURSOR_PARAMETERS, args))
        if any(
            key in chosen or key not in _PSYCOPG2_CURSOR_PARAMETERS for key in kwargs
        ):
            return None
        chosen.update(kwargs)
        if chosen.get("name") is not None:
            return None
        factory = (
            chosen.get("cursor_factory")
            or getattr(connection, "cursor_factory", None)
            or _psycopg2_base_cursor()
        )
        recording = _safe_recording_cursor(factory)
        if recording is None:
            return None
        return {**chosen, "cursor_factory": recording}
    except Exception:
        return None


def _safe_recording_cursor(chosen: Any) -> type | None:
    if not isinstance(chosen, type):
        return None
    try:
        return _recording_class(chosen, _Psycopg2RecordingCursor)
    except Exception:
        return None


_recording_classes: dict[tuple[type, type], type] = {}


def _recording_class(base: type, mixin: type) -> type:
    if issubclass(base, mixin):
        return base
    found = _recording_classes.get((base, mixin))
    if found is None:
        found = type(base.__name__, (mixin, base), {"__module__": base.__module__})
        _recording_classes[(base, mixin)] = found
    return found


_recording_connection_classes: dict[type, type] = {}


def _recording_connection_class(base: type, driver_connection: type) -> type:
    leaf = _recording_class(driver_connection, _Psycopg2RecordingConnection)
    if issubclass(base, _Psycopg2RecordingConnection):
        return base
    if base is driver_connection:
        return leaf
    found = _recording_connection_classes.get(base)
    if found is None:
        found = type(base.__name__, (base, leaf), {"__module__": base.__module__})
        _recording_connection_classes[base] = found
    return found


def _psycopg2_base_cursor() -> type:
    return importlib.import_module("psycopg2.extensions").cursor  # type: ignore[no-any-return]


def _install_psycopg2() -> None:
    psycopg2 = importlib.import_module("psycopg2")
    extensions = importlib.import_module("psycopg2.extensions")
    original = psycopg2.connect
    if getattr(original, "_bitfab_postgres", False):
        return

    @functools.wraps(original)
    def connect(
        dsn: Any = None,
        connection_factory: Any = None,
        cursor_factory: Any = None,
        **kwargs: Any,
    ) -> Any:
        factory = connection_factory
        chosen = connection_factory or extensions.connection
        if isinstance(chosen, type) and issubclass(chosen, extensions.connection):
            try:
                factory = _recording_connection_class(chosen, extensions.connection)
            except Exception:
                factory = connection_factory
        return original(
            dsn,
            connection_factory=factory,
            cursor_factory=cursor_factory,
            **kwargs,
        )

    connect._bitfab_postgres = True  # type: ignore[attr-defined]
    psycopg2.connect = connect


def _asyncpg_host(connection: Any) -> Any:
    return getattr(connection, "_addr", None)


def _asyncpg_fetch_view(verb: str) -> Callable[[Any], Any]:
    def view(rows: Any) -> dict[str, Any]:
        found = list(rows or [])
        return _output(verb.upper(), len(found), found)

    return view


def _asyncpg_fetchrow_view(verb: str) -> Callable[[Any], Any]:
    def view(row: Any) -> dict[str, Any]:
        found = [] if row is None else [row]
        return _output(verb.upper(), len(found), found)

    return view


def _asyncpg_fetchval_view(verb: str) -> Callable[[Any], Any]:
    def view(value: Any) -> dict[str, Any]:
        return _output(verb.upper(), None, [[value]])

    return view


def _asyncpg_execute_view(verb: str) -> Callable[[Any], Any]:
    def view(status: Any) -> dict[str, Any]:
        command = status if isinstance(status, str) and status else verb.upper()
        return _output(command, _status_count(status))

    return view


def _asyncpg_many_view(verb: str) -> Callable[[Any], Any]:
    def view(_result: Any) -> dict[str, Any]:
        return _output(verb.upper(), None)

    return view


_ASYNCPG_VIEWS: dict[str, Callable[[str], Callable[[Any], Any]]] = {
    "execute": _asyncpg_execute_view,
    "executemany": _asyncpg_many_view,
    "fetch": _asyncpg_fetch_view,
    "fetchmany": _asyncpg_fetch_view,
    "fetchrow": _asyncpg_fetchrow_view,
    "fetchval": _asyncpg_fetchval_view,
}
_ASYNCPG_MANY = frozenset({"executemany", "fetchmany"})


def _asyncpg_connection_query(
    _connection: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> Any:
    return args[0] if args else kwargs.get("query", kwargs.get("command"))


def _asyncpg_statement_query(
    statement: Any, _args: tuple[Any, ...], _kwargs: dict[str, Any]
) -> Any:
    return statement.get_query()


def _asyncpg_plain_view(
    _connection: Any, view: Callable[[Any], dict[str, Any]]
) -> Callable[[Any], Any]:
    return view


def _statement_status_view(
    statement: Any, view: Callable[[Any], dict[str, Any]]
) -> Callable[[Any], Any]:
    def with_status(result: Any) -> dict[str, Any]:
        output = view(result)
        status = statement.get_statusmsg()
        if isinstance(status, str) and status:
            output["command"] = status
            if output.get("rowCount") is None:
                output["rowCount"] = _status_count(status)
        return output

    return with_status


@dataclass(frozen=True)
class _AsyncpgTarget:
    query_of: Callable[[Any, tuple[Any, ...], dict[str, Any]], Any]
    connection_of: Callable[[Any], Any]
    params_at: int
    wrap_view: Callable[[Any, Callable[[Any], dict[str, Any]]], Callable[[Any], Any]]


_ASYNCPG_CONNECTION = _AsyncpgTarget(
    query_of=_asyncpg_connection_query,
    connection_of=lambda connection: connection,
    params_at=1,
    wrap_view=_asyncpg_plain_view,
)
_ASYNCPG_STATEMENT = _AsyncpgTarget(
    query_of=_asyncpg_statement_query,
    connection_of=lambda statement: statement._connection,
    params_at=0,
    wrap_view=_statement_status_view,
)


def _asyncpg_method(
    original: Callable[..., Any], method: str, target: _AsyncpgTarget
) -> Callable[..., Any]:
    many = method in _ASYNCPG_MANY

    @functools.wraps(original)
    async def run(self: Any, *args: Any, **kwargs: Any) -> Any:
        planned = _plan(
            target.query_of(self, args, kwargs),
            lambda: _asyncpg_host(target.connection_of(self)),
            None,
        )
        if planned is None:
            return await original(self, *args, **kwargs)
        params: Any = list(args[target.params_at :]) or None
        if many:
            params, args, kwargs = _listed_param_sets(
                args, kwargs, "args", target.params_at
            )
        return await _run_async(
            planned,
            params,
            many,
            lambda: original(self, *args, **kwargs),
            target.wrap_view(self, _ASYNCPG_VIEWS[method](planned.verb)),
        )

    run._bitfab_postgres = True  # type: ignore[attr-defined]
    return run


def _install_asyncpg() -> None:
    connection = importlib.import_module("asyncpg.connection").Connection
    statement = importlib.import_module("asyncpg.prepared_stmt").PreparedStatement
    for method in (
        "execute",
        "executemany",
        "fetch",
        "fetchmany",
        "fetchrow",
        "fetchval",
    ):
        _patch(
            connection,
            method,
            lambda o, m=method: _asyncpg_method(o, m, _ASYNCPG_CONNECTION),
        )
    for method in ("executemany", "fetch", "fetchmany", "fetchrow", "fetchval"):
        _patch(
            statement,
            method,
            lambda o, m=method: _asyncpg_method(o, m, _ASYNCPG_STATEMENT),
        )


_DRIVERS: dict[str, Callable[[], None]] = {
    "psycopg": _install_psycopg,
    "psycopg2": _install_psycopg2,
    "asyncpg": _install_asyncpg,
}


def install() -> None:
    with _install_lock:
        for driver, patch_driver in _DRIVERS.items():
            if driver in _installed:
                continue
            try:
                patch_driver()
            except ImportError:
                continue
            except Exception as error:
                warn_once(
                    f"postgres-sandbox-install:{driver}",
                    f"Bitfab could not record {driver} statements during replay "
                    f"({type(error).__name__}: {error}); they still run.",
                )
            _installed.add(driver)
