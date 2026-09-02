import json
import os
from collections import Counter
from enum import Enum
from html import escape
from pathlib import Path
from typing import TypedDict

import typer

from runlayer_cli import regex_safe
from runlayer_cli.models_api import SkillScanFileScore, SkillScanResponse
from runlayer_cli.skills.models import DiscoveredSkill

_RISK_LEVEL_ORDER = {
    "Minimal": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
}
_RISK_LEVEL_DISPLAY_ORDER = ("High", "Medium", "Low", "Minimal")
_REASON_SEVERITY_PATTERN = regex_safe.compile(
    r"^\[(WARN|BLOCK)]\s*", regex_safe.IGNORECASE
)
_REMEDIATION_HINTS = {
    "Block": "Remove or rewrite the flagged behavior, then rescan before allowing this skill.",
    "Warn": "Review the flagged behavior, document why it is required, then rescan.",
    "Finding": "Review this finding in Audit Logs.",
}
_MAX_SKILLS = 10
_MAX_FILES_PER_SKILL = 5
_MAX_REASONS_PER_FILE = 3
_MAX_MARKDOWN_TEXT_LENGTH = 500
_NO_FILE_FINDINGS = (
    "Model-level detection; findings are not attributed to individual files."
)
_MODEL_LEVEL_HINT = "Open the Audit Logs entry for this scan ID."
_NO_REASON = "No reason returned; review this file in Audit Logs."


class FailOn(str, Enum):
    WARN = "warn"
    BLOCK = "block"


_EXIT_CODES = {
    FailOn.WARN: 2,
    FailOn.BLOCK: 3,
}

ScannedSkill = tuple[DiscoveredSkill, SkillScanResponse]


class _ReasonRow(TypedDict):
    reason_class: str
    text: str
    hint: str


class _FileRow(TypedDict):
    name: str
    risk_level: str
    reasons: list[_ReasonRow]
    reasons_omitted: int


class _SkillRow(TypedDict):
    name: str
    risk_level: str
    classification: str
    skill_score: float
    files: list[_FileRow]
    files_omitted: int


class ScanSummary(TypedDict):
    scan_id: str
    skill_count: int
    file_count: int
    skill_counts: dict[str, int]
    file_counts: dict[str, int]
    heading: str
    skills: list[_SkillRow]
    skills_omitted: int
    exit_explanation: str | None


def render_scan_results(scanned_skills: list[ScannedSkill]) -> str:
    if len(scanned_skills) == 1:
        return scanned_skills[0][1].model_dump_json(indent=2)

    payload = {
        "skills": [
            {
                "path": skill.path,
                "name": skill.name,
                **result.model_dump(mode="json"),
            }
            for skill, result in scanned_skills
        ]
    }
    return json.dumps(payload, indent=2)


def should_fail(risk_level: str, fail_on: FailOn | None) -> bool:
    if fail_on is None:
        return False
    level = _RISK_LEVEL_ORDER.get(risk_level, max(_RISK_LEVEL_ORDER.values()) + 1)
    threshold = 2 if fail_on == FailOn.WARN else 3
    return level >= threshold


def exit_code(fail_on: FailOn) -> int:
    return _EXIT_CODES[fail_on]


def _single_line(value: str) -> str:
    sanitized = "".join(
        character if character.isprintable() else " " for character in value
    )
    return sanitized[:1000]


def _markdown_text(value: str) -> str:
    return (
        escape(_single_line(value)[:_MAX_MARKDOWN_TEXT_LENGTH], quote=False)
        .replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("|", "\\|")
        .replace("`", "&#96;")
    )


def _markdown_code_span(value: str) -> str:
    text = _single_line(value)[:_MAX_MARKDOWN_TEXT_LENGTH].replace("`", "'")
    return f"`{text}`"


def _risk_counts(risk_levels: list[str]) -> dict[str, int]:
    counts = {level: 0 for level in _RISK_LEVEL_DISPLAY_ORDER}
    counts["Unknown"] = 0
    for risk_level in risk_levels:
        key = risk_level if risk_level in _RISK_LEVEL_ORDER else "Unknown"
        counts[key] += 1
    return counts


def _format_risk_counts(counts: dict[str, int]) -> str:
    levels = [
        *_RISK_LEVEL_DISPLAY_ORDER,
        *(["Unknown"] if counts["Unknown"] else []),
    ]
    return ", ".join(f"{level} {counts[level]}" for level in levels)


def _reason_summary(reason: str) -> tuple[str, str, str]:
    match = _REASON_SEVERITY_PATTERN.match(reason)
    reason_class = match.group(1).title() if match else "Finding"
    text = reason[match.end() :] if match else reason
    return (
        reason_class,
        _single_line(text).strip() or "No reason details returned",
        _REMEDIATION_HINTS[reason_class],
    )


