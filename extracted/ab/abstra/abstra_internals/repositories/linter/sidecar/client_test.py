"""Contract tests for SidecarLinterRepository (PR1, TDD).

The client is exercised against an in-process fake child that speaks the real
protocol over OS pipes — no real subprocess here (lifecycle_test.py covers
that). These tests freeze the client's behavioral contract: mirror semantics,
degraded mode, deploy fail-closed, respawn/resync, irrecoverability policy.
"""

import json
import os
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from abstra_internals.repositories.linter.repository import LinterRepository
from abstra_internals.repositories.linter.sidecar.client import (
    SidecarLinterRepository,
    SidecarUnavailableError,
)
from abstra_internals.repositories.linter.sidecar.protocol import RpcChannel

NO_RESPONSE = object()


def _rules(*names: str) -> list:
    """Rule-like stand-ins: the client only reads .name (serialization by
    name); real rule resolution lives in the child."""
    return [SimpleNamespace(name=name) for name in names]


def _wait_for(predicate, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


CHECKS_FULL = [
    {
        "name": "RuleA",
        "label": "Rule A label",
        "type": "bug",
        "issues": [
            {
                "label": "broken thing",
                "fixes": [{"name": "FixIt", "label": "Fix it now"}],
            }
        ],
        "fixWithAi": True,
    },
    {
        "name": "RuleB",
        "label": "Rule B label",
        "type": "info",
        "issues": [],
        "fixWithAi": False,
    },
]

CHECKS_PARTIAL = [
    {
        "name": "RuleA",
        "label": "Rule A label",
        "type": "bug",
        "issues": [],
        "fixWithAi": True,
    }
]


def _default_handler(fake, method, params, rid):
    if method == "run_all":
        return {"checks": CHECKS_FULL}
    if method == "run_rules":
        return {"checks": CHECKS_PARTIAL}
    if method == "get_checks":
        return {"checks": CHECKS_FULL}
    if method == "apply_fix":
        return {"ok": True, "checks": CHECKS_FULL, "process_action": None}
    if method == "fix_all":
        return {"ok": True, "process_action": None}
    if method == "blocking_checks_for_deploy":
        return {"blocking": [CHECKS_FULL[0]], "checks": CHECKS_FULL}
    if method == "shutdown":
        return {"ok": True}
    raise AssertionError("unexpected method %s" % method)


class FakeSidecar:
    """In-process stand-in for the child: a Popen-like handle whose pipes are
    served by a thread speaking the sidecar protocol."""

    def __init__(self, handler=_default_handler, hello=True):
        c2s_r, c2s_w = os.pipe()  # client -> "child"
        s2c_r, s2c_w = os.pipe()  # "child" -> client
        # Popen-like surface used by the client
        self.stdin = os.fdopen(c2s_w, "wb")
        self.stdout = os.fdopen(s2c_r, "rb")
        self.pid = 99999
        self.returncode = None
        # Our side of the pipes
        self._reader = os.fdopen(c2s_r, "rb")
        self._writer = os.fdopen(s2c_w, "wb")
        self.chan = RpcChannel(self._reader, self._writer)
        self.received = []
        self.reverse_results = []
        self._handler = handler
        if hello:
            self.chan.notify("hello", {"lib_version": "fake", "protocol_version": 1})
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        def dispatch(msg):
            method = msg.get("method")
            params = msg.get("params")
            rid = msg.get("id")
            self.received.append((method, params))
            if rid is None:
                return
            try:
                result = self._handler(self, method, params, rid)
            except Exception as e:  # noqa: BLE001
                self.chan.respond_error(rid, str(e))
                return
            if result is NO_RESPONSE:
                return
            self.chan.respond(rid, result)

        try:
            self.chan.pump(dispatch)
        except Exception:
            pass

    def methods(self):
        return [m for m, _ in self.received]

    # --- Popen-like API ---

    def poll(self):
        return self.returncode

    def kill(self):
        if self.returncode is None:
            self.returncode = -9
        # _writer first (EOF for the client's reader), then our stdin end so
        # our own pump unblocks BEFORE _reader is closed (closing a reader
        # under a blocked read deadlocks on the buffer lock).
        for stream in (self._writer, self.stdin, self._reader):
            try:
                stream.close()
            except Exception:
                pass

    def terminate(self):
        self.kill()

    def wait(self, timeout=None):
        if self.returncode is None:
            self.returncode = 0
        return self.returncode

    def close_all(self):
        self.kill()
        for stream in (self.stdin, self.stdout):
            try:
                stream.close()
            except Exception:
                pass


def _dead_on_arrival_factory(fakes):
    def factory():
        fake = FakeSidecar(hello=False)
        fake.kill()
        fakes.append(fake)
        return fake

    return factory


class ClientTestBase(unittest.TestCase):
    def _make_repo(self, handler=_default_handler, **kwargs):
        fakes = []

        def factory():
            fake = FakeSidecar(handler)
            fakes.append(fake)
            return fake

        defaults: dict = dict(
            popen_factory=factory,
            request_timeout=5.0,
            backoff_schedule=[0.0, 0.0, 0.0],
            is_web=False,
            exiter=Mock(),
            process_action_executor=Mock(),
            diagnostics_handler=Mock(return_value=[]),
            on_checks_updated=Mock(),
        )
        defaults.update(kwargs)
        repo = SidecarLinterRepository(**defaults)
        self.addCleanup(repo.stop)
        self.addCleanup(lambda: [f.close_all() for f in fakes])
        return repo, fakes


class ClientContractTest(ClientTestBase):
    def test_implements_linter_repository_abc(self):
        repo, _ = self._make_repo()
        self.assertIsInstance(repo, LinterRepository)

    def test_checks_is_instance_state_not_class_state(self):
        repo1, _ = self._make_repo()
        repo2, _ = self._make_repo()
        repo1.update_checks()
        self.assertEqual(len(repo1.checks), len(CHECKS_FULL))
        self.assertEqual(list(repo2.checks), [])
        self.assertEqual(list(LinterRepository.checks), [])

    def test_update_specific_checks_serializes_names_and_abs_paths(self):
        repo, fakes = self._make_repo()
        rules = _rules("RuleA", "RuleB")
        result = repo.update_specific_checks(rules, paths=[Path("/tmp/proj/a.py")])

        run_rules = next((m, p) for m, p in fakes[0].received if m == "run_rules")
        self.assertEqual(run_rules[1]["rules"], ["RuleA", "RuleB"])
        self.assertEqual(len(run_rules[1]["paths"]), 1)
        sent_path = run_rules[1]["paths"][0]
        self.assertIsInstance(sent_path, str)
        self.assertTrue(os.path.isabs(sent_path))
        self.assertTrue(sent_path.endswith("a.py"))

        self.assertEqual([c.to_dict() for c in result], CHECKS_PARTIAL)

    def test_update_specific_checks_without_paths_sends_null(self):
        repo, fakes = self._make_repo()
        repo.update_specific_checks(_rules("RuleA"))
        run_rules = next((m, p) for m, p in fakes[0].received if m == "run_rules")
        self.assertIsNone(run_rules[1]["paths"])

    def test_mirror_exposes_full_check_contract(self):
        repo, _ = self._make_repo()
        repo.update_checks()

        check = repo.checks[0]
        self.assertEqual(check.to_dict(), CHECKS_FULL[0])
        # JSON-serializable end to end (broadcast path)
        json.dumps([c.to_dict() for c in repo.checks])

        self.assertEqual(check.name, "RuleA")
        self.assertEqual(check.label, "Rule A label")
        self.assertEqual(check.type, "bug")
        self.assertTrue(check.fix_with_ai)

        issue = check.issues[0]
        self.assertEqual(issue.make_label(), "broken thing")
        fix = issue.fixes[0]
        self.assertEqual(fix.name, "FixIt")
        self.assertEqual(fix.make_label(), "Fix it now")
        with self.assertRaises(NotImplementedError):
            fix.fix()

    def test_find_issues_serves_mirror_without_rpc(self):
        repo, fakes = self._make_repo()
        repo.update_checks()
        fakes[0].received.clear()
        result = repo.find_issues_in_codebase()
        self.assertEqual([c.to_dict() for c in result], CHECKS_FULL)
        self.assertEqual(fakes[0].received, [])

    def test_find_issues_rpcs_get_checks_when_mirror_empty(self):
        repo, fakes = self._make_repo()
        result = repo.find_issues_in_codebase()
        self.assertIn("get_checks", fakes[0].methods())
        self.assertEqual([c.to_dict() for c in result], CHECKS_FULL)

    def test_empty_checks_response_does_not_wipe_mirror(self):
        def handler(fake, method, params, rid):
            if method == "run_rules":
                return {"checks": []}
            return _default_handler(fake, method, params, rid)

        repo, _ = self._make_repo(handler)
        repo.update_checks()
        self.assertEqual(len(repo.checks), len(CHECKS_FULL))

        result = repo.update_specific_checks(_rules("RuleA"))
        self.assertEqual([c.to_dict() for c in repo.checks], CHECKS_FULL)
        self.assertEqual([c.to_dict() for c in result], CHECKS_FULL)

    def test_get_blocking_checks_filters_mirror_locally(self):
        def handler(fake, method, params, rid):
            if method == "run_all":
                return {
                    "checks": [
                        {
                            "name": "BugWithIssues",
                            "label": "x",
                            "type": "bug",
                            "issues": [{"label": "i", "fixes": []}],
                            "fixWithAi": False,
                        },
                        {
                            "name": "BugNoIssues",
                            "label": "x",
                            "type": "bug",
                            "issues": [],
                            "fixWithAi": False,
                        },
                        {
                            "name": "InfoWithIssues",
                            "label": "x",
                            "type": "info",
                            "issues": [{"label": "i", "fixes": []}],
                            "fixWithAi": False,
                        },
                        {
                            "name": "SecurityWithIssues",
                            "label": "x",
                            "type": "security",
                            "issues": [{"label": "i", "fixes": []}],
                            "fixWithAi": False,
                        },
                    ]
                }
            return _default_handler(fake, method, params, rid)

        repo, fakes = self._make_repo(handler)
        repo.update_checks()
        fakes[0].received.clear()

        blocking = repo.get_blocking_checks()
        self.assertEqual(
            sorted(c.name for c in blocking),
            ["BugWithIssues", "SecurityWithIssues"],
        )
        self.assertEqual(fakes[0].received, [])

    def test_fix_issue_returns_bool_and_executes_process_action(self):
        def handler(fake, method, params, rid):
            if method == "apply_fix":
                return {
                    "ok": True,
                    "checks": CHECKS_FULL,
                    "process_action": "restart_editor",
                }
            return _default_handler(fake, method, params, rid)

        executor = Mock()
        repo, fakes = self._make_repo(handler, process_action_executor=executor)
        ok = repo.fix_issue_in_codebase("RuleA", "FixIt")
        self.assertTrue(ok)
        executor.assert_called_once_with("restart_editor")
        apply_fix = next((m, p) for m, p in fakes[0].received if m == "apply_fix")
        self.assertEqual(apply_fix[1], {"rule": "RuleA", "fix": "FixIt"})
        self.assertEqual([c.to_dict() for c in repo.checks], CHECKS_FULL)

    def test_fix_issue_false_does_not_execute_action(self):
        def handler(fake, method, params, rid):
            if method == "apply_fix":
                return {"ok": False, "checks": [], "process_action": None}
            return _default_handler(fake, method, params, rid)

        executor = Mock()
        repo, _ = self._make_repo(handler, process_action_executor=executor)
        self.assertFalse(repo.fix_issue_in_codebase("Nope", "Nada"))
        executor.assert_not_called()


class ClientDegradedModeTest(ClientTestBase):
    def test_spawn_failure_degrades_without_raising(self):
        def factory():
            raise OSError("spawn denied")

        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            is_web=False,
            exiter=Mock(),
        )
        self.addCleanup(repo.stop)

        self.assertEqual(list(repo.update_checks()), [])
        self.assertEqual(list(repo.find_issues_in_codebase()), [])
        self.assertFalse(repo.fix_issue_in_codebase("RuleA", "FixIt"))

    def test_child_death_returns_stale_mirror(self):
        calls = {"n": 0}
        fakes = []

        def factory():
            calls["n"] += 1
            if calls["n"] > 1:
                raise OSError("no respawn for you")
            fake = FakeSidecar()
            fakes.append(fake)
            return fake

        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            is_web=False,
            exiter=Mock(),
        )
        self.addCleanup(repo.stop)

        repo.update_checks()
        self.assertEqual([c.to_dict() for c in repo.checks], CHECKS_FULL)

        fakes[0].kill()
        result = repo.update_specific_checks(_rules("RuleA"))
        self.assertEqual([c.to_dict() for c in result], CHECKS_FULL)

    def test_eof_fails_pending_request_quickly(self):
        def handler(fake, method, params, rid):
            if method == "run_all":
                return NO_RESPONSE
            return _default_handler(fake, method, params, rid)

        repo, fakes = self._make_repo(handler, request_timeout=30.0)
        done = {}

        def call():
            start = time.monotonic()
            done["result"] = repo.update_checks()
            done["elapsed"] = time.monotonic() - start

        t = threading.Thread(target=call, daemon=True)
        t.start()
        time.sleep(0.3)
        fakes[0].kill()
        t.join(timeout=10)
        self.assertIn("elapsed", done)
        self.assertLess(done["elapsed"], 8)
        self.assertEqual(list(done["result"]), [])

    def test_timeout_kills_child_and_recovers_on_next_call(self):
        def handler(fake, method, params, rid):
            if method == "run_rules":
                return NO_RESPONSE
            return _default_handler(fake, method, params, rid)

        repo, fakes = self._make_repo(handler, request_timeout=0.5)
        start = time.monotonic()
        result = repo.update_specific_checks(_rules("RuleA"))
        elapsed = time.monotonic() - start
        self.assertEqual(list(result), [])  # degraded: stale (empty) mirror
        self.assertGreaterEqual(elapsed, 0.3)
        self.assertLess(elapsed, 8)
        self.assertIsNotNone(fakes[0].poll())  # hung child was killed

        checks = repo.update_checks()
        self.assertEqual([c.to_dict() for c in checks], CHECKS_FULL)
        self.assertEqual(len(fakes), 2)
        self.assertIsNone(fakes[1].poll())  # healthy replacement left alone

    def test_deploy_gate_fail_closed_when_unavailable(self):
        def factory():
            raise OSError("spawn denied")

        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            is_web=False,
            exiter=Mock(),
        )
        self.addCleanup(repo.stop)
        with self.assertRaises(SidecarUnavailableError):
            repo.get_blocking_checks_for_deploy()

    def test_deploy_gate_returns_blocking_when_healthy(self):
        repo, _ = self._make_repo()
        blocking = repo.get_blocking_checks_for_deploy()
        self.assertEqual([c.to_dict() for c in blocking], [CHECKS_FULL[0]])
        # Mirror refreshed from the same response
        self.assertEqual([c.to_dict() for c in repo.checks], CHECKS_FULL)


