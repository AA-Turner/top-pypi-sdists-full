# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Build and validate the metadata-only EU runner verdict."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

COMMANDS = frozenset({"spec", "check", "discover", "read"})
_COMMAND_ORDER = ("spec", "check", "discover", "read")
CHECK_NAMES = frozenset(
    {
        "Catalog schema",
        "Command execution",
        "Connector cache hit ratio",
        "Final state per stream",
        "Field values",
        "HTTP replay coverage",
        "Primary key integrity (control)",
        "Primary key integrity (target)",
        "Primary key presence",
        "Record counts",
        "Reproduction case",
        "Spec compatibility",
        "Stream coverage",
    }
)
_TOP_LEVEL_KEYS = {
    "schema_version",
    "output_mode",
    "commands",
    "success",
    "regression_detected",
    "both_failed",
    "incomplete",
    "not_exercised",
    "totals",
    "checks",
}


def _record_count(result: Any) -> int:
    if not isinstance(result, dict):
        return 0
    counts = result.get("record_counts_per_stream")
    if not isinstance(counts, dict):
        return 0
    return sum(value for value in counts.values() if type(value) is int and value >= 0)


def _command_from_report(path: Path, report: dict[str, Any]) -> dict[str, Any] | None:
    command = path.parent.name
    if command not in COMMANDS:
        command = report.get("command")
    if command not in COMMANDS:
        return None
    target = report.get("target")
    control = report.get("control")
    target = target if isinstance(target, dict) else {}
    control = control if isinstance(control, dict) else {}
    target_exit = target.get("exit_code")
    control_exit = control.get("exit_code")
    passed = report.get("success") is True
    return {
        "command": command,
        "control_exit_code": control_exit if type(control_exit) is int else None,
        "target_exit_code": target_exit if type(target_exit) is int else None,
        "passed": passed,
    }


