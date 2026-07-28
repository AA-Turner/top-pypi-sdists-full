import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.context import (
    LintContext,
    reset_lint_context,
    set_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterCheck,
    LinterIssue,
    LinterRule,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.linter.rules import (
    rules,
    run_after_package_install,
)

# The only event that changes the installed-package set the child's caches depend
# on is a package install/uninstall, which the editor signals by running exactly
# this rule group (unscoped). Matching it — instead of "any unscoped pass" — keeps
# the caches warm across boot/abstra.json/.env passes, so an unrelated config
# change no longer forces a cold packages_distributions/transitive recompute on
# the next save.
_PACKAGE_INSTALL_RULE_NAMES = frozenset(r.name for r in run_after_package_install)


# How long the deploy gate waits for a scheduled/in-flight lint to settle before
# giving up and re-verifying itself. Matches the sidecar deploy-gate timeout.
DEPLOY_GATE_WAIT_SECONDS = 120.0

RUN_NEVER = "never_run"
RUN_RUNNING = "running"
RUN_SUCCESS = "success"
RUN_FAILED = "failed"


class LinterRunGate:
    """Outcome of the last lint pass, so the deploy gate can trust the
    incrementally-maintained mirror instead of re-linting from scratch.

    ``mark_pending`` covers both a scheduled (debounced) and an in-flight pass —
    deploy waits on ``settled`` while pending. ``mark_success``/``mark_failed``
    resolve it: deploy trusts SUCCESS as a fresh full verdict and re-verifies on
    FAILED or NEVER_RUN. Thread-safe: the editor lints on a timer thread while
    the deploy gate reads from an HTTP thread.

    Pending passes are COUNTED: each ``mark_pending`` must be resolved by
    exactly one ``mark_success``/``mark_failed``, and the gate only settles
    when none remain. Otherwise a pass completing while another is scheduled
    (or between the groups of a partitioned run) would read as settled and let
    a deploy trust a mirror that misses the newest edit. The settled status is
    FAILED if any pass in the window failed (the mirror may be partially
    stale), SUCCESS only if all of them succeeded."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._status = RUN_NEVER
        self._pending = 0
        self._window_failed = False
        self._settled = threading.Event()
        self._settled.set()

    def mark_pending(self) -> None:
        with self._lock:
            self._pending += 1
            self._status = RUN_RUNNING
            self._settled.clear()

    def mark_success(self) -> None:
        self._resolve(failed=False)

    def mark_failed(self) -> None:
        self._resolve(failed=True)

    def _resolve(self, failed: bool) -> None:
        with self._lock:
            self._window_failed = self._window_failed or failed
            self._pending = max(0, self._pending - 1)
            if self._pending == 0:
                self._status = RUN_FAILED if self._window_failed else RUN_SUCCESS
                self._window_failed = False
                self._settled.set()

    @property
    def status(self) -> str:
        with self._lock:
            return self._status

    def wait_settled(self, timeout: float) -> bool:
        """Block until the pending/in-flight pass resolves. Returns False on
        timeout (caller then re-verifies rather than trusting a stuck state)."""
        return self._settled.wait(timeout)


class LinterRepository(ABC):
    checks: List[LinterCheck] = []
    # True when the last lint operation could not actually run and `checks` is
    # a stale mirror (e.g. the sidecar child is dead). In-process repositories
    # always run for real, so they never degrade.
    degraded: bool = False
    # Last-pass outcome, used by the deploy gate.
    run_gate: "LinterRunGate"

    @abstractmethod
    def find_issues_in_codebase(self) -> List[LinterCheck]:
        pass

    @abstractmethod
    def update_checks(self, revalidate_caches: bool = False) -> List[LinterCheck]:
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


def failed_check(rule: LinterRule) -> LinterCheck:
    """A rule that crashed still yields a check — with status="failed" and no
    issues — instead of silently vanishing from the results (which read as a
    pass) or, on merged passes, leaving its stale previous check alive."""
    return LinterCheck(
        name=rule.name,
        label=rule.label,
        issues=[],
        status="failed",
    )


def check_rule(rule, checks_list, context=None):
    # Publish the per-pass context into this thread's ContextVar so the rule
    # (which reads current_lint_context()) shares the single project load.
    # Threads don't inherit the caller's context vars, so each worker sets it.
    token = set_lint_context(context)
    try:
        check = rule.check()
        checks_list.append(check)
    except Exception as e:
        AbstraLogger.error(f"[Linter] rule {rule.name} crashed: {e}")
        AbstraLogger.capture_exception(e)
        checks_list.append(failed_check(rule))
    finally:
        reset_lint_context(token)


BLOCKING_TYPES = {"error"}


def check_is_blocking(check: LinterCheck) -> bool:
    if check.status == "failed":
        return True
    return any(issue.type in BLOCKING_TYPES for issue in check.issues)


# Fixes with process-level side effects (pip upgrade + editor restart) rather
# than a local file edit, so "fix all" must skip them. Keyed by fix name, not
# rule name: since RequirementsAnalyzer groups every requirements verdict, a
# rule-level exclusion would drop all its deterministic fixes too.
# UpdateAbstraToLatestVersion is here because it triggers a self-update
# (EditorUpdateController.trigger_update → pip install + editor restart); a bulk
# "fix all" must not restart the pod as a side effect.
BULK_FIX_EXCLUDED_FIXES: set[str] = {
    "UpdateAbstraToLatestVersion",
    # InstallRequirements calls restart_editor_and_workers on success.
    "InstallRequirements",
}


class LocalLinterRepository(LinterRepository):
    def __init__(self, serial: bool = False):
        self.checks: List[LinterCheck] = []
        # Single-flight lock: prevents concurrent callers (boot _initial_lint
        # racing the first HTTP /check, or overlapping save-triggered lints)
        # from each spawning their own thread-per-rule fan-out.
        self._run_lock = threading.Lock()
        # serial=True runs rules on the caller thread, one at a time — used by
        # the linter sidecar child, where thread-per-rule would only inflate
        # the pod's CFS throttle. Default keeps the threaded fan-out.
        self._serial = serial
        # Tracks the last pass's outcome
        self.run_gate = LinterRunGate()

    def find_issues_in_codebase(self) -> List[LinterCheck]:
        """
        Retrieve all linter checks that have been performed on the project.

        This method returns the cached list of all linter checks from the most recent
        analysis run. Each check represents a specific rule that was evaluated against
        the project code, including any issues found and available fixes.

        Returns:
            List[LinterCheck]: List of linter check objects, each containing:
                - name: Unique identifier for the linter rule
                - type: Severity level ('warning', 'error')
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

    def update_checks(self, revalidate_caches: bool = False):
        with self._run_lock:
            return self._run_rules(
                rules, merge=False, revalidate_caches=revalidate_caches
            )

    def update_specific_checks(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> List[LinterCheck]:
        with self._run_lock:
            return self._run_rules(target_rules, merge=True, paths=paths)

    def _execute_rules(
        self,
        target_rules: List[LinterRule],
        paths: Optional[List[Path]] = None,
        context: Optional[LintContext] = None,
    ) -> Tuple[List[LinterCheck], List[Tuple[LinterRule, List[LinterIssue]]]]:
        """Run rules on threads. Returns (full_checks, scoped_results).

        Rules that support path-scoping run only on `paths` (when given) and
        land in scoped_results — their issues must be merged per-path into the
        existing check instead of replacing it.

        `context` is the per-pass LintContext; each worker publishes it into its
        ContextVar (threads don't inherit the caller's) so all rules share one
        project load.
        """
        new_checks: List[LinterCheck] = []
        scoped_results: List[Tuple[LinterRule, List[LinterIssue]]] = []
        threads = []

        def check_rule_scoped(rule: PathScopedLinterRule, scope: List[Path]):
            token = set_lint_context(context)
            try:
                issues: List[LinterIssue] = []
                for path in scope:
                    issues.extend(rule.find_issues(path))
                scoped_results.append((rule, issues))
            except Exception as e:
                AbstraLogger.error(f"[Linter] rule {rule.name} crashed: {e}")
                AbstraLogger.capture_exception(e)
                # Into new_checks (not scoped_results): the failed check must
                # REPLACE the rule's previous one in the merge, not be merged
                # with the stale issues kept for unscoped paths.
                new_checks.append(failed_check(rule))
            finally:
                reset_lint_context(token)

        if self._serial:
            # Workers materialize their own failures as status="failed"
            # checks, so a raising rule never aborts the pass.
            for rule in target_rules:
                if paths is not None and isinstance(rule, PathScopedLinterRule):
                    check_rule_scoped(rule, paths)
                else:
                    check_rule(rule, new_checks, context)
            return new_checks, scoped_results

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
                    args=(rule, new_checks, context),
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
            issues=kept_issues + new_issues,
        )

    def _run_rules(
        self,
        target_rules: List[LinterRule],
        merge: bool,
        paths: Optional[List[Path]] = None,
        revalidate_caches: bool = False,
    ) -> List[LinterCheck]:
        self.run_gate.mark_pending()
        try:
            if {r.name for r in target_rules} == _PACKAGE_INSTALL_RULE_NAMES:
                self._refresh_install_sensitive_caches()

            # One context per pass: the project is loaded once and shared by every
            # rule (via the ContextVar the fan-out workers publish), instead of each
            # project-reading rule re-loading it under the class lock.
            context = LintContext(revalidate_caches=revalidate_caches)
            new_checks, scoped_results = self._execute_rules(
                target_rules, paths=paths, context=context
            )

            if scoped_results:
                scope_keys = {linter_path_key(p) for p in paths or []}
                for rule, issues in scoped_results:
                    new_checks.append(
                        self._merge_scoped_check(rule, issues, scope_keys)
                    )

            if merge:
                updated_names = {c.name for c in new_checks}
                merged = [c for c in self.checks if c.name not in updated_names]
                merged.extend(new_checks)
                merged.sort(key=lambda c: 0 if check_is_blocking(c) else 1)
                self.checks = merged
            else:
                new_checks.sort(key=lambda c: 0 if check_is_blocking(c) else 1)
                self.checks = new_checks
        except Exception:
            self.run_gate.mark_failed()
            raise
        self.run_gate.mark_success()
        return self.checks

    def _refresh_install_sensitive_caches(self) -> None:
        """Called only on the package-install pass (run_after_package_install) —
        the editor's signal after a package install/uninstall. Those invalidate()
        hooks fire in the EDITOR process, but the linter runs in a separate
        sidecar child whose in-memory caches would otherwise stay stale for up to
        the TTL. Narrowing to this pass (instead of any unscoped pass) means an
        abstra.json/.env change doesn't force a cold recompute on the next save.
        Imported locally to avoid an import cycle at module load."""
        from abstra_internals.repositories.linter.rules.conflicting_name import (
            _ReservedNamesCache,
        )
        from abstra_internals.services.requirements import (
            _PackagesDistributionsCache,
            _TransitiveDependenciesCache,
        )

        _PackagesDistributionsCache.invalidate()
        _TransitiveDependenciesCache.invalidate()
        _ReservedNamesCache.invalidate()

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
                    try:
                        new_check = rule.check()
                    except Exception as e:
                        AbstraLogger.error(f"[Linter] rule {rule.name} crashed: {e}")
                        AbstraLogger.capture_exception(e)
                        new_check = failed_check(rule)
                    self.checks = [
                        new_check if check.name == rule_name else check
                        for check in self.checks
                    ]
                    break

    def fix_all_linters(self):
        for check in self.checks:
            for issue in check.issues:
                for fix in issue.fixes:
                    if fix.name in BULK_FIX_EXCLUDED_FIXES:
                        continue
                    fix.fix()

    def get_blocking_checks(self) -> List[LinterCheck]:
        return [check for check in self.checks if check_is_blocking(check)]

    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        # Trust the incrementally-maintained mirror instead of re-linting every
        # deploy: wait for any scheduled/in-flight pass to settle, then re-verify
        # only if the last one couldn't be trusted (failed, or nothing ran yet).
        # A fresh SUCCESS mirror is the common case and needs no work.
        self.run_gate.wait_settled(DEPLOY_GATE_WAIT_SECONDS)
        with self._run_lock:
            if self.run_gate.status == RUN_SUCCESS and self.checks:
                return self.get_blocking_checks()
            # Failed / never ran / still pending after the wait — recompute a
            # full, fresh verdict (holds the lock; _run_rules is non-reentrant).
            self._run_rules(rules, merge=False)
            return self.get_blocking_checks()


class ProductionLinterRepository(LinterRepository):
    """
    This is a dummy repository. Linters are not available in production.
    """

    def find_issues_in_codebase(self) -> List[LinterCheck]:
        raise NotImplementedError("Linters are not available in production.")

    def update_checks(self, revalidate_caches: bool = False) -> List[LinterCheck]:
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
