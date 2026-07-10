"""Registry of open agent toolkits so the executor can close leaks.

Warm executors are reused across executions. Toolkits that hold OS resources
(e.g. BrowserTools' playwright driver + Chromium) register themselves here on
init and unregister on close(). The executor teardown calls
`close_leaked_tools()` after every execution: anything user code (or
`run_agent`, which never closes tools) left open would otherwise survive into
the next execution — playwright's sync driver keeps an asyncio loop marked as
running on the thread, and each reuse stacked another driver + Chromium until
the executor died mid-delivery ("Execution did not complete on a previous
delivery").

This module must stay import-light (no playwright import): the executor loads
it on every execution, including ones that never touch a browser.
"""

import threading
from typing import Any, List

_lock = threading.Lock()
_open_tools: List[Any] = []


def register_tool(tool: Any) -> None:
    with _lock:
        _open_tools.append(tool)


def unregister_tool(tool: Any) -> None:
    with _lock:
        try:
            _open_tools.remove(tool)
        except ValueError:
            pass


def open_tools_count() -> int:
    with _lock:
        return len(_open_tools)


def close_leaked_tools() -> int:
    """Close every tool still registered and return how many were leaked.

    Close errors are swallowed per tool: one broken toolkit must not keep the
    executor from releasing the others.
    """
    with _lock:
        leaked = _open_tools[:]
        _open_tools.clear()
    for tool in leaked:
        try:
            tool.close()
        except Exception as e:
            # A failed close means the resource may still be alive — make it
            # observable instead of silently reporting the leak as handled.
            try:
                from abstra_internals.logger import AbstraLogger

                AbstraLogger.error(
                    f"[lifecycle] Failed to close leaked {type(tool).__name__}: {e}"
                )
            except Exception:
                pass
    return len(leaked)
