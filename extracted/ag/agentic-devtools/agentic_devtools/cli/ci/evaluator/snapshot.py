"""Snapshot builder for the post-agent evaluator.

Gathers all PR state needed for classification into an immutable
PostAgentSnapshot dataclass.
"""

from __future__ import annotations

import logging
import re

from ..guards import (
    CYCLE_TRACKER_MARKER,
    DEDUP_MARKER_PATTERN,
    REPAIR_SATISFIED_MARKER,
    REVIEW_ID_MARKER_RE,
    THREAD_EVALUATED_MARKER,
    find_repair_satisfied_review_id,
)
from ..models import COPILOT_COMMENT_LOGINS, IssueCommentInfo, is_copilot_login
from ..provider import CIPlatformProvider
from ..review_thread_state import fetch_review_thread_states
from .lock import _LOCK_MARKER as _EVALUATOR_LOCK_MARKER
from .lock import check_lock_status
from .models import CommentInfo, PostAgentSnapshot, ThreadInfo

logger = logging.getLogger(__name__)

_SENTINEL_MARKER = "<!-- copilot-agent-result -->"

# Issue-comment control markers whose exact spelling the HTML-comment balancer
# could synthesize by inserting a closing ``-->`` into a truncated opener (e.g.
# ``<!-- ai-pr-loop:repair-satisfied`` at end of a quoted line becomes the
# canonical marker). If a sanitized rewrite would introduce one of these trusted
# signals — or a ``review-id`` marker — that was not already present, the rewrite
# must not be persisted back to the provider: a later evaluator run would
# otherwise treat the synthesized marker as a genuine Copilot signal (for
# example incorrectly clearing a suppressed-comments block).
_SYNTHESIZABLE_CONTROL_MARKERS = (
    _SENTINEL_MARKER,
    REPAIR_SATISFIED_MARKER,
    THREAD_EVALUATED_MARKER,
    CYCLE_TRACKER_MARKER,
    _EVALUATOR_LOCK_MARKER,
)

# Variable-content dedup/dispatch markers the balancer could likewise synthesize
# by closing a truncated opener. Their embedded fields (review id, SHAs, ISO-8601
# timestamp) mean a fixed-string ``.count`` check is insufficient, so the full
# ordered list of complete markers is compared instead (as with ``review-id``):
#
# * ``<!-- copilot-trigger:{review_id}[:{iso8601_utc}] -->`` — scanned by
#   :func:`is_duplicate_trigger`; a synthesized marker with an unparseable
#   timestamp is treated as a non-expiring duplicate, permanently suppressing a
#   legitimate re-dispatch.
# * ``<!-- repair-dispatch:{sha}:{count}:{writer_token} -->`` — parsed by
#   :data:`DEDUP_MARKER_PATTERN` in :func:`check_deduplication`; a synthesized
#   marker can shadow the real dedup-tracking comment and skew the dispatch
#   count or redirect the next update into a Copilot-authored comment.
# * ``<!-- agdt:conflict-repair:{base}:{head}:{iso8601_utc} -->`` — located by
#   ``find_comment(CONFLICT_REPAIR_MARKER_PREFIX)`` on behalf of
#   :class:`~agentic_devtools.cli.ci.pipeline.actions.dispatch_conflict_resolution.DispatchConflictResolutionAction`.
#   Both ``should_dispatch_conflict_repair`` and ``count_conflict_repair_dispatches``
#   are identity-scoped to the PR-token login (``dispatch_login``), so neither a
#   verbatim quote nor a synthesized marker in a Copilot-authored comment can
#   affect deduplication or the attempt count — they are equally inert.
#   The escaping here is therefore defense in depth rather than a load-bearing
#   protection.
#
# Each pattern requires the closing ``-->`` (which the balancer inserts), so a
# truncated opener present in the original body does not match until it has been
# balanced — the resulting mismatch blocks persistence.
_COPILOT_TRIGGER_MARKER_RE = re.compile(r"<!--\s*copilot-trigger:[^>]*?-->")
_CONFLICT_REPAIR_MARKER_RE = re.compile(r"<!--\s*agdt:conflict-repair:[^>]*?-->")
_SYNTHESIZABLE_CONTROL_MARKER_PATTERNS = (
    REVIEW_ID_MARKER_RE,
    _COPILOT_TRIGGER_MARKER_RE,
    DEDUP_MARKER_PATTERN,
    _CONFLICT_REPAIR_MARKER_RE,
)
_ATX_HEADING_RE = re.compile(r"^#{1,6}(?:[ \t]|$)")
# CommonMark type-1 and type-6 HTML block tag names that may interrupt a paragraph.
# Type-1: <pre>, <script>, <style>, <textarea> (and their closing variants).
# Type-6: the block-level elements listed in the CommonMark spec §4.6.
# Type-7 tags (e.g. <span>, <em>) cannot interrupt a paragraph and are excluded.
_HTML_BLOCK_TYPE1_NAMES = frozenset({"pre", "script", "style", "textarea"})
_HTML_BLOCK_TYPE6_NAMES = frozenset(
    {
        "address",
        "article",
        "aside",
        "base",
        "basefont",
        "blockquote",
        "body",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "link",
        "main",
        "menu",
        "menuitem",
        "meta",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "param",
        "search",
        "section",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
    }
)
_HTML_BLOCK_INTERRUPT_NAMES = _HTML_BLOCK_TYPE1_NAMES | _HTML_BLOCK_TYPE6_NAMES
# Matches a line-leading open/close tag whose name is a paragraph-interrupting
# block-level element (type-1 or type-6).  The tag name is captured so callers
# can look it up in _HTML_BLOCK_INTERRUPT_NAMES (case-insensitively).
_HTML_BLOCK_TAG_START_RE = re.compile(r"^</?([A-Za-z][A-Za-z0-9-]*)(?:\s[^>]*)?>")
# Matches a line-leading list-item marker on blockquote-stripped content: a
# bullet (``-``/``+``/``*``) or an ordered marker (1-9 digits then ``.`` or
# ``)``), followed by a space/tab or end of line. Used both for list-item
# content-indent tracking and to detect paragraph-breaking list items. CommonMark
# only lets an ordered list interrupt an active paragraph when it starts at ``1``
# (handled by :func:`_interrupts_paragraph_with_list_item`), but non-``1``
# ordered markers still count as list items after a real block boundary.
_LIST_ITEM_RE = re.compile(r"^(?P<marker>(?:[-+*])|(?P<ordered>\d{1,9}[.)]))(?:[ \t]|$)")


