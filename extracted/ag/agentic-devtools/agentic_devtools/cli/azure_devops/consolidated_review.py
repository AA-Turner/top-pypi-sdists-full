"""Consolidated PR review comment renderer.

Renders an agentic-devtools review state into the markdown comment(s) for **one
reviewed commit** — a root comment plus zero or more continuation reply comments
— using a status headline and top-level ``<details>/<summary>`` sections. There
is **one top-level review thread per reviewed commit** (not one per PR); prior
commits are summarized as a hash + link index, not embedded in full.

While a commit's review is **in progress** (not all files reviewed yet) only a
lightweight status headline is rendered, so each file submission patches a tiny
comment instead of re-rendering the whole review. Once the review is
**complete** (every file terminal), the full content is rendered.

Code suggestions are still posted as separate line-anchored threads (for line
context and the native Apply/reply UX), but each suggestion is **also embedded**
in this comment with its thread link and full content, so the entire review —
including suggestions — can be reconstructed from this commit's thread.

Structure (top to bottom, once complete):

  - Headline (status + stats + ``v2`` consolidated marker, including commit SHA)
  - Overview section: overall Progress & Models, rebase / skipped notes
  - Status sections: one heading per status group, then one top-level
    ``<details>`` per file (status, summary, per-file Progress, suggestions)
  - Review Narrative
  - **Previous reviews** index: a bulleted list of prior reviewed commits, each
    a short hash + status/model + a link jumping to that commit's thread — no
    embedded prior content
  - Activity Log

Size is governed by a simple **smart cutoff**. A single comment is filled with
whole top-level sections until its running length first exceeds
:data:`SMART_CUTOFF_CHARS`; the section that crossed the threshold is allowed to
complete, and any remaining sections roll over into one or more **continuation**
reply comments (each carrying a ``type:continuation`` marker with the commit SHA
and a 1-based sequence). There is no content-dropping budget degradation and no
hard truncation — the full review is always preserved across the root comment
plus its continuations.

No backwards compatibility: this renderer emits the ``v2`` format only.
Previous-version (``v1``) per-file / activity-log comments are ignored by the
consuming logic and are never read or migrated here.
"""

from __future__ import annotations

from .review_attribution import get_model_icon
from .review_state import (
    FileEntry,
    ReviewState,
    ReviewStatus,
    SuggestionEntry,
    compute_aggregate_status,
)
from .review_templates import (
    _SEVERITY_LABELS,
    _SEVERITY_ORDER,
    _STATUS_EMOJI,
    _VERDICT_DISPLAY,
    build_discussion_url,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Smart-cutoff threshold (characters). A review comment is filled with whole
#: top-level sections until its running length first exceeds this value; the
#: crossing section completes and the remaining sections roll over into
#: continuation reply comments. Chosen below GitHub's 65,536 hard limit (Azure
#: DevOps allows 150,000) so the root comment stays comfortably within range
#: while keeping each section intact.
SMART_CUTOFF_CHARS = 50000

#: Hard character cap per comment. This intentionally stays a few thousand
#: characters below GitHub's 65,536-character hard limit so the rendered root
#: headline / markers and continuation headers still fit even when a section is
#: chunked right up to this cap.
HARD_CAP_CHARS = 62000

#: Maximum number of Activity Log entries rendered (newest-first); older
#: sessions are summarized as a single count line so the log cannot grow
#: unbounded on long-lived PRs.
_ACTIVITY_LOG_MAX_ENTRIES = 15

#: Marker version for the consolidated (single-comment) review format. This is
#: intentionally distinct from the legacy ``v1`` per-thread markers; the
#: consolidated logic ignores ``v1`` comments entirely (no backwards compat).
CONSOLIDATED_MARKER_VERSION = 2

#: Marker type for the single consolidated review comment (the root comment of a
#: commit's review thread).
CONSOLIDATED_MARKER_TYPE = "consolidated"

#: Marker type for a continuation reply comment holding roll-over content.
CONTINUATION_MARKER_TYPE = "continuation"

#: Marker type for an additional-model review reply within a commit thread.
MODEL_REPLY_MARKER_TYPE = "model-review"


def build_consolidated_marker(pr_id: int, commit_hash: str | None) -> str:
    """Build the ``v2`` consolidated-review marker for the root comment.

    The marker embeds the reviewed commit SHA so the entire review — including
    which commit it targets — can be recovered from this one comment, even if
    all local state is lost.

    Args:
        pr_id: Pull request ID.
        commit_hash: Full reviewed commit SHA (``None`` → omitted).

    Returns:
        An HTML-comment marker string, e.g.
        ``<!-- agdt-review:v2 type:consolidated pr:42 commit:abc123... -->``.
    """
    parts = [f"type:{CONSOLIDATED_MARKER_TYPE}", f"pr:{pr_id}"]
    if commit_hash:
        parts.append(f"commit:{commit_hash}")
    payload = " ".join(parts)
    return f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} {payload} -->"


