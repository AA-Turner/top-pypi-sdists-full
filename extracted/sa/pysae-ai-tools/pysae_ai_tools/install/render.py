"""Terminal rendering for the meta-installer.

Icons, section/category headers, per-tool status lines, install-result lines
and the fast binary-only probe view. Pure presentation: it reads tool state
(through the typed :func:`registry._instance` contract) and prints — it never
installs.
"""

import json
import os
import shutil
from typing import Any

import typer

from .common.base import BinaryTool, Status, ToolState
from .orchestrator import Result
from .registry import (
    CATEGORY_ORDER,
    TOOLS,
    Category,
    Mode,
    Tool,
    _find_tool,
    _instance,
    _tools_by_category,
)

CATEGORY_HEADER: dict[Category, str] = {
    Category.LANGUAGE: "Language toolchains",
    Category.CLI: "CLI binaries",
    Category.MCP: "MCP servers",
    Category.PLUGIN: "Assistant skills & plugins",
    Category.EMBEDDED: "Embedded (hooks, shell & env)",
}

CATEGORY_ICON: dict[Category, str] = {
    Category.LANGUAGE: "🌐",
    Category.CLI: "🔧",
    Category.MCP: "🔌",
    Category.PLUGIN: "🧩",
    Category.EMBEDDED: "📦",
}

SECTION_ENV = "🔑 Environment variables"
SECTION_SUMMARY = "📊 Summary"
SECTION_RULE = "─" * 60


def _section_header(title: str) -> None:
    typer.echo("")
    typer.echo(f"  {title}")
    typer.echo(f"  {SECTION_RULE}")


def _category_header(cat: Category) -> None:
    """Print a section header for a category (only when it has any tools)."""
    _section_header(f"{CATEGORY_ICON[cat]} {CATEGORY_HEADER[cat]}")


def _extract_identity(tool: Tool, payload: dict[str, Any]) -> list[tuple[str, str | None]]:
    """Extract identity/context lines by delegating to the tool's extract_identity method."""
    try:
        return list(_instance(tool.module).extract_identity(payload))
    except Exception:  # noqa: BLE001
        return []


def _version_hint(found: bool, needs_update: bool, state_payload: dict[str, Any]) -> str:
    """Human version segment for a tool's status line: the installed version
    and, when it adds information, the installable (latest) version.

    - installed & up-to-date → ``v1.2.3`` (latest equals it, shown implicitly)
    - installed & outdated   → ``v1.2.0 → v1.3.0``
    - not installed          → ``not installed (installable v1.3.0)``

    The outdated arrow is driven by ``needs_update`` (the same signal as the
    icon, which normalises the ``v`` prefix) rather than a raw string compare,
    so ``3.3.4`` vs ``v3.3.4`` doesn't read as a spurious update.

    Empty for non-binary tools (MCP servers, plugins, embedded entries): they
    have no version concept — readiness shows via the icon and identity lines.
    """
    binary = state_payload.get("binary")
    if not isinstance(binary, dict):
        return ""
    installed = (binary.get("version") or "").strip()
    latest = (state_payload.get("latest") or "").strip()
    if not found:
        return f"not installed (installable {latest})" if latest else "not installed"
    if needs_update and latest:
        return f"{installed} → {latest}"
    return installed or "installed"


def _render_tool_status(tool: Tool) -> str:
    """Render a single tool's status line. Returns the detected status
    (``installed`` / ``needs-update`` / ``missing``).
    """
    state: ToolState | None = None
    state_payload: dict[str, Any] = {}
    try:
        state = _instance(tool.module).get_state()
        state_payload = state.to_dict()
    except Exception:  # noqa: BLE001
        pass

    status: Status = state.classify() if state is not None else ("installed" if shutil.which(tool.name) else "missing")
    found = status != "missing"
    needs_update = status == "needs-update"
    needs_reconfigure = status == "needs-reconfigure"
    auth_failed = status == "auth-required"
    if not found:
        icon = "✗"
        color = typer.colors.RED
    elif needs_update:
        icon = "⬆"
        color = typer.colors.YELLOW
    elif needs_reconfigure:
        icon = "⚙"
        color = typer.colors.YELLOW
    elif auth_failed:
        icon = "⚠"
        color = typer.colors.YELLOW
    else:
        icon = "✓"
        color = typer.colors.GREEN
    env_parts: list[str] = []
    if not found:
        for var in tool.env_vars:
            if os.environ.get(var):
                env_parts.append(f"  ✓ ${var}")
            else:
                env_parts.append(f"  ✗ ${var}")

    identity_lines = _extract_identity(tool, state_payload)

    version_hint = _version_hint(found, needs_update, state_payload)
    if needs_reconfigure:
        status_hint = " (secret rotated — run `tools install`)"
    elif auth_failed:
        status_hint = " (auth required)"
    else:
        status_hint = ""

    line = f"  {icon} {tool.name:<20} {version_hint}".rstrip()
    has_details = bool(identity_lines or env_parts)
    typer.secho(f"{line}{status_hint}", fg=color, nl=not has_details)
    if has_details:
        typer.echo("")
    for text, line_color in identity_lines:
        typer.secho(f"      {text}", fg=line_color or typer.colors.BRIGHT_BLACK)
    for part in env_parts:
        var_set = part.startswith("  ✓")
        typer.secho(f"    {part}", fg=typer.colors.GREEN if var_set else typer.colors.YELLOW)

    return status


