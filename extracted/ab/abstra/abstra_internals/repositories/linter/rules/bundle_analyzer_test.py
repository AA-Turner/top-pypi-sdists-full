import os
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.consts.filepaths import GITIGNORE_FILEPATH
from abstra_internals.repositories.git.native import NativeGitRepository
from abstra_internals.repositories.linter.rules.bundle_analyzer import (
    BundleAnalyzer,
    EnvInBundleFound,
    UntrackEnv,
    VenvInBundleFound,
    virtualenv_ignored,
)
from abstra_internals.services.fs import FileSystemService
from tests.fixtures import clear_dir, init_dir

MOD = "abstra_internals.repositories.linter.rules.bundle_analyzer"


def _issues_of(issue_type):
    """The analyzer emits every bundle verdict at once, so each test filters
    down to the sub-check under test."""
    return [i for i in BundleAnalyzer().find_issues() if isinstance(i, issue_type)]


class EnvInBundleTest(TestCase):
    def setUp(self) -> None:
        self.root = init_dir()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def _env_issues(self):
        return _issues_of(EnvInBundleFound)

    def test_env_on_bundle_valid_default(self):
        env_file = self.root / ".env"
        self.assertFalse(env_file.exists())
        self.assertEqual(len(self._env_issues()), 0)

    def test_env_on_bundle_valid_with_env(self):
        env_file = self.root / ".env"
        abstraignore_file = self.root / GITIGNORE_FILEPATH
        abstraignore_file.write_text(".env")
        env_file.touch()
        self.assertEqual(len(self._env_issues()), 0)

    def test_env_on_bundle_invalid_without_gitignore_file(self):
        env_file = self.root / ".env"
        env_file.touch()
        self.assertEqual(len(self._env_issues()), 1)

    def test_env_on_bundle_invalid_with_gitignore_file(self):
        env_file = self.root / ".env"
        env_file.touch()
        abstraignore_file = self.root / GITIGNORE_FILEPATH
        abstraignore_file.touch()
        self.assertEqual(len(self._env_issues()), 1)

    def test_env_on_bundle_fix(self):
        env_file = self.root / ".env"
        env_file.touch()
        issues = self._env_issues()
        self.assertEqual(len(issues), 1)
        issues[0].fixes[0].fix()
        self.assertEqual(len(self._env_issues()), 0)
        abstraignore_file = self.root / GITIGNORE_FILEPATH
        self.assertTrue(abstraignore_file.exists())
        with abstraignore_file.open("r") as file:
            content = file.read()
            self.assertTrue(".env" in content)

    def test_env_on_bundle_fix_does_not_duplicate_existing_entry(self):
        env_file = self.root / ".env"
        env_file.touch()
        gitignore_file = self.root / GITIGNORE_FILEPATH
        gitignore_file.write_text(".env\n")

        UntrackEnv().fix()

        lines = [
            line.strip()
            for line in gitignore_file.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(lines.count(".env"), 1)

    def test_env_on_bundle_fix_recognizes_rooted_env_entry(self):
        env_file = self.root / ".env"
        env_file.touch()
        gitignore_file = self.root / GITIGNORE_FILEPATH
        gitignore_file.write_text("/.env\n")

        UntrackEnv().fix()

        lines = [
            line.strip()
            for line in gitignore_file.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(lines, ["/.env"])

    def test_env_on_bundle_fix_does_not_duplicate_when_env_is_tracked(self):
        # `git check-ignore` reports tracked files as not-ignored, so a guard
        # based on it would falsely re-append `.env` even when it is listed.
        FileSystemService.clear_gitignore_cache()
        repo = NativeGitRepository(self.root)
        self.assertTrue(repo.init_repository())

        env_file = self.root / ".env"
        env_file.write_text("SECRET=foo\n")
        success, _ = repo.commit_changes("track .env")
        self.assertTrue(success)

        gitignore_file = self.root / GITIGNORE_FILEPATH
        gitignore_file.write_text(".env\n")
        FileSystemService.clear_gitignore_cache()

        UntrackEnv().fix()

        lines = [
            line.strip()
            for line in gitignore_file.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(lines.count(".env"), 1)

    def test_env_on_bundle_fix_appends_when_entry_missing(self):
        env_file = self.root / ".env"
        env_file.touch()
        gitignore_file = self.root / GITIGNORE_FILEPATH
        gitignore_file.write_text("node_modules\n")

        UntrackEnv().fix()

        lines = [
            line.strip()
            for line in gitignore_file.read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(lines.count(".env"), 1)
        self.assertIn("node_modules", lines)


class VenvInBundleTest(TestCase):
    def setUp(self):
        self.root = init_dir()
        # Initialize git repo for gitignore checks to work
        os.system(f"git init {self.root} --quiet")

    def tearDown(self):
        clear_dir(self.root)

    def _patch_paths(self, venv_dirname):
        return patch(
            f"{MOD}.get_root_and_prefix_path",
            return_value=(
                self.root.resolve().as_posix(),
                (self.root / venv_dirname).resolve().as_posix(),
            ),
        )

    def test_venv_ignored_when_in_gitignore_without_slash(self):
        """Test that venv is detected as ignored when .gitignore contains 'venv'"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("venv\n")

        with self._patch_paths("venv"):
            self.assertTrue(virtualenv_ignored())

    def test_venv_ignored_when_in_gitignore_with_trailing_slash(self):
        """Test that venv is detected as ignored when .gitignore contains 'venv/'"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("venv/\n")

        with self._patch_paths("venv"):
            self.assertTrue(virtualenv_ignored())

    def test_venv_ignored_when_in_gitignore_with_wildcard(self):
        """Test that venv is detected as ignored when .gitignore contains '**/venv'"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("**/venv\n")

        with self._patch_paths("venv"):
            self.assertTrue(virtualenv_ignored())

    def test_dot_venv_ignored_when_in_gitignore(self):
        """Test that .venv is detected as ignored when .gitignore contains '.venv'"""
        (self.root / ".venv").mkdir()
        (self.root / ".gitignore").write_text(".venv\n")

        with self._patch_paths(".venv"):
            self.assertTrue(virtualenv_ignored())

    def test_venv_not_ignored_when_not_in_gitignore(self):
        """Test that venv is not detected as ignored when not in .gitignore"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("other_folder\n")

        with self._patch_paths("venv"):
            self.assertFalse(virtualenv_ignored())

    def test_no_issues_when_venv_in_gitignore(self):
        """No venv issue when the virtualenv folder is in .gitignore"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("venv\n")

        with (
            patch(f"{MOD}.running_under_virtualenv", return_value=True),
            patch(f"{MOD}.virtualenv_inside_project", return_value=True),
            self._patch_paths("venv"),
        ):
            self.assertEqual(_issues_of(VenvInBundleFound), [])

    def test_issues_when_venv_not_in_gitignore(self):
        """Venv issue when the virtualenv folder is not in .gitignore"""
        (self.root / "venv").mkdir()
        (self.root / ".gitignore").write_text("other_folder\n")

        with (
            patch(f"{MOD}.running_under_virtualenv", return_value=True),
            patch(f"{MOD}.virtualenv_inside_project", return_value=True),
            self._patch_paths("venv"),
        ):
            self.assertEqual(len(_issues_of(VenvInBundleFound)), 1)
