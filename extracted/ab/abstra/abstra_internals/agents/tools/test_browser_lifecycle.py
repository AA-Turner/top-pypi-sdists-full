"""Regression tests for the BrowserTools event-loop leak inside warm executors.

Bug: BrowserTools started one `sync_playwright()` driver per instance and
nothing closed it at the end of an execution. Playwright's sync API keeps an
asyncio loop "running" on the thread (via greenlets) while the driver is open,
so the next execution reusing the warm executor found a stale running loop,
clobbered it with `asyncio._set_running_loop(None)` and stacked a second
driver + Chromium in the same process — until the executor died and RabbitMQ
redelivered the message ("Execution did not complete on a previous delivery").

These tests exercise the fix at the driver level (no Chromium required, CI
does not install browsers):
- the playwright driver is shared per thread with refcounting
- open tools register themselves and executor teardown closes leaks
- after cleanup the thread has no running-loop marker left
"""

import asyncio
import os
import unittest
from typing import Any, cast

from abstra_internals.agents import lifecycle
from abstra_internals.agents.tools.browser import (
    BrowserTools,
    _acquire_playwright,
    _release_playwright,
)


def running_loop_marker():
    """Return the loop asyncio believes is running on this thread, if any."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


class FakeTool:
    def __init__(self):
        self.closed = False
        lifecycle.register_tool(self)

    def close(self):
        self.closed = True
        lifecycle.unregister_tool(self)


class BrokenTool(FakeTool):
    def close(self):
        super().close()
        raise RuntimeError("boom")


class LeakyDriverTool:
    """Mirrors BrowserTools' lifecycle contract without launching Chromium."""

    def __init__(self):
        self._pw = _acquire_playwright()
        self._closed = False
        lifecycle.register_tool(self)

    def close(self):
        if self._closed:
            return
        self._closed = True
        _release_playwright()
        lifecycle.unregister_tool(self)


class TestLeakedToolsRegistry(unittest.TestCase):
    def tearDown(self):
        lifecycle.close_leaked_tools()

    def test_close_leaked_tools_closes_registered_instances(self):
        tool = FakeTool()
        self.assertEqual(lifecycle.open_tools_count(), 1)

        closed = lifecycle.close_leaked_tools()

        self.assertEqual(closed, 1)
        self.assertTrue(tool.closed)
        self.assertEqual(lifecycle.open_tools_count(), 0)

    def test_tool_closed_by_user_is_not_leaked(self):
        tool = FakeTool()
        tool.close()

        self.assertEqual(lifecycle.open_tools_count(), 0)
        self.assertEqual(lifecycle.close_leaked_tools(), 0)

    def test_close_leaked_tools_survives_broken_close(self):
        broken = BrokenTool()
        healthy = FakeTool()

        closed = lifecycle.close_leaked_tools()

        self.assertTrue(broken.closed)
        self.assertTrue(healthy.closed)
        self.assertEqual(closed, 2)
        self.assertEqual(lifecycle.open_tools_count(), 0)

    def test_double_close_is_idempotent(self):
        tool = FakeTool()
        tool.close()
        tool.close()

        self.assertEqual(lifecycle.open_tools_count(), 0)


class TestSharedPlaywrightDriver(unittest.TestCase):
    def tearDown(self):
        lifecycle.close_leaked_tools()
        # Drain any refs a failing test left behind (bounded to avoid hanging)
        for _ in range(10):
            if running_loop_marker() is None:
                break
            _release_playwright()

    def test_acquire_is_shared_per_thread(self):
        first = _acquire_playwright()
        marker_after_first = running_loop_marker()
        second = _acquire_playwright()

        self.assertIs(first, second)
        # The second acquire must not touch the thread's loop state — the old
        # code called asyncio._set_running_loop(None) here, corrupting the
        # already-running driver loop.
        self.assertIs(running_loop_marker(), marker_after_first)

        _release_playwright()
        _release_playwright()

    def test_release_last_reference_stops_driver_and_clears_loop_marker(self):
        _acquire_playwright()
        self.assertIsNotNone(running_loop_marker())

        _release_playwright()

        self.assertIsNone(running_loop_marker())

    def test_driver_survives_until_last_reference(self):
        _acquire_playwright()
        _acquire_playwright()

        _release_playwright()
        self.assertIsNotNone(running_loop_marker())

        _release_playwright()
        self.assertIsNone(running_loop_marker())

    def test_reacquire_after_full_release_starts_fresh_driver(self):
        first = _acquire_playwright()
        _release_playwright()

        second = _acquire_playwright()
        self.assertIsNot(first, second)
        _release_playwright()
        self.assertIsNone(running_loop_marker())


