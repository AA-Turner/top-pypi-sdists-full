"""Parsing helpers for legacy findings in recovered CCR sections."""

from __future__ import annotations

import re

import agentic_devtools.cli.github.ccr_review_format as _format

__all__ = [
    "_EXPLANATION_HEADING_RE",
    "_LEGACY_SEVERITY_ENTRY_RE",
    "_independent_legacy_spans",
    "_is_duplicate_picture_legacy_entry",
    "_legacy_severity_location",
]

_LEGACY_SEVERITY_ENTRY_RE = re.compile(
    r"^[ \t]{0,3}\*\*(?P<location>[^*\n]+)\*\*[ \t]+"
    r"\[(?P<severity>P[0-4]|critical|high|medium|low)\][ \t]+(?P<title>\S.*)$",
    re.IGNORECASE | re.MULTILINE,
)
_EXPLANATION_HEADING_RE = re.compile(
    r"^[ \t]{0,3}#{1,6}[ \t]+Why this fails[ \t]*#*[ \t]*\r?$",
    re.IGNORECASE | re.MULTILINE,
)
_SEVERITY_NAME_TO_LEVEL = {"CRITICAL": "P0", "HIGH": "P1", "MEDIUM": "P2", "LOW": "P3"}


def _structured_start_severity(structured_match: re.Match[str] | None) -> str:
    if structured_match is None:
        return ""
    line = structured_match.group(0).lstrip()
    picture = re.search(r"<picture\b.*?</picture>", line, re.IGNORECASE)
    picture_severity = None
    if picture:
        alt = re.search(r"\balt=[\"']([^\"']+)[\"']", picture.group(0), re.IGNORECASE)
        picture_severity = _format._SEVERITY_RE.search(alt.group(1)) if alt else None
    line = re.sub(r"<picture\b.*?</picture>", "", line, flags=re.IGNORECASE)
    line = re.sub(r"</?summary>", "", line, flags=re.IGNORECASE).strip()
    line = line.lstrip("#*- ").strip()
    severity_prefix = _format._SEVERITY_PREFIX_RE.match(line)
    severity = picture_severity or severity_prefix
    return next(group for group in severity.groups() if group).upper() if severity else ""


def _severity_compatible_legacy_text(
    structured_match: re.Match[str] | None,
    legacy_text: str,
) -> tuple[bool, str]:
    legacy_lines = legacy_text.splitlines(keepends=True)
    first_index = next((index for index, line in enumerate(legacy_lines) if line.strip()), None)
    if first_index is None:
        return True, legacy_text
    first_line = legacy_lines[first_index]
    if re.match(r"^(?: {4,}| {0,3}\t)", first_line) is not None:
        return True, legacy_text
    leading = len(first_line) - len(first_line.lstrip(" \t:*-"))
    legacy_severity = _format._SEVERITY_PREFIX_RE.match(first_line[leading:])
    if legacy_severity is None:
        return True, legacy_text
    legacy_level = next(group for group in legacy_severity.groups() if group).upper()
    structured_level = _structured_start_severity(structured_match)
    legacy_level = _SEVERITY_NAME_TO_LEVEL.get(legacy_level, legacy_level)
    structured_level = _SEVERITY_NAME_TO_LEVEL.get(structured_level, structured_level)
    if structured_level and structured_level != legacy_level:
        return False, legacy_text
    legacy_lines[first_index] = first_line[:leading] + first_line[leading + legacy_severity.end() :]
    return True, "".join(legacy_lines)


def _legacy_severity_location(legacy_entry: re.Match[str]) -> tuple[str, int | None]:
    """Parse a legacy location while preserving paths enclosed in inline code."""
    location = legacy_entry.group("location").strip()
    code_span = _format._INLINE_CODE_COMPARISON_RE.fullmatch(location)
    if code_span:
        ticks = code_span.group("ticks")
        location = location[len(ticks) : -len(ticks)]
    else:
        location = _format._unescape_markdown_path(location)
    suffix = re.fullmatch(r"(.+?):(\d+)", location)
    if suffix:
        return suffix.group(1), int(suffix.group(2))
    return location, None


