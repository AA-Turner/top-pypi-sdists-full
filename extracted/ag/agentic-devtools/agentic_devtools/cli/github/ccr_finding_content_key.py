"""Canonicalization helpers for CCR finding content."""

from __future__ import annotations

import re
from dataclasses import dataclass

import agentic_devtools.cli.github.ccr_review_format as _format


@dataclass
class _FindingContentState:
    key_parts: list[tuple[str, str]]
    prose_lines: list[str]
    fenced_lines: list[str]
    indented_lines: list[str]
    open_delim: str | None = None
    has_content: bool = False


def _normalize_prose(text: str) -> str:
    parts: list[str] = []
    offset = 0
    for match in _format._INLINE_CODE_COMPARISON_RE.finditer(text):
        parts.append(re.sub(r"\s+", " ", text[offset : match.start()]))
        parts.append(match.group(0))
        offset = match.end()
    parts.append(re.sub(r"\s+", " ", text[offset:]))
    return "".join(parts).strip()


def _append_prose(state: _FindingContentState) -> None:
    normalized = _normalize_prose("".join(state.prose_lines))
    if normalized:
        state.key_parts.append(("prose", normalized))
    state.prose_lines.clear()


def _append_indented_code(state: _FindingContentState) -> None:
    while state.indented_lines and not state.indented_lines[-1].strip():
        state.indented_lines.pop()
    if state.indented_lines:
        state.key_parts.append(("indented", "".join(state.indented_lines).rstrip("\r\n")))
        state.indented_lines.clear()


def _is_finding_metadata_line(
    line: str,
    metadata_line: str,
    has_content: bool,
) -> bool:
    line_without_newline = line.removesuffix("\n").removesuffix("\r")
    metadata_line = metadata_line.removesuffix("\n").removesuffix("\r")
    return bool(
        _format._FILE_FIELD_START_RE.match(metadata_line)
        or _format._LINE_LOCATION_RE.fullmatch(metadata_line.strip())
        or (not has_content and _format._STANDALONE_FILE_LOCATION_RE.match(line_without_newline))
        or (not has_content and _format._FINDING_START_RE.match(line))
    )


def _process_finding_content_line(
    line: str,
    metadata_line: str,
    line_start_offset: int,
    inline_span_ranges: tuple[tuple[int, int], ...],
    state: _FindingContentState,
) -> None:
    line_without_newline = line.removesuffix("\n").removesuffix("\r")
    inside_inline_span = any(start < line_start_offset < end for start, end in inline_span_ranges)
    fence_match = None if inside_inline_span else _format._FENCE_DELIM_RE.match(line_without_newline)
    if state.open_delim is not None:
        state.fenced_lines.append(line)
        if (
            fence_match
            and fence_match.group(1)[0] == state.open_delim[0]
            and len(fence_match.group(1)) >= len(state.open_delim)
            and line_without_newline[fence_match.end() :].strip() == ""
        ):
            state.key_parts.append(("fenced", "".join(state.fenced_lines).removesuffix("\n").removesuffix("\r")))
            state.fenced_lines.clear()
            state.open_delim = None
        return
    is_indented_code = (
        not inside_inline_span
        and bool(line_without_newline.strip())
        and re.match(r"^(?: {4,}| {0,3}\t)", line_without_newline) is not None
    )
    if state.indented_lines:
        if not line_without_newline.strip() or is_indented_code:
            state.indented_lines.append(line)
            return
        _append_indented_code(state)
    if is_indented_code:
        _append_prose(state)
        state.indented_lines.append(line)
        state.has_content = True
        return
    if not inside_inline_span and re.fullmatch(
        r"[ \t]*</?details\b[^>]*>[ \t]*\r?", line_without_newline, re.IGNORECASE
    ):
        return
    if fence_match and not (fence_match.group(1).startswith("`") and "`" in line_without_newline[fence_match.end() :]):
        _append_prose(state)
        state.open_delim = fence_match.group(1)
        state.fenced_lines.append(line)
        state.has_content = True
        return
    if _is_finding_metadata_line(line, metadata_line, state.has_content):
        return
    if not state.has_content and not line_without_newline.strip():
        state.prose_lines.append(line)
        return
    bullet_match = re.match(r"^[ \t]{0,3}[*-] ", line) if not state.has_content else None
    state.prose_lines.append(line[bullet_match.end() :] if bullet_match else line)
    state.has_content = True


def _remove_appended_legacy_spans(
    text: str,
    spans: tuple[tuple[int, int], ...],
    source_offset: int,
) -> str:
    parts: list[str] = []
    content_offset = 0
    for start, end in spans:
        relative_start = start - source_offset
        relative_end = end - source_offset
        if content_offset <= relative_start <= len(text) and relative_start <= relative_end:
            parts.append(text[content_offset:relative_start])
            content_offset = min(relative_end, len(text))
    parts.append(text[content_offset:])
    return "".join(parts)


def _finding_content_key(
    finding_body: str,
    appended_legacy_spans: tuple[tuple[int, int], ...] = (),
    source_offset: int = 0,
) -> tuple[tuple[str, str], ...]:
    finding_body = _remove_appended_legacy_spans(finding_body, appended_legacy_spans, source_offset)
    masked_body = _format._mask_fenced_blocks(finding_body)
    masked_body = _format._INLINE_CODE_COMPARISON_RE.sub(
        lambda match: re.sub(r"[^\r\n]", " ", match.group(0)),
        masked_body,
    )
    masked_body = re.sub(
        r"(?m)^(?: {4,}| {0,3}\t)[^\r\n]*",
        lambda match: " " * len(match.group(0)),
        masked_body,
    )
    resolution_statuses = tuple(_format._EXPLICITLY_RESOLVED_RE.finditer(masked_body))
    if resolution_statuses:
        parts: list[str] = []
        content_offset = 0
        for match in resolution_statuses:
            parts.append(finding_body[content_offset : match.start()])
            content_offset = match.end()
        parts.append(finding_body[content_offset:])
        finding_body = "".join(parts)
    state = _FindingContentState([], [], [], [])
    unfenced_body = _format._mask_fenced_blocks(finding_body)
    inline_span_ranges = tuple(
        (match.start(), match.end()) for match in _format._INLINE_CODE_COMPARISON_RE.finditer(unfenced_body)
    )
    metadata_body = _format._INLINE_CODE_COMPARISON_RE.sub(
        lambda match: re.sub(r"[^\r\n]", " ", match.group(0)),
        unfenced_body,
    )
    line_offset = 0
    for line in finding_body.splitlines(keepends=True):
        line_start_offset = line_offset
        line_offset += len(line)
        metadata_line = metadata_body[line_start_offset:line_offset]
        _process_finding_content_line(line, metadata_line, line_start_offset, inline_span_ranges, state)
    _append_indented_code(state)
    state.key_parts.append(("fenced", "".join(state.fenced_lines)))
    _append_prose(state)
    return tuple(state.key_parts)