class ClientRespawnTest(ClientTestBase):
    def test_resync_after_respawn_runs_run_all_first_and_broadcasts(self):
        on_updated = Mock()
        repo, fakes = self._make_repo(on_checks_updated=on_updated)
        repo.update_checks()
        self.assertEqual(len(fakes), 1)

        fakes[0].kill()
        result = repo.update_specific_checks(_rules("RuleA"))

        self.assertEqual(len(fakes), 2)
        lint_methods = [m for m in fakes[1].methods() if m != "hello"]
        self.assertEqual(lint_methods[0], "run_all")
        self.assertIn("run_rules", lint_methods)
        self.assertEqual([c.to_dict() for c in result], CHECKS_PARTIAL)

        # The resync broadcast is asynchronous (waiter thread) — poll for it.
        self.assertTrue(_wait_for(lambda: on_updated.called))
        broadcast_checks = on_updated.call_args[0][0]
        self.assertEqual([c.to_dict() for c in broadcast_checks], CHECKS_FULL)

    def test_no_resync_on_first_spawn(self):
        on_updated = Mock()
        repo, fakes = self._make_repo(on_checks_updated=on_updated)
        repo.update_specific_checks(_rules("RuleA"))
        lint_methods = [m for m in fakes[0].methods() if m != "hello"]
        self.assertEqual(lint_methods, ["run_rules"])
        on_updated.assert_not_called()


