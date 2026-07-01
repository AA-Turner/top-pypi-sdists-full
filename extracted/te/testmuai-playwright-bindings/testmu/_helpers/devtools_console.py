from __future__ import annotations

import textwrap
import traceback

import concurrent.futures
import testmu._helpers.devtools_network as _net
from testmu._helpers.devtools_network import DevtoolsQueryResult


class _ReadOnlyConsoleLog:
    """Query-only wrapper for ConsoleEntry list in worker process."""

    def __init__(self, entries: list) -> None:
        self._entries = entries

    def messages(
        self,
        *,
        level: str | None = None,
        text_contains: str | None = None,
        after: float | None = None,
        before: float | None = None,
        is_exception: bool | None = None,
    ) -> list:
        result = []
        for e in self._entries:
            if level and e.level != level:
                continue
            if text_contains and text_contains not in e.text:
                continue
            if after and e.timestamp_ms < after:
                continue
            if before and e.timestamp_ms > before:
                continue
            if is_exception is not None and e.is_exception != is_exception:
                continue
            result.append(e)
        return result

    def errors(self) -> list:
        return [e for e in self._entries if e.level == "error"]

    def warnings(self) -> list:
        return [e for e in self._entries if e.level == "warning"]

    def exceptions(self) -> list:
        return [e for e in self._entries if e.is_exception]


def _run_console_worker(code: str, entries: list) -> tuple[str, str]:
    """Runs in the shared pre-spawned worker process."""
    import json
    import math
    import re

    log = _ReadOnlyConsoleLog(entries)

    wrapped = textwrap.dedent(f"""\
def __extract__():
{textwrap.indent(code, '    ')}

__result__ = __extract__()
""")
    try:
        ns: dict = {"json": json, "re": re, "math": math, "console": log}
        exec(compile(wrapped, "<devtools-console-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_console_query(
    code: str,
    console_log: object,
    timeout_sec: float = 2.0,
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against console log. Shares pool with network."""
    entries = list(console_log._entries)

    try:
        future = _net._executor.submit(_run_console_worker, code, entries)
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
