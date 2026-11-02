"""Hierarchy-aware orchestration for the SpecKit Phase 3 quality gates."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .cross_ref import cross_ref_command
from .pass_e2.validator import test_coverage_command
from .scaffold_common import FeatureResolutionError, get_repo_root, resolve_active_feature
from .validate_frs import validate_frs_command
from .verify_artifacts import verify_artifacts_command

_PASS_G_SEVERITIES = {
    "invalid": "HIGH",
    "ambiguous": "MEDIUM",
    "partial": "LOW",
    "skipped": "LOW",
    "matched": "LOW",
    "new_symbol": "LOW",
}
_NON_WARNING_PASS_G_STATUSES = frozenset({"matched", "new_symbol"})
_REPORT_SECTIONS = (
    "## Coverage Summary",
    "## E.2 Test Coverage",
    "## Artifact Path Verification",
    "## Pass G Findings",
)


def _invoke_json_command(
    command: Callable[[list[str]], None],
    argv: list[str],
    gate_name: str,
) -> tuple[dict[str, Any], int]:
    """Run an existing JSON-producing gate and preserve its 0/1/2 outcome."""
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            command(argv)
    except SystemExit as exc:
        if exc.code is None:
            exit_code = 0
        elif isinstance(exc.code, int):
            exit_code = exc.code
        else:
            raise RuntimeError(f"{gate_name} returned a non-integer exit code: {exc.code!r}")
    except Exception as exc:
        detail = stderr.getvalue().strip()
        suffix = f": {detail}" if detail else ""
        raise RuntimeError(f"{gate_name} could not run: {exc}{suffix}") from exc
    else:
        exit_code = 0

    if exit_code not in (0, 1):
        detail = stderr.getvalue().strip() or stdout.getvalue().strip()
        suffix = f": {detail}" if detail else ""
        raise RuntimeError(f"{gate_name} returned operational error {exit_code}{suffix}")

    try:
        payload = json.loads(stdout.getvalue())
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{gate_name} emitted malformed JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{gate_name} JSON output must be a JSON object")
    return payload, exit_code


def _pass_g_severity(finding: dict[str, Any]) -> str:
    """Map the existing Pass G status/candidate data to its report severity."""
    status = finding.get("status")
    candidates = finding.get("candidates")
    if not isinstance(status, str) or status not in _PASS_G_SEVERITIES:
        raise ValueError(f"unsupported Pass G status: {status!r}")
    if not isinstance(candidates, list) or any(not isinstance(candidate, dict) for candidate in candidates):
        raise ValueError("Pass G finding candidates must be a list of objects")
    if status == "invalid" and candidates:
        return "MEDIUM"
    return _PASS_G_SEVERITIES[status]


def _write_atomically(path: Path, content: str) -> None:
    """Write complete UTF-8 contents beside *path*, then atomically replace it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except OSError:
        if temporary_path is not None:
            with contextlib.suppress(OSError):
                temporary_path.unlink(missing_ok=True)
        raise


