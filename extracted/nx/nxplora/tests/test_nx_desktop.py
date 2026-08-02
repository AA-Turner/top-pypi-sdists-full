"""
NX CLI — desktop agent (nx_desktop) unit tests. Proves the pure orchestration (poll → run → report, bounded, a
raising run reported 'failed' not lost) and the transport parsing — with NO network and NO Mac. The concrete HTTP
+ control_computer executor are deploy/device-proven.

Run: python3 tests/test_nx_desktop.py
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_desktop as nd  # noqa: E402


class TestMapReport(unittest.TestCase):
    def test_done(self):
        status, summary = nd.map_run_to_report("open notes", {"ok": True, "done": True, "steps": []})
        self.assertEqual(status, "done")
        self.assertIn("Goal: open notes", summary)

    def test_failed_on_not_ok_or_planner_error(self):
        self.assertEqual(nd.map_run_to_report("x", {"ok": False})[0], "failed")
        self.assertEqual(nd.map_run_to_report("x", {"ok": True, "halted": "planner_error"})[0], "failed")

    def test_prohibited_is_done_with_note(self):
        status, summary = nd.map_run_to_report("pay", {"ok": True, "halted": "prohibited", "steps": []})
        self.assertEqual(status, "done")  # an honest partial stop, not a failure
        self.assertIn("credential/payment", summary)


class TestOrchestration(unittest.TestCase):
    def test_empty_queue_runs_nothing(self):
        r = nd.run_desktop_missions(fetch_next=lambda: None, run_mission=lambda g: {"ok": True, "done": True}, report=lambda *a: True)
        self.assertEqual(r["ran"], 0)

    def test_runs_missions_until_queue_empty(self):
        missions = iter([{"mission_id": "m1", "goal": "a"}, {"mission_id": "m2", "goal": "b"}, None])
        reported = []
        r = nd.run_desktop_missions(
            fetch_next=lambda: next(missions),
            run_mission=lambda g: {"ok": True, "done": True, "steps": []},
            report=lambda mid, s, summ: reported.append((mid, s)) or True,
        )
        self.assertEqual(r["ran"], 2)
        self.assertEqual([x[0] for x in reported], ["m1", "m2"])
        self.assertTrue(all(x[1] == "done" for x in reported))

    def test_a_raising_run_is_reported_failed_not_lost(self):
        missions = iter([{"mission_id": "m1", "goal": "boom"}, None])
        reported = []
        def run(_g):
            raise RuntimeError("kaboom")
        r = nd.run_desktop_missions(fetch_next=lambda: next(missions), run_mission=run,
                                    report=lambda mid, s, summ: reported.append((mid, s)) or True)
        self.assertEqual(reported, [("m1", "failed")])  # the mission is reported failed, never silently dropped
        self.assertEqual(r["failed"], 1)

    def test_bounded_by_max_missions(self):
        # an endless queue is bounded so the agent can't loop forever
        r = nd.run_desktop_missions(fetch_next=lambda: {"mission_id": "m", "goal": "g"},
                                    run_mission=lambda g: {"ok": True, "done": True},
                                    report=lambda *a: True, max_missions=2)
        self.assertEqual(r["ran"], 2)


class TestTransport(unittest.TestCase):
    def test_fetch_next_parses_mission(self):
        with mock.patch.object(nd, "_http_post_json", return_value={"ok": True, "mission": {"missionId": "m9", "goal": "do it"}}):
            m = nd.nexplora_fetch_next("https://api.nexplora.ai", "tok", "MacBook")
            self.assertEqual(m, {"mission_id": "m9", "goal": "do it"})

    def test_fetch_next_none_on_empty_or_not_ok(self):
        with mock.patch.object(nd, "_http_post_json", return_value={"ok": True, "mission": None}):
            self.assertIsNone(nd.nexplora_fetch_next("b", "t", "a"))
        with mock.patch.object(nd, "_http_post_json", return_value={"ok": False}):
            self.assertIsNone(nd.nexplora_fetch_next("b", "t", "a"))
        with mock.patch.object(nd, "_http_post_json", return_value=None):
            self.assertIsNone(nd.nexplora_fetch_next("b", "t", "a"))

    def test_report_returns_ok(self):
        with mock.patch.object(nd, "_http_post_json", return_value={"ok": True}):
            self.assertTrue(nd.nexplora_report("b", "t", "m1", "done", "did it"))
        with mock.patch.object(nd, "_http_post_json", return_value=None):
            self.assertFalse(nd.nexplora_report("b", "t", "m1", "done", "did it"))

    def test_make_transport_binds(self):
        fetch, report = nd.make_transport("https://api.nexplora.ai", "tok", "MacBook")
        self.assertTrue(callable(fetch) and callable(report))


if __name__ == "__main__":
    unittest.main()
