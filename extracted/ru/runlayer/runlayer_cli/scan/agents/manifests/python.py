"""Python dependency-manifest parsers.

Covers ``pyproject.toml``, ``requirements*.txt``, ``setup.py``, ``setup.cfg``,
and the ``uv.lock`` / ``poetry.lock`` / ``Pipfile.lock`` locks. Standard library
only (``ast``, ``configparser``, ``json``, ``tomllib``/``tomli``).
"""

from __future__ import annotations

import ast
import configparser
import json
import sys
from collections.abc import Callable
from pathlib import Path

from runlayer_cli.scan.agents.manifests._common import pep508_name

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - exercised only on Python 3.10
    import tomli as tomllib


def parse_pyproject(path: Path) -> list[str]:
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: list[str] = []
    project = data.get("project", {})
    for spec in project.get("dependencies", []) or []:
        name = pep508_name(spec)
        if name:
            names.append(name)
    for group in (project.get("optional-dependencies", {}) or {}).values():
        for spec in group or []:
            name = pep508_name(spec)
            if name:
                names.append(name)
    # PEP 735 dependency groups.
    for group in (data.get("dependency-groups", {}) or {}).values():
        for spec in group or []:
            if isinstance(spec, str):
                name = pep508_name(spec)
                if name:
                    names.append(name)
    # Poetry-style table: keys are dependency names.
    poetry = data.get("tool", {}).get("poetry", {})
    for key in poetry.get("dependencies", {}) or {}:
        if key.lower() != "python":
            names.append(key)
    return names


def parse_requirements_txt(path: Path) -> list[str]:
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        # Skip blanks, comments, and pip flags (-r, -e, --hash, etc.).
        if not stripped or stripped.startswith(("#", "-")):
            continue
        # Drop inline environment markers / options after a semicolon or space.
        name = pep508_name(stripped)
        if name:
            names.append(name)
    return names


def parse_setup_py(path: Path) -> list[str]:
    """Best-effort ``setup.py`` parse: read literal install/extras requirements.

    Only static string literals inside ``install_requires`` / ``extras_require``
    are read; dynamically computed requirement lists are ignored (they cannot be
    resolved without executing the file, which we never do).
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []

    def _collect_from_list(node: ast.AST) -> None:
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            for el in node.elts:
                if isinstance(el, ast.Constant) and isinstance(el.value, str):
                    name = pep508_name(el.value)
                    if name:
                        names.append(name)

    for node in ast.walk(tree):
        if not isinstance(node, ast.keyword):
            continue
        if node.arg == "install_requires":
            _collect_from_list(node.value)
        elif node.arg == "extras_require" and isinstance(node.value, ast.Dict):
            for value in node.value.values:
                _collect_from_list(value)
    return names


def parse_setup_cfg(path: Path) -> list[str]:
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    names: list[str] = []
    raw_blocks: list[str] = []
    if parser.has_option("options", "install_requires"):
        raw_blocks.append(parser.get("options", "install_requires"))
    if parser.has_section("options.extras_require"):
        for _, value in parser.items("options.extras_require"):
            raw_blocks.append(value)
    for block in raw_blocks:
        for line in block.splitlines():
            name = pep508_name(line)
            if name:
                names.append(name)
    return names


def parse_toml_lock_packages(path: Path) -> list[str]:
    """Parse ``uv.lock`` / ``poetry.lock`` ``[[package]]`` name entries."""
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    names: list[str] = []
    for pkg in data.get("package", []) or []:
        if isinstance(pkg, dict):
            name = pkg.get("name")
            if isinstance(name, str):
                names.append(name)
    return names


def parse_pipfile_lock(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for section in ("default", "develop"):
        names.extend((data.get(section) or {}).keys())
    return names


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    "pyproject.toml": parse_pyproject,
    "requirements.txt": parse_requirements_txt,
    "setup.py": parse_setup_py,
    "setup.cfg": parse_setup_cfg,
    "uv.lock": parse_toml_lock_packages,
    "poetry.lock": parse_toml_lock_packages,
    "Pipfile.lock": parse_pipfile_lock,
}