def build_continuation_marker(pr_id: int, commit_hash: str | None, sequence: int) -> str:
    """Build a ``v2`` continuation marker for a roll-over reply comment.

    Args:
        pr_id: Pull request ID.
        commit_hash: Full reviewed commit SHA (``None`` → omitted).
        sequence: 1-based continuation sequence number.

    Returns:
        An HTML-comment marker string, e.g.
        ``<!-- agdt-review:v2 type:continuation pr:42 commit:abc seq:1 -->``.
    """
    parts = [f"type:{CONTINUATION_MARKER_TYPE}", f"pr:{pr_id}"]
    if commit_hash:
        parts.append(f"commit:{commit_hash}")
    parts.append(f"seq:{sequence}")
    payload = " ".join(parts)
    return f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} {payload} -->"


def is_consolidated_comment(content: str | None) -> bool:
    """Return ``True`` when *content* carries the ``v2`` consolidated marker.

    Used to identify the root consolidated review comment on a PR (e.g. for
    state recovery). Legacy ``v1`` per-thread comments never match, so the
    consolidated logic ignores them entirely (no backwards compatibility).

    Args:
        content: A comment's markdown content (may be ``None``).

    Returns:
        ``True`` if the content contains the consolidated-review marker prefix
        and the ``consolidated`` type token, else ``False``.
    """
    if not content:
        return False
    marker_prefix = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} "
    return marker_prefix in content and f"type:{CONSOLIDATED_MARKER_TYPE}" in content


def is_continuation_comment(content: str | None) -> bool:
    """Return ``True`` when *content* carries the ``v2`` continuation marker."""
    if not content:
        return False
    marker_prefix = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} "
    return marker_prefix in content and f"type:{CONTINUATION_MARKER_TYPE}" in content


def build_model_reply_marker(pr_id: int, commit_hash: str | None, model_id: str) -> str:
    """Build a ``v2`` marker for an additional-model review reply.

    A different model reviewing the *same* commit posts its review as a reply
    within that commit's thread (no ``--force-rereview`` needed). This marker
    ties the reply to the commit + model so the reply can be recovered and
    updated in place on subsequent runs of the same model.

    Args:
        pr_id: Pull request ID.
        commit_hash: Full reviewed commit SHA (``None`` → omitted).
        model_id: The reviewing model identifier.

    Returns:
        An HTML-comment marker string, e.g.
        ``<!-- agdt-review:v2 type:model-review pr:42 commit:abc model:gpt-5 -->``.
    """
    parts = [f"type:{MODEL_REPLY_MARKER_TYPE}", f"pr:{pr_id}"]
    if commit_hash:
        parts.append(f"commit:{commit_hash}")
    parts.append(f"model:{model_id}")
    payload = " ".join(parts)
    return f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} {payload} -->"


def is_model_reply_comment(content: str | None) -> bool:
    """Return ``True`` when *content* carries the ``v2`` model-review marker."""
    if not content:
        return False
    marker_prefix = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} "
    return marker_prefix in content and f"type:{MODEL_REPLY_MARKER_TYPE}" in content


