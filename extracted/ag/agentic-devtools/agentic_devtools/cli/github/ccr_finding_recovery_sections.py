"""Parsing helpers for missed and suppressed CCR finding sections."""

from __future__ import annotations

import re
from dataclasses import replace

import agentic_devtools.cli.github.ccr_review_format as _format
from agentic_devtools.cli.github.ccr_finding_missed_entries import (
    _EXPLANATION_HEADING_RE,
    _LEGACY_SEVERITY_ENTRY_RE,
    _independent_legacy_spans,
    _is_duplicate_picture_legacy_entry,
    _legacy_severity_location,
)


def _summary_declaration_bounds(
    masked: str,
    declaration: re.Match[str],
    next_declaration: int,
) -> tuple[int, bool]:
    details_depth = sum(
        -1 if tag.group(0).startswith("</") else 1
        for tag in re.finditer(r"</?details\b[^>]*>", masked[: declaration.start()], re.IGNORECASE)
    )
    containing_depth = max(details_depth - 1, 0)
    summary_in_details = details_depth > 0
    for tag in re.finditer(r"</?details\b[^>]*>", masked[declaration.end() : next_declaration], re.IGNORECASE):
        if tag.group(0).startswith("</"):
            details_depth -= 1
            if details_depth == containing_depth:
                return declaration.end() + tag.start(), summary_in_details
        else:
            details_depth += 1
    return next_declaration, summary_in_details


def _declaration_content_bounds(
    body: str,
    masked: str,
    declarations: list[re.Match[str]],
    index: int,
) -> tuple[int, int]:
    declaration = declarations[index]
    content_start = body.find("\n", declaration.end())
    content_start = len(body) if content_start < 0 else content_start + 1
    next_declaration = declarations[index + 1].start() if index + 1 < len(declarations) else len(body)
    is_summary = declaration.group(0).lstrip().lower().startswith("<summary>")
    if is_summary:
        content_end, summary_in_details = _summary_declaration_bounds(masked, declaration, next_declaration)
        if not summary_in_details and "previously" in declaration.group(0).lower():
            content_end = content_start
        return content_start, content_end
    content_end = next_declaration
    section_heading = re.match(r"^[ \t]{0,3}(#{1,6})[ \t]+", masked[declaration.start() :])
    heading_level = len(section_heading.group(1)) if section_heading else 6
    heading_end = re.search(
        rf"^[ \t]{{0,3}}#{{1,{heading_level}}}[ \t]+",
        masked[content_start:content_end],
        re.MULTILINE,
    )
    return content_start, content_start + heading_end.start() if heading_end else content_end


def _mask_spans(text: str, spans: tuple[tuple[int, int], ...]) -> str:
    """Blank text spans while preserving line boundaries and offsets."""
    characters = list(text)
    for start, end in spans:
        for index in range(start, end):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters)


def _finding_is_explicitly_resolved(block: str, path: str, line: int | None) -> bool:
    """Check the finding's own text, excluding independent legacy entries."""
    independent_spans = _independent_legacy_spans(
        block,
        structured_path=path,
        structured_line=line,
    )
    text = _mask_spans(_format._mask_fenced_blocks(block), independent_spans)
    return bool(_format._EXPLICITLY_RESOLVED_RE.search(_format._mask_inline_code(text)))


def _legacy_suppressed_block_candidates(
    body: str,
    masked: str,
    source_order: bool,
) -> list[tuple[int, str, int, int | None]]:
    candidates: list[tuple[int, str, int, int | None]] = []
    for legacy in _format._LEGACY_SUPPRESSED_BLOCK_RE.finditer(masked):
        summary = legacy.group(1)
        count_match = re.search(r"\((\d+)\)", summary)
        if count_match and int(count_match.group(1)) == 0:
            continue
        declared_count = int(count_match.group(1)) if count_match else None
        start, end = legacy.span(2)
        raw_content = body[start:end]
        content = raw_content.strip()
        if not content:
            continue
        content_start = start + len(raw_content) - len(raw_content.lstrip())
        candidate = (legacy.start(), content, content_start, declared_count)
        if not source_order:
            return [candidate]
        candidates.append(candidate)
    return candidates


