# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Support for gunicorn's pre-fork model.

When gunicorn's master process initializes the agent (e.g. with --preload), the agent
starts its background threads in the master. The master then forks every worker: at
startup, and again whenever a worker needs replacing (e.g. after --max-requests). Only
the forking thread exists in a child, so anything another thread was doing at fork time
(holding a lock, writing a log message, applying CVE shields) stays frozen mid-operation
in the child forever.

The master never serves requests, so it doesn't need the agent's background threads once
the application is loaded. Before gunicorn forks anything, we wait for those threads to
finish, and they're never restarted in the master. Every fork then happens while no agent
thread is running. Workers restart the threads they need via thread_watcher.ensure_running.

The patch is registered by agent_state.initialize(), which runs wherever the application
is loaded (when the Contrast middleware is constructed). That's also where the agent
starts its background threads, so the patch exists exactly in the processes that might
need it:

- With --preload, the master loads the application, so it starts agent threads and gets
  the patch. Arbiter.start then waits for those threads before forking any workers.
- Without --preload, the master never loads the application, so it starts no agent
  threads and is never patched. Each worker initializes the agent after it's forked; the
  patch is registered there too, but workers never call Arbiter.start, so it's inert.
"""

from __future__ import annotations

import sys
import threading
from typing import TYPE_CHECKING

import contrast
from contrast.agent.assess.rules.providers.enable import PROVIDERS_THREAD_NAME
from contrast.agent.inventory.library_reader import LIBRARY_READER_THREAD_NAME
from contrast.agent.policy import patch_manager
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_loudly
from contrast.utils.monitoring import VIZTRACER_SAVE_THREAD_NAME
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from types import ModuleType

logger = logging.getLogger("contrast")

MODULE_TO_PATCH = "gunicorn.arbiter"

_SELF_TERMINATING_THREAD_NAMES = (
    LIBRARY_READER_THREAD_NAME,
    PROVIDERS_THREAD_NAME,
    VIZTRACER_SAVE_THREAD_NAME,
)


@fail_loudly("Failed to stop agent background threads before forking")
def stop_background_threads() -> None:
    """
    Wait for every agent background thread in this process to finish.
    """
    logger.info("Waiting for agent background threads to finish before forking")

    for name in _SELF_TERMINATING_THREAD_NAMES:
        _join_threads_named(name)

    settings_thread = Settings().settings_thread
    if settings_thread is not None and settings_thread.is_alive():
        settings_thread.stop()
        settings_thread.join()

    # Telemetry is stopped last so it can still report errors from the other threads.
    # Its stop is quick when it's idle.
    if (telemetry := contrast.TELEMETRY) is not None:
        telemetry.stop(timeout=None)
        contrast.TELEMETRY = None

    logger.info(
        "Agent background threads finished",
        remaining_threads=[t.name for t in threading.enumerate()],
    )


def _join_threads_named(name: str) -> None:
    for thread in threading.enumerate():
        if thread.name == name:
            assert thread is not threading.current_thread()
            thread.join()


def build_start_patch(orig_func, _):
    """
    Arbiter.start runs once in the master process, after the application is loaded
    (with --preload) and before any worker is forked.
    """

    def start(wrapped, instance, args, kwargs):
        stop_background_threads()
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, start)


def patch_gunicorn_arbiter(arbiter_module: ModuleType) -> None:
    build_and_apply_patch(arbiter_module.Arbiter, "start", build_start_patch)


def register_patches() -> None:
    register_module_patcher(patch_gunicorn_arbiter, MODULE_TO_PATCH)


def reverse_patches() -> None:
    unregister_module_patcher(MODULE_TO_PATCH)
    if (arbiter_module := sys.modules.get(MODULE_TO_PATCH)) is None:
        return
    patch_manager.reverse_patches_by_owner(arbiter_module.Arbiter)
