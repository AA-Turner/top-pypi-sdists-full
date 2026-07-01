"""
CVC channel-aware markdown formatting.

Pure functions, no I/O, no platform-specific imports. Each helper takes
a string of agent-emitted markdown and returns a string formatted for
a specific channel (Telegram MarkdownV2, Discord/Slack/Markdown-elsewhere,
or plain text).

The goal is to match the Hermes-level user experience: tables become
Telegram-friendly row groups, code stays code, links are real links,
and the user's eye can scan the response instead of fighting the
renderer.

Why not use a single markdown library for all platforms?
  - Telegram has MarkdownV2 which is strict about escaping ~80
    special characters.
  - Discord/Slack use a CommonMark-ish subset that doesn't support
    tables natively.
  - WhatsApp uses a tiny subset (bold/italic/strike/code/blockquote).
  - Some channels need plain text (Signal voice transcripts, basic
    email).

Each helper documents the subset it supports and falls back gracefully.
"""

from __future__ import annotations

import re
from typing import List


# ─────────────────────────────────────────────────────────────────────────────
# Telegram MarkdownV2 helpers
# ─────────────────────────────────────────────────────────────────────────────

# Characters that MUST be escaped outside of pre/code blocks in MDv2.
# Order matches the Telegram docs and the Hermes vendored implementation.
_MDV2_SPECIAL = r"_*[]()~`>#+-=|{}.!\\"
_MDV2_ESCAPE_RE = re.compile(r"([" + re.escape(_MDV2_SPECIAL) + r"])")


def escape_mdv2(text: str) -> str:
    """Escape a plain string for safe inclusion in Telegram MarkdownV2.

    Pre/code blocks are NOT escaped — callers must keep them on their own
    lines and pass them through unchanged.
    """
    return _MDV2_ESCAPE_RE.sub(r"\\\1", text)


def strip_mdv2(text: str) -> str:
    """Inverse of :func:`escape_mdv2` — used when sending to a non-MDv2
    backend (HTML fallback, plain text). Strips the escape backslashes."""
    return re.sub(r"\\([_*[\]()~`>#+\-=|{}.!\\])", r"\1", text)


# ─────────────────────────────────────────────────────────────────────────────
# GFM table detection + rewrite
# ─────────────────────────────────────────────────────────────────────────────

_TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


def _is_table_row(line: str) -> bool:
    """True if *line* could plausibly be a GFM table row.

    A table row has at least one `|` and is non-empty. We don't try to be
    strict here — the separator check below is what actually proves it's
    a table.
    """
    return "|" in line and line.strip() != ""


