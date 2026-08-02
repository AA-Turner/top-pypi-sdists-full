"""Retrieve the changelog and/or release notes of a given version and render them.

    pysae-ai-tools code release-content [VERSION] \\
        [--lang fr|en|it] [--render markdown|slack|txt] \\
        [--changelog/--no-changelog] [--release-notes/--no-release-notes] \\
        [--root DIR] [--project-url URL]

Consolidates the logic of the legacy ``.send-slack-tag-content`` CI job: it
reads the ``## [tag] date`` section of ``CHANGELOG.md`` and/or the homonymous
section of ``docs/release-notes/release-notes.<lang>.md`` for ``VERSION``
(defaulting to the latest local git tag), assembles them into a single markdown
block, then renders that block to the chosen surface (Slack mrkdwn by
``--render slack``, plain text by ``--render txt``, raw markdown by default).

The rendered block is written to stdout — the caller decides what to do with it
(escape + ``curl`` to Slack in CI, paste into a release page, etc.). When both
sources are included, the release notes come first (user-facing) and the
changelog follows under a ``### Changelog`` sub-heading.
"""

import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated

import typer

from ..common.markdown_render import MAINTENANCE_NOTES, RENDERERS, prefix_section_emoji, render
from .changelog import find_existing_section, resolve_project_url
from .release_notes import SUPPORTED_LANGUAGES, release_config, release_notes_file, resolve_latest_tag

CHANGELOG_LABEL = "### Changelog"
"""Sub-heading prepended to the changelog body when both sources are included."""

LANGUAGE_LABELS: dict[str, str] = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "it": "🇮🇹 Italiano",
}
"""Flag + endonym heading prefixed before each language section in the
multi-language GitLab release description (🇫🇷 Français / 🇬🇧 English / 🇮🇹 Italiano)."""

HR = "---"
"""Markdown horizontal rule separating each language section (and the changelog)
in the GitLab release description. Joined with surrounding blank lines so GitLab
renders it as a rule rather than a setext heading underline."""


@dataclass
class Section:
    """A single ``## [tag] date`` section extracted from a markdown file."""

    tag: str
    date: str
    body: str


def extract_section(content: str, tag: str) -> Section | None:
    """Extract the ``## [tag] date`` section (heading date + body) from ``content``.

    Returns ``None`` when no section for ``tag`` is present. Reuses the same
    pattern ``code.changelog`` uses to locate an existing release section.
    """
    match = find_existing_section(content, tag)
    if match is None:
        return None
    return Section(tag=tag, date=match.group("date").strip(), body=match.group("body").strip("\n").rstrip())


def _read_section(path: Path, tag: str) -> Section | None:
    """Read ``path`` and extract the section for ``tag``, or ``None`` if absent."""
    if not path.is_file():
        return None
    return extract_section(path.read_text(encoding="utf-8"), tag)


def _blockquote(text: str) -> str:
    """Prefix every line of ``text`` with a markdown blockquote marker (``> ``)."""
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def build_block(changelog: Section | None, release_notes: Section | None, *, heading: bool = True) -> str:
    """Assemble one markdown block from the available sections.

    With ``heading`` (the default), the version heading ``## [tag] date`` is
    emitted once at the top. Pass ``heading=False`` to omit it — useful when the
    surface already shows the version (e.g. a GitLab release, whose name is the
    tag), so the description should open straight on the first notes section.

    Release notes come first; the changelog body is always wrapped as a markdown
    blockquote (rendered as a Slack quote block by ``--render slack``) and, when
    release notes are also present, is introduced by a ``### Changelog``
    sub-heading kept *inside* the blockquote so the whole changelog block — its
    title and its entries — renders as one Slack quote rather than a bare heading
    floating above the quoted entries.
    """
    primary = release_notes or changelog
    assert primary is not None  # callers guarantee at least one section
    parts = [f"## [{primary.tag}] {primary.date}".rstrip()] if heading else []
    if release_notes and release_notes.body:
        parts.append(release_notes.body)
    if changelog and changelog.body:
        body = f"{CHANGELOG_LABEL}\n\n{changelog.body}" if release_notes else changelog.body
        parts.append(_blockquote(body))
    return "\n\n".join(parts)


@dataclass
class ReleaseDescription:
    """Assembled release description plus the version's date (from the changelog)."""

    markdown: str
    date: str


