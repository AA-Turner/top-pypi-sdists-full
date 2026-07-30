"""Contract tests for process actions (PR1, TDD).

Fixes with process-wide effects (today: the abstra upgrade restart) must not
execute os._exit/os.execv inside the sidecar. The mechanism: a module-level
hook — the default handler executes immediately (in-process behavior is
byte-identical to today's), while the sidecar installs a collector that ships
the action back to the main process via the apply_fix RPC response.
"""

import sys
import unittest
from unittest.mock import patch

from abstra_internals.repositories.linter import process_actions


class ProcessActionHookTest(unittest.TestCase):
    def tearDown(self):
        process_actions.set_process_action_handler(None)

    def test_default_handler_executes_immediately(self):
        with patch.object(process_actions, "execute_process_action") as execute:
            process_actions.request_process_action("restart_editor")
        execute.assert_called_once_with("restart_editor", reason=None)

    def test_registered_handler_intercepts_execution(self):
        collected = []
        process_actions.set_process_action_handler(collected.append)
        with patch.object(process_actions, "execute_process_action") as execute:
            process_actions.request_process_action("restart_editor")
        self.assertEqual(collected, ["restart_editor"])
        execute.assert_not_called()

    def test_clearing_handler_restores_default(self):
        process_actions.set_process_action_handler(lambda action: None)
        process_actions.set_process_action_handler(None)
        with patch.object(process_actions, "execute_process_action") as execute:
            process_actions.request_process_action("restart_editor")
        execute.assert_called_once_with("restart_editor", reason=None)

    def test_default_handler_forwards_reason(self):
        with patch.object(process_actions, "execute_process_action") as execute:
            process_actions.request_process_action(
                "restart_editor", reason="UpdateAbstra"
            )
        execute.assert_called_once_with("restart_editor", reason="UpdateAbstra")


class ExecuteProcessActionTest(unittest.TestCase):
    def test_local_mode_execs_editor_in_place(self):
        with patch("os.execv") as execv, patch("os._exit") as exit_:
            process_actions.execute_process_action("restart_editor", is_web=False)
        execv.assert_called_once()
        exit_.assert_not_called()
        args = execv.call_args[0]
        self.assertEqual(args[0], sys.executable)
        self.assertEqual(args[1][0], sys.executable)

    def test_web_mode_exits_for_kubelet_restart(self):
        with patch("os.execv") as execv, patch("os._exit") as exit_:
            process_actions.execute_process_action("restart_editor", is_web=True)
        exit_.assert_called_once_with(0)
        execv.assert_not_called()

    def test_web_mode_emits_restart_lifecycle_before_exit(self):
        events = []
        with (
            patch("os._exit") as exit_,
            patch.object(
                process_actions.AbstraLogger,
                "lifecycle",
                side_effect=lambda msg, attrs: events.append((msg, attrs)),
            ),
        ):
            process_actions.execute_process_action(
                "restart_editor", is_web=True, reason="InstallPackage"
            )
        exit_.assert_called_once_with(0)
        self.assertEqual(len(events), 1)
        _, attrs = events[0]
        self.assertEqual(attrs["stage"], "editor.restart_requested")
        self.assertEqual(attrs["action"], "restart_editor")
        self.assertEqual(attrs["reason"], "InstallPackage")

    def test_local_mode_emits_no_lifecycle(self):
        events = []
        with (
            patch("os.execv"),
            patch.object(
                process_actions.AbstraLogger,
                "lifecycle",
                side_effect=lambda msg, attrs: events.append((msg, attrs)),
            ),
        ):
            process_actions.execute_process_action("restart_editor", is_web=False)
        self.assertEqual(events, [])

    def test_unknown_action_is_a_noop(self):
        with patch("os.execv") as execv, patch("os._exit") as exit_:
            process_actions.execute_process_action("dance_party", is_web=False)
        execv.assert_not_called()
        exit_.assert_not_called()


