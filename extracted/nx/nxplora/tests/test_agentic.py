"""
Tests for agentic execution mode:
- execution canvas
- approve/reject gate
- self-edit parsing and application
- integration auto-detection
"""

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_canvas
import nx_autoconnect
import nx_executor


class TestNXCanvas(unittest.TestCase):
    def test_canvas_tracks_steps(self):
        canvas = nx_canvas.NXCanvas("Test task")
        canvas.steps.append({"label": "Step 1", "status": "done", "time": "1s"})
        self.assertEqual(len(canvas.steps), 1)
        self.assertEqual(canvas.task, "Test task")


class TestApproveGate(unittest.TestCase):
    def test_approve_returns_true(self):
        with mock.patch("builtins.input", return_value="a"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "")

    def test_approve_all_returns_session_flag(self):
        with mock.patch("builtins.input", return_value="aa"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "session_approve_all")

    def test_reject_returns_false(self):
        with mock.patch("builtins.input", return_value="r"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertFalse(approved)
        self.assertEqual(reason, "")

    def test_reject_with_reason_returns_reason(self):
        with mock.patch("builtins.input", side_effect=["rr", "wrong approach"]):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertFalse(approved)
        self.assertEqual(reason, "wrong approach")

    def test_arrow_key_approve(self):
        with mock.patch.object(nx_canvas.Application, "run", return_value="approve"):
            with mock.patch("sys.stdin.isatty", return_value=True), \
                 mock.patch("sys.stdout.isatty", return_value=True):
                approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "")

    def test_arrow_key_approve_all(self):
        with mock.patch.object(nx_canvas.Application, "run", return_value="approve_all"):
            with mock.patch("sys.stdin.isatty", return_value=True), \
                 mock.patch("sys.stdout.isatty", return_value=True):
                approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "session_approve_all")

    def test_arrow_key_reject(self):
        with mock.patch.object(nx_canvas.Application, "run", return_value="reject"):
            with mock.patch("sys.stdin.isatty", return_value=True), \
                 mock.patch("sys.stdout.isatty", return_value=True):
                approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertFalse(approved)
        self.assertEqual(reason, "")

    def test_codespace_clean_tty_uses_arrow_keys(self):
        # A VS Code / Codespace terminal that IS a clean tty now gets the ARROW-KEY gate
        # (↑↓ + Enter), not the forced typed fallback. Proven by the arrow-key
        # Application.run being the thing that decides the result.
        with mock.patch.dict(os.environ, {"CODESPACES": "true", "TERM_PROGRAM": "vscode"}), \
             mock.patch("sys.stdin.isatty", return_value=True), \
             mock.patch("sys.stdout.isatty", return_value=True), \
             mock.patch.object(nx_canvas.Application, "run", return_value="approve"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "")

    def test_non_tty_still_uses_plain_gate(self):
        # No tty (pipe / test / CI) still uses the typed fallback — arrow-key app must not run.
        def _must_not_run(*a, **k):
            raise AssertionError("arrow-key app must not run without a tty")
        with mock.patch("sys.stdin.isatty", return_value=False), \
             mock.patch("sys.stdout.isatty", return_value=False), \
             mock.patch.object(nx_canvas.Application, "run", side_effect=_must_not_run), \
             mock.patch("builtins.input", return_value="1"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)

    def test_arrow_key_none_result_falls_back_not_blocked(self):
        # THE bug Victor hit: in a browser Codespace the arrow-key app returns None even
        # after the operator hits Enter on Approve. That must fall back to the plain gate
        # (so the approval registers), NEVER silently return blocked/not-approved.
        _clear = {k: "" for k in ("TERM_PROGRAM", "VSCODE_INJECTION", "VSCODE_PID",
                                  "VSCODE_IPC_HOOK_CLI", "VSCODE_GIT_IPC_HANDLE",
                                  "REMOTE_CONTAINERS", "CODESPACES", "CODESPACE_NAME",
                                  "GITHUB_CODESPACES", "GITHUB_CODESPACE_TOKEN",
                                  "NX_APPROVE_GATE_FALLBACK")}
        _clear["HOSTNAME"] = "localbox"
        with mock.patch.dict(os.environ, _clear), \
             mock.patch.object(nx_canvas.Application, "run", return_value=None), \
             mock.patch("sys.stdin.isatty", return_value=True), \
             mock.patch("sys.stdout.isatty", return_value=True), \
             mock.patch("builtins.input", return_value="a"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved, "None from the arrow-key app must fall back, not block")
        self.assertEqual(reason, "")

    def test_fallback_bare_enter_reprompts_then_approves(self):
        # THE bug: the plain gate printed "↑↓ Select / Enter Confirm" then read a typed
        # line, so the operator pressed Enter on nothing -> input()="" -> blocked though
        # they meant Approve. A bare Enter must RE-PROMPT; then "a" approves.
        with mock.patch("builtins.input", side_effect=["", "", "a"]):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved, "bare Enter must re-prompt, not silently block")
        self.assertEqual(reason, "")

    def test_fallback_all_empty_fails_closed(self):
        # Repeated empty input must NOT spin forever and must fail CLOSED (not approve).
        with mock.patch("builtins.input", side_effect=[""] * 8):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertFalse(approved)

    def test_fallback_number_1_approves(self):
        # Numbers match the menu: 1 = Approve.
        with mock.patch("builtins.input", return_value="1"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "")

    def test_fallback_number_2_approves_all(self):
        # 2 = Approve all (this session).
        with mock.patch("builtins.input", return_value="2"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertTrue(approved)
        self.assertEqual(reason, "session_approve_all")

    def test_fallback_number_3_rejects(self):
        # 3 = Reject.
        with mock.patch("builtins.input", return_value="3"):
            approved, reason = nx_canvas.approve_gate("summary", [])
        self.assertFalse(approved)


class TestSelfEdit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.py"
        self.path.write_text("def old():\n    pass\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_self_edit_replaces_code(self):
        result = nx_executor.self_edit(
            str(self.path),
            "def old():\n    pass\n",
            "def new():\n    return 1\n",
        )
        self.assertTrue(result.get("success"))
        self.assertIn("new", self.path.read_text())

    def test_self_edit_fails_when_old_code_missing(self):
        result = nx_executor.self_edit(str(self.path), "nonexistent", "replacement")
        self.assertFalse(result.get("success"))
        self.assertIn("not found", result.get("error", "").lower())


class TestParseFileEdits(unittest.TestCase):
    def test_parse_single_edit(self):
        response = (
            "Here's the fix:\n"
            "```file: nx_cli.py\n"
            "# old_code\n"
            "old line\n"
            "# new_code\n"
            "new line\n"
            "```"
        )
        edits = nx_executor.parse_file_edits(response)
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0]["file"], "nx_cli.py")
        self.assertEqual(edits[0]["old_code"], "old line")
        self.assertEqual(edits[0]["new_code"], "new line")

    def test_parse_multiple_edits(self):
        response = (
            "```file: a.py\n# old_code\na\n# new_code\nb\n```\n"
            "```file: b.py\n# old_code\nc\n# new_code\nd\n```"
        )
        edits = nx_executor.parse_file_edits(response)
        self.assertEqual(len(edits), 2)

    def test_parse_no_edits(self):
        self.assertEqual(nx_executor.parse_file_edits("No edits here"), [])

    def test_parse_rejects_relative_path_hallucination(self):
        response = (
            "```file: relative/path/to/file.py\n"
            "# old_code\nold\n# new_code\nnew\n```"
        )
        self.assertEqual(nx_executor.parse_file_edits(response), [])

    def test_parse_rejects_unsupported_extension(self):
        response = (
            "```file: config.exe\n"
            "# old_code\nold\n# new_code\nnew\n```"
        )
        self.assertEqual(nx_executor.parse_file_edits(response), [])

    def test_parse_accepts_supported_extensions(self):
        for ext in (".py", ".json", ".md", ".txt", ".yaml", ".sh", ".toml"):
            response = (
                f"```file: file{ext}\n"
                f"# old_code\nold\n# new_code\nnew\n```"
            )
            edits = nx_executor.parse_file_edits(response)
            self.assertEqual(len(edits), 1, f"extension {ext} should be accepted")
            self.assertEqual(edits[0]["file"], f"file{ext}")