def release_description(
    root: Path,
    tag: str,
    *,
    lang: str = "fr",
    changelog: bool = True,
    release_notes: bool = True,
    heading: bool = True,
) -> ReleaseDescription | None:
    """Assemble the markdown block for ``tag`` (release notes + quoted changelog) and its date.

    Same content the Slack release message is built from — release notes first,
    the changelog wrapped as a blockquote — but left as markdown (GitLab renders
    GitLab-Flavored Markdown natively). With ``heading=False`` the ``## [tag] date``
    title is dropped so the block opens on the first notes section. ``date`` is the
    section date written in the changelog/release notes (``YYYY-MM-DD``), suitable
    for a release's ``released_at``. Returns ``None`` when neither source has a
    section for ``tag``.
    """
    changelog_section = _read_section(root / "CHANGELOG.md", tag) if changelog else None
    release_notes_section = _read_section(release_notes_file(root, lang), tag) if release_notes else None
    if changelog_section is None and release_notes_section is None:
        return None
    # Content keeps release notes first; the date is the one written in the
    # changelog (the release date), falling back to the release notes section.
    date_source = changelog_section or release_notes_section
    assert date_source is not None
    # No user-facing notes but there is content (a changelog) → maintenance release:
    # show the localized maintenance placeholder (the renderers prefix it with 🔧)
    # above the quoted changelog, instead of a bare changelog block.
    if release_notes and release_notes_section is None:
        release_notes_section = Section(tag=tag, date=date_source.date, body=MAINTENANCE_NOTES[lang])
    # Prefix section headings with the same emojis as the Slack message, keeping markdown.
    markdown = prefix_section_emoji(build_block(changelog_section, release_notes_section, heading=heading))
    return ReleaseDescription(markdown=markdown, date=date_source.date)


def _resolve_languages(root: Path, languages: Sequence[str] | None) -> list[str]:
    """Languages to render, in canonical order: the explicit list, else the project config."""
    return list(languages) if languages is not None else release_config(root).languages


def gitlab_release_description(
    root: Path,
    tag: str,
    *,
    languages: Sequence[str] | None = None,
    changelog: bool = True,
) -> ReleaseDescription | None:
    """Assemble the multi-language GitLab release description for ``tag``.

    Each configured language's user-facing notes are emitted in turn, every one
    introduced by a flag label heading (🇫🇷 Français / 🇬🇧 English / 🇮🇹 Italiano)
    and separated by a horizontal rule (``---``); the changelog follows once at the
    very bottom under a ``### Changelog`` heading (not blockquoted).
    ``languages`` defaults to the project's release-notes config
    (``release.notes.languages`` in ``.pysae-ai-tools.yaml``), so a FR-only backend
    keeps a single section. When no language has a section but a changelog exists, a localized
    maintenance placeholder opens the description. Returns ``None`` when neither a
    language section nor a changelog is present for ``tag``. ``date`` is the section
    date (the changelog's, else the first language's), suitable for ``released_at``.
    """
    langs = _resolve_languages(root, languages)
    changelog_section = _read_section(root / "CHANGELOG.md", tag) if changelog else None

    sections: list[str] = []
    date = ""
    for lang in langs:
        notes = _read_section(release_notes_file(root, lang), tag)
        if notes is None:
            continue
        date = date or notes.date
        sections.append(f"## {LANGUAGE_LABELS.get(lang, lang)}\n\n{notes.body}")

    # No user-facing notes for any language but a changelog exists → maintenance
    # release: open on the localized placeholder (renderers prefix it with 🔧).
    if not sections and changelog_section is not None:
        primary = langs[0] if langs else "fr"
        label = LANGUAGE_LABELS.get(primary, primary)
        sections.append(f"## {label}\n\n{MAINTENANCE_NOTES.get(primary, MAINTENANCE_NOTES['fr'])}")

    if changelog_section is not None and changelog_section.body:
        date = date or changelog_section.date
        sections.append(f"{CHANGELOG_LABEL}\n\n{changelog_section.body}")

    if not sections:
        return None
    markdown = prefix_section_emoji(f"\n\n{HR}\n\n".join(sections))
    return ReleaseDescription(markdown=markdown, date=date)


@dataclass
class SlackReleaseContent:
    """Slack-rendered release content split for the #mep self-updating message.

    ``primary`` is the body attached to the main message (the first available
    language's notes, **no changelog**). ``replies`` are the ordered thread
    replies — one per remaining language, then the changelog last — each a
    ``(kind, slack_mrkdwn)`` pair where ``kind`` is the language code (``en`` /
    ``it``) or ``"changelog"`` (used as the idempotency key for the reply).
    """

    primary: str = ""
    replies: list[tuple[str, str]] = field(default_factory=list)


def _slack_notes(root: Path, tag: str, lang: str, project_url: str) -> str | None:
    """Slack-rendered user-facing notes for one language (no changelog), or ``None``.

    Opened by the language's flag label (🇫🇷 Français / 🇬🇧 English / 🇮🇹 Italiano),
    matching the per-language headings of the GitLab release description.
    """
    notes = _read_section(release_notes_file(root, lang), tag)
    if notes is None:
        return None
    label = LANGUAGE_LABELS.get(lang, lang)
    return render(f"## {label}\n\n{notes.body}", "slack", project_url)


