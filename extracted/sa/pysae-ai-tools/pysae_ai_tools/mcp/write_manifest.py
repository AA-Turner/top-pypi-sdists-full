"""``pysae-ai-tools mcp write-manifest`` — (re)write the plugin's ``.mcp.json``.

Writes secret-free shim entries for a set of MCP servers into the deployed Claude
plugin manifest. Used by CI (``docker/auth.sh``) so the image serves MCP through
the plugin — same ``mcp__plugin_pysae_<server>__*`` tool names as a local install —
instead of injecting resolved servers into ``~/.claude.json``.

``--skip-unavailable`` drops any server whose secrets cannot be resolved in the
current environment (the shim's own resolution path, run silently), so a job that
lacks a given secret simply does not declare that server.
"""

import json
import os
from pathlib import Path
from typing import Annotated, Any

import typer


def _managed_tools() -> dict[str, Any]:
    """Map every managed server name → its ``McpTool`` instance."""
    from ..install.registry import TOOLS, Category, _instance

    out: dict[str, Any] = {}
    for entry in TOOLS:
        if entry.category is not Category.MCP:
            continue
        try:
            instance = _instance(entry.module)
        except Exception:  # noqa: BLE001
            continue
        for name in instance.mcp_server_names():
            out[name] = instance
    return out


def _is_available(instance: Any) -> bool:
    """True when the server's config resolves in the current environment.

    Runs the shim's resolution path (env → resolver) silently and
    non-interactively; any failure means the secrets are not available here."""
    from ..env import trace
    from ..env.resolve import try_auto_resolve

    try:
        with trace.silence_trace(), trace.assume_noninteractive():
            for var in instance.env_required:
                if not os.environ.get(var):
                    try_auto_resolve(var)
            instance.prepare()
            instance.build_config()
        return True
    except Exception:  # noqa: BLE001
        return False


def main(
    servers: Annotated[
        list[str] | None,
        typer.Argument(help="Server names to declare (default: all managed servers)."),
    ] = None,
    all_servers: Annotated[
        bool, typer.Option("--all", help="Declare every managed server (ignores positional names).")
    ] = False,
    skip_unavailable: Annotated[
        bool, typer.Option("--skip-unavailable", help="Drop servers whose secrets do not resolve here.")
    ] = False,
    path: Annotated[
        Path | None,
        typer.Option("--path", help="Manifest path to write (default: the deployed plugin's .mcp.json)."),
    ] = None,
) -> None:
    """Write the plugin ``.mcp.json`` with shim entries for the selected servers."""
    from ..install.common import mcp_manifest
    from ..install.common.skills_deploy import claude_plugin_manifest_path

    managed = _managed_tools()
    if all_servers or not servers:
        wanted = list(managed)
    else:
        unknown = [s for s in servers if s not in managed]
        if unknown:
            typer.echo(f"mcp write-manifest: unknown server(s): {', '.join(unknown)}", err=True)
            raise typer.Exit(code=1)
        wanted = list(servers)

    skipped: list[str] = []
    if skip_unavailable:
        available: list[str] = []
        for name in wanted:
            if _is_available(managed[name]):
                available.append(name)
            else:
                skipped.append(name)
        wanted = available

    target = path or claude_plugin_manifest_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(mcp_manifest.build_plugin_mcp_json(wanted), indent=2) + "\n", encoding="utf-8")

    typer.echo(f"mcp write-manifest: declared {len(wanted)} server(s) → {target}", err=True)
    if wanted:
        typer.echo(f"  declared: {', '.join(wanted)}", err=True)
    if skipped:
        typer.echo(f"  skipped (unavailable): {', '.join(skipped)}", err=True)
