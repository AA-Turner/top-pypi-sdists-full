"""Typer command layer + file-I/O orchestration for ``code changelog``.

Sub-commands:
    pysae-ai-tools code changelog init                     # bootstrap changelogs/ + CHANGELOG.md
    pysae-ai-tools code changelog generate [description]   # create entry
    pysae-ai-tools code changelog validate [--fix] [PATH]  # lint changelogs/
    pysae-ai-tools code changelog release TAG              # merge changelogs/* into CHANGELOG.md

The pure entry-generation, validation and markdown-merge logic lives in
:mod:`.core`; version-tag semantics in :mod:`..versioning`. This module reads
and writes the on-disk files and exposes the CLI.

The ``--fix`` mode reformats non-conforming entries by extracting type/IID
hints from the filename when missing (e.g. ``feat-123-slug.md``).
"""

import json
import re
import subprocess
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Annotated

import typer

from ...common.project_config import flag_enabled
from ..versioning import RELEASE_TAG_RE, find_prerelease_predecessor, is_hotfix_tag, tag_base
from .core import (
    _CHANGELOG_HEADER,
    ChangelogTooLongError,
    _build_section,
    _delink_issue_refs,
    _first_bullet,
    _has_issue_ref,
    _length_failure_reason,
    _linkify_issue_refs,
    _splice_section,
    _strip_bullet,
    _try_fix,
    _validate_body,
    _ValidationFailure,
    find_existing_section,
    generate_entry,
    merge_changelog,
)


