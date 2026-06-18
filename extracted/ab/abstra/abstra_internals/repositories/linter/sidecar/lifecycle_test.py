"""Lifecycle tests with a REAL sidecar child process (PR1, TDD).

Spawns the actual `python -m abstra_internals.repositories.linter.sidecar`
module against a temp project. Covers spawn, kill -9 + respawn + resync,
EOF self-shutdown, graceful stop without orphans, and fd-level stdout hygiene
(a rule print must land on stderr, never corrupt the protocol).
"""

import os
import subprocess
import time
import unittest
from unittest.mock import Mock

import pytest

from abstra_internals.controllers.main import MainController
from abstra_internals.repositories.factory import build_editor_repositories
from abstra_internals.repositories.linter.rules import rules as ALL_RULES
from abstra_internals.repositories.linter.sidecar.client import (
    SidecarLinterRepository,
    spawn_sidecar_process,
)
from tests.fixtures import clear_dir, init_dir

# Real child boot (imports the whole rule stack) + a resync full pass can
# exceed the suite's default 60s per-test budget on slower machines.
# method="signal": the default thread-based timer is a non-daemon thread that
# deadlocks BaseTest.tearDown's wait_non_daemon_threads (pre-existing issue —
# the reason codebase_events_test/rule_groups_test "hang" under
# --timeout-method=thread).
pytestmark = pytest.mark.timeout(120, method="signal")


def _rule(name):
    return next(r for r in ALL_RULES if r.name == name)


def _wait_for(predicate, timeout=15.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return False


class SidecarLifecycleTest(unittest.TestCase):
    """Light project fixture (init_dir + MainController for create_stage),
    WITHOUT BaseTest's consumer/executor pool — its warmup children rewrite
    project files asynchronously and add noise to lifecycle timing."""

    def setUp(self):
        # Keep NewVersionOfAbstraAvailable out of the CHILD's registry so the
        # resync full pass never performs network calls (rules/__init__.py
        # reads this env at import time; the child inherits our environ).
        self._old_bundled = os.environ.get("ABSTRA_RUNNING_IN_BUNDLED_APP")
        os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = "1"
        self.root = init_dir()
        self.repositories = build_editor_repositories()
        self.controller = MainController(self.repositories)

    def tearDown(self):
        clear_dir(self.root)
        if self._old_bundled is None:
            os.environ.pop("ABSTRA_RUNNING_IN_BUNDLED_APP", None)
        else:
            os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = self._old_bundled

    def _make_repo(self, **kwargs):
        defaults: dict = dict(
            request_timeout=90.0,
            backoff_schedule=[0.1, 0.1],
            is_web=False,
            exiter=Mock(),
            diagnostics_handler=lambda code: [],
        )
        defaults.update(kwargs)
        repo = SidecarLinterRepository(**defaults)
        self.addCleanup(repo.stop)
        return repo

    def test_spawn_and_run_rules_round_trip(self):
        (self.root / "bad.css").write_text("body { : red; }")
        repo = self._make_repo()

        checks = repo.update_specific_checks([_rule("CssSyntax")])

        by_name = {c.name: c for c in checks}
        self.assertIn("CssSyntax", by_name)
        self.assertEqual(len(by_name["CssSyntax"].issues), 1)
        self.assertIn("bad.css", by_name["CssSyntax"].issues[0].make_label())

        proc = repo.child_process
        assert proc is not None
        self.assertIsNone(proc.poll())

    def test_kill9_respawns_and_resyncs_mirror(self):
        (self.root / "bad.css").write_text("body { : red; }")
        repo = self._make_repo()
        repo.update_specific_checks([_rule("CssSyntax")])

        proc1 = repo.child_process
        assert proc1 is not None
        pid1 = proc1.pid
        proc1.kill()
        self.assertTrue(_wait_for(lambda: proc1.poll() is not None))

        checks = repo.update_specific_checks([_rule("CssSyntax")])

        proc2 = repo.child_process
        assert proc2 is not None
        self.assertNotEqual(proc2.pid, pid1)

        # The respawn resync (run_all) is queued before our run_rules, so by
        # the time the call returns the mirror holds the full registry's
        # checks, not just CssSyntax.
        names = {c.name for c in checks}
        self.assertIn("CssSyntax", names)
        self.assertIn("SyntaxErrors", names)
        self.assertIn("MissingAbstraInRequirements", names)
        css = next(c for c in checks if c.name == "CssSyntax")
        self.assertEqual(len(css.issues), 1)

    def test_eof_on_stdin_makes_child_exit_alone(self):
        repo = self._make_repo()
        repo.update_specific_checks([_rule("CssSyntax")])
        proc = repo.child_process
        assert proc is not None and proc.stdin is not None
        self.assertIsNone(proc.poll())

        proc.stdin.close()

        self.assertTrue(
            _wait_for(lambda: proc.poll() is not None),
            "child must exit by itself on stdin EOF",
        )

    def test_stop_terminates_child_without_orphans(self):
        repo = self._make_repo()
        repo.update_specific_checks([_rule("CssSyntax")])
        proc = repo.child_process
        assert proc is not None
        self.assertIsNone(proc.poll())

        repo.stop()
        self.assertTrue(_wait_for(lambda: proc.poll() is not None))

        # Idempotent
        repo.stop()

    def test_rule_print_goes_to_stderr_and_protocol_survives(self):
        stage = self.controller.create_stage("tasklet", "Bad", "bad_stage.py")
        stage.file_path.write_bytes(b"\x80\x81\xfe\xff")

        repo = self._make_repo(
            popen_factory=lambda: spawn_sidecar_process(stderr=subprocess.PIPE)
        )
        checks = repo.update_specific_checks([_rule("MainBlockInStage")])

        # The protocol must survive the rule's print(): a valid response with
        # the rule's check (the undecodable stage is printed about + skipped).
        names = {c.name for c in checks}
        self.assertIn("MainBlockInStage", names)

        proc = repo.child_process
        assert proc is not None and proc.stderr is not None
        repo.stop()
        self.assertTrue(_wait_for(lambda: proc.poll() is not None))
        stderr_output = proc.stderr.read()
        self.assertIn(b"Error while processing", stderr_output)


if __name__ == "__main__":
    unittest.main()
