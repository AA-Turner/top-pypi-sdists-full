"""AST-based import resolution for deep source context.

Parses Python source files to identify first-party imports that are
affected by the current diff, enabling the review LLM to understand
type definitions and interfaces used by the changed code.
"""

from __future__ import annotations

import ast
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# First-party package prefix for resolving imports.
_FIRST_PARTY_PACKAGE = "agentic_devtools"


def _parse_imports(source_code: str) -> list[dict[str, Any]]:
    """Parse import statements from Python source code.

    Args:
        source_code: Python source code string.

    Returns:
        List of import info dicts with ``module``, ``names``, ``line`` fields.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        logger.debug("AST parse failed, skipping import resolution")
        return []

    imports: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound_name = alias.asname or alias.name.split(".", 1)[0]
                imports.append(
                    {
                        "module": alias.name,
                        "names": [bound_name],
                        "line": node.lineno,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names = [alias.asname or alias.name for alias in node.names]
                imports.append(
                    {
                        "module": node.module,
                        "names": names,
                        "line": node.lineno,
                        "level": node.level,
                    }
                )
            elif node.level > 0:
                # Module-less relative import: ``from . import X`` → treat each
                # imported name as a sibling module at the same package level.
                for alias in node.names:
                    imports.append(
                        {
                            "module": alias.name,
                            "names": [alias.asname or alias.name],
                            "line": node.lineno,
                            "level": node.level,
                        }
                    )

    return imports


def _resolve_module_to_path(module_name: str) -> str | None:
    """Resolve a first-party module name to a file path.

    Only resolves modules under ``agentic_devtools/``.

    Args:
        module_name: Dotted module name (e.g., "agentic_devtools.cli.git.core").

    Returns:
        Repository-relative file path, or None if not first-party.
    """
    if module_name != _FIRST_PARTY_PACKAGE and not module_name.startswith(_FIRST_PARTY_PACKAGE + "."):
        return None

    # Convert dots to path separators
    path = module_name.replace(".", "/")

    # Could be a module file or a package
    return f"{path}.py"


def _is_import_affected(
    import_info: dict[str, Any],
    diff_lines: list[int] | None,
    source_code: str | None,
) -> bool:
    """Determine if an import is affected by the diff.

    An import is "affected" if:
    1. The diff overlaps the import statement line, OR
    2. A symbol imported from the module is referenced in changed lines

    Args:
        import_info: Import dict with module, names, line fields.
        diff_lines: List of changed line numbers (1-based), or None for all.
        source_code: Full source code (for symbol reference checking).

    Returns:
        True if the import is considered affected.
    """
    if diff_lines is None:
        # If no diff info, include all imports
        return True

    # Check if import line itself is in the diff
    if import_info["line"] in diff_lines:
        return True

    # Check if any imported symbol name appears in changed lines
    if source_code and diff_lines:
        lines = source_code.splitlines()
        imported_names = import_info.get("names", [])
        for line_no in diff_lines:
            if 1 <= line_no <= len(lines):
                line_content = lines[line_no - 1]
                for name in imported_names:
                    if re.search(r"\b" + re.escape(name) + r"\b", line_content):
                        return True

    return False


def resolve_imports(
    source_code: str,
    file_path: str,
    *,
    diff_lines: list[int] | None = None,
    visited: set[str] | None = None,
    repo_root: Path | str | None = None,
    max_depth: int = 1,
) -> list[str]:
    """Resolve affected first-party imports from a source file.

    Uses AST parsing to extract imports, filters to first-party only,
    and checks if the import is affected by the diff.  Only **direct**
    imports (depth-1) are resolved; ``max_depth`` values greater than 1
    are accepted for API compatibility but do not currently trigger
    recursive resolution.  Visited-set cycle prevention is still applied
    to the resolved paths.

    Args:
        source_code: Content of the source file.
        file_path: Path of the source file (for cycle detection).
        diff_lines: Changed line numbers (1-based) for "affected" filtering.
        visited: Set of already-visited file paths (cycle prevention).
        repo_root: Repository root for resolving module paths.  When
            ``None``, both the module-file path (``<module>.py``) and its
            package ``__init__.py`` candidate are returned without a
            filesystem existence check.
        max_depth: Reserved for future depth-limited recursion.  Must be
            a positive integer; currently only depth-1 (direct imports) is
            implemented regardless of the value supplied.

    Returns:
        List of repository-relative POSIX file paths for affected imports.
    """
    if max_depth <= 0:
        raise ValueError(f"max_depth must be a positive integer, got {max_depth!r}")

    if visited is None:
        visited = set()

    # Normalize and add current file to visited set
    clean_path = file_path.lstrip("/")
    if clean_path in visited:
        return []
    visited.add(clean_path)

    imports = _parse_imports(source_code)
    if not imports:
        return []

    resolved_paths: list[str] = []
    for import_info in imports:
        module_name = import_info["module"]
        level = import_info.get("level", 0)

        if level > 0:
            # Qualify relative import against the current file's package.
            # e.g., file agentic_devtools/cli/git/core.py, level=1, module="config"
            # → qualified name = "agentic_devtools.cli.git.config"
            pkg_parts = clean_path.replace("/", ".").removesuffix(".py").split(".")
            # Strip 'level' components from the right to obtain the base package.
            pkg_parts = pkg_parts[:-level] if level < len(pkg_parts) else []
            if pkg_parts:
                module_name = ".".join(pkg_parts + [module_name]) if module_name else ".".join(pkg_parts)
            else:
                # Relative import goes above the root — skip it.
                continue

        resolved_path = _resolve_module_to_path(module_name)
        if resolved_path is None:
            continue

        # Skip if already visited (cycle prevention)
        if resolved_path in visited:
            continue

        # Check if this import is affected by the diff
        if not _is_import_affected(import_info, diff_lines, source_code):
            continue

        # Verify file exists if repo_root provided; otherwise include both module
        # and package candidates since filesystem cannot be checked.
        if repo_root is not None:
            full_path = Path(repo_root) / resolved_path
            if not full_path.is_file():
                # Try as package __init__.py
                package_init = Path(repo_root) / resolved_path[:-3] / "__init__.py"
                if package_init.is_file():
                    resolved_path = (Path(resolved_path[:-3]) / "__init__.py").as_posix()
                else:
                    continue
        else:
            # API-only mode: include both module file and package __init__.py
            # candidates since we cannot check the filesystem.
            package_init_path = (Path(resolved_path[:-3]) / "__init__.py").as_posix()
            if package_init_path not in visited:
                resolved_paths.append(package_init_path)

        resolved_paths.append(resolved_path)

    return sorted(set(resolved_paths))
