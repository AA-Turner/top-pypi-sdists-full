from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.repositories.linter.models import PathScopedLinterRule
from abstra_internals.repositories.linter.rules.new_version_of_abstra_available import (
    NewVersionOfAbstraAvailable,
)
from abstra_internals.version import VersionStatus

_PVM_PATH = (
    "abstra_internals.repositories.linter.rules."
    "new_version_of_abstra_available.PackageVersionManager"
)


class NewVersionScopedTest(TestCase):
    """The new-version check hits PyPI (cached 15 min). It must not run on a
    per-save (scoped) pass — the version cannot change because of a file edit.
    The existing banner (a project-global issue, path=None) is preserved across
    scoped runs by the merge, so the rule simply returns [] when scoped."""

    def test_is_path_scoped_rule(self):
        self.assertIsInstance(NewVersionOfAbstraAvailable(), PathScopedLinterRule)

    def test_scoped_run_returns_empty_without_checking_version(self):
        rule = NewVersionOfAbstraAvailable()
        with patch(_PVM_PATH) as mock_pvm:
            issues = rule.find_issues(path=Path("script.py"))
        self.assertEqual(issues, [])
        mock_pvm.assert_not_called()

    def test_full_run_emits_banner_when_outdated(self):
        rule = NewVersionOfAbstraAvailable()
        with patch(_PVM_PATH) as mock_pvm:
            instance = mock_pvm.return_value
            instance.get_version_status.return_value = VersionStatus.OUT_OF_DATE
            instance.cached_latest_version = "9.9.9"
            instance.current_local_version = "1.0.0"
            issues = rule.find_issues()
        self.assertEqual(len(issues), 1)

    def test_full_run_no_banner_when_up_to_date(self):
        rule = NewVersionOfAbstraAvailable()
        with patch(_PVM_PATH) as mock_pvm:
            instance = mock_pvm.return_value
            instance.get_version_status.return_value = "anything-but-out-of-date"
            issues = rule.find_issues()
        self.assertEqual(issues, [])
