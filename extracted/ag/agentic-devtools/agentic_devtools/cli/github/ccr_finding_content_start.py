"""Finding-start and legacy-boundary parsing helpers for CCR review bodies."""

from __future__ import annotations

import re
from dataclasses import dataclass

import agentic_devtools.cli.github.ccr_review_format as _format
from agentic_devtools.cli.github.ccr_finding_content_key import (
    _finding_content_key as _finding_content_key,
)
from agentic_devtools.cli.github.ccr_finding_missed_entries import _severity_compatible_legacy_text

_SEVERITY_BULLET_RE = re.compile(
    r"[-*][ \t]+(?:(?:\*\*)?\[(?:P[0-4]|critical|high|medium|low)\](?:\*\*)?[ \t]*"
    r"|\*\*Severity:\*\*[ \t]*)\S",
    re.IGNORECASE,
)


@dataclass
class _FindingStartContext:
    text: str
    location_text: str
    comparison_text: str
    header_matches: dict[int, re.Match[str]]
    legacy_header_offsets: set[int]
    candidates: list[re.Match[str]]
    structured_occurrences: set[int]
    declared_count: int | None
    ambiguous_path_aliases: set[int] | None


def _has_location_metadata(text: str) -> bool:
    return any(
        pattern.search(text)
        for pattern in (_format._FILE_FIELD_START_RE, _format._STANDALONE_FILE_LOCATION_RE, _format._LINE_LOCATION_RE)
    )


def _is_structured_occurrence(
    line: str, heading: re.Match[str] | None, following_text: str, following_location: str
) -> bool:
    return bool(
        re.match(r"<summary>\s*<picture\b", line, re.IGNORECASE)
        or (heading and re.match(r"\[(?:P[0-4]|critical|high|medium|low)\]", heading.group(1), re.I))
        or _has_location_metadata(following_text)
        or _format._STANDALONE_FILE_LOCATION_RE.search(following_location)
    )


def _next_boundary(context: _FindingStartContext, index: int, match: re.Match[str]) -> int:
    if index + 1 == len(context.candidates):
        return len(context.text)
    next_candidate = context.candidates[index + 1]
    for offset in sorted(context.legacy_header_offsets):
        header = context.header_matches[offset]
        if (
            match.start() < offset < next_candidate.start()
            and not context.text[header.end() : next_candidate.start()].strip()
        ):
            return offset
    return next_candidate.start()


def _legacy_header_matches(location_text: str) -> dict[int, re.Match[str]]:
    return {
        match.start(): match
        for pattern in (_format._ENTRY_HEADER_INLINE_RE, _format._ENTRY_HEADER_ONLY_RE)
        for match in pattern.finditer(location_text)
        if not _format._FILE_FIELD_START_RE.match(match.group(0))
        and not _is_explanatory_standalone_location(location_text, match)
    }


def _structured_finding_occurrences(context: _FindingStartContext) -> set[int]:
    structured_occurrences: set[int] = set()
    for index, match in enumerate(context.candidates):
        line = match.group(0).lstrip()
        heading = re.match(r"#{1,6}[ \t]+(.*)", line)
        boundary = _next_boundary(context, index, match)
        following_text = context.text[match.end() : boundary]
        following_location = context.location_text[match.end() : boundary]
        if _is_structured_occurrence(line, heading, following_text, following_location):
            structured_occurrences.add(match.start())
    return structured_occurrences


def _location_parts(path: str, surrounding_text: str) -> tuple[str, int | None]:
    suffix = re.fullmatch(r"(.+?):(\d+)", path)
    if suffix:
        return suffix.group(1), int(suffix.group(2))
    line_match = _format._LINE_LOCATION_RE.search(surrounding_text)
    return path, int(line_match.group(1)) if line_match else None


def _legacy_location(context: _FindingStartContext, header: re.Match[str]) -> tuple[str, int | None]:
    location = header.group(1).strip()
    path, line = _location_parts(location, "")
    if not _format._is_inline_code_header(context.location_text, header):
        path = _format._unescape_markdown_path(path)
    return path, line


def _structured_location(
    context: _FindingStartContext,
    structured_start: int,
    header_offset: int,
) -> tuple[str, int | None] | None:
    structured_text = context.location_text[structured_start:header_offset]
    location_match = _format._FILE_LOCATION_RE.search(structured_text)
    if location_match:
        path = (location_match.group(1) or location_match.group(2) or "").strip()
        if location_match.group(1) is None:
            path = _format._unescape_markdown_path(path)
        return _location_parts(path, structured_text)
    standalone_match = _format._STANDALONE_FILE_LOCATION_RE.search(structured_text)
    if standalone_match is None:
        return None
    path, line = _location_parts(standalone_match.group(1).strip(), "")
    return path, line


