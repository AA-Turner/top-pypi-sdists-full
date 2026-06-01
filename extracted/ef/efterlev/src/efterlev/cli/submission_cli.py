"""CLI handler for `efterlev submission package`. Renders the SubmissionResult."""

from __future__ import annotations

from pathlib import Path

import typer

from efterlev.primitives.submission import build_submission


def run_submission_package(
    target: Path,
    *,
    output: Path | None,
    archive: bool,
    package_version: str | None,
) -> int:
    """Execute the submission-package command. Returns process exit code."""
    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        return 1

    result = build_submission(
        root,
        output=output,
        archive=archive,
        package_version=package_version,
    )

    typer.echo("")
    typer.echo("  Building submission package...")
    for a in result.artifacts:
        typer.echo(f"  ✓ {a.archive_path}  ({a.size_bytes:,} bytes)")
    typer.echo("")
    if result.missing:
        typer.echo("  Missing pieces (informational, not blocking):")
        for m in result.missing:
            typer.echo(f"    - {m}")
        typer.echo("")
    typer.echo(f"  Written to: {result.output_path}")
    if result.is_archive:
        size_kb = result.output_path.stat().st_size / 1024
        typer.echo(f"  Size:       {size_kb:,.1f} KB")
    typer.echo(f"  Version:    {result.package_version}")
    typer.echo("")
    typer.echo("  Hand this to your 3PAO. Re-run after closing more gaps; the")
    typer.echo("  package is versioned so you can show progress across iterations.")
    typer.echo("")
    return 0