class TestApplyFileEdits(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "nx_cli.py").write_text("old line\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_apply_edits(self):
        edits = [{"file": "nx_cli.py", "old_code": "old line", "new_code": "new line"}]
        results = nx_executor.apply_file_edits(edits, source_dir=str(self.base))
        self.assertTrue(results[0].get("success"))
        self.assertIn("new line", (self.base / "nx_cli.py").read_text())


class TestIntegrationDetection(unittest.TestCase):
    def test_detect_shopify(self):
        needed = nx_autoconnect.detect_needed_integrations("analyze my shopify store")
        self.assertIn("shopify", needed)

    def test_detect_github(self):
        needed = nx_autoconnect.detect_needed_integrations("open a pull request on github")
        self.assertIn("github", needed)

    def test_detect_multiple(self):
        needed = nx_autoconnect.detect_needed_integrations("sync shopify orders to slack")
        self.assertIn("shopify", needed)
        self.assertIn("slack", needed)

    def test_no_integrations(self):
        needed = nx_autoconnect.detect_needed_integrations("hello world")
        self.assertEqual(needed, [])


class TestAgenticTaskDetection(unittest.TestCase):
    def test_detects_fix(self):
        from nx_cli import is_agentic_code_task
        self.assertTrue(is_agentic_code_task("fix the /world bug"))

    def test_detects_edit(self):
        from nx_cli import is_agentic_code_task
        self.assertTrue(is_agentic_code_task("edit nx_cli.py"))

    def test_ignores_chat(self):
        from nx_cli import is_agentic_code_task
        self.assertFalse(is_agentic_code_task("tell me about paris"))

    def test_detects_add(self):
        from nx_cli import is_agentic_code_task
        self.assertTrue(is_agentic_code_task("add a separator line"))


if __name__ == "__main__":
    unittest.main()
