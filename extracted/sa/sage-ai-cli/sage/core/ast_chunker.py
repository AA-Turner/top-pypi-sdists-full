"""AST-aware chunking for RAG.

Default chunker in core/rag.py splits files at fixed line windows. That's
fast but breaks function bodies in half — the model retrieves only the
first 80 lines of `def big_function(...)`, missing the rest.

AST-aware chunking splits on *symbol* boundaries: each function, class,
or top-level block becomes its own chunk. Retrieval becomes semantically
tight: "how does foo work?" → returns the entire `foo` function.

Backend strategy:
  - tree-sitter (multi-language) when installed
  - regex fallback for Python (def/class), JS/TS (function/class/const)
  - linewise fallback if neither matches

Output is a list of `Chunk` objects matching `core/rag.py:Chunk`.
"""

from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "AstChunk",
    "chunk_ast",
    "chunk_python_regex",
    "chunk_jsts_regex",
    "available_backend",
]


@dataclass
class AstChunk:
    file_path: str
    start_line: int
    end_line: int
    text: str
    symbol: str = ""           # "function:foo" or "class:Bar" or "block:n"
    language: str = ""


# ── Tree-sitter backend (optional) ─────────────────────────────────────

def _have_tree_sitter() -> bool:
    return importlib.util.find_spec("tree_sitter") is not None


# Languages we can chunk via tree-sitter when the parser is installed.
_TS_PARSERS = {
    ".py":   "python",
    ".js":   "javascript",
    ".jsx":  "javascript",
    ".ts":   "typescript",
    ".tsx":  "typescript",
    ".rs":   "rust",
    ".go":   "go",
    ".java": "java",
    ".cpp":  "cpp",
    ".c":    "c",
    ".rb":   "ruby",
}

_SYMBOL_NODE_TYPES = {
    "function_definition", "function_declaration", "method_definition",
    "class_definition", "class_declaration",
    "function_item", "impl_item",                     # Rust
    "function_declaration",                           # Go
    "method_declaration",                             # Java
}


def chunk_with_tree_sitter(text: str, language: str, file_path: str) -> list[AstChunk] | None:
    """Try tree-sitter chunking; return None if backend unavailable."""
    if not _have_tree_sitter():
        return None
    try:
        # tree-sitter-languages bundles parsers for everything
        from tree_sitter_languages import get_parser  # type: ignore
        parser = get_parser(language)
    except Exception:
        return None
    tree = parser.parse(text.encode("utf-8"))
    chunks: list[AstChunk] = []
    lines = text.split("\n")
    cursor = tree.walk()
    visited = set()

    def emit(node, symbol_name: str) -> None:
        sl = node.start_point[0] + 1
        el = node.end_point[0] + 1
        body = "\n".join(lines[sl - 1: el])
        chunks.append(AstChunk(
            file_path=file_path,
            start_line=sl, end_line=el,
            text=body, symbol=symbol_name, language=language,
        ))

    def walk(node):
        node_id = (node.start_byte, node.end_byte, node.type)
        if node_id in visited:
            return
        visited.add(node_id)
        if node.type in _SYMBOL_NODE_TYPES:
            # Try to capture symbol name from a child of type "identifier"
            name = ""
            for child in node.children:
                if child.type in ("identifier", "type_identifier", "property_identifier"):
                    name = child.text.decode("utf-8", errors="replace")
                    break
            emit(node, f"{node.type}:{name}" if name else node.type)
            return
        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return chunks or None


# ── Regex fallbacks ──────────────────────────────────────────────────

_PY_DEF_RE = re.compile(r"^(?P<indent>\s*)(?:async\s+)?(def|class)\s+(?P<name>\w+)", re.MULTILINE)
_JSTS_DEF_RE = re.compile(
    r"^(?:export\s+)?(?:async\s+)?"
    r"(?:function\s+(?P<fn>\w+)|class\s+(?P<cls>\w+)|const\s+(?P<arrow>\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)",
    re.MULTILINE,
)


def _slice_lines(text: str, start_zero: int, end_zero: int) -> str:
    return "\n".join(text.split("\n")[start_zero:end_zero])


def chunk_python_regex(text: str, file_path: str) -> list[AstChunk]:
    lines = text.split("\n")
    matches = list(_PY_DEF_RE.finditer(text))
    if not matches:
        return []
    chunks: list[AstChunk] = []
    starts: list[tuple[int, str]] = []
    for m in matches:
        line_no = text[:m.start()].count("\n")
        starts.append((line_no, m.group("name")))
    for i, (sl, name) in enumerate(starts):
        el = starts[i + 1][0] if i + 1 < len(starts) else len(lines)
        body = "\n".join(lines[sl:el])
        chunks.append(AstChunk(
            file_path=file_path, start_line=sl + 1, end_line=el,
            text=body, symbol=f"py:{name}", language="python",
        ))
    return chunks


def chunk_jsts_regex(text: str, file_path: str) -> list[AstChunk]:
    lines = text.split("\n")
    matches = list(_JSTS_DEF_RE.finditer(text))
    if not matches:
        return []
    chunks: list[AstChunk] = []
    for i, m in enumerate(matches):
        sl = text[:m.start()].count("\n")
        el = text[:matches[i + 1].start()].count("\n") if i + 1 < len(matches) else len(lines)
        name = m.group("fn") or m.group("cls") or m.group("arrow") or "anon"
        chunks.append(AstChunk(
            file_path=file_path, start_line=sl + 1, end_line=el,
            text="\n".join(lines[sl:el]), symbol=f"js:{name}", language="javascript",
        ))
    return chunks


# ── Public entry ─────────────────────────────────────────────────────

def available_backend() -> str:
    return "tree-sitter" if _have_tree_sitter() else "regex"


def chunk_ast(path: Path, *, root: Path | None = None) -> list[AstChunk]:
    """Chunk a file by symbol boundaries; returns [] for unsupported files."""
    try:
        text = path.read_text("utf-8", errors="replace")
    except OSError:
        return []
    if not text.strip():
        return []
    rel = str(path.relative_to(root)) if root else str(path)
    suffix = path.suffix.lower()
    language = _TS_PARSERS.get(suffix, "")

    if language:
        chunks = chunk_with_tree_sitter(text, language, rel)
        if chunks:
            return chunks

    # Regex fallback by file type
    if suffix == ".py":
        chunks = chunk_python_regex(text, rel)
        if chunks:
            return chunks
    if suffix in {".js", ".jsx", ".ts", ".tsx"}:
        chunks = chunk_jsts_regex(text, rel)
        if chunks:
            return chunks

    # Linewise fallback (mirrors rag._chunk_file behaviour)
    lines = text.split("\n")
    return [AstChunk(
        file_path=rel, start_line=1, end_line=len(lines),
        text=text, symbol="block:0", language=language or "unknown",
    )]
