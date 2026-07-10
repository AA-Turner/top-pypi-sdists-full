"""Contract tests for the sidecar server side (PR1, TDD).

The server is exercised in-process with an injected fake repository and
in-memory pipes — no child process is spawned here. Process-level behavior
(fd hygiene, real spawn) is covered by lifecycle_test.py.
"""

import os
import threading
import time
import unittest
from pathlib import Path
from typing import Callable, Optional

from abstra_internals.repositories.linter import process_actions
from abstra_internals.repositories.linter.sidecar.protocol import (
    PROTOCOL_VERSION,
    RpcChannel,
    RpcError,
)
from abstra_internals.repositories.linter.sidecar.server import SidecarLinterServer

LINT_METHODS = (
    "run_all",
    "run_rules",
    "apply_fix",
    "fix_all",
    "get_checks",
    "blocking_checks_for_deploy",
)


def _close_quietly(*streams):
    for stream in streams:
        try:
            stream.close()
        except Exception:
            pass


class _FakeCheck:
    def __init__(self, name, type="info", issues=None):
        self.name = name
        self.type = type
        self.issues = issues if issues is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "label": "label of %s" % self.name,
            "type": self.type,
            "issues": self.issues,
            "fixWithAi": False,
        }


class _FakeRule:
    def __init__(self, name):
        self.name = name


class _FakeRepo:
    """Mimics the LocalLinterRepository surface the server depends on."""

    def __init__(self):
        self.checks = [_FakeCheck("RuleA", "bug")]
        self.calls = []
        self.update_specific_hook: Optional[Callable[..., None]] = None
        self.update_checks_hook: Optional[Callable[[], None]] = None
        self.fix_issue_hook: Optional[Callable[[str, str], bool]] = None
        self.active = 0
        self.max_active = 0
        self._active_lock = threading.Lock()

    def _enter(self):
        with self._active_lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)

    def _exit(self):
        with self._active_lock:
            self.active -= 1

    def update_checks(self, revalidate_caches=False):
        self._enter()
        try:
            self.calls.append(("update_checks",))
            if self.update_checks_hook:
                self.update_checks_hook()
            return self.checks
        finally:
            self._exit()

    def update_specific_checks(self, target_rules, paths=None):
        self._enter()
        try:
            self.calls.append(("update_specific_checks", list(target_rules), paths))
            if self.update_specific_hook:
                self.update_specific_hook(target_rules, paths)
            return self.checks
        finally:
            self._exit()

    def find_issues_in_codebase(self):
        self.calls.append(("find_issues_in_codebase",))
        return self.checks

    def fix_issue_in_codebase(self, rule_name, fix_name):
        self.calls.append(("fix_issue_in_codebase", rule_name, fix_name))
        if self.fix_issue_hook:
            return self.fix_issue_hook(rule_name, fix_name)
        return True

    def fix_all_linters(self):
        self.calls.append(("fix_all_linters",))

    def get_blocking_checks_for_deploy(self):
        self.calls.append(("get_blocking_checks_for_deploy",))
        return [c for c in self.checks if c.type == "bug"]