class ClientIrrecoverableTest(ClientTestBase):
    def test_web_mode_calls_exiter_once_after_threshold(self):
        fakes = []
        factory = _dead_on_arrival_factory(fakes)
        exiter = Mock()
        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            premature_death_threshold=3,
            is_web=True,
            exiter=exiter,
        )
        self.addCleanup(repo.stop)

        for _ in range(5):
            repo.update_checks()

        self.assertEqual(exiter.call_count, 1)
        self.assertEqual(len(fakes), 3)

    def test_local_mode_degrades_terminally_without_exiter(self):
        fakes = []
        factory = _dead_on_arrival_factory(fakes)
        exiter = Mock()
        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            premature_death_threshold=3,
            is_web=False,
            exiter=exiter,
        )
        self.addCleanup(repo.stop)

        for _ in range(5):
            self.assertEqual(list(repo.update_checks()), [])

        exiter.assert_not_called()
        self.assertEqual(len(fakes), 3)

    def test_successful_rpc_resets_premature_death_counter(self):
        fakes = []
        state = {"healthy_round": False}

        def factory():
            if state["healthy_round"]:
                fake = FakeSidecar()
            else:
                fake = FakeSidecar(hello=False)
                fake.kill()
            fakes.append(fake)
            return fake

        exiter = Mock()
        repo = SidecarLinterRepository(
            popen_factory=factory,
            request_timeout=2.0,
            backoff_schedule=[0.0],
            premature_death_threshold=3,
            is_web=True,
            exiter=exiter,
        )
        self.addCleanup(repo.stop)
        self.addCleanup(lambda: [f.close_all() for f in fakes])

        repo.update_checks()  # death 1
        repo.update_checks()  # death 2
        state["healthy_round"] = True
        checks = repo.update_checks()  # healthy: counter resets
        self.assertEqual([c.to_dict() for c in checks], CHECKS_FULL)

        fakes[-1].kill()
        state["healthy_round"] = False
        # Death of the healthy child (+1) plus one DOA respawn (+1) = 2 < 3.
        # Without the reset this call would cross the threshold (2 + 2 >= 3).
        repo.update_checks()
        exiter.assert_not_called()


