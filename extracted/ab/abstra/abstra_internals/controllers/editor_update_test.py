from contextlib import contextmanager
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.controllers.editor_update import (
    EditorUpdateController,
    _do_update,
    _update_lib_version,
)
from abstra_internals.version import VersionStatus

_MOD = "abstra_internals.controllers.editor_update"


@contextmanager
def _fake_lock(acquired: bool):
    yield acquired


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

    def test_update_bails_when_lock_is_held(self):
        # Another thread or process (the button, the linter fix, or the
        # background auto-stage) holds the update lock — this invocation must do
        # nothing, and must NOT fall through to an in-place pip.
        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.try_update_lock", return_value=_fake_lock(False)),
            patch(f"{_MOD}._do_update") as do_update,
        ):
            _update_lib_version()

        do_update.assert_not_called()

    def test_update_runs_when_lock_is_free(self):
        with (
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}.try_update_lock", return_value=_fake_lock(True)),
            patch(f"{_MOD}._do_update") as do_update,
        ):
            _update_lib_version()

        do_update.assert_called_once()

    def test_do_update_web_shim_stages_without_restart(self):
        # Deferred path: stage the slot but don't flip/restart — the user
        # restarts later via EditorRestartController.
        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=True),
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}._latest_known_version", return_value="9.9.9"),
            patch(f"{_MOD}.stage_and_prune_locked") as stage,
            patch(f"{_MOD}.restart_editor_and_workers") as restart,
        ):
            _do_update()

        stage.assert_called_once_with(Path("/packages"), "9.9.9")
        restart.assert_not_called()

    def test_do_update_without_shim_upgrades_in_place_and_restarts(self):
        # Legacy immediate path (pre-shim web / desktop): in-place pip + restart.
        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=False),
            patch(f"{_MOD}.stage_and_prune_locked") as stage,
            patch("subprocess.check_call") as check_call,
            patch(f"{_MOD}.restart_editor_and_workers") as restart,
        ):
            _do_update()

        stage.assert_not_called()
        check_call.assert_called_once()
        restart.assert_called_once()

    def test_restarts_false_on_deferred_path(self):
        # `restarts` means "restarts immediately on click"; the deferred staged
        # path (web + shim) only stages, so it must be False. `deferred` True.
        with (
            patch(f"{_MOD}.PackageVersionManager") as pvm,
            patch(f"{_MOD}.is_windows", return_value=False),
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=True),
        ):
            inst = pvm.return_value
            inst.get_version_status.return_value = VersionStatus.OUT_OF_DATE
            inst.cached_latest_version = "9.9.9"
            inst.current_local_version = "1.0.0"
            EditorUpdateController.refresh()
            state = EditorUpdateController.state()

        self.assertTrue(state["available"])
        self.assertFalse(state["restarts"])
        self.assertTrue(state["deferred"])

    def test_deferred_false_off_the_staged_path(self):
        with (
            patch(f"{_MOD}.EDITOR_MODE", "local"),
            patch(f"{_MOD}.shim_active", return_value=False),
        ):
            self.assertFalse(EditorUpdateController.state()["deferred"])

    def test_auto_stage_on_deferred_path_delegates_to_helper(self):
        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=True),
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}._latest_known_version", return_value="9.9.9"),
            patch(f"{_MOD}.try_update_lock", return_value=_fake_lock(True)),
            patch(f"{_MOD}.stage_and_prune_locked", return_value=True) as stage,
        ):
            EditorUpdateController._available = True
            staged = EditorUpdateController.auto_stage_if_needed()

        self.assertTrue(staged)
        stage.assert_called_once_with(Path("/packages"), "9.9.9")

    def test_auto_stage_noop_off_deferred_path(self):
        with (
            patch(f"{_MOD}.EDITOR_MODE", "local"),
            patch(f"{_MOD}.shim_active", return_value=False),
            patch(f"{_MOD}.stage_and_prune_locked") as stage,
        ):
            EditorUpdateController._available = True
            self.assertFalse(EditorUpdateController.auto_stage_if_needed())

        stage.assert_not_called()

    def test_auto_stage_propagates_helper_skip(self):
        # The helper returns False when the latest is already staged; auto-stage
        # must propagate that (nothing new to broadcast).
        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=True),
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}._latest_known_version", return_value="9.9.9"),
            patch(f"{_MOD}.try_update_lock", return_value=_fake_lock(True)),
            patch(f"{_MOD}.stage_and_prune_locked", return_value=False),
        ):
            EditorUpdateController._available = True
            self.assertFalse(EditorUpdateController.auto_stage_if_needed())

    def test_auto_stage_bails_when_lock_held(self):
        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch(f"{_MOD}.shim_active", return_value=True),
            patch(f"{_MOD}.get_userbase", return_value=Path("/packages")),
            patch(f"{_MOD}._latest_known_version", return_value="9.9.9"),
            patch(f"{_MOD}.try_update_lock", return_value=_fake_lock(False)),
            patch(f"{_MOD}.stage_and_prune_locked") as stage,
        ):
            EditorUpdateController._available = True
            self.assertFalse(EditorUpdateController.auto_stage_if_needed())

        stage.assert_not_called()