class UpdateAbstraFixFlowTest(unittest.TestCase):
    """The upgrade fix must route its restart through the hook in BOTH
    editor modes — never calling os.execv/os._exit directly anymore."""

    def tearDown(self):
        process_actions.set_process_action_handler(None)

    def test_local_mode_flow_routes_restart_through_hook(self):
        from abstra_internals.controllers import editor_update as mod

        collected = []
        process_actions.set_process_action_handler(collected.append)
        with (
            patch("subprocess.check_call") as check_call,
            patch("os.execv") as execv,
            patch("os._exit") as exit_,
            patch.object(process_actions, "EDITOR_MODE", "local"),
        ):
            mod._update_lib_version()

        check_call.assert_called_once()
        self.assertIn("abstra", check_call.call_args[0][0])
        self.assertEqual(collected, ["restart_editor"])
        execv.assert_not_called()
        exit_.assert_not_called()

    def test_web_mode_flow_routes_restart_through_hook(self):
        from abstra_internals.controllers import editor_update as mod

        collected = []
        process_actions.set_process_action_handler(collected.append)
        with (
            patch("subprocess.check_call") as check_call,
            patch("os.execv") as execv,
            patch("os._exit") as exit_,
            patch.object(process_actions, "EDITOR_MODE", "web"),
            patch.object(process_actions, "RABBITMQ_CONNECTION_URI", None),
        ):
            mod._update_lib_version()

        check_call.assert_called_once()
        self.assertEqual(collected, ["restart_editor"])
        execv.assert_not_called()
        exit_.assert_not_called()

    def test_pip_failure_requests_no_action(self):
        from abstra_internals.controllers import editor_update as mod

        collected = []
        process_actions.set_process_action_handler(collected.append)
        with (
            patch("subprocess.check_call", side_effect=RuntimeError("pip exploded")),
            patch("os.execv") as execv,
            patch("os._exit") as exit_,
        ):
            mod._update_lib_version()  # must swallow, as today

        self.assertEqual(collected, [])
        execv.assert_not_called()
        exit_.assert_not_called()


_RESTART_MOD = "abstra_internals.controllers.editor_restart"
_STATUS_MOD = "abstra_internals.controllers.editor_status_events"


class MarkNeedsRestartTest(unittest.TestCase):
    """PR1b: a dependency install on the web editor defers the restart — it marks
    a restart as pending (surfaced as a "Restart editor" button) instead of
    dropping the pod. MARK_NEEDS_RESTART is a bare signal: it carries no data
    because the restart never needs the package names and the UI is generic."""

    def tearDown(self):
        process_actions.set_process_action_handler(None)

    def test_execute_marks_pending_and_rebroadcasts(self):
        with (
            patch("os._exit") as exit_,
            patch("os.execv") as execv,
            patch(
                f"{_RESTART_MOD}.EditorRestartController.mark_dependencies_installed"
            ) as mark,
            patch(f"{_STATUS_MOD}.EditorStatusEventController.broadcast") as broadcast,
        ):
            process_actions.execute_process_action(process_actions.MARK_NEEDS_RESTART)
        mark.assert_called_once_with()
        broadcast.assert_called_once()
        # Marking must NOT restart — that is the whole point of deferring.
        exit_.assert_not_called()
        execv.assert_not_called()

    def test_web_defers_by_requesting_the_mark_action(self):
        collected = []
        process_actions.set_process_action_handler(collected.append)
        with patch.object(process_actions, "EDITOR_MODE", "web"):
            process_actions.restart_or_defer_after_install()
        self.assertEqual(collected, [process_actions.MARK_NEEDS_RESTART])

    def test_non_web_restarts_immediately(self):
        with (
            patch.object(process_actions, "EDITOR_MODE", "local"),
            patch.object(process_actions, "restart_editor_and_workers") as restart,
        ):
            process_actions.restart_or_defer_after_install()
        restart.assert_called_once()


if __name__ == "__main__":
    unittest.main()
