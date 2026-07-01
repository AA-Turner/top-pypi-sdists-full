from __future__ import annotations

import textwrap
import traceback

import testmu._helpers.devtools_network as _net
import concurrent.futures
from testmu._helpers.devtools_network import DevtoolsQueryResult


class _ReadOnlyCookieStore:
    """Query-only wrapper for CookieEntry list in worker process."""

    def __init__(self, entries: list) -> None:
        self._entries = entries

    def all(self) -> list:
        return list(self._entries)

    def get(self, name: str):
        for e in self._entries:
            if e.name == name:
                return e
        return None

    def names(self) -> list[str]:
        return [e.name for e in self._entries]

    def by_domain(self, domain: str) -> list:
        return [e for e in self._entries if e.domain == domain or e.domain.endswith(f".{domain}")]


def _run_cookies_worker(code: str, entries: list) -> tuple[str, str]:
    import json, math, re
    store = _ReadOnlyCookieStore(entries)
    wrapped = textwrap.dedent(f"""\
def __extract__():
{textwrap.indent(code, '    ')}

__result__ = __extract__()
""")
    try:
        ns: dict = {"json": json, "re": re, "math": math, "cookies": store}
        exec(compile(wrapped, "<devtools-cookies-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_cookies_query(
    code: str,
    cookie_store: object,
    timeout_sec: float = 2.0,
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against cookie store. Shares pool with network/console."""
    entries = list(cookie_store._entries)
    try:
        future = _net._executor.submit(_run_cookies_worker, code, entries)
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
