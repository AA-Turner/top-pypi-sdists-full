"""Unified CLI: ``pysae-ai-tools tools <command> [tool-name]``.

The Typer app wiring ``install`` / ``status`` / ``require`` / ``configure``
to the orchestration engine (:mod:`orchestrator`), the renderers
(:mod:`render`) and the interactive selection logic (:mod:`selection`).
"""

import json
from typing import Annotated

import typer

from . import orchestrator, render, selection
from .mcp_cleanup import app as mcp_cleanup_app
from .registry import TOOL_NAMES, TOOLS, Category, Mode, Tool, _find_tool

app = typer.Typer(no_args_is_help=True, help="Install, check, and manage Pysae CLI tools and MCP servers")
app.add_typer(mcp_cleanup_app, name="mcp-cleanup")


def _resolve_tools(tool_names: list[str] | None) -> list[Tool]:
    """Validate and resolve a list of tool names. Exits on the first unknown name."""
    if not tool_names:
        return list(TOOLS)
    tools: list[Tool] = []
    for name in tool_names:
        tool = _find_tool(name)
        if not tool:
            typer.echo(f"Unknown tool: {name}. Available: {', '.join(TOOL_NAMES)}", err=True)
            raise typer.Exit(code=1)
        tools.append(tool)
    return tools


@app.command()
def status(
    tool_names: Annotated[
        list[str] | None,
        typer.Argument(help="Tool name(s) — one or more positional names. Default: all.", show_default=False),
    ] = None,
    json_output: Annotated[bool, typer.Option("--json", help="JSON output")] = False,
    binaries_only: Annotated[
        bool,
        typer.Option(
            "--binaries-only",
            help="Fast path: report only installed binary versions (parallel `<bin> --version`), "
            "no auth / config / context / latest-version checks. Non-binary tools are omitted.",
        ),
    ] = False,
) -> None:
    """Show installed/missing tools and required environment variables.

    Accepts zero or more positional tool names (e.g. ``status kubectl argocd``).
    """
    if binaries_only:
        render._status_binaries(_resolve_tools(tool_names) if tool_names else list(TOOLS), json_output=json_output)
        return

    if tool_names:
        tools = _resolve_tools(tool_names)
        if json_output:
            typer.echo(json.dumps([orchestrator._state_dict(t) for t in tools]))
        else:
            for tool in tools:
                render._status_one(tool)
        return

    if json_output:
        typer.echo(json.dumps([orchestrator._state_dict(t) for t in TOOLS]))
    else:
        render._status_all()