def _anchored_suppressed_block_candidates(
    body: str,
    masked: str,
    source_order: bool,
) -> list[tuple[int, str, int, int | None]]:
    candidates: list[tuple[int, str, int, int | None]] = []
    for anchor in _format._SUPPRESSED_ANCHOR_RE.finditer(masked):
        declared_count = int(anchor.group(1) or anchor.group(2))
        if declared_count == 0:
            continue
        newline = masked.find("\n", anchor.end())
        if newline == -1:
            continue
        end_match = _format._SUPPRESSED_BLOCK_END_RE.search(masked, newline + 1)
        end = end_match.start() if end_match else len(body)
        raw_content = body[newline + 1 : end]
        content = raw_content.strip()
        if not content:
            continue
        content_start = newline + 1 + len(raw_content) - len(raw_content.lstrip())
        candidate = (anchor.start(), content, content_start, declared_count)
        if not source_order:
            return [candidate]
        candidates.append(candidate)
    return candidates


def _find_suppressed_block_with_offset(
    body: str,
    *,
    source_order: bool = False,
) -> tuple[str, int, int | None] | None:
    masked = _format._mask_inline_code(_format._mask_fenced_blocks(body))
    candidates = _legacy_suppressed_block_candidates(body, masked, source_order)
    if candidates and not source_order:
        _, content, content_start, declared_count = candidates[0]
        return content, content_start, declared_count
    candidates.extend(_anchored_suppressed_block_candidates(body, masked, source_order))
    if not candidates:
        return None
    if not source_order:
        _, content, content_start, declared_count = candidates[0]
        return content, content_start, declared_count
    _offset, content, content_start, declared_count = min(candidates, key=lambda candidate: candidate[0])
    return content, content_start, declared_count


def _find_suppressed_block(body: str, *, source_order: bool = False) -> str | None:
    result = _find_suppressed_block_with_offset(body, source_order=source_order)
    return result[0] if result is not None else None


def _suppressed_entry_headers(masked_block: str) -> dict[int, tuple[str, int, bool]]:
    starts: dict[int, tuple[str, int, bool]] = {}
    for match in _format._ENTRY_HEADER_INLINE_RE.finditer(masked_block):
        starts.setdefault(
            match.start(),
            (
                match.group(1).strip(),
                match.end(),
                _format._is_inline_code_header(masked_block, match),
            ),
        )
    for match in _format._ENTRY_HEADER_ONLY_RE.finditer(masked_block):
        if _format._is_explanatory_standalone_location(masked_block, match):
            continue
        starts.setdefault(
            match.start(),
            (
                match.group(1).strip(),
                match.end(),
                _format._is_inline_code_header(masked_block, match),
            ),
        )
    return starts


def _suppressed_entry_boundaries(
    inline_masked_block: str,
    masked_block: str,
    block: str,
    declared_count: int | None,
) -> dict[int, int]:
    legacy_header_offsets = {
        match.start()
        for pattern in (_format._ENTRY_HEADER_INLINE_RE, _format._ENTRY_HEADER_ONLY_RE)
        for match in pattern.finditer(masked_block)
        if not _format._FILE_FIELD_START_RE.match(match.group(0))
        and not _format._is_explanatory_standalone_location(masked_block, match)
    }
    structured_starts = {
        match.start()
        for match in _format._finding_start_matches(
            inline_masked_block,
            metadata_text=masked_block,
            content_text=block,
            legacy_header_offsets=legacy_header_offsets,
            declared_count=declared_count,
        )
    }
    boundaries = sorted(set(_suppressed_entry_headers(masked_block)) | structured_starts)
    return dict(zip(boundaries, [*boundaries[1:], len(block)]))


def _suppressed_entry_body(block: str, header_end: int, next_offset: int) -> str:
    text = block[header_end:next_offset].strip()
    return text[2:].strip() if text[:2] in ("* ", "- ") else text


def _fallback_suppressed_entries(block: str, masked_block: str) -> list[tuple[str, str]]:
    return [
        (_format.UNKNOWN_FILE, original_line.strip())
        for original_line, masked_line in zip(block.split("\n"), masked_block.split("\n"), strict=False)
        if masked_line.strip()
    ]


def extract_suppressed_comment_entries(
    body: str,
    *,
    source_order: bool = False,
    declared_count: int | None = None,
) -> list[tuple[str, str]]:
    """Extract ``(path, body)`` pairs from a recovered suppressed block."""
    if not body:
        return []
    located = _find_suppressed_block_with_offset(body, source_order=source_order)
    if not located:
        return []
    block, _offset, selected_count = located
    declared_count = declared_count if declared_count is not None else selected_count
    masked_block = _format._mask_fenced_blocks(block)
    inline_masked_block = _format._mask_inline_code(masked_block)
    starts = _suppressed_entry_headers(masked_block)
    ordered = sorted(starts.items())
    boundary_ends = _suppressed_entry_boundaries(
        inline_masked_block,
        masked_block,
        block,
        declared_count,
    )
    entries: list[tuple[str, str]] = []
    for offset, (path, header_end, is_inline_code) in ordered:
        text = _suppressed_entry_body(block, header_end, boundary_ends[offset])
        if not text:
            continue
        if not is_inline_code:
            path = _format._unescape_markdown_path(path)
        entries.append((path or _format.UNKNOWN_FILE, text))
    return entries or _fallback_suppressed_entries(block, masked_block)