def _render_report(result: dict[str, Any]) -> str:
    """Render the analysis report exclusively from a canonical persisted result."""
    gates = result["gates"]
    fr_gate = gates["fr_validation"]
    fr_metrics = fr_gate.get("metrics", {})
    total_frs = fr_metrics.get("total", 0)
    covered_frs = fr_metrics.get("covered_count", 0)
    coverage_percent = fr_metrics.get("coverage_percent", 100)
    coverage_line = f"{covered_frs}/{total_frs} FRs covered ({coverage_percent}%)"
    if fr_gate["status"] == "skipped":
        coverage_line = f"Skipped: {fr_gate['skip_reason']}"

    lines = [
        "# Phase 3 Gate Analysis Report",
        "",
        f"- Hierarchy level: `{result['hierarchy_level']}`",
        f"- Spec directory: `{result['spec_dir']}`",
        f"- Overall status: **{result['status']}**",
        "",
        _REPORT_SECTIONS[0],
        "",
        f"- FR validation: {coverage_line}",
        "",
    ]
    for finding in fr_gate.get("findings", []):
        lines.append(
            f"- **{finding.get('severity', 'INFO')}** {finding.get('key', '')}: {finding.get('description', '')}"
        )
    lines.extend(["", _REPORT_SECTIONS[1], ""])

    coverage_gate = gates["test_coverage"]
    if coverage_gate["status"] == "skipped":
        lines.append(f"Skipped: {coverage_gate['skip_reason']}")
    else:
        summary_table = coverage_gate.get("metrics", {}).get("summary_table", "")
        if not isinstance(summary_table, str):
            raise RuntimeError("E.2 test coverage summary_table must be a string")
        lines.append(summary_table or "No E.2 findings.")
        for finding in coverage_gate.get("findings", []):
            lines.append(
                f"- **{finding.get('severity', 'INFO')}** {finding.get('key', '')}: {finding.get('description', '')}"
            )

    artifact_gate = gates["artifact_path_verification"]
    lines.extend(["", _REPORT_SECTIONS[2], ""])
    if artifact_gate["status"] == "skipped":
        lines.append(f"Skipped: {artifact_gate['skip_reason']}")
    else:
        checks = artifact_gate.get("metrics", {}).get("checks_run", [])
        lines.append(f"Checks run: {', '.join(checks) if checks else 'none'}")
        if not artifact_gate.get("findings"):
            lines.append("All required artifact paths verified.")
        for finding in artifact_gate.get("findings", []):
            lines.append(
                f"- **{finding.get('severity', 'HIGH')}** {finding.get('check', '')}: {finding.get('detail', '')}"
            )

    pass_g_gate = gates["pass_g"]
    lines.extend(["", _REPORT_SECTIONS[3], ""])
    if pass_g_gate["status"] == "skipped":
        lines.append(f"Skipped: {pass_g_gate['skip_reason']}")
    elif not pass_g_gate.get("findings"):
        lines.append("No code-reference findings.")
    else:
        for finding in pass_g_gate["findings"]:
            status = finding.get("status", "unknown")
            reference = finding.get("reference", {})
            text = reference.get("text", "")
            location = reference.get("plan_location", "")
            lines.append(
                f"- **{finding['severity']}** `{status}` `{text}` ({location}): {finding.get('explanation', '')}"
            )
    return "\n".join(lines).rstrip() + "\n"