def _record_ambiguous_path_alias(context: _FindingStartContext, offset: int) -> None:
    if context.ambiguous_path_aliases is None:
        return
    next_occurrence = min(
        (start for start in context.structured_occurrences if start > offset),
        default=len(context.text),
    )
    headings = re.compile(
        r"^[ \t]{0,3}#{1,6}[ \t]+(?!(?:\[(?:P[0-4]|critical|high|medium|low)\]))\S.*$",
        re.IGNORECASE | re.MULTILINE,
    )
    for candidate in headings.finditer(context.text[offset:]):
        candidate_start = offset + candidate.start()
        if candidate_start > next_occurrence:
            break
        next_candidate = min(
            (item.start() for item in context.candidates if item.start() > candidate_start),
            default=len(context.text),
        )
        following = context.comparison_text[offset + candidate.end() : next_candidate]
        if not _has_location_metadata(following):
            context.ambiguous_path_aliases.add(offset)
            break
        if candidate_start == next_occurrence:
            break


def _is_duplicate_legacy_header(context: _FindingStartContext, offset: int) -> bool:
    header = context.header_matches[offset]
    legacy_path, legacy_line = _legacy_location(context, header)
    previous = max((start for start in context.structured_occurrences if start < offset), default=None)
    if previous is None:
        return False
    structured_location = _structured_location(context, previous, offset)
    if structured_location is None:
        return False
    structured_path, structured_line = structured_location
    same_path = _format.ccr_path_match_key(legacy_path) == _format.ccr_path_match_key(structured_path)
    same_line = legacy_line is None or structured_line is None or legacy_line == structured_line
    if not same_path or not same_line:
        return False
    next_candidate = min(
        (candidate.start() for candidate in context.candidates if candidate.start() > offset),
        default=len(context.text),
    )
    next_header = min(
        (candidate for candidate in context.legacy_header_offsets if candidate > offset),
        default=len(context.text),
    )
    next_offset = min(next_candidate, next_header)
    structured_match = next((item for item in context.candidates if item.start() == previous), None)
    compatible, normalized_legacy = _severity_compatible_legacy_text(
        structured_match,
        context.comparison_text[header.end() : next_offset],
    )
    if not compatible:
        return False
    structured_content = _finding_content_key(context.comparison_text[previous:offset])
    duplicate = bool(structured_content and structured_content == _finding_content_key(normalized_legacy))
    if context.declared_count is not None and legacy_path != structured_path:
        if duplicate and ("\u200b" in legacy_path or "\u200b" in structured_path):
            _record_ambiguous_path_alias(context, offset)
        return False
    return duplicate


def _legacy_headers(context: _FindingStartContext) -> list[int]:
    legacy_headers: list[int] = []
    for offset in context.legacy_header_offsets:
        previous_line = next((line for line in reversed(context.text[:offset].splitlines()) if line.strip()), "")
        if _format._FINDING_START_RE.match(previous_line):
            header = context.header_matches[offset]
            next_line = next((line for line in context.text[header.end() :].splitlines() if line.strip()), "")
            if not _format._SEVERITY_PREFIX_RE.match(next_line.lstrip(" \t-*")):
                continue
        legacy_headers.append(offset)
    return legacy_headers


def _has_declared_count_slot(
    context: _FindingStartContext,
    legacy_headers: list[int],
    starts: list[re.Match[str]],
) -> bool:
    if context.declared_count is None:
        return False
    duplicate_headers = sum(not _is_duplicate_legacy_header(context, offset) for offset in legacy_headers)
    return context.declared_count > duplicate_headers + len(
        context.structured_occurrences | {match.start() for match in starts}
    )


def _has_legacy_explanation(
    context: _FindingStartContext,
    header_end: int,
    end: int,
) -> bool:
    return any(
        line.strip()
        and not _format._FILE_FIELD_START_RE.match(line)
        and not _format._LINE_LOCATION_RE.fullmatch(line.strip())
        for line in context.comparison_text[header_end:end].splitlines()
    )


def _legacy_entry_header_end(
    context: _FindingStartContext,
    match_start: int,
    legacy_headers: list[int],
) -> tuple[int, re.Match[str] | None, re.Match[str] | None]:
    separator = re.search(r"\r?\n[ \t]*\r?\n[ \t]*$", context.text[:match_start])
    preceding = max(
        (
            offset
            for offset in legacy_headers
            if offset < match_start and (separator is None or offset < separator.start())
        ),
        default=None,
    )
    header = context.header_matches.get(preceding) if preceding is not None else None
    end = header.end() if header else context.text.find("\n", preceding) if preceding is not None else -1
    if end < 0:
        end = separator.start() if separator else match_start
    return end, separator, header