def extract_commit_hash_from_marker(content: str | None) -> str | None:
    """Extract the commit SHA embedded in a ``v2`` agdt-review marker.

    Parses the ``commit:<sha>`` token from the first agdt-review marker found
    in *content*. Used when scanning PR threads to match a consolidated comment
    against a specific reviewed commit SHA.

    Args:
        content: A comment's markdown content (may be ``None``).

    Returns:
        The commit SHA string, or ``None`` if the marker is absent or contains
        no ``commit:`` field.
    """
    if not content:
        return None
    marker_prefix = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} "
    start = content.find(marker_prefix)
    if start == -1:
        return None
    close_comment = "-->"
    end = content.find(close_comment, start)
    if end == -1:
        return None
    # Include the closing "-->" so the slice represents the full marker string.
    marker_payload = content[start : end + len(close_comment)]
    commit_token = "commit:"  # nosec B105 - marker token, not a credential
    idx = marker_payload.find(commit_token)
    if idx == -1:
        return None
    sha_start = idx + len(commit_token)
    # The SHA ends at the next space (separating marker tokens) or at "-->" —
    # whichever comes first. Filter out -1 (not-found) sentinels before min().
    boundaries = [
        marker_payload.find(" ", sha_start),
        marker_payload.find(close_comment, sha_start),
    ]
    valid = [b for b in boundaries if b != -1]
    sha = marker_payload[sha_start : min(valid)].strip()
    return sha if sha else None


def extract_continuation_seq_from_marker(content: str | None) -> int | None:
    """Extract the sequence number embedded in a ``v2`` continuation marker.

    Parses the ``seq:<n>`` token from the first agdt-review marker found in
    *content*. Used when scanning PR threads to de-duplicate continuation
    comments that share the same sequence slot (which can occur when a
    cross-identity 403 on a PATCH causes a fallback reply to be posted alongside
    the original comment).

    Args:
        content: A comment's markdown content (may be ``None``).

    Returns:
        The 1-based sequence integer, or ``None`` if the marker is absent or
        contains no ``seq:`` field, or if the field value is not a valid integer.
    """
    if not content:
        return None
    marker_prefix = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} "
    start = content.find(marker_prefix)
    if start == -1:
        return None
    close_comment = "-->"
    end = content.find(close_comment, start)
    if end == -1:
        return None
    marker_payload = content[start : end + len(close_comment)]
    seq_token = "seq:"  # nosec B105 - marker token, not a credential
    idx = marker_payload.find(seq_token)
    if idx == -1:
        return None
    seq_start = idx + len(seq_token)
    boundaries = [
        marker_payload.find(" ", seq_start),
        marker_payload.find(close_comment, seq_start),
    ]
    valid = [b for b in boundaries if b != -1]
    if not valid:  # pragma: no cover — marker_payload always ends with "-->"
        return None
    seq_str = marker_payload[seq_start : min(valid)].strip()
    try:
        return int(seq_str)
    except ValueError:
        return None


#: Severity marker emoji for suggestion grouping headings.
_SEVERITY_EMOJI: dict[str, str] = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢",
}

#: Status display order for the per-commit status sections.
_SECTION_ORDER: list[tuple[str, str]] = [
    (ReviewStatus.NEEDS_WORK.value, "📝 Needs Work"),
    (ReviewStatus.APPROVED.value, "✅ Approved"),
    (ReviewStatus.IN_PROGRESS.value, "🔃 In Progress"),
    (ReviewStatus.UNREVIEWED.value, "⏳ Unreviewed"),
]


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def _short_hash(commit_hash: str | None) -> str:
    """Return the first 8 chars of a commit hash, or ``"unknown"``."""
    if not commit_hash:
        return "unknown"
    return commit_hash[:8]


def _normalize_status(status: str) -> str:
    """Map an unknown status into the ``unreviewed`` bucket."""
    known = {s.value for s in ReviewStatus}
    return status if status in known else ReviewStatus.UNREVIEWED.value


def _count_by_status(files: dict[str, FileEntry]) -> dict[str, int]:
    """Count files per (normalized) status."""
    counts: dict[str, int] = {}
    for fe in files.values():
        status = _normalize_status(fe.status)
        counts[status] = counts.get(status, 0) + 1
    return counts


