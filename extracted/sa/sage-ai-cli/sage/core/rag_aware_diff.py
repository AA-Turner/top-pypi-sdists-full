"""Item #5 — RAG-aware diff: flag references to symbols not in the project."""

from __future__ import annotations

import re
from dataclasses import dataclass

from sage.core.project_grammar import ProjectSymbols

__all__ = ["UnknownReference", "flag_unknown_references"]


@dataclass
class UnknownReference:
    name: str
    line: int
    context: str


_PY_FROM_IMPORT = re.compile(r"^\s*from\s+\S+\s+import\s+(.+?)(?:\s+as\s+\S+)?\s*$", re.MULTILINE)
_PY_FUNC_CALL = re.compile(r"\b([a-zA-Z_]\w*)\s*\(")


def flag_unknown_references(code: str, syms: ProjectSymbols, *,
                             language: str = "python") -> list[UnknownReference]:
    flags: list[UnknownReference] = []
    if not code or not syms.names:
        return flags

    # Stdlib + common builtins we never flag
    builtins = {
        "print", "len", "range", "isinstance", "type", "str", "int", "float",
        "list", "dict", "set", "tuple", "bool", "bytes", "bytearray",
        "open", "input", "id", "getattr", "setattr", "hasattr", "delattr",
        "abs", "min", "max", "sum", "any", "all", "sorted", "reversed",
        "enumerate", "zip", "map", "filter", "iter", "next",
    }

    # Catch `from x import nonexistent`
    if language == "python":
        for m in _PY_FROM_IMPORT.finditer(code):
            names_str = m.group(1)
            line = code[:m.start()].count("\n") + 1
            for n in re.split(r"\s*,\s*", names_str):
                n = n.strip()
                if not n:
                    continue
                if n not in syms.names and n not in builtins:
                    flags.append(UnknownReference(
                        name=n, line=line,
                        context=m.group(0).strip(),
                    ))

    return flags
