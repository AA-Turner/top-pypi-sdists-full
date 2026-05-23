from unittest import TestCase

from abstra_internals.consts.filepaths import GITIGNORE_FILEPATH
from abstra_internals.repositories.git.native import NativeGitRepository
from abstra_internals.repositories.linter.rules.env_in_bundle import (
    EnvInBundle,
    UntrackEnv,
)
from abstra_internals.services.fs import FileSystemService
from tests.fixtures import clear_dir, init_dir


class EnvInBundleTest(TestCase):
    def setUp(self) -> None:
        self.root = init_dir()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def test_env_on_bundle_valid_default(self):
        rule = EnvInBundle()
        env_file = self.root / ".env"
        self.assertFalse(env_file.exists())
        self.assertEqual(len(rule.find_issues()), 0)

    def test_env_on_bundle_valid_with_env(self):
        rule = EnvInBundle()
        env_file = self.root / ".env"
        abstraignore_file = self.root / GITIGNORE_FILEPATH
        abstraignore_file.write_text(".env")
        env_file.touch()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_env_on_bundle_invalid_without_gitignore_file(self):
        env_file = self.root / ".env"
        env_file.touch()
        rule = EnvInBundle()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_env_on_bundle_invalid_with_gitignore_file(self):
        env_file = self.root / ".env"
        env_file.touch()
        abstraignore_file = self.root / GITIGNORE_FILEPATH
        abstraignore_file.touch()
        rule = EnvInBundle()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_env_on_bundle_fix(self):
        env_file = self.root / ".env"
        env_file.touch()
        rule = EnvInBundle()
        self.assertEqual(len(rule.find_issues()), 1)
        rule.find_issues()[0].fixes[0].fix()
        self.assertEqual(len(rule.find_issues()), 0)
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
