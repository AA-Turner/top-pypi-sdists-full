"""
NX CLI — phone control bridge (nx_phone) unit tests.

Proves the pure layer with no device: action parsing, the REUSED safety gate (tap/swipe/type/key/open_app GATED,
observe SAFE, credential/payment CONTEXT PROHIBITED — and honestly, a bare card number with NO context word →
GATED, because the gate is word-based not PAN-digit-based), adb-command mapping (always `-s <id>` pinned), keyevent
+ text escaping, device parsing/selection, preflight, and the control loop's gating. Executor (adb/simctl) is
device-proven, not exercised here.

Run: python3 tests/test_nx_phone.py
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_phone as ph  # noqa: E402


# ── action parsing ──────────────────────────────────────────────────────────────────────────────────────────
class TestParse(unittest.TestCase):
    def test_tap_and_swipe_coords(self):
        a = ph.parse_phone_action({"kind": "tap", "x": "40", "y": 90, "target": "search box"})
        self.assertEqual((a["x"], a["y"]), (40, 90))
        s = ph.parse_phone_action({"kind": "swipe", "x": 1, "y": 2, "to_x": 3, "to_y": 4})
        self.assertEqual((s["x"], s["y"], s["to_x"], s["to_y"]), (1, 2, 3, 4))

    def test_type_key_open(self):
        self.assertEqual(ph.parse_phone_action({"kind": "type", "text": "hi"})["text"], "hi")
        self.assertEqual(ph.parse_phone_action({"kind": "key", "keys": "back"})["keys"], "back")
        self.assertEqual(ph.parse_phone_action({"kind": "open_app", "app": "Chrome"})["app"], "Chrome")

    def test_unknown_becomes_done(self):
        self.assertEqual(ph.parse_phone_action({"kind": "factory_reset"})["kind"], "done")
        self.assertEqual(ph.parse_phone_action("nope")["kind"], "done")

    def test_parse_plan_phone_action_from_answer(self):
        a = ph.parse_plan_phone_action('ok: {"kind":"tap","x":5,"y":6,"target":"ok btn"}')
        self.assertEqual(a["kind"], "tap")
        self.assertEqual((a["x"], a["y"]), (5, 6))


# ── the REUSED safety gate ──────────────────────────────────────────────────────────────────────────────────
class TestGate(unittest.TestCase):
    def test_observe_safe_acts_gated(self):
        for k in ("screenshot", "wait", "done"):
            self.assertEqual(ph.classify_phone_action({"kind": k}), "SAFE", k)
        for k in ("tap", "swipe", "type", "key", "open_app"):
            self.assertEqual(ph.classify_phone_action({"kind": k, "target": "a button"}), "GATED", k)

    def test_credential_and_payment_context_prohibited(self):
        self.assertEqual(ph.classify_phone_action({"kind": "type", "text": "x", "target": "password field"}), "PROHIBITED")
        self.assertEqual(ph.classify_phone_action({"kind": "tap", "target": "Confirm payment"}), "PROHIBITED")
        self.assertEqual(ph.classify_phone_action({"kind": "tap", "target": "Place order"}), "PROHIBITED")
        self.assertEqual(ph.classify_phone_action({"kind": "type", "text": "4111 1111 1111 1111", "why": "enter card number"}), "PROHIBITED")

    def test_bare_card_number_without_context_is_gated_not_prohibited(self):
        # HONEST: the gate is WORD-based (matches 'card number'/'payment'/'otp'/…), not raw-PAN digit detection.
        # A bare number with no context word lands GATED — per-op confirm, fail-closed headless — not PROHIBITED.
        self.assertEqual(ph.classify_phone_action({"kind": "type", "text": "4111 1111 1111 1111"}), "GATED")


# ── adb command mapping (always -s pinned) ──────────────────────────────────────────────────────────────────
class TestAdbCommand(unittest.TestCase):
    def test_every_command_pins_device(self):
        for a in ({"kind": "tap", "x": 1, "y": 2}, {"kind": "type", "text": "hi"},
                  {"kind": "key", "keys": "back"}, {"kind": "screenshot"}):
            argv = ph.adb_command(a, "emulator-5554")
            self.assertEqual(argv[:3], ["adb", "-s", "emulator-5554"], a)

    def test_tap_swipe_type_key_shapes(self):
        self.assertEqual(ph.adb_command({"kind": "tap", "x": 10, "y": 20}, "D")[3:], ["shell", "input", "tap", "10", "20"])
        self.assertEqual(ph.adb_command({"kind": "swipe", "x": 1, "y": 2, "to_x": 3, "to_y": 4, "ms": 250}, "D")[3:],
                         ["shell", "input", "swipe", "1", "2", "3", "4", "250"])
        self.assertEqual(ph.adb_command({"kind": "key", "keys": "back"}, "D")[3:], ["shell", "input", "keyevent", "KEYCODE_BACK"])

    def test_open_app_resolves_package_or_empty(self):
        self.assertIn("com.android.chrome", ph.adb_command({"kind": "open_app", "app": "Chrome"}, "D"))
        self.assertEqual(ph.adb_command({"kind": "open_app", "app": "SomeUnknownApp"}, "D"), [])  # unresolved → empty
        self.assertIn("com.foo.bar", ph.adb_command({"kind": "open_app", "app": "com.foo.bar"}, "D"))  # dotted → passthrough


class TestKeyAndText(unittest.TestCase):
    def test_keyevent_map(self):
        self.assertEqual(ph.android_keyevent("enter"), "KEYCODE_ENTER")
        self.assertEqual(ph.android_keyevent("back"), "KEYCODE_BACK")
        self.assertEqual(ph.android_keyevent("KEYCODE_HOME"), "KEYCODE_HOME")

    def test_text_escape(self):
        self.assertEqual(ph.android_text_escape("hello world"), "hello%sworld")
        esc = ph.android_text_escape("a;b&c")
        self.assertIn("\\;", esc)
        self.assertIn("\\&", esc)


# ── device parsing + selection + preflight ──────────────────────────────────────────────────────────────────
class TestDetect(unittest.TestCase):
    def test_parse_adb_devices_online_only(self):
        out = "List of devices attached\nemulator-5554\tdevice\nZZZ\toffline\nWWW\tunauthorized\n"
        devs = ph.parse_adb_devices(out)
        self.assertEqual([d["id"] for d in devs], ["emulator-5554"])

    def test_parse_simctl_booted(self):
        js = '{"devices":{"iOS 17":[{"udid":"ABC","name":"iPhone 15","state":"Booted"},{"udid":"D","name":"x","state":"Shutdown"}]}}'
        devs = ph.parse_simctl_booted(js)
        self.assertEqual(len(devs), 1)
        self.assertEqual(devs[0]["kind"], "ios_sim")

    def test_select_device(self):
        one = [{"id": "a", "name": "A", "kind": "android"}]
        two = one + [{"id": "b", "name": "B", "kind": "android"}]
        self.assertEqual(ph.select_device(one)["id"], "a")
        self.assertIsNone(ph.select_device(two))          # ambiguous
        self.assertEqual(ph.select_device(two, "b")["id"], "b")  # prefer wins
        self.assertIsNone(ph.select_device([]))

    def test_preflight_states(self):
        with mock.patch.object(ph, "is_android_available", return_value=False), mock.patch.object(ph, "is_ios_sim_available", return_value=False):
            self.assertEqual(ph.phone_preflight(devices=[])["reason"], "no_tooling")
        with mock.patch.object(ph, "is_android_available", return_value=True), mock.patch.object(ph, "is_ios_sim_available", return_value=False):
            self.assertEqual(ph.phone_preflight(devices=[])["reason"], "no_device")
            self.assertTrue(ph.phone_preflight(devices=[{"id": "a", "name": "A", "kind": "android"}])["ready"])
            self.assertEqual(ph.phone_preflight(devices=[{"id": "s", "kind": "ios_sim", "name": "sim"}])["reason"], "ios_input_unsupported")


# ── control loop gating (executor mocked) ───────────────────────────────────────────────────────────────────
class TestControlLoop(unittest.TestCase):
    _DEV = {"id": "emulator-5554", "kind": "android", "name": "Pixel"}

    def _ready(self):
        return mock.patch.object(ph, "phone_preflight", return_value={"ready": True, "device": self._DEV})

    def test_unavailable_short_circuits(self):
        with mock.patch.object(ph, "phone_preflight", return_value={"ready": False, "reason": "no_device", "guidance": "connect"}):
            r = ph.control_phone("do it", planner=lambda g, o: "{}", device=self._DEV)
            self.assertFalse(r["ok"])
            self.assertEqual(r["halted"], "no_device")

    def test_prohibited_never_executes(self):
        with self._ready(), mock.patch.object(ph, "take_phone_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(ph, "observe_phone_context", return_value={}), mock.patch.object(ph, "execute_phone_action") as ex:
            r = ph.control_phone("pay", planner=lambda g, o: '{"kind":"tap","target":"Confirm payment"}', confirm=lambda d: True, device=self._DEV)
            ex.assert_not_called()
            self.assertEqual(r["halted"], "prohibited")

    def test_gated_without_confirm_declined_fail_closed(self):
        with self._ready(), mock.patch.object(ph, "take_phone_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(ph, "observe_phone_context", return_value={}), mock.patch.object(ph, "execute_phone_action") as ex:
            r = ph.control_phone("tap", planner=lambda g, o: '{"kind":"tap","x":1,"y":2,"target":"Save"}', device=self._DEV)
            ex.assert_not_called()
            self.assertEqual(r["halted"], "declined")

    def test_gated_with_confirm_executes_then_done(self):
        answers = iter(['{"kind":"tap","x":1,"y":2,"target":"Save"}', '{"kind":"done","why":"saved"}'])
        with self._ready(), mock.patch.object(ph, "take_phone_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(ph, "observe_phone_context", return_value={}), mock.patch.object(ph, "execute_phone_action", return_value={"ok": True}) as ex:
            r = ph.control_phone("tap save", planner=lambda g, o: next(answers), confirm=lambda d: True, device=self._DEV)
            self.assertTrue(ex.called)
            self.assertTrue(r["done"])


class TestPlanner(unittest.TestCase):
    def test_plan_next_phone_action(self):
        cap = {}
        def fake(prompt):
            cap["p"] = prompt
            return '{"kind":"open_app","app":"Chrome"}'
        a = ph.plan_next_phone_action("open chrome", {"context": {"activity": "com.android.launcher"}, "history": []}, fake)
        self.assertEqual(a["kind"], "open_app")
        self.assertIn("GOAL: open chrome", cap["p"])
        self.assertIn("com.android.launcher", cap["p"])

    def test_planner_model_error_is_done(self):
        def boom(_):
            raise RuntimeError("down")
        self.assertEqual(ph.plan_next_phone_action("x", {}, boom)["kind"], "done")


if __name__ == "__main__":
    unittest.main()
