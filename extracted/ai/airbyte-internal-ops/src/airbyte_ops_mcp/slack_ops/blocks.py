# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack Block Kit construction and validation utilities.

This module converts Slack mrkdwn text into Block Kit blocks and validates
them using `slack_sdk.models.blocks`.  It runs **locally** on the agent's
machine — the GitHub Actions workflow only receives the finished blocks JSON.

Public API:
    - `validate_message` — reject illegal markdown patterns
    - `build_blocks` — convert mrkdwn text to Block Kit blocks
"""

from __future__ import annotations

import re

from slack_sdk.models.blocks import HeaderBlock, SectionBlock
from slack_sdk.models.blocks.basic_components import (
    MarkdownTextObject,
    PlainTextObject,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
_H3_RE = re.compile(r"^###\s+(.+)$", re.MULTILINE)
_MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
_BULLET_RE = re.compile(r"^[-*] ", re.MULTILINE)

# Inline mrkdwn patterns for rich-text element parsing.
# Groups: (1) bold  (2) italic  (3) strikethrough  (4) slack link  (5) inline code
_INLINE_RE = re.compile(
    r"(\*[^*]+\*)"  # bold: *text*
    r"|(_[^_]+_)"  # italic: _text_
    r"|(~[^~]+~)"  # strikethrough: ~text~
    r"|(<[^|>]+(?:\|[^>]*)?>)"  # slack link: <url|text> or <url>
    r"|(`[^`]+`)"  # inline code: `text`
)

_MAX_BLOCKS = 50
_MAX_SECTION_CHARS = 3000
_MAX_HEADER_CHARS = 150

# Patterns that Slack cannot render properly.
# Each entry is (compiled regex, human-readable description).
_ILLEGAL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"^\|.*\|\s*\n\|[\s:|-]+\|",
            re.MULTILINE,
        ),
        "Markdown table (pipe-delimited rows with a separator line)",
    ),
]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_message(message_text: str) -> None:
    """Reject message text that contains Slack-incompatible markdown.

    Raises `ValueError` with a descriptive message listing every
    illegal pattern found so the calling agent can fix them all at once.
    """
    violations: list[str] = []
    for pattern, description in _ILLEGAL_PATTERNS:
        if pattern.search(message_text):
            violations.append(description)

    if violations:
        bullet_list = "\n".join(f"  - {v}" for v in violations)
        raise ValueError(
            "Message contains markdown that Slack cannot render:\n"
            f"{bullet_list}\n"
            "Rewrite the message using only Slack mrkdwn formatting "
            "(*bold*, _italic_, `code`, lists, links) before retrying."
        )


# ---------------------------------------------------------------------------
# Rich-text helpers
# ---------------------------------------------------------------------------

_BULLET_MARKER = "\u2022 "


def _parse_mrkdwn_inline(text: str) -> list[dict]:
    """Parse Slack mrkdwn inline formatting into rich_text elements.

    Handles `*bold*`, `_italic_`, `~strikethrough~`, `<url|label>` links,
    and `code`.  Everything else is returned as plain text elements.
    """
    elements: list[dict] = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        # Plain text before this match
        if m.start() > pos:
            elements.append({"type": "text", "text": text[pos : m.start()]})

        if m.group(1):  # bold
            inner = m.group(1)[1:-1]
            elements.append({"type": "text", "text": inner, "style": {"bold": True}})
        elif m.group(2):  # italic
            inner = m.group(2)[1:-1]
            elements.append({"type": "text", "text": inner, "style": {"italic": True}})
        elif m.group(3):  # strikethrough
            inner = m.group(3)[1:-1]
            elements.append({"type": "text", "text": inner, "style": {"strike": True}})
        elif m.group(4):  # link
            raw = m.group(4)[1:-1]  # strip < >
            if "|" in raw:
                url, label = raw.split("|", 1)
                elements.append({"type": "link", "url": url, "text": label})
            else:
                elements.append({"type": "link", "url": raw})
        elif m.group(5):  # code
            inner = m.group(5)[1:-1]
            elements.append({"type": "text", "text": inner, "style": {"code": True}})

        pos = m.end()

    # Remaining plain text
    if pos < len(text):
        elements.append({"type": "text", "text": text[pos:]})

    return elements or [{"type": "text", "text": text}]


def _build_rich_text_list_block(bullet_lines: list[str]) -> dict:
    """Build a `rich_text` block containing a bullet list.

    Each *bullet_line* should start with the `_BULLET_MARKER` prefix
    (Unicode bullet + space).  The prefix is stripped before parsing
    inline formatting.

    Using `rich_text` with `rich_text_list` gives Slack-native bullet
    rendering where wrapped lines are indented past the bullet character.
    """
    items: list[dict] = []
    for line in bullet_lines:
        content = (
            line[len(_BULLET_MARKER) :] if line.startswith(_BULLET_MARKER) else line
        )
        items.append(
            {
                "type": "rich_text_section",
                "elements": _parse_mrkdwn_inline(content),
            }
        )
    return {
        "type": "rich_text",
        "elements": [
            {
                "type": "rich_text_list",
                "style": "bullet",
                "elements": items,
            }
        ],
    }


def _emit_section_blocks(section: str, blocks: list[dict]) -> None:
    """Split *section* into runs of bullet / non-bullet lines.

    Non-bullet runs are emitted as `section` blocks (mrkdwn).
    Bullet runs are emitted as `rich_text` blocks with `rich_text_list`.
    """
    lines = section.split("\n")
    buf_text: list[str] = []
    buf_bullets: list[str] = []

    def flush_text() -> None:
        if buf_text:
            joined = "\n".join(buf_text)
            blocks.append(
                SectionBlock(
                    text=MarkdownTextObject(text=joined[:_MAX_SECTION_CHARS])
                ).to_dict()
            )
            buf_text.clear()

    def flush_bullets() -> None:
        if buf_bullets:
            blocks.append(_build_rich_text_list_block(list(buf_bullets)))
            buf_bullets.clear()

    for line in lines:
        if line.startswith(_BULLET_MARKER):
            flush_text()
            buf_bullets.append(line)
        else:
            flush_bullets()
            buf_text.append(line)

    flush_text()
    flush_bullets()


# ---------------------------------------------------------------------------
# Block building
# ---------------------------------------------------------------------------


def build_blocks(message_text: str) -> list[dict]:
    """Convert markdown-style text into validated Slack Block Kit blocks.

    Handles the following translations:

    - `[text](url)` -> Slack mrkdwn link (`<url|text>`)
    - `## Heading` -> Block Kit `header` block (large title, plain text)
    - `### Subheading` -> Bold mrkdwn text (`*Subheading*`) in a section
    - `- item` / `* item` -> `rich_text` bullet list with proper
      indentation (wrapped lines align past the bullet character)
    - Double newlines split remaining text into separate visual blocks
    - Each mrkdwn section is capped at 3 000 characters (Slack limit)
    - Total blocks are capped at 50 (Slack limit)

    Non-bullet text is rendered in `section` blocks (Slack mrkdwn).
    Bullet lists are rendered in `rich_text` blocks so Slack indents
    wrapped lines past the bullet character.

    Returns:
        A list of Block Kit block dicts ready for `chat.postMessage`.
    """
    # Translate markdown links to Slack mrkdwn links
    text = _MD_LINK_RE.sub(r"<\2|\1>", message_text)

    # Translate ### headings into bold mrkdwn inline
    text = _H3_RE.sub(r"*\1*", text)

    # Normalise markdown-style bullets (- / *) to a Unicode bullet marker
    text = _BULLET_RE.sub(_BULLET_MARKER, text)

    blocks: list[dict] = []
    for chunk in re.split(r"(^##\s+.+$)", text, flags=re.MULTILINE):
        chunk = chunk.strip()
        if not chunk:
            continue

        h2_match = _H2_RE.match(chunk)
        if h2_match:
            header_text = h2_match.group(1).strip()[:_MAX_HEADER_CHARS]
            blocks.append(
                HeaderBlock(
                    text=PlainTextObject(text=header_text, emoji=True)
                ).to_dict()
            )
            continue

        for section in chunk.split("\n\n"):
            section = section.strip()
            if not section:
                continue
            _emit_section_blocks(section, blocks)

    # Enforce the 50-block Slack maximum
    return blocks[:_MAX_BLOCKS]
