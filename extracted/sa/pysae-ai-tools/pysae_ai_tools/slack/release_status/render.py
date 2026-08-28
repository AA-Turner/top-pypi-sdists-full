"""Pure rendering of a :class:`ReleaseState` into Slack Block Kit / plain text.

Every function here is a pure function of the state (plus the reply/chunk
helpers used for long bodies) — no Slack call, no I/O — so the message layout
and the chunking logic are testable without mocking any transport.
"""

from ...common.project_config import Track
from .state import FAILED, TRACK_ORDER, TRACKS, ReleaseState

REPLY_BLOCK_MAX = 2900
"""Max chars per thread-reply section block. Slack caps a section's mrkdwn text at
3000; a reply longer than this (a long changelog) is split into several section
blocks at line boundaries so nothing is silently truncated."""


def _state_label(track: str, state_key: str) -> str:
    """French label for a (track, state) pair; the key itself for unknowns."""
    if state_key == FAILED:
        return "Échec"
    for key, label in TRACKS[track]:
        if key == state_key:
            return label
    return state_key


def _state_icon(track: str, state_key: str) -> str:
    """:white_check_mark: terminal, :x: failure, :white_circle: pending (not started), else :hourglass_flowing_sand:."""
    if state_key == FAILED:
        return ":x:"
    if TRACKS[track] and TRACKS[track][-1][0] == state_key:
        return ":white_check_mark:"
    if state_key == "pending":
        return ":white_circle:"
    return ":hourglass_flowing_sand:"


def render_track_line(track: str, state_key: str) -> str:
    """One mrkdwn status line: ``<icon> <emoji> *Track* — Label``."""
    t = Track(track)
    return f"{_state_icon(track, state_key)} {t.emoji} *{t.label}* — {_state_label(track, state_key)}"


def render_blocks(state: ReleaseState) -> list[dict[str, object]]:
    """Render the message blocks: header + present track lines, then the changelog."""
    lines = [f":rocket: *{state.app} — {state.version}*"]
    track_lines = [render_track_line(t, state.tracks[t]) for t in TRACK_ORDER if t in state.tracks]
    if track_lines:
        lines.append("")
        lines.extend(track_lines)
    blocks: list[dict[str, object]] = [{"type": "section", "text": {"type": "mrkdwn", "text": "\n".join(lines)}}]
    if state.content:
        blocks.append({"type": "divider"})
        # Split across several section blocks (Slack caps a section's mrkdwn at 3000)
        # so long notes / changelog render in full instead of being truncated.
        blocks.extend(_reply_blocks(state.content))
    return blocks


def content_from_blocks(blocks: object) -> str:
    """Read ``state.content`` back out of a rendered message — inverse of :func:`render_blocks`.

    The message is the single source of truth for its own body: the notes live in the
    section blocks that follow the divider, so they never have to be duplicated into the
    Slack metadata (whose payload Slack silently discards past
    :data:`..state.METADATA_PAYLOAD_SAFE_BYTES`, orphaning the message).

    Rejoining the chunks restores the text ``render_blocks`` was given, save for a single
    line longer than :data:`REPLY_BLOCK_MAX` that :func:`_split_chunks` had to hard-split.
    Returns ``""`` for a message with no content section (or unreadable blocks).
    """
    if not isinstance(blocks, list):
        return ""
    chunks: list[str] = []
    past_divider = False
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "divider":
            past_divider = True
            continue
        if not past_divider or block.get("type") != "section":
            continue
        text = block.get("text")
        if isinstance(text, dict) and isinstance(text.get("text"), str):
            chunks.append(text["text"])
    return "\n".join(chunks)


def render_text(state: ReleaseState) -> str:
    """Plain-text fallback (notification + the metadata-less searchable summary)."""
    parts = [f"{state.app} {state.version}"]
    summary = [f"{Track(t).label}: {_state_label(t, state.tracks[t])}" for t in TRACK_ORDER if t in state.tracks]
    if summary:
        parts.append(" — " + "; ".join(summary))
    return "".join(parts)


def _split_chunks(text: str, limit: int) -> list[str]:
    """Split ``text`` into chunks of at most ``limit`` chars, preferring line breaks.

    Lines are accumulated until the next one would overflow ``limit``, then a new
    chunk starts. A single line longer than ``limit`` (rare — a giant URL) is
    hard-split. Always returns at least one (possibly empty) chunk.
    """
    chunks: list[str] = []
    cur = ""
    for line in text.split("\n"):
        while len(line) > limit:
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(line[:limit])
            line = line[limit:]
        candidate = line if not cur else f"{cur}\n{line}"
        if len(candidate) > limit and cur:
            chunks.append(cur)
            cur = line
        else:
            cur = candidate
    if cur:
        chunks.append(cur)
    return chunks or [""]


def _reply_blocks(text: str) -> list[dict[str, object]]:
    """Render a thread-reply body as one or more Slack section blocks (≤3000 chars each)."""
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": chunk}} for chunk in _split_chunks(text, REPLY_BLOCK_MAX)
    ]