class ServerTestBase(unittest.TestCase):
    def setUp(self):
        self.repo = _FakeRepo()
        self.registry = [_FakeRule("RuleA"), _FakeRule("RuleB")]
        self.notifications = []
        self.reverse_requests = []
        self.reverse_responder = None  # fn(chan, msg) for child->main requests

    def _start(self, **server_kwargs):
        c2s_r, c2s_w = os.pipe()
        s2c_r, s2c_w = os.pipe()
        server_reader = os.fdopen(c2s_r, "rb")
        server_writer = os.fdopen(s2c_w, "wb")
        self.client_reader = os.fdopen(s2c_r, "rb")
        self.client_writer = os.fdopen(c2s_w, "wb")
        # Writers first: EOF unblocks the serve/pump threads before their
        # readers are closed (closing a reader mid-read deadlocks).
        self.addCleanup(
            lambda: _close_quietly(
                self.client_writer, server_writer, server_reader, self.client_reader
            )
        )

        server_kwargs.setdefault("lib_version", "test-lib-1")
        self.server = SidecarLinterServer(
            repository=self.repo,
            registry=self.registry,
            reader=server_reader,
            writer=server_writer,
            **server_kwargs,
        )
        self.serve_thread = threading.Thread(target=self.server.serve, daemon=True)
        self.serve_thread.start()

        self.chan = RpcChannel(self.client_reader, self.client_writer)

        def dispatch(msg):
            if "method" in msg and "id" not in msg:
                self.notifications.append(msg)
            elif "method" in msg:
                self.reverse_requests.append(msg)
                if self.reverse_responder:
                    self.reverse_responder(self.chan, msg)

        self.pump_thread = threading.Thread(
            target=self._pump_quietly, args=(dispatch,), daemon=True
        )
        self.pump_thread.start()
        return self.server

    def _pump_quietly(self, dispatch):
        try:
            self.chan.pump(dispatch)
        except Exception:
            pass

    def _wait_for(self, predicate, timeout=5.0):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return True
            time.sleep(0.01)
        return False


class ServerDispatchTest(ServerTestBase):
    def test_hello_notification_is_sent_first(self):
        self._start()
        self.assertTrue(self._wait_for(lambda: len(self.notifications) > 0))
        hello = self.notifications[0]
        self.assertEqual(hello["method"], "hello")
        self.assertEqual(hello["params"]["protocol_version"], PROTOCOL_VERSION)
        self.assertEqual(hello["params"]["lib_version"], "test-lib-1")

    def test_run_all_returns_serialized_checks(self):
        self._start()
        result = self.chan.request("run_all", timeout=5)
        self.assertEqual(result, {"checks": [c.to_dict() for c in self.repo.checks]})
        self.assertIn(("update_checks",), self.repo.calls)

    def test_run_rules_resolves_names_and_ignores_unknown(self):
        self._start()
        result = self.chan.request(
            "run_rules", {"rules": ["RuleA", "DoesNotExist"], "paths": None}, timeout=5
        )
        self.assertEqual(result["checks"], [c.to_dict() for c in self.repo.checks])
        call = next(c for c in self.repo.calls if c[0] == "update_specific_checks")
        passed_rules = call[1]
        self.assertEqual([r.name for r in passed_rules], ["RuleA"])
        self.assertIs(passed_rules[0], self.registry[0])
        self.assertIsNone(call[2])

    def test_run_rules_deserializes_paths(self):
        self._start()
        self.chan.request(
            "run_rules",
            {"rules": ["RuleB"], "paths": ["/tmp/proj/a.py", "/tmp/proj/b.py"]},
            timeout=5,
        )
        call = next(c for c in self.repo.calls if c[0] == "update_specific_checks")
        self.assertEqual(call[2], [Path("/tmp/proj/a.py"), Path("/tmp/proj/b.py")])

    def test_lint_ops_run_serially_in_fifo_order(self):
        self._start()
        order = []
        first_started = threading.Event()
        release = threading.Event()

        def hook(rules, paths):
            order.append([r.name for r in rules])
            if not first_started.is_set():
                first_started.set()
                release.wait(timeout=10)

        self.repo.update_specific_hook = hook

        def call(names):
            self.chan.request("run_rules", {"rules": names, "paths": None}, timeout=15)

        t1 = threading.Thread(target=call, args=(["RuleA"],), daemon=True)
        t1.start()
        self.assertTrue(first_started.wait(timeout=5))
        t2 = threading.Thread(target=call, args=(["RuleB"],), daemon=True)
        t2.start()
        time.sleep(0.2)
        t3 = threading.Thread(target=call, args=(["RuleA", "RuleB"],), daemon=True)
        t3.start()
        time.sleep(0.2)
        release.set()
        for t in (t1, t2, t3):
            t.join(timeout=10)
        self.assertEqual(order, [["RuleA"], ["RuleB"], ["RuleA", "RuleB"]])
        self.assertEqual(self.repo.max_active, 1)

    def test_handler_exception_returns_error_and_server_survives(self):
        self._start()
        boom = {"on": True}

        def hook():
            if boom["on"]:
                raise ValueError("kaboom from rule land")

        self.repo.update_checks_hook = hook
        with self.assertRaises(RpcError) as cm:
            self.chan.request("run_all", timeout=5)
        self.assertIn("kaboom from rule land", str(cm.exception))

        boom["on"] = False
        result = self.chan.request("run_all", timeout=5)
        self.assertIn("checks", result)

    def test_unknown_method_returns_error(self):
        self._start()
        with self.assertRaises(RpcError):
            self.chan.request("frobnicate", {"x": 1}, timeout=5)
        # server still alive
        self.assertIn("checks", self.chan.request("run_all", timeout=5))

    def test_get_checks_calls_find_issues(self):
        self._start()
        result = self.chan.request("get_checks", timeout=5)
        self.assertEqual(result["checks"], [c.to_dict() for c in self.repo.checks])
        self.assertIn(("find_issues_in_codebase",), self.repo.calls)

    def test_blocking_checks_for_deploy_returns_blocking_and_full(self):
        self.repo = _FakeRepo()
        self.repo.checks = [
            _FakeCheck("Blocker", "bug"),
            _FakeCheck("Info", "info"),
        ]
        self._start()
        result = self.chan.request("blocking_checks_for_deploy", timeout=5)
        self.assertEqual([c["name"] for c in result["blocking"]], ["Blocker"])
        self.assertEqual([c["name"] for c in result["checks"]], ["Blocker", "Info"])

    def test_fix_all_runs_and_acknowledges(self):
        self._start()
        result = self.chan.request("fix_all", timeout=5)
        self.assertTrue(result["ok"])
        self.assertIn(("fix_all_linters",), self.repo.calls)