def _advance_column(column: int, char: str) -> int:
    """Return the next visual column after consuming one whitespace character."""
    if char == "\t":
        return column + (4 - (column % 4))
    return column + (1 if char == " " else 0)


def _leading_whitespace_columns(text: str, *, start_column: int = 0) -> int:
    """Return the visual width of ``text``'s leading whitespace.

    Tabs expand to the next four-column stop from ``start_column`` so callers can
    measure indentation relative to an existing container column.
    """
    column = start_column
    i = 0
    while i < len(text) and text[i] in {" ", "\t"}:
        column = _advance_column(column, text[i])
        i += 1
    return column - start_column


def _list_item_content_indent(stripped: str, indent: int) -> int | None:
    """Return the content indent (columns) for a list-item line, or ``None``.

    ``stripped`` is the line with blockquote markers and leading whitespace
    removed; ``indent`` is its leading indentation in columns relative to any
    enclosing blockquote. Follows the CommonMark rule that 1–4 spaces after the
    marker set the item's content indent, while more than four spaces (or an
    empty item) fall back to a single space — the extra indentation then becomes
    indented code *within* the item. Used so an indented line inside a list item
    is measured relative to the item's content column rather than column zero.
    """
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return None
    marker = match.group(0).rstrip(" \t")
    rest = stripped[len(marker) :]
    padding_cols = _leading_whitespace_columns(rest, start_column=indent + len(marker))
    if padding_cols > 4 or not rest.strip():
        padding_cols = 1
    return indent + len(marker) + padding_cols


def _strip_list_item_prefix_for_block_detection(stripped: str, indent: int) -> str:
    """Return ``stripped`` with only a list marker's effective padding removed."""
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return stripped
    marker = match.group(0).rstrip(" \t")
    rest = stripped[len(marker) :]
    if not rest:
        return ""
    padding_cols = _leading_whitespace_columns(rest, start_column=indent + len(marker))
    if padding_cols > 4:
        return rest[1:] if rest[:1] in {" ", "\t"} else rest
    return rest.lstrip(" \t")


def _interrupts_paragraph_with_list_item(stripped: str, *, in_list_context: bool) -> bool:
    """Return True when ``stripped`` starts a list item that may interrupt a paragraph.

    CommonMark allows bullet-list items to interrupt a paragraph, but ordered
    lists only do so when their marker starts at ``1``. Non-``1`` ordered
    markers are still recognised as list items by :func:`_list_item_content_indent`;
    they just do not flush an already-active *top-level* paragraph. Within an
    existing list container, a later ordered item (e.g. ``2.`` after ``1.``)
    still starts a new sibling item and must therefore break paragraph
    accumulation.
    """
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return False
    ordered = match.group("ordered")
    # ``ordered`` (when present) is the digits plus a trailing ``.``/``)``; the
    # start number must equal ``1`` (parsed as int to handle leading zeroes such
    # as ``01.``) — ``14.`` / ``10)`` do not interrupt.
    return ordered is None or int(ordered[:-1]) == 1 or in_list_context


def _get_review_thread_statuses(
    provider: CIPlatformProvider,
    pr_number: int,
) -> dict[int, tuple[bool, bool]]:
    """Map review comment IDs to (is_resolved, has_reply) when provider supports it.

    Returns an empty mapping when the provider cannot report review-thread state
    (missing capability or failed lookup). Callers then default every thread to
    ``is_resolved=False``, which fails closed: a provider that lacks the
    capability can never make threads look resolved.
    """
    result = fetch_review_thread_states(provider, pr_number)
    if result.degraded:
        logger.warning(
            "PR #%d: review-thread state unavailable (%s) — treating all threads as unresolved",
            pr_number,
            result.reason,
        )
    return result.states