def _severity_counts_label(suggestions: list[SuggestionEntry]) -> str:
    """Return a compact severity-count label, e.g. ``"1 High, 2 Medium"``.

    Suggestions with unknown severity values (not in high/medium/low) are
    counted and appended as ``"N Other"`` so files with only non-standard
    severities still surface in the severity label.
    """
    counts = {"high": 0, "medium": 0, "low": 0}
    other = 0
    for s in suggestions:
        sev = _normalized_severity_key(s.severity)
        if sev in counts:
            counts[sev] += 1
        else:
            other += 1
    parts = [f"{counts[sev]} {sev.capitalize()}" for sev in _SEVERITY_ORDER if counts[sev] > 0]
    if other > 0:
        parts.append(f"{other} Other")
    return ", ".join(parts)


def _normalized_severity_key(severity: object) -> str:
    """Normalize severity to lowercase; non-string values become empty."""
    if not isinstance(severity, str):
        return ""
    return severity.strip().lower()


# ---------------------------------------------------------------------------
# Suggestion + file rendering
# ---------------------------------------------------------------------------


def _render_suggestion(base_url: str, suggestion: SuggestionEntry) -> list[str]:
    """Render a single suggestion as a bullet plus an inner ``<details>`` block.

    The bullet links to the suggestion's line-anchored thread; the inner
    ``<details>`` embeds the full content so the review is self-describing.
    When ``replacement_code`` is set on the suggestion, it is rendered as a
    fenced ``suggestion`` block (matching what was posted to the ADO thread).
    """
    url = build_discussion_url(base_url, suggestion.threadId, suggestion.commentId)
    out_of_scope = " *(out of scope)*" if suggestion.outOfScope else ""
    # First line of content as the inline bullet label.
    content = suggestion.content or ""
    first_line = content.strip().splitlines()[0] if content.strip() else "(no detail)"
    bullet = f"- [{suggestion.linkText}]({url}){out_of_scope} — {first_line}"

    sev = _normalized_severity_key(suggestion.severity)
    sev_label = sev.capitalize() if sev else "Unknown"
    line_label = (
        f"line {suggestion.line}"
        if suggestion.endLine == suggestion.line
        else f"lines {suggestion.line}\u2013{suggestion.endLine}"
    )
    detail = [
        "  <details>",
        f"  <summary>suggestion detail \u00b7 thread #{suggestion.threadId}</summary>",
        "",
        f"  > **Severity:** {sev_label} \u00b7 **{line_label}** \u00b7 **Thread:** [#{suggestion.threadId}]({url})",
        "  >",
    ]
    for content_line in content.splitlines():
        detail.append(f"  > {content_line}")
    replacement_code = suggestion.replacement_code or ""
    if replacement_code.strip():
        detail += [
            "  >",
            "  > ```suggestion",
            *[f"  > {code_line}" for code_line in replacement_code.splitlines()],
            "  > ```",
        ]
    detail += ["", "  </details>"]
    return [bullet, *detail]


def _render_file_block(base_url: str, file_entry: FileEntry) -> list[str]:
    """Render a single file as a nested ``<details>`` block.

    Args:
        base_url: PR root URL for discussion links.
        file_entry: The file's review state.

    Returns:
        Markdown lines for the file block.
    """
    status = _normalize_status(file_entry.status)
    emoji = _STATUS_EMOJI.get(status, "")
    sev_label = _severity_counts_label(file_entry.suggestions)
    sev_suffix = f" — {sev_label}" if sev_label else ""

    summary_line = f"{emoji} {file_entry.fileName}{sev_suffix}"
    lines = [
        "<details>",
        f"<summary>{summary_line}</summary>",
        "",
        f"*Status:* {_VERDICT_DISPLAY.get(status, status)}",
        "",
        "**Summary of Changes**",
        "",
        file_entry.summary or "_Awaiting review..._",
    ]

    # Suggestions.
    lines += ["", "**Suggestions**", ""]
    if not file_entry.suggestions:
        lines.append("- None")
    else:
        by_sev: dict[str, list[SuggestionEntry]] = {sev: [] for sev in _SEVERITY_ORDER}
        other_severities: list[str] = []
        for s in file_entry.suggestions:
            sev = _normalized_severity_key(s.severity)
            if sev in by_sev:
                by_sev[sev].append(s)
            else:
                other_key = sev or "unknown"
                if other_key not in by_sev:
                    by_sev[other_key] = []
                    other_severities.append(other_key)
                by_sev[other_key].append(s)
        for sev in _SEVERITY_ORDER:
            group = by_sev[sev]
            if not group:
                continue
            lines += ["", f"#### {_SEVERITY_EMOJI.get(sev, '')} {_SEVERITY_LABELS[sev]}"]
            for s in group:
                lines += _render_suggestion(base_url, s)
        for sev in other_severities:
            label = sev.capitalize() if sev else "Unknown"
            lines += ["", f"#### ⚪ Other Severity ({label})"]
            for s in by_sev[sev]:
                lines += _render_suggestion(base_url, s)

    lines += ["", "</details>"]
    return lines


