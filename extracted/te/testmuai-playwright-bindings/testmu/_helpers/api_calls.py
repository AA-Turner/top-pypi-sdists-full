"""Query sandbox for agent-executed API calls.

Mirror of devtools_network.py: LLM-generated extraction code runs in a
pre-spawned single-worker process pool against a read-only view of the
api_calls log, with the same restricted-builtins namespace. The sandbox
object is `api_calls` (vs `network` for devtools).
"""

from __future__ import annotations

import concurrent.futures
import textwrap
import traceback

from testmu._helpers.devtools_network import DevtoolsQueryResult, _ctx

_executor = concurrent.futures.ProcessPoolExecutor(max_workers=1, mp_context=_ctx)

import atexit as _atexit
_atexit.register(lambda: _executor.shutdown(wait=False, cancel_futures=True))


class _ReadOnlyApiCalls:
    """Query-only wrapper over a list of ApiCallEntry objects."""

    def __init__(self, entries: list) -> None:
        self._entries = list(entries)

    def all(self) -> list:
        return list(self._entries)

    def requests(
        self,
        *,
        method: str | None = None,
        url_contains: str | None = None,
        status: int | range | None = None,
    ) -> list:
        result = []
        for e in self._entries:
            req = e.request or {}
            resp = e.response or {}
            if method and str(req.get("method", "")).upper() != method.upper():
                continue
            if url_contains and url_contains not in str(req.get("url", "")):
                continue
            if status is not None:
                st = resp.get("status")
                if isinstance(status, range):
                    if st is None or st not in status:
                        continue
                elif st != status:
                    continue
            result.append(e)
        return result

    def last(self, **filters):
        matches = self.requests(**filters)
        return matches[-1] if matches else None


def _run_in_worker(code: str, entries: list) -> tuple[str, str]:
    """Runs in a pre-spawned worker process — fully isolated."""
    import json
    import math
    import re

    calls = _ReadOnlyApiCalls(entries)

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
            "api_calls": calls,
        }
        exec(compile(wrapped, "<api-calls-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def _api_calls_query(
    code: str,
    entries: list,
    timeout_sec: float = 2.0,
) -> DevtoolsQueryResult:
    """Raw sandbox executor — runs extraction code against a list of entries.

    Private; same signature shape as devtools_network_query(code, log). The
    public single-arg async wrapper ``api_calls_query`` (below) is what
    generated test code calls.
    """
    try:
        future = _executor.submit(_run_in_worker, code, list(entries))
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


async def api_calls_query(code: str) -> str:
    """Single-arg async wrapper called by generated test code as
    ``testmu.api_calls_query(<code>)``.

    Mirrors ``devtoolsNetworkQuery``: injects the live api-call log and returns
    the extracted string ("" on failure) — not a ``DevtoolsQueryResult`` — so
    the output variable receives the value.
    """
    from testmu._helpers.execute_api import get_api_call_log

    result = _api_calls_query(code, get_api_call_log())
    return result.value if result.success else ""


def _replace_executor() -> None:
    """Kill stuck workers and create a fresh pool."""
    global _executor
    # CPython implementation detail: _processes is not public API but stable 3.7-3.13
    for pid, proc in list(_executor._processes.items()):
        proc.terminate()
    _executor.shutdown(wait=False, cancel_futures=True)
    _executor = concurrent.futures.ProcessPoolExecutor(max_workers=1, mp_context=_ctx)
