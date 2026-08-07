"""Pysae AI tools — root CLI built on click LazyGroup + typer leaves.

Subcommands are imported on demand: invoking ``pysae-ai-tools tools install argocd``
only imports the install orchestrator (and the argocd tool it drives), not
the full tree. This keeps cold start under ~150 ms for most commands.

Usage:
    pysae-ai-tools --help
    pysae-ai-tools <group> --help
    pysae-ai-tools <group> <command> [options]

Examples:
    pysae-ai-tools code changelog --write
    pysae-ai-tools tools install argocd
    pysae-ai-tools glab issue-audit
    pysae-ai-tools ci run status
    pysae-ai-tools ci release next-version --bump minor
"""

import sys
from typing import Any

import click

from .common.lazy_group import LazyGroup


def _version_callback(ctx: click.Context, _param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    from pysae_ai_tools import __version__

    click.echo(f"pysae-ai-tools {__version__}")
    ctx.exit()


def _build_version_callback(ctx: click.Context, _param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    from pysae_ai_tools import compute_version

    click.echo(compute_version(build=True))
    ctx.exit()


app = LazyGroup(
    name="pysae-ai-tools",
    help="Pysae AI tools — shared utilities for Claude Code skills.",
    no_args_is_help=True,
    params=[
        click.Option(
            ["--version"],
            is_flag=True,
            expose_value=False,
            is_eager=True,
            callback=_version_callback,
            help="Show version and exit.",
        ),
        click.Option(
            ["--build-version"],
            is_flag=True,
            expose_value=False,
            is_eager=True,
            callback=_build_version_callback,
            help="Show clean build version (no .dev suffix) and exit.",
        ),
    ],
    lazy_subcommands={
        # Top-level single commands
        "self-update": "pysae_ai_tools.self_update:main",
        "install-completion": "pysae_ai_tools.install_completion:main",
        "uninstall": "pysae_ai_tools.uninstall:main",
        # Top-level multi-command apps
        "tracker": "pysae_ai_tools.tracker.__main__:app",
        "usage": "pysae_ai_tools.usage.__main__:app",
        "secrets": "pysae_ai_tools.secrets.__main__:app",
        "tools": "pysae_ai_tools.install.cli:app",
        # Command groups (one module per group under <group>/group.py)
        "glab": "pysae_ai_tools.glab.group:app",
        "mcp": "pysae_ai_tools.mcp.group:app",
        "issue": "pysae_ai_tools.issue.group:app",
        "mr": "pysae_ai_tools.mr.group:app",
        "ci": "pysae_ai_tools.ci.group:app",
        "env": "pysae_ai_tools.env.group:app",
        "aws": "pysae_ai_tools.aws.group:app",
        "auth0": "pysae_ai_tools.auth0.group:app",
        "atlas": "pysae_ai_tools.atlas.group:app",
        "mongo": "pysae_ai_tools.mongo.group:app",
        "slack": "pysae_ai_tools.slack.group:app",
        "openapi": "pysae_ai_tools.openapi.group:app",
        "internal": "pysae_ai_tools.internal.group:app",
        "code": "pysae_ai_tools.code.group:app",
        "design": "pysae_ai_tools.design.group:app",
        "docs": "pysae_ai_tools.docs.group:app",
        "agent": "pysae_ai_tools.agent.group:app",
        "skills": "pysae_ai_tools.skills.group:app",
        "stats": "pysae_ai_tools.stats.group:app",
        "project": "pysae_ai_tools.project.group:app",
        "pysae": "pysae_ai_tools.pysae.group:app",
        "figma": "pysae_ai_tools.figma.group:app",
    },
)


@app.result_callback()
@click.pass_context
def _after_command(ctx: click.Context, /, _result: Any, **_kwargs: Any) -> None:
    """Runs after any successful subcommand — the auto-update and token-rotation ticks."""
    # Skip when the invoked subcommand has just removed or replaced the package
    # files on disk: the lazy imports below would fail with ModuleNotFoundError.
    if ctx.invoked_subcommand in {"uninstall", "self-update"}:
        return

    from pysae_ai_tools.token_rotation import maybe_rotate_tokens
    from pysae_ai_tools.version_check import maybe_check_version

    # Rotation first, and unconditionally: it has its own switch and its own
    # skip rules, which are looser than the version check's (see its docstring).
    maybe_rotate_tokens()
    maybe_check_version()


def _force_utf8_output() -> None:
    """Force stdout/stderr to UTF-8 so the CLI's Unicode glyphs (✓ ✗ ⬆ …) never
    crash on a legacy console codepage. Windows PowerShell/cmd default to a
    cp125x codepage that cannot encode them, raising UnicodeEncodeError mid-run
    (e.g. in `tools install`). No-op where the streams are already UTF-8.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def main() -> None:
    _force_utf8_output()
    app()


if __name__ == "__main__":
    main()