# ---------------------------------------------------------------------------
# Status sections (top-level, full fidelity)
# ---------------------------------------------------------------------------


def _render_status_file_sections(state: ReviewState, base_url: str, status_val: str, section_title: str) -> list[str]:
    """Render a status group as a heading section plus one section per file.

    Returns an ordered list of top-level section strings: a single heading
    section (e.g. ``### 📝 Needs Work (3)``) followed by one section per file
    (each rendered at full fidelity). Each file is its own top-level section so
    the smart-cutoff splitter can roll individual files into continuation
    comments. Returns an empty list when no files have *status_val*.
    """
    section_files = sorted(
        ((path, fe) for path, fe in state.files.items() if _normalize_status(fe.status) == status_val),
        key=lambda x: (x[1].folder or "root", x[0]),
    )
    if not section_files:
        return []
    count = len(section_files)
    sections: list[str] = [f"### {section_title} ({count})"]

    current_folder: str | None = None
    for _path, fe in section_files:
        folder = fe.folder or "root"
        block: list[str] = []
        if folder != current_folder:
            block += [f"**{folder}**", ""]
            current_folder = folder
        block += _render_file_block(base_url, fe)
        sections.append("\n".join(block).rstrip())
    return sections


def _render_overview_section(state: ReviewState) -> list[str]:
    """Render the overall progress / model table + rebase / skipped notes.

    This is a small top-level section that always stays in the root comment.
    Returns an empty list when there is nothing overview-worthy to show.
    """
    lines: list[str] = []
    if state.rebaseConflicts:
        lines += [
            "> \u26a0\ufe0f **Rebase Conflicts Detected** — the reviewed code could not be rebased onto the "
            "target branch and may be out of date with main.",
            "",
        ]

    if state.skippedFiles:
        not_on_branch = sum(1 for sf in state.skippedFiles if sf.reason == "not_on_branch")
        detail = f" ({not_on_branch} not on branch)" if not_on_branch else ""
        lines += ["", f"*Skipped files:* {len(state.skippedFiles)}{detail}"]

    return lines


def _render_narrative_section(state: ReviewState) -> list[str]:
    """Render the review narrative as a top-level ``<details>`` section."""
    narrative = state.overallSummary.narrativeSummary
    if not narrative:
        return []
    return [
        "<details>",
        "<summary>📖 Review Narrative</summary>",
        "",
        narrative,
        "",
        "</details>",
    ]


# ---------------------------------------------------------------------------
# Previous-reviews index (hash + link only — no embedded content)
# ---------------------------------------------------------------------------


