from importlib.metadata import PackageNotFoundError
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.controllers.editor_update import EditorUpdateController
from abstra_internals.version import VersionStatus

_MOD = "abstra_internals.controllers.editor_update"


class EditorUpdateControllerTest(TestCase):
    def tearDown(self):
        EditorUpdateController._available = False
        EditorUpdateController._label = ""
        EditorUpdateController._restarts = False

    def test_available_when_out_of_date(self):
        with (
            patch(f"{_MOD}.PackageVersionManager") as pvm,
            patch(f"{_MOD}.is_windows", return_value=False),
        ):
            inst = pvm.return_value
            inst.get_version_status.return_value = VersionStatus.OUT_OF_DATE
            inst.cached_latest_version = "9.9.9"
            inst.current_local_version = "1.0.0"
            EditorUpdateController.refresh()

        state = EditorUpdateController.state()
        self.assertTrue(state["available"])
        self.assertIn("9.9.9", state["label"])
        self.assertTrue(state["restarts"])

    def test_not_available_when_up_to_date(self):
        with patch(f"{_MOD}.PackageVersionManager") as pvm:
            pvm.return_value.get_version_status.return_value = VersionStatus.UP_TO_DATE
            EditorUpdateController.refresh()

        self.assertFalse(EditorUpdateController.state()["available"])

    def test_not_available_when_package_not_found(self):
        with patch(f"{_MOD}.PackageVersionManager", side_effect=PackageNotFoundError()):
            EditorUpdateController.refresh()

        self.assertFalse(EditorUpdateController.state()["available"])

    def test_windows_update_does_not_restart(self):
        with (
            patch(f"{_MOD}.PackageVersionManager") as pvm,
            patch(f"{_MOD}.is_windows", return_value=True),
        ):
            inst = pvm.return_value
            inst.get_version_status.return_value = VersionStatus.OUT_OF_DATE
            inst.cached_latest_version = "9.9.9"
            inst.current_local_version = "1.0.0"
            EditorUpdateController.refresh()

        self.assertFalse(EditorUpdateController.state()["restarts"])

    def test_trigger_update_non_windows_runs_pip(self):
        with (
            patch(f"{_MOD}.is_windows", return_value=False),
            patch(f"{_MOD}._update_lib_version") as upd,
            patch(f"{_MOD}.webbrowser.open") as browser,
        ):
            EditorUpdateController.trigger_update()

        upd.assert_called_once()
        browser.assert_not_called()

    def test_trigger_update_windows_opens_changelog(self):
        with (
            patch(f"{_MOD}.is_windows", return_value=True),
            patch(f"{_MOD}._update_lib_version") as upd,
            patch(f"{_MOD}.webbrowser.open") as browser,
        ):
            EditorUpdateController.trigger_update()

        browser.assert_called_once()
        upd.assert_not_called()
