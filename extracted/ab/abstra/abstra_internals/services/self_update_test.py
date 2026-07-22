import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from abstra_internals.services.self_update import (
    SHIM_MARKER_ENV,
    VERSIONS_DIRNAME,
    current_pointer,
    flip,
    perform_staged_update,
    prune,
    stage,
)

PY_TAG = f"{sys.version_info.major}.{sys.version_info.minor}"
CHECK_CALL_TARGET = "abstra_internals.services.self_update.subprocess.check_call"


def make_slot(userbase: Path, version: str) -> Path:
    slot = userbase / VERSIONS_DIRNAME / version
    site = slot / "lib" / f"python{PY_TAG}" / "site-packages"
    (site / "abstra").mkdir(parents=True)
    return slot


def fake_pip_install(recorded: list):
    # stage() installs in two passes, so this runs more than once per stage;
    # keep it idempotent.
    def check_call(cmd, env, **_kwargs):
        recorded.append({"cmd": cmd, "env": env})
        staging = Path(env["PYTHONUSERBASE"])
        site = staging / "lib" / f"python{PY_TAG}" / "site-packages"
        (site / "abstra").mkdir(parents=True, exist_ok=True)
        return 0

    return check_call


class SlotTestBase(unittest.TestCase):
    def setUp(self) -> None:
        tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(tmp_dir.cleanup)
        self.userbase = Path(tmp_dir.name)


class TestStage(SlotTestBase):
    def test_installs_into_versioned_slot(self):
        recorded = []
        with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
            slot = stage(self.userbase, "9.9.9")

        self.assertEqual(slot, self.userbase / VERSIONS_DIRNAME / "9.9.9")
        self.assertTrue(
            (slot / "lib" / f"python{PY_TAG}" / "site-packages" / "abstra").is_dir()
        )
        self.assertFalse((self.userbase / VERSIONS_DIRNAME / ".staging-9.9.9").exists())
        self.assertEqual(recorded[0]["cmd"][-1], "abstra==9.9.9")

    def test_two_pass_install_forces_abstra_then_resolves_deps(self):
        # Pass 1 forces abstra into the slot ignoring the ambient install (the
        # image bakes abstra into the global site-packages, so a plain install
        # would copy nothing when target <= image version) while keeping deps
        # out. Pass 2 pulls in only the deps not already satisfied.
        recorded = []
        with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
            stage(self.userbase, "9.9.9")

        self.assertEqual(len(recorded), 2)
        self.assertIn("--ignore-installed", recorded[0]["cmd"])
        self.assertIn("--no-deps", recorded[0]["cmd"])
        # The dependency-resolution pass must not force/limit the resolver.
        self.assertNotIn("--ignore-installed", recorded[1]["cmd"])
        self.assertNotIn("--no-deps", recorded[1]["cmd"])

    def test_pip_env_targets_staging_and_strips_pythonpath(self):
        recorded = []
        with mock.patch.dict(os.environ, {"PYTHONPATH": "/active-slot"}):
            with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
                stage(self.userbase, "9.9.9")

        env = recorded[0]["env"]
        self.assertEqual(
            env["PYTHONUSERBASE"],
            str(self.userbase / VERSIONS_DIRNAME / ".staging-9.9.9"),
        )
        # The active slot must not satisfy dependencies of the new slot.
        self.assertNotIn("PYTHONPATH", env)

    def test_pip_failure_leaves_no_slot_nor_staging(self):
        def failing_pip(cmd, env, **_kwargs):
            Path(env["PYTHONUSERBASE"]).mkdir(parents=True)
            raise subprocess.CalledProcessError(1, cmd)

        with mock.patch(CHECK_CALL_TARGET, side_effect=failing_pip):
            with self.assertRaises(subprocess.CalledProcessError):
                stage(self.userbase, "9.9.9")

        versions_dir = self.userbase / VERSIONS_DIRNAME
        self.assertFalse((versions_dir / "9.9.9").exists())
        self.assertFalse((versions_dir / ".staging-9.9.9").exists())

    def test_install_without_abstra_package_is_rejected(self):
        def pip_without_abstra(cmd, env, **_kwargs):
            staging = Path(env["PYTHONUSERBASE"])
            site = staging / "lib" / f"python{PY_TAG}" / "site-packages"
            site.mkdir(parents=True, exist_ok=True)
            return 0

        with mock.patch(CHECK_CALL_TARGET, side_effect=pip_without_abstra):
            with self.assertRaises(RuntimeError):
                stage(self.userbase, "9.9.9")

        self.assertFalse((self.userbase / VERSIONS_DIRNAME / "9.9.9").exists())