def _render_previous_reviews_index(state: ReviewState, base_url: str) -> list[str]:
    """Render the 'Previous reviews' index from the per-commit comment registry.

    Each prior commit (any commit other than the current one) renders as a
    single bullet: short hash, status, reviewing model(s), and a link that jumps
    to that commit's review thread/comment. No prior content is embedded —
    readers follow the link to the dedicated per-commit comment.

    Args:
        state: The full review state.
        base_url: PR root URL for building discussion links.

    Returns:
        Markdown lines (empty list when there are no prior commits recorded).
    """
    current = state.commitHash or ""
    prior = [cc for sha, cc in state.commitComments.items() if sha != current]
    # Newest-first by timestamp (ISO strings sort lexicographically); entries
    # without a timestamp sort last.
    prior.sort(key=lambda cc: cc.timestamp or "", reverse=True)
    if not prior:
        return []

    lines = [
        "<details>",
        f"<summary><b>🗂️ Previous reviews ({len(prior)})</b></summary>",
        "",
    ]
    for cc in prior:
        short = _short_hash(cc.commitHash)
        status_display = _VERDICT_DISPLAY.get(cc.status, cc.status)
        models = ", ".join(m.modelId for m in cc.models) or "unknown"
        if cc.threadId > 0 and cc.rootCommentId > 0:
            url = build_discussion_url(base_url, cc.threadId, cc.rootCommentId)
            ref = f"[`{short}`]({url})"
        else:
            ref = f"`{short}`"
        lines.append(f"- {ref} — {status_display} — {models}")
    lines += ["", "</details>"]
    return lines


# ---------------------------------------------------------------------------
# Activity-log block (capped, newest-first)
# ---------------------------------------------------------------------------


def _render_activity_log_block(state: ReviewState) -> list[str]:
    """Render a compact Activity Log from session metadata (newest-first, capped)."""
    if not state.sessions:
        return []
    ordered = sorted(state.sessions, key=lambda s: s.startedUtc or "", reverse=True)
    shown = ordered[:_ACTIVITY_LOG_MAX_ENTRIES]
    omitted = len(ordered) - len(shown)
    lines = ["<details>", "<summary><b>📜 Activity Log</b></summary>", ""]
    for session in shown:
        short = _short_hash(session.commitHash)
        when = session.completedUtc or session.startedUtc or "unknown"
        status = session.status or "pending"
        sid = session.sessionId[:8]
        lines.append(f"- `{short}` · {status} · {when} · {session.modelId} · session `{sid}`")
    if omitted:
        lines.append(f"- *…and {omitted} older session(s).*")
    lines += ["", "</details>"]
    return lines


# ---------------------------------------------------------------------------
# Headline + completion detection
# ---------------------------------------------------------------------------


def is_review_complete(state: ReviewState) -> bool:
    """Return ``True`` when every file in the review has a terminal status.

    A review is complete once all files are ``approved`` or ``needs-work``.
    While incomplete (any file unreviewed/in-progress, or no files at all), the
    comment is kept lightweight (status headline only).
    """
    if not state.files:
        return False
    from .review_state import COMPLETE_STATUSES

    return all(_normalize_status(fe.status) in COMPLETE_STATUSES for fe in state.files.values())


def _render_headline(state: ReviewState, *, complete: bool) -> list[str]:
    """Render the marker + headline + reviewer/stats line for the root comment.

    The same headline is used for both the lightweight in-progress comment and
    the full completed comment; only the verb ("Being reviewed by" vs
    "Reviewed by") differs.
    """
    statuses = [_normalize_status(fe.status) for fe in state.files.values()]
    overall = compute_aggregate_status(statuses)
    counts = _count_by_status(state.files)
    approved_n = counts.get(ReviewStatus.APPROVED.value, 0)
    needs_n = counts.get(ReviewStatus.NEEDS_WORK.value, 0)
    total_n = len(state.files)
    reviewed_n = sum(1 for s in statuses if s in {ReviewStatus.APPROVED.value, ReviewStatus.NEEDS_WORK.value})
    short = _short_hash(state.commitHash)
    icon = get_model_icon(state.modelId)
    verb = "Reviewed by" if complete else "Being reviewed by"

    return [
        build_consolidated_marker(state.prId, state.commitHash),
        f"## 🔍 Pull Request Review — {_VERDICT_DISPLAY.get(overall, overall)}",
        "",
        f"🤖 *{verb}* {icon} **{state.modelId or 'unknown'}** \u00b7 "
        f"latest commit `{short}` \u00b7 **{approved_n} approved \u00b7 {needs_n} need work \u00b7 "
        f"{reviewed_n}/{total_n} reviewed**",
    ]