def _is_legacy_entry_candidate(
    context: _FindingStartContext,
    index: int,
    match: re.Match[str],
    legacy_headers: list[int],
    starts: list[re.Match[str]],
) -> bool:
    line = match.group(0).lstrip()
    heading = re.match(r"#{1,6}[ \t]+(.*)", line)
    boundary = _next_boundary(context, index, match)
    following = context.text[match.end() : boundary]
    following_location = context.location_text[match.end() : boundary]
    has_location = _has_location_metadata(following) or bool(
        _format._STANDALONE_FILE_LOCATION_RE.search(following_location)
    )
    has_severity = bool(heading and re.match(r"\[(?:P[0-4]|critical|high|medium|low)\]", heading.group(1), re.I))
    if has_location or has_severity or re.match(r"<summary>\s*<picture\b", line, re.IGNORECASE):
        return False
    header_end, separator, _ = _legacy_entry_header_end(context, match.start(), legacy_headers)
    has_explanation = _has_legacy_explanation(
        context,
        header_end,
        separator.start() if separator else match.start(),
    )
    severity_bullet = _SEVERITY_BULLET_RE.match(line)
    separated = separator and not any(separator.start() < offset < match.start() for offset in legacy_headers)
    is_severity_bullet = bool(
        severity_bullet and has_explanation and (separated or _has_declared_count_slot(context, legacy_headers, starts))
    )
    is_finding_heading = bool(
        heading and len(line) - len(line.lstrip("#")) <= 3 and _has_declared_count_slot(context, legacy_headers, starts)
    )
    return not (is_severity_bullet or is_finding_heading)


def _finding_start_matches(
    text: str,
    *,
    metadata_text: str | None = None,
    content_text: str | None = None,
    legacy_header_offsets: set[int] | None = None,
    declared_count: int | None = None,
    ambiguous_path_aliases: set[int] | None = None,
) -> list[re.Match[str]]:
    """Return structured finding starts without splitting legacy explanations."""
    location_text = metadata_text if metadata_text is not None else text
    context = _FindingStartContext(
        text=text,
        location_text=location_text,
        comparison_text=content_text if content_text is not None else text,
        header_matches=_legacy_header_matches(location_text),
        legacy_header_offsets=set(),
        candidates=list(_format._FINDING_START_RE.finditer(text)),
        structured_occurrences=set(),
        declared_count=declared_count,
        ambiguous_path_aliases=ambiguous_path_aliases,
    )
    context.legacy_header_offsets = (
        legacy_header_offsets & set(context.header_matches)
        if legacy_header_offsets is not None
        else set(context.header_matches)
    )
    context.structured_occurrences = _structured_finding_occurrences(context)
    legacy_headers = _legacy_headers(context)
    starts: list[re.Match[str]] = []
    last_start = -1
    for index, match in enumerate(context.candidates):
        inside_legacy_entry = any(last_start < offset < match.start() for offset in legacy_headers)
        if inside_legacy_entry and _is_legacy_entry_candidate(context, index, match, legacy_headers, starts):
            continue
        starts.append(match)
        last_start = match.start()
    return starts


def _is_explanatory_standalone_location(text: str, match: re.Match[str]) -> bool:
    """Return whether a standalone backticked location is explanatory, not an entry header."""
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.start())
    line = text[line_start : line_end if line_end >= 0 else len(text)].removesuffix("\r")
    if not _format._STANDALONE_FILE_LOCATION_RE.fullmatch(line):
        return False
    next_line_start = line_end + 1
    next_nonblank_line = next((candidate for candidate in text[next_line_start:].splitlines() if candidate.strip()), "")
    if re.match(r"^[ \t]{0,3}[*-][ \t]+\S", next_nonblank_line):
        return False
    preceding_text = text[:line_start]
    if re.search(r"(?:\r?\n)[ \t]*(?:\r?\n)$", preceding_text):
        return False
    preceding_lines = preceding_text.splitlines()
    previous_line = next((line.strip() for line in reversed(preceding_lines) if line.strip()), "")
    if not previous_line:
        return False
    return not (
        _format._FINDING_START_RE.match(previous_line)
        or _format._FILE_FIELD_START_RE.match(previous_line)
        or _format._LINE_LOCATION_RE.match(previous_line)
        or re.search(r"</?summary\b", previous_line, re.IGNORECASE)
    )
