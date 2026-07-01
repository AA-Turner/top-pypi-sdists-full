from __future__ import annotations

import textwrap
import traceback

import testmu._helpers.devtools_network as _net
import concurrent.futures
from testmu._helpers.devtools_network import DevtoolsQueryResult


class _ReadOnlyStorage:
    """Query-only wrapper for localStorage dict in worker process."""

    def __init__(self, data: dict) -> None:
        self._data = data

    def all(self) -> dict[str, str]:
        return dict(self._data)

    def get(self, key: str) -> str | None:
        return self._data.get(key)

    def keys(self) -> list[str]:
        return list(self._data.keys())

    def has(self, key: str) -> bool:
        return key in self._data


def _run_storage_worker(code: str, data: dict) -> tuple[str, str]:
    import json, math, re
    store = _ReadOnlyStorage(data)
    wrapped = textwrap.dedent(f"""\
def __extract__():
{textwrap.indent(code, '    ')}

__result__ = __extract__()
""")
    try:
        ns: dict = {"json": json, "re": re, "math": math, "storage": store}
        exec(compile(wrapped, "<devtools-storage-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_storage_query(
    code: str,
    storage_store: object,
    timeout_sec: float = 2.0,
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against storage store. Shares pool."""
    data = dict(storage_store._data) if hasattr(storage_store, '_data') else storage_store.all()
    try:
        future = _net._executor.submit(_run_storage_worker, code, data)
        tag, val = future.result(timeout=timeout_sec)
    except concurrent.futures.TimeoutError:
        _net._replace_executor()
        return DevtoolsQueryResult(success=False, error="Execution timeout: code exceeded time limit")
    except concurrent.futures.BrokenExecutor:
        _net._replace_executor()
        return DevtoolsQueryResult(success=False, error="Executor crashed — replaced")
    except Exception as exc:
        return DevtoolsQueryResult(success=False, error=str(exc))
    if tag == "ok":
        return DevtoolsQueryResult(success=True, value=val)
    return DevtoolsQueryResult(success=False, error=val)