# ---------------------------------------------------------------------------
# Smart-cutoff splitter
# ---------------------------------------------------------------------------


def _chunk_oversized_sections(sections: list[str]) -> list[str]:
    """Split any section whose raw length exceeds :data:`HARD_CAP_CHARS`.

    Sections within the limit are returned unchanged. Oversized sections are
    split into consecutive character-level chunks of at most
    :data:`HARD_CAP_CHARS` characters each, guaranteeing that the splitter
    never has to handle a section that would alone exceed the platform hard
    limit.

    Args:
        sections: Ordered list of rendered section strings.

    Returns:
        A new list with oversized sections expanded into multiple chunks.
    """
    result: list[str] = []
    for section in sections:
        if len(section) <= HARD_CAP_CHARS:
            result.append(section)
        else:
            start = 0
            while start < len(section):
                result.append(section[start : start + HARD_CAP_CHARS])
                start += HARD_CAP_CHARS
    return result


def _split_into_comments(headline: str, sections: list[str], pr_id: int, commit_hash: str | None) -> list[str]:
    """Split a headline + ordered top-level sections into root + continuations.

    Before adding each section (after the first), the loop computes the
    *projected* size that would result from the addition and stops if it would
    exceed either :data:`SMART_CUTOFF_CHARS` (soft) or :data:`HARD_CAP_CHARS`
    (hard). The stopped section begins the next continuation comment. Each
    comment always contains at least one section (when any remain) so progress
    is guaranteed even for an oversized single section.

    Two enforcement layers prevent comments from exceeding the platform hard limit:

    1. **Pre-chunking** (:func:`_chunk_oversized_sections`) splits any section
       larger than :data:`HARD_CAP_CHARS` into character-level chunks, so no
       single section fed to this loop exceeds the cap.
    2. **Projected-size guard** — before adding any section after the first, the
       loop checks whether the projected size would exceed either limit (using the
       same *projected* basis for both checks), and breaks early if so.

    Args:
        headline: The root comment headline (already rendered to a string,
            carrying the ``v2`` consolidated marker).
        sections: Ordered top-level section strings.
        pr_id: Pull request ID (for continuation markers).
        commit_hash: Full reviewed commit SHA (for continuation markers).

    Returns:
        A list of comment strings: the root comment followed by zero or more
        continuation comments. Each continuation carries a ``type:continuation``
        marker tying it to *commit_hash* and its 1-based sequence. Always
        contains at least the root.
    """
    chunked = _chunk_oversized_sections(sections)
    comments: list[str] = []
    idx = 0
    n = len(chunked)
    while True:
        if not comments:
            parts = [headline]
            length = len(headline)
        else:
            seq = len(comments)
            cont_marker = build_continuation_marker(pr_id, commit_hash, seq)
            cont_header = f"{cont_marker}\n### 🔁 Review (continued {seq})"
            parts = [cont_header]
            length = len(cont_header)
        added_any = False
        while idx < n:
            section = chunked[idx]
            projected = length + len(section) + 2  # +2 for "\n\n" join separator
            if added_any and (projected > SMART_CUTOFF_CHARS or projected > HARD_CAP_CHARS):
                break
            parts.append(section)
            length = projected
            idx += 1
            added_any = True
        comments.append("\n\n".join(parts).rstrip() + "\n")
        if idx >= n:
            break
    return comments


# ---------------------------------------------------------------------------
# Top-level renderers
# ---------------------------------------------------------------------------


def _build_sections(state: ReviewState, base_url: str) -> list[str]:
    """Build the ordered list of top-level section strings for a full review.

    Each reviewed file becomes its **own** top-level section (preceded by a
    lightweight status/folder heading section) so the smart-cutoff splitter can
    roll individual files over into continuation comments. This avoids the prior
    problem where an entire status group rendered as one indivisible section.
    """
    sections: list[str] = []

    overview = _render_overview_section(state)
    if overview:
        sections.append("\n".join(overview))

    for status_val, section_title in _SECTION_ORDER:
        sections.extend(_render_status_file_sections(state, base_url, status_val, section_title))

    narrative = _render_narrative_section(state)
    if narrative:
        sections.append("\n".join(narrative))

    prev_index = _render_previous_reviews_index(state, base_url)
    if prev_index:
        sections.append("\n".join(prev_index))

    activity = _render_activity_log_block(state)
    if activity:
        sections.append("\n".join(activity))

    return sections


