"""Unit tests for nx_background — the non-blocking background command runner.

The safety gate + launcher are injectable, so these prove the decision logic (gate refusal, task
lifecycle, status transitions, tail read) WITHOUT depending on the CLI, plus one REAL detached run
to prove the end-to-end launch + poll on this machine.

Run: python3 -m unittest tests.test_background   (from nx/cli/)
"""
import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_background as bg


class _FakeProc:
    """A stand-in Popen: poll() returns None until `finish(rc)` is called."""
    def __init__(self, pid=4242):
        self.pid = pid
        self._rc = None

    def finish(self, rc):
        self._rc = rc

    def poll(self):
        return self._rc


class BackgroundGateTests(unittest.TestCase):
    def test_empty_command_refused(self):
        self.assertIn("error", bg.start_background("   "))

    def test_safety_gate_blocks_before_launch(self):
        launched = {"n": 0}

        def refuse(cmd):
            return "Refused: nope"

        def launcher(cmd, cwd, log):  # must NOT be called when the gate refuses
            launched["n"] += 1
            return _FakeProc()

        res = bg.start_background("rm -rf /", safety=refuse, launcher=launcher)
        self.assertEqual(res.get("error"), "Refused: nope")
        self.assertEqual(launched["n"], 0, "a refused command must never reach the launcher")

    def test_launch_returns_task_id_and_pid(self):
        proc = _FakeProc(pid=99)
        res = bg.start_background("sleep 1", safety=lambda c: None, launcher=lambda c, w, l: proc)
        self.assertTrue(res.get("started"))
        self.assertIn("task_id", res)
        self.assertEqual(res["pid"], 99)


class BackgroundLifecycleTests(unittest.TestCase):
    def test_status_running_then_done_then_failed(self):
        proc = _FakeProc()
        res = bg.start_background("long job", safety=lambda c: None, launcher=lambda c, w, l: proc)
        tid = res["task_id"]

        # running while poll() is None
        self.assertEqual(bg.poll(tid)["status"], "running")

        # exit 0 -> done
        proc.finish(0)
        p = bg.poll(tid)
        self.assertEqual(p["status"], "done")
        self.assertEqual(p["returncode"], 0)

        # a second task that fails
        proc2 = _FakeProc()
        res2 = bg.start_background("bad job", safety=lambda c: None, launcher=lambda c, w, l: proc2)
        proc2.finish(2)
        p2 = bg.poll(res2["task_id"])
        self.assertEqual(p2["status"], "failed")
        self.assertEqual(p2["returncode"], 2)

    def test_poll_unknown_task(self):
        self.assertIn("error", bg.poll("nope-not-a-task"))

    def test_list_tasks_reports_tracked(self):
        proc = _FakeProc()
        res = bg.start_background("echo hey", safety=lambda c: None, launcher=lambda c, w, l: proc)
        ids = [r["task_id"] for r in bg.list_tasks()]
        self.assertIn(res["task_id"], ids)


class BackgroundRealRunTest(unittest.TestCase):
    def test_real_detached_command_completes_and_output_is_read(self):
        # A REAL detached run (default launcher) — proves the Popen + log + poll path on this machine.
        res = bg.start_background("printf 'hello-bg'", safety=lambda c: None)
        self.assertTrue(res.get("started"), res)
        tid = res["task_id"]
        # Wait (bounded) for it to finish.
        for _ in range(50):
            p = bg.poll(tid)
            if p["status"] in ("done", "failed"):
                break
            time.sleep(0.1)
        p = bg.poll(tid)
        self.assertIn(p["status"], ("done", "failed"))
        self.assertEqual(p.get("returncode"), 0)
        self.assertIn("hello-bg", bg.read_output(tid)["output"])


if __name__ == "__main__":
    unittest.main()
