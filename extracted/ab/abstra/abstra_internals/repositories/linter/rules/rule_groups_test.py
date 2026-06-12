from pathlib import Path
from unittest.mock import patch

from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
    PathScopedLinterRule,
    linter_path_key,
)
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


class PyreflyBufferIsFilteredOutInLintFiles(BaseTest):
    """lint_files must not trigger a lint pass for .pyrefly_buffer.py — the
    PyreflyLSP rewrites that scratch file on every type-check."""

    def setUp(self):
        super().setUp()
        self.repos = self.controller.repositories
        self.event_controller = CodebaseEventController(self.repos)

    def test_pyrefly_buffer_does_not_trigger_lint(self):
        from abstra_internals.controllers.linter_events import LinterEventController

        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(
                    Path(".pyrefly_buffer.py"), "changed", None
                )
        mock.assert_not_called()


class _FakeScopedRule(PathScopedLinterRule):
    """Scoped rule with controllable per-file + global issues."""

    label = "Fake scoped rule"
    type = "info"

    def __init__(self, issues_by_path: dict, global_issues: list):
        # path key (linter_path_key format) -> list of labels; global issues
        # are only returned by full (unscoped) runs.
        self.issues_by_path = issues_by_path
        self.global_issues = global_issues

    def _issue(self, label, path_key):
        issue = LinterIssue()
        issue.label = label
        issue.fixes = []
        issue.path = path_key
        return issue

    def find_issues(self, path=None):
        if path is not None:
            key = linter_path_key(path)
            return [self._issue(lbl, key) for lbl in self.issues_by_path.get(key, [])]
        issues = [self._issue(lbl, None) for lbl in self.global_issues]
        for key, labels in self.issues_by_path.items():
            issues.extend(self._issue(lbl, key) for lbl in labels)
        return issues


class PathScopedMergeTest(BaseTest):
    """update_specific_checks(paths=...) merges per-(rule, path) instead of
    replacing the whole check."""

    def _check(self, repo, rule):
        return next(c for c in repo.checks if c.name == rule.name)

    def test_scoped_run_preserves_other_files_and_global_issues(self):
        rule = _FakeScopedRule(
            {"a.py": ["issue in a"], "b.py": ["issue in b"]},
            global_issues=["global issue"],
        )
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule])  # full seed
        self.assertEqual(len(self._check(repo, rule).issues), 3)

        # a.py fixed: scoped re-run must drop only a.py's issue
        rule.issues_by_path["a.py"] = []
        repo.update_specific_checks([rule], paths=[Path("a.py")])

        labels = {i.label for i in self._check(repo, rule).issues}
        self.assertEqual(labels, {"issue in b", "global issue"})

    def test_scoped_run_replaces_issues_of_relinted_path(self):
        rule = _FakeScopedRule({"a.py": ["old issue in a"]}, global_issues=[])
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule])

        rule.issues_by_path["a.py"] = ["new issue in a"]
        repo.update_specific_checks([rule], paths=[Path("a.py")])

        labels = {i.label for i in self._check(repo, rule).issues}
        self.assertEqual(labels, {"new issue in a"})

    def test_scoped_run_evicts_issues_of_deleted_path(self):
        rule = _FakeScopedRule({"a.py": ["issue in a"]}, global_issues=[])
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule])

        # File gone: scoped run yields nothing for a.py → issue evicted
        rule.issues_by_path = {}
        repo.update_specific_checks([rule], paths=[Path("a.py")])
        self.assertEqual(self._check(repo, rule).issues, [])

    def test_scoped_run_without_prior_check_uses_fresh_issues(self):
        rule = _FakeScopedRule({"a.py": ["issue in a"]}, global_issues=[])
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule], paths=[Path("a.py")])
        labels = {i.label for i in self._check(repo, rule).issues}
        self.assertEqual(labels, {"issue in a"})

    def test_unscoped_rule_with_paths_falls_back_to_full_run(self):
        calls = []

        class _FullRule(LinterRule):
            label = "Full rule"
            type = "info"

            def find_issues(self):
                calls.append("full")
                return []

        rule = _FullRule()
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule], paths=[Path("a.py")])
        self.assertEqual(calls, ["full"])
        self.assertEqual(self._check(repo, rule).issues, [])

    def test_scoped_run_keeps_live_fix_objects_of_other_paths(self):
        rule = _FakeScopedRule(
            {"a.py": ["issue in a"], "b.py": ["issue in b"]}, global_issues=[]
        )
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule])
        b_issue = next(i for i in self._check(repo, rule).issues if i.path == "b.py")

        repo.update_specific_checks([rule], paths=[Path("a.py")])
        kept = next(i for i in self._check(repo, rule).issues if i.path == "b.py")
        self.assertIs(kept, b_issue)


class LintFilesScopingTest(BaseTest):
    """lint_files passes a path scope for source files and no scope for
    config files."""

    def setUp(self):
        super().setUp()
        self.repos = self.controller.repositories
        self.event_controller = CodebaseEventController(self.repos)
        # The content-hash gate is class-level state; a previous test linting
        # the same relative path with identical content would gate this one.
        CodebaseEventController._content_hashes.clear()

    def _lint(self, filepath):
        from abstra_internals.controllers.linter_events import LinterEventController

        with patch.object(
            self.repos.linter, "update_specific_checks", return_value=[]
        ) as mock:
            with patch.object(LinterEventController, "broadcast"):
                self.event_controller.lint_files(filepath, "changed", None)
        return mock

    def test_py_event_is_path_scoped(self):
        mock = self._lint(Path("test.py"))
        self.assertEqual(mock.call_args.kwargs["paths"], [Path("test.py")])

    def test_requirements_event_is_unscoped(self):
        mock = self._lint(Path("requirements.txt"))
        self.assertIsNone(mock.call_args.kwargs["paths"])

    def test_abstra_json_event_is_unscoped(self):
        mock = self._lint(Path("abstra.json"))
        self.assertIsNone(mock.call_args.kwargs["paths"])


class ScheduleLintScopeAccumulationTest(BaseTest):
    """The debounce accumulates (rule → paths); an unscoped event is sticky."""

    def setUp(self):
        super().setUp()
        self._cls = CodebaseEventController
        self._cls.configure(self.controller.repositories, controller_driven=True)

    def tearDown(self):
        if self._cls._lint_timer is not None:
            self._cls._lint_timer.cancel()
            self._cls._lint_timer = None
        self._cls._pending_rules = {}
        self._cls._pending_scopes = {}
        self._cls._pending_full = False
        self._cls._controller_driven = False
        self._cls._repositories = None
        super().tearDown()

    def test_paths_accumulate_across_debounce(self):
        with patch.object(self._cls, "_run_pending_lint"):
            self._cls._schedule_lint(rules=run_after_py_change, scope=Path("a.py"))
            self._cls._schedule_lint(rules=run_after_py_change, scope=Path("b.py"))
            name = run_after_py_change[0].name
            self.assertEqual(
                self._cls._pending_scopes[name], {Path("a.py"), Path("b.py")}
            )

    def test_unscoped_event_overrides_accumulated_paths(self):
        with patch.object(self._cls, "_run_pending_lint"):
            self._cls._schedule_lint(rules=run_after_py_change, scope=Path("a.py"))
            self._cls._schedule_lint(rules=run_after_py_change, scope=None)
            self._cls._schedule_lint(rules=run_after_py_change, scope=Path("b.py"))
            name = run_after_py_change[0].name
            self.assertIsNone(self._cls._pending_scopes[name])