def _compute_markdown_code_mask(body: str) -> list[bool]:
    """Return a per-character mask where ``True`` marks Markdown *code* positions.

    Characters inside fenced code blocks (delimited by a line-leading run of at
    least three ``` ``` ``` backticks or ``~~~`` tildes), indented code blocks (a
    line indented four or more columns that does not continue a paragraph), and
    inline code spans (delimited by matching backtick runs) are marked ``True``.

    Fence delimiters follow the CommonMark rules that matter for masking: a
    backtick fence's info string may not contain a backtick (so a line such as
    ``` ```lang` ``` is text, not a fence), and a closing fence may be indented
    at most three columns (a fence indented four or more columns is code content,
    not a closer). Getting either wrong would mask — and thus fail to close — an
    unterminated ``<!--`` on a following line.

    Inline code spans may span multiple lines within a single paragraph:
    GitHub-Flavored Markdown joins a paragraph's lines before matching backtick
    runs, so ``\u0060a\\nb\u0060`` is one code span. Backtick matching therefore
    runs over the whole paragraph, resetting at paragraph-breaking block
    boundaries (blank lines including bare ``>`` blank-in-blockquote lines;
    fenced/indented code blocks; blockquote-depth *increases* — a lazy
    continuation line that merely drops ``>`` markers stays in the paragraph;
    heading/hr block starts, including setext ``=``/``--`` underlines;
    line-leading ``<!--`` HTML block openers; and new list-item markers).
    Matching per paragraph (rather than per
    line) mirrors the
    provider's own rendering, so a ``<!--`` that the provider treats as code is
    masked and one it treats as a real comment is left unmasked.

    Indented code blocks follow the CommonMark rule that four-space (or tab)
    indentation is only code when it does *not* interrupt a paragraph. An
    indented line immediately after paragraph text is a lazy continuation and
    renders as normal text, so its ``<!--`` stays unmasked (and thus closeable);
    only an indented line following a blank line or block boundary is genuine
    code and is masked. Indentation is measured relative to any enclosing
    blockquote, so ``>     <!--`` is recognised the same as ``    <!--``, and
    relative to any enclosing list item's content column, so a four-space line
    inside ``- item`` (content indent two) is an ordinary block, not code.

    The HTML-comment sanitizer uses this mask to skip ``<!--`` / ``-->``
    sequences that live inside code. Markdown renders such sequences as literal
    text, so they never break rendering and must not be rewritten when a
    sanitized body is persisted back to the provider.

    Args:
        body: Raw comment body text.

    Returns:
        A list of booleans, one per character in ``body``.
    """
    mask = [False] * len(body)

    def _is_thematic_break(text: str) -> bool:
        compact = text.replace(" ", "").replace("\t", "")
        if len(compact) < 3:
            return False
        ch = compact[0]
        return ch in {"-", "_", "*"} and all(c == ch for c in compact)

    def _is_setext_underline(text: str) -> bool:
        """Return True for a setext-heading underline (a run of ``=`` or ``-``).

        A line of only ``=`` (any length) or only ``-`` (length >= 2) underlines
        the preceding paragraph as a setext heading (CommonMark §4.3), so it
        terminates paragraph accumulation just like an ATX heading: a code span
        cannot pair a backtick across the underline into the following block.
        ``-`` runs of length >= 3 are already handled as thematic breaks; a lone
        ``-`` is left to list-item handling, so only ``=`` runs and the length-2
        ``--`` case are added here.
        """
        compact = text.strip()
        return (
            bool(compact)
            and all(c == compact[0] for c in compact)
            and (compact[0] == "=" or (compact[0] == "-" and len(compact) >= 2))
        )

    def _starts_paragraph_breaking_block(text: str, indent_cols: int) -> bool:
        if indent_cols > 3:
            return False
        return bool(_ATX_HEADING_RE.match(text) or _is_thematic_break(text) or _is_setext_underline(text))

    def _starts_html_block(text: str, indent_cols: int) -> bool:
        """Return True when ``text`` starts a line-leading CommonMark HTML block.

        For sanitizer safety we treat HTML-comment openers (type 2), processing
        instructions/CDATA/declarations, and line-leading block-level HTML tags
        (types 1 and 6) as block starts. They interrupt any active paragraph so
        cross-line backticks cannot mask a live ``<!--`` opener on the HTML line.

        Type-7 tags (e.g. ``<span>``, ``<em>``) are excluded because they cannot
        interrupt a paragraph; treating them as block starts would incorrectly
        flush the paragraph and leave a following ``<!--`` on the next line
        unmasked when it is actually inside an inline code span.
        """
        if indent_cols > 3 or not text.startswith("<"):
            return False
        if (
            text.startswith("<!--")
            or text.startswith("<?")
            or text.startswith("<![CDATA[")
            or (text.startswith("<!") and len(text) > 2 and text[2].isupper())
        ):
            return True
        m = _HTML_BLOCK_TAG_START_RE.match(text)
        return m is not None and m.group(1).lower() in _HTML_BLOCK_INTERRUPT_NAMES

    def _mark_inline_spans(start: int, end: int) -> None:
        """Mask inline code spans within ``body[start:end]`` (one paragraph).

        A backtick run opens a span closed by the next run of *equal* length,
        which may lie on a later line of the same paragraph. An unmatched run is
        literal and masks nothing.

        CommonMark backslash-escape rule: an odd-length run of ``\\`` before a
        backtick escapes that backtick (renders as a literal backtick), so it
        cannot *open* a span. Escapes do not apply inside a code span, so a
        closing run of equal length still closes the span even when preceded by
        a backslash.
        """
        i = start
        while i < end:
            if body[i] != "`":
                i += 1
                continue
            # A backtick preceded by an odd-length backslash run is a CommonMark
            # backslash escape — the backtick renders literally and cannot open a
            # code span.  Count the run of ``\`` characters immediately before
            # this position and skip the escaped backtick if the count is odd.
            bs = 0
            j = i - 1
            while j >= start and body[j] == "\\":
                bs += 1
                j -= 1
            if bs % 2 == 1:
                i += 1
                continue
            run_start = i
            while i < end and body[i] == "`":
                i += 1
            run = i - run_start
            # A span closes at the next run of exactly ``run`` backticks.
            # CommonMark backslash escapes do NOT apply inside a code span, so a
            # closing run is a delimiter even when preceded by a backslash (e.g.
            # `` `foo\` `` closes at the trailing backtick, yielding ``foo\``).
            # The ``k`` cursor resumes just past each run scanned.
            close = -1
            k = i
            while k < end:
                if body[k] != "`":
                    k += 1
                    continue
                tick_start = k
                while k < end and body[k] == "`":
                    k += 1
                if k - tick_start == run:
                    close = tick_start
                    break
            if close != -1:
                for p in range(run_start, close + run):
                    mask[p] = True
                i = close + run
            # Unmatched backticks are literal — ``i`` already sits past the run.

    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_bq_depth = 0  # blockquote depth at which the fence opened
    fence_list_indent = 0  # list-item content-indent column at which the fence opened
    offset = 0
    para_start = -1  # offset of the current paragraph's first char, or -1 if none
    para_end = 0  # offset just past the current paragraph's last char
    para_bq_depth = 0  # blockquote depth of the paragraph being accumulated
    list_content_indents: list[int] = []  # stack of open list-item content-indent columns
    list_blockquote_depths: list[int] = []  # blockquote depth at which each list item opened

    def _current_list_content_indent() -> int:
        return list_content_indents[-1] if list_content_indents else 0

    def _pop_list_context() -> None:
        list_content_indents.pop()
        list_blockquote_depths.pop()

    def _flush_paragraph() -> None:
        nonlocal para_start
        if para_start != -1:
            _mark_inline_spans(para_start, para_end)
            para_start = -1

    for line in body.split("\n"):
        line_len = len(line)
        # Strip leading whitespace and any number of blockquote ``>`` markers
        # (e.g. ``> > ``` ``), so that quoted fenced code blocks and quoted blank
        # lines are recognised the same way as un-quoted ones.  The original
        # ``line`` is still used for inline-code detection (where backtick
        # positions matter) and for mask-offset arithmetic, so we keep both.
        # Count the depth (number of ``>`` markers) so a context change (e.g.
        # from a normal paragraph into a blockquote) flushes the current
        # paragraph — CommonMark containers are block-level boundaries that a
        # code span cannot cross.
        stripped = line.lstrip(" \t")
        bq_depth = 0
        while stripped.startswith(">"):
            bq_depth += 1
            stripped = stripped[1:].lstrip(" \t")
        # Measure the line's indentation in a coordinate system that ignores
        # blockquote markers but preserves every real whitespace column around
        # them. For ``  > quote`` this stays at column two, so the parent list
        # item's content column is preserved across the nested blockquote.
        indent = 0
        cursor = 0
        while cursor < line_len:
            while cursor < line_len and line[cursor] in {" ", "\t"}:
                indent = _advance_column(indent, line[cursor])
                cursor += 1
            if cursor >= line_len or line[cursor] != ">":
                break
            cursor += 1
            if cursor < line_len and line[cursor] == " ":
                cursor += 1
        if not in_fence:
            while list_blockquote_depths and bq_depth < list_blockquote_depths[-1]:
                _pop_list_context()
        previous_list_content_indent = _current_list_content_indent()
        list_item_candidate = bool(
            stripped
            and not _is_thematic_break(stripped)
            and indent - previous_list_content_indent <= 3
            and _LIST_ITEM_RE.match(stripped)
        )
        list_item_starts_block = list_item_candidate and (
            para_start == -1
            or _interrupts_paragraph_with_list_item(
                stripped,
                in_list_context=previous_list_content_indent > 0,
            )
        )
        block_stripped = (
            _strip_list_item_prefix_for_block_detection(stripped, indent) if list_item_starts_block else stripped
        )
        # Count a leading run of >=3 backticks or tildes (a code-fence delimiter).
        fence_run = 0
        if block_stripped[:1] in ("`", "~"):
            delimiter = block_stripped[0]
            for ch in block_stripped:
                if ch != delimiter:
                    break
                fence_run += 1
            if fence_run < 3:
                fence_run = 0
            elif delimiter == "`" and "`" in block_stripped[fence_run:]:
                # A backtick fence's info string may not contain a backtick
                # (CommonMark); a line such as ```` ```lang` ```` is therefore not a
                # fence delimiter at all. Tilde fences have no such restriction. Zero
                # the run so the line is treated as ordinary text and any ``<!--`` on
                # the following line stays unmasked (and thus closeable).
                fence_run = 0
        # In CommonMark a fenced code block is scoped to its container.  A
        # depth change (leaving the blockquote that opened the fence) implicitly
        # closes the fence so the current line is processed normally.  Likewise,
        # a nonblank line that de-indents out of the list item that opened the
        # fence (its content column) leaves the fence's container and implicitly
        # closes it — analogous to the blockquote-depth handling — so a later
        # ``<!--`` outside the list is not masked as code.
        if in_fence and bq_depth != fence_bq_depth:
            in_fence = False
        elif in_fence and stripped and indent < fence_list_indent:
            in_fence = False
        if not in_fence and stripped:
            if (
                para_start != -1
                and list_content_indents
                and indent < _current_list_content_indent()
                and (
                    fence_run >= 3
                    or _starts_html_block(block_stripped, indent - _current_list_content_indent())
                    or _starts_paragraph_breaking_block(block_stripped, indent - _current_list_content_indent())
                )
            ):
                while list_content_indents and indent < list_content_indents[-1]:
                    _pop_list_context()
            previous_list_content_indent = _current_list_content_indent()
            # Track a stack of enclosing list-item content indents so that
            # indentation is measured relative to the innermost still-open item.
            # When a nested item ends, popping back to the parent item restores
            # the parent's content column instead of resetting all the way to
            # column zero.
            #
            # Guard: only recognise a list item when (a) the line is indented
            # at most three columns past the enclosing content column — a line
            # indented four or more columns past that column is an indented code
            # block and must not push false list context into following lines,
            # and (b) the line is not a thematic break (``- - -``, ``* * *``,
            # ``___``, etc.) — CommonMark gives thematic breaks higher
            # precedence than list items, so they must not update list context.
            item_indent = _list_item_content_indent(stripped, indent) if list_item_starts_block else None
            if item_indent is not None:
                while list_content_indents and indent < list_content_indents[-1]:
                    _pop_list_context()
                list_content_indents.append(item_indent)
                list_blockquote_depths.append(bq_depth)
            else:
                # Only pop the list-item stack when we are not inside an
                # active paragraph.  A less-indented line that arrives while
                # a paragraph is accumulating is a CommonMark *lazy
                # continuation*: it remains inside the enclosing list item
                # even though its column is below the item's content indent.
                # Popping here would misclassify the next indented line as
                # top-level indented code instead of text two columns into
                # the still-open item, causing the sanitizer to leave a
                # real ``<!--`` unterminated.
                if para_start == -1:
                    while list_content_indents and indent < list_content_indents[-1]:
                        _pop_list_context()
        list_content_indent = _current_list_content_indent()
        if in_fence:
            for k in range(offset, offset + line_len):
                mask[k] = True
            # A closing fence is a bare run of the same delimiter, at least as
            # long as the opener (an info string means it is a content line),
            # indented at most three columns relative to any blockquote *and* to
            # the enclosing list item's content column (a fence indented four or
            # more columns past that column is content, not a closer) — measured
            # the same way as the opener so a list-nested fence is closed here.
            if (
                indent - list_content_indent <= 3
                and fence_run >= fence_len
                and stripped[:1] == fence_char
                and stripped.rstrip().rstrip(fence_char) == ""
            ):
                in_fence = False
        elif not stripped:
            # A blank line (or bare ``>`` blank-in-blockquote) ends the paragraph.
            _flush_paragraph()
        elif indent - list_content_indent >= 4 and para_start == -1:
            # An indented code block: four or more columns of indentation past any
            # enclosing list item's content column, that does not continue a
            # paragraph. (An indented line *within* a paragraph is a lazy
            # continuation — normal text — so it falls through to paragraph
            # accumulation and stays unmasked.)
            for k in range(offset, offset + line_len):
                mask[k] = True
        elif fence_run >= 3 and indent - list_content_indent <= 3:
            # A fence opens a new block; flush the paragraph it interrupts.
            # CommonMark requires at most three columns of indentation for a fence
            # opener, measured relative to the enclosing list item's content
            # column (as the indented-code branch above does); a line indented
            # four or more columns past that column is ordinary paragraph text (or
            # an indented-code continuation) and falls through.
            _flush_paragraph()
            in_fence = True
            fence_char = block_stripped[0]
            fence_len = fence_run
            fence_bq_depth = bq_depth
            fence_list_indent = list_content_indent
            for k in range(offset, offset + line_len):
                mask[k] = True
        else:
            # Accumulate this line into the current paragraph; inline code spans
            # are matched across the whole paragraph when it is flushed.
            # An *increase* in blockquote depth enters a deeper CommonMark
            # container (a block-level boundary a code span cannot cross), so
            # flush the previous paragraph first. A *decrease* is not a boundary:
            # CommonMark allows a blockquote paragraph to be lazily continued by a
            # line that omits the ``>`` markers, so such a line stays in the same
            # paragraph and keeps accumulating.
            if para_start != -1 and bq_depth > para_bq_depth:
                _flush_paragraph()
            # A line-leading HTML block opener interrupts the paragraph.
            # Flush the previous paragraph to sever any cross-line backtick
            # pairing, but leave the opener line unmasked and do NOT start a new
            # paragraph with it so any live ``<!--`` on that line remains
            # closeable.
            if _starts_html_block(block_stripped, indent - list_content_indent):
                _flush_paragraph()
            # Heading and thematic-break lines are self-contained blocks.
            # Flush any in-progress paragraph and do NOT start a new one with
            # this line; that way backticks inside a heading cannot pair with
            # backticks on a following paragraph line and mask an ``<!--``.
            # We still call ``_mark_inline_spans`` for the heading/thematic-break
            # line itself so that inline-code HTML examples on that line are
            # masked and cannot be misidentified as live ``<!--`` openers.
            elif _starts_paragraph_breaking_block(block_stripped, indent - list_content_indent):
                _flush_paragraph()
                _mark_inline_spans(offset, offset + line_len)
            else:
                # A new list-item marker begins a separate CommonMark container
                # block; a code span cannot cross into it, so flush the previous
                # paragraph before starting a fresh one with this line. (A lazy
                # continuation line carries no marker and keeps accumulating.)
                if para_start != -1 and _interrupts_paragraph_with_list_item(
                    stripped,
                    in_list_context=previous_list_content_indent > 0,
                ):
                    _flush_paragraph()
                if para_start == -1:
                    para_start = offset
                    para_bq_depth = bq_depth
                para_end = offset + line_len
        offset += line_len + 1
    _flush_paragraph()
    return mask


