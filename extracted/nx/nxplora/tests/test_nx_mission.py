"""NX autonomous missions ($mission) — pure client-helper tests (no network)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_mission as nm  # noqa: E402


class TestPayload(unittest.TestCase):
    def test_defaults_to_dry_run(self):
        p = nm.mission_payload("book 5 calls")
        self.assertEqual(p["mode"], "dry_run")
        self.assertEqual(p["goal"], "book 5 calls")
        self.assertEqual(p["source"], "nx_cli")
        self.assertNotIn("settings", p)

    def test_clamps_invalid_mode_to_dry_run(self):
        self.assertEqual(nm.mission_payload("g", mode="YOLO")["mode"], "dry_run")
        self.assertEqual(nm.mission_payload("g", mode="live")["mode"], "live")

    def test_includes_settings_and_model_when_given(self):
        p = nm.mission_payload("g", settings={"daily_cap": 20}, model_intent="gpt-5")
        self.assertEqual(p["settings"], {"daily_cap": 20})
        self.assertEqual(p["model_intent"], "gpt-5")

    def test_goal_is_capped_and_stripped(self):
        p = nm.mission_payload("  hi  ")
        self.assertEqual(p["goal"], "hi")
        self.assertLessEqual(len(nm.mission_payload("x" * 99999)["goal"]), 8000)


class TestParse(unittest.TestCase):
    def test_parse_mission_id(self):
        self.assertEqual(nm.parse_mission_id({"ok": True, "missionId": "m1"}), "m1")
        self.assertIsNone(nm.parse_mission_id({"ok": False, "missionId": "m1"}))
        self.assertIsNone(nm.parse_mission_id({"ok": True}))
        self.assertIsNone(nm.parse_mission_id(None))


class TestSummary(unittest.TestCase):
    def test_status_label_and_terminal(self):
        self.assertEqual(nm.status_label("awaiting_authorization"), "waiting for your OK to go live")
        self.assertTrue(nm.is_terminal("done"))
        self.assertTrue(nm.is_terminal("failed"))
        self.assertFalse(nm.is_terminal("running"))

    def test_summarize_none(self):
        self.assertEqual(nm.summarize_mission(None), "No mission found.")

    def test_summarize_tallies_and_awaiting_hint(self):
        row = {"status": "awaiting_authorization", "goal": "sell", "sends": 0, "drafts": 3, "refused": 1}
        out = nm.summarize_mission(row)
        self.assertIn("0 sent", out)
        self.assertIn("3 drafted", out)
        self.assertIn("1 left for you", out)
        self.assertIn("Authorize live", out)

    def test_summarize_done_shows_summary(self):
        row = {"status": "done", "goal": "sell", "sends": 5, "drafts": 0, "refused": 0, "summary": "booked 5 calls"}
        out = nm.summarize_mission(row)
        self.assertIn("done", out)
        self.assertIn("booked 5 calls", out)




class TestSchedule(unittest.TestCase):
    def test_schedule_payload_defaults(self):
        p = nm.schedule_payload("daily outreach")
        self.assertEqual(p["cadence"], "daily")
        self.assertEqual(p["mode"], "dry_run")
        self.assertEqual(p["goal"], "daily outreach")

    def test_schedule_payload_clamps(self):
        self.assertEqual(nm.schedule_payload("g", cadence="yearly")["cadence"], "daily")
        self.assertEqual(nm.schedule_payload("g", cadence="weekly", mode="live")["cadence"], "weekly")
        self.assertEqual(nm.schedule_payload("g", mode="YOLO")["mode"], "dry_run")

    def test_cadence_from_text(self):
        self.assertEqual(nm.cadence_from_text("every hour"), "hourly")
        self.assertEqual(nm.cadence_from_text("weekly please"), "weekly")
        self.assertEqual(nm.cadence_from_text("each day"), "daily")
        self.assertEqual(nm.cadence_from_text(""), "daily")

    def test_parse_schedule_id(self):
        self.assertEqual(nm.parse_schedule_id({"ok": True, "scheduleId": "s1"}), "s1")
        self.assertIsNone(nm.parse_schedule_id({"ok": False, "scheduleId": "s1"}))
        self.assertIsNone(nm.parse_schedule_id(None))

    def test_summarize_schedules(self):
        self.assertEqual(nm.summarize_schedules(None), "No recurring missions scheduled.")
        self.assertEqual(nm.summarize_schedules([]), "No recurring missions scheduled.")
        out = nm.summarize_schedules([{"goal": "outreach", "cadence": "daily", "mode": "dry_run", "enabled": True}])
        self.assertIn("outreach", out)
        self.assertIn("daily", out)
        self.assertIn("on", out)


if __name__ == "__main__":
    unittest.main()
