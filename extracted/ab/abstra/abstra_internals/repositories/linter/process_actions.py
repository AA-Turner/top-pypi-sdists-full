"""Process-wide side effects requested by linter fixes.

The abstra-upgrade fix needs to restart the EDITOR process after pip swaps
site-packages. With the linter sidecar, fixes run in the child process, where
os._exit/os.execv would restart the wrong process. Fixes therefore call
request_process_action() instead of exiting directly:

- default handler (editor process / in-process kill-switch path): executes the
  action immediately — byte-identical to the historical behavior;
- the sidecar server installs a collector handler, ships the action back in
  the apply_fix RPC response, and the editor-side client executes it there.
"""

import os
import sys
import threading
from typing import Callable, Optional

from abstra_internals.environment import EDITOR_MODE, RABBITMQ_CONNECTION_URI
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.producer import WebEditorControlProducerRepository

RESTART_EDITOR = "restart_editor"

_handler_lock = threading.Lock()
_handler: Optional[Callable[[str], None]] = None


def set_process_action_handler(handler: Optional[Callable[[str], None]]) -> None:
    """Install a handler that intercepts process actions (None restores the
    default execute-immediately behavior)."""
    global _handler
    with _handler_lock:
        _handler = handler


def request_process_action(action: str) -> None:
    with _handler_lock:
        handler = _handler
    if handler is not None:
        handler(action)
        return
    execute_process_action(action)


def execute_process_action(action: str, is_web: Optional[bool] = None) -> None:
    if action != RESTART_EDITOR:
        AbstraLogger.warning(f"[ProcessAction] Unknown process action: {action}")
        return

    if is_web is None:
        from abstra_internals.environment import EDITOR_MODE

        is_web = EDITOR_MODE == "web"

    if is_web:
        # sys.exit() doesn't work because Flask runs in threaded mode;
        # os._exit() terminates directly and the kubelet restarts the pod.
        AbstraLogger.warning("[ProcessAction] Exiting editor for the pod to restart")
        os._exit(0)
    else:
        AbstraLogger.warning("[ProcessAction] Restarting editor in place")
        os.execv(sys.executable, [sys.executable] + sys.argv)


def restart_editor_and_workers(log_prefix: str) -> None:
    """Restart the worker tier and then the editor after a pip install.

    A freshly ``pip install``ed package is on disk but invisible to any process
    that fixed its ``sys.path`` / imported its modules before the install — and
    compiled deps (numpy/pandas) can't be reliably reloaded in-process. So the
    only dependable way to make new packages visible to BOTH tiers is a restart:

    - workers (forkserver + forked executors) reload via the RabbitMQ control
      broadcast, so user code runs against the new packages;
    - the editor restarts via the process-action hook, which respawns the
      linter sidecar so its checks re-discover the packages.

    Same sequence the abstra-upgrade fix uses; workers first, then the editor.
    """
    if EDITOR_MODE == "web" and RABBITMQ_CONNECTION_URI:
        try:
            WebEditorControlProducerRepository(
                RABBITMQ_CONNECTION_URI
            ).restart_workers()
            AbstraLogger.warning(f"{log_prefix} Sent restart signal to workers")
        except Exception as e:
            AbstraLogger.error(
                f"{log_prefix} Failed to send restart signal to workers: {e}"
            )

    AbstraLogger.warning(f"{log_prefix} Requesting editor restart")
    request_process_action(RESTART_EDITOR)