def _find_missed_section_starts(
    content: str,
    section: str,
    declared_count: int | None,
    ambiguous_path_aliases: set[int] | None,
) -> tuple[list[int], dict[int, re.Match[str]]]:
    fence_masked = _format._mask_fenced_blocks(content)
    masked = _format._mask_inline_code(fence_masked)
    legacy_headers = (
        {
            match.start(): match
            for pattern in (_format._ENTRY_HEADER_INLINE_RE, _format._ENTRY_HEADER_ONLY_RE)
            for match in pattern.finditer(fence_masked)
            if not _format._FILE_FIELD_START_RE.match(match.group(0))
            and not _format._is_explanatory_standalone_location(fence_masked, match)
        }
        if section == "suppressed"
        else {}
    )
    starts = [
        match.start()
        for match in _format._finding_start_matches(
            masked,
            metadata_text=fence_masked,
            content_text=content,
            legacy_header_offsets=set(legacy_headers),
            declared_count=declared_count or None,
            ambiguous_path_aliases=ambiguous_path_aliases,
        )
    ]
    if section == "previously_missed":
        explanation_offsets = {match.start() for match in _EXPLANATION_HEADING_RE.finditer(masked)}
        legacy_entries = {match.start(): match for match in _LEGACY_SEVERITY_ENTRY_RE.finditer(fence_masked)}
        entry_offsets = (set(starts) - explanation_offsets) | set(legacy_entries)
        first_entry = min(entry_offsets, default=len(content))
        starts = sorted(entry_offsets | {offset for offset in explanation_offsets if offset < first_entry})
    for offset in _format._FILE_FIELD_START_RE.finditer(masked):
        previous_start = max((start for start in starts if start <= offset.start()), default=None)
        if previous_start is None or _format._FILE_FIELD_START_RE.search(masked[previous_start : offset.start()]):
            starts.append(offset.start())
    return sorted(set(starts)), legacy_headers


def _missed_section_block_bounds(
    content: str,
    starts: list[int],
    index: int,
    section: str,
    legacy_header_matches: dict[int, re.Match[str]],
) -> tuple[int, int]:
    start = starts[index]
    end = starts[index + 1] if index + 1 < len(starts) else len(content)
    if section != "suppressed":
        return start, end
    previous_start = starts[index - 1] if index else -1
    preceding_header = max(
        (offset for offset in legacy_header_matches if previous_start < offset < start),
        default=None,
    )
    if preceding_header is None:
        return start, end
    header_match = legacy_header_matches[preceding_header]
    if content[header_match.end() : start].strip():
        return start, end
    next_header = min((offset for offset in legacy_header_matches if offset > preceding_header), default=end)
    return preceding_header, min(end, next_header)


def _missed_finding_title(block: str) -> tuple[str, str]:
    block_lines = [line.strip() for line in block.splitlines() if line.strip()]
    first_line = block_lines[0]
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match(first_line)
    if legacy_entry:
        return legacy_entry.group("title").strip(), legacy_entry.group("severity").upper()
    if (
        _format._FILE_LOCATION_RE.match(first_line)
        or _format._STANDALONE_FILE_LOCATION_RE.match(first_line)
        or _format._LINE_LOCATION_RE.match(first_line)
    ):
        first_line = next(
            (
                line
                for line in block_lines[1:]
                if not _format._FILE_LOCATION_RE.match(line)
                and not _format._STANDALONE_FILE_LOCATION_RE.match(line)
                and not _format._LINE_LOCATION_RE.match(line)
            ),
            first_line,
        )
    picture_match = re.search(r"<picture\b.*?</picture>", first_line, re.IGNORECASE)
    picture_alt = (
        re.search(r"\balt=[\"']([^\"']+)[\"']", picture_match.group(0), re.IGNORECASE) if picture_match else None
    )
    picture_severity = _format._SEVERITY_RE.search(picture_alt.group(1)) if picture_alt else None
    first_line = re.sub(r"<picture\b.*?</picture>", "", first_line, flags=re.IGNORECASE)
    first_line = re.sub(r"</?summary>", "", first_line, flags=re.IGNORECASE).strip()
    title = first_line.lstrip("#*- ").strip()
    title = re.sub(r"^\*\*|\*\*$", "", title).strip()
    severity_prefix = _format._SEVERITY_PREFIX_RE.match(title)
    severity_match = picture_severity or severity_prefix
    severity = next(group for group in severity_match.groups() if group).upper() if severity_match else ""
    if severity_prefix:
        title = title[severity_prefix.end() :].lstrip(" \t:*-")
    return title, severity


