from pathlib import Path
from unittest.mock import patch

from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.rules import (
    rules,
    run_after_abstra_json_change,
    run_after_css_change,
    run_after_env_or_gitignore_change,
    run_after_html_change,
    run_after_js_change,
    run_after_package_install,
    run_after_py_change,
    run_after_requirements_change,
)
from tests.fixtures import BaseTest


class RuleGroupCompletenessTest(BaseTest):
    """Every rule must appear in at least one trigger group."""

    def _all_group_names(self):
        all_groups = [
            run_after_py_change,
            run_after_requirements_change,
            run_after_abstra_json_change,
            run_after_env_or_gitignore_change,
            run_after_package_install,
            run_after_html_change,
            run_after_css_change,
            run_after_js_change,
        ]
        names = set()
        for group in all_groups:
            for rule in group:
                names.add(rule.name)
        return names

    def test_rules_equals_union_of_groups(self):
        rules_names = {r.name for r in rules}
        group_names = self._all_group_names()
        self.assertEqual(rules_names, group_names)

    def test_no_duplicates_in_rules(self):
        names = [r.name for r in rules]
        self.assertEqual(len(names), len(set(names)))


class UpdateSpecificChecksTest(BaseTest):
    """update_specific_checks merges results into existing cache."""

    def test_merge_preserves_other_checks(self):
        repo = LocalLinterRepository()
        repo.update_checks()
        all_names = {c.name for c in repo.checks}

        # Run only the py-change subset
        repo.update_specific_checks(run_after_py_change)
        after_names = {c.name for c in repo.checks}

        # All original checks should still be present
        self.assertEqual(all_names, after_names)

    def test_merge_updates_targeted_checks(self):
        repo = LocalLinterRepository()
        repo.update_checks()
        old_checks = {c.name: c for c in repo.checks}

        # Run a specific subset
        repo.update_specific_checks(run_after_requirements_change)
        new_checks = {c.name: c for c in repo.checks}

        targeted_names = {r.name for r in run_after_requirements_change}
        for name in targeted_names:
            # Targeted checks should be new instances (refreshed)
            self.assertIn(name, new_checks)
            self.assertIsNot(new_checks[name], old_checks[name])

    def test_update_specific_does_not_run_all_rules(self):
        repo = LocalLinterRepository()
        repo.update_checks()
        initial_count = len(repo.checks)

        # Running a subset should not add new check names
        repo.update_specific_checks(run_after_env_or_gitignore_change)
        self.assertEqual(len(repo.checks), initial_count)


class LintFilesRoutingTest(BaseTest):
    """lint_files dispatches to the correct rule group based on filename."""

    def setUp(self):
        super().setUp()
        self.repos = self.controller.repositories
        self.event_controller = CodebaseEventController(self.repos)

    def test_py_file_triggers_py_rules(self):
        expected = {r.name for r in run_after_py_change}
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(Path("test.py"), "changed", None)
            called_rules = {r.name for r in mock.call_args[0][0]}
            self.assertEqual(called_rules, expected)

    def test_requirements_triggers_requirements_rules(self):
        expected = {r.name for r in run_after_requirements_change}
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(
                    Path("requirements.txt"), "changed", None
                )
            called_rules = {r.name for r in mock.call_args[0][0]}
            self.assertEqual(called_rules, expected)

    def test_abstra_json_triggers_config_rules(self):
        expected = {r.name for r in run_after_abstra_json_change}
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(Path("abstra.json"), "changed", None)
            called_rules = {r.name for r in mock.call_args[0][0]}
            self.assertEqual(called_rules, expected)

    def test_env_triggers_env_rules(self):
        expected = {r.name for r in run_after_env_or_gitignore_change}
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(Path(".env"), "changed", None)
            called_rules = {r.name for r in mock.call_args[0][0]}
            self.assertEqual(called_rules, expected)

    def test_gitignore_triggers_env_rules(self):
        expected = {r.name for r in run_after_env_or_gitignore_change}
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(Path(".gitignore"), "changed", None)
            called_rules = {r.name for r in mock.call_args[0][0]}
            self.assertEqual(called_rules, expected)

    def test_random_file_triggers_nothing(self):
        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            from abstra_internals.controllers.linter_events import LinterEventController

            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(Path("readme.md"), "changed", None)
            mock.assert_not_called()
