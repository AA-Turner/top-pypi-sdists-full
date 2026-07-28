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
    activate_pending_update,
    flip,
    get_current_pointer,
    get_pending_version,
    perform_staged_update,
    prune,
    stage,
    stage_and_prune_locked,
    try_update_lock,
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

        pointer = get_current_pointer(self.userbase)
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
            Path(os.readlink(get_current_pointer(self.userbase))).parents[2], slot_b
        )

    def test_overwrites_leftover_tmp_symlink(self):
        slot = make_slot(self.userbase, "1.0.0")
        pointer = get_current_pointer(self.userbase)
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
            Path(os.readlink(get_current_pointer(self.userbase))).parents[2], new_slot
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
            Path(os.readlink(get_current_pointer(self.userbase))).parents[2], active
        )
        self.assertTrue(active.is_dir())


class TestPointerLayout(SlotTestBase):
    def test_pointer_name_encodes_python_minor_version(self):
        self.assertEqual(
            get_current_pointer(self.userbase).name, f"abstra-current-py{PY_TAG}"
        )


class TestPendingVersion(SlotTestBase):
    def test_none_without_slots(self):
        self.assertIsNone(get_pending_version(self.userbase))

    def test_slot_without_pointer_is_pending(self):
        # Never-flipped (first update): a staged slot with no pointer is pending.
        make_slot(self.userbase, "3.31.14")
        self.assertEqual(get_pending_version(self.userbase), "3.31.14")

    def test_none_when_pointer_at_newest(self):
        slot = make_slot(self.userbase, "3.31.14")
        flip(self.userbase, slot)
        self.assertIsNone(get_pending_version(self.userbase))

    def test_newest_slot_beyond_pointer_is_pending(self):
        active = make_slot(self.userbase, "3.31.13")
        flip(self.userbase, active)
        make_slot(self.userbase, "3.31.14")  # staged, not flipped
        self.assertEqual(get_pending_version(self.userbase), "3.31.14")

    def test_compares_by_version_not_lexicographically(self):
        active = make_slot(self.userbase, "3.9.0")
        flip(self.userbase, active)
        make_slot(self.userbase, "3.31.14")
        # "3.31.14" < "3.9.0" as strings, but 3.31.14 is the newer version.
        self.assertEqual(get_pending_version(self.userbase), "3.31.14")

    def test_ignores_staging_dirs(self):
        (self.userbase / VERSIONS_DIRNAME / ".staging-3.31.14").mkdir(parents=True)
        self.assertIsNone(get_pending_version(self.userbase))


class TestActivatePendingUpdate(SlotTestBase):
    def test_flips_pending_and_returns_version(self):
        active = make_slot(self.userbase, "3.31.13")
        flip(self.userbase, active)
        make_slot(self.userbase, "3.31.14")

        env = {SHIM_MARKER_ENV: "1", "PYTHONUSERBASE": str(self.userbase)}
        with mock.patch.dict(os.environ, env):
            activated = activate_pending_update()

        self.assertEqual(activated, "3.31.14")
        pointed = Path(os.readlink(get_current_pointer(self.userbase))).parents[2]
        self.assertEqual(pointed, self.userbase / VERSIONS_DIRNAME / "3.31.14")
        # Previous kept for rollback; nothing older to prune here.
        self.assertTrue((self.userbase / VERSIONS_DIRNAME / "3.31.13").is_dir())

    def test_noop_when_nothing_pending(self):
        active = make_slot(self.userbase, "3.31.14")
        flip(self.userbase, active)

        env = {SHIM_MARKER_ENV: "1", "PYTHONUSERBASE": str(self.userbase)}
        with mock.patch.dict(os.environ, env):
            self.assertIsNone(activate_pending_update())

    def test_none_without_userbase(self):
        env = {k: v for k, v in os.environ.items() if k != "PYTHONUSERBASE"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertIsNone(activate_pending_update())


class TestStageAndPruneLocked(SlotTestBase):
    def test_stages_and_keeps_active_and_new_pruning_intermediate(self):
        # Running X (a slot the pointer targets), X+1 staged but not flipped;
        # staging X+2 must delete X+1 and keep BOTH the active X and the new X+2.
        active = make_slot(self.userbase, "3.31.13")
        flip(self.userbase, active)
        make_slot(self.userbase, "3.31.14")  # intermediate, never activated

        recorded = []
        with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
            staged = stage_and_prune_locked(self.userbase, "3.31.15")

        self.assertTrue(staged)
        versions = self.userbase / VERSIONS_DIRNAME
        self.assertTrue((versions / "3.31.13").is_dir())  # active kept
        self.assertTrue((versions / "3.31.15").is_dir())  # new kept
        self.assertFalse((versions / "3.31.14").exists())  # intermediate pruned
        # It does NOT flip: the pointer still targets the active version.
        self.assertEqual(
            Path(os.readlink(get_current_pointer(self.userbase))).parents[2], active
        )

    def test_keeps_new_only_when_no_active_pointer(self):
        # Running X from /packages (no pointer). X isn't a slot; staging X+2 with
        # an intermediate X+1 present prunes X+1, keeps only the new slot.
        make_slot(self.userbase, "3.31.14")  # intermediate staged, no pointer

        recorded = []
        with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
            stage_and_prune_locked(self.userbase, "3.31.15")

        versions = self.userbase / VERSIONS_DIRNAME
        self.assertTrue((versions / "3.31.15").is_dir())
        self.assertFalse((versions / "3.31.14").exists())

    def test_idempotent_when_already_pending(self):
        make_slot(self.userbase, "3.31.15")  # already the pending (no pointer)

        recorded = []
        with mock.patch(CHECK_CALL_TARGET, side_effect=fake_pip_install(recorded)):
            staged = stage_and_prune_locked(self.userbase, "3.31.15")

        self.assertFalse(staged)
        self.assertEqual(recorded, [])  # no re-install


class TestTryUpdateLock(SlotTestBase):
    def test_serializes_threads_within_the_same_process(self):
        # The fcntl file lock is a no-op between threads of one process; this is
        # the intra-process guard that stops the editor's own threads (boot
        # lint, on-connect check, periodic checker, the button) from racing into
        # stage() and clobbering the shared staging dir. While one context holds
        # it, a second acquire in the same process must yield False.
        with try_update_lock(self.userbase) as first:
            self.assertTrue(first)
            with try_update_lock(self.userbase) as second:
                self.assertFalse(second)

    def test_reacquirable_after_release(self):
        with try_update_lock(self.userbase) as acquired:
            self.assertTrue(acquired)
        with try_update_lock(self.userbase) as acquired:
            self.assertTrue(acquired)

    def test_thread_lock_only_without_userbase(self):
        # Desktop / non-slotted: no shared FS to guard, so only the thread lock
        # applies and the context is always acquired.
        with try_update_lock(None) as acquired:
            self.assertTrue(acquired)


if __name__ == "__main__":
    unittest.main()