def run_phase3_gates_command(argv: list[str] | None = None) -> None:
    """Evaluate the applicable Phase 3 gates and persist their canonical result."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-run-phase3-gates",
        description="Run the hierarchy-aware SpecKit Phase 3 gates and write a verified report.",
    )
    parser.add_argument("--spec-dir", type=Path, help="Feature/task spec directory; defaults to the active feature.")
    parser.add_argument("--hierarchy-level", required=True, choices=("epic", "feature", "task"))
    parser.add_argument(
        "--spec-context",
        type=Path,
        help="Task-level parent directory containing spec.md (required for task hierarchy).",
    )
    parser.add_argument("--json", action="store_true", help="Emit the canonical JSON result to stdout.")
    args = parser.parse_args(argv)

    try:
        if args.spec_context is not None and args.hierarchy_level != "task":
            raise RuntimeError("--spec-context is only valid for task hierarchy")
        if args.spec_dir is None:
            try:
                spec_dir = resolve_active_feature().feature_dir.resolve()
            except FeatureResolutionError as exc:
                raise RuntimeError(f"Cannot resolve active SpecKit feature directory: {exc}") from exc
        else:
            spec_dir = args.spec_dir.expanduser().resolve()
        if not spec_dir.is_dir():
            raise RuntimeError(f"Spec directory does not exist or is not a directory: {spec_dir}")

        hierarchy = args.hierarchy_level
        parent_spec: Path | None = None
        if hierarchy == "feature":
            required_inputs = ["spec.md", "tasks.md", "plan.md"]
        elif hierarchy == "task":
            required_inputs = ["tasks.md"]
            if args.spec_context is None:
                raise RuntimeError("Task hierarchy requires --spec-context pointing to a parent directory.")
            parent_dir = args.spec_context.expanduser().resolve()
            if not parent_dir.is_dir():
                raise RuntimeError(f"Task --spec-context must be a parent directory: {parent_dir}")
            parent_spec = parent_dir / "spec.md"
            required_inputs.append(str(parent_spec))
        else:
            required_inputs = ["plan.md"]
        for input_name in required_inputs:
            input_path = Path(input_name) if Path(input_name).is_absolute() else spec_dir / input_name
            if not input_path.is_file():
                raise RuntimeError(f"Required Phase 3 input is missing: {input_path}")
            try:
                input_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise RuntimeError(f"Cannot read required Phase 3 input {input_path}: {exc}") from exc

        repo_root = get_repo_root().resolve()
        gates: dict[str, dict[str, Any]] = {}

        if hierarchy == "epic":
            gates["fr_validation"] = {
                "status": "skipped",
                "skip_reason": "epic level",
                "findings": [],
                "metrics": {},
            }
            gates["test_coverage"] = {
                "status": "skipped",
                "skip_reason": "epic level",
                "findings": [],
                "metrics": {},
            }
        else:
            spec_path = parent_spec or spec_dir / "spec.md"
            fr_payload, fr_exit = _invoke_json_command(
                validate_frs_command,
                ["--spec-file", str(spec_path), "--tasks-file", str(spec_dir / "tasks.md"), "--json"],
                "FR validation",
            )
            covered = fr_payload.get("covered")
            uncovered = fr_payload.get("uncovered")
            total = fr_payload.get("total")
            if (
                not isinstance(covered, list)
                or not isinstance(uncovered, list)
                or not isinstance(total, int)
                or isinstance(total, bool)
                or any(not isinstance(item, str) for item in (*covered, *uncovered))
            ):
                raise RuntimeError("FR validation emitted an invalid result schema")
            covered_ids = set(covered)
            uncovered_ids = set(uncovered)
            if total < 0 or total != len(covered_ids | uncovered_ids):
                raise RuntimeError("FR validation total does not match unique covered and uncovered FRs")
            if (fr_exit == 1) != bool(uncovered):
                raise RuntimeError("FR validation exit code does not match its reported coverage")
            fr_findings = [
                {
                    "key": fr_id,
                    "severity": "HIGH",
                    "description": f"{fr_id} is not referenced by tasks.md.",
                }
                for fr_id in uncovered
            ]
            if fr_payload.get("warning"):
                if not isinstance(fr_payload["warning"], str):
                    raise RuntimeError("FR validation warning must be a string")
                fr_findings.append({"severity": "LOW", "description": fr_payload["warning"]})
            fr_coverage_percent = round((len(covered_ids) / total) * 100, 2) if total else 100
            gates["fr_validation"] = {
                "status": "failed"
                if uncovered
                else ("passed_with_warnings" if fr_payload.get("warning") else "passed"),
                "findings": fr_findings,
                "metrics": {
                    "spec_file": str(spec_path),
                    "total": total,
                    "covered_count": len(covered_ids),
                    "uncovered_count": len(uncovered_ids),
                    "coverage_percent": fr_coverage_percent,
                },
            }

            coverage_payload, coverage_exit = _invoke_json_command(
                test_coverage_command,
                ["--spec-file", str(spec_path), "--tasks-file", str(spec_dir / "tasks.md"), "--json"],
                "E.2 test coverage",
            )
            coverage_findings = coverage_payload.get("findings")
            coverage_summary = coverage_payload.get("summary")
            coverage_map = coverage_payload.get("coverage", {})
            summary_table = coverage_payload.get("summary_table", "")
            if (
                not isinstance(coverage_findings, list)
                or not isinstance(coverage_summary, dict)
                or not isinstance(coverage_map, dict)
                or not isinstance(summary_table, str)
            ):
                raise RuntimeError("E.2 test coverage emitted an invalid result schema")
            if any(not isinstance(finding, dict) for finding in coverage_findings):
                raise RuntimeError("E.2 test coverage findings must be JSON objects")
            if (coverage_exit == 1) != bool(coverage_findings):
                raise RuntimeError("E.2 test coverage exit code does not match its findings")
            gates["test_coverage"] = {
                "status": "failed" if coverage_findings else "passed",
                "findings": coverage_findings,
                "metrics": {
                    "summary": coverage_summary,
                    "coverage": coverage_map,
                    "summary_table": summary_table,
                },
            }

        verification_args = [
            "--spec-dir",
            str(spec_dir),
            "--repo-root",
            str(repo_root),
            "--phase",
            "4" if hierarchy == "task" else "3",
            "--json",
        ]
        if parent_spec is not None:
            verification_args.extend(("--spec-context", str(parent_spec)))
        verification_payload, verification_exit = _invoke_json_command(
            verify_artifacts_command,
            verification_args,
            "artifact-path verification",
        )
        violations = verification_payload.get("violations")
        checks_run = verification_payload.get("checks_run")
        passed = verification_payload.get("passed")
        if (
            not isinstance(violations, list)
            or not isinstance(checks_run, list)
            or any(not isinstance(check, str) for check in checks_run)
            or not isinstance(passed, bool)
        ):
            raise RuntimeError("Artifact-path verification emitted an invalid result schema")
        if any(not isinstance(violation, dict) for violation in violations):
            raise RuntimeError("Artifact-path verification violations must be JSON objects")
        if passed != (not violations):
            raise RuntimeError("Artifact-path verification passed value does not match its violations")
        if (verification_exit == 1) != (not passed):
            raise RuntimeError("Artifact-path verification exit code does not match its passed value")
        gates["artifact_path_verification"] = {
            "status": "failed" if not passed else "passed",
            "findings": violations,
            "metrics": {"checks_run": checks_run},
        }

        if hierarchy == "task":
            gates["pass_g"] = {
                "status": "skipped",
                "skip_reason": "task level has no local plan.md",
                "findings": [],
                "metrics": {},
            }
        else:
            pass_g_payload, pass_g_exit = _invoke_json_command(
                cross_ref_command,
                [
                    "--plan-file",
                    str(spec_dir / "plan.md"),
                    "--repo-root",
                    str(repo_root),
                    "--json",
                ],
                "Pass G cross-reference",
            )
            pass_g_findings = pass_g_payload.get("findings")
            if not isinstance(pass_g_findings, list) or any(not isinstance(item, dict) for item in pass_g_findings):
                raise RuntimeError("Pass G cross-reference emitted an invalid result schema")
            normalized_findings: list[dict[str, Any]] = []
            for finding in pass_g_findings:
                if not isinstance(finding.get("reference"), dict):
                    raise RuntimeError("Pass G finding reference must be a JSON object")
                if "explanation" in finding and not isinstance(finding["explanation"], str):
                    raise RuntimeError("Pass G finding explanation must be a string")
                try:
                    severity = _pass_g_severity(finding)
                except ValueError as exc:
                    raise RuntimeError(f"Pass G cross-reference emitted an invalid finding: {exc}") from exc
                normalized_findings.append({**finding, "severity": severity})
            high_findings = [
                finding
                for finding in normalized_findings
                if finding["status"] == "invalid" and finding["severity"] == "HIGH"
            ]
            if (pass_g_exit == 1) != bool(high_findings):
                raise RuntimeError("Pass G exit code does not match its HIGH-severity findings")
            critical_findings = [finding for finding in normalized_findings if finding["severity"] == "CRITICAL"]
            has_warnings = any(finding["status"] not in _NON_WARNING_PASS_G_STATUSES for finding in normalized_findings)
            gates["pass_g"] = {
                "status": "failed" if critical_findings else ("passed_with_warnings" if has_warnings else "passed"),
                "findings": normalized_findings,
                "metrics": {
                    "summary": pass_g_payload.get("summary", {}),
                    "total_references": pass_g_payload.get("total_references", len(pass_g_findings)),
                    "elapsed_seconds": pass_g_payload.get("elapsed_seconds", 0),
                },
            }

        overall_status = (
            "failed"
            if any(gate["status"] == "failed" for gate in gates.values())
            else (
                "passed_with_warnings"
                if any(gate["status"] == "passed_with_warnings" for gate in gates.values())
                else "passed"
            )
        )
        result = {
            "schema_version": 1,
            "hierarchy_level": hierarchy,
            "spec_dir": str(spec_dir),
            "status": overall_status,
            "gates": gates,
        }
        serialized = json.dumps(result, indent=2) + "\n"
        result_path = spec_dir / "generated" / "phase3-gates.json"
        report_path = spec_dir / "generated" / "analysis-report.md"
        _write_atomically(result_path, serialized)
        persisted_result = json.loads(result_path.read_text(encoding="utf-8"))
        if not isinstance(persisted_result, dict) or persisted_result != result:
            raise RuntimeError("Persisted Phase 3 gate result does not match the staged result")
        report = _render_report(persisted_result)
        if any(section not in report for section in _REPORT_SECTIONS):
            raise RuntimeError("Generated analysis report is missing a required section")
        _write_atomically(report_path, report)
        persisted_report = report_path.read_text(encoding="utf-8")
        if persisted_report != _render_report(persisted_result):
            raise RuntimeError("Generated analysis report is inconsistent with phase3-gates.json")

        final_verification_args = [
            "--spec-dir",
            str(spec_dir),
            "--repo-root",
            str(repo_root),
            "--json",
        ]
        if hierarchy in {"epic", "task"}:
            final_phase = "3" if hierarchy == "epic" else "4"
            final_verification_args.extend(("--phase", final_phase))
        if parent_spec is not None:
            final_verification_args.extend(("--spec-context", str(parent_spec)))
        final_payload, final_exit = _invoke_json_command(
            verify_artifacts_command,
            final_verification_args,
            "complete artifact verification",
        )
        final_violations = final_payload.get("violations")
        final_checks_run = final_payload.get("checks_run")
        final_passed = final_payload.get("passed")
        if (
            not isinstance(final_violations, list)
            or not isinstance(final_checks_run, list)
            or any(not isinstance(check, str) for check in final_checks_run)
            or not isinstance(final_passed, bool)
        ):
            raise RuntimeError("Complete artifact verification emitted an invalid result schema")
        if any(not isinstance(violation, dict) for violation in final_violations):
            raise RuntimeError("Complete artifact verification violations must be JSON objects")
        if final_passed != (not final_violations):
            raise RuntimeError("Complete artifact verification passed value does not match its violations")
        if (final_exit == 1) != (not final_passed):
            raise RuntimeError("Complete artifact verification exit code does not match its passed value")
        gates["artifact_path_verification"] = {
            "status": "failed" if not final_passed else "passed",
            "findings": final_violations,
            "metrics": {"checks_run": final_checks_run},
        }
        overall_status = (
            "failed"
            if any(gate["status"] == "failed" for gate in gates.values())
            else (
                "passed_with_warnings"
                if any(gate["status"] == "passed_with_warnings" for gate in gates.values())
                else "passed"
            )
        )
        result["status"] = overall_status
        serialized = json.dumps(result, indent=2) + "\n"
        _write_atomically(result_path, serialized)
        persisted_result = json.loads(result_path.read_text(encoding="utf-8"))
        if not isinstance(persisted_result, dict) or persisted_result != result:
            raise RuntimeError("Persisted Phase 3 gate result does not match the final result")
        report = _render_report(persisted_result)
        if any(section not in report for section in _REPORT_SECTIONS):
            raise RuntimeError("Generated analysis report is missing a required section")
        _write_atomically(report_path, report)
        persisted_report = report_path.read_text(encoding="utf-8")
        if persisted_report != _render_report(persisted_result):
            raise RuntimeError("Generated analysis report is inconsistent with phase3-gates.json")
        sys.stdout.write(serialized if args.json else persisted_report)
        raise SystemExit(1 if overall_status == "failed" else 0)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuntimeError, KeyError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