def resolve_project_url(repo_root: Path) -> str:
    """Resolve the GitLab project URL from ``repo_root``'s ``origin`` remote.

    Returns an empty string if the remote is missing, unreadable, or not a
    recognised GitLab URL. Mirrors the SSH/HTTPS parsing used by
    ``internal.detect_context.detect``.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""
    if result.returncode != 0:
        return ""
    remote_url = (result.stdout or "").strip()
    if not remote_url:
        return ""
    match = re.search(r"gitlab\.com[:/](.+?)(?:\.git)?$", remote_url)
    if not match:
        return ""
    return f"https://gitlab.com/{match.group(1)}"


def _collect_entries(changelogs_dir: Path) -> str:
    """Concatenate all ``*.md`` files in ``changelogs_dir`` (sorted), normalizing bullets."""
    if not changelogs_dir.is_dir():
        return ""
    parts: list[str] = []
    for path in sorted(changelogs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").rstrip("\n")
        if text:
            parts.append(text)
    body = "\n".join(parts)
    # Normalize "- " bullets to "* "
    body = re.sub(r"^-\s", "* ", body, flags=re.MULTILINE)
    return body


def _generate(
    description: str, write: bool, type_: str, issue_iid: str, as_json: bool, create_directory: bool = False
) -> None:
    """Generate a changelog entry and emit output (human-readable by default).

    The **only** case where nothing is generated is when the repo has no
    ``CHANGELOG.md`` at its root: that signals a project which doesn't use the
    changelog system, so we skip cleanly (exit 0). ``create_directory`` restores
    the legacy behaviour — generate regardless, creating ``changelogs/`` as
    needed even when there is no ``CHANGELOG.md``.
    """
    if not flag_enabled(Path.cwd(), "changelog", "enabled"):
        msg = "changelog.enabled is false for this repo — changelog generation skipped"
        if as_json:
            json.dump({"skipped": "changelog_disabled", "message": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            typer.secho(f"• {msg}", fg=typer.colors.YELLOW)
        return

    changelogs_dir = Path("changelogs")
    if not Path("CHANGELOG.md").is_file() and not create_directory:
        msg = "no CHANGELOG.md at the repo root — changelog generation skipped (this repo does not use changelogs)"
        if as_json:
            json.dump({"skipped": "changelog_md_absent", "message": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            typer.secho(f"• {msg}", fg=typer.colors.YELLOW)
        return

    try:
        entry = generate_entry(description=description, change_type=type_, issue_iid=issue_iid)
    except ChangelogTooLongError as err:
        if as_json:
            json.dump(
                {
                    "error": "description_too_long",
                    "message": str(err),
                    "current_length": err.current_length,
                    "max_total_length": err.max_total_length,
                    "max_description_length": err.max_description_length,
                    "type": err.change_type,
                    "issue_iid": err.issue_iid,
                    "description": err.description,
                    "content": err.content,
                },
                sys.stdout,
                indent=2,
            )
            sys.stdout.write("\n")
        else:
            typer.secho(f"✗ {err}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from err

    if write and not entry.already_exists:
        # We've decided to generate (CHANGELOG.md present, or --create-directory);
        # create changelogs/ if needed so the entry can be written.
        changelogs_dir.mkdir(parents=True, exist_ok=True)
        Path(entry.file).write_text(entry.content + "\n", encoding="utf-8")

    if as_json:
        json.dump(asdict(entry), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if entry.already_exists:
        typer.secho(f"• {entry.file} already exists", fg=typer.colors.YELLOW)
    elif write:
        typer.secho(f"✓ wrote {entry.file}", fg=typer.colors.GREEN)
    else:
        typer.secho(f"→ would write {entry.file}", fg=typer.colors.CYAN)
    typer.echo(entry.content)


def _rewrite_line(file: Path, content: str, idx: int, new_line: str) -> None:
    lines = content.splitlines()
    lines[idx] = new_line
    new_content = "\n".join(lines)
    if content.endswith("\n"):
        new_content += "\n"
    file.write_text(new_content, encoding="utf-8")


def _validate_files(files: list[Path], fix: bool) -> tuple[list[_ValidationFailure], int, int]:
    """Validate a list of changelog files. Returns (failures, fixed, total)."""
    failures: list[_ValidationFailure] = []
    fixed = 0

    for file in files:
        if not file.exists():
            failures.append(_ValidationFailure(file, "file not found", ""))
            continue
        content = file.read_text(encoding="utf-8")
        first = _first_bullet(content)
        if first is None:
            failures.append(_ValidationFailure(file, "empty file", ""))
            continue
        line, idx = first

        # A markdown-linked issue reference — ``([#62](…/issues/62))``, the form a
        # previous release run leaves behind — is normalized back to the bare
        # ``(#62)`` before every check, so the mandatory-reference and length-budget
        # checks see the entry as the author wrote it rather than tripping on the
        # embedded URL. The on-disk file keeps its link untouched: it is only
        # rewritten when ``--fix`` genuinely reformats a non-conforming entry.
        check_line = _delink_issue_refs(line)

        # Resolve the line to its final (possibly auto-fixed) form and decide if
        # the conventional-commits format is satisfied.
        body = _strip_bullet(check_line)
        format_ok = body is not None and _validate_body(body)
        final_line = check_line
        # Auto-fix when the format is broken OR the mandatory issue reference is
        # missing — ``_try_fix`` recovers the type/IID from the filename and
        # re-emits the strict ``* type: desc (#iid)`` form.
        if fix and (not format_ok or not _has_issue_ref(final_line)):
            fixed_line = _try_fix(check_line, file.name)
            if fixed_line and (b := _strip_bullet(fixed_line)) and _validate_body(b):
                if fixed_line != line:
                    _rewrite_line(file, content, idx, fixed_line)
                    fixed += 1
                final_line = fixed_line
                format_ok = True

        if not format_ok:
            reason = "missing '* ' bullet" if body is None else "does not match conventional commits"
            failures.append(_ValidationFailure(file, reason, line))
            continue

        # Changelog entries MUST carry a trailing issue reference (e.g. ``(#123)``)
        # — unlike commit messages, where it is optional. ``--fix`` can only add
        # one when the line or filename exposes an IID; otherwise it surfaces here.
        if not _has_issue_ref(final_line):
            failures.append(_ValidationFailure(file, "missing trailing issue reference, e.g. (#123)", final_line))
            continue

        # Format is valid (original or auto-fixed) — now enforce the length budget.
        # A too-long entry cannot be auto-fixed: trimming the description is a
        # semantic edit, so it always surfaces as a failure with the char count.
        length_reason = _length_failure_reason(final_line)
        if length_reason is not None:
            failures.append(_ValidationFailure(file, length_reason, final_line))

    return failures, fixed, len(files)


def release(
    tag: str,
    repo_root: Path,
    today: str | None = None,
    project_url: str | None = None,
) -> tuple[str, str, list[Path]]:
    """Merge ``changelogs/*.md`` into ``CHANGELOG.md`` under a release tag.

    When ``project_url`` is ``None``, it is resolved from the ``origin`` remote
    of ``repo_root``. Pass an empty string to skip linkification.

    The function is **idempotent on re-release**. If ``CHANGELOG.md`` already
    contains a ``## [tag] DATE`` section (typically because a previous release
    attempt for the same tag was interrupted after this step), the original
    heading and its existing bullets are preserved verbatim — including the
    date, which is **never overwritten** even if ``today`` differs — and any
    new entries currently sitting under ``changelogs/`` are appended at the end
    of the existing bullet list. When no new entries are present, the file is
    left untouched and ``consumed_files`` is empty.

    Returns ``(new_content, section_raw, consumed_files)``:
      - ``new_content``: full ``CHANGELOG.md`` with markdown issue links (or
        the input file content verbatim if the re-release was a no-op);
      - ``section_raw``: the complete release section with bare ``(#123)``
        refs, suitable for surfaces that don't render markdown (annotated git
        tag messages, GitLab's ``/-/tags`` preformatted view). Empty when the
        re-release was a no-op;
      - ``consumed_files``: changelog entries to delete after writing.

    The caller decides whether to write the result and delete the consumed files.
    """
    if not RELEASE_TAG_RE.match(tag):
        raise ValueError(f"Invalid tag: {tag}. It must start with 'v' and be valid semver")

    changelogs_dir = repo_root / "changelogs"
    changelog_file = repo_root / "CHANGELOG.md"
    today = today or date.today().isoformat()
    if project_url is None:
        project_url = resolve_project_url(repo_root)

    body_raw_new = _collect_entries(changelogs_dir)
    existing = changelog_file.read_text(encoding="utf-8") if changelog_file.exists() else ""

    existing_match = find_existing_section(existing, tag)
    if existing_match is not None:
        # Re-release path: the section already exists from a prior interrupted
        # release attempt. Keep the original heading (date included) and bullets,
        # and only append the new entries collected from ``changelogs/`` since.
        consumed = sorted(changelogs_dir.glob("*.md")) if changelogs_dir.is_dir() else []

        if not body_raw_new:
            # Nothing new to merge — full idempotency, do not even rewrite the file.
            return existing, "", []

        preserved_date = existing_match.group("date").strip()
        existing_body_linked = existing_match.group("body").strip("\n").rstrip()

        body_linked_new = _linkify_issue_refs(body_raw_new, project_url)
        merged_body_linked = existing_body_linked + "\n" + body_linked_new if existing_body_linked else body_linked_new

        new_section_linked = f"## [{tag}] {preserved_date}\n\n{merged_body_linked}"
        new_content = _splice_section(existing, existing_match, new_section_linked)

        # Reconstruct the bare-ref version for the annotated tag message.
        existing_body_raw = _delink_issue_refs(existing_body_linked)
        merged_body_raw = existing_body_raw + "\n" + body_raw_new if existing_body_raw else body_raw_new
        section_raw = f"## [{tag}] {preserved_date}\n\n{merged_body_raw}"

        return new_content, section_raw, consumed

    # Prerelease coalescing path: an earlier prerelease of the same base
    # (``v6.0.0-beta.1`` when releasing ``v6.0.0-beta.2`` or the final ``v6.0.0``)
    # already has a section. Rename that single section to ``tag``, re-date it to
    # ``today`` (this is a new release), and append the new entries — so the whole
    # ``v6.0.0`` line stays a single coalesced section instead of stacking one per
    # prerelease. A *hotfix* (``v5.3.16-1``) is exempt: it is a standalone release
    # that gets its own fresh section, exactly like a final release — no coalescing.
    base = tag_base(tag)
    predecessor = find_prerelease_predecessor(existing, base, tag) if base and not is_hotfix_tag(tag) else None
    if predecessor is not None:
        consumed = sorted(changelogs_dir.glob("*.md")) if changelogs_dir.is_dir() else []

        existing_body_linked = predecessor.group("body").strip("\n").rstrip()
        if body_raw_new:
            body_linked_new = _linkify_issue_refs(body_raw_new, project_url)
            merged_body_linked = (
                existing_body_linked + "\n" + body_linked_new if existing_body_linked else body_linked_new
            )
        else:
            merged_body_linked = existing_body_linked

        new_section_linked = _build_section(tag, merged_body_linked, today)
        new_content = _splice_section(existing, predecessor, new_section_linked)

        existing_body_raw = _delink_issue_refs(existing_body_linked)
        merged_body_raw = (
            existing_body_raw + "\n" + body_raw_new
            if (existing_body_raw and body_raw_new)
            else (existing_body_raw or body_raw_new)
        )
        section_raw = _build_section(tag, merged_body_raw, today)

        return new_content, section_raw, consumed

    # Fresh release path.
    section_raw = _build_section(tag, body_raw_new, today)
    body_linked = _linkify_issue_refs(body_raw_new, project_url)
    section_linked = _build_section(tag, body_linked, today)
    new_content = merge_changelog(existing, section_linked)

    consumed = sorted(changelogs_dir.glob("*.md")) if changelogs_dir.is_dir() else []
    return new_content, section_raw, consumed


# ---------------------------------------------------------------------------
# Typer app
# ---------------------------------------------------------------------------

app = typer.Typer(no_args_is_help=True, add_completion=False, help=__doc__)


@app.command(name="generate", help="Generate a changelog entry from branch context.")
def generate(
    description: Annotated[list[str] | None, typer.Argument(help="Description override")] = None,
    write: Annotated[
        bool, typer.Option("--write/--no-write", help="Write the file to disk if it does not exist")
    ] = True,
    type_: Annotated[str, typer.Option("--type", help="Change type override (feat, fix, tech, ...)")] = "",
    issue_iid: Annotated[
        str,
        typer.Option(
            "--issue-iid",
            help="Issue IID override (skips detect-context and branch-name parsing).",
        ),
    ] = "",
    as_json: Annotated[bool, typer.Option("--json", help="Emit JSON output instead of human-readable text")] = False,
    create_directory: Annotated[
        bool,
        typer.Option(
            "--create-directory",
            help="Legacy behaviour: generate even when there is no CHANGELOG.md at the repo root, "
            "creating changelogs/ as needed. By default a missing CHANGELOG.md skips generation.",
        ),
    ] = False,
) -> None:
    desc = " ".join(description) if description else ""
    _generate(desc, write, type_, issue_iid, as_json, create_directory)


@app.command(name="init", help="Bootstrap the changelog system: changelogs/ dir + an empty CHANGELOG.md (idempotent).")
def init(
    root: Annotated[Path, typer.Option("--root", help="Project root (defaults to the current directory).")] = Path("."),
) -> None:
    """Create the ``changelogs/`` directory and a header-only ``CHANGELOG.md`` at
    the repo root, opting the project into the changelog system.

    Idempotent: existing files are left untouched (never overwritten), so it is
    safe to re-run.
    """
    root = root.resolve()
    changelogs_dir = root / "changelogs"
    changelog_md = root / "CHANGELOG.md"

    if changelogs_dir.is_dir():
        typer.secho("• changelogs/ already exists", fg=typer.colors.YELLOW)
    else:
        changelogs_dir.mkdir(parents=True, exist_ok=True)
        typer.secho("✓ created changelogs/", fg=typer.colors.GREEN)

    if changelog_md.is_file():
        typer.secho("• CHANGELOG.md already exists", fg=typer.colors.YELLOW)
    else:
        changelog_md.write_text(_CHANGELOG_HEADER, encoding="utf-8")
        typer.secho("✓ created CHANGELOG.md", fg=typer.colors.GREEN)


@app.command(name="release", help="Merge changelogs/*.md into CHANGELOG.md for a new release tag.")
def release_command(
    tag: Annotated[str, typer.Argument(help="Release tag (vMAJOR.MINOR.PATCH)")],
    root: Annotated[
        Path,
        typer.Option("--root", help="Project root (defaults to current directory)"),
    ] = Path("."),
    keep_entries: Annotated[
        bool,
        typer.Option("--keep-entries", help="Do not delete files under changelogs/ after merging"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Print the resulting CHANGELOG.md to stdout and do not write anything"),
    ] = False,
) -> None:
    changelog_path = root / "CHANGELOG.md"
    existing_before = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    re_release = find_existing_section(existing_before, tag) is not None

    try:
        new_content, _section_raw, consumed = release(tag=tag, repo_root=root)
    except ValueError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    if dry_run:
        sys.stdout.write(new_content)
        return

    if re_release and not consumed:
        # Idempotent no-op: section already present and nothing new to merge.
        typer.secho(
            f"• CHANGELOG.md already contains {tag} and no new changelogs/ entries — nothing to do",
            fg=typer.colors.YELLOW,
        )
        return

    changelog_path.write_text(new_content, encoding="utf-8")
    if not keep_entries:
        for path in consumed:
            path.unlink()

    if re_release:
        typer.secho(
            f"✓ CHANGELOG.md: appended {len(consumed)} new entrie(s) to existing {tag} section",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"✓ CHANGELOG.md updated with {tag} ({len(consumed)} entrie(s) merged)",
            fg=typer.colors.GREEN,
        )


@app.command(name="validate", help="Validate changelog files (strict conventional commits + length budget).")
def validate(
    files: Annotated[
        list[Path] | None,
        typer.Argument(help="Changelog files or directory (default: changelogs/)"),
    ] = None,
    fix: Annotated[bool, typer.Option("--fix", help="Auto-fix non-conforming entries when possible")] = False,
) -> None:
    # Resolve file list: explicit files, directory, or default
    if files:
        resolved: list[Path] = []
        for f in files:
            if f.is_dir():
                resolved.extend(sorted(f.glob("*.md")))
            elif f.suffix == ".md":
                resolved.append(f)
        if not resolved:
            typer.secho("No .md files found in arguments", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
    else:
        path = Path("changelogs")
        if not path.exists() or not path.is_dir():
            typer.secho(f"Directory not found: {path}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
        resolved = sorted(path.glob("*.md"))

    failures, fixed, total = _validate_files(resolved, fix)

    for fail in failures:
        typer.secho(f"✗ {fail.file}: {fail.reason}", fg=typer.colors.RED, err=True)
        if fail.line:
            typer.echo(f"  → {fail.line}", err=True)

    if failures:
        suffix = f" — {fixed} auto-fixed" if fixed else ""
        typer.secho(
            f"\n{len(failures)} invalid file(s) over {total}{suffix}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    if fixed:
        typer.secho(
            f"✎ {fixed} fixed changelog file(s) (now valid)",
            fg=typer.colors.YELLOW,
        )
        remaining = total - fixed
        if remaining > 0:
            typer.secho(
                f"✓ {remaining} valid changelog file(s)",
                fg=typer.colors.GREEN,
            )
        raise typer.Exit(code=1)

    typer.secho(f"✓ {total} valid changelog file(s)", fg=typer.colors.GREEN)