def render_commit_review_comments(state: ReviewState, base_url: str, *, force_in_progress: bool = False) -> list[str]:
    """Render a commit's review as a root comment plus continuation comments.

    While the review is **in progress** (not all files reviewed), this returns a
    single lightweight comment containing only the status headline — so each
    file submission patches a tiny comment rather than re-rendering the entire
    review. Once the review is **complete**, the full content is rendered and
    split across the root comment and any continuation comments using the
    :data:`SMART_CUTOFF_CHARS` smart cutoff.

    Args:
        state: The full review state to render.
        base_url: PR root URL for building discussion links.
        force_in_progress: When ``True``, always render the lightweight
            in-progress headline even if every file has a terminal status. Used
            by the live progress refresh (``agdt-pr-review-refresh-comment``),
            whose ``X/Y reviewed`` count is driven by the answer ledger rather
            than the terminal review state, so it must not prematurely render the
            full content before submit has posted verdicts/suggestion threads.

    Returns:
        A list of markdown comment strings: ``[root]`` while in progress, or
        ``[root, continuation_1, ...]`` once complete and large enough to split.
    """
    complete = is_review_complete(state) and not force_in_progress
    headline = "\n".join(_render_headline(state, complete=complete))
    if not complete:
        # Lightweight in-progress comment: headline only.
        return [headline.rstrip() + "\n"]
    sections = _build_sections(state, base_url)
    return _split_into_comments(headline, sections, state.prId, state.commitHash)


def render_consolidated_review_comment(state: ReviewState, base_url: str) -> str:
    """Render the full consolidated review comment as a single string.

    This is the root comment produced by :func:`render_commit_review_comments`
    (the lightweight headline while in progress, or the headline plus all
    sections once complete). Callers that handle continuation comments should
    use :func:`render_commit_review_comments` instead; this single-string form
    is retained for the file-review status-cascade update path and for tests
    that only inspect the primary comment content.

    Args:
        state: The full review state to render.
        base_url: PR root URL for building discussion links.

    Returns:
        The rendered root comment markdown string.
    """
    return render_commit_review_comments(state, base_url)[0]


def render_model_review_reply(state: ReviewState, model_id: str, base_url: str) -> str:
    """Render an additional model's review as a reply within a commit thread.

    A different model reviewing the same commit posts its review as a reply (no
    ``--force-rereview`` needed). The reply carries a ``model-review`` marker so
    it can be recovered and updated in place when that same model re-runs.

    The body summarises the commit's current file statuses (each terminal file
    rendered once); files still unreviewed/in-progress are omitted.

    Args:
        state: The full review state.
        model_id: The additional reviewing model's identifier.
        base_url: PR root URL for building discussion links.

    Returns:
        The rendered reply markdown string (always carries the marker).
    """
    icon = get_model_icon(model_id)
    short = _short_hash(state.commitHash)
    lines: list[str] = [
        build_model_reply_marker(state.prId, state.commitHash, model_id),
        f"### 🤝 Additional review by {icon} **{model_id}** \u00b7 commit `{short}`",
        "",
    ]

    approved_n = 0
    needs_n = 0
    file_lines: list[str] = []
    for file_path in sorted(state.files):
        fe = state.files[file_path]
        status = _normalize_status(fe.status)
        if status == ReviewStatus.APPROVED.value:
            approved_n += 1
        elif status == ReviewStatus.NEEDS_WORK.value:
            needs_n += 1
        else:
            continue
        display = _VERDICT_DISPLAY.get(status, status)
        file_lines.append(f"- `{file_path}` — {display}")

    lines.append(f"🤖 **{approved_n} approved \u00b7 {needs_n} need work** for this commit.")
    if file_lines:
        lines.append("")
        lines.extend(file_lines)
    return "\n".join(lines).rstrip() + "\n"