def _summary_skills(
    scanned_skills: list[ScannedSkill],
    fail_on: FailOn | None,
) -> tuple[str, list[ScannedSkill]]:
    effective_fail_on = fail_on or FailOn.WARN
    heading = "Failing skills" if fail_on else "Elevated skills"
    skills = [
        (skill, result)
        for skill, result in scanned_skills
        if should_fail(result.skill_risk_level, effective_fail_on)
    ]
    return heading, skills


def _summary_files(
    result: SkillScanResponse, fail_on: FailOn | None
) -> list[SkillScanFileScore]:
    effective_fail_on = fail_on or FailOn.WARN
    files = [
        file for file in result.files if should_fail(file.risk_level, effective_fail_on)
    ]
    if not files:
        files = [file for file in result.files if file.reasons]
    return files


def _risk_label(risk_level: str) -> str:
    return _single_line(risk_level).strip() or "Unknown"


def _format_failing_risk_counts(failing_skills: list[ScannedSkill]) -> str:
    counts = Counter(
        _risk_label(result.skill_risk_level) for _, result in failing_skills
    )
    known_levels = [
        level for level in _RISK_LEVEL_DISPLAY_ORDER if counts.get(level, 0)
    ]
    other_levels = sorted(
        (level for level in counts if level not in _RISK_LEVEL_ORDER),
        key=str.casefold,
    )
    return ", ".join(
        f"{level} {counts[level]}" for level in [*known_levels, *other_levels]
    )


def _exit_explanation(
    fail_on: FailOn | None, failing_skills: list[ScannedSkill]
) -> str | None:
    explanation = None
    if fail_on is not None and failing_skills:
        explanation = (
            f"exiting {exit_code(fail_on)}: {len(failing_skills)} skill(s) failed "
            f"--fail-on={fail_on.value} "
            f"(risk levels: {_format_failing_risk_counts(failing_skills)})"
        )
    return explanation


def _reason_rows(file: SkillScanFileScore) -> tuple[list[_ReasonRow], int]:
    shown_reasons = file.reasons[:_MAX_REASONS_PER_FILE]
    rows = [
        _ReasonRow(reason_class=reason_class, text=text, hint=hint)
        for reason_class, text, hint in (
            _reason_summary(reason) for reason in shown_reasons
        )
    ]
    return rows, len(file.reasons) - len(shown_reasons)


def _file_rows(
    result: SkillScanResponse, fail_on: FailOn | None
) -> tuple[list[_FileRow], int]:
    summary_files = _summary_files(result, fail_on)
    shown_files = summary_files[:_MAX_FILES_PER_SKILL]
    rows: list[_FileRow] = []
    for file in shown_files:
        reasons, reasons_omitted = _reason_rows(file)
        rows.append(
            _FileRow(
                name=file.name,
                risk_level=file.risk_level,
                reasons=reasons,
                reasons_omitted=reasons_omitted,
            )
        )
    return rows, len(summary_files) - len(shown_files)


def build_scan_summary(
    scanned_skills: list[ScannedSkill],
    scan_id: str,
    fail_on: FailOn | None,
) -> ScanSummary:
    heading, summary_skills = _summary_skills(scanned_skills, fail_on)
    shown_skills = summary_skills[:_MAX_SKILLS]
    skills: list[_SkillRow] = []
    for skill, result in shown_skills:
        files, files_omitted = _file_rows(result, fail_on)
        skills.append(
            _SkillRow(
                name=skill.name,
                risk_level=result.skill_risk_level,
                classification=result.classification,
                skill_score=result.skill_score,
                files=files,
                files_omitted=files_omitted,
            )
        )
    return ScanSummary(
        scan_id=scan_id,
        skill_count=len(scanned_skills),
        # Count files from the scan response, not discovery: the backend drops
        # empty/whitespace-only files before scoring, and this total must match
        # the per-file risk counts below and the audit log's file_count.
        file_count=sum(len(result.files) for _, result in scanned_skills),
        skill_counts=_risk_counts(
            [result.skill_risk_level for _, result in scanned_skills]
        ),
        file_counts=_risk_counts(
            [file.risk_level for _, result in scanned_skills for file in result.files]
        ),
        heading=heading,
        skills=skills,
        skills_omitted=len(summary_skills) - len(shown_skills),
        exit_explanation=_exit_explanation(fail_on, summary_skills),
    )


def _skill_metadata(skill: _SkillRow, *, markdown: bool) -> str:
    values = [
        skill["name"],
        skill["risk_level"],
        skill["classification"],
        f"score {skill['skill_score']:.2f}",
    ]
    if markdown:
        values = [_markdown_text(value) for value in values]
    else:
        values = [_single_line(value) for value in values]
    return f"{values[0]} ({'; '.join(values[1:])})"


def _omission_text(count: int, noun: str) -> str:
    suffix = "" if count == 1 else "s"
    return f"...and {count} more {noun}{suffix} (see Audit Logs)"


