from __future__ import annotations

import concurrent.futures
import textwrap
import traceback
from dataclasses import dataclass


@dataclass
class DevtoolsQueryResult:
    success: bool
    value: str | None = None
    error: str | None = None


# Backwards-compat alias
NetworkQueryResult = DevtoolsQueryResult


import multiprocessing as _mp
try:
    _ctx = _mp.get_context("forkserver")
except ValueError:
    _ctx = _mp.get_context("spawn")
_executor = concurrent.futures.ProcessPoolExecutor(max_workers=1, mp_context=_ctx)

import atexit as _atexit
_atexit.register(lambda: _executor.shutdown(wait=False, cancel_futures=True))


class _ReadOnlyNetworkLog:
    """Lightweight query-only wrapper over a list of NetworkEntry objects.
    Lives inside testmu — self-contained, no external dependency."""

    def __init__(self, entries: list) -> None:
        self._entries = entries
        self._by_domain: dict[str, list[int]] = {}
        self._by_route: dict[tuple[str, str, str], list[int]] = {}
        for idx, entry in enumerate(entries):
            self._by_domain.setdefault(entry.domain, []).append(idx)
            route_key = (entry.domain, entry.method, entry.path)
            self._by_route.setdefault(route_key, []).append(idx)

    def requests(
        self,
        *,
        domain: str | None = None,
        method: str | None = None,
        path: str | None = None,
        path_glob: str | None = None,
        status: int | range | None = None,
        resource_type: str | None = None,
        after: float | None = None,
        before: float | None = None,
    ) -> list:
        import fnmatch

        if domain and method and path:
            indices = self._by_route.get((domain, method, path), [])
            candidates = [self._entries[i] for i in indices]
        elif domain:
            indices = self._by_domain.get(domain, [])
            candidates = [self._entries[i] for i in indices]
        else:
            candidates = list(self._entries)

        result = []
        for e in candidates:
            if method and e.method != method:
                continue
            if path and e.path != path:
                continue
            if path_glob and not fnmatch.fnmatch(e.path, path_glob):
                continue
            if status is not None:
                if isinstance(status, range):
                    if e.response_status is None or e.response_status not in status:
                        continue
                elif e.response_status != status:
                    continue
            if resource_type and e.resource_type != resource_type:
                continue
            if after and e.timing and e.timing.start_ms < after:
                continue
            if before and e.timing and e.timing.start_ms > before:
                continue
            result.append(e)
        return result

    def domains(self) -> list[str]:
        return list(self._by_domain.keys())

    def routes(self) -> list[tuple[str, str, str]]:
        return list(self._by_route.keys())


class _ReadOnlyWebSocketLog:
    """Query-only wrapper over captured WebSocketConnection objects — the
    `websocket` object exposed inside devtools_network_query. Light filters only;
    the extraction code does the rest. Mirror of _ReadOnlyNetworkLog."""

    def __init__(self, connections: list) -> None:
        self._connections = connections

    def connections(
        self,
        *,
        url: str | None = None,
        url_glob: str | None = None,
    ) -> list:
        import fnmatch

        result = []
        for c in self._connections:
            if url and c.url != url:
                continue
            if url_glob and not fnmatch.fnmatch(c.url, url_glob):
                continue
            result.append(c)
        return result

    def frames(
        self,
        *,
        url: str | None = None,
        url_glob: str | None = None,
        direction: str | None = None,
        include_binary: bool = False,
    ) -> list:
        """Frames across all matching connections, merged and sorted by the
        global monotonic `seq`. Binary frames are excluded unless include_binary."""
        import fnmatch

        frames = []
        for c in self._connections:
            if url and c.url != url:
                continue
            if url_glob and not fnmatch.fnmatch(c.url, url_glob):
                continue
            for f in c.frames:
                if direction and f.direction != direction:
                    continue
                if f.is_binary and not include_binary:
                    continue
                frames.append(f)
        frames.sort(key=lambda f: f.seq)
        return frames


class _ReadOnlySSELog:
    """Query-only wrapper over captured SSEConnection objects — the `sse` object
    exposed inside devtools_network_query. Light filters only; the extraction
    code does the rest. Mirror of _ReadOnlyWebSocketLog."""

    def __init__(self, connections: list) -> None:
        self._connections = connections

    def connections(
        self,
        *,
        url: str | None = None,
        url_glob: str | None = None,
    ) -> list:
        import fnmatch

        result = []
        for c in self._connections:
            if url and c.url != url:
                continue
            if url_glob and not fnmatch.fnmatch(c.url, url_glob):
                continue
            result.append(c)
        return result

    def messages(
        self,
        *,
        url: str | None = None,
        url_glob: str | None = None,
        event: str | None = None,
    ) -> list:
        """Messages across all matching connections, merged and sorted by the
        global monotonic `seq`. `event` filters on the SSE event-type."""
        import fnmatch

        msgs = []
        for c in self._connections:
            if url and c.url != url:
                continue
            if url_glob and not fnmatch.fnmatch(c.url, url_glob):
                continue
            for m in c.messages:
                if event is not None and m.event != event:
                    continue
                msgs.append(m)
        msgs.sort(key=lambda m: m.seq)
        return msgs


