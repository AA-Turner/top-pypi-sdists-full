"""Baseline-aware Ruff complexity checks."""

from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

from agentic_devtools.cli.checks.quality_baseline import read_quality_baseline

COMPLEXITY_RULES = ("C901", "PLR0912", "PLR0915")
_DEFAULT_THRESHOLDS = {"C901": 10, "PLR0912": 12, "PLR0915": 50}
_METRIC_PATTERNS = {
    "C901": re.compile(r"^.+ is too complex \((\d+) > (\d+)\)$"),
    "PLR0912": re.compile(r"^Too many branches \((\d+) > (\d+)\)$"),
    "PLR0915": re.compile(r"^Too many statements \((\d+) > (\d+)\)$"),
}


def _parse_complexity_metric(rule: str, message: str) -> int:
    pattern = _METRIC_PATTERNS.get(rule)
    if pattern is None:
        raise ValueError(f"unsupported complexity rule {rule!r}")
    match = pattern.fullmatch(message)
    if match is None:
        raise ValueError(f"unrecognized {rule} complexity metric message {message!r}")

    measured, threshold = (int(value) for value in match.groups())
    default_threshold = _DEFAULT_THRESHOLDS[rule]
    if threshold != default_threshold or measured <= threshold:
        raise ValueError(
            f"expected a measured count above the default {rule} threshold "
            f"of {default_threshold}, got {measured} > {threshold}"
        )
    return measured


class ComplexityChecker:
    """Compare current Ruff complexity findings with the shared baseline."""

    def __init__(self, repo_root: str | Path) -> None:
        self.root = Path(repo_root).resolve()
        self._function_cache: dict[str, list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, str, int, int]]] = {}

    def check(self) -> tuple[bool, str]:
        """Return whether every complexity finding is present in the baseline."""
        _, baseline, error = read_quality_baseline(self.root)
        if error is not None:
            return False, error

        findings, error = self._run_ruff()
        if error is not None:
            return False, error

        current, error = self._collect_findings(findings)
        if error is not None:
            return False, error

        errors: list[str] = []
        for identifier, (message, metric) in current.items():
            if identifier not in baseline:
                errors.append(f"FAIL: New complexity violation {identifier}: {message}")
            else:
                rule = identifier.split("::", 2)[1]
                try:
                    baseline_metric = _parse_complexity_metric(rule, baseline[identifier])
                except ValueError as exc:
                    return False, f"ERROR: Could not parse baseline complexity metric for {identifier}: {exc}"
                if metric > baseline_metric:
                    errors.append(
                        f"FAIL: Tracked complexity violation grew for {identifier}: "
                        f"baseline metric {baseline_metric} != current metric {metric}."
                    )
        warnings = [
            f"WARNING: Baseline complexity entry {identifier} is no longer present; retain the grow-only entry."
            for identifier in sorted(baseline)
            if identifier not in current
        ]
        messages = [*errors, *warnings]
        if not messages:
            return True, "OK — no unbaselined complexity violations."
        return not errors, "\n".join(messages)

    def _run_ruff(self) -> tuple[list[object], str | None]:
        try:
            result = subprocess.run(
                [
                    "ruff",
                    "check",
                    "--select",
                    ",".join(COMPLEXITY_RULES),
                    "--output-format",
                    "json",
                    ".",
                ],
                cwd=self.root,
                capture_output=True,
                text=True,
                shell=False,
            )
        except OSError as exc:
            return [], f"ERROR: Could not run Ruff complexity check: {exc}"
        if result.returncode not in (0, 1):
            detail = (result.stderr or result.stdout).strip()
            return [], f"ERROR: Ruff complexity check exited with code {result.returncode}: {detail}"
        if not result.stdout.strip():
            if result.returncode == 0:
                return [], None
            return [], "ERROR: Ruff complexity check failed without JSON diagnostics."
        try:
            findings = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return [], f"ERROR: Invalid Ruff complexity output: {exc}"
        if not isinstance(findings, list):
            return [], "ERROR: Invalid Ruff complexity output: expected a JSON array."
        if result.returncode == 1 and not findings:
            return [], "ERROR: Ruff complexity check failed without diagnostics."
        return findings, None

    def _collect_findings(self, findings: list[object]) -> tuple[dict[str, tuple[str, int]], str | None]:
        current: dict[str, tuple[str, int]] = {}
        try:
            for finding in findings:
                identifier, message = self._finding_identifier(finding)
                if identifier in current:
                    return {}, f"ERROR: Duplicate Ruff complexity finding: {identifier}."
                rule = identifier.split("::", 2)[1]
                current[identifier] = (message, _parse_complexity_metric(rule, message))
        except (OSError, UnicodeError, SyntaxError, ValueError, TypeError) as exc:
            return {}, f"ERROR: Could not identify Ruff complexity finding: {exc}"
        return current, None

    def _finding_identifier(self, finding: object) -> tuple[str, str]:
        if not isinstance(finding, dict):
            raise ValueError("finding must be an object")
        code = finding.get("code")
        filename = finding.get("filename")
        location = finding.get("location")
        message = finding.get("message")
        if code not in COMPLEXITY_RULES or not isinstance(filename, str) or not isinstance(message, str):
            raise ValueError("finding has an invalid code, filename, or message")
        if not isinstance(location, dict):
            raise ValueError("finding location must be an object")
        row = location.get("row")
        if isinstance(row, bool) or not isinstance(row, int) or row < 1:
            raise ValueError("finding row must be a positive integer")

        path = Path(filename)
        if not path.is_absolute():
            path = self.root / path
        try:
            relative_path = path.resolve().relative_to(self.root).as_posix()
        except ValueError as exc:
            raise ValueError(f"finding path is outside the repository: {filename}") from exc
        qualified_name = self._function_name(relative_path, row)
        identifier = f"{relative_path}::{code}::{qualified_name}"
        return identifier, message

    def _function_name(self, relative_path: str, row: int) -> str:
        if relative_path not in self._function_cache:
            source_path = self.root / Path(relative_path)
            source = source_path.read_text(encoding="utf-8-sig")
            tree = ast.parse(source, filename=relative_path)
            definitions: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, str, int, int]] = []
            name_counts: dict[str, int] = {}

            def visit(node: ast.AST, scopes: tuple[str, ...]) -> None:
                next_scopes = scopes
                if isinstance(node, ast.ClassDef):
                    next_scopes = (*scopes, node.name)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.end_lineno is None:
                        raise ValueError(f"function has no end line: {relative_path}:{node.lineno}")
                    qualified_name = ".".join((*scopes, node.name))
                    occurrence = name_counts.get(qualified_name, 0) + 1
                    name_counts[qualified_name] = occurrence
                    definitions.append((node, qualified_name, node.end_lineno, occurrence))
                    next_scopes = (*scopes, node.name)
                for child in ast.iter_child_nodes(node):
                    visit(child, next_scopes)

            visit(tree, ())
            self._function_cache[relative_path] = definitions

        candidates = [
            definition
            for definition in self._function_cache[relative_path]
            if definition[0].lineno <= row <= definition[2]
        ]
        if not candidates:
            raise ValueError(f"no function encloses Ruff finding at {relative_path}:{row}")
        _, matched_name, _, occurrence = min(candidates, key=lambda item: item[2] - item[0].lineno)
        if occurrence > 1:
            return f"{matched_name}#{occurrence}"
        return matched_name
