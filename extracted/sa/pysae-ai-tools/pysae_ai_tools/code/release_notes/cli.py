"""Typer command layer + file-I/O orchestration for ``code release-notes``.

Sub-commands:
    pysae-ai-tools code release-notes gather [--tag VTAG] [--root DIR]

    pysae-ai-tools code release-notes validate LANG BODY [--kind markdown|google-play|apple-app-store]

    pysae-ai-tools code release-notes merge VTAG \\
        --fr-file FILE     --en-file FILE     --it-file FILE \\
        --fr-txt-file FILE --en-txt-file FILE --it-txt-file FILE \\
        [--root DIR] [--dry-run]

``gather`` collects the raw material (commits since the latest tag + pending
changelog entries — see :mod:`.gather`) and emits a JSON payload the skill feeds
to the LLM.

``validate`` checks a single body against the canonical template
(``--kind=markdown``, default; ``md`` is accepted as a legacy alias) or against the
plain-text store rules (``--kind=google-play``: ≤500 chars; ``--kind=apple-app-store``:
≤4000 chars — no markdown headings/bullets/links, no issue refs).

``merge`` writes **six** files all-or-nothing (three accumulating per-language
markdown files plus three per-language plain-text store files). Every body is
validated *before* any file is written, so a violation in one body aborts the
whole merge without touching disk. The pure section-building / merge logic lives
in :mod:`.core`.
"""

import json
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Annotated

import typer

from ...common.project_config import flag_enabled
from ..versioning import RELEASE_TAG_RE, is_store_skipping_prerelease
from .core import (
    CANONICAL_SECTIONS,
    MAINTENANCE_NOTE,
    MAX_TXT_500_LENGTH,
    MAX_TXT_4000_LENGTH,
    SUPPORTED_LANGUAGES,
    SUPPORTED_VARIANTS,
    _merge_variant_content,
    _target_for_variant,
    _validate_for_variant,
    release_config,
    validate_body,
    validate_txt_body,
)
from .gather import list_commits_since_tag, list_pending_changelog_entries, resolve_latest_tag

app = typer.Typer(no_args_is_help=True, add_completion=False, help=__doc__)


