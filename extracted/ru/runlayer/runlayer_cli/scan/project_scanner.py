"""Scan for project-level files (MCP configs and skill artifacts) using find.

Note: macOS Spotlight (mdfind) does NOT index hidden files or files in hidden
directories, so we must use the find command instead.
"""

from __future__ import annotations

import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from runlayer_cli.scan.clients import MCPClientDefinition

logger = structlog.get_logger(__name__)


@dataclass
class ProjectConfig:
    """A discovered project-level MCP configuration."""

    config_path: Path
    project_path: Path  # Root of the project (parent of config)
    client_name: str
    servers_key: str


EXCLUDED_DIRECTORIES: list[str] = [
    "node_modules",
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    "vendor",
    "Library/Caches",
    "Library/Application Support",
    "AppData",
    ".Trash",
    "tmp",
    "temp",
    ".cache",
    ".npm",
    ".yarn",
]


def find_files_under_home(
    filenames: list[str],
    timeout: int = 60,
    max_depth: int = 5,
) -> list[Path]:
    """Find files by name under the user's home directory.

    Platform-aware: uses ``find`` on macOS/Linux, PowerShell on Windows.
    Both MCP config scanning and skill scanning share this single crawl.

    Entries containing ``/`` are treated as path-suffix patterns and matched
    with ``find -path "*/<pattern>"`` instead of ``-name``.  This prevents
    generic basenames like ``config.toml`` from flooding the crawl results.

    Args:
        filenames: Exact filenames **or** relative-path patterns to search for
                   (e.g. ``[".mcp.json", ".codex/config.toml", "SKILL.md"]``)
        timeout: Max seconds before aborting the search
        max_depth: Directory depth limit

    Returns:
        De-duplicated list of discovered file paths.
    """
    if not filenames:
        return []

    unique = sorted(set(filenames))
    system = platform.system()
    if system in ("Darwin", "Linux"):
        return _search_unix(unique, timeout, max_depth)
    if system == "Windows":
        return _search_windows(unique, timeout, max_depth)
    logger.warning("unsupported_platform_for_file_search", platform=system)
    return []


def scan_for_project_configs(
    clients: list[MCPClientDefinition],
    timeout: int = 60,
    max_depth: int = 5,
    precomputed_paths: list[Path] | None = None,
) -> list[ProjectConfig]:
    """Scan for project-level MCP configuration files.

    When *precomputed_paths* is supplied the filesystem crawl is skipped and
    results are matched against the already-discovered paths instead.  This
    lets the caller run a single ``find_files_under_home`` for both MCP and
    skill filenames and split the results afterward.

    Args:
        clients: Client definitions with ``project_config`` patterns.
        timeout: Search timeout (ignored when *precomputed_paths* given).
        max_depth: Search depth (ignored when *precomputed_paths* given).
        precomputed_paths: Optional pre-crawled paths to match against.

    Returns:
        List of discovered ``ProjectConfig`` instances.
    """
    search_patterns: dict[str, list[tuple[str, str, str | None]]] = {}
    global_config_paths: set[Path] = set()

    for client in clients:
        for pc in client.iter_project_configs():
            rel_path = pc.relative_path
            filename = Path(rel_path).name
            path_contains = None
            if "/" in rel_path:
                path_contains = rel_path.rsplit("/", 1)[0]

            if filename not in search_patterns:
                search_patterns[filename] = []
            search_patterns[filename].append(
                (
                    client.name,
                    pc.servers_key,
                    path_contains,
                )
            )

        for config_path_def in client.paths:
            resolved = config_path_def.resolve()
            if resolved is not None:
                global_config_paths.add(resolved.resolve())

    if not search_patterns:
        logger.debug("No clients with project configs to scan")
        return []

    if precomputed_paths is not None:
        found_paths = precomputed_paths
    else:
        logger.info("Scanning for project configs", max_depth=max_depth)
        find_patterns: list[str] = []
        for client in clients:
            for pc in client.iter_project_configs():
                rel = pc.relative_path
                pattern = rel if "/" in rel else Path(rel).name
                if pattern not in find_patterns:
                    find_patterns.append(pattern)
        found_paths = find_files_under_home(find_patterns, timeout, max_depth)

    found_configs: list[ProjectConfig] = []
    for path in found_paths:
        filename = path.name
        if filename not in search_patterns:
            continue

        if path.resolve() in global_config_paths:
            continue

        for client_name, servers_key, path_contains in search_patterns[filename]:
            if path_contains and path.parent.name != path_contains:
                continue

            project_path = _get_project_root(path, path_contains)

            found_configs.append(
                ProjectConfig(
                    config_path=path,
                    project_path=project_path,
                    client_name=client_name,
                    servers_key=servers_key,
                )
            )
            logger.debug("Found project config", client=client_name)

    logger.info("Project config scan complete", found=len(found_configs))
    return found_configs