def _independent_legacy_spans(
    block: str,
    *,
    structured_path: str,
    structured_line: int | None,
) -> tuple[tuple[int, int], ...]:
    """Return legacy-entry spans that are not the structured finding occurrence."""
    masked = _format._mask_fenced_blocks(block)
    headers = {
        match.start(): match
        for pattern in (_format._ENTRY_HEADER_INLINE_RE, _format._ENTRY_HEADER_ONLY_RE)
        for match in pattern.finditer(masked)
        if not _format._FILE_FIELD_START_RE.match(match.group(0))
        and not _format._is_explanatory_standalone_location(masked, match)
    }
    offsets = sorted(headers)
    independent: list[tuple[int, int]] = []
    structured_content = block[: offsets[0]] if offsets else block
    structured_content_key = _format._finding_content_key(structured_content)
    has_structured_content = any(value for _kind, value in structured_content_key)
    if offsets:
        first_finding_start = _format._FINDING_START_RE.match(masked)
        first_header = headers[offsets[0]]
        line_start = masked.rfind("\n", 0, first_header.start()) + 1
        line_end = masked.find("\n", first_header.start())
        first_header_line = masked[line_start : line_end if line_end >= 0 else len(masked)].removesuffix("\r")
        content_before_location = block[first_finding_start.end() : first_header.start()] if first_finding_start else ""
        has_content_before_location = any(
            value for _kind, value in _format._finding_content_key(content_before_location)
        )
        if (
            first_finding_start
            and (not has_structured_content or not has_content_before_location)
            and _format._STANDALONE_FILE_LOCATION_RE.fullmatch(first_header_line)
        ):
            offsets = offsets[1:]
            structured_content = block[: offsets[0]] if offsets else block
            structured_content_key = _format._finding_content_key(structured_content)
            has_structured_content = any(value for _kind, value in structured_content_key)
    for index, offset in enumerate(offsets):
        header = headers[offset]
        location = header.group(1).strip()
        suffix = re.fullmatch(r"(.+?):(\d+)", location)
        legacy_path = suffix.group(1) if suffix else location
        if not _format._is_inline_code_header(masked, header):
            legacy_path = _format._unescape_markdown_path(legacy_path)
        legacy_line = int(suffix.group(2)) if suffix else None
        same_path = legacy_path == structured_path
        same_line = structured_line is None or legacy_line is None or structured_line == legacy_line
        end = offsets[index + 1] if index + 1 < len(offsets) else len(block)
        legacy_content = block[header.end() : end]
        structured_match = _format._FINDING_START_RE.search(_format._mask_fenced_blocks(structured_content))
        severity_compatible, normalized_legacy_content = _severity_compatible_legacy_text(
            structured_match,
            legacy_content,
        )
        legacy_content_key = _format._finding_content_key(normalized_legacy_content)
        same_content = has_structured_content and severity_compatible and structured_content_key == legacy_content_key
        if same_path and same_line and same_content:
            continue
        independent.append((offset, end))
    return tuple(independent)


def _is_duplicate_picture_legacy_entry(
    previous: _format.CCRFinding,
    legacy_entry: re.Match[str],
    legacy_content: str,
) -> bool:
    """Return whether a legacy entry duplicates a preceding picture-summary finding."""
    if not re.search(r"<picture\b", previous.body, re.IGNORECASE):
        return False
    path, line = _legacy_severity_location(legacy_entry)
    severity = legacy_entry.group("severity").upper()
    severity = _SEVERITY_NAME_TO_LEVEL.get(severity, severity)
    previous_severity = previous.severity.upper()
    previous_severity = _SEVERITY_NAME_TO_LEVEL.get(previous_severity, previous_severity)
    return (
        _format.ccr_path_match_key(path) == _format.ccr_path_match_key(previous.path)
        and line == previous.line
        and severity == previous_severity
        and legacy_entry.group("title").strip() == previous.title
        and _format._finding_content_key(legacy_content) == _format._finding_content_key(previous.body)
    )
