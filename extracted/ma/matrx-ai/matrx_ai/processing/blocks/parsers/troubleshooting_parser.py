"""Troubleshooting parser — port of parseTroubleshootingMarkdown.ts."""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.troubleshooting import (
    TroubleshootingBlockData,
    TroubleshootingIssue,
    TroubleshootingLink,
    TroubleshootingSolution,
    TroubleshootingStep,
)

_SYMPTOM_RE = re.compile(r'^\*\*Symptom:\*\*\s*(.*)', re.IGNORECASE)
_SOLUTION_RE = re.compile(r'^(\d+)\.\s*\*\*([^*]+)\*\*:?\s*(.*)')
_STEP_RE = re.compile(r'^\s*-\s*(.+)')
_CAUSE_RE = re.compile(r'^(?:\d+\.\s*|-\s*)(.+)')
_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
_DIFFICULTY_RE = re.compile(r'\((easy|medium|hard)\)', re.IGNORECASE)
_TIME_RE = re.compile(r'\((\d+(?:\.\d+)?\s*(?:min|minute|hour|hr)s?)\)', re.IGNORECASE)
_CODE_RE = re.compile(r'`([^`]+)`')
_SEVERITY_KEYWORDS = {
    "critical": "critical", "high": "high", "medium": "medium", "low": "low",
}


def parse_troubleshooting(content: str) -> TroubleshootingBlockData | None:
    """Parse troubleshooting markdown into structured data."""
    try:
        clean = re.sub(r'</?troubleshooting>', '', content).strip()
        lines = clean.split("\n")

        title = ""
        description: str | None = None
        issues: list[TroubleshootingIssue] = []
        current_issue: TroubleshootingIssue | None = None
        current_solution: TroubleshootingSolution | None = None
        section = ""  # "causes" | "solutions" | "related"
        in_code_block = False
        issue_idx = 0
        solution_idx = 0
        step_idx = 0

        for line in lines:
            trimmed = line.strip()

            if trimmed.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                if current_solution and current_solution.steps:
                    current_solution.steps[-1].commands.append(trimmed)
                continue

            if not trimmed:
                continue

            # Title
            if trimmed.startswith("###") and not title:
                title = re.sub(r'^#+\s*', '', trimmed).strip()
                continue

            # Symptom → new issue
            sym_m = _SYMPTOM_RE.match(trimmed)
            if sym_m:
                if current_solution and current_issue:
                    current_issue.solutions.append(current_solution)
                    current_solution = None
                if current_issue:
                    issues.append(current_issue)
                symptom_text = sym_m.group(1).strip() or trimmed
                severity = _detect_severity(symptom_text)
                current_issue = TroubleshootingIssue(
                    id=f"issue-{issue_idx}",
                    symptom=symptom_text,
                    severity=severity,
                )
                issue_idx += 1
                section = "causes"
                current_solution = None
                continue

            # Section headers
            lower = trimmed.lower()
            if "possible cause" in lower or lower.startswith("**cause"):
                section = "causes"
                continue
            if "solution" in lower and trimmed.startswith("**"):
                if current_solution and current_issue:
                    current_issue.solutions.append(current_solution)
                    current_solution = None
                section = "solutions"
                continue
            if "related issue" in lower:
                if current_solution and current_issue:
                    current_issue.solutions.append(current_solution)
                    current_solution = None
                section = "related"
                continue

            if current_issue is None:
                if title and description is None and not trimmed.startswith("**"):
                    description = trimmed
                continue

            # Solutions
            if section == "solutions":
                sol_m = _SOLUTION_RE.match(trimmed)
                if sol_m:
                    if current_solution:
                        current_issue.solutions.append(current_solution)
                    desc = sol_m.group(3).strip()
                    current_solution = TroubleshootingSolution(
                        id=f"solution-{solution_idx}",
                        title=sol_m.group(2).strip(),
                        description=desc or None,
                    )
                    solution_idx += 1
                    continue

                step_m = _STEP_RE.match(trimmed)
                if step_m and current_solution is not None:
                    step_text = step_m.group(1).strip()
                    links = [
                        TroubleshootingLink(title=m.group(1), url=m.group(2))
                        for m in _LINK_RE.finditer(step_text)
                    ]
                    diff_m = _DIFFICULTY_RE.search(step_text)
                    time_m = _TIME_RE.search(step_text)
                    commands = _CODE_RE.findall(step_text)
                    # Use the full step text as description, strip inline markers
                    desc_text = _LINK_RE.sub('', step_text)
                    desc_text = _DIFFICULTY_RE.sub('', desc_text)
                    desc_text = _TIME_RE.sub('', desc_text).strip()
                    current_solution.steps.append(TroubleshootingStep(
                        id=f"step-{step_idx}",
                        title=desc_text[:80] or f"Step {step_idx + 1}",
                        description=desc_text,
                        commands=commands,
                        difficulty=diff_m.group(1).lower() if diff_m else None,
                        estimated_time=time_m.group(1) if time_m else None,
                        links=links,
                    ))
                    step_idx += 1
                    continue

            # Causes
            if section == "causes":
                cause_m = _CAUSE_RE.match(trimmed)
                if cause_m:
                    current_issue.causes.append(cause_m.group(1).strip())
                    continue

            # Related issues
            if section == "related":
                cause_m = _CAUSE_RE.match(trimmed)
                if cause_m:
                    current_issue.related_issues.append(cause_m.group(1).strip())

        if current_solution and current_issue:
            current_issue.solutions.append(current_solution)
        if current_issue:
            issues.append(current_issue)

        return TroubleshootingBlockData(
            title=title or "Troubleshooting Guide",
            description=description,
            issues=issues,
        )
    except Exception:
        return None


def _detect_severity(text: str) -> str | None:
    lower = text.lower()
    for kw, val in _SEVERITY_KEYWORDS.items():
        if kw in lower:
            return val
    return None
