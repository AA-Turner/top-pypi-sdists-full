"""Run one call in a short-lived child process, so a native crash fails THAT call, not the server.

Parsing what a website sent runs C code (selectolax, lxml). When that code dies — a segmentation fault, an abort —
Python gets no exception: the whole process ends, and with it every other run, request and stream it was serving.
On 2026-10-16 one brewery's phone link killed the workflow worker nine times and the API server three times in
25 minutes, and each restart brought the same run back to crash it again.

:func:`run_isolated` runs ``module:function`` in a fresh interpreter (``sys.executable``, about 35 ms to start for
the page pre-pass), passes JSON in on stdin and reads JSON back on stdout. If the child dies, times out or raises,
the caller gets :class:`IsolatedCallFailed` naming what happened — a loud failure of that one call; the parent
process keeps running. Only JSON-safe arguments and results cross, and the child binds no host capability (no
database, no knobs), so only pure functions belong here (``matrx_scraper.clean_content.page_prepass``).
"""

from __future__ import annotations

import asyncio
import json
import signal
import sys
import weakref
from typing import Any

#: The child: import the target, call it with the JSON arguments, print the JSON result. A Python exception is
#: reported as JSON with exit code 3, so it is told apart from a crash.
_CHILD = r"""
import importlib, json, sys, traceback
target, = sys.argv[1:2]
mod, _, fn = target.partition(":")
try:
    args = json.loads(sys.stdin.buffer.read() or b"[]")
    result = getattr(importlib.import_module(mod), fn)(*args)
except BaseException as exc:
    sys.stdout.write(json.dumps({"error": type(exc).__name__ + ": " + str(exc), "trace": traceback.format_exc()[-2000:]}))
    sys.stdout.flush()
    sys.exit(3)
sys.stdout.write(json.dumps({"result": result}))
sys.stdout.flush()
"""

#: Children at once in one process. Each is short (one page) and a fresh interpreter costs memory, so a burst of
#: pages queues here instead of forking dozens of interpreters at once.
MAX_CONCURRENT_CHILDREN = 4
_slots: weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, asyncio.Semaphore] = weakref.WeakKeyDictionary()


class IsolatedCallFailed(RuntimeError):
    """The isolated call did not return: the child crashed (``signal`` names how), timed out, or raised."""

    def __init__(self, target: str, reason: str, *, signal_name: str | None = None, exit_code: int | None = None):
        super().__init__(f"{target} failed in its isolated process: {reason}")
        self.target = target
        self.reason = reason
        self.signal_name = signal_name
        self.exit_code = exit_code


def _slot() -> asyncio.Semaphore:
    loop = asyncio.get_running_loop()
    sem = _slots.get(loop)
    if sem is None:
        sem = _slots[loop] = asyncio.Semaphore(MAX_CONCURRENT_CHILDREN)
    return sem


def _signal_name(code: int) -> str:
    try:
        return signal.Signals(-code).name
    except ValueError:
        return f"signal {-code}"


async def run_isolated(target: str, *args: Any, limit_seconds: float = 60.0) -> Any:
    """``module:function(*args)`` in a child process; its JSON result, or :class:`IsolatedCallFailed`."""
    payload = json.dumps(list(args)).encode()
    async with _slot():
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", _CHILD, target,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(payload), timeout=limit_seconds)
        except TimeoutError:
            proc.kill()
            await proc.wait()
            raise IsolatedCallFailed(target, f"no answer within {limit_seconds:g}s; the child was killed") from None
        except BaseException:
            # Our caller was canceled: never leave the child running behind it.
            if proc.returncode is None:
                proc.kill()
                await proc.wait()
            raise
    code = proc.returncode or 0
    if code < 0:
        name = _signal_name(code)
        tail = err.decode(errors="replace").strip()[-800:]
        raise IsolatedCallFailed(target, f"the child process died ({name}){': ' + tail if tail else ''}",
                                 signal_name=name, exit_code=code)
    try:
        answer = json.loads(out or b"{}")
    except ValueError:
        answer = {}
    if code != 0 or "result" not in answer:
        reason = answer.get("error") or err.decode(errors="replace").strip()[-800:] or f"exit code {code}"
        raise IsolatedCallFailed(target, str(reason), exit_code=code)
    return answer["result"]


__all__ = ["MAX_CONCURRENT_CHILDREN", "IsolatedCallFailed", "run_isolated"]