def _split_table_row(line: str) -> List[str]:
    """Split a simple GFM table row into stripped cell values."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _render_table_block_as_row_groups(rows: List[str]) -> str:
    """Render a contiguous block of table rows as a Telegram-friendly
    bulleted "row groups" list. One bullet per data row, cells inline
    with ` · ` separators.

    Telegram MarkdownV2 doesn't render GFM tables natively; users see
    raw `| ... |` which looks broken. This rewrite produces the same
    information in a form that ANY renderer (Telegram, WhatsApp,
    Signal, plain SMS, email) can display legibly.
    """
    parsed: List[List[str]] = []
    for r in rows:
        cells = _split_table_row(r)
        if cells:
            parsed.append(cells)

    if len(parsed) < 2:
        # Not actually a table — return the raw lines back.
        return "\n".join(rows)

    header = parsed[0]
    body = parsed[2:] if len(parsed) >= 3 and _TABLE_SEPARATOR_RE.match(rows[1]) else parsed[1:]
    out: List[str] = []
    for row in body:
        if len(row) == len(header):
            bits = [f"*{header[i]}*: {row[i]}" for i in range(len(row))]
            out.append("• " + " · ".join(bits))
        else:
            # Mismatched column count — degrade gracefully.
            out.append("• " + " · ".join(row))
    return "\n".join(out)


def wrap_markdown_tables(text: str) -> str:
    """Detect GFM-style pipe tables and rewrite them as row-group bullets.

    The transformation is idempotent: re-running it on already-rewritten
    text is a no-op because the bullet rows no longer contain `|`.
    """
    lines = text.split("\n")
    out: List[str] = []
    i = 0
    while i < len(lines):
        if (
            _is_table_row(lines[i])
            and i + 1 < len(lines)
            and _TABLE_SEPARATOR_RE.match(lines[i + 1])
        ):
            block = [lines[i], lines[i + 1]]
            j = i + 2
            while j < len(lines) and _is_table_row(lines[j]):
                block.append(lines[j])
                j += 1
            out.append(_render_table_block_as_row_groups(block))
            i = j
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


# ─────────────────────────────────────────────────────────────────────────────
# Telegram message splitting
# ─────────────────────────────────────────────────────────────────────────────

# Telegram caps messages at 4096 chars total; we leave headroom for safety.
_TELEGRAM_MAX = 4000


def split_message(text: str, limit: int = _TELEGRAM_MAX) -> List[str]:
    """Split *text* into ≤ *limit*-char chunks, preferring paragraph
    boundaries, then newlines, then spaces.

    The split logic mirrors the Hermes vendored telegram.py split_message
    so that users who migrate from Hermes to CVC see the same chunking
    behavior.
    """
    if len(text) <= limit:
        return [text]

    chunks: List[str] = []
    remaining = text
    while len(remaining) > limit:
        # Try to split at the last double-newline before the limit.
        window = remaining[:limit]
        split_at = window.rfind("\n\n")
        if split_at < limit // 2:
            split_at = window.rfind("\n")
        if split_at < limit // 2:
            split_at = window.rfind(" ")
        if split_at < limit // 4:
            split_at = limit  # Hard cut.
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# Channel-agnostic markdown → plain text (for WhatsApp / SMS / voice)
# ─────────────────────────────────────────────────────────────────────────────

_FENCE_RE = re.compile(r"```[a-zA-Z0-9_+\-]*\n(.*?)```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)")
_STRIKE_RE = re.compile(r"~~([^~]+)~~")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
_BLOCKQUOTE_RE = re.compile(r"^>\s?", re.MULTILINE)


def markdown_to_plain(text: str) -> str:
    """Convert agent markdown to a plain-text approximation.

    Used for channels that don't render markdown at all (Signal,
    WhatsApp text-only mode, SMS, voice transcripts). Strips code
    fences (replaces with the code body), removes bold/italic markers,
    unwraps links to "label (url)", strips heading hashes and
    blockquote markers.
    """
    # Code fences first so we don't strip their backticks.
    text = _FENCE_RE.sub(lambda m: m.group(1).strip(), text)
    text = _INLINE_CODE_RE.sub(r"\1", text)
    text = _BOLD_RE.sub(r"\1\2", text)
    text = _ITALIC_RE.sub(r"\1\2", text)
    text = _STRIKE_RE.sub(r"\1", text)
    text = _LINK_RE.sub(r"\1 (\2)", text)
    text = _HEADING_RE.sub("", text)
    text = _BLOCKQUOTE_RE.sub("", text)
    return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# Agent markdown → Telegram MarkdownV2
# ─────────────────────────────────────────────────────────────────────────────
#
# This is the canonical bridge between what the LLM produces (common
# markdown: **bold**, __italic__, `code`, [label](url), # heading)
# and what Telegram's MarkdownV2 parser accepts (different syntax for
# every inline element, plus mandatory escaping of ~20 special chars
# outside of code/pre blocks).
#
# Strategy: stash the code/pre blocks first, transform the rest into
# MDv2 syntax, then escape any remaining special chars. Finally,
# restore the stashed blocks verbatim — Telegram handles escaping
# inside ``` ``` itself, and we MUST NOT touch the contents.
#
# This is the missing function that ``cvc/integrations/channels/telegram.py``
# has been importing since v3.4 — without it the entire adapter
# fails to load, the channel never registers with the gateway,
# and Telegram "stops responding" silently. Adding it here fixes
# the root cause; the streaming/persona/emoji work in the rest of
# the codebase can finally execute against a live Telegram adapter.

_MDV2_SPECIAL = re.compile(r"([_*\[\]()~`>#+\-=|{}.!\\])")  # type: ignore[assignment]

# These are MDv2 *syntax* markers, not text that needs escaping.
# After we transform `**bold**` → `*bold*`, those `*` are syntax
# and must NOT be escaped. The escape pass below knows about this set.
_MDV2_MARKER_CHARS = set("*~_|`")


def markdown_to_mdv2(text: str) -> str:
    """Convert agent markdown to Telegram MarkdownV2.

    Handles inline formatting transforms (``**bold**`` → ``*bold*``,
    ``__italic__`` → ``_italic_``, ``~~strike~~`` → ``~strike~``,
    ``[label](url)`` → ``[label](url)`` with chars escaped, ``# h``
    → ``*h*``, ``> q`` → ``|q|`` style blockquote), preserves code
    blocks verbatim (Telegram handles their internals), and escapes
    the remaining MDv2-special characters in non-code regions.
    """
    if not text:
        return ""

    # ── 1. Stash fenced code blocks (``` ... ```) ──────────────────
    # Use a sentinel that cannot appear in normal text so the regex
    # replacement is unambiguous.
    fences: List[str] = []

    def _stash_fence(m: "re.Match[str]") -> str:
        fences.append(m.group(0))
        return f"\x00FENCE{len(fences) - 1}\x00"

    text = _FENCE_RE.sub(_stash_fence, text)

    # ── 2. Stash inline code spans (`code`) ────────────────────────
    inline_codes: List[str] = []

    def _stash_inline(m: "re.Match[str]") -> str:
        inline_codes.append(m.group(1))
        return f"\x00CODE{len(inline_codes) - 1}\x00"

    text = _INLINE_CODE_RE.sub(_stash_inline, text)

    # ── 3. Escape MDv2-special chars FIRST ─────────────────────────
    # We escape before transforming so that, e.g., a literal `_` in
    # the input becomes `\_`, and the italic transform later sees
    # `\_` + body + `\_` which is unambiguous. This is the standard
    # "escape early, transform late" pattern.
    text = _MDV2_SPECIAL.sub(r"\\\1", text)  # type: ignore[attr-defined]

    # ── 4. Inline formatting transforms ────────────────────────────
    # Bold: **x** or __x__  →  *x* (MDv2 uses single * for bold).
    # After escape, the surrounding markers are `\*\*` / `\_\_`; we
    # match those and replace with a SINGLE raw `*` pair.
    text = re.sub(r"\\\*\\\*(.+?)\\\*\\\*", r"*\1*", text, flags=re.DOTALL)
    text = re.sub(r"\\_\\_(.+?)\\_\\_", r"*\1*", text, flags=re.DOTALL)
    # Italic: \*x\* or \_x\_  →  _x_  (MDv2 uses _).
    text = re.sub(r"\\\*([^\\\*]+)\\\*", r"_\1_", text)
    text = re.sub(r"\\_([^\\\\_]+)\\_", r"_\1_", text)
    # Strikethrough: \~\~x\~\~  →  ~x~  (MDv2 uses single ~).
    text = re.sub(r"\\~\\~(.+?)\\~\\~", r"~\1~", text, flags=re.DOTALL)
    # Headings: \# h  →  *h*  (MDv2 doesn't render `#`; bold is the
    # closest equivalent and looks right for short titles).
    text = re.sub(r"\\#\s+", "*", text)
    # Blockquotes: \> q  →  |q  (MDv2 has no blockquote; pipe is
    # the conventional Telegram substitute).
    text = re.sub(r"\\>\s?", "| ", text)
    # Links: \[label\]\(url\)  →  [label](url) — keep the brackets/
    # parens as syntax markers; the inside is already escaped. We
    # strip the backslashes from the delimiting chars so Telegram
    # parses them as link syntax, not escaped chars. URL chars
    # inside the parens are unescaped because Telegram doesn't
    # apply MDv2 escaping to the URL portion of a link (URLs are
    # taken as-is).
    def _link_sub(m: "re.Match[str]") -> str:
        label = m.group(1)
        url = re.sub(r"\\(.)", r"\1", m.group(2))  # unescape URL
        return f"[{label}]({url})"

    text = re.sub(
        r"\\\[(.+?)\\\]\\\((.+?)\\\)",
        _link_sub,
        text,
        flags=re.DOTALL,
    )

    # ── 5. Restore stashed code blocks verbatim ────────────────────
    # Telegram expects the surrounding ``` ... ``` to be intact and
    # the contents UNESCAPED. Re-stitch them.
    for i, block in enumerate(fences):
        text = text.replace(f"\x00FENCE{i}\x00", block)
    for i, code in enumerate(inline_codes):
        text = text.replace(f"\x00CODE{i}\x00", f"`{code}`")

    return text