class TestWarmExecutorLeakRecovery(unittest.TestCase):
    """End-to-end reproduction of the reported bug at the driver level."""

    def test_leaked_tool_is_recovered_between_executions(self):
        # Execution 1: user code creates browser tooling and never closes it
        # (run_agent does not close tools either).
        LeakyDriverTool()

        # The bug mechanism: the warm executor thread still believes an
        # asyncio loop is running after user code finished.
        self.assertIsNotNone(running_loop_marker())

        # Executor teardown between executions must close the leak...
        closed = lifecycle.close_leaked_tools()
        self.assertEqual(closed, 1)

        # ...leaving the thread clean for the next execution: no stale
        # running loop, no stacked driver.
        self.assertIsNone(running_loop_marker())

        # Execution 2 starts from a clean slate.
        tool = LeakyDriverTool()
        self.assertIsNotNone(running_loop_marker())
        tool.close()
        self.assertIsNone(running_loop_marker())


class _RaisingPage:
    def __init__(self, exc: BaseException):
        self._exc = exc

    def close(self):
        raise self._exc


class TestCloseIsBaseExceptionSafe(unittest.TestCase):
    """The executor's SIGTERM handler raises ClientAbandoned (a BaseException).

    If it lands mid-close(), the shared driver reference and the registry
    entry must still be released — otherwise the refcount is stuck >0 forever
    and the driver leaks across every later execution of the warm executor."""

    def tearDown(self):
        lifecycle.close_leaked_tools()
        for _ in range(10):
            if running_loop_marker() is None:
                break
            _release_playwright()

    def test_close_releases_driver_when_page_close_raises_base_exception(self):
        tool = BrowserTools.__new__(BrowserTools)
        tool.debug_mode = False
        tool._closed = False
        tool._is_remote = True
        tool.pages = {"p": cast(Any, _RaisingPage(KeyboardInterrupt()))}
        _acquire_playwright()
        lifecycle.register_tool(tool)

        with self.assertRaises(KeyboardInterrupt):
            tool.close()

        # Driver reference dropped and tool unregistered despite the raise.
        self.assertIsNone(running_loop_marker())
        self.assertEqual(lifecycle.open_tools_count(), 0)


class TestBrowserToolsRealChromium(unittest.TestCase):
    """Same scenarios with the real BrowserTools + Chromium.

    Skipped where Chromium is not installed (CI does not install browsers);
    run locally with `playwright install chromium`.
    """

    def setUp(self):
        pw = _acquire_playwright()
        try:
            if not os.path.exists(pw.chromium.executable_path):
                self.skipTest(
                    "Chromium not installed (run `playwright install chromium`)"
                )
        finally:
            _release_playwright()

    def tearDown(self):
        lifecycle.close_leaked_tools()

    def test_warm_executor_reuse_recovers_leaked_browser(self):
        # Execution 1: tasklet creates BrowserTools and never closes it.
        BrowserTools(headless=True)
        self.assertIsNotNone(running_loop_marker())

        # Executor teardown between executions.
        self.assertEqual(lifecycle.close_leaked_tools(), 1)
        self.assertIsNone(running_loop_marker())

        # Execution 2: clean init — before the fix this was the run that
        # logged "Found running event loop, unsetting it" and stacked a
        # second driver + Chromium.
        tools = BrowserTools(headless=True)
        self.assertIsNotNone(running_loop_marker())
        tools.close()
        self.assertIsNone(running_loop_marker())
        self.assertEqual(lifecycle.open_tools_count(), 0)

    def test_two_browser_tools_in_same_execution_share_driver(self):
        first = BrowserTools(headless=True)
        second = BrowserTools(headless=True)

        first.close()
        # The shared driver survives while another instance still holds it.
        self.assertIsNotNone(running_loop_marker())

        second.close()
        self.assertIsNone(running_loop_marker())
        self.assertEqual(lifecycle.open_tools_count(), 0)
