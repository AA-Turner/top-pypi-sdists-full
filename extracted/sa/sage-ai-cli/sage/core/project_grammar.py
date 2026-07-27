"""Project-aware grammar — make hallucinated imports impossible."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["ProjectSymbols", "extract_project_symbols", "build_import_grammar"]


@dataclass
class ProjectSymbols:
    modules: set[str] = field(default_factory=set)
    names: set[str] = field(default_factory=set)


_PY_DEF_RE = re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+(\w+)", re.MULTILINE)
_PY_DUNDER_ALL_RE = re.compile(r"__all__\s*=\s*\[([^\]]+)\]")
_JS_EXPORT_RE = re.compile(
    r"^\s*export\s+(?:default\s+)?(?:async\s+)?"
    r"(?:function\s+(\w+)|class\s+(\w+)|const\s+(\w+)|let\s+(\w+)|var\s+(\w+))",
    re.MULTILINE,
)


def _extract_py(text: str, module_path: str, syms: ProjectSymbols) -> None:
    syms.modules.add(module_path)
    for m in _PY_DEF_RE.finditer(text):
        name = m.group(1)
        if not name.startswith("_"):
            syms.names.add(name)
    for m in _PY_DUNDER_ALL_RE.finditer(text):
        body = m.group(1)
        for tok in re.findall(r"['\"](\w+)['\"]", body):
            syms.names.add(tok)


def _extract_js(text: str, module_path: str, syms: ProjectSymbols) -> None:
    syms.modules.add(module_path)
    for m in _JS_EXPORT_RE.finditer(text):
        for grp in m.groups():
            if grp:
                syms.names.add(grp)


def _module_path_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root)
    parts = list(rel.parts)
    parts[-1] = parts[-1].rsplit(".", 1)[0]
    return ".".join(parts)


def extract_project_symbols(cwd: Path, *, max_files: int = 1000) -> ProjectSymbols:
    syms = ProjectSymbols()
    seen = 0
    skip_dirs = {"node_modules", ".git", "__pycache__", ".venv", "venv",
                 "dist", "build", ".next", "target", "vendor"}
    for dirpath, dirnames, filenames in os.walk(cwd):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for name in filenames:
            ext = name.rsplit(".", 1)[-1].lower()
            if ext not in {"py", "js", "jsx", "ts", "tsx"}:
                continue
            p = Path(dirpath) / name
            try:
                text = p.read_text("utf-8", errors="replace")
            except OSError:
                continue
            mod = _module_path_for(p, cwd)
            if ext == "py":
                _extract_py(text, mod, syms)
            else:
                _extract_js(text, mod, syms)
            seen += 1
            if seen >= max_files:
                return syms
    return syms


def _gbnf_alt(items: list[str]) -> str:
    if not items:
        return r'"_no_symbols_"'
    return " | ".join(f'"{x}"' for x in sorted(items))


def build_import_grammar(syms: ProjectSymbols) -> str:
    modules = sorted(m for m in syms.modules if m and "/" not in m)[:200]
    names = sorted(syms.names)[:500]
    return (
        "root ::= line (\"\\n\" line)*\n"
        f"line ::= \"from \" module \" import \" name | \"import \" module\n"
        f"module ::= {_gbnf_alt(modules)}\n"
        f"name ::= {_gbnf_alt(names)}\n"
    )
