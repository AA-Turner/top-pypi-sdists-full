"""Uninstall pysae-ai-tools: remove the Claude Code plugin and the Python package.

Removes via uv tool uninstall.

Usage:
    pysae-ai-tools uninstall
    pysae-ai-tools uninstall --keep-plugin   # keep Claude Code plugin
    pysae-ai-tools uninstall --dry-run       # show what would be done
"""

import os
import shutil
import subprocess
import sys
from typing import Annotated

import typer

from .common.windows import schedule_deferred_cmd

PACKAGE = "pysae-ai-tools"

INSTALL_BASE_URL = "https://tools.pysae.com/pysae-ai-tools"

# Set to True when ``_schedule_windows_deferred_uninstall`` succeeds. Tells
# ``main`` to skip the "another installation found" warning, because the
# uv-managed shim that ``shutil.which`` will still see is exactly the one
# we just scheduled for deletion.
_deferred_cleanup_scheduled = False


def _is_running_in_powershell() -> bool:
    """Best-effort: are we running under a PowerShell host (vs cmd.exe)?

    PowerShell — both Windows PowerShell 5.x and PowerShell Core 7+ —
    sets ``PSModulePath`` automatically; cmd.exe doesn't. The value is
    inherited from parent to child, so a cmd.exe spawned *from inside*
    PowerShell will be misclassified as PowerShell. That's acceptable
    here: the worst case is we recommend the ``irm | iex`` form to a
    cmd user, which they'll notice immediately and can switch to the
    cmd one (also displayed below the primary line).
    """
    if os.name != "nt":
        return False
    return bool(os.environ.get("PSModulePath"))


def _reinstall_commands() -> list[str]:
    """Lines to print under "To reinstall:" — primary first, alts after.

    On Windows we try to put the most likely shell first (PowerShell vs
    cmd), but always include the other so a misdetection doesn't leave
    the user stuck.
    """
    if os.name != "nt":
        return [f"curl -fsSL {INSTALL_BASE_URL}/install.sh | bash"]

    ps = f"irm {INSTALL_BASE_URL}/install.ps1 | iex"
    cmd = f"curl -fsSL {INSTALL_BASE_URL}/install.cmd -o install.cmd && install.cmd"
    if _is_running_in_powershell():
        return [
            f"PowerShell:  {ps}",
            f"cmd.exe:     {cmd}",
        ]
    return [
        f"cmd.exe:     {cmd}",
        f"PowerShell:  {ps}",
    ]


def _uv_tool_dir() -> str | None:
    """Return the path to the uv tool root, or None if uv is missing/unhealthy."""
    return _run_uv_dir([])


def _uv_tool_bin_dir() -> str | None:
    """Return uv's tool bin directory (where shims live), or None on failure."""
    return _run_uv_dir(["--bin"])