def _slack_changelog(root: Path, tag: str, project_url: str) -> str | None:
    """Slack-rendered changelog for ``tag`` under a ``### Changelog`` heading, or ``None``.

    Not wrapped as a quote here — the changelog stands alone as its own thread
    reply, so it renders as a normal message opened by a *📝 Changelog* heading.
    """
    section = _read_section(root / "CHANGELOG.md", tag)
    if section is None or not section.body:
        return None
    return render(f"{CHANGELOG_LABEL}\n\n{section.body}", "slack", project_url)


def release_slack_content(
    root: Path,
    tag: str,
    *,
    languages: Sequence[str] | None = None,
    project_url: str = "",
) -> SlackReleaseContent:
    """Build the #mep main-message body + ordered thread replies for ``tag``.

    The first available language's notes go to the main message; every other
    configured language becomes a reply, and the changelog is appended as the
    final reply. ``languages`` defaults to the project's release-notes config, so
    a FR-only project yields just a main message + a changelog reply. ``project_url``
    defaults to ``$CI_PROJECT_URL`` then the ``origin`` remote (for tag/issue links).
    """
    langs = _resolve_languages(root, languages)
    url = project_url or os.environ.get("CI_PROJECT_URL", "") or resolve_project_url(root)

    content = SlackReleaseContent()
    for lang in langs:
        text = _slack_notes(root, tag, lang, url)
        if text is None:
            continue
        if not content.primary:
            content.primary = text
        else:
            content.replies.append((lang, text))
    changelog_text = _slack_changelog(root, tag, url)
    if changelog_text:
        content.replies.append(("changelog", changelog_text))
    return content


def main(
    version: Annotated[
        str,
        typer.Argument(help="Release tag (e.g. v1.2.3). Defaults to the latest local git tag."),
    ] = "",
    lang: Annotated[
        str,
        typer.Option("--lang", help=f"Release notes language, one of {SUPPORTED_LANGUAGES}."),
    ] = "fr",
    render_target: Annotated[
        str,
        typer.Option("--render", help=f"Output renderer, one of {sorted(RENDERERS)}."),
    ] = "markdown",
    changelog: Annotated[
        bool,
        typer.Option("--changelog/--no-changelog", help="Include the CHANGELOG.md section."),
    ] = True,
    release_notes: Annotated[
        bool,
        typer.Option(
            "--release-notes/--no-release-notes",
            help="Include the docs/release-notes/release-notes.<lang>.md section.",
        ),
    ] = True,
    root: Annotated[
        Path,
        typer.Option("--root", help="Repository root (defaults to current directory)."),
    ] = Path("."),
    project_url: Annotated[
        str,
        typer.Option(
            "--project-url",
            envvar="CI_PROJECT_URL",
            help="GitLab project URL for Slack tag/issue links (falls back to the origin remote).",
        ),
    ] = "",
) -> None:
    """Render the changelog and/or release notes of a version to stdout."""
    if not changelog and not release_notes:
        typer.secho(
            "✗ Nothing to render: pass at least one of --changelog / --release-notes.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    if render_target not in RENDERERS:
        typer.secho(
            f"✗ Unsupported render target: {render_target!r}. Pick one of {sorted(RENDERERS)}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    if release_notes and lang not in SUPPORTED_LANGUAGES:
        typer.secho(
            f"✗ Unsupported language: {lang!r}. Pick one of {SUPPORTED_LANGUAGES}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    tag = version or resolve_latest_tag(root)
    if not tag:
        typer.secho(
            "✗ No version given and no local git tag found. Pass an explicit VERSION (e.g. v1.2.3).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    changelog_section: Section | None = None
    if changelog:
        changelog_section = _read_section(root / "CHANGELOG.md", tag)
        if changelog_section is None:
            typer.secho(
                f"• No CHANGELOG.md section found for {tag} — skipping changelog.", fg=typer.colors.YELLOW, err=True
            )

    release_notes_section: Section | None = None
    if release_notes:
        release_notes_section = _read_section(release_notes_file(root, lang), tag)
        if release_notes_section is None:
            typer.secho(
                f"• No {lang.upper()} release notes section found for {tag} — skipping release notes.",
                fg=typer.colors.YELLOW,
                err=True,
            )

    if changelog_section is None and release_notes_section is None:
        typer.secho(f"✗ No changelog or release notes content found for {tag}.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    block = build_block(changelog_section, release_notes_section)
    resolved_url = project_url or (resolve_project_url(root) if render_target == "slack" else "")
    sys.stdout.write(render(block, render_target, resolved_url))
    sys.stdout.write("\n")