def _search_unix(filenames: list[str], timeout: int, max_depth: int) -> list[Path]:
    """
    Use find command to locate MCP config files on macOS/Linux.

    Note: We use find instead of mdfind because Spotlight does NOT index
    hidden files (starting with .) or files in hidden directories.
    """
    found_paths: list[Path] = []
    home = str(Path.home())

    # Build match conditions.  Plain filenames use -name; entries with "/"
    # use -path to avoid matching generic basenames like "config.toml" everywhere.
    name_conditions: list[str] = []
    for filename in filenames:
        if "/" in filename:
            cond = ["-path", f"*/{filename}"]
        else:
            cond = ["-name", filename]
        if name_conditions:
            name_conditions.extend(["-o", *cond])
        else:
            name_conditions.extend(cond)

    # Build exclusion conditions
    exclude_conditions: list[str] = []
    for excluded in EXCLUDED_DIRECTORIES:
        exclude_conditions.extend(["!", "-path", f"*/{excluded}/*"])

    cmd = [
        "find",
        home,
        "-maxdepth",
        str(max_depth),
        "-type",
        "f",
        "(",
        *name_conditions,
        ")",
        *exclude_conditions,
    ]

    try:
        logger.debug(f"Running find command with {len(filenames)} filename patterns")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # find returns exit code 1 if some dirs are unreadable, but still outputs results
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            path = Path(line)
            if path.is_file():
                found_paths.append(path)

    except subprocess.TimeoutExpired:
        logger.warning(f"find command timed out after {timeout}s")
    except FileNotFoundError:
        logger.warning("find command not found")
    except Exception as e:
        logger.warning(f"find command failed: {e}")

    return found_paths


def _escape_powershell_string(value: str) -> str:
    """
    Escape a string for safe use in PowerShell single-quoted strings.

    In PowerShell single-quoted strings, only single quotes need escaping
    (doubled to ''). Other special characters like $, `, and " are treated
    literally within single quotes.
    """
    return value.replace("'", "''")


def _search_windows(filenames: list[str], timeout: int, max_depth: int) -> list[Path]:
    """
    Use PowerShell to find MCP config files on Windows.
    """
    found_paths: list[Path] = []
    home = str(Path.home())

    # Escape all user-controlled strings for PowerShell single-quoted context
    safe_home = _escape_powershell_string(home)
    safe_excludes = [_escape_powershell_string(d) for d in EXCLUDED_DIRECTORIES]

    # Split into plain filenames vs path-suffix patterns (contain "/")
    plain = [_escape_powershell_string(f) for f in filenames if "/" not in f]
    path_patterns = [
        _escape_powershell_string(f).replace("/", "\\") for f in filenames if "/" in f
    ]

    exclude_list = ", ".join([f"'{d}'" for d in safe_excludes])

    if not isinstance(max_depth, int) or max_depth < 0 or max_depth > 10:
        logger.warning(
            f"Invalid max_depth '{max_depth}' provided. Using default max_depth=5."
        )
        max_depth = 5

    # Build a Where-Object filter that checks plain names with -in and
    # path-suffix patterns with -like.
    clauses: list[str] = []
    if plain:
        filename_list = ", ".join([f"'{f}'" for f in plain])
        clauses.append(f"$_.Name -in @({filename_list})")
    for pp in path_patterns:
        clauses.append(f"$path -like '*\\{pp}'")
    where_match = " -or ".join(clauses) if clauses else "$false"

    cmd = f"""
    $excludeDirs = @({exclude_list})
    Get-ChildItem -Path '{safe_home}' -Recurse -Depth {max_depth} -File -Force -ErrorAction SilentlyContinue |
    Where-Object {{
        $path = $_.FullName
        ({where_match}) -and
        -not ($excludeDirs | ForEach-Object {{ $path -like "*\\$_\\*" }} | Where-Object {{ $_ }})
    }} |
    Select-Object -ExpandProperty FullName
    """

    try:
        logger.debug(
            f"Running PowerShell search with {len(filenames)} filename patterns"
        )

        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            path = Path(line)
            if path.is_file():
                found_paths.append(path)

    except subprocess.TimeoutExpired:
        logger.warning(f"PowerShell search timed out after {timeout}s")
    except Exception as e:
        logger.warning(f"PowerShell search failed: {e}")

    return found_paths


def _get_project_root(config_path: Path, path_contains: str | None) -> Path:
    """
    Determine the project root directory from a config file path.

    For ".mcp.json" -> parent directory is project root
    For ".vscode/mcp.json" -> grandparent directory is project root
    """
    if path_contains:
        # Config is in a subdirectory like .vscode/
        # Go up one more level
        return config_path.parent.parent
    else:
        # Config is at project root
        return config_path.parent