def render_scan_summary_text(summary: ScanSummary) -> str:
    scan_id = summary["scan_id"]
    lines = [
        "",
        "Runlayer skills scan summary",
        f"Scan ID: {_single_line(scan_id)}",
        f"Audit Logs: search for scan ID {_single_line(scan_id)}",
        f"Scanned: {summary['skill_count']} skill(s), {summary['file_count']} file(s)",
        f"Skill risk levels: {_format_risk_counts(summary['skill_counts'])}",
        f"File risk levels: {_format_risk_counts(summary['file_counts'])}",
    ]

    if summary["skills"]:
        lines.extend(["", f"{summary['heading']}:"])
        for skill in summary["skills"]:
            lines.append(f"- {_skill_metadata(skill, markdown=False)}")
            if not skill["files"]:
                lines.append(f"  - {_NO_FILE_FINDINGS}")
                lines.append(f"    Next step: {_MODEL_LEVEL_HINT}")
            for file in skill["files"]:
                lines.append(
                    f"  - {_single_line(file['name'])} "
                    f"({_single_line(file['risk_level'])})"
                )
                if not file["reasons"]:
                    lines.append(f"    - {_NO_REASON}")
                for reason in file["reasons"]:
                    lines.append(f"    - [{reason['reason_class']}] {reason['text']}")
                    lines.append(f"      Next step: {reason['hint']}")
                if file["reasons_omitted"]:
                    lines.append(
                        f"    - {_omission_text(file['reasons_omitted'], 'reason')}"
                    )
            if skill["files_omitted"]:
                lines.append(f"  - {_omission_text(skill['files_omitted'], 'file')}")
        if summary["skills_omitted"]:
            lines.append(f"- {_omission_text(summary['skills_omitted'], 'skill')}")

    if summary["exit_explanation"]:
        lines.extend(["", summary["exit_explanation"]])
    return "\n".join(lines)


def render_scan_summary_markdown(summary: ScanSummary) -> str:
    skill_counts = summary["skill_counts"]
    file_counts = summary["file_counts"]
    lines = [
        "## Runlayer skills scan",
        "",
        f"- Scan ID: `{_markdown_text(summary['scan_id'])}`",
        "- Audit Logs: search for this scan ID",
        f"- Skills scanned: {summary['skill_count']}",
        f"- Files scanned: {summary['file_count']}",
        "",
        "| Risk | Skills | Files |",
        "| --- | ---: | ---: |",
    ]
    count_levels = [
        *_RISK_LEVEL_DISPLAY_ORDER,
        *(["Unknown"] if skill_counts["Unknown"] or file_counts["Unknown"] else []),
    ]
    lines.extend(
        f"| {level} | {skill_counts[level]} | {file_counts[level]} |"
        for level in count_levels
    )

    if summary["skills"]:
        lines.extend(["", f"### {summary['heading']}"])
        for skill in summary["skills"]:
            lines.extend(
                [
                    "",
                    f"#### {_skill_metadata(skill, markdown=True)}",
                ]
            )
            if not skill["files"]:
                lines.append(f"- {_NO_FILE_FINDINGS}")
                lines.append(f"  - Next step: {_MODEL_LEVEL_HINT}")
            for file in skill["files"]:
                lines.append(
                    f"- **{_markdown_text(file['name'])}** "
                    f"({_markdown_text(file['risk_level'])})"
                )
                if not file["reasons"]:
                    lines.append(f"  - {_NO_REASON}")
                for reason in file["reasons"]:
                    lines.append(
                        f"  - **{reason['reason_class']}:** "
                        f"{_markdown_code_span(reason['text'])}"
                    )
                    lines.append(f"    - Next step: {_markdown_text(reason['hint'])}")
                if file["reasons_omitted"]:
                    lines.append(
                        f"  - {_omission_text(file['reasons_omitted'], 'reason')}"
                    )
            if skill["files_omitted"]:
                lines.append(f"- {_omission_text(skill['files_omitted'], 'file')}")
        if summary["skills_omitted"]:
            lines.append(f"- {_omission_text(summary['skills_omitted'], 'skill')}")

    if summary["exit_explanation"]:
        lines.extend(["", f"**{_markdown_text(summary['exit_explanation'])}**"])
    return "\n".join(lines)


def emit_scan_summary(
    scanned_skills: list[ScannedSkill],
    scan_id: str,
    fail_on: FailOn | None,
) -> None:
    summary = build_scan_summary(scanned_skills, scan_id, fail_on)
    typer.echo(render_scan_summary_text(summary), err=True)
    github_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary_path:
        try:
            with Path(github_summary_path).open("a", encoding="utf-8") as summary_file:
                summary_file.write("\n")
                summary_file.write(render_scan_summary_markdown(summary))
                summary_file.write("\n")
        except OSError as exc:
            typer.echo(
                f"warning: could not write GITHUB_STEP_SUMMARY: "
                f"{_single_line(str(exc))}",
                err=True,
            )