def _run_in_worker(
    code: str,
    entries: list,
    ws_connections: list | None = None,
    sse_connections: list | None = None,
) -> tuple[str, str]:
    """Runs in a pre-spawned worker process — fully isolated."""
    import json
    import math
    import re

    log = _ReadOnlyNetworkLog(entries)

    wrapped = textwrap.dedent(f"""\
def __extract__():
{textwrap.indent(code, '    ')}

__result__ = __extract__()
""")
    try:
        # Restrict builtins: only allow safe built-in names; block __import__
        import builtins as _builtins
        _allowed_builtins = {
            name: getattr(_builtins, name)
            for name in (
                "None", "True", "False",
                "abs", "all", "any", "bool", "bytes", "chr", "dict", "dir",
                "divmod", "enumerate", "filter", "float", "format", "frozenset",
                "getattr", "hasattr", "hash", "hex", "int", "isinstance",
                "issubclass", "iter", "len", "list", "map", "max", "min",
                "next", "oct", "ord", "pow", "print", "range", "repr",
                "reversed", "round", "set", "slice", "sorted", "str", "sum",
                "tuple", "type", "vars", "zip",
                "ArithmeticError", "AssertionError", "AttributeError",
                "EOFError", "Exception", "FileNotFoundError", "FloatingPointError",
                "IOError", "ImportError", "IndexError", "KeyError", "LookupError",
                "MemoryError", "ModuleNotFoundError", "NameError", "NotImplemented",
                "NotImplementedError", "OSError", "OverflowError", "RecursionError",
                "RuntimeError", "StopIteration", "SyntaxError", "TypeError",
                "UnicodeDecodeError", "UnicodeEncodeError", "UnicodeError",
                "ValueError", "ZeroDivisionError",
            )
            if hasattr(_builtins, name)
        }
        ns: dict = {
            "__builtins__": _allowed_builtins,
            "json": json,
            "re": re,
            "math": math,
            "network": log,
        }
        # Expose `websocket` only when WS was captured. On the network-only path
        # the key stays absent (not None), so a bare `websocket` reference raises
        # NameError exactly as before.
        if ws_connections is not None:
            ns["websocket"] = _ReadOnlyWebSocketLog(ws_connections)
        # Expose `sse` only when SSE was captured — same absent-not-None rule.
        # Independent of `websocket`: a query can read either, both, or neither.
        if sse_connections is not None:
            ns["sse"] = _ReadOnlySSELog(sse_connections)
        exec(compile(wrapped, "<devtools-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_network_query(
    code: str,
    network_log: object,
    ws_log: object | None = None,
    timeout_sec: float = 2.0,
    sse_log: object | None = None,
) -> DevtoolsQueryResult:
    """Execute extraction code in an isolated worker process.

    When `ws_log` is provided, the worker also exposes a `websocket` object
    (`.frames(...)`/`.connections(...)`) alongside `network`, so one query can read
    HTTP (network.requests) and WebSocket frames. When `sse_log` is provided, an
    `sse` object (`.messages(...)`/`.connections(...)`) is also exposed. The two
    are independent — a query can read network only, +ws, +sse, or all three.
    Default None ⇒ that surface is absent (a bare reference raises NameError)."""
    entries = list(network_log._entries)
    ws_connections = list(ws_log._connections) if ws_log is not None else None
    sse_connections = list(sse_log._connections) if sse_log is not None else None

    try:
        future = _executor.submit(_run_in_worker, code, entries, ws_connections, sse_connections)
        tag, val = future.result(timeout=timeout_sec)
    except concurrent.futures.TimeoutError:
        _replace_executor()
        return DevtoolsQueryResult(success=False, error="Execution timeout: code exceeded time limit")
    except concurrent.futures.BrokenExecutor:
        _replace_executor()
        return DevtoolsQueryResult(success=False, error="Executor crashed — replaced")
    except Exception as exc:
        return DevtoolsQueryResult(success=False, error=str(exc))

    if tag == "ok":
        return DevtoolsQueryResult(success=True, value=val)
    return DevtoolsQueryResult(success=False, error=val)


def _replace_executor() -> None:
    """Kill stuck workers and create a fresh pool."""
    global _executor
    # CPython implementation detail: _processes is not public API but stable 3.7-3.13
    for pid, proc in list(_executor._processes.items()):
        proc.terminate()
    _executor.shutdown(wait=False, cancel_futures=True)
    _executor = concurrent.futures.ProcessPoolExecutor(max_workers=1, mp_context=_ctx)


def shutdown_executor() -> None:
    """Terminate the worker pool. Registered via atexit at import time."""
    _executor.shutdown(wait=False, cancel_futures=True)