def _sanitize_unterminated_html_comments_with_insertions(body: str) -> tuple[str, tuple[int, ...]]:
    """Return the balanced body plus the start offsets of inserted closers.

    A cloud agent's completion reply frequently quotes a repair-dispatch comment
    and truncates it mid–HTML-comment, leaving a ``<!--`` with no closing
    ``-->``. On GitHub the unterminated comment swallows everything that follows.
    This helper closes every unterminated ``<!--`` — at the end of its own line,
    immediately before the next opener on that line, or at the end of the string
    — so every opener ends up with its own closer and all subsequent content
    stays visible.

    Two properties keep the rewrite safe:

    * **Insert-only.** It never deletes text, so a well-formed sentinel such as
      ``<!-- copilot-agent-result -->`` is preserved verbatim and downstream
      substring checks (sentinel / HEAD-SHA detection) remain correct.
    * **Code-aware.** ``<!--`` / ``-->`` inside Markdown fenced code blocks or
      inline code spans are ignored, so a literal comment sample inside a code
      block is never rewritten when the sanitized body is persisted back to the
      provider.
    * **Escape-aware.** A ``\\<!--`` sequence (odd-length backslash run before
      ``<``) is a CommonMark backslash escape that renders as the literal text
      ``&lt;!--``; it is not an HTML comment opener and is never balanced or
      rewritten.

    Args:
        body: Raw comment body text.

    Returns:
        A tuple of the balanced body and the start offsets of each inserted
        `` -->`` closer within that balanced body.
    """
    mask = _compute_markdown_code_mask(body)

    def _find_outside_code(sub: str, start: int) -> int:
        idx = body.find(sub, start)
        while idx != -1 and mask[idx]:
            idx = body.find(sub, idx + 1)
        return idx

    def _is_backslash_escaped(idx: int) -> bool:
        """Return True when the character at ``idx`` is preceded by an odd-length
        run of backslashes — making it a CommonMark backslash escape sequence.

        CommonMark's backslash-escape rule: one backslash escapes the following
        ASCII punctuation character, so ``\\<`` renders as a literal ``<``
        (not an HTML opener). Two backslashes render as one literal backslash,
        leaving the next character un-escaped. In general, an odd-length run
        means the character at ``idx`` is escaped; an even-length run means the
        backslashes cancel each other out and the character is not escaped.
        """
        n = 0
        i = idx - 1
        while i >= 0 and body[i] == "\\":
            n += 1
            i -= 1
        return n % 2 == 1

    insertions: list[int] = []
    search_from = 0
    end = len(body)
    while True:
        open_idx = _find_outside_code("<!--", search_from)
        if open_idx == -1:
            break
        if _is_backslash_escaped(open_idx):
            # ``\<!--`` is a CommonMark escape for a literal ``<``; it is not a
            # real HTML comment opener and must not be balanced or rewritten.
            search_from = open_idx + 4
            continue
        # Once an unmasked ``<!--`` has opened an HTML comment, Markdown code
        # syntax is inactive until the first raw ``-->``.  Use a raw string
        # search for the closer so a ``-->`` that happens to sit inside a
        # backtick code span (e.g. ``<!-- text `-->` tail``) is not missed.
        # The code mask is only needed to decide whether the *opener* itself is
        # inside a code construct; for the closer we always want the first raw
        # occurrence after the opener.
        close_idx = body.find("-->", open_idx + 4)
        next_open = _find_outside_code("<!--", open_idx + 4)
        if close_idx != -1 and (next_open == -1 or next_open > close_idx):
            # Well-formed comment — skip past its closer.
            search_from = close_idx + 3
            continue
        # Unterminated: no closer, or another opener precedes the candidate
        # closer (so that ``-->`` belongs to the inner comment, not this one).
        line_end = body.find("\n", open_idx)
        if next_open != -1 and (line_end == -1 or next_open < line_end):
            # Close this opener just before the next opener on the same line,
            # then continue scanning from that opener so it is balanced too.
            insertions.append(next_open)
            search_from = next_open
            continue
        if line_end == -1:
            # Unterminated on the final line — append the closer at the end.
            insertions.append(end)
            break
        # Close at the end of this opener's line so later lines still render,
        # then resume past the newline (``<!--`` never starts on a ``\n``).
        insertions.append(line_end)
        search_from = line_end + 1
    if not insertions:
        return body, ()
    pieces: list[str] = []
    inserted_positions: list[int] = []
    prev = 0
    rendered_len = 0
    for pos in insertions:
        chunk = body[prev:pos]
        pieces.append(chunk)
        rendered_len += len(chunk)
        inserted_positions.append(rendered_len)
        pieces.append(" -->")
        rendered_len += 4
        prev = pos
    pieces.append(body[prev:])
    return "".join(pieces), tuple(inserted_positions)


