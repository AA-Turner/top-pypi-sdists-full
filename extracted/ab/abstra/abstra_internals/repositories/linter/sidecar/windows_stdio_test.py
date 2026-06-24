"""Windows stdio framing smoke for the linter sidecar.

Regression guard for the Windows-only bug where the child's inherited pipe
stdio comes up in the MS C runtime's TEXT mode (O_TEXT), translating \\n<->\\r\\n
and silently corrupting the binary Content-Length framing (protocol.py). The
child would stay alive but mute and the editor's request only failed on its full
timeout (the customer's `blocking_checks_for_deploy timed out after 600s`). The
fix forces both protocol fds to binary in the child entrypoint (__main__.py).

These tests spawn the REAL child and exercise the framing end to end. They pass
trivially off Windows (no translation there) and are the actual guard on
Windows: without the fix the round trip never completes and the test fails on
the request timeout instead of returning checks. Run them on a Windows PC to
validate the fix:

    pytest abstra_internals/repositories/linter/sidecar/windows_stdio_test.py
"""

import os
import unittest
from unittest.mock import Mock

import pytest

from abstra_internals.repositories.factory import build_editor_repositories
from abstra_internals.repositories.linter.rules import rules as ALL_RULES
from abstra_internals.repositories.linter.sidecar.client import (
    SidecarLinterRepository,
)
from tests.fixtures import clear_dir, init_dir

# Real child boot imports the whole rule stack; signal method avoids the
# non-daemon timer thread that deadlocks BaseTest teardown (see lifecycle_test).
pytestmark = pytest.mark.timeout(120, method="signal")


def _rule(name):
    return next(r for r in ALL_RULES if r.name == name)


class SidecarWindowsStdioTest(unittest.TestCase):
    """Light fixture (init_dir, no BaseTest consumer/executor pool), with
    NewVersionOfAbstraAvailable kept out of the child's registry so the resync
    full pass never hits the network."""

    def setUp(self):
        self._old_bundled = os.environ.get("ABSTRA_RUNNING_IN_BUNDLED_APP")
        os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = "1"
        self.root = init_dir()
        self.repositories = build_editor_repositories()

    def tearDown(self):
        clear_dir(self.root)
        if self._old_bundled is None:
            os.environ.pop("ABSTRA_RUNNING_IN_BUNDLED_APP", None)
        else:
            os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = self._old_bundled

    def _make_repo(self):
        # A modest timeout so a regression FAILS FAST instead of hanging: on a
        # broken (text-mode) child the round trip never returns.
        repo = SidecarLinterRepository(
            request_timeout=60.0,
            backoff_schedule=[0.1, 0.1],
            is_web=False,
            exiter=Mock(),
        )
        self.addCleanup(repo.stop)
        return repo

    def test_round_trip_survives_stdio_framing(self):
        """A single framed request+response must cross the pipe intact. On
        Windows this only holds when the child set its fds to binary."""
        (self.root / "bad.css").write_text("body { : red; }")
        repo = self._make_repo()

        checks = repo.update_specific_checks([_rule("CssSyntax")])

        by_name = {c.name: c for c in checks}
        self.assertIn("CssSyntax", by_name)
        self.assertEqual(len(by_name["CssSyntax"].issues), 1)
        proc = repo.child_process
        assert proc is not None
        self.assertIsNone(proc.poll(), "child must still be alive after the round trip")

    def test_many_sequential_frames_stay_aligned(self):
        """Several requests over the SAME child. Newline translation corrupts
        the byte counts cumulatively, so frame N+1 would desync even if frame 1
        slipped through — catching corruption a single round trip might miss."""
        (self.root / "bad.css").write_text("body { : red; }")
        repo = self._make_repo()

        for i in range(8):
            checks = repo.update_specific_checks([_rule("CssSyntax")])
            by_name = {c.name: c for c in checks}
            self.assertIn("CssSyntax", by_name, f"frame {i} desynced")
            self.assertEqual(
                len(by_name["CssSyntax"].issues), 1, f"frame {i} payload wrong"
            )

        proc = repo.child_process
        assert proc is not None
        self.assertIsNone(proc.poll())


if __name__ == "__main__":
    unittest.main()
