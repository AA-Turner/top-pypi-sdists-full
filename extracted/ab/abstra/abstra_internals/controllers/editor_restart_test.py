from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.controllers.editor_restart import EditorRestartController

_MOD = "abstra_internals.controllers.editor_restart"


class EditorRestartControllerTest(TestCase):
    def setUp(self):
        EditorRestartController._pending_packages = set()

    def tearDown(self):
        EditorRestartController._pending_packages = set()

    def test_no_reasons_when_nothing_pending(self):
        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.get_pending_version", return_value=None),
        ):
            state = EditorRestartController.state()

        self.assertFalse(state["required"])
        self.assertIsNone(state["abstra_update"])
        self.assertIsNone(state["dependencies"])

    def test_abstra_reason_derived_from_pending_slot(self):
        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.get_pending_version", return_value="3.31.14"),
        ):
            state = EditorRestartController.state()

        self.assertTrue(state["required"])
        self.assertEqual(state["abstra_update"], {"target_version": "3.31.14"})
        self.assertIsNone(state["dependencies"])

    def test_abstra_reason_absent_without_userbase(self):
        with patch(f"{_MOD}.get_userbase", return_value=None):
            state = EditorRestartController.state()

        self.assertIsNone(state["abstra_update"])

    def test_dependencies_reason_accumulates_in_memory(self):
        EditorRestartController.mark_dependencies_installed(["numpy"])
        EditorRestartController.mark_dependencies_installed(["pandas", "numpy"])

        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.get_pending_version", return_value=None),
        ):
            state = EditorRestartController.state()

        self.assertTrue(state["required"])
        # Deduped and sorted.
        self.assertEqual(state["dependencies"], {"packages": ["numpy", "pandas"]})

    def test_both_reasons_can_coexist(self):
        EditorRestartController.mark_dependencies_installed(["numpy"])
        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.get_pending_version", return_value="3.31.14"),
        ):
            state = EditorRestartController.state()

        self.assertTrue(state["required"])
        self.assertIsNotNone(state["abstra_update"])
        self.assertIsNotNone(state["dependencies"])

    def test_restart_now_activates_then_restarts(self):
        with (
            patch(f"{_MOD}.activate_pending_update") as activate,
            patch(f"{_MOD}.restart_editor_and_workers") as restart,
        ):
            EditorRestartController.restart_now()

        activate.assert_called_once()
        restart.assert_called_once()
