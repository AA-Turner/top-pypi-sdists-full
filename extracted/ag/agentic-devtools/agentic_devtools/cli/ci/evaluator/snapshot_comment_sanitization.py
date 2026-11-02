"""Balance unterminated HTML comments without altering Markdown code."""

from __future__ import annotations

from . import snapshot


def _find_outside_code(body: str, mask: list[bool], sub: str, start: int) -> int:
    """Find the next occurrence of ``sub`` that is outside Markdown code."""
    idx = body.find(sub, start)
    while idx != -1 and mask[idx]:
        idx = body.find(sub, idx + 1)
    return idx


def _is_backslash_escaped(body: str, idx: int) -> bool:
    """Return True when ``idx`` follows an odd-length run of backslashes.

    A single backslash escapes the following punctuation character. Two
    backslashes cancel each other, so only odd-length runs escape the marker.
    """
    n = 0
    i = idx - 1
    while i >= 0 and body[i] == "\\":
        n += 1
        i -= 1
    return n % 2 == 1


def _next_comment_insertion(
    body: str,
    mask: list[bool],
    search_from: int,
) -> tuple[int | None, int, bool] | None:
    """Find one comment insertion, the next search offset, and whether scanning is done."""
    open_idx = _find_outside_code(body, mask, "<!--", search_from)
    if open_idx == -1:
        return None
    if _is_backslash_escaped(body, open_idx):
        return None, open_idx + 4, False

    # Markdown code syntax becomes inactive inside an HTML comment, so the first
    # raw closer after the opener is the relevant one, even inside a backtick span.
    close_idx = body.find("-->", open_idx + 4)
    next_open = _find_outside_code(body, mask, "<!--", open_idx + 4)
    if close_idx != -1 and (next_open == -1 or next_open > close_idx):
        return None, close_idx + 3, False

    line_end = body.find("\n", open_idx)
    if next_open != -1 and (line_end == -1 or next_open < line_end):
        return next_open, next_open, False
    if line_end == -1:
        return len(body), len(body), True
    return line_end, line_end + 1, False


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
    mask = snapshot._compute_markdown_code_mask(body)

    insertions: list[int] = []
    search_from = 0
    while True:
        insertion = _next_comment_insertion(body, mask, search_from)
        if insertion is None:
            break
        insertion_idx, search_from, finished = insertion
        if insertion_idx is not None:
            insertions.append(insertion_idx)
        if finished:
            break
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