def _missed_finding_location(block: str) -> tuple[str, int | None]:
    metadata_block = _format._mask_fenced_blocks(block)
    legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match(metadata_block)
    if legacy_entry:
        return _legacy_severity_location(legacy_entry)
    location_match = _format._FILE_LOCATION_RE.search(metadata_block)
    if location_match is None:
        location_match = _format._STANDALONE_FILE_LOCATION_RE.search(metadata_block)
    path = _format.UNKNOWN_FILE
    line_number: int | None = None
    if location_match:
        is_inline_code = location_match.group(1) is not None
        path = (location_match.group(1) or location_match.group(2) or "").strip()
        suffix = re.fullmatch(r"(.+?):(\d+)", path)
        if suffix:
            path = suffix.group(1)
            line_number = int(suffix.group(2))
        else:
            line_match = _format._LINE_LOCATION_RE.search(metadata_block)
            if line_match:
                line_number = int(line_match.group(1))
        if not is_inline_code:
            path = _format._unescape_markdown_path(path)
    return path, line_number


def _missed_finding(
    block: str,
    section: str,
    ordinal: int,
    source_review_id: int,
    source_review_url: str,
) -> _format.CCRFinding:
    title, severity = _missed_finding_title(block)
    path, line_number = _missed_finding_location(block)
    return _format.CCRFinding(
        section=section,
        ordinal=ordinal,
        severity=severity,
        title=title or path,
        body=block,
        path=path,
        line=line_number,
        source_review_id=source_review_id,
        source_review_url=source_review_url,
        explicitly_resolved=_finding_is_explicitly_resolved(block, path, line_number),
    )


def _parse_missed_section_entries(
    content: str,
    section: str,
    *,
    declared_count: int | None = None,
    source_review_id: int,
    source_review_url: str,
    ambiguous_path_aliases: set[int] | None = None,
) -> list[tuple[int, _format.CCRFinding]]:
    """Parse finding blocks from a missed/suppressed section without interpreting code."""
    starts, legacy_header_matches = _find_missed_section_starts(
        content,
        section,
        declared_count,
        ambiguous_path_aliases,
    )
    if not starts:
        return []

    findings: list[tuple[int, _format.CCRFinding]] = []
    deferred_alias_duplicates: list[tuple[int, int]] = []
    for index, start in enumerate(starts):
        block_start, end = _missed_section_block_bounds(
            content,
            starts,
            index,
            section,
            legacy_header_matches,
        )
        block = content[block_start:end].strip()
        finding = _missed_finding(
            block,
            section,
            len(findings) + 1,
            source_review_id,
            source_review_url,
        )
        legacy_entry = _LEGACY_SEVERITY_ENTRY_RE.match(block)
        if section == "previously_missed" and findings and legacy_entry:
            previous_offset, previous = findings[-1]
            if _is_duplicate_picture_legacy_entry(previous, legacy_entry, block[legacy_entry.end() :]):
                legacy_path, _legacy_line = _legacy_severity_location(legacy_entry)
                if legacy_path == previous.path:
                    findings[-1] = (
                        previous_offset,
                        replace(
                            previous,
                            explicitly_resolved=previous.explicitly_resolved or finding.explicitly_resolved,
                        ),
                    )
                    continue
                deferred_alias_duplicates.append((len(findings), len(findings) - 1))
        findings.append((block_start, finding))
    if deferred_alias_duplicates:
        distinct_count = len(findings) - len(deferred_alias_duplicates)
        aliases_to_keep = (
            min(max(declared_count - distinct_count, 0), len(deferred_alias_duplicates))
            if declared_count is not None
            else 0
        )
        kept_alias_indexes = {index for index, _duplicate_index in deferred_alias_duplicates[:aliases_to_keep]}
        for finding_index, duplicate_index in reversed(deferred_alias_duplicates):
            if finding_index in kept_alias_indexes:
                continue
            candidate = findings[finding_index][1]
            duplicate_offset, duplicate = findings[duplicate_index]
            findings[duplicate_index] = (
                duplicate_offset,
                replace(
                    duplicate,
                    explicitly_resolved=duplicate.explicitly_resolved or candidate.explicitly_resolved,
                ),
            )
            del findings[finding_index]
        findings = [
            (offset, finding if finding.ordinal == ordinal else replace(finding, ordinal=ordinal))
            for ordinal, (offset, finding) in enumerate(findings, start=1)
        ]
    return findings