def _sanitize_unterminated_html_comments(body: str) -> str:
    """Balance any unterminated ``<!--`` sequences so they cannot break rendering."""
    sanitized_body, _inserted_positions = _sanitize_unterminated_html_comments_with_insertions(body)
    return sanitized_body


def _get_latest_agent_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    comments: list | None = None,
    *,
    persist_sanitized_body: bool = False,
) -> CommentInfo | None:
    """Get the latest Copilot-authored issue comment if supported by provider.

    When ``persist_sanitized_body`` is ``True``, any balanced-body rewrite is
    also patched back to the source issue comment so GitHub no longer renders
    the remainder of the comment as swallowed by an unterminated HTML comment.
    Persistence is best-effort: read paths keep working even if the PATCH fails.
    """
    if comments is None:
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if not callable(list_issue_comments):
            return None
        comments = list_issue_comments(pr_number)
    latest = _get_latest_copilot_issue_comment(comments)
    if latest is None:
        return None
    sanitized_body, inserted_positions = _sanitize_unterminated_html_comments_with_insertions(latest.body)
    persisted_body = (
        _neutralize_synthesized_control_markers(sanitized_body, inserted_positions)
        if persist_sanitized_body and sanitized_body != latest.body
        else sanitized_body
    )
    if (
        persist_sanitized_body
        and persisted_body != latest.body
        and not _introduces_control_marker(latest.body, persisted_body)
    ):
        update_comment = getattr(provider, "update_comment", None)
        if callable(update_comment):
            try:
                update_comment(latest.id, persisted_body)
            except Exception as exc:
                logger.warning(
                    "Failed to persist sanitized Copilot comment %d on PR #%d: %s",
                    latest.id,
                    pr_number,
                    exc,
                )
    return CommentInfo(
        id=latest.id,
        author=latest.author,
        body=persisted_body if persist_sanitized_body else sanitized_body,
        created_at=latest.created_at,
    )


