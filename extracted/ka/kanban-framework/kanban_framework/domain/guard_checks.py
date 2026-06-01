"""Internal guard checks — private _check_* methods used by Guard.

Extracted from guard.py for maintainability. All methods operate on Task
and Filesystem, returning CheckResult. Import via Guard._checks property.
"""
from __future__ import annotations

import re
from pathlib import Path

from kanban_framework.types import Task, Phase
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.guard import CheckResult


class GuardChecks:
    """Collection of internal guard check methods.

    Instantiated by Guard, shares the same fs/config references.
    """

    def __init__(self, fs: Filesystem, config: Config):
        self._fs = fs
        self._cfg = config

    def check_knowledge_artifact(self, task: Task, filename: str, hint: str) -> CheckResult:
        """Check a knowledge artifact exists — non-blocking warning by default. (#236)"""
        td = self._fs.task_dir(task.id)
        f = td / filename
        if self._fs.file_exists(f) and f.stat().st_size > 0:
            return CheckResult(passed=True)
        return CheckResult(passed=True, warnings=[f"{filename} missing — {hint}"])

    def _get_execute_guard(self, mode: str | None = None) -> dict:
        """Read guard config for execute phase from workflow.json.

        Priority: modes.<mode>.phases[].guard → top-level phases[].guard → {}
        """
        workflow = self._cfg.workflow
        if mode:
            modes_cfg = workflow.get("modes", {})
            mode_cfg = modes_cfg.get(mode, {}) if isinstance(modes_cfg, dict) else {}
            mode_phases = mode_cfg.get("phases", []) if isinstance(mode_cfg, dict) else []
            for p in mode_phases:
                if isinstance(p, dict) and p.get("id") == "execute":
                    g = p.get("guard")
                    if isinstance(g, dict):
                        return g
        for p in workflow.get("phases", []):
            if isinstance(p, dict) and p.get("id") == "execute":
                g = p.get("guard")
                if isinstance(g, dict):
                    return g
        return {}

    def check_quick_scope(self, task: Task) -> CheckResult:
        """Check quick mode changes stay within scope. (#331, #396)"""
        from kanban_framework.infra.git import Git
        repo_root = self._fs._root
        if not (repo_root / ".git").is_dir():
            return CheckResult(passed=True)
        try:
            git = Git(repo_root)
            stat = git.diff_stat()
        except Exception:
            return CheckResult(passed=True)
        # Filter out .kanban/ internal files — only count source code changes
        source_files = [f for f in stat.get("file_list", [])
                        if not f.startswith(".kanban/")]
        files_changed = len(source_files)
        warnings = []
        limits = self._get_execute_guard(getattr(task, 'mode', None)).get("quick_limits", {})
        _MAX_FILES = limits.get("max_files", 3)
        _MAX_TOTAL_LINES = limits.get("max_total_lines", 40)
        _MAX_ADDED_LINES = limits.get("max_added_lines", 20)
        total_lines = stat["added"] + stat["deleted"]
        if files_changed > _MAX_FILES:
            warnings.append(
                f"Quick 模式修改了 {files_changed} 个文件，超出上限（≤{_MAX_FILES}）")
        if total_lines > _MAX_TOTAL_LINES:
            warnings.append(
                f"Quick 模式总改动 {total_lines} 行（+{stat['added']}/-{stat['deleted']}），"
                f"超出上限（≤{_MAX_TOTAL_LINES}）")
        if stat["added"] > _MAX_ADDED_LINES:
            warnings.append(
                f"Quick 模式新增 {stat['added']} 行，超出预期（≤{_MAX_ADDED_LINES}）")
        if stat["deleted"] > stat["added"] * 2:
            warnings.append(
                f"删除 {stat['deleted']} 行远超新增 {stat['added']} 行，可能存在非 bug fix 的重构")
        return CheckResult(passed=len(warnings) == 0, warnings=warnings)

    def check_knowledge_references(self, task: Task) -> CheckResult:
        """Check spec.md and plan files contain knowledge references (K-NNN format)."""
        td = self._fs.task_dir(task.id)
        ref_pattern = re.compile(r'[A-Za-z]*\d{3,}')
        files_to_check = [td / "spec.md"]
        plan_dir = td / "plan"
        if plan_dir.is_dir():
            files_to_check.extend(sorted(plan_dir.glob("*.md")))

        found_refs = set()
        for f in files_to_check:
            if not self._fs.file_exists(f):
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            found_refs.update(ref_pattern.findall(text))

        if found_refs:
            return CheckResult(passed=True,
                warnings=[f"Knowledge refs in artifacts: {sorted(found_refs)}"])
        return CheckResult(passed=True,
            warnings=["No knowledge references (K-NNN) found in spec.md or plan/*.md — "
                       "task may lack knowledge base integration"])

    def check_file(self, task: Task, filename: str) -> CheckResult:
        task_dir = self._fs.task_dir(task.id)
        candidates = [
            task_dir / filename,
        ]
        iteration_dir = self._fs.iteration_dir(task.id, task.iteration)
        candidates.append(iteration_dir / filename)
        # New subdirectory structure: reviews/ execute/ evaluate/
        candidates.append(iteration_dir / "reviews" / filename)
        candidates.append(iteration_dir / "execute" / filename)
        candidates.append(iteration_dir / "evaluate" / filename)
        candidates.append(task_dir / "plan" / filename)
        # task_dir phase subdirectories (agent may place files here)
        candidates.append(task_dir / "execute" / filename)
        candidates.append(task_dir / "evaluate" / filename)
        candidates.append(task_dir / "reviews" / filename)
        # Old report dir (backward compat)
        candidates.append(iteration_dir / "reports" / filename)

        # Also check round-suffixed versions (_r1, _r2, ...) in reviews/
        # for multi-round review phases (#157)
        if filename.endswith("_report.json"):
            base = filename.replace(".json", "")
            reviews_dir = iteration_dir / "reviews"
            if reviews_dir.is_dir():
                for f in sorted(reviews_dir.glob(f"{base}_r*.json")):
                    candidates.append(f)

        for filepath in candidates:
            if self._fs.file_exists(filepath):
                if filepath.stat().st_size == 0:
                    return CheckResult(passed=False, failures=[f"{filename} is empty"])
                return CheckResult(passed=True)

        return CheckResult(passed=False, failures=[f"{filename} missing"])

    def check_test_files(self, task: Task) -> CheckResult:
        """IR-10: Verify test files exist alongside implementation files."""
        if not task.worktree_path:
            return CheckResult(passed=True)
        wt = Path(task.worktree_path)
        cfg = self._cfg
        output_dir = cfg.raw.get("output_dir", "src")
        code_dir = wt / output_dir
        if not code_dir.exists():
            return CheckResult(passed=True)
        test_patterns = ["test_*.py", "*_test.py", "*.test.js", "*.spec.ts"]
        source_patterns = ["*.py", "*.js", "*.ts"]
        source_files: list[Path] = []
        for pat in source_patterns:
            source_files.extend(code_dir.rglob(pat))
        test_files: list[Path] = []
        for pat in test_patterns:
            test_files.extend(code_dir.rglob(pat))
        if source_files and not test_files:
            return CheckResult(
                passed=False,
                failures=["no test files found — IR-10 requires tests for all code changes"],
            )
        return CheckResult(passed=True)

    def check_tdd_evidence(self, task: Task) -> CheckResult:
        """Verify TDD evidence table in execution_summary.md.

        Checks that the TDD evidence table exists and each row shows
        RED=FAIL (not PASS), proving tests were written before code.
        Quick and lightweight modes are exempt — only full mode requires TDD evidence.
        """
        if getattr(task, 'mode', '') in ('quick', 'lightweight'):
            return CheckResult(passed=True)
        if task.lightweight:
            return CheckResult(passed=True)
        task_dir = self._fs.task_dir(task.id)
        iter_dir = self._fs.iteration_dir(task.id, task.iteration)
        # Search all common locations (#343)
        candidates = [
            iter_dir / "execution_summary.md",
            iter_dir / "execute" / "execution_summary.md",
            task_dir / "execution_summary.md",
        ]
        summary_file = None
        for c in candidates:
            if self._fs.file_exists(c):
                summary_file = c
                break
        if summary_file is None:
            return CheckResult(
                passed=False,
                failures=["execution_summary.md missing — cannot verify TDD evidence"],
            )
        content = summary_file.read_text(encoding="utf-8")

        # Look for the TDD evidence table header
        if "## TDD 执行证据" not in content:
            return CheckResult(
                passed=False,
                failures=[
                    "TDD evidence table missing in execution_summary.md — "
                    "must contain '## TDD 执行证据' section. Expected format:\n"
                    "## TDD 执行证据\n"
                    "| 功能点 | 测试文件 | RED (Fail) | GREEN (Pass) | 备注 |\n"
                    "|--------|----------|------------|--------------|------|\n"
                    "| feature | test_X.py | FAIL: reason | PASS | note |"
                ],
            )

        # Extract table rows (lines starting with | after the header)
        tdd_section = content.split("## TDD 执行证据")[1]
        if "## " in tdd_section:
            tdd_section = tdd_section.split("## ")[0]

        rows = [line.strip() for line in tdd_section.split("\n")
                if line.strip().startswith("|") and "RED" not in line
                and "---" not in line and "功能点" not in line]

        if not rows:
            return CheckResult(
                passed=False,
                failures=["TDD evidence table has no data rows — each feature point needs a RED→GREEN evidence row"],
            )

        # Check each row for RED=FAIL evidence
        failures = []
        for row in rows:
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if len(cells) < 5:
                continue
            feature = cells[0]
            red_result = cells[2]
            # Regression/coverage tests: RED=PASS is expected (testing existing features)
            is_regression = any(kw in feature.lower() for kw in
                ("regression", "coverage", "验证", "回归", "覆盖率"))
            if is_regression:
                continue  # regression tests may have RED=PASS
            red_upper = red_result.upper()
            if "PASS" in red_upper and "FAIL" not in red_upper:
                failures.append(
                    f"{feature}: RED phase was PASS — test did not fail before implementation, "
                    "TDD not correctly executed (test didn't catch missing feature)"
                )
            elif "FAIL" not in red_upper and red_upper not in ("N/A", "SKIP", "-", "✅", "✔", "OK", "PASS"):
                # Broaden acceptance: strip common emoji/checkmarks and treat empty as OK
                import re as _re
                stripped = _re.sub(r'[✅✔✓🟢🟩💚⭕✖❌🔴🟥×✗☐☑]', '', red_result).strip()
                if stripped and stripped not in ("-", "N/A", "SKIP", "OK"):
                    failures.append(
                        f"{feature}: RED phase result unclear — must show FAIL with reason, got '{red_result}'"
                    )

        if failures:
            return CheckResult(passed=False, failures=failures)
        return CheckResult(passed=True)

    # --- test_spec.md coverage check (#387) ---
    _UT_PATTERN = re.compile(r"\b(UT-\d+)\b", re.IGNORECASE)
    _TEST_FILE_PATTERNS = ["test_*.py", "*_test.py", "*.test.js", "*.spec.ts"]

    def check_test_spec_coverage(self, task: Task) -> CheckResult:
        """Verify test_spec.md test cases are implemented in actual test files.

        Parses test_spec.md for UT-xxx identifiers, then searches test files
        in the worktree for those identifiers. Reports coverage ratio.
        """
        if getattr(task, 'mode', '') == 'quick':
            return CheckResult(passed=True)
        task_dir = self._fs.task_dir(task.id)
        spec_file = task_dir / "test_spec.md"
        if not spec_file.is_file():
            return CheckResult(passed=True)
        spec_text = spec_file.read_text(encoding="utf-8", errors="replace")
        required_ids = sorted(set(self._UT_PATTERN.findall(spec_text.upper())))
        if not required_ids:
            return CheckResult(passed=True)
        if not task.worktree_path:
            return CheckResult(passed=True)
        test_content = self._read_all_test_files(task.worktree_path)
        if not test_content:
            return CheckResult(
                passed=False,
                failures=[
                    f"test_spec.md defines {len(required_ids)} test cases ({', '.join(required_ids[:5])}...) "
                    "but no test files found in worktree"
                ],
            )
        covered = [uid for uid in required_ids if uid in test_content.upper()]
        missing = [uid for uid in required_ids if uid not in covered]
        ratio = len(covered) / len(required_ids)
        threshold = self._get_execute_guard(getattr(task, 'mode', None)).get("test_spec_coverage_threshold", 0.5)
        if ratio < threshold:
            return CheckResult(
                passed=False,
                failures=[
                    f"test_spec coverage {ratio:.0%}: {len(covered)}/{len(required_ids)} cases implemented. "
                    f"Missing: {', '.join(missing)}"
                ],
            )
        if missing:
            return CheckResult(
                passed=True,
                warnings=[
                    f"test_spec coverage {ratio:.0%}: missing {', '.join(missing)}"
                ],
            )
        return CheckResult(passed=True)

    def _read_all_test_files(self, worktree_path: str) -> str:
        wt = Path(worktree_path)
        parts: list[str] = []
        for pat in self._TEST_FILE_PATTERNS:
            for f in wt.rglob(pat):
                try:
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
        return "\n".join(parts)