def _run_uv_dir(extra_args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["uv", "tool", "dir", *extra_args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    path = result.stdout.strip()
    return path or None


def _is_uv_managed_path(path: str) -> bool:
    """Return True if ``path`` resolves inside one of uv's tool directories.

    Used to suppress the "another installation found" warning when the
    binary on PATH is the uv-managed shim we just (or just scheduled to)
    uninstalled.
    """
    try:
        candidate = os.path.normcase(os.path.realpath(path))
    except OSError:
        return False

    for raw_dir in (_uv_tool_bin_dir(), _uv_tool_dir()):
        if not raw_dir:
            continue
        try:
            normalized = os.path.normcase(os.path.realpath(raw_dir))
        except OSError:
            continue
        if candidate == normalized or candidate.startswith(normalized + os.sep):
            return True
    return False


def _force_remove_tool_dir(dry_run: bool) -> bool:
    """Fallback when ``uv tool uninstall`` fails: delete the tool dir directly.

    Handles the corrupted-state case where ``uv tool list`` reports
    ``Failed find package ... in tool environment`` — the registration exists
    but the venv is broken, so ``uv tool uninstall`` refuses to act.
    """
    root = _uv_tool_dir()
    if not root:
        return False
    target = os.path.join(root, PACKAGE)
    if not os.path.isdir(target):
        return False
    if dry_run:
        print(f"  [dry-run] would remove tool dir: {target}", file=sys.stderr)
        return True
    try:
        shutil.rmtree(target)
    except OSError as exc:
        print(f"  Failed to remove {target}: {exc}", file=sys.stderr)
        return False
    print(f"  Removed stale tool dir: {target}", file=sys.stderr)
    return True


def _schedule_windows_deferred_uninstall() -> bool:
    """Spawn a detached cmd that runs ``uv tool uninstall`` after we exit.

    On Windows the running ``pysae-ai-tools.exe`` is locked while it executes,
    so neither ``uv tool uninstall`` nor ``shutil.rmtree`` can wipe the
    Scripts directory. The workaround: write a small batch script that polls
    for our PID to disappear, then runs the uninstall, then deletes itself.

    Defense in depth: capture the package and shim paths now (while uv's
    manifest is still readable) so the bat can wipe them directly even
    if ``uv tool uninstall`` fails inside the bat.
    """
    if os.name != "nt":
        return False

    global _deferred_cleanup_scheduled

    tool_root = _uv_tool_dir() or ""
    bin_root = _uv_tool_bin_dir() or ""
    pkg_dir = os.path.join(tool_root, PACKAGE) if tool_root else ""
    shim_lower = os.path.join(bin_root, f"{PACKAGE}.exe") if bin_root else ""
    shim_upper = os.path.join(bin_root, f"{PACKAGE}.EXE") if bin_root else ""

    script_lines = [f"uv tool uninstall {PACKAGE} >nul 2>&1"]
    # Belt-and-suspenders: nuke the package dir and shim directly in case uv
    # fails (corrupted manifest, partial earlier removal, etc.).
    if pkg_dir:
        script_lines.append(f'if exist "{pkg_dir}" rmdir /s /q "{pkg_dir}" >nul 2>&1')
    if shim_lower:
        script_lines.append(f'if exist "{shim_lower}" del /q /f "{shim_lower}" >nul 2>&1')
    if shim_upper and shim_upper != shim_lower:
        script_lines.append(f'if exist "{shim_upper}" del /q /f "{shim_upper}" >nul 2>&1')

    try:
        schedule_deferred_cmd(os.getpid(), script_lines)
    except OSError as exc:
        print(f"  Failed to schedule deferred uninstall: {exc}", file=sys.stderr)
        return False

    _deferred_cleanup_scheduled = True
    return True


def _uninstall_package(dry_run: bool) -> bool:
    """Uninstall the Python package via uv. Returns True on success."""
    cmd = ["uv", "tool", "uninstall", PACKAGE]

    if dry_run:
        print(f"  [dry-run] {' '.join(cmd)}", file=sys.stderr)
        return True

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=30)
    except FileNotFoundError:
        print("  uv not found on PATH.", file=sys.stderr)
        return False

    if result.returncode == 0:
        return True

    stderr = (result.stderr or "").strip()
    if stderr:
        for line in stderr.splitlines():
            print(f"  uv: {line}", file=sys.stderr)

    # On Windows the running .exe is locked; ``uv tool uninstall`` and
    # rmtree both fail with "access denied". Schedule a deferred cleanup
    # via a detached cmd so the uninstall completes after we exit.
    if os.name == "nt" and stderr and "os error 5" in stderr.lower():
        if _schedule_windows_deferred_uninstall():
            print(
                "  Scheduled deferred uninstall — will complete a few seconds after this process exits.",
                file=sys.stderr,
            )
            print(
                "  (Wait ~5s before running pysae-ai-tools again — cleanup happens after we exit.)",
                file=sys.stderr,
            )
            return True

    # Fallback: the tool dir may exist in a corrupted state where uv refuses
    # to uninstall. Remove it directly.
    print("  Falling back to direct tool-dir removal...", file=sys.stderr)
    return _force_remove_tool_dir(dry_run)


def _uninstall_plugin(dry_run: bool) -> bool:
    """Tear down the Claude Code plugin via the install module.

    Delegates to :func:`pysae_ai_tools.install.claude_plugin.do_uninstall`
    so the full cleanup is in a single place — marketplace registration,
    persistent marketplace tree, and direct-copy fallback.
    """
    from .install import claude_plugin

    if dry_run:
        report = claude_plugin.tool.do_uninstall(dry_run=True)
        for key in ("marketplace_remove_cmd", "marketplace_dir", "plugin_cache"):
            value = report.extra.get(key)
            if value:
                print(f"  [dry-run] would remove: {value}", file=sys.stderr)
        return True

    report = claude_plugin.tool.do_uninstall(dry_run=False)
    removed = report.extra.get("removed") or []
    if not removed:
        print("  Plugin not installed, skipping.", file=sys.stderr)
        return True
    for path in removed:
        print(f"  removed {path}", file=sys.stderr)
    return True


def _uninstall_codex_plugin(dry_run: bool) -> None:
    """Tear down the native Codex plugin and any legacy global skill copies."""
    from .install import codex_plugin

    if dry_run:
        report = codex_plugin.tool.do_uninstall(dry_run=True)
        for key in ("plugin_remove_cmd", "marketplace_remove_cmd", "marketplace_dir"):
            value = report.extra.get(key)
            if value:
                print(f"  [dry-run] would remove: {value}", file=sys.stderr)
        for path in report.extra.get("would_remove") or []:
            print(f"  [dry-run] would remove: {path}", file=sys.stderr)
        return

    report = codex_plugin.tool.do_uninstall(dry_run=False)
    removed = report.extra.get("removed") or []
    if not removed:
        print("  Codex plugin not installed, skipping.", file=sys.stderr)
        return
    for path in removed:
        print(f"  removed {path}", file=sys.stderr)


def _uninstall_claude_settings(dry_run: bool) -> None:
    """Remove the assistant security defaults the plugins applied: the Claude allow-list and the
    Pysae-managed hooks (usage, tracker, mcp-cleanup) in ``~/.claude/settings.json``, plus the
    Codex sandbox key in ``~/.codex/config.toml``."""
    from typing import cast

    from .install.common.assistants import CLAUDE, CODEX
    from .install.common.perms_targets import ClaudePermsStore
    from .install.common.skills_deploy import _migrate_legacy_claude_hooks, legacy_claude_hooks_present

    # CLAUDE.perms is the Claude allow-list store; the cast surfaces its introspection
    # (removable / removable_flags) used only for the "removed N permissions" report.
    claude_perms = cast(ClaudePermsStore, CLAUDE.perms)
    codex_perms = CODEX.perms

    if dry_run:
        hooks = legacy_claude_hooks_present()
        perms = len(claude_perms.removable() + claude_perms.removable_flags())
        codex_perms_set = CODEX.is_active() and codex_perms.is_satisfied()
        if hooks:
            print("  [dry-run] would remove the Pysae-managed hooks", file=sys.stderr)
        if perms > 0:
            print(f"  [dry-run] would remove {perms} managed permission(s) from settings.json", file=sys.stderr)
        if codex_perms_set:
            print("  [dry-run] would remove the Codex sandbox network_access key", file=sys.stderr)
        if not hooks and perms <= 0 and not codex_perms_set:
            print("  Nothing to clean in settings.json, skipping.", file=sys.stderr)
        return

    try:
        removed_hooks = _migrate_legacy_claude_hooks()
        if removed_hooks:
            print(f"  removed the Pysae-managed hooks ({', '.join(removed_hooks)})", file=sys.stderr)
        managed = claude_perms.removable() + claude_perms.removable_flags()
        count = len(managed) if claude_perms.revert() else 0
        if count:
            print(f"  removed {count} managed permission(s) from settings.json", file=sys.stderr)
        codex_removed = codex_perms.revert()
        if codex_removed:
            print("  removed the Codex sandbox network_access key", file=sys.stderr)
        if not removed_hooks and not count and not codex_removed:
            print("  Nothing to clean in settings.json, skipping.", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        print(f"  Could not clean settings.json: {exc}", file=sys.stderr)


def _uninstall_mcp_servers(dry_run: bool) -> None:
    """Remove the MCP servers `tools install` registered in ~/.claude.json (best-effort)."""
    from .install.all import uninstall_mcp_servers

    try:
        removed = uninstall_mcp_servers(dry_run=dry_run)
    except Exception as exc:  # noqa: BLE001
        print(f"  Could not clean MCP servers: {exc}", file=sys.stderr)
        return
    if not removed:
        print("  No managed MCP servers configured, skipping.", file=sys.stderr)
        return
    prefix = "  [dry-run] would remove" if dry_run else "  removed"
    for name in removed:
        print(f"{prefix} MCP server {name}", file=sys.stderr)


def _uninstall_shell_init(dry_run: bool) -> None:
    """Strip the ``pysae-env`` line from every shell rc (best-effort)."""
    from .install import shell_init

    try:
        report = shell_init.tool.do_uninstall(dry_run=dry_run)
    except Exception as exc:  # noqa: BLE001
        print(f"  Could not clean shell rc files: {exc}", file=sys.stderr)
        return
    removed = report.extra.get("removed") or []
    if not removed:
        print("  Not configured in any shell, skipping.", file=sys.stderr)
        return
    for rc in removed:
        prefix = "  [dry-run] would clean" if dry_run else "  cleaned"
        print(f"{prefix} {rc}", file=sys.stderr)


def _uninstall_registry_credential(dry_run: bool) -> None:
    """Strip the GitLab registry credential from every ecosystem the CLI posed it in."""
    from .install import registry_credential

    try:
        if dry_run:
            removed = {
                name: registry_credential.CONSUMERS_BY_NAME[name].state(registry_credential.targets()).locations
                for name in registry_credential.CONSUMERS_BY_NAME
            }
        else:
            removed = registry_credential.remove_everywhere()
    except Exception as exc:  # noqa: BLE001
        print(f"  Could not clean the registry credential: {exc}", file=sys.stderr)
        return

    cleaned = {name: locations for name, locations in removed.items() if locations}
    if not cleaned:
        print("  No registry credential configured, skipping.", file=sys.stderr)
        return
    prefix = "  [dry-run] would clean" if dry_run else "  cleaned"
    for name, locations in cleaned.items():
        print(f"{prefix} {name}: {', '.join(locations)}", file=sys.stderr)


def main(
    keep_plugin: Annotated[
        bool,
        typer.Option("--keep-plugin", help="Keep the Claude Code plugin installed"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Show what would be done without making changes"),
    ] = False,
) -> None:
    """Uninstall pysae-ai-tools and the Claude Code plugin."""
    # Step 1: Remove Claude Code plugin
    if not keep_plugin:
        print("Removing Claude Code plugin...", file=sys.stderr)
        if _uninstall_plugin(dry_run):
            print("  Claude Code plugin removed.", file=sys.stderr)
        else:
            print("  Failed to remove plugin.", file=sys.stderr)

        print("Removing Codex skills...", file=sys.stderr)
        _uninstall_codex_plugin(dry_run)

    # Step 1b: Remove the pysae-env shell integration from every shell rc.
    print("Removing pysae-env shell integration...", file=sys.stderr)
    _uninstall_shell_init(dry_run)

    # Step 1c: Remove the MCP servers registered by `tools install`.
    print("Removing managed MCP servers...", file=sys.stderr)
    _uninstall_mcp_servers(dry_run)

    # Step 1d: Clean settings.json (mcp-cleanup hook + default allow-list).
    print("Cleaning Claude settings.json...", file=sys.stderr)
    _uninstall_claude_settings(dry_run)

    # Step 1e: Remove the GitLab registry credential from uv, Node and Docker.
    print("Removing the GitLab registry credential...", file=sys.stderr)
    _uninstall_registry_credential(dry_run)

    # Step 2: Remove Python package via uv
    print(f"Removing {PACKAGE}...", file=sys.stderr)
    if _uninstall_package(dry_run):
        print(f"  {PACKAGE} removed.", file=sys.stderr)
    else:
        print(f"  Failed to remove {PACKAGE} (not installed or uv not found).", file=sys.stderr)
        raise typer.Exit(code=1)

    if not dry_run and not _deferred_cleanup_scheduled:
        # Check if another installation is still on PATH (e.g. editable install in .venv).
        # Skip the uv-managed shim — that's the one we just uninstalled, and
        # warning about it would be misleading. We also skip this check entirely
        # when a deferred cleanup was scheduled: the shim is still on disk by
        # design, the detached cmd is about to wipe it.
        remaining = shutil.which(PACKAGE)
        if remaining and not _is_uv_managed_path(remaining):
            print(f"\n⚠ Another installation found at {remaining}", file=sys.stderr)
            print("  This is likely an editable install in a local .venv.", file=sys.stderr)
            print(f"  To fully remove: pip uninstall {PACKAGE} (from that venv)", file=sys.stderr)
        print("\nDone. To reinstall:", file=sys.stderr)
        print("", file=sys.stderr)
        for line in _reinstall_commands():
            print(f"  {line}", file=sys.stderr)
        print("", file=sys.stderr)
