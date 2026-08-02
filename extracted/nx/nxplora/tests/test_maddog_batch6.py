"""Maddog batch 6 — local shell as a native tool (NX deploys like Claude Code).

NX can now run local CLIs (deploy/build/git) itself via a native run_command tool —
e.g. `vercel --prod --yes` to ship a project — instead of the remote MCP that can't
upload local code. EVERY command stays behind the approval gate (fails closed).

These tests prove the wiring + the gate WITHOUT running any real command (run_command
is mocked) — no deploys, no shell side effects.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli as N        # noqa: E402
import nx_mcp_tools as T  # noqa: E402


class ShellToolSchema(unittest.TestCase):
    def test_run_command_tool_shape(self):
        fn = N._RUN_CMD_TOOL["function"]
        self.assertEqual(N._RUN_CMD_TOOL["type"], "function")
        self.assertEqual(fn["name"], "run_command")
        self.assertIn("command", fn["parameters"]["properties"])
        self.assertIn("command", fn["parameters"]["required"])
        self.assertIn("vercel", fn["description"].lower())   # documents the deploy use


class ApprovalGate(unittest.TestCase):
    def test_fails_closed_without_approval(self):
        # approver says NO → run_command must NOT execute, result is blocked.
        with mock.patch.object(N, "run_command") as rc:
            res, _ = N._handle_run_command("vercel --prod --yes", lambda cmd: False, {})
        rc.assert_not_called()
        self.assertFalse(res["success"])
        self.assertTrue(res.get("blocked"))

    def test_runs_when_approved(self):
        # approver says YES → run_command executes with the exact cmd, output returned.
        with mock.patch.object(N, "run_command",
                               return_value={"stdout": "Vercel CLI 54.11.1", "stderr": "", "success": True}) as rc:
            res, _ = N._handle_run_command("vercel --version", lambda cmd: True, {})
        rc.assert_called_once()
        self.assertEqual(rc.call_args[0][0], "vercel --version")
        self.assertTrue(res["success"])
        self.assertIn("54.11.1", res["output"])

    def test_no_approver_fails_closed(self):
        with mock.patch.object(N, "run_command") as rc:
            res, _ = N._handle_run_command("rm -rf /", None, {})
        rc.assert_not_called()
        self.assertFalse(res["success"])


class WiredIntoNativeLoop(unittest.TestCase):
    def test_native_loop_routes_run_command_through_gate(self):
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_cli.py")).read()
        # the native loop has a dedicated run_command branch that uses the approver
        self.assertIn('if c["name"] == "run_command":', src)
        self.assertIn("_handle_run_command(_cmd, _make_command_approver(cfg), cfg)", src)
        # the shell tool gets appended to the native schema (FIRST element of the appended list,
        # which now also carries the first-party + background tools — so match the open bracket, not a
        # single-element list).
        self.assertIn("_native_tools=_native_tools+[_RUN_CMD_TOOL", src)


class DeployRecipe(unittest.TestCase):
    def test_rule7_deploys_via_cli_not_remote(self):
        fs = {"vercel": {"name": "Vercel", "tools": [{"name": "deploy_to_vercel"}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: fs), \
             mock.patch.object(T, "connected_slugs", lambda: ["vercel"]):
            tp = T.tools_prompt()
        self.assertIn("vercel --prod", tp)            # deploy via the local CLI
        self.assertIn("run_command", tp)
        self.assertIn("CANNOT upload local files", tp)  # honest about the remote tool


if __name__ == "__main__":
    unittest.main()