def _neutralize_synthesized_control_markers(body: str, inserted_positions: tuple[int, ...]) -> str:
    """Escape any trusted marker whose closing ``-->`` was synthesized by balancing."""
    opener_positions: set[int] = set()
    for pos in inserted_positions:
        open_idx = body.rfind("<!--", 0, pos)
        if open_idx == -1:
            continue
        candidate = body[open_idx : pos + 4]
        if candidate in _SYNTHESIZABLE_CONTROL_MARKERS or any(
            pattern.fullmatch(candidate) for pattern in _SYNTHESIZABLE_CONTROL_MARKER_PATTERNS
        ):
            opener_positions.add(open_idx)
    if not opener_positions:
        return body
    pieces: list[str] = []
    prev = 0
    for open_idx in sorted(opener_positions):
        pieces.append(body[prev:open_idx])
        pieces.append("&lt;!--")
        prev = open_idx + 4
    pieces.append(body[prev:])
    return "".join(pieces)


def _introduces_control_marker(original: str, sanitized: str) -> bool:
    """Return True when *sanitized* gains a trusted control marker absent in *original*.

    The HTML-comment balancer inserts a closing ``-->`` into a truncated
    ``<!--`` opener. That can synthesize the *exact* spelling of a trusted
    issue-comment control marker (e.g. :data:`REPAIR_SATISFIED_MARKER` or a
    ``review-id`` marker) that a later evaluator run would accept as a genuine
    Copilot signal. Persistence paths neutralize those synthesized markers
    first; this helper remains the final safety check that no trusted signal
    absent in the original body survives the rewrite.

    Presence alone is insufficient: a comment may already carry one legitimate
    marker while balancing forges a *second* one (e.g. an earlier truncated
    ``<!-- review-id:999`` alongside a valid ``<!-- review-id:123 -->``). A
    later run reading the first regex match would then trust the wrong signal.
    Compare marker *counts* and the complete ordered list of matches — for the
    ``review-id`` marker as well as the variable-content ``copilot-trigger``
    dedup marker, ``repair-dispatch`` dedup marker, and
    ``agdt:conflict-repair`` dispatch marker — so any newly synthesized trusted
    signal blocks persistence.
    """
    for marker in _SYNTHESIZABLE_CONTROL_MARKERS:
        if sanitized.count(marker) > original.count(marker):
            return True
    for pattern in _SYNTHESIZABLE_CONTROL_MARKER_PATTERNS:
        if pattern.findall(sanitized) != pattern.findall(original):
            return True
    return False