def _checks(report: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    target = report.get("target")
    control = report.get("control")
    target = target if isinstance(target, dict) else {}
    control = control if isinstance(control, dict) else {}
    target_exit = target.get("exit_code")
    control_exit = control.get("exit_code")
    if type(target_exit) is int:
        checks.append(
            {
                "check_name": "Command execution",
                "passed": target_exit == 0
                and (
                    control_exit is None
                    or (type(control_exit) is int and control_exit == 0)
                ),
            }
        )

    comparison = report.get("comparison")
    if isinstance(comparison, dict):
        for key, name in (
            ("spec", "Spec compatibility"),
            ("catalog_schema", "Catalog schema"),
            ("final_state", "Final state per stream"),
        ):
            detail = comparison.get(key)
            if isinstance(detail, dict) and type(detail.get("passed")) is bool:
                checks.append({"check_name": name, "passed": detail["passed"]})

    record_comparison = report.get("record_comparison")
    record_checks = (
        record_comparison.get("checks") if isinstance(record_comparison, dict) else None
    )
    if isinstance(record_checks, dict):
        for key, name in (
            ("record_counts", "Record counts"),
            ("pk_presence", "Primary key presence"),
            ("pk_uniqueness_control", "Primary key integrity (control)"),
            ("pk_uniqueness_target", "Primary key integrity (target)"),
            ("field_values", "Field values"),
        ):
            detail = record_checks.get(key)
            if isinstance(detail, dict) and type(detail.get("passed")) is bool:
                checks.append({"check_name": name, "passed": detail["passed"]})

    source = report.get("checks", [])
    if isinstance(source, list):
        for item in source:
            if not isinstance(item, dict):
                continue
            name = item.get("check_name", item.get("name"))
            passed = item.get("passed")
            if name in CHECK_NAMES and type(passed) is bool:
                checks.append({"check_name": name, "passed": passed})
    return checks


def build_verdict(output_dir: Path) -> dict[str, Any]:
    """Project CLI reports or a runner summary onto the fixed safe schema."""
    reports: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(output_dir.rglob("regression_report.json")):
        report = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(report, dict):
            if report.get("output_mode") != "masked":
                raise ValueError("CLI report output_mode must be masked")
            reports.append((path, report))

    summary_path = output_dir / "summary.json"
    summary = (
        json.loads(summary_path.read_text(encoding="utf-8"))
        if summary_path.is_file()
        else {}
    )
    if not isinstance(summary, dict):
        summary = {}

    commands = []
    checks = []
    stream_count = control_record_count = target_record_count = 0
    for path, report in reports:
        command = _command_from_report(path, report)
        if command is not None:
            commands.append(command)
        target = report.get("target")
        control = report.get("control")
        target = target if isinstance(target, dict) else {}
        control = control if isinstance(control, dict) else {}
        target_counts = target.get("record_counts_per_stream")
        control_counts = control.get("record_counts_per_stream")
        target_counts = target_counts if isinstance(target_counts, dict) else {}
        control_counts = control_counts if isinstance(control_counts, dict) else {}
        stream_count = max(stream_count, len(set(target_counts) | set(control_counts)))
        target_record_count += _record_count(target)
        control_record_count += _record_count(control)
        checks.extend(_checks(report))

    if not commands and isinstance(summary.get("commands"), list):
        for item in summary["commands"]:
            if (
                isinstance(item, dict)
                and item.get("command") in COMMANDS
                and type(item.get("exit_code")) is int
                and type(item.get("passed")) is bool
            ):
                commands.append(
                    {
                        "command": item["command"],
                        "control_exit_code": None,
                        "target_exit_code": item["exit_code"],
                        "passed": item["passed"],
                    }
                )

    commands.sort(key=lambda item: _COMMAND_ORDER.index(item["command"]))
    if reports:
        # The CLI exits 0 on a failed verdict, so the summary alone can call a
        # regression a pass. A report can fail the run but never pass one the
        # summary failed: a command that crashed wrote no report.
        success = summary.get("success", True) is True and all(
            report.get("success") is True
            and report.get("regression_detected") is not True
            for _, report in reports
        )
    elif "success" in summary:
        success = summary.get("success") is True
    else:
        success = bool(commands) and all(item["passed"] for item in commands)
    incomplete = summary.get("incomplete") is True or any(
        report.get("incomplete") is True for _, report in reports
    )
    not_exercised = summary.get("not_exercised") is True or any(
        report.get("not_exercised") is True for _, report in reports
    )
    success = success and not (incomplete or not_exercised)
    verdict = {
        "schema_version": 2,
        "output_mode": "masked",
        "commands": commands,
        "success": success,
        "regression_detected": any(
            report.get("regression_detected") is True for _, report in reports
        ),
        "both_failed": summary.get("both_failed") is True
        or any(report.get("both_failed") is True for _, report in reports),
        "incomplete": incomplete,
        "not_exercised": not_exercised,
        "totals": {
            "stream_count": stream_count,
            "control_record_count": control_record_count,
            "target_record_count": target_record_count,
        },
        "checks": checks,
    }
    validate_verdict(verdict)
    return verdict


def validate_verdict(data: Any) -> None:
    """Reject free text, unknown keys, and non-metadata values."""
    if not isinstance(data, dict) or set(data) != _TOP_LEVEL_KEYS:
        raise ValueError("verdict has an invalid key set")
    if type(data["schema_version"]) is not int or data["schema_version"] != 2:
        raise ValueError("verdict schema_version must be 2")
    if data["output_mode"] != "masked":
        raise ValueError("verdict output_mode must be masked")
    for key in (
        "success",
        "regression_detected",
        "both_failed",
        "incomplete",
        "not_exercised",
    ):
        if type(data[key]) is not bool:
            raise ValueError(f"verdict {key} must be boolean")
    if data["success"] and (data["incomplete"] or data["not_exercised"]):
        raise ValueError(
            "verdict success cannot be true when incomplete or not_exercised"
        )

    if not isinstance(data["commands"], list):
        raise ValueError("verdict commands must be a list")
    for item in data["commands"]:
        if not isinstance(item, dict) or set(item) != {
            "command",
            "control_exit_code",
            "target_exit_code",
            "passed",
        }:
            raise ValueError("verdict command has an invalid key set")
        if item["command"] not in COMMANDS:
            raise ValueError("verdict command is not an allowed command")
        if type(item["passed"]) is not bool:
            raise ValueError("verdict command passed must be boolean")
        for key in ("control_exit_code", "target_exit_code"):
            if item[key] is not None and (type(item[key]) is not int or item[key] < 0):
                raise ValueError(f"verdict {key} must be a non-negative integer")

    totals = data["totals"]
    if not isinstance(totals, dict) or set(totals) != {
        "stream_count",
        "control_record_count",
        "target_record_count",
    }:
        raise ValueError("verdict totals have an invalid key set")
    if any(type(value) is not int or value < 0 for value in totals.values()):
        raise ValueError("verdict totals must be non-negative integers")

    if not isinstance(data["checks"], list):
        raise ValueError("verdict checks must be a list")
    for item in data["checks"]:
        if not isinstance(item, dict) or set(item) != {"check_name", "passed"}:
            raise ValueError("verdict check has an invalid key set")
        if item["check_name"] not in CHECK_NAMES:
            raise ValueError("verdict check name is not allowed")
        if type(item["passed"]) is not bool:
            raise ValueError("verdict check passed must be boolean")
