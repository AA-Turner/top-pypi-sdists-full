"""Render a markdown release block to a target surface (Slack mrkdwn, plain text).

The source is always markdown — a ``## [tag] date`` heading followed by ``### ``
sub-sections and ``* `` bullets, the exact shape produced by
``code.changelog`` (CHANGELOG.md) and ``code.release_notes``
(docs/release-notes/release-notes.<lang>.md). Each renderer is a pure
``str -> str`` function so new targets can be added without touching the
extraction logic.

Supported renderers (see :data:`RENDERERS`):

- ``markdown`` — identity passthrough (the source is already markdown).
- ``slack`` — Slack mrkdwn: ``## [tag] date`` → ``*tag* date`` (tag linkified
  to ``project_url/-/tags/tag`` when known), ``### Heading`` → ``*Heading*``
  (with a per-section emoji prefix for known sections, see :data:`_SECTION_EMOJI`),
  ``* ``/``- `` bullets → ``• ``, ``[text](url)`` → ``<url|text>``,
  ``**bold**`` → ``*bold*``, and bare ``(#NN)`` issue refs linkified to
  ``project_url/-/issues/NN`` when known. Markdown blockquote lines (``> …``)
  are kept as Slack quote lines (their inner content rendered normally).
- ``txt`` — plain text: heading markers and emphasis stripped, links reduced to
  their text, bullets normalized to ``- ``.
"""

import re
from collections.abc import Callable