@app.command(
    name="config",
    help="Print the resolved release-notes config (languages, variants, prompt) as JSON.",
)
def config_cmd(
    root: Annotated[
        Path,
        typer.Option("--root", help="Project root (defaults to current directory)."),
    ] = Path("."),
) -> None:
    cfg = release_config(root)
    json.dump(
        {"languages": cfg.languages, "variants": cfg.variants, "prompt": cfg.prompt},
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")


@app.command(
    name="gather",
    help="Collect commits + pending changelog entries since the latest tag, emit JSON.",
)
def gather(
    tag: Annotated[
        str,
        typer.Option(
            "--tag",
            help="Latest tag to diff against (defaults to auto-detected via 'git tag').",
        ),
    ] = "",
    root: Annotated[
        Path,
        typer.Option("--root", help="Repository root (defaults to current directory)."),
    ] = Path("."),
) -> None:
    latest_tag = tag or resolve_latest_tag(root)
    commits = list_commits_since_tag(root, latest_tag)
    entries = list_pending_changelog_entries(root)
    cfg = release_config(root)
    json.dump(
        {
            "latest_tag": latest_tag,
            "commits": [asdict(c) for c in commits],
            "changelog_entries": [asdict(e) for e in entries],
            "config": {"languages": cfg.languages, "variants": cfg.variants, "prompt": cfg.prompt},
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")


_TXT_KIND_LIMITS: dict[str, tuple[int, str]] = {
    "google-play": (MAX_TXT_500_LENGTH, "Google Play"),
    "apple-app-store": (MAX_TXT_4000_LENGTH, "Apple App Store"),
}


@app.command(
    name="validate",
    help=(
        "Check a single release notes body against the rules for its kind. "
        "--kind=markdown (default; 'md' accepted as alias) for the canonical markdown, --kind=google-play for the "
        f"≤{MAX_TXT_500_LENGTH}-char store summary, --kind=apple-app-store for the "
        f"≤{MAX_TXT_4000_LENGTH}-char store summary."
    ),
)
def validate(
    lang: Annotated[str, typer.Argument(help=f"Language code, one of {SUPPORTED_LANGUAGES}.")],
    body_file: Annotated[Path, typer.Argument(help="Path to the body file to validate.")],
    kind: Annotated[
        str,
        typer.Option(
            "--kind",
            help=(
                "'markdown' (canonical markdown; 'md' accepted as a legacy alias), "
                "'google-play' (≤500 chars plain text), or 'apple-app-store' (≤4000 chars)."
            ),
        ),
    ] = "markdown",
) -> None:
    if lang not in CANONICAL_SECTIONS:
        typer.secho(
            f"✗ Unsupported language: {lang!r}. Pick one of {SUPPORTED_LANGUAGES}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    # ``markdown`` is the canonical kind (it matches the SUPPORTED_VARIANTS / config
    # vocabulary); ``md`` is kept as a backward-compatible alias.
    if kind == "md":
        kind = "markdown"
    allowed_kinds = {"markdown", *_TXT_KIND_LIMITS.keys()}
    if kind not in allowed_kinds:
        typer.secho(
            f"✗ Unsupported kind: {kind!r}. Pick one of {sorted(allowed_kinds)}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    if not body_file.exists():
        typer.secho(f"✗ Body file not found: {body_file}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    body = body_file.read_text(encoding="utf-8")
    if kind == "markdown":
        violations = validate_body(body, lang)
        label = "canonical markdown template"
    else:
        max_length, store_name = _TXT_KIND_LIMITS[kind]
        violations = validate_txt_body(body, lang, max_length)
        label = f"{store_name} plain-text rules (≤{max_length}-char body)"

    if violations:
        typer.secho(f"✗ {lang.upper()} body violates the {label}:", fg=typer.colors.RED, err=True)
        for v in violations:
            typer.echo(f"  • {v}", err=True)
        raise typer.Exit(code=1)

    if kind == "markdown":
        typer.secho(f"✓ {lang.upper()} markdown body matches the canonical template.", fg=typer.colors.GREEN)
    else:
        max_length, store_name = _TXT_KIND_LIMITS[kind]
        typer.secho(
            f"✓ {lang.upper()} {store_name} body fits the {max_length}-char limit ({len(body)} chars).",
            fg=typer.colors.GREEN,
        )


_VARIANT_LABELS: dict[str, str] = {
    "markdown": "markdown",
    "google-play": f"Google Play (≤{MAX_TXT_500_LENGTH})",
    "apple-app-store": f"Apple App Store (≤{MAX_TXT_4000_LENGTH})",
}

_VARIANT_OPTION_TEMPLATES: dict[str, str] = {
    "markdown": "--{lang}-file",
    "google-play": "--{lang}-google-play-file",
    "apple-app-store": "--{lang}-apple-app-store-file",
}


@app.command(
    name="merge",
    help=(
        "Insert one synthesised section per language into the consolidated files at "
        "docs/release-notes/release-notes.{lang}{.md,.google-play.txt,.apple-app-store.txt}. "
        "Which languages/variants are written is driven by .pysae-ai-tools.yaml (release.notes/stores) "
        "(default: all). Files accumulate releases newest-first."
    ),
)
def merge(
    tag: Annotated[str, typer.Argument(help="Release tag (vMAJOR.MINOR.PATCH).")],
    fr_file: Annotated[
        Path | None,
        typer.Option("--fr-file", help="French markdown body (no top-level header)."),
    ] = None,
    en_file: Annotated[
        Path | None,
        typer.Option("--en-file", help="English markdown body (no top-level header)."),
    ] = None,
    it_file: Annotated[
        Path | None,
        typer.Option("--it-file", help="Italian markdown body (no top-level header)."),
    ] = None,
    fr_google_play_file: Annotated[
        Path | None,
        typer.Option(
            "--fr-google-play-file",
            help=f"French Google Play body (≤{MAX_TXT_500_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    en_google_play_file: Annotated[
        Path | None,
        typer.Option(
            "--en-google-play-file",
            help=f"English Google Play body (≤{MAX_TXT_500_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    it_google_play_file: Annotated[
        Path | None,
        typer.Option(
            "--it-google-play-file",
            help=f"Italian Google Play body (≤{MAX_TXT_500_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    fr_apple_app_store_file: Annotated[
        Path | None,
        typer.Option(
            "--fr-apple-app-store-file",
            help=f"French Apple App Store body (≤{MAX_TXT_4000_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    en_apple_app_store_file: Annotated[
        Path | None,
        typer.Option(
            "--en-apple-app-store-file",
            help=f"English Apple App Store body (≤{MAX_TXT_4000_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    it_apple_app_store_file: Annotated[
        Path | None,
        typer.Option(
            "--it-apple-app-store-file",
            help=f"Italian Apple App Store body (≤{MAX_TXT_4000_LENGTH} chars, plain text, header excluded).",
        ),
    ] = None,
    root: Annotated[
        Path,
        typer.Option("--root", help="Project root (defaults to current directory)."),
    ] = Path("."),
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Print each merged file to stdout instead of writing."),
    ] = False,
) -> None:
    if not flag_enabled(root, "release", "notes", "enabled"):
        typer.secho("• release.notes.enabled is false for this repo — release notes skipped", fg=typer.colors.YELLOW)
        return
    if not RELEASE_TAG_RE.match(tag):
        typer.secho(
            f"✗ Invalid tag: {tag}. It must start with 'v' and be valid semver (vX.Y.Z or vX.Y.Z-label.N).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    # Which (variant, language) pairs to write is driven by .pysae-ai-tools.yaml; both
    # default to everything. Files for non-selected pairs are simply ignored,
    # even if passed — so callers may keep passing all nine.
    cfg = release_config(root)
    # Betas (alpha/beta/rc) never publish to the stores — only the webapp markdown
    # notes are produced; the Google Play / Apple store variants are generated
    # only at the final release that closes the prerelease line. A *hotfix*
    # (``-hotfix.N`` / ``-N``) is store-bound like a final release, so it keeps every
    # variant — only beta prereleases are markdown-only.
    markdown_only = is_store_skipping_prerelease(tag)
    selected_variants = [v for v in cfg.variants if v == "markdown"] if markdown_only else cfg.variants
    sources: dict[str, dict[str, Path | None]] = {
        "markdown": {"fr": fr_file, "en": en_file, "it": it_file},
        "google-play": {"fr": fr_google_play_file, "en": en_google_play_file, "it": it_google_play_file},
        "apple-app-store": {
            "fr": fr_apple_app_store_file,
            "en": en_apple_app_store_file,
            "it": it_apple_app_store_file,
        },
    }
    expected = [
        (variant, lang)
        for variant in SUPPORTED_VARIANTS
        if variant in selected_variants
        for lang in SUPPORTED_LANGUAGES
        if lang in cfg.languages
    ]

    # Every selected pair needs a body file that exists on disk.
    missing: list[str] = []
    for variant, lang in expected:
        path = sources[variant][lang]
        if path is None:
            flag = _VARIANT_OPTION_TEMPLATES[variant].format(lang=lang)
            missing.append(f"{lang}/{variant} — pass {flag}")
        elif not path.exists():
            missing.append(f"{lang}/{variant}: file not found ({path})")
    if missing:
        typer.secho(
            "✗ missing body files required by .pysae-ai-tools.yaml (release.notes/stores):",
            fg=typer.colors.RED,
            err=True,
        )
        for item in missing:
            typer.echo(f"  • {item}", err=True)
        raise typer.Exit(code=1)

    # Read + validate every selected body *before* writing anything — so a
    # violation anywhere aborts cleanly without leaving files half-merged.
    bodies: dict[tuple[str, str], str] = {}
    any_violation = False
    for variant, lang in expected:
        path = sources[variant][lang]
        assert path is not None  # guaranteed by the missing-files check above
        body = path.read_text(encoding="utf-8")
        bodies[(variant, lang)] = body
        # An empty body means "no user-facing change" — replaced below by the
        # maintenance placeholder (our own content), so it skips validation.
        if not body.strip():
            continue
        violations = _validate_for_variant(variant, body, lang)
        if violations:
            any_violation = True
            typer.secho(
                f"✗ {lang.upper()} {_VARIANT_LABELS[variant]} body violates its rules ({path}):",
                fg=typer.colors.RED,
                err=True,
            )
            for v in violations:
                typer.echo(f"  • {v}", err=True)
    if any_violation:
        typer.secho(
            "\nFix the violations above and re-run. The canonical template and the per-store "
            "plain-text rules are documented in the /code-release-notes skill.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    # No user-facing change (all technical/excluded) → empty body. Still write
    # the section with the maintenance-release placeholder so the version is
    # present everywhere and release verification passes.
    for key, body in bodies.items():
        if not body.strip():
            bodies[key] = MAINTENANCE_NOTE[key[1]]

    today = date.today().isoformat()
    written: list[Path] = []

    def _write(target: Path, content: str) -> None:
        if dry_run:
            sys.stdout.write(f"--- {target} ---\n")
            sys.stdout.write(content if content.endswith("\n") else content + "\n")
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(target)

    for variant, lang in expected:
        target = _target_for_variant(variant, root, lang)
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        _write(target, _merge_variant_content(variant, existing, tag, bodies[(variant, lang)], today, lang))

    if dry_run:
        return

    rel_paths = "\n  ".join(str(p.relative_to(root)) for p in written)
    typer.secho(f"✓ release-notes updated with {tag}:\n  {rel_paths}", fg=typer.colors.GREEN)