@app.command()
def require(
    tool_names: Annotated[
        list[str],
        typer.Argument(help="Tool name(s) — at least one required.", show_default=False),
    ],
    json_output: Annotated[bool, typer.Option("--json", help="JSON output")] = False,
) -> None:
    """Check that the given tools are ready (installed, authenticated).

    Exits 0 when every named tool is callable; non-zero otherwise. ``missing``
    and ``auth-required`` are blocking — the matching ``pysae-ai-tools tools
    install <tools>`` command is printed to stderr. ``needs-update`` and
    ``needs-reconfigure`` (a secret baked into the config was rotated
    upstream) are *non-blocking*: the tool still resolves, so the skill is
    allowed to proceed and the suggested ``tools install`` command is surfaced
    as a yellow notice on stderr.

    Designed to be called from a skill prelude:

    ::

        pysae-ai-tools tools require kubectl datadog-mcp || exit 1
    """
    tools = _resolve_tools(tool_names)
    classifications = [(t, orchestrator._classify(t)) for t in tools]
    blocking = [(t, status) for t, status in classifications if status in ("missing", "auth-required")]
    outdated = [t for t, status in classifications if status == "needs-update"]
    stale = [t for t, status in classifications if status == "needs-reconfigure"]

    if json_output:
        payload: dict[str, object] = {
            "ready": not blocking,
            "tools": [{"name": t.name, "status": s} for t, s in classifications],
        }
        if blocking:
            payload["install_command"] = "pysae-ai-tools tools install " + " ".join(t.name for t, _ in blocking)
        if outdated:
            payload["outdated"] = [t.name for t in outdated]
            payload["update_command"] = "pysae-ai-tools tools install " + " ".join(t.name for t in outdated)
        if stale:
            payload["stale"] = [t.name for t in stale]
            payload["reconfigure_command"] = "pysae-ai-tools tools install " + " ".join(t.name for t in stale)
        typer.echo(json.dumps(payload))
        if blocking:
            raise typer.Exit(code=1)
        return

    if outdated:
        for tool in outdated:
            typer.secho(f"  ! {tool.name:<20} (update available)", fg=typer.colors.YELLOW, err=True)
        update_cmd = "pysae-ai-tools tools install " + " ".join(t.name for t in outdated)
        typer.secho(f"  Run when ready: {update_cmd}", fg=typer.colors.YELLOW, err=True)

    if stale:
        for tool in stale:
            typer.secho(f"  ⚙ {tool.name:<20} (secret rotated)", fg=typer.colors.YELLOW, err=True)
        reconfigure_cmd = "pysae-ai-tools tools install " + " ".join(t.name for t in stale)
        typer.secho(f"  Reconfigure with: {reconfigure_cmd}", fg=typer.colors.YELLOW, err=True)

    if not blocking:
        return

    for tool, status in blocking:
        typer.secho(f"  ✗ {tool.name:<20} ({status})", fg=typer.colors.RED, err=True)
    install_cmd = "pysae-ai-tools tools install " + " ".join(t.name for t, _ in blocking)
    typer.secho(f"\n  Run: {install_cmd}", fg=typer.colors.YELLOW, err=True)
    raise typer.Exit(code=1)


@app.command()
def configure(
    reset: Annotated[
        bool,
        typer.Option("--reset", help="Ignore the saved selection and start from the defaults."),
    ] = False,
    all_tools: Annotated[
        bool,
        typer.Option("--all", help="Select every tool non-interactively (skip the checklist)."),
    ] = False,
    required_only: Annotated[
        bool,
        typer.Option("--required-only", help="Select only the REQUIRED tools non-interactively (skip the checklist)."),
    ] = False,
    non_interactive: Annotated[
        bool,
        typer.Option(
            "--non-interactive",
            help="Never prompt, even on a TTY. Requires --all or --required-only to pick the selection.",
        ),
    ] = False,
) -> None:
    """Configure which tools are installed by `tools install`."""
    from ..config import get_tools_known_at_save, get_tools_to_install, set_tools_to_install
    from .common.checklist import force_non_interactive, is_interactive

    if all_tools and required_only:
        typer.secho("FAILED: --all and --required-only are mutually exclusive", err=True, fg=typer.colors.RED)
        raise typer.Exit(code=2)

    if non_interactive:
        force_non_interactive()

    if all_tools or required_only:
        # Deterministic, TTY-free selection — the only way `configure` runs in
        # a non-interactive environment (CI, image build). --all takes every
        # tool; --required-only keeps just the REQUIRED tier.
        selected = [t.name for t in TOOLS if all_tools or t.mode is Mode.REQUIRED]
    else:
        if not is_interactive():
            typer.secho(
                "FAILED: terminal is not interactive — cannot show the checklist. "
                "Use --all or --required-only to select non-interactively.",
                err=True,
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)
        initial = None if reset else get_tools_to_install()
        known = None if reset else get_tools_known_at_save()
        chosen = selection._prompt_tool_selection(initial, known)
        if chosen is None:
            typer.secho(
                "FAILED: terminal is not interactive — cannot show the checklist.", err=True, fg=typer.colors.RED
            )
            raise typer.Exit(code=1)
        selected = chosen

    set_tools_to_install(selected, known=TOOL_NAMES)
    typer.echo("")
    typer.secho(f"  Configuration enregistrée — {len(selected)} outil(s) sélectionné(s).", fg=typer.colors.GREEN)

    # Parameter / env-var prompting hits typer.prompt and only makes sense with
    # a TTY; skip it on the non-interactive --all / --required-only path (env
    # vars still auto-resolve at install time).
    if is_interactive():
        selected_tools = [t for t in TOOLS if t.name in selected]
        from .common.interactive import configure_parameters

        configure_parameters({t.name for t in selected_tools})
        orchestrator._configure_env_vars(selected_tools)


