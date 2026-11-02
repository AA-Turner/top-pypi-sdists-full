"""Snapshot utilities for Markdown-aware comment processing."""

from __future__ import annotations

from .snapshot_markdown_blocks import (
    _ATX_HEADING_RE,
    _HTML_BLOCK_INTERRUPT_NAMES,
    _HTML_BLOCK_TAG_START_RE,
    _LIST_ITEM_RE,
    _advance_column,
    _interrupts_paragraph_with_list_item,
    _list_item_content_indent,
    _strip_list_item_prefix_for_block_detection,
)


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
