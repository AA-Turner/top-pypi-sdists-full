"""Contract tests for LocalLinterRepository's serial execution mode (PR1, TDD).

The sidecar child runs rules serially (serial=True). The in-process
kill-switch path keeps today's thread-per-rule fan-out (default serial=False).
Failure semantics (both modes): a rule that raises never aborts the run and
materializes as a status="failed" check with no issues, instead of silently
vanishing from the results.
"""

import threading
import unittest

from abstra_internals.repositories.linter.models import (
    LinterIssue,
    LinterRule,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from tests.fixtures import clear_dir, init_dir


class _OkRuleOne(LinterRule):
    label = "ok one"
    type = "info"

    def __init__(self, log):
        self.log = log

    def find_issues(self):
        self.log.append((self.name, threading.current_thread()))
        return []


class _OkRuleTwo(LinterRule):
    label = "ok two"
    type = "info"

    def __init__(self, log):
        self.log = log

    def find_issues(self):
        self.log.append((self.name, threading.current_thread()))
        return []


class _BoomRule(LinterRule):
    label = "boom"
    type = "info"

    def find_issues(self):
        raise RuntimeError("rule exploded")


class _FlakyBlockingRule(LinterRule):
    """Succeeds (with one issue) until `broken` is flipped, then crashes."""

    label = "flaky blocking"
    type = "error"

    def __init__(self):
        self.broken = False

    def find_issues(self):
        if self.broken:
            raise RuntimeError("rule exploded")
        issue = LinterIssue()
        issue.label = "real issue"
        issue.fixes = []
        return [issue]


class _ScopedFakeRule(PathScopedLinterRule):
    label = "scoped fake"
    type = "info"

    def __init__(self, issues_by_path):
        self.issues_by_path = dict(issues_by_path)

    def _issue(self, label, path_key):
        issue = LinterIssue()
        issue.label = label
        issue.fixes = []
        issue.path = path_key
        return issue

    def find_issues(self, path=None):
        if path is not None:
            key = linter_path_key(path)
            return [
                self._issue(label, key) for label in self.issues_by_path.get(key, [])
            ]
        issues = []
        for key, labels in self.issues_by_path.items():
            issues.extend(self._issue(label, key) for label in labels)
        return issues


class SerialExecutionTest(unittest.TestCase):
    def setUp(self):
        self.root = init_dir()

    def tearDown(self):
        clear_dir(self.root)

    def test_serial_runs_in_caller_thread(self):
        log = []
        repo = LocalLinterRepository(serial=True)
        repo.update_specific_checks([_OkRuleOne(log), _OkRuleTwo(log)])

        self.assertEqual(len(log), 2)
        threads = {thread for _, thread in log}
        self.assertEqual(threads, {threading.current_thread()})
        names = {c.name for c in repo.checks}
        self.assertEqual(names, {"_OkRuleOne", "_OkRuleTwo"})

    def test_serial_materializes_failing_rule_and_keeps_going(self):
        log = []
        repo = LocalLinterRepository(serial=True)
        repo.update_specific_checks([_OkRuleOne(log), _BoomRule(), _OkRuleTwo(log)])

        names = {c.name for c in repo.checks}
        self.assertEqual(names, {"_OkRuleOne", "_BoomRule", "_OkRuleTwo"})
        self.assertEqual(len(log), 2)

        boom = next(c for c in repo.checks if c.name == "_BoomRule")
        self.assertEqual(boom.status, "failed")
        self.assertEqual(boom.issues, [])
        ok = next(c for c in repo.checks if c.name == "_OkRuleOne")
        self.assertEqual(ok.status, "ok")

    def test_threaded_default_runs_in_worker_threads(self):
        log = []
        repo = LocalLinterRepository()
        repo.update_specific_checks([_OkRuleOne(log)])

        self.assertEqual(len(log), 1)
        _, thread = log[0]
        self.assertNotEqual(thread, threading.current_thread())
        self.assertTrue(thread.name.startswith("LinterCheck["))

    def test_threaded_default_materializes_failing_rule(self):
        # Parity with serial mode: the worker catches the crash and appends a
        # failed check instead of letting the thread die silently.
        log = []
        repo = LocalLinterRepository()
        repo.update_specific_checks([_OkRuleOne(log), _BoomRule()])
        names = {c.name for c in repo.checks}
        self.assertEqual(names, {"_OkRuleOne", "_BoomRule"})
        boom = next(c for c in repo.checks if c.name == "_BoomRule")
        self.assertEqual(boom.status, "failed")

    def test_failed_check_replaces_stale_check_on_merge(self):
        # A rule that crashes on a merged pass must not leave its previous
        # (stale) issues alive: the failed check replaces the old one.
        rule = _FlakyBlockingRule()
        repo = LocalLinterRepository(serial=True)
        repo.update_specific_checks([rule])
        self.assertEqual(len(repo.checks[0].issues), 1)

        rule.broken = True
        repo.update_specific_checks([rule])
        check = repo.checks[0]
        self.assertEqual(check.status, "failed")
        self.assertEqual(check.issues, [])

    def test_failed_blocking_rule_blocks_and_message_says_verify(self):
        from abstra_internals.repositories.linter.models import deploy_gate_message

        rule = _FlakyBlockingRule()
        rule.broken = True
        repo = LocalLinterRepository(serial=True)
        repo.update_specific_checks([rule])

        blocking = repo.get_blocking_checks()
        self.assertEqual([c.name for c in blocking], ["_FlakyBlockingRule"])
        message = deploy_gate_message(blocking)
        self.assertIn("Could not verify", message)
        self.assertIn("flaky blocking", message)

        # Real issues take precedence over the could-not-verify wording.
        rule.broken = False
        repo.update_specific_checks([rule])
        blocking = repo.get_blocking_checks()
        message = deploy_gate_message(blocking)
        self.assertIn("fix all linter issues", message)

    def test_serial_scoped_merge_matches_threaded(self):
        a_path = self.root / "a.py"
        b_path = self.root / "b.py"

        states = {}
        for label, serial in (("threaded", False), ("serial", True)):
            rule = _ScopedFakeRule(
                {
                    linter_path_key(a_path): ["issue in a"],
                    linter_path_key(b_path): ["issue in b"],
                }
            )
            repo = LocalLinterRepository(serial=serial)
            repo.update_specific_checks([rule])

            rule.issues_by_path[linter_path_key(a_path)] = []
            repo.update_specific_checks([rule], paths=[a_path])
            states[label] = [c.to_dict() for c in repo.checks]

        self.assertEqual(states["threaded"], states["serial"])
        labels = {issue["label"] for issue in states["serial"][0]["issues"]}
        self.assertEqual(labels, {"issue in b"})


if __name__ == "__main__":
    unittest.main()