@app.command()
def install(
    tool_names: Annotated[
        list[str] | None,
        typer.Argument(help="Tool name(s) — one or more positional names. Default: all.", show_default=False),
    ] = None,
    skip: Annotated[
        list[str] | None,
        typer.Option("--skip", help="Skip these tools (repeatable)."),
    ] = None,
    json_output: Annotated[bool, typer.Option("--json", help="JSON output")] = False,
    non_interactive: Annotated[
        bool,
        typer.Option(
            "--non-interactive",
            help="Never involve a human — no checklist, no env-var question, and no resolver that "
            "would open a browser (Slack OAuth, `glab auth login`) — even on a TTY. Uses the saved "
            "selection (or defaults) and auto-resolves what it can. Implied in CI / non-TTY.",
        ),
    ] = False,
    configure_only: Annotated[
        bool,
        typer.Option(
            "--configure-only",
            help="Only (re-)apply configuration — auth, MCP registration, contexts, env vars. "
            "Never installs or updates a binary.",
        ),
    ] = False,
    install_only: Annotated[
        bool,
        typer.Option(
            "--install-only",
            help="Only install or update the binary — never configure (no auth, MCP registration, "
            "contexts, or env var resolution). Mirror of --configure-only.",
        ),
    ] = False,
    category: Annotated[
        list[Category] | None,
        typer.Option(
            "--category",
            help="Install every tool in this category (repeatable), bypassing the checklist. "
            "E.g. --category plugin installs the assistant skill deployments. "
            "Mutually exclusive with positional tool names.",
        ),
    ] = None,
    selected_only: Annotated[
        bool,
        typer.Option(
            "--selected",
            help="With --category, restrict to tools already in the saved selection — "
            "reconfigure what is installed, never add new tools. Used by self-update.",
        ),
    ] = False,
) -> None:
    """Install or update tools.

    Accepts zero or more positional tool names (e.g. ``install kubectl argocd``), or
    ``--category <cat>`` to install every tool in a category.
    """
    if configure_only and install_only:
        typer.echo("FAILED: --configure-only and --install-only are mutually exclusive", err=True)
        raise typer.Exit(code=2)
    if category and tool_names:
        typer.echo("FAILED: --category and positional tool names are mutually exclusive", err=True)
        raise typer.Exit(code=2)
    if non_interactive:
        from .common.checklist import force_non_interactive

        force_non_interactive()

    if category:
        skip_set = set(skip or [])
        wanted = set(category)
        cat_tools = [t for t in TOOLS if t.category in wanted and t.name not in skip_set]
        if selected_only:
            from ..config import get_tools_to_install

            selected_names = set(get_tools_to_install() or [])
            cat_tools = [t for t in cat_tools if t.name in selected_names]
        cat_results = [
            orchestrator._install_one(
                t,
                dry_run=False,
                configure_only=configure_only,
                install_only=install_only,
            )
            for t in cat_tools
        ]
        if json_output:
            typer.echo(json.dumps([r.to_dict() for r in cat_results]))
        else:
            for r in cat_results:
                render._render_install_result(r)
        if any(r.status == "failed" for r in cat_results):
            raise typer.Exit(code=1)
        return

    if tool_names:
        tools = _resolve_tools(tool_names)
        results = [
            orchestrator._install_one(
                t,
                dry_run=False,
                configure_only=configure_only,
                install_only=install_only,
            )
            for t in tools
        ]
        if json_output:
            typer.echo(json.dumps([r.to_dict() for r in results]))
        else:
            for r in results:
                render._render_install_result(r)
        if any(r.status == "failed" for r in results):
            raise typer.Exit(code=1)
        return

    from ..config import get_tools_known_at_save, get_tools_to_install, set_tools_to_install

    selected = get_tools_to_install()
    known = get_tools_known_at_save()
    effective_known = selection._effective_known(selected, known)

    # Detect tools that were added to the package since the last configure
    # save — typically after a self-update bumping the package version.
    # Legacy users (no snapshot) fall back to ``selected`` as the implicit
    # snapshot so newly-added tools still surface.
    new_tools = {t.name for t in TOOLS if t.name not in effective_known} if effective_known is not None else set()

    # Trigger the interactive checklist when:
    # - first run (nothing saved yet), OR
    # - the package now ships tools the user hasn't seen yet (NEW marker
    #   in the checklist lets them opt in/out explicitly).
    needs_prompt = selected is None or bool(new_tools)

    if not json_output and needs_prompt:
        chosen = selection._prompt_tool_selection(selected, known)
        if chosen is not None:
            set_tools_to_install(chosen, known=TOOL_NAMES)
            selected = chosen
            from .common.interactive import configure_parameters

            configure_parameters(set(chosen))
        elif selected is not None and new_tools:
            # Non-interactive terminal — fall back to default_selected for
            # the new tools and persist the snapshot to silence subsequent
            # runs.
            merged = set(selected) | {t.name for t in TOOLS if t.name in new_tools and t.default_selected}
            selected = sorted(merged)
            set_tools_to_install(selected, known=TOOL_NAMES)
    elif json_output and selected is not None and new_tools:
        # JSON / CI mode — never prompt; auto-extend with new defaults so
        # CI runs are deterministic and the snapshot is kept in sync.
        merged = set(selected) | {t.name for t in TOOLS if t.name in new_tools and t.default_selected}
        if merged != set(selected):
            selected = sorted(merged)
            set_tools_to_install(selected, known=TOOL_NAMES)

    selection_set: set[str] | None = set(selected) if selected is not None else None

    if json_output:
        # In JSON mode, --skip still works; selection is honoured if persisted.
        skip_set = set(skip or ())
        if selection_set is not None:
            skip_set |= {t.name for t in TOOLS if t.name not in selection_set and t.mode is not Mode.REQUIRED}
        results = orchestrator.install_all(
            skip=tuple(skip_set),
            configure_only=configure_only,
            install_only=install_only,
        )
        counts = {
            "installed": 0,
            "updated": 0,
            "configured": 0,
            "up-to-date": 0,
            "skipped": 0,
            "failed": 0,
            "manually-installed": 0,
        }
        for r in results:
            counts[r.status] = counts.get(r.status, 0) + 1
        typer.echo(json.dumps({"results": [r.to_dict() for r in results], "summary": counts}))
    else:
        results = orchestrator._install_pretty(
            skip=tuple(skip or ()),
            selection=selection_set,
            configure_only=configure_only,
            install_only=install_only,
        )
        counts = {
            "installed": 0,
            "updated": 0,
            "configured": 0,
            "up-to-date": 0,
            "skipped": 0,
            "failed": 0,
            "manually-installed": 0,
        }
        for r in results:
            counts[r.status] = counts.get(r.status, 0) + 1
        render._section_header(render.SECTION_SUMMARY)
        summary = ", ".join(f"{v} {k}" for k, v in counts.items() if v)
        typer.echo(f"  {summary or 'no tools processed'}")
        typer.secho(
            "  → Pour modifier la liste des outils installés : `pysae-ai-tools tools configure`",
            fg=typer.colors.BRIGHT_BLACK,
        )
    if counts["failed"]:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