def _status_one(tool: Tool) -> None:
    """Show status for a single tool."""
    _render_tool_status(tool)


def _binary_probe(tool: Tool) -> dict[str, Any] | None:
    """Fast, local-only probe of a binary tool: run ``<bin> --version`` and
    return its presence / installed version / path.

    Returns ``None`` for non-binary tools (MCP servers, plugins, embedded
    entries), which have no binary to probe. Does **no** network call, auth
    check, context check or latest-version fetch — the fast path behind
    ``tools status --binaries-only``.
    """
    try:
        instance = _instance(tool.module)
    except Exception:  # noqa: BLE001
        return None
    if not isinstance(instance, BinaryTool):
        return None

    from .common import binary

    bs = binary.status(
        instance.binary_name,
        version_arg=instance.version_arg,
        timeout=instance.version_timeout,
    )
    return {"name": tool.name, "installed": bs.installed, "version": bs.version, "path": bs.path}


def _status_binaries(tools: list[Tool], *, json_output: bool) -> None:
    """Render (or emit as JSON) installed binary versions only, probed in
    parallel and grouped by category. Non-binary tools are omitted, so only
    categories that hold at least one binary get a section header."""
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=min(16, max(1, len(tools)))) as pool:
        probed = list(pool.map(_binary_probe, tools))

    if json_output:
        typer.echo(json.dumps([r for r in probed if r is not None]))
        return

    by_name = {r["name"]: r for r in probed if r is not None}
    grouped = _tools_by_category(tuple(tools))
    for cat in CATEGORY_ORDER:
        bucket = [t for t in (grouped.get(cat) or []) if t.name in by_name]
        if not bucket:
            continue
        _category_header(cat)
        for tool in bucket:
            r = by_name[tool.name]
            installed = bool(r["installed"])
            icon = "✓" if installed else "✗"
            color = typer.colors.GREEN if installed else typer.colors.RED
            version = str(r["version"]) or ("installed" if installed else "not installed")
            typer.secho(f"  {icon} {tool.name:<20} {version}", fg=color)


def _status_all() -> None:
    """Show installed/missing tools and required environment variables, grouped by category."""
    counts = {"installed": 0, "needs-update": 0, "auth-required": 0, "missing": 0}
    grouped = _tools_by_category()
    for cat in CATEGORY_ORDER:
        bucket = grouped.get(cat) or []
        if not bucket:
            continue
        _category_header(cat)
        for tool in bucket:
            status = _render_tool_status(tool)
            counts[status] = counts.get(status, 0) + 1

    tools_with_env = [t for t in TOOLS if t.env_vars and not t.installed]
    if tools_with_env:
        _section_header(SECTION_ENV)
        for tool in tools_with_env:
            env = tool.env
            typer.echo(f"  {tool.name}:")
            for var in tool.env_vars:
                present = bool(os.environ.get(var))
                icon = "✓" if present else "✗"
                color = typer.colors.GREEN if present else typer.colors.YELLOW
                typer.secho(f"    {icon} ${var}", fg=color)
                if not present and var in env.help:
                    typer.secho(f"      → {env.help[var]}", fg=typer.colors.BRIGHT_BLACK)
            typer.echo("")

    _section_header(SECTION_SUMMARY)
    summary = ", ".join(f"{v} {k}" for k, v in counts.items() if v)
    typer.echo(f"  {summary or 'no tools'}")


def _render_install_result(r: Result) -> None:
    """Render a single install result with icon + color, matching status style."""
    if r.status == "up-to-date":
        icon, color = "✓", typer.colors.GREEN
    elif r.status == "manually-installed":
        icon, color = "✓", typer.colors.GREEN
    elif r.status == "installed":
        icon, color = "⬆", typer.colors.YELLOW
    elif r.status == "updated":
        icon, color = "⬆", typer.colors.YELLOW
    elif r.status == "configured":
        icon, color = "⚙", typer.colors.CYAN
    elif r.status == "skipped":
        icon, color = "⊘", typer.colors.BRIGHT_BLACK
    else:  # failed
        icon, color = "✗", typer.colors.RED

    tool = _find_tool(r.name)
    mode_tag = f" ({tool.mode.value})" if tool is not None and tool.mode != Mode.OPTIONAL else ""

    suffix = ""
    if r.status in ("installed", "updated") and isinstance(r.detail, dict):
        version = r.detail.get("version", "")
        if version:
            suffix = f" → {version}"
    if r.error:
        suffix = f" — {r.error}"
    elif r.status == "skipped" and isinstance(r.detail, dict):
        reason = r.detail.get("reason")
        if reason:
            suffix = f" — {reason}"

    label = "manually installed" if r.status == "manually-installed" else r.status
    typer.secho(f"  {icon} {r.name:<20} {label}{suffix}{mode_tag}", fg=color)
