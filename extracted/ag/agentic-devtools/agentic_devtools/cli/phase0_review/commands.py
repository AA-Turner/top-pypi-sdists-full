"""Read-only orchestration for the Phase 0 factual-review gate."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.config import (
    FACTUAL_REVIEW_INPUT_STATE_KEY,
    INTEGRITY_STATE_KEY,
    PHASE0_PR_CHECKLIST,
    PROCESSING_TIMEOUT_SECONDS,
)
from agentic_devtools.cli.phase0_review.contract import (
    ContractResult,
    load_contract,
    validate_integrity,
    validate_paths,
    validate_schema,
)
from agentic_devtools.cli.phase0_review.helpers import (
    frontmatter_validate,
    resolve_safe_path,
    structural_compare,
)
from agentic_devtools.cli.phase0_review.report import (
    Finding,
    malformed_input,
    missing_input,
    render_report,
    structural,
)
from agentic_devtools.state import get_repo_root, get_value


def inject_phase0_checklist(pr_body: str, phase: int | str) -> str:
    """Append the factual-review checklist only to Phase 0 PR bodies."""
    normalized = str(phase).strip().lower().replace("phase", "").strip()
    if normalized != "0" or PHASE0_PR_CHECKLIST in pr_body:
        return pr_body
    separator = "\n\n" if pr_body else ""
    return f"{pr_body}{separator}{PHASE0_PR_CHECKLIST}\n"


def _state_artifact_path(
    value: Any,
    repo_root: Path,
    label: str,
) -> tuple[Path | None, list[Finding]]:
    if isinstance(value, Path):
        value = str(value)
    if not isinstance(value, str) or not value.strip():
        return None, [missing_input(label, "state key is absent or empty")]
    path, error = resolve_safe_path(value, repo_root, require_relative=False)
    if error:
        return None, [malformed_input(f"{label} is a safe repository path", error)]
    if path is None:
        return None, [malformed_input(f"{label} is a safe repository path", "path was not resolved")]
    try:
        if not path.exists():
            return None, [missing_input(label, "file does not exist")]
        if not path.is_file():
            return None, [malformed_input(f"{label} resolves to a regular file", f"found {path}")]
    except OSError as exc:
        return None, [missing_input(label, f"unreadable: {exc}")]
    return path, []


def _read_artifacts(result: ContractResult) -> None:
    for label, path in result.paths.items():
        try:
            raw = path.read_bytes()
        except OSError as exc:
            result.findings.append(missing_input(label, f"unreadable: {exc}"))
            continue
        result.artifact_bytes[label] = raw
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            result.findings.append(malformed_input(f"{label} is readable UTF-8", str(exc)))


def run_review(
    *,
    repo_root: Path | None = None,
    input_path: str | Path | None = None,
    integrity_path: str | Path | None = None,
    clock: Callable[[], float] = time.monotonic,
    deadline: float | None = None,
) -> str:
    """Run the bounded, deterministic, read-only Phase 0 review."""
    root = repo_root or get_repo_root()
    findings: list[Finding] = []
    if root is None:
        return render_report([missing_input("repository root", "not inside a git repository")])
    root = root.resolve()
    expires_at = deadline if deadline is not None else clock() + PROCESSING_TIMEOUT_SECONDS

    def expired() -> bool:
        return clock() >= expires_at

    raw_input_path: Any = input_path
    if raw_input_path is None:
        raw_input_path = get_value(FACTUAL_REVIEW_INPUT_STATE_KEY)
    payload_path, path_findings = _state_artifact_path(raw_input_path, root, "factual-review payload")
    findings.extend(path_findings)
    if expired():
        return render_report(findings, timed_out=True)
    if payload_path is None:
        return render_report(findings)

    contract = load_contract(payload_path)
    findings.extend(contract.findings)
    if expired():
        return render_report(findings, timed_out=True)
    if contract.data is not None:
        schema_findings = validate_schema(contract.data)
        findings.extend(schema_findings)
        paths, artifact_findings = validate_paths(contract.data, root)
        contract.paths.update(paths)
        findings.extend(artifact_findings)
        contract_finding_count = len(contract.findings)
        _read_artifacts(contract)
        findings.extend(contract.findings[contract_finding_count:])

    raw_integrity_path: Any = integrity_path
    if raw_integrity_path is None:
        raw_integrity_path = get_value(INTEGRITY_STATE_KEY)
    resolved_integrity, integrity_path_findings = _state_artifact_path(
        raw_integrity_path,
        root,
        "phase0-integrity.json",
    )
    findings.extend(integrity_path_findings)
    if expired():
        return render_report(findings, timed_out=True)
    if resolved_integrity is not None and contract.payload_bytes is not None:
        findings.extend(
            validate_integrity(
                resolved_integrity,
                contract.payload_bytes,
                contract.artifact_bytes,
            )
        )

    required_artifacts = {
        "issue_md.path",
        "template.selected_path",
        "template.structure_snapshot_path",
    }
    if contract.data is not None and required_artifacts <= contract.artifact_bytes.keys():
        source = contract.data.get("source")
        if isinstance(source, dict):
            try:
                issue_md = contract.artifact_bytes["issue_md.path"].decode("utf-8")
            except UnicodeDecodeError:
                if expired():
                    return render_report(findings, timed_out=True)
                return render_report(findings)
            try:
                snapshot = contract.artifact_bytes["template.structure_snapshot_path"].decode("utf-8")
            except UnicodeDecodeError:
                if expired():
                    return render_report(findings, timed_out=True)
                return render_report(findings)
            frontmatter_findings, frontmatter = frontmatter_validate(snapshot, issue_md)
            findings.extend(structural(expected, observed) for expected, observed in frontmatter_findings)
            structure = structural_compare(snapshot, issue_md, source)
            findings.extend(structural(expected, observed) for expected, observed in structure.findings)
            findings.extend(malformed_input(expected, observed) for expected, observed in structure.malformed)
            if expired():
                return render_report(findings, timed_out=True)
            findings.extend(compare_content(source, frontmatter, structure))
    if expired():
        return render_report(findings, timed_out=True)
    return render_report(findings)


def phase0_review_command() -> None:
    """CLI/background-task command that prints the normative report."""
    report = run_review()
    print(report)
    lines = report.splitlines()
    verdict_index = next((index for index, line in enumerate(lines) if line == "## Verdict"), None)
    if verdict_index is None:
        verdict_index = next((index for index, line in enumerate(lines) if "## Verdict" in line), None)
    if verdict_index is None or verdict_index + 1 >= len(lines):
        print("ERROR: report is missing a complete verdict section")
        raise SystemExit(1)
    if lines[verdict_index + 1] == "CHANGES REQUESTED":
        raise SystemExit(1)
