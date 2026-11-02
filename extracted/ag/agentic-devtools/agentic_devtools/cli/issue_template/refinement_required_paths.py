"""Parse required repository paths from a structured refinement section."""

import re as _re

from agentic_devtools.cli.issue_template.refinement_body_sections import (
    find_refinement_section_spans as _find_refinement_section_spans,
)
from agentic_devtools.cli.issue_template.refinement_paths import normalize_refinement_path as _normalize_refinement_path

_SECTION_NAME = "Affected Files & Components"
_MARKDOWN_ENTRY = _re.compile(r"-[ \t]+`([^`]*)`[ \t]*—[ \t]*(.*)")
_JIRA_ENTRY = _re.compile(r"\*[ \t]+\{\{([^{}]*)\}\}[ \t]*—[ \t]*(.*)")
_FENCE = _re.compile(r" {0,3}(`{3,}|~{3,})(.*)")
_FENCE_END = _re.compile(r" {0,3}(`{3,}|~{3,})[ \t]*")
_PATH_MESSAGES = {
    "empty_token": "Required path token is empty.",
    "control_character": "Required path token contains a control character.",
    "whitespace_character": "Required path token contains whitespace.",
    "absolute_path": "Required path must be repository-relative.",
    "traversal_segment": 'Required path must not contain "." or ".." segments.',
}
_SECTION_ERRORS = {
    0: ("missing_required_section", f"Required section '{_SECTION_NAME}' is missing."),
    2: ("repeated_required_section", f"Required section '{_SECTION_NAME}' appears more than once."),
}
_MALFORMED = {
    "code": "malformed_required_entry",
    "path": None,
    "message": "Required path entry does not match the Markdown or Jira grammar.",
}


def _consume_required_entry(
    line: str,
    syntax: str,
    fence: str,
) -> tuple[str, str | None, dict[str, str | None] | None]:
    if syntax == "markdown":
        opening = _FENCE.fullmatch(line)
        closing = _FENCE_END.fullmatch(line)
        starts_fence = opening is not None and not (opening[1][0] == "`" and "`" in opening[2])
        if fence:
            if fence and closing and closing[1][0] == fence[0] and len(closing[1]) >= len(fence):
                fence = ""
            return fence, None, _MALFORMED.copy()
        if starts_fence and opening is not None:
            return opening[1], None, _MALFORMED.copy()

    pattern = _MARKDOWN_ENTRY if syntax == "markdown" else _JIRA_ENTRY
    match = pattern.fullmatch(line)
    if match is None or not match[2].strip(" \t"):
        return fence, None, _MALFORMED.copy()
    normalized, lexical_error = _normalize_refinement_path(match[1].strip(" \t"))
    if lexical_error is not None:
        diagnostic = {
            "code": "invalid_required_path",
            "path": None,
            "message": _PATH_MESSAGES[lexical_error],
        }
        return fence, None, diagnostic
    return fence, normalized, None


def parse_required_refinement_paths(body: str) -> dict[str, list[str] | list[dict[str, str | None]]]:
    """Return normalized paths and deterministic diagnostics from one required section."""
    spans = _find_refinement_section_spans(body, _SECTION_NAME)
    if len(spans) != 1:
        code, message = _SECTION_ERRORS[min(len(spans), 2)]
        return {"paths": [], "errors": [{"code": code, "path": None, "message": message}]}

    physical_body = _re.sub(r"(?:\r\n|\r|\n)\Z", "", body)
    lines = _re.split(r"\r\n|\r|\n", physical_body)
    start, end, syntax = spans[0]
    paths: list[str] = []
    errors: list[dict[str, str | None]] = []
    fence = ""
    for line in (line for line in lines[start + 1 : end] if line.strip(" \t")):
        fence, path, error = _consume_required_entry(line, syntax, fence)
        if error is not None:
            errors.append(error)
        if path is not None and path not in paths:
            paths.append(path)

    if not paths:
        errors.append(
            {
                "code": "empty_required_section",
                "path": None,
                "message": f"Required section '{_SECTION_NAME}' has no valid entries.",
            }
        )
    errors.sort(key=lambda error: (error["code"] or "", error["path"] or "", error["message"] or ""))
    return {"paths": paths, "errors": errors}
