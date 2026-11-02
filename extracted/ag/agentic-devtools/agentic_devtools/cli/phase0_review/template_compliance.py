"""Validate the structure of a rendered ``issue.md`` document."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.cli.phase0_review.config import FRONTMATTER_FIELDS

_REQUIRED_SECTIONS = ("Description",)
_OPTIONAL_SECTIONS = ("Dependencies", "Constraints", "Properties", "Provenance")
_STRING_FIELDS = ("id", "title", "type", "status", "provider", "rendered_at")


def _diagnostic(level: str, message: str) -> dict[str, str]:
    return {"level": level, "message": message}


def _split_document(content: str) -> tuple[str | None, list[str], str | None]:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0] != "---":
        return None, lines, "missing opening frontmatter delimiter '---'"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, lines, "missing closing frontmatter delimiter '---'"
    return "\n".join(lines[1:end]), lines[end + 1 :], None


def _headings(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            prefix, _, title = stripped.partition(" ")
            if prefix and set(prefix) == {"#"} and title:
                result.append((len(prefix), title.strip()))
    return result


def _schema_diagnostics(frontmatter: str | None) -> list[dict[str, str]]:
    if frontmatter is None:
        return [_diagnostic("error", "frontmatter cannot be validated")]
    try:
        parsed: Any = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        return [_diagnostic("error", f"frontmatter is not valid YAML: {exc}")]
    if not isinstance(parsed, dict):
        return [_diagnostic("error", "frontmatter must be a mapping")]

    diagnostics: list[dict[str, str]] = []
    for field in FRONTMATTER_FIELDS:
        if field not in parsed:
            diagnostics.append(_diagnostic("error", f"missing required frontmatter field '{field}'"))
    unexpected = sorted(set(parsed) - set(FRONTMATTER_FIELDS))
    diagnostics.extend(_diagnostic("error", f"unexpected frontmatter field '{field}'") for field in unexpected)
    for field in _STRING_FIELDS:
        if field in parsed and not isinstance(parsed[field], str):
            diagnostics.append(_diagnostic("error", f"frontmatter field '{field}' must be a string"))
    if "labels" in parsed and (
        not isinstance(parsed["labels"], list) or any(not isinstance(label, str) for label in parsed["labels"])
    ):
        diagnostics.append(_diagnostic("error", "frontmatter field 'labels' must be a list of strings"))
    return diagnostics


def check_issue_template(
    issue_path: Path,
    *,
    expected_sections: tuple[str, ...] = _REQUIRED_SECTIONS,
) -> list[dict[str, str]]:
    """Return all structural diagnostics for a rendered ``issue.md`` file."""
    try:
        content = issue_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [_diagnostic("error", f"cannot read issue.md: {exc}")]

    frontmatter, body, delimiter_error = _split_document(content)
    diagnostics: list[dict[str, str]] = []
    if delimiter_error:
        diagnostics.append(_diagnostic("error", delimiter_error))
    diagnostics.extend(_schema_diagnostics(frontmatter))

    headings = _headings(body)
    names = [name for _, name in headings]
    for section in expected_sections:
        if section not in names:
            diagnostics.append(_diagnostic("error", f"missing required section '## {section}'"))
    for section in _OPTIONAL_SECTIONS:
        if section not in names:
            diagnostics.append(_diagnostic("warning", f"optional section '## {section}' is missing"))
    if headings and headings[0][0] != 1:
        diagnostics.append(_diagnostic("warning", "document must begin with a level-one title"))
    if any(level != 2 for level, _ in headings[1:]):
        diagnostics.append(_diagnostic("warning", "section headings should use level-two Markdown headings"))
    if names != list(dict.fromkeys(names)):
        diagnostics.append(_diagnostic("warning", "section headings contain duplicates"))
    return diagnostics


def check_issue_template_cli() -> None:
    """Validate one issue.md file and exit non-zero only for errors."""
    parser = argparse.ArgumentParser(
        prog="agdt-check-issue-template",
        description="Check issue.md frontmatter and Markdown section compliance.",
    )
    parser.add_argument("--file", type=Path, default=Path("issue.md"), help="issue.md file to validate")
    args = parser.parse_args()
    diagnostics = check_issue_template(args.file)
    for diagnostic in diagnostics:
        print(f"{diagnostic['level']}: {diagnostic['message']}", file=sys.stderr)
    errors = sum(diagnostic["level"] == "error" for diagnostic in diagnostics)
    warnings = sum(diagnostic["level"] == "warning" for diagnostic in diagnostics)
    print(f"Checked {args.file}: {errors} error(s), {warnings} warning(s)", file=sys.stderr)
    raise SystemExit(1 if errors else 0)