_VERSION_HEADING_RE = re.compile(r"^##\s+\[([^\]]+)\]\s*(.*)$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_BULLET_RE = re.compile(r"^(\s*)[*-]\s+")
_QUOTE_RE = re.compile(r"^>\s?(.*)$")
_CONTINUATION_RE = re.compile(r"^\s+\S")  # indented, non-blank → a wrapped continuation line
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_BARE_ISSUE_REF_RE = re.compile(r"\(#(\d+)\)")

_SECTION_EMOJI: dict[str, str] = {
    # Release notes canonical sections (FR / EN / IT).
    "Nouveautés": "✨",
    "What's new": "✨",
    "Novità": "✨",
    "Améliorations": "🚀",
    "Improvements": "🚀",
    "Miglioramenti": "🚀",
    "Corrections": "🐛",
    "Fixes": "🐛",
    "Correzioni": "🐛",
    # Changelog label inserted by ``code release-content`` when both sources show.
    "Changelog": "📝",
}
"""Emoji prefixed before each Slack section heading, keyed by heading text.

The ``⚠️ Important`` / ``⚠️ Importante`` sections already carry their emoji in
the heading text, so they are intentionally absent here (no double emoji).
Headings not in this map are bolded without a prefix.
"""

MAINTENANCE_EMOJI = "🔧"
"""Prefixed before a maintenance-release placeholder line when rendering."""

MAINTENANCE_NOTES: dict[str, str] = {
    "fr": "Version de maintenance — aucun changement visible pour les utilisateurs.",
    "en": "Maintenance release — no user-facing changes.",
    "it": "Versione di manutenzione — nessuna modifica visibile per gli utenti.",
}
"""Placeholder body written when a release has no user-facing change (all changes
technical/excluded). Defined here so the renderers (Slack + GitLab markdown) can
recognise the line and prefix it with :data:`MAINTENANCE_EMOJI`; reused by
``code.release_notes`` as the body it writes."""

_MAINTENANCE_SET = frozenset(MAINTENANCE_NOTES.values())


def _maintenance_prefixed(line: str) -> str | None:
    """Return the maintenance placeholder prefixed with its emoji, or ``None``.

    ``None`` when ``line`` is not a maintenance note (or already prefixed).
    """
    stripped = line.strip()
    if stripped in _MAINTENANCE_SET and not stripped.startswith(MAINTENANCE_EMOJI):
        return f"{MAINTENANCE_EMOJI} {stripped}"
    return None


def unwrap_hard_wraps(md: str) -> str:
    """Join hard-wrapped continuation lines back onto the line they belong to.

    Release notes are hard-wrapped at 120 chars, their continuation lines
    indented to align under the bullet text (see ``code.release_notes``). Slack
    has no fixed column width, so a physical newline mid-bullet renders as an
    ugly break in the middle of an item; each logical item must collapse to a
    single line first. A *continuation* line — one that, after an optional
    ``> `` quote prefix, is indented and is itself neither a bullet nor a
    heading — is merged into the previous output line, its leading indent reduced
    to a single space. The quote prefix is part of a line's identity: a quoted
    line never merges into a non-quoted one (or vice versa), so the changelog
    quote block stays intact.
    """
    out: list[str] = []
    prev_quoted = False
    for raw in md.splitlines():
        quote = _QUOTE_RE.match(raw)
        quoted = quote is not None
        inner = quote.group(1) if quote else raw
        mergeable = (
            bool(out)
            and bool(out[-1].strip())
            and quoted == prev_quoted
            and bool(inner.strip())
            and _CONTINUATION_RE.match(inner) is not None
            and _BULLET_RE.match(inner) is None
            and _HEADING_RE.match(inner.strip()) is None
        )
        if mergeable:
            out[-1] = f"{out[-1].rstrip()} {inner.strip()}"
        else:
            out.append(raw)
            prev_quoted = quoted
    return "\n".join(out)


def _slack_inline(text: str, project_url: str) -> str:
    """Apply Slack inline transforms: links, bold, then bare issue refs.

    Markdown links are converted first so an already-linkified CHANGELOG ref
    (``([#42](url))``) becomes ``(<url|#42>)`` and is *not* re-processed by the
    bare-ref pass below.
    """
    text = _MD_LINK_RE.sub(lambda m: f"<{m.group(2)}|{m.group(1)}>", text)
    text = _BOLD_RE.sub(r"*\1*", text)
    if project_url:
        text = _BARE_ISSUE_REF_RE.sub(
            lambda m: f"(<{project_url}/-/issues/{m.group(1)}|#{m.group(1)}>)",
            text,
        )
    return text


def _slack_line(raw: str, project_url: str) -> str:
    """Render a single non-quoted markdown line as Slack mrkdwn."""
    maintenance = _maintenance_prefixed(raw)
    if maintenance is not None:
        return _slack_inline(maintenance, project_url)
    version = _VERSION_HEADING_RE.match(raw)
    if version:
        tag, rest = version.group(1), version.group(2).strip()
        label = f"<{project_url}/-/tags/{tag}|{tag}>" if project_url else tag
        line = f"*{label}*" + (f" {rest}" if rest else "")
        return _slack_inline(line, project_url)
    heading = _HEADING_RE.match(raw)
    if heading:
        text = heading.group(2).strip()
        emoji = _SECTION_EMOJI.get(text)
        label = f"{emoji} {text}" if emoji else text
        return _slack_inline(f"*{label}*", project_url)
    bullet = _BULLET_RE.match(raw)
    if bullet:
        raw = _BULLET_RE.sub(f"{bullet.group(1)}• ", raw)
    return _slack_inline(raw, project_url)


def render_slack(md: str, project_url: str = "") -> str:
    """Render a markdown release block as Slack mrkdwn. See module docstring.

    Markdown blockquote lines (``> …``) are preserved as Slack quote lines —
    their inner content is rendered normally (bullets → ``•``, links, refs) and
    re-prefixed with ``> ``. This is what turns the changelog block assembled by
    ``code release-content`` into a Slack quote block.

    Hard-wrapped continuation lines (120-char release-notes wrapping) are first
    collapsed back into their item via :func:`unwrap_hard_wraps` so Slack — which
    has no fixed width — never breaks in the middle of a bullet.
    """
    if not md:
        return md
    md = unwrap_hard_wraps(md)
    out: list[str] = []
    for raw in md.splitlines():
        quote = _QUOTE_RE.match(raw)
        if quote:
            inner = quote.group(1)
            out.append(f"> {_slack_line(inner, project_url)}" if inner else ">")
        else:
            out.append(_slack_line(raw, project_url))
    return "\n".join(out)


def prefix_section_emoji(md: str) -> str:
    """Prefix known section headings with their emoji, keeping markdown intact.

    Same per-section emojis as the Slack renderer (``### Nouveautés`` →
    ``### ✨ Nouveautés``, ``### Changelog`` → ``### 📝 Changelog``), but the
    markdown structure (``###``, bullets, blockquotes) is preserved — so a GitLab
    release description carries the same pictograms as the Slack message. Headings
    inside a blockquote (the quoted changelog) are handled too. Idempotent: a
    heading that already starts with its emoji is left as-is.
    """
    if not md:
        return md
    out: list[str] = []
    for raw in md.splitlines():
        quote = _QUOTE_RE.match(raw)
        inner = quote.group(1) if quote else raw
        heading = _HEADING_RE.match(inner)
        if heading:
            hashes, text = heading.group(1), heading.group(2).strip()
            emoji = _SECTION_EMOJI.get(text)
            if emoji and not text.startswith(emoji):
                inner = f"{hashes} {emoji} {text}"
                raw = f"> {inner}" if quote else inner
        else:
            maintenance = _maintenance_prefixed(inner)
            if maintenance is not None:
                raw = f"> {maintenance}" if quote else maintenance
        out.append(raw)
    return "\n".join(out)


def _txt_inline(text: str) -> str:
    """Strip markdown emphasis and reduce links to their visible text."""
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _BOLD_RE.sub(r"\1", text)
    return text


def _txt_line(raw: str) -> str:
    """Render a single non-quoted markdown line as plain text."""
    version = _VERSION_HEADING_RE.match(raw)
    if version:
        tag, rest = version.group(1), version.group(2).strip()
        return f"{tag} {rest}".rstrip()
    heading = _HEADING_RE.match(raw)
    if heading:
        return _txt_inline(heading.group(2).strip())
    bullet = _BULLET_RE.match(raw)
    if bullet:
        raw = _BULLET_RE.sub(f"{bullet.group(1)}- ", raw)
    return _txt_inline(raw)


def render_txt(md: str, project_url: str = "") -> str:
    """Render a markdown release block as plain text. ``project_url`` is ignored.

    Blockquote lines (``> …``) keep their ``> `` prefix — a common plain-text
    quoting convention — with the inner content rendered normally.
    """
    if not md:
        return md
    out: list[str] = []
    for raw in md.splitlines():
        quote = _QUOTE_RE.match(raw)
        if quote:
            inner = quote.group(1)
            out.append(f"> {_txt_line(inner)}" if inner else ">")
        else:
            out.append(_txt_line(raw))
    return "\n".join(out)


def render_markdown(md: str, project_url: str = "") -> str:
    """Identity renderer — the source is already markdown. ``project_url`` is ignored."""
    return md


RENDERERS: dict[str, Callable[[str, str], str]] = {
    "markdown": render_markdown,
    "slack": render_slack,
    "txt": render_txt,
}
"""Renderer registry keyed by ``--render`` value. Add a new target by registering here."""


def render(md: str, target: str, project_url: str = "") -> str:
    """Render ``md`` to ``target``. Raises ``KeyError`` for an unknown target."""
    return RENDERERS[target](md, project_url)