def _get_latest_copilot_issue_comment(comments: list[IssueCommentInfo]) -> IssueCommentInfo | None:
    """Return the newest Copilot-authored issue comment from *comments*."""
    copilot_comments = [comment for comment in comments if comment.author in COPILOT_COMMENT_LOGINS]
    if not copilot_comments:
        return None
    return max(copilot_comments, key=lambda comment: (comment.created_at, comment.id))


def _has_evaluator_sentinel_comment(
    provider: CIPlatformProvider,
    pr_number: int,
    current_head_sha: str,
    comments: list | None = None,
) -> bool:
    """Return True when any issue comment is an evaluator-synthesized sentinel for the current HEAD.

    Evaluator-synthesized sentinels (from ``synthesize_sentinel()`` / ``verify_and_resolve()``)
    are posted via ``provider.post_comment()`` using the workflow token rather than a Copilot
    login, so they are not captured by ``_get_latest_agent_comment()``.  Scope the check to
    ``current_head_sha`` (first 8 chars) to avoid false positives from older cycle sentinels
    on the same PR.
    """
    if not current_head_sha:
        return False
    head_sha_short = current_head_sha[:8]
    if comments is None:
        list_issue_comments = getattr(provider, "list_issue_comments", None)
        if not callable(list_issue_comments):
            return False
        try:
            comments = list_issue_comments(pr_number)
        except Exception as exc:
            logger.warning("Failed to fetch issue comments for evaluator sentinel check on PR #%d: %s", pr_number, exc)
            return False
    return any(_SENTINEL_MARKER in c.body and head_sha_short in c.body for c in comments)


