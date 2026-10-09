"""Virtual clipboard — store, interception script, install, query executor.

The test owns its clipboard entirely: an in-process ClipboardStore plus a JS
interception layer injected into every frame. The OS/process clipboard is
never read and never written. Spec:
v16 repo docs/superpowers/specs/2026-06-12-virtual-clipboard-design.md.

Shared by exported binding tests (via testmu.configure(clipboard=True)) and
by the recording path (which creates its own store and calls install_clipboard).
"""

from __future__ import annotations

import base64
import concurrent.futures
import hashlib
import json
import logging
import math
import re
import textwrap
import traceback

import testmu._v3._helpers.devtools_network as _net
from testmu._v3._helpers.devtools_network import DevtoolsQueryResult

logger = logging.getLogger("testmu.clipboard")

from testmu._clipboard_store import ClipboardStore  # noqa: E402,F401  (re-exported)


# ---------------------------------------------------------------------------
# Interception script (injected into every frame, before page scripts)
# ---------------------------------------------------------------------------

def _load_intercept_js() -> str:
    """Single-source interception script — shipped as package data so the
    same file can be diffed/synced against the TS package's copy."""
    from importlib.resources import files
    return files("testmu._v3._helpers").joinpath("clipboard_intercept.js").read_text(encoding="utf-8")


INTERCEPT_JS = _load_intercept_js()


async def install_clipboard(context, store: ClipboardStore) -> None:
    """Install the interception layer on a browser context.

    Applies to pages created/navigated after install — callers install at
    context creation (runner) or session start (bindings).
    """

    async def _bridge(source, payload: str) -> str:
        try:
            msg = json.loads(payload)
        except Exception:
            return "{}"
        if msg.get("op") == "capture":
            store.replace_from_reps(msg.get("reps") or [])
            return "{}"
        if msg.get("op") == "read":
            return json.dumps({"reps": store.to_reps()})
        return "{}"

    await context.expose_binding("__v16ClipboardBridge", _bridge)
    await context.add_init_script(INTERCEPT_JS)


async def paste_via_page(page, store: ClipboardStore) -> None:
    """Execute the synthesis routine directly at document.activeElement."""
    payload = {"reps": store.to_reps()}
    await page.evaluate(
        "(entry) => window.__v16ClipboardPaste(entry, false)", payload,
    )


# ---------------------------------------------------------------------------
# Query executor (devtool_clipboard analyzer) — mirrors devtools_storage
# ---------------------------------------------------------------------------

def _run_clipboard_worker(code: str, reps: list) -> tuple:
    try:
        store = ClipboardStore()
        store._reps = reps
        body = textwrap.indent(code, "    ")
        wrapped = f"def __extract__(clipboard):\n{body}\n__result__ = __extract__(__clipboard__)"
        ns: dict = {"json": json, "re": re, "math": math, "__clipboard__": store}
        exec(compile(wrapped, "<devtools-clipboard-extract>", "exec"), ns)
        raw = ns.get("__result__")
        return ("ok", str(raw) if raw is not None else "")
    except Exception:
        return ("err", traceback.format_exc())


def devtools_clipboard_query(
    code: str,
    clipboard_store: ClipboardStore,
    timeout_sec: float = 2.0,
) -> DevtoolsQueryResult:
    """Execute LLM-generated code against the virtual clipboard. Shares pool."""
    reps = clipboard_store.to_reps()
    try:
        future = _net._executor.submit(_run_clipboard_worker, code, reps)
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