class ServerProcessActionTest(ServerTestBase):
    def tearDown(self):
        process_actions.set_process_action_handler(None)
        super().tearDown()

    def test_apply_fix_collects_process_action_and_resets(self):
        self._start()

        def fix_with_action(rule_name, fix_name):
            process_actions.request_process_action("restart_editor")
            return True

        self.repo.fix_issue_hook = fix_with_action
        result = self.chan.request(
            "apply_fix", {"rule": "RuleA", "fix": "FixIt"}, timeout=5
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["process_action"], "restart_editor")
        self.assertEqual(result["checks"], [c.to_dict() for c in self.repo.checks])

        # Collector must be reset between requests
        self.repo.fix_issue_hook = lambda rule, fix: True
        result2 = self.chan.request(
            "apply_fix", {"rule": "RuleA", "fix": "Other"}, timeout=5
        )
        self.assertTrue(result2["ok"])
        self.assertIsNone(result2.get("process_action"))

    def test_apply_fix_returns_false_when_fix_not_found(self):
        self._start()
        self.repo.fix_issue_hook = lambda rule, fix: False
        result = self.chan.request(
            "apply_fix", {"rule": "Nope", "fix": "Nada"}, timeout=5
        )
        self.assertFalse(result["ok"])


class ServerLifecycleTest(ServerTestBase):
    def test_shutdown_request_stops_serve(self):
        self._start()
        result = self.chan.request("shutdown", timeout=5)
        self.assertTrue(result["ok"])
        self.serve_thread.join(timeout=5)
        self.assertFalse(self.serve_thread.is_alive())

    def test_eof_stops_serve(self):
        self._start()
        # Ensure the server is fully up before slamming the pipe shut
        self.chan.request("run_all", timeout=5)
        self.client_writer.close()
        self.serve_thread.join(timeout=5)
        self.assertFalse(self.serve_thread.is_alive())


if __name__ == "__main__":
    unittest.main()