class ClientReverseRequestTest(ClientTestBase):
    def test_lsp_diagnostics_reverse_request_is_served(self):
        def handler(fake, method, params, rid):
            if method == "run_all":

                def work():
                    diag = fake.chan.request(
                        "lsp_diagnostics", {"code": "xyz"}, timeout=5
                    )
                    fake.reverse_results.append(diag)
                    fake.chan.respond(rid, {"checks": CHECKS_FULL})

                threading.Thread(target=work, daemon=True).start()
                return NO_RESPONSE
            return _default_handler(fake, method, params, rid)

        diagnostics_handler = Mock(return_value=[{"d": 7}])
        repo, fakes = self._make_repo(handler, diagnostics_handler=diagnostics_handler)
        checks = repo.update_checks()
        self.assertEqual([c.to_dict() for c in checks], CHECKS_FULL)
        diagnostics_handler.assert_called_once_with("xyz")
        self.assertEqual(fakes[0].reverse_results, [{"diagnostics": [{"d": 7}]}])


class ClientStopTest(ClientTestBase):
    def test_stop_is_idempotent_and_terminal(self):
        repo, fakes = self._make_repo()
        repo.update_checks()
        repo.stop()
        repo.stop()
        shutdowns = [m for m in fakes[0].methods() if m == "shutdown"]
        self.assertLessEqual(len(shutdowns), 1)

        spawned_before = len(fakes)
        # After stop: degraded, no new spawns
        result = repo.update_specific_checks(_rules("RuleA"))
        self.assertEqual([c.to_dict() for c in result], CHECKS_FULL)  # stale mirror
        self.assertEqual(len(fakes), spawned_before)


if __name__ == "__main__":
    unittest.main()
