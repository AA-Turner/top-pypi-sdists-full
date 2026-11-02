"""Rename a dev deploy's top-level packages so two dev deploys cannot collide.

``DataBaasS3DagBundle`` appends every bundle directory to the dag-processor's
process-wide ``sys.path``. Two dev deploys shipping a same-named top-level
package then compete for one module name, and which copy wins differs per
pod (DAT-202). Suffixing each top-level package and module with the dev key
removes the collision.

``dags/`` is left alone because Airflow loads it by path, as are dotfiles.
Only absolute imports are rewritten; relative ones stay inside their package.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from databaas_utils.errors import LakehouseError

_SKIPPED_DIR = "dags"
_AIRFLOWIGNORE = ".airflowignore"


class NamespacingError(LakehouseError):
    """Renaming left the tree broken, so the deploy was stopped."""


def suffix_for(dev_key: str) -> str:
    """``_<dev_key>`` as a valid identifier suffix."""
    ident = dev_key.replace("-", "_")
    if ident[:1].isdigit():
        ident = "_" + ident
    return f"_{ident}"


def _rename_maps(directory: Path, suffix: str) -> tuple[dict[str, str], dict[str, str]]:
    """Module renames and on-disk renames; they differ for single ``.py`` files."""
    modules: dict[str, str] = {}
    paths: dict[str, str] = {}
    for entry in sorted(directory.iterdir()):
        if entry.name.startswith(".") or entry.name == _SKIPPED_DIR:
            continue
        if entry.is_dir() and any(entry.rglob("*.py")):
            modules[entry.name] = entry.name + suffix
            paths[entry.name] = entry.name + suffix
        elif entry.is_file() and entry.suffix == ".py":
            modules[entry.stem] = entry.stem + suffix
            paths[entry.name] = entry.stem + suffix + ".py"
    return modules, paths


def _rewrite_ref(dotted: str, modules: dict[str, str]) -> str | None:
    top, _, rest = dotted.partition(".")
    if top not in modules:
        return None
    return modules[top] + ("." + rest if rest else "")


def _rewrite_imports(path: Path, modules: dict[str, str]) -> None:
    source = path.read_text()
    tree = ast.parse(source, filename=str(path))
    starts = [0]
    for line in source.splitlines(keepends=True):
        starts.append(starts[-1] + len(line))

    def offset(lineno: int, col: int) -> int:
        return starts[lineno - 1] + col

    edits: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue
            renamed = _rewrite_ref(node.module, modules)
            names = [(node.module, renamed)] if renamed else []
        elif isinstance(node, ast.Import):
            names = [
                (alias.name, new)
                for alias in node.names
                if (new := _rewrite_ref(alias.name, modules))
            ]
        else:
            continue
        if not names:
            continue
        start = offset(node.lineno, node.col_offset)
        end = offset(node.end_lineno or node.lineno, node.end_col_offset or 0)
        statement = source[start:end]
        rewritten = statement
        for old, new in names:
            rewritten = re.sub(rf"\b{re.escape(old)}\b", new, rewritten, count=1)
        if rewritten != statement:
            edits.append((start, end, rewritten))

    if not edits:
        return
    text = source
    for start, end, new_text in sorted(edits, reverse=True):
        text = text[:start] + new_text + text[end:]
    path.write_text(text)


def _rewrite_airflowignore(directory: Path, modules: dict[str, str]) -> None:
    ignore = directory / _AIRFLOWIGNORE
    if not ignore.exists():
        return
    lines = []
    for line in ignore.read_text().splitlines(keepends=True):
        name = line.strip().strip("/")
        lines.append(line.replace(name, modules[name]) if name in modules else line)
    ignore.write_text("".join(lines))


def namespace_packages(directory: Path, dev_key: str) -> dict[str, str]:
    """Suffix `directory`'s top-level packages and modules with `dev_key`, in place.

    Rewrites absolute imports of them in every ``.py`` file and their entries
    in ``.airflowignore``. Only call it on a staged copy.

    Returns:
        The module renames, old name to new.

    Raises:
        NamespacingError: If a file does not parse, before or after renaming,
            or a renamed path is left behind.
    """
    modules, paths = _rename_maps(directory, suffix_for(dev_key))
    if not modules:
        return {}
    for py_file in directory.rglob("*.py"):
        try:
            _rewrite_imports(py_file, modules)
        except SyntaxError as exc:
            raise NamespacingError(
                f"cannot namespace {py_file.relative_to(directory)}: {exc}"
            ) from exc
    for old, new in paths.items():
        (directory / old).rename(directory / new)
    _rewrite_airflowignore(directory, modules)

    left = [old for old in paths if (directory / old).exists()]
    if left:
        raise NamespacingError(f"still present after renaming: {', '.join(left)}")
    broken = []
    for py_file in directory.rglob("*.py"):
        try:
            ast.parse(py_file.read_text(), filename=str(py_file))
        except SyntaxError as exc:
            broken.append(f"{py_file.relative_to(directory)}: {exc}")
    if broken:
        raise NamespacingError("namespacing broke " + "; ".join(broken))
    return modules
