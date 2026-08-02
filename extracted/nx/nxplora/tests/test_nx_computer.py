"""
NX CLI — computer-use (nx_computer) unit tests.

Proves the SAFE-by-construction decision layer with no GUI: action parsing, the three-tier safety gate
(observe=SAFE / act=GATED / credential+payment=PROHIBITED), coordinate clamping, permission preflight + guidance,
and the control loop's gating (a GATED action needs confirm; a PROHIBITED action is refused; fail-closed headless).
The executor (screencapture/cliclick/osascript) is device-proven, not exercised here.

Run: python3 tests/test_nx_computer.py
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_computer as nc  # noqa: E402


# ── action parsing ──────────────────────────────────────────────────────────────────────────────────────────
class TestParse(unittest.TestCase):
    def test_click_coords_coerced(self):
        a = nc.parse_computer_action({"kind": "click", "x": "42", "y": 100, "target": "Save button"})
        self.assertEqual(a["kind"], "click")
        self.assertEqual((a["x"], a["y"]), (42, 100))
        self.assertEqual(a["target"], "Save button")

    def test_type_and_key_and_open(self):
        self.assertEqual(nc.parse_computer_action({"kind": "type", "text": "hello"})["text"], "hello")
        self.assertEqual(nc.parse_computer_action({"kind": "key", "combo": "cmd+s"})["keys"], "cmd+s")
        self.assertEqual(nc.parse_computer_action({"kind": "open_app", "app": "Safari"})["app"], "Safari")

    def test_unknown_kind_becomes_done(self):
        self.assertEqual(nc.parse_computer_action({"kind": "nuke_everything"})["kind"], "done")
        self.assertEqual(nc.parse_computer_action("not a dict")["kind"], "done")

    def test_parse_plan_action_extracts_json(self):
        ans = 'Sure, I will click Save.\n{"kind":"click","x":10,"y":20,"target":"Save"}\nDone.'
        a = nc.parse_plan_action(ans)
        self.assertEqual(a["kind"], "click")
        self.assertEqual(a["x"], 10)

    def test_parse_plan_action_no_json_is_done(self):
        self.assertEqual(nc.parse_plan_action("just prose, no json")["kind"], "done")
        self.assertEqual(nc.parse_plan_action("")["kind"], "done")


# ── safety gate ─────────────────────────────────────────────────────────────────────────────────────────────
class TestGate(unittest.TestCase):
    def test_observe_actions_are_safe(self):
        for k in ("screenshot", "move", "scroll", "wait", "done"):
            self.assertEqual(nc.classify_computer_action({"kind": k}), "SAFE", k)

    def test_real_actions_are_gated(self):
        for k in ("click", "double_click", "right_click", "drag", "type", "key", "open_app"):
            self.assertEqual(nc.classify_computer_action({"kind": k, "target": "a button"}), "GATED", k)

    def test_credentials_and_payment_are_prohibited(self):
        self.assertEqual(nc.classify_computer_action({"kind": "type", "text": "hunter2", "target": "password field"}), "PROHIBITED")
        self.assertEqual(nc.classify_computer_action({"kind": "click", "target": "Confirm payment"}), "PROHIBITED")
        self.assertEqual(nc.classify_computer_action({"kind": "click", "target": "Place order"}), "PROHIBITED")
        self.assertEqual(nc.classify_computer_action({"kind": "type", "text": "4111 1111 1111 1111", "why": "enter card number"}), "PROHIBITED")

    def test_prohibited_beats_observe_when_sensitive(self):
        # even a 'move' toward a credential context is treated as prohibited (defense-in-depth on the haystack)
        self.assertEqual(nc.classify_computer_action({"kind": "move", "target": "seed phrase box"}), "PROHIBITED")

    def test_describe_action_hides_full_typed_text(self):
        d = nc.describe_action({"kind": "type", "text": "x" * 100})
        self.assertIn("…", d)
        self.assertLess(len(d), 60)


# ── coordinate bounds ───────────────────────────────────────────────────────────────────────────────────────
class TestBounds(unittest.TestCase):
    def test_clamps_into_screen(self):
        self.assertEqual(nc.validate_point(5000, -3, 1440, 900), (1439, 0))
        self.assertEqual(nc.validate_point(100, 200, 1440, 900), (100, 200))

    def test_non_numeric_is_none(self):
        self.assertIsNone(nc.validate_point("abc", 10, 1440, 900))


# ── capability + permission preflight ───────────────────────────────────────────────────────────────────────
class TestPreflight(unittest.TestCase):
    def test_non_macos_is_not_ready_with_guidance(self):
        with mock.patch.object(nc, "detect_executor", return_value={"os": "Linux", "macos": False, "screenshot": False, "click": False, "backend": None}):
            pf = nc.preflight()
            self.assertFalse(pf["ready"])
            self.assertEqual(pf["reason"], "unsupported_os")
            self.assertIn("macOS", pf["guidance"])

    def test_macos_without_tools_guides_grants(self):
        cap = {"os": "Darwin", "macos": True, "screenshot": False, "click": False, "backend": None}
        g = nc.permission_guidance(cap)
        self.assertIn("Accessibility", g)
        self.assertIn("Screen", g)

    def test_ready_when_mac_has_tools(self):
        with mock.patch.object(nc, "detect_executor", return_value={"os": "Darwin", "macos": True, "screenshot": True, "click": True, "backend": "cliclick"}):
            self.assertTrue(nc.preflight()["ready"])


# ── one-click permission remediation (open the exact pane + pop macOS's own grant dialog) ───────────────────
class TestRemediation(unittest.TestCase):
    def test_privacy_pane_urls_are_the_exact_panes(self):
        self.assertIn("Privacy_Accessibility", nc.PRIVACY_PANE_URLS["accessibility"])
        self.assertIn("Privacy_ScreenCapture", nc.PRIVACY_PANE_URLS["screen_recording"])

    def test_open_privacy_pane_calls_open_with_the_deep_link(self):
        calls = []
        with mock.patch.object(nc, "is_macos", return_value=True), \
             mock.patch.object(nc, "_run", side_effect=lambda cmd, timeout=8: calls.append(cmd) or {"ok": True}):
            r = nc.open_privacy_pane("accessibility")
            self.assertTrue(r["ok"])
            self.assertEqual(calls[0][0], "open")
            self.assertIn("Privacy_Accessibility", calls[0][1])

    def test_accessibility_granted_reads_the_denial(self):
        with mock.patch.object(nc, "is_macos", return_value=True), \
             mock.patch.object(nc.shutil, "which", return_value="/usr/bin/osascript"):
            with mock.patch.object(nc, "_run", return_value={"ok": False, "stderr": "osascript is not allowed assistive access. (-1719)"}):
                self.assertIs(nc.accessibility_granted(), False)
            with mock.patch.object(nc, "_run", return_value={"ok": True, "stdout": "Finder"}):
                self.assertIs(nc.accessibility_granted(), True)

    def test_install_cliclick_returns_the_one_command(self):
        with mock.patch.object(nc.shutil, "which", side_effect=lambda x: None if x == "cliclick" else "/opt/homebrew/bin/brew"):
            r = nc.install_cliclick(run=False)
            self.assertEqual(r["cmd"], ["brew", "install", "cliclick"])
            self.assertFalse(r["installed"])
        with mock.patch.object(nc.shutil, "which", return_value=None):  # no brew
            r = nc.install_cliclick(run=False)
            self.assertEqual(r["error"], "no_brew")

    def test_remediate_opens_panes_and_offers_cliclick(self):
        opened = []
        cap = {"os": "Darwin", "macos": True, "screenshot": True, "click": False, "backend": None}
        with mock.patch.object(nc, "open_privacy_pane", side_effect=lambda w: opened.append(w) or {"ok": True, "which": w}), \
             mock.patch.object(nc, "trigger_permission_prompts", return_value={"screen_recording": True, "accessibility": True}), \
             mock.patch.object(nc, "install_cliclick", return_value={"ok": True, "cmd": ["brew", "install", "cliclick"], "installed": False}):
            r = nc.remediate_permissions(cap=cap)
            self.assertEqual(set(r["opened"]), {"accessibility", "screen_recording"})
            self.assertTrue(r["prompted"]["accessibility"])
            self.assertIsNotNone(r["cliclick"])  # backend missing → offered


# ── bundled precise-control backend (pynput — ships with nx, no Homebrew) ───────────────────────────────────
class TestPynputBackend(unittest.TestCase):
    def test_detect_prefers_pynput_when_available(self):
        with mock.patch.object(nc, "_pynput_available", return_value=True), \
             mock.patch.object(nc.shutil, "which", return_value="/x"):  # cliclick + osascript also present
            self.assertEqual(nc.detect_executor()["backend"], "pynput")

    def test_execute_action_routes_to_pynput(self):
        with mock.patch.object(nc, "detect_executor",
                               return_value={"macos": True, "backend": "pynput", "click": True, "screenshot": True}), \
             mock.patch.object(nc, "_execute_pynput", return_value={"ok": True}) as m:
            self.assertTrue(nc.execute_action({"kind": "click", "x": 10, "y": 20})["ok"])
            m.assert_called_once()

    def test_execute_pynput_click_and_type_via_fake_module(self):
        import sys, types
        calls = []

        class _B:
            left = "L"; right = "R"

        class _MC:
            def __init__(self): self.position = (0, 0)
            def click(self, b, n): calls.append(("click", b, n))
            def press(self, b): calls.append(("press", b))
            def release(self, b): calls.append(("release", b))
            def scroll(self, dx, dy): calls.append(("scroll", dx, dy))

        class _KC:
            def type(self, t): calls.append(("type", t))

        fake_mouse = types.ModuleType("pynput.mouse"); fake_mouse.Controller = _MC; fake_mouse.Button = _B
        fake_kbd = types.ModuleType("pynput.keyboard"); fake_kbd.Controller = _KC; fake_kbd.Key = type("K", (), {})
        fake_pkg = types.ModuleType("pynput"); fake_pkg.mouse = fake_mouse; fake_pkg.keyboard = fake_kbd
        with mock.patch.dict(sys.modules, {"pynput": fake_pkg, "pynput.mouse": fake_mouse, "pynput.keyboard": fake_kbd}):
            self.assertTrue(nc._execute_pynput({"kind": "click", "x": 5, "y": 6})["ok"])
            self.assertTrue(nc._execute_pynput({"kind": "type", "text": "hi"})["ok"])
        self.assertIn(("click", "L", 1), calls)
        self.assertIn(("type", "hi"), calls)


# ── the control loop's gating (executor mocked; no GUI) ─────────────────────────────────────────────────────
class TestControlLoop(unittest.TestCase):
    def _ready(self):
        return mock.patch.object(nc, "preflight", return_value={"ready": True})

    def test_unavailable_short_circuits_with_guidance(self):
        with mock.patch.object(nc, "preflight", return_value={"ready": False, "reason": "unsupported_os", "guidance": "grant..."}):
            r = nc.control_computer("do a thing", planner=lambda g, o: "{}")
            self.assertFalse(r["ok"])
            self.assertEqual(r["halted"], "unsupported_os")
            self.assertIn("guidance", r)

    def test_prohibited_action_is_refused_never_executed(self):
        with self._ready(), mock.patch.object(nc, "take_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(nc, "execute_action") as ex:
            r = nc.control_computer("log in", planner=lambda g, o: '{"kind":"type","text":"pw","target":"password"}', confirm=lambda d: True)
            ex.assert_not_called()  # a PROHIBITED action never reaches the executor
            self.assertEqual(r["halted"], "prohibited")

    def test_gated_action_without_confirm_is_declined_fail_closed(self):
        with self._ready(), mock.patch.object(nc, "take_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(nc, "execute_action") as ex:
            r = nc.control_computer("click save", planner=lambda g, o: '{"kind":"click","x":1,"y":2,"target":"Save"}')  # no confirm ⇒ fail closed
            ex.assert_not_called()
            self.assertEqual(r["halted"], "declined")

    def test_gated_action_with_confirm_executes_then_done(self):
        answers = ['{"kind":"click","x":1,"y":2,"target":"Save"}', '{"kind":"done","why":"saved"}']
        it = iter(answers)
        with self._ready(), mock.patch.object(nc, "take_screenshot", return_value={"ok": True, "path": "/tmp/x.png"}), \
             mock.patch.object(nc, "execute_action", return_value={"ok": True}) as ex:
            r = nc.control_computer("click save", planner=lambda g, o: next(it), confirm=lambda d: True)
            self.assertTrue(ex.called)
            self.assertTrue(r["done"])
            self.assertEqual(r["steps"][0]["executed"], True)


# ── planner (text observation → action, model injected) ─────────────────────────────────────────────────────
class TestPlanner(unittest.TestCase):
    def test_plan_next_action_builds_prompt_and_parses(self):
        captured = {}
        def fake_model(prompt):
            captured["prompt"] = prompt
            return '{"kind":"open_app","app":"Safari","why":"start"}'
        obs = {"screenshot_ok": True, "context": {"app": "Finder", "window": "Downloads"},
               "history": [{"action": {"kind": "click", "target": "X"}, "executed": True}]}
        a = nc.plan_next_action("open safari", obs, fake_model)
        self.assertEqual(a["kind"], "open_app")
        self.assertEqual(a["app"], "Safari")
        self.assertIn("GOAL: open safari", captured["prompt"])
        self.assertIn("app=Finder", captured["prompt"])
        self.assertIn("What you've done", captured["prompt"])  # history included

    def test_plan_next_action_model_error_is_done(self):
        def boom(_):
            raise RuntimeError("model down")
        self.assertEqual(nc.plan_next_action("x", {}, boom)["kind"], "done")

    def test_observe_context_empty_off_mac(self):
        with mock.patch.object(nc, "is_macos", return_value=False):
            self.assertEqual(nc.observe_context(), {})


if __name__ == "__main__":
    unittest.main()
