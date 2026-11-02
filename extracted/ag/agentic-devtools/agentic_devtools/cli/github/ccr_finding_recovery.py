"""Finding-recovery orchestration for CCR review bodies.

Section helpers are re-exported from this module and then through ccr_review_format to preserve its parser API.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

import agentic_devtools.cli.github.ccr_review_format as _format
from agentic_devtools.cli.github.ccr_finding_missed_entries import (
    _SEVERITY_NAME_TO_LEVEL,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _declaration_content_bounds as _declaration_content_bounds,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _find_suppressed_block as _find_suppressed_block,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _find_suppressed_block_with_offset as _find_suppressed_block_with_offset,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _finding_is_explicitly_resolved as _finding_is_explicitly_resolved,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _independent_legacy_spans as _independent_legacy_spans,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _mask_spans as _mask_spans,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _parse_missed_section_entries as _parse_missed_section_entries,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _suppressed_entry_boundaries as _suppressed_entry_boundaries,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    _suppressed_entry_headers as _suppressed_entry_headers,
)
from agentic_devtools.cli.github.ccr_finding_recovery_sections import (
    extract_suppressed_comment_entries as extract_suppressed_comment_entries,
)


@dataclass
class _FindingRecoveryState:
    body: str
    source_review_id: int
    source_review_url: str
    findings_with_offset: list[tuple[int, _format.CCRFinding]] = field(default_factory=list)
    shortfalls: list[tuple[str, int, int]] = field(default_factory=list)
    suppressed_declarations: list[list[int]] = field(default_factory=list)
    low_confidence_declarations: list[tuple[int, int]] = field(default_factory=list)
    parsed_any_suppressed: bool = False
    deferred_duplicate_candidates: dict[int, list[tuple[int, _format.CCRFinding, int]]] = field(default_factory=dict)
    search_start: int = 0
    deduplicated_finding_indexes: set[int] = field(default_factory=set)


@dataclass
class _SuppressedBlock:
    block: str
    block_offset: int
    declared_count: int | None
    structured_spans: tuple[tuple[int, int], ...]
    parsed_entries: list[tuple[str, str]]
    masked_block: str
    ordered_headers: list[tuple[int, tuple[str, int, bool]]]
    boundary_ends: dict[int, int]
    legacy_occurrences: tuple[tuple[int, int], ...]
    matched_header_offsets: set[int] = field(default_factory=set)
    fallback_offsets: set[int] = field(default_factory=set)


@dataclass
class _LegacyEntry:
    offset: int
    occurrence: str
    body: str
    candidate_body: str
    finding_occurrences: tuple[tuple[int, int], ...]


@dataclass
class _LegacyFindingDetails:
    path: str
    line: int | None
    title: str
    severity: str
    comparison_content: tuple[tuple[str, str], ...]
    has_suppressed_declaration: bool
    unrecovered_declaration_index: int | None


def _collect_declared_findings(state: _FindingRecoveryState, declarations: list[re.Match[str]], masked: str) -> None:
    for index, declaration in enumerate(declarations):
        declared = int(next(count for count in declaration.groups() if count is not None))
        header = declaration.group(0).lower()
        section = "previously_missed" if "previously" in header else "suppressed"
        content_start, content_end = _declaration_content_bounds(state.body, masked, declarations, index)
        raw_content = state.body[content_start:content_end]
        ambiguous_path_aliases: set[int] = set()
        entries = _parse_missed_section_entries(
            raw_content,
            section,
            declared_count=declared,
            source_review_id=state.source_review_id,
            source_review_url=state.source_review_url,
            ambiguous_path_aliases=ambiguous_path_aliases,
        )
        recovered = len(entries)
        safely_recovered = max(recovered - len(ambiguous_path_aliases), 0)
        if declared != safely_recovered:
            state.shortfalls.append((section, declared, safely_recovered))
        if section == "suppressed":
            state.suppressed_declarations.append([content_start, content_end, declared, safely_recovered])
            if "low confidence" in header and "suppressed" not in header:
                state.low_confidence_declarations.append((content_start, content_end))
        state.findings_with_offset.extend((content_start + offset, entry) for offset, entry in entries)


def _prepare_suppressed_block(
    state: _FindingRecoveryState,
    block: str,
    block_offset: int,
    declared_count: int | None,
) -> _SuppressedBlock | None:
    uncounted_entries: list[tuple[int, _format.CCRFinding]] = []
    if declared_count is None:
        # Counted blocks use the count-aware parser; spans here constrain uncounted fallbacks.
        uncounted_entries = _parse_missed_section_entries(
            block,
            "suppressed",
            declared_count=None,
            source_review_id=state.source_review_id,
            source_review_url=state.source_review_url,
        )
        state.findings_with_offset.extend((block_offset + offset, entry) for offset, entry in uncounted_entries)
    structured_offsets = [offset for offset, _entry in uncounted_entries]
    # Preserve base behavior: the final structured span owns the remainder of the block.
    structured_spans = tuple(
        (start, structured_offsets[index + 1] if index + 1 < len(structured_offsets) else len(block))
        for index, start in enumerate(structured_offsets)
    )
    parsed_entries = _format.extract_suppressed_comment_entries(
        state.body[state.search_start :],
        source_order=True,
        declared_count=declared_count,
    )
    if not parsed_entries:
        return None
    masked_block = _format._mask_fenced_blocks(block)
    headers = _suppressed_entry_headers(masked_block)
    ordered_headers = sorted(headers.items())
    boundary_ends = _suppressed_entry_boundaries(
        _format._mask_inline_code(masked_block),
        masked_block,
        block,
        declared_count,
    )
    legacy_occurrences = tuple(
        (block_offset + offset, block_offset + boundary_ends[offset]) for offset, _header in ordered_headers
    )
    return _SuppressedBlock(
        block,
        block_offset,
        declared_count,
        structured_spans,
        parsed_entries,
        masked_block,
        ordered_headers,
        boundary_ends,
        legacy_occurrences,
    )


def _is_low_confidence_fallback(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    path: str,
) -> bool:
    return (
        not block.ordered_headers
        and path == _format.UNKNOWN_FILE
        and any(start <= block.block_offset < end for start, end in state.low_confidence_declarations)
    )


def _match_suppressed_header(
    block: _SuppressedBlock,
    path: str,
    entry_body: str,
) -> _LegacyEntry | None:
    for header_offset, (header_path, header_end, is_inline_code) in block.ordered_headers:
        if header_offset in block.matched_header_offsets:
            continue
        next_offset = block.boundary_ends[header_offset]
        original_body = block.block[header_end:next_offset]
        candidate_body = original_body.strip()
        if candidate_body[:2] in ("* ", "- "):
            candidate_body = candidate_body[2:].strip()
        if not is_inline_code:
            header_path = _format._unescape_markdown_path(header_path)
        if _format.ccr_path_match_key(header_path) != _format.ccr_path_match_key(path) or candidate_body != entry_body:
            continue
        legacy_body = re.sub(r"^(?:[ \t]*\r?\n)+|(?:\r?\n[ \t]*)+$", "", original_body)
        legacy_bullet = re.match(r"^[ \t]{0,3}[*-] ", legacy_body)
        if legacy_bullet:
            legacy_body = legacy_body[legacy_bullet.end() :]
        block.matched_header_offsets.add(header_offset)
        return _LegacyEntry(
            header_offset,
            block.block[header_offset:next_offset].strip(),
            legacy_body,
            original_body,
            block.legacy_occurrences,
        )
    return None


def _match_headerless_suppressed_entry(
    block: _SuppressedBlock,
    path: str,
    entry_body: str,
) -> _LegacyEntry | None:
    if block.ordered_headers or path != _format.UNKNOWN_FILE:
        return None
    offset = 0
    for original_line, masked_line in zip(
        block.block.splitlines(keepends=True),
        block.masked_block.splitlines(keepends=True),
        strict=False,
    ):
        structured = any(start <= offset < end for start, end in block.structured_spans)
        if (
            masked_line.strip()
            and original_line.strip() == entry_body
            and offset not in block.fallback_offsets
            and not structured
        ):
            block.fallback_offsets.add(offset)
            occurrence = original_line.rstrip("\r\n")
            return _LegacyEntry(
                offset,
                occurrence,
                occurrence,
                original_line,
                ((block.block_offset + offset, block.block_offset + offset + len(original_line)),),
            )
        offset += len(original_line)
    return None


def _legacy_finding_details(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    entry: _LegacyEntry,
    path: str,
    entry_body: str,
) -> _LegacyFindingDetails:
    line_match = re.search(r":(\d+)$", path)
    source_path = path[: line_match.start()] if line_match else path
    line = int(line_match.group(1)) if line_match else None
    title = entry_body.splitlines()[0]
    severity_prefix = _format._SEVERITY_PREFIX_RE.match(title)
    blank_separated_bullet = bool(re.match(r"^[ \t]*\r?\n[ \t]*\r?\n[ \t]*[*-][ \t]+", entry.candidate_body))
    severity = next(group for group in severity_prefix.groups() if group).upper() if severity_prefix else ""
    if severity_prefix and blank_separated_bullet:
        title = title[severity_prefix.end() :].lstrip(" \t:*-")
    comparison_body = entry.body
    if severity_prefix:
        comparison_body = comparison_body[severity_prefix.end() :].lstrip(" \t:*-")
    absolute_offset = block.block_offset + entry.offset
    suppressed_declaration = any(
        start <= absolute_offset < end for start, end, _declared, _recovered in state.suppressed_declarations
    )
    unrecovered_index = next(
        (
            index
            for index, (start, end, declared, recovered) in enumerate(state.suppressed_declarations)
            if start <= absolute_offset < end and recovered < declared
        ),
        None,
    )
    return _LegacyFindingDetails(
        source_path,
        line,
        title,
        severity,
        _format._finding_content_key(comparison_body),
        suppressed_declaration,
        unrecovered_index,
    )


def _duplicate_finding_matches(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    entry: _LegacyEntry,
    details: _LegacyFindingDetails,
    index: int,
    finding_offset: int,
    finding: _format.CCRFinding,
) -> bool:
    if (
        index in state.deduplicated_finding_indexes
        or finding.section != "suppressed"
        or finding.ordinal <= 0
        or _format.ccr_path_match_key(finding.path) != _format.ccr_path_match_key(details.path)
        or (finding.line is not None and details.line is not None and finding.line != details.line)
        or (
            finding.severity
            and details.severity
            and _SEVERITY_NAME_TO_LEVEL.get(finding.severity.upper(), finding.severity.upper())
            != _SEVERITY_NAME_TO_LEVEL.get(details.severity, details.severity)
        )
    ):
        return False
    content_key = _format._finding_content_key(
        finding.body,
        entry.finding_occurrences,
        state.body.index(finding.body, finding_offset),
    )
    same_content = content_key == details.comparison_content or (
        not any(value for _kind, value in content_key) and entry.occurrence in finding.body
    )
    if not same_content:
        return False
    next_offset = min(
        (
            candidate_offset
            for candidate_offset, candidate in state.findings_with_offset
            if candidate_offset > finding_offset and candidate.section == "suppressed" and candidate.ordinal > 0
        ),
        default=block.block_offset + len(block.block),
    )
    absolute_entry_offset = block.block_offset + entry.offset
    return (
        block.block_offset <= finding_offset < block.block_offset + len(block.block)
        and absolute_entry_offset >= finding_offset
        and absolute_entry_offset < next_offset
    )


def _find_duplicate_finding_index(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    entry: _LegacyEntry,
    details: _LegacyFindingDetails,
) -> int | None:
    for index, (finding_offset, finding) in enumerate(state.findings_with_offset):
        if _duplicate_finding_matches(state, block, entry, details, index, finding_offset, finding):
            return index
    return None


def _append_legacy_finding(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    entry: _LegacyEntry,
    entry_body: str,
    details: _LegacyFindingDetails,
    duplicate_index: int | None,
) -> None:
    finding = _format.CCRFinding(
        section="suppressed",
        ordinal=0,
        severity=details.severity,
        title=details.title[:160],
        body=entry_body,
        path=details.path,
        line=details.line,
        source_review_id=state.source_review_id,
        source_review_url=state.source_review_url,
        explicitly_resolved=bool(
            _format._EXPLICITLY_RESOLVED_RE.search(_format._mask_inline_code(_format._mask_fenced_blocks(entry_body)))
        ),
    )
    if duplicate_index is not None and (
        state.findings_with_offset[duplicate_index][1].path == details.path
        or (details.has_suppressed_declaration and details.unrecovered_declaration_index is None)
    ):
        findings = state.findings_with_offset
        duplicate_offset, duplicate = findings[duplicate_index]
        if finding.explicitly_resolved and not duplicate.explicitly_resolved:
            findings[duplicate_index] = duplicate_offset, replace(duplicate, explicitly_resolved=True)
        state.deduplicated_finding_indexes.add(duplicate_index)
        return
    absolute_offset = block.block_offset + entry.offset
    state.findings_with_offset.append((absolute_offset, finding))
    if duplicate_index is not None and details.unrecovered_declaration_index is not None:
        state.deduplicated_finding_indexes.add(duplicate_index)
        state.deferred_duplicate_candidates.setdefault(details.unrecovered_declaration_index, []).append(
            (absolute_offset, finding, state.findings_with_offset[duplicate_index][0])
        )
    for declaration in state.suppressed_declarations:
        if declaration[0] <= absolute_offset < declaration[1]:
            declaration[3] += 1
            break


def _process_suppressed_entry(
    state: _FindingRecoveryState,
    block: _SuppressedBlock,
    path: str,
    entry_body: str,
) -> None:
    if _is_low_confidence_fallback(state, block, path):
        return
    legacy_entry = _match_suppressed_header(block, path, entry_body)
    if legacy_entry is None:
        legacy_entry = _match_headerless_suppressed_entry(block, path, entry_body)
    if legacy_entry is None:
        return
    details = _legacy_finding_details(state, block, legacy_entry, path, entry_body)
    duplicate_index = _find_duplicate_finding_index(state, block, legacy_entry, details)
    _append_legacy_finding(state, block, legacy_entry, entry_body, details, duplicate_index)


def _collect_legacy_suppressed_findings(state: _FindingRecoveryState) -> None:
    state.search_start = 0
    while state.search_start < len(state.body):
        remaining = state.body[state.search_start :]
        located = _format._find_suppressed_block_with_offset(remaining, source_order=True)
        if not located:
            break
        block, relative_offset, declared = located
        block_offset = state.search_start + relative_offset
        context = _prepare_suppressed_block(state, block, block_offset, declared)
        if context is None:
            break
        state.parsed_any_suppressed = True
        for path, entry_body in context.parsed_entries:
            _process_suppressed_entry(state, context, path, entry_body)
        state.search_start = block_offset + len(block)


def _finalize_deferred_duplicates(state: _FindingRecoveryState) -> None:
    findings = state.findings_with_offset
    for declaration_index, candidates in state.deferred_duplicate_candidates.items():
        declaration = state.suppressed_declarations[declaration_index]
        excess = declaration[3] - declaration[2]
        for candidate_offset, candidate, duplicate_offset in candidates[: max(excess, 0)]:
            findings.remove((candidate_offset, candidate))
            duplicate_index, duplicate = next(
                (index, finding) for index, (offset, finding) in enumerate(findings) if offset == duplicate_offset
            )
            if candidate.explicitly_resolved and not duplicate.explicitly_resolved:
                findings[duplicate_index] = duplicate_offset, replace(duplicate, explicitly_resolved=True)
            declaration[3] -= 1


def _finalize_recovery(state: _FindingRecoveryState) -> _format.CCRFindingRecovery:
    _finalize_deferred_duplicates(state)
    if state.parsed_any_suppressed and state.suppressed_declarations:
        state.shortfalls = [shortfall for shortfall in state.shortfalls if shortfall[0] != "suppressed"]
        state.shortfalls.extend(
            ("suppressed", declared, recovered)
            for _start, _end, declared, recovered in state.suppressed_declarations
            if declared != recovered
        )
    state.findings_with_offset.sort(key=lambda pair: pair[0])
    ordinals: dict[str, int] = {}
    findings: list[_format.CCRFinding] = []
    for _offset, finding in state.findings_with_offset:
        ordinals[finding.section] = ordinals.get(finding.section, 0) + 1
        findings.append(
            _format.CCRFinding(
                section=finding.section,
                ordinal=ordinals[finding.section],
                severity=finding.severity,
                title=finding.title,
                body=finding.body,
                path=finding.path,
                line=finding.line,
                source_review_id=finding.source_review_id,
                source_review_url=finding.source_review_url,
                explicitly_resolved=finding.explicitly_resolved,
            )
        )
    return _format.CCRFindingRecovery(findings=tuple(findings), shortfalls=tuple(state.shortfalls))


def extract_ccr_findings(
    body: str,
    *,
    source_review_id: int = 0,
    source_review_url: str = "",
) -> _format.CCRFindingRecovery:
    """Recover missed and suppressed finding occurrences in body order."""
    if not body:
        return _format.CCRFindingRecovery(findings=())
    state = _FindingRecoveryState(body, source_review_id, source_review_url)
    masked = _format._mask_inline_code(_format._mask_fenced_blocks(body))
    declarations = list(_format._CCR_SECTION_DECLARATION_RE.finditer(masked))
    _collect_declared_findings(state, declarations, masked)
    _collect_legacy_suppressed_findings(state)
    return _finalize_recovery(state)