def build_snapshot(
    provider: CIPlatformProvider,
    pr_number: int,
    repo: str,
    *,
    current_lock_token: str | None = None,
    persist_sanitized_comment: bool = False,
) -> PostAgentSnapshot:
    """Build an immutable snapshot of the PR state for classification.

    Gathers all data needed by ``classify_post_agent_state()`` using
    provider methods. This function performs I/O (via the provider) but
    produces an immutable result suitable for pure classification.

    Args:
        provider: CI platform provider.
        pr_number: Pull request number.
        repo: Full repository name (owner/repo).
        current_lock_token: Lock token held by the current evaluator run, if any.
        persist_sanitized_comment: When True, best-effort patch a sanitized
            Copilot issue comment back to the provider.

    Returns:
        Frozen PostAgentSnapshot with all relevant PR state.
    """
    # 1. Get PR metadata for HEAD SHA
    pr_meta = provider.get_pr_metadata(pr_number)
    current_head_sha = pr_meta.head_sha

    # 2. Get reviews to find the latest Copilot review
    reviews = provider.list_reviews(pr_number)
    copilot_reviews = [r for r in reviews if is_copilot_login(r.user)]
    # Sort by ID descending to get the latest
    copilot_reviews.sort(key=lambda r: r.id, reverse=True)

    review_id = 0
    review_commit_sha = ""
    if copilot_reviews:
        latest_review = copilot_reviews[0]
        review_id = latest_review.id
        review_commit_sha = latest_review.commit_sha

    # 3. Determine if HEAD changed since the review
    head_changed = bool(review_commit_sha and current_head_sha and review_commit_sha != current_head_sha)

    def _load_review_threads(target_review_id: int) -> list[ThreadInfo]:
        loaded_threads: list[ThreadInfo] = []
        try:
            thread_statuses: dict[int, tuple[bool, bool]] = {}
            try:
                thread_statuses = _get_review_thread_statuses(provider, pr_number)
            except Exception:
                logger.warning("Failed to fetch review thread statuses for PR #%d", pr_number)

            review_comments = provider.list_review_comments(pr_number, target_review_id)
            for rc in review_comments:
                # Skip synthetic review-body entries — they have no real GitHub
                # thread and must not be used for thread-resolution lookup.
                if rc.id < 0:
                    continue
                is_resolved, has_reply = thread_statuses.get(rc.id, (False, False))
                loaded_threads.append(
                    ThreadInfo(
                        comment_id=rc.id,
                        path=rc.path,
                        start_line=rc.start_line,
                        end_line=rc.end_line,
                        is_resolved=is_resolved,
                        has_reply=has_reply,
                        body=rc.body,
                    )
                )
        except Exception as exc:
            logger.warning("Failed to fetch review comments for review %d: %s", target_review_id, exc)
        return loaded_threads

    # 4. Get review threads (comments from the review)
    threads: list[ThreadInfo] = []
    if review_id:
        threads = _load_review_threads(review_id)

    # 5. Find latest Copilot agent comment (issue comment, not review comment)
    list_issue_comments = getattr(provider, "list_issue_comments", None)
    issue_comments: list = []
    if callable(list_issue_comments):
        try:
            issue_comments = list_issue_comments(pr_number)
        except Exception as exc:
            logger.warning("Failed to fetch issue comments for PR #%d: %s", pr_number, exc)

    latest_agent_comment = _get_latest_agent_comment(
        provider,
        pr_number,
        comments=issue_comments,
        persist_sanitized_body=persist_sanitized_comment,
    )
    latest_agent_issue_comment = _get_latest_copilot_issue_comment(issue_comments)

    head_sha_short = current_head_sha[:8] if current_head_sha else ""

    # Sentinel is present if:
    # (a) the latest Copilot comment contains the marker and is scoped to the current
    #     HEAD (avoids treating stale prior-cycle sentinels as current completion), or
    # (b) any issue comment contains an evaluator-synthesized sentinel scoped to the
    #     current HEAD (posted via provider.post_comment() by the workflow token, not
    #     a Copilot login, so not captured by _get_latest_agent_comment()).
    has_sentinel = bool(
        (
            latest_agent_issue_comment is not None
            and _SENTINEL_MARKER in latest_agent_issue_comment.body
            and bool(head_sha_short)
            and head_sha_short in latest_agent_issue_comment.body
        )
        or _has_evaluator_sentinel_comment(provider, pr_number, current_head_sha, comments=issue_comments)
    )

    # 6. Check lock status
    lock_status = check_lock_status(provider, pr_number)

    # 7. Get PR diff (prefer post-review range diff when available)
    diff_text = ""
    try:
        if review_commit_sha and head_changed:
            diff_text = provider.get_commit_range_diff(review_commit_sha, current_head_sha)
        else:
            diff_text = provider.get_pr_diff(pr_number)
    except (NotImplementedError, Exception):
        logger.debug("PR diff unavailable for PR #%d", pr_number)

    lock_holder = lock_status.holder if lock_status.is_locked and not lock_status.is_stale else ""
    if current_lock_token and lock_holder == current_lock_token:
        lock_holder = ""

    # 8. Detect repair-satisfied marker in Copilot-authored issue comments
    repair_satisfied_review_id = find_repair_satisfied_review_id(issue_comments)
    has_repair_satisfied_marker = repair_satisfied_review_id is not None

    # If active Copilot review cannot be derived from list_reviews(), fall back to the
    # review-id encoded in the repair-satisfied marker so thread state can still be loaded.
    if not review_id and repair_satisfied_review_id:
        review_id = repair_satisfied_review_id
        threads = _load_review_threads(review_id)

    return PostAgentSnapshot(
        pr_number=pr_number,
        repo=repo,
        has_sentinel=has_sentinel,
        head_changed_since_review=head_changed,
        threads=tuple(threads),
        latest_agent_comment=latest_agent_comment,
        review_id=review_id,
        review_commit_sha=review_commit_sha,
        current_head_sha=current_head_sha,
        lock_holder=lock_holder,
        lock_age_seconds=lock_status.age_seconds,
        diff_text=diff_text,
        has_repair_satisfied_marker=has_repair_satisfied_marker,
        repair_satisfied_review_id=repair_satisfied_review_id,
    )
