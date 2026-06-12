import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from abstra_internals.repositories.linter.models import (
    LinterCheck,
    LinterIssue,
    LinterRule,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.linter.rules import rules


class LinterRepository(ABC):
    checks: List[LinterCheck] = []

    @abstractmethod
    def find_issues_in_codebase(self) -> List[LinterCheck]:
        pass

    @abstractmethod
    def update_checks(self) -> List[LinterCheck]:
        pass

    @abstractmethod
    def update_specific_checks(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> List[LinterCheck]:
        pass

    @abstractmethod
    def fix_issue_in_codebase(self, rule_name: str, fix_name: str) -> bool:
        pass

    @abstractmethod
    def fix_all_linters(self):
        pass

    @abstractmethod
    def get_blocking_checks(self) -> List[LinterCheck]:
        pass

    @abstractmethod
    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        pass


def check_rule(rule, checks_list):
    check = rule.check()
    checks_list.append(check)


LINTER_TYPE_PRIORITY = {"security": 0, "error": 1, "bug": 2, "warning": 3, "info": 4}
BLOCKING_TYPES = {"error", "security", "bug"}


class LocalLinterRepository(LinterRepository):
    def __init__(self):
        self.checks: List[LinterCheck] = []
        # Single-flight lock: prevents concurrent callers (boot _initial_lint
        # racing the first HTTP /check, or overlapping save-triggered lints)
        # from each spawning their own thread-per-rule fan-out.
        self._run_lock = threading.Lock()

    def find_issues_in_codebase(self) -> List[LinterCheck]:
        """
        Retrieve all linter checks that have been performed on the project.

        This method returns the cached list of all linter checks from the most recent
        analysis run. Each check represents a specific rule that was evaluated against
        the project code, including any issues found and available fixes.

        Returns:
            List[LinterCheck]: List of linter check objects, each containing:
                - name: Unique identifier for the linter rule
                - type: Severity level ('info', 'warning', 'error', 'security', 'bug')
                - description: Human-readable description of what the rule checks
                - issues: List of specific issues found by this rule
                - fixes: Available automatic fixes for the issues
            ```

        Note:
            - Returns cached results from the last update_checks() call
            - Empty list if update_checks() has never been called
            - Issues include file location and line number information
            - Fixes can be applied automatically using fix_linter() method
            - Check types determine severity and whether they block deployment

        Copywritings:
            Retrieve all linter checks
            Retrieving all linter checks...
        """
        if self.checks:
            return self.checks
        # Non-blocking acquire: if another caller is already running the
        # fan-out, return the current state (possibly empty during boot)
        # instead of spawning a second fan-out or blocking the HTTP thread.
        # The /events WebSocket backfills the populated checks on completion.
        if not self._run_lock.acquire(blocking=False):
            return self.checks
        try:
            if self.checks:
                return self.checks
            # Call _run_rules directly (NOT update_checks) — _run_lock is
            # non-reentrant and we already hold it.
            self._run_rules(rules, merge=False)
            return self.checks
        finally:
            self._run_lock.release()

    def update_checks(self):
        with self._run_lock:
            return self._run_rules(rules, merge=False)

    def update_specific_checks(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> List[LinterCheck]:
        with self._run_lock:
            return self._run_rules(target_rules, merge=True, paths=paths)

    def _execute_rules(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> Tuple[List[LinterCheck], List[Tuple[LinterRule, List[LinterIssue]]]]:
        """Run rules on threads. Returns (full_checks, scoped_results).

        Rules that support path-scoping run only on `paths` (when given) and
        land in scoped_results — their issues must be merged per-path into the
        existing check instead of replacing it.
        """
        new_checks: List[LinterCheck] = []
        scoped_results: List[Tuple[LinterRule, List[LinterIssue]]] = []
        threads = []

        def check_rule_scoped(rule: PathScopedLinterRule, scope: List[Path]):
            issues: List[LinterIssue] = []
            for path in scope:
                issues.extend(rule.find_issues(path))
            scoped_results.append((rule, issues))

        for rule in target_rules:
            if paths is not None and isinstance(rule, PathScopedLinterRule):
                thread = threading.Thread(
                    target=check_rule_scoped,
                    args=(rule, paths),
                    name=f"LinterCheck[{rule.name}]",
                )
            else:
                thread = threading.Thread(
                    target=check_rule,
                    args=(rule, new_checks),
                    name=f"LinterCheck[{rule.name}]",
                )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return new_checks, scoped_results

    def _merge_scoped_check(
        self,
        rule: LinterRule,
        new_issues: List[LinterIssue],
        scope_keys: set,
    ) -> LinterCheck:
        """Build the updated check for a path-scoped run: keep the previous
        issues outside the re-linted paths (other files + project-global ones,
        with their live fix objects) and swap in the fresh issues."""
        old_check = next((c for c in self.checks if c.name == rule.name), None)
        kept_issues = (
            [i for i in old_check.issues if i.path not in scope_keys]
            if old_check
            else []
        )
        return LinterCheck(
            name=rule.name,
            label=rule.label,
            type=rule.type,
            issues=kept_issues + new_issues,
            fix_with_ai=rule.fix_with_ai,
        )

    def _run_rules(
        self,
        target_rules: List[LinterRule],
        merge: bool,
        paths: Optional[List[Path]] = None,
    ) -> List[LinterCheck]:
        new_checks, scoped_results = self._execute_rules(target_rules, paths=paths)

        if scoped_results:
            scope_keys = {linter_path_key(p) for p in paths or []}
            for rule, issues in scoped_results:
                new_checks.append(self._merge_scoped_check(rule, issues, scope_keys))

        if merge:
            updated_names = {c.name for c in new_checks}
            merged = [c for c in self.checks if c.name not in updated_names]
            merged.extend(new_checks)
            merged.sort(key=lambda c: LINTER_TYPE_PRIORITY.get(c.type, 4))
            self.checks = merged
        else:
            new_checks.sort(key=lambda c: LINTER_TYPE_PRIORITY.get(c.type, 4))
            self.checks = new_checks

        return self.checks

    def fix_issue_in_codebase(self, rule_name: str, fix_name: str):
        """
        Apply a specific automatic fix for a linter issue.

        This method searches for a specific linter rule and fix combination,
        then applies the fix automatically. It's used to resolve individual
        linter issues without affecting other parts of the code.

        Args:
            rule_name (str): Name of the linter rule that found the issue.
                Must match exactly with the rule name from get_checks().
            fix_name (str): Name of the specific fix to apply.
                Must match exactly with a fix name available for the rule's issues.

        Returns:
            bool: True if the fix was found and applied successfully, False otherwise.

        Example:
            ```python
            linter_repo = LocalLinterRepository()
            linter_repo.update_checks()

            checks = linter_repo.get_checks()

            # Find issues that can be fixed
            for check in checks:
                if check.issues:
                    print(f"Rule: {check.name}")
                    for issue in check.issues:
                        for fix in issue.fixes:
                            print(f"Available fix: {fix.name}")

                            # Apply a specific fix
                            success = linter_repo.fix_linter(check.name, fix.name)
                            if success:
                                print(f"✓ Applied fix: {fix.name}")
                            else:
                                print(f"✗ Failed to apply fix: {fix.name}")

            # Example: Fix a specific formatting issue
            success = linter_repo.fix_linter("code_formatting", "add_missing_imports")
            if success:
                print("Import formatting fixed!")

            # Example: Fix security vulnerability
            success = linter_repo.fix_linter("security_check", "sanitize_input")
            if success:
                print("Security issue resolved!")
            else:
                print("Fix not found or failed to apply")

            # Re-run checks to see if issues were resolved
            linter_repo.update_checks()
            updated_checks = linter_repo.get_checks()
            ```

        Note:
            - Rule and fix names are case-sensitive and must match exactly
            - Returns False if rule_name or fix_name is not found
            - Applies the fix immediately to the project files
            - Some fixes may modify multiple files or lines of code
            - Re-run update_checks() after fixing to see updated results
            - Use get_checks() first to see available rules and fixes

        Copywritings:
            Apply a specific automatic fix for a linter issue
            Applying a specific automatic fix for a linter issue...
        """
        for check in self.checks:
            if check.name == rule_name:
                for issue in check.issues:
                    for fix in issue.fixes:
                        if fix.name == fix_name:
                            fix.fix()
                            self._update_check_for_rule(rule_name)
                            return True
        return False

    def _update_check_for_rule(self, rule_name: str):
        """Re-run the check for a specific rule and update the cache."""
        # Hold the single-flight lock: this re-runs rule.check() and rebinds
        # self.checks, which would otherwise race a concurrent fan-out.
        # fix_issue_in_codebase is the only caller and does not hold the
        # lock, so there is no re-entrancy.
        with self._run_lock:
            for rule in rules:
                if rule.name == rule_name:
                    new_check = rule.check()
                    self.checks = [
                        new_check if check.name == rule_name else check
                        for check in self.checks
                    ]
                    break

    def fix_all_linters(self):
        for check in self.checks:
            if check.type != "info":
                for issue in check.issues:
                    for fix in issue.fixes:
                        fix.fix()

    def get_blocking_checks(self) -> List[LinterCheck]:
        return [
            check
            for check in self.checks
            if check.type in BLOCKING_TYPES and check.issues
        ]

    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        blocking_rules = [r for r in rules if r.type in BLOCKING_TYPES]
        self.update_specific_checks(blocking_rules)
        return self.get_blocking_checks()


class ProductionLinterRepository(LinterRepository):
    """
    This is a dummy repository. Linters are not available in production.
    """

    def find_issues_in_codebase(self) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")

    def update_checks(self) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")

    def update_specific_checks(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")

    def fix_issue_in_codebase(self, rule_name: str, fix_name: str) -> bool:
        raise NotImplementedError("Linters are not available in production.")

    def fix_all_linters(self):
        raise NotImplementedError("Linters are not available in production.")

    def get_blocking_checks(self) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")

    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")