class TestFlip(SlotTestBase):
    def test_points_at_slot_site_packages(self):
        slot = make_slot(self.userbase, "1.0.0")

        previous = flip(self.userbase, slot)

        pointer = current_pointer(self.userbase)
        self.assertIsNone(previous)
        self.assertTrue(pointer.is_symlink())
        self.assertEqual(
            Path(os.readlink(pointer)),
            slot / "lib" / f"python{PY_TAG}" / "site-packages",
        )

    def test_returns_previous_slot(self):
        slot_a = make_slot(self.userbase, "1.0.0")
        slot_b = make_slot(self.userbase, "2.0.0")

        flip(self.userbase, slot_a)
        previous = flip(self.userbase, slot_b)

        self.assertEqual(previous, slot_a)
        self.assertEqual(
            Path(os.readlink(current_pointer(self.userbase))).parents[2], slot_b
        )

    def test_overwrites_leftover_tmp_symlink(self):
        slot = make_slot(self.userbase, "1.0.0")
        pointer = current_pointer(self.userbase)
        tmp_link = pointer.with_name(pointer.name + ".tmp")
        os.symlink(self.userbase / "stale-target", tmp_link)

        flip(self.userbase, slot)

        self.assertFalse(tmp_link.exists() or tmp_link.is_symlink())
        self.assertEqual(Path(os.readlink(pointer)).parents[2], slot)


class TestPrune(SlotTestBase):
    def test_removes_everything_but_kept_slots(self):
        old = make_slot(self.userbase, "1.0.0")
        previous = make_slot(self.userbase, "2.0.0")
        current = make_slot(self.userbase, "3.0.0")
        stale_staging = self.userbase / VERSIONS_DIRNAME / ".staging-4.0.0"
        stale_staging.mkdir()

        prune(self.userbase, keep={previous, current})

        self.assertFalse(old.exists())
        self.assertFalse(stale_staging.exists())
        self.assertTrue(previous.is_dir())
        self.assertTrue(current.is_dir())


class TestPerformStagedUpdate(SlotTestBase):
    def test_falls_back_without_shim_marker(self):
        # No boot shim -> flipping a slot would never be activated, so we must
        # not slot; the caller falls back to the legacy in-place upgrade.
        recorded = []
        env = {k: v for k, v in os.environ.items() if k != SHIM_MARKER_ENV}
        env["PYTHONUSERBASE"] = str(self.userbase)
        with mock.patch.dict(os.environ, env, clear=True):
            with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
                self.assertFalse(perform_staged_update("9.9.9"))
        # It must bail before running pip.
        self.assertEqual(recorded, [])

    def test_falls_back_without_userbase(self):
        env = {k: v for k, v in os.environ.items() if k != "PYTHONUSERBASE"}
        env[SHIM_MARKER_ENV] = "1"
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertFalse(perform_staged_update("9.9.9"))

    def test_stages_flips_and_prunes(self):
        recorded = []
        previous = make_slot(self.userbase, "1.0.0")
        ancient = make_slot(self.userbase, "0.9.0")
        flip(self.userbase, previous)

        env = {SHIM_MARKER_ENV: "1", "PYTHONUSERBASE": str(self.userbase)}
        with mock.patch.dict(os.environ, env):
            with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
                self.assertTrue(perform_staged_update("2.0.0"))

        new_slot = self.userbase / VERSIONS_DIRNAME / "2.0.0"
        self.assertEqual(
            Path(os.readlink(current_pointer(self.userbase))).parents[2], new_slot
        )
        # Previous slot is kept for cheap rollback; older ones are pruned.
        self.assertTrue(previous.is_dir())
        self.assertFalse(ancient.exists())

    def test_failure_never_touches_the_pointer(self):
        def failing_pip(cmd, env, **_kwargs):
            raise subprocess.CalledProcessError(1, cmd)

        active = make_slot(self.userbase, "1.0.0")
        flip(self.userbase, active)

        env = {SHIM_MARKER_ENV: "1", "PYTHONUSERBASE": str(self.userbase)}
        with mock.patch.dict(os.environ, env):
            with mock.patch(CHECK_CALL_TARGET, side_effect=failing_pip):
                with self.assertRaises(subprocess.CalledProcessError):
                    perform_staged_update("2.0.0")

        self.assertEqual(
            Path(os.readlink(current_pointer(self.userbase))).parents[2], active
        )
        self.assertTrue(active.is_dir())


class TestPointerLayout(SlotTestBase):
    def test_pointer_name_encodes_python_minor_version(self):
        self.assertEqual(
            current_pointer(self.userbase).name, f"abstra-current-py{PY_TAG}"
        )


if __name__ == "__main__":
    unittest.main()
