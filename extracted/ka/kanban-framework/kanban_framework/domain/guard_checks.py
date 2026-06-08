"""Internal guard checks — private _check_* methods used by Guard.

Extracted from guard.py for maintainability. All methods operate on Task
and Filesystem, returning CheckResult. Import via Guard._checks property.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from kanban_framework.types import Task, Phase
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config


# Field names agents may use for matched entries in knowledge_used.json
_MATCHED_FIELD_NAMES = (
    "matched", "matched_knowledge", "matched_entries",
    "selected_entries", "entries", "items", "results", "relevant",
)

_NO_MATCH_REASON_FIELDS = (
    "no_match_reason", "unmatched_reason", "fallback_reason",
    "empty_reason", "reason", "no_match_explanation",
)


def _extract_matched_entries(data: dict) -> list:
    """Extract matched entries from knowledge_used.json, tolerating any field name."""
    for field in _MATCHED_FIELD_NAMES:
        val = data.get(field)
        if isinstance(val, list) and val:
            return val
    # Fallback: find any top-level list containing dicts with id/title
    for val in data.values():
        if (isinstance(val, list) and val
                and isinstance(val[0], dict)
                and ("id" in val[0] or "title" in val[0])):
            return val
    return []
from kanban_framework.domain.guard import CheckResult


class GuardChecks:
    """Collection of internal guard check methods.

    Instantiated by Guard, shares the same fs/config references.
    """

    def _get_mode_execute_guard(self, mode: str) -> dict:
        """Read execute phase guard config for a specific mode."""
        import json
        try:
            wf_file = self._fs.kanban_dir / "workflows" / f"{mode}.json"
            if wf_file.is_file():
                data = json.loads(wf_file.read_text(encoding="utf-8"))
                for p in data.get("phases", []):
                    if isinstance(p, dict) and p.get("id") == "execute":
                        return p.get("guard", {})
        except Exception:
            pass
        return {}

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

    def _is_knowledge_base_empty(self) -> bool:
        """Check if the knowledge base has zero active entries."""
        try:
            from kanban_framework.domain.knowledge import KnowledgeManager
            km = KnowledgeManager(self._fs, self._cfg)
            entries = km.list_entries(status="active", limit=1)
            return len(entries) == 0
        except Exception:
            return False

    def check_knowledge_references(self, task: Task) -> CheckResult:
        """Verify knowledge_used.json exists, and spec/plan files reference K-NNN entries."""
        td = self._fs.task_dir(task.id)
        failures = []
        warnings = []

        # 0. Empty knowledge base + no knowledge_used.json — skip check (#536-002)
        ku_path = td / "plan" / "knowledge_used.json"
        if not self._fs.file_exists(ku_path) and self._is_knowledge_base_empty():
            return CheckResult(passed=True, warnings=[
                "Knowledge base is empty — K-NNN reference check skipped. "
                "Add entries with 'kanban knowledge add' to enable this check."
            ])

        # 1. knowledge_used.json must exist and be non-empty
        ku_path = td / "plan" / "knowledge_used.json"
        if not self._fs.file_exists(ku_path):
            failures.append(
                "plan/knowledge_used.json missing — knowledge search step did not produce this file. "
                "Fix: ensure plan.knowledge_search step runs and writes results to "
                "$task_dir/plan/knowledge_used.json with format "
                '{\"matched\": [{\"id\": \"K001\", \"title\": \"...\", \"relevance\": \"high\"}]}')
        elif ku_path.stat().st_size == 0:
            failures.append(
                "plan/knowledge_used.json is empty (0 bytes) — knowledge search agent "
                "wrote an empty file. Fix: re-run the knowledge search step, or if the "
                "knowledge base is genuinely empty, write {\"no_match_reason\": \"...\"} "
                "to skip this check")
        else:
            try:
                data = json.loads(ku_path.read_text(encoding="utf-8"))
                matched = _extract_matched_entries(data)
                if not matched:
                    no_reason = ""
                    for rf in _NO_MATCH_REASON_FIELDS:
                        if data.get(rf):
                            no_reason = data[rf]
                            break
                    if no_reason:
                        warnings.append(f"knowledge_used.json has no matches, reason: {no_reason}")
                    else:
                        failures.append(
                            "plan/knowledge_used.json has no matched entries and no reason given. "
                            "The file exists but contains no recognized entry list (expected fields: "
                            "matched/selected_entries/entries/items/results). "
                            "Fix: either populate with {\"matched\": [...]} or add "
                            "{\"no_match_reason\": \"<why no matches>\"} to skip this check")
            except (ValueError, OSError):
                failures.append(
                    "plan/knowledge_used.json is malformed (invalid JSON). "
                    "Fix: ensure the file contains valid JSON, e.g. "
                    '{\"matched\": [{\"id\": \"K001\", \"title\": \"...\"}]}')

        # 2. spec.md or plan/*.md must contain K-NNN or scope-NNN references
        #    Skip this check when knowledge_used.json reports no matches with a reason
        #    (e.g., empty knowledge base on new projects)
        skip_ref_check = warnings and "no matches" in warnings[-1]
        if not skip_ref_check:
            # Match knowledge entry IDs: K001, K001-K003, alice001, test011, etc.
            # Scope IDs: 1-15 lowercase alphanumeric prefix + 3+ digits
            # K IDs: K + 3+ digits
            ref_pattern = re.compile(
                r'(?:知识库参考|knowledge refs?)\s*[：:]\s*\[?([^\]]+)\]?|'  # 知识库参考: [K001, alice002]
                r'\[([A-Za-z][A-Za-z0-9]{0,14}\d{3,})\]|'                  # [K001] or [alice001]
                r'\*\*([A-Za-z][A-Za-z0-9]{0,14}\d{3,})\*\*|'              # **K001**
                r'\b([A-Za-z][A-Za-z0-9]{0,14}\d{3,})\b'                   # bare K001 or alice001
            )
            files_to_check = [td / "spec.md"]
            plan_dir = td / "plan"
            if plan_dir.is_dir():
                files_to_check.extend(sorted(plan_dir.glob("*.md")))

            found_refs = set()
            for f in files_to_check:
                if not self._fs.file_exists(f):
                    continue
                text = f.read_text(encoding="utf-8", errors="replace")
                for m in ref_pattern.finditer(text):
                    for g in m.groups():
                        if not g:
                            continue
                        # Split comma/space separated refs from 知识库参考: header
                        for part in re.split(r'[,，\s]+', g.strip()):
                            part = part.strip().strip('[]')
                            if re.match(r'^[A-Za-z][A-Za-z0-9]{0,14}\d{3,}$', part):
                                found_refs.add(part)

            if found_refs:
                warnings.append(f"Knowledge refs in artifacts: {sorted(found_refs)}")
            else:
                failures.append(
                    "No knowledge references (K-NNN or scope-NNN) found in spec.md or plan/*.md — "
                    "the agent must document which knowledge entries were applied. "
                    "Fix: add a '知识库参考' section to spec.md or plan files with "
                    "references like [K001], [alice001], e.g. '知识库参考: K001 避免 XX 问题'")

        return CheckResult(passed=len(failures) == 0, failures=failures, warnings=warnings)

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
                    return CheckResult(passed=False, failures=[
                        f"{filename} exists but is empty (0 bytes). "
                        f"Fix: ensure the agent writes actual content to {filename}"])
                return CheckResult(passed=True)

        return CheckResult(passed=False, failures=[
            f"{filename} not found in task directory. "
            f"Searched: task root, iteration-N/, plan/, execute/, reviews/. "
            f"Fix: ensure the agent produces {filename} in the correct location"])

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
        Only runs when the mode's guard config explicitly includes 'tdd_evidence'.
        """
        from kanban_framework.infra.consts import Consts
        mode = getattr(task, 'mode', '') or Consts.DEFAULT_MODE
        guard_cfg = self._get_mode_execute_guard(mode)
        # If guard config exists with explicit checks list, use it
        if 'checks' in guard_cfg:
            if 'tdd_evidence' not in guard_cfg['checks']:
                return CheckResult(passed=True)
        else:
            # No guard config — default: exempt (no mode requires TDD by default)
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
                    "TDD not correctly executed (test didn't catch missing feature). "
                    "Fix: write the test FIRST, run it to see it FAIL, then implement the feature"
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
        from kanban_framework.infra.consts import Consts
        mode = getattr(task, 'mode', '') or Consts.DEFAULT_MODE
        guard_cfg = self._get_mode_execute_guard(mode)
        # If guard config exists with explicit checks list, use it
        if 'checks' in guard_cfg:
            if 'test_spec_coverage' not in guard_cfg['checks']:
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

    # --- external tool scope resolution ---

    _WORKTREE_GLOB = "**/*.py"

    def _resolve_files(self, task: Task, scope: str) -> list[str]:
        """Determine which files an external tool should check.

        Args:
            task: The task whose worktree to scan.
            scope: One of "worktree", "changed", or "glob:PATTERN".

        Returns:
            List of absolute file paths matching the scope criteria.
            Empty list when worktree_path is not set.
        """
        wt = Path(task.worktree_path) if task.worktree_path else None
        if wt is None or not wt.is_dir():
            # Fall back to project root when no worktree (direct task execution)
            wt = self._fs.root
            if not wt.is_dir():
                return []

        if scope == "worktree":
            return sorted(str(f) for f in wt.glob(self._WORKTREE_GLOB))

        if scope == "changed":
            return self._resolve_changed_files(wt)

        if scope.startswith("glob:"):
            pattern = scope[len("glob:"):]
            return sorted(str(f) for f in wt.glob(pattern))

        # Unknown scope — default to worktree glob
        return sorted(str(f) for f in wt.glob(self._WORKTREE_GLOB))

    def _resolve_changed_files(self, wt: Path) -> list[str]:
        """Return files changed (added/modified) via git diff, falling back to worktree glob."""
        import subprocess
        if not (wt / ".git").is_dir():
            return sorted(str(f) for f in wt.glob(self._WORKTREE_GLOB))
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=AM", "HEAD"],
                cwd=wt, capture_output=True, text=True, check=True,
            )
            staged = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=AM", "--cached", "HEAD"],
                cwd=wt, capture_output=True, text=True, check=True,
            )
            files = set(result.stdout.splitlines()) | set(staged.stdout.splitlines())
            files.discard("")
            return sorted(str(wt / f) for f in sorted(files) if (wt / f).is_file())
        except (subprocess.CalledProcessError, OSError):
            return sorted(str(f) for f in wt.glob(self._WORKTREE_GLOB))

    def check_external_tool(self, task: Task, tool_config: dict) -> CheckResult:
        """Execute an external CLI tool and return a CheckResult.

        Runs the configured command against files resolved by ``_resolve_files``.
        Supports fail/warn pattern matching, exit code checks, severity levels,
        and timeout control. Writes tool output to a log file in the task dir.

        Args:
            task: The task whose worktree to scan for files.
            tool_config: Dict with keys ``name``, ``command``, and optional
                ``scope``, ``timeout_seconds``, ``fail_pattern``, ``warn_pattern``,
                ``fail_on_exit_code``, ``severity``.
        """
        # 1. Resolve files
        scope = tool_config.get("scope", "changed")
        files = self._resolve_files(task, scope)
        if not files:
            return CheckResult(passed=True, warnings=["No files to check"])

        # 2. Build command — replace ${files} placeholder (safe quoting for shell)
        import shlex
        tool_name = tool_config.get("name", "unknown")
        command_tmpl = tool_config.get("command", "")
        command = command_tmpl.replace("${files}", shlex.join(files))
        timeout = tool_config.get("timeout_seconds", 120)
        worktree = task.worktree_path or "."

        # 3. Execute via subprocess
        try:
            proc = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                timeout=timeout, cwd=worktree,
            )
        except FileNotFoundError:
            return CheckResult(
                passed=True,
                warnings=[f"{tool_name} not installed, check skipped"],
            )
        except subprocess.TimeoutExpired:
            return CheckResult(
                passed=False,
                failures=[f"{tool_name} timed out after {timeout}s"],
            )

        # Shell returns exit code 127 for "command not found"
        if proc.returncode == 127:
            return CheckResult(
                passed=True,
                warnings=[f"{tool_name} not installed — check skipped. "
                          f"Install with: pip install {tool_name}"],
            )

        output = proc.stdout + proc.stderr

        # 4. Write log file
        task_dir = self._fs.task_dir(task.id)
        self._fs.ensure_dir(task_dir)
        log_path = task_dir / f"guard_external_{tool_name}.log"
        log_path.write_text(output, encoding="utf-8")

        # 5. Match fail_pattern -> failures
        failures: list[str] = []
        fail_pat = tool_config.get("fail_pattern")
        if fail_pat:
            for line in output.splitlines():
                if re.search(fail_pat, line):
                    failures.append(line.strip())

        # 6. Exit code check
        if tool_config.get("fail_on_exit_code", True) and proc.returncode != 0:
            if not failures:
                failures.append(
                    f"{tool_name} exited with code {proc.returncode}. "
                    f"Full output saved to guard_external_{tool_name}.log. "
                    f"Fix: resolve the errors above and re-run"
                )

        # 7. Match warn_pattern -> warnings
        warnings: list[str] = []
        warn_pat = tool_config.get("warn_pattern")
        if warn_pat:
            for line in output.splitlines():
                if re.search(warn_pat, line):
                    warnings.append(line.strip())

        # 8. Severity determines blocking
        severity = tool_config.get("severity", "error")
        if severity == "warning":
            return CheckResult(passed=True, warnings=warnings + failures)
        return CheckResult(passed=len(failures) == 0, failures=failures, warnings=warnings)
