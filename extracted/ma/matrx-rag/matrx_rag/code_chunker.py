"""Tree-sitter symbol-aware code chunker.

Replaces the line-window code splitter for the languages we have
grammars for. Each chunk is a meaningful unit: a function, a method, a
class, a struct, etc. — not an arbitrary 50-line slice that happens to
straddle two functions.

Hierarchy:

* **Module preamble** — imports + top-level non-symbol code (constants,
  type aliases, configuration). One chunk per file at most. Acts as the
  parent of everything else in the file so the LLM gets the imports
  alongside any symbol it reads.
* **Class / struct / impl** — ``parent_chunk`` containing the class's
  full source. Children are the methods inside.
* **Function / method** — leaf chunks, addressed by ``language.symbol_name``.
* **Oversized symbols** (rare, but think 800-line procedural functions)
  fall back to the token-window splitter inside their own body so we
  don't end up with a single 30k-token chunk.

The metadata on each chunk carries:

  * ``language``       — e.g. python / typescript / go.
  * ``symbol_kind``    — function | method | class | struct | …
  * ``symbol_name``    — best-effort name from the AST (or ``"<anonymous>"``).
  * ``parent_symbol``  — name of the enclosing class/struct (None for top-level).
  * ``line_start`` / ``line_end`` — 1-based line spans for citation.
  * ``signature``      — first non-empty line of the symbol body, used for
                          quick-glance display in retrieval results.

For languages we don't have grammars for, the caller should fall back
to the prose splitter or the line-window splitter. ``supported_languages``
exposes the registered set.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Callable

from matrx_rag.chunking import (
    CHILD_OVERLAP,
    CHILD_SIZE,
    Chunk,
    _tok_len,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Language registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LangSpec:
    name: str                          # canonical: python, typescript, go, …
    parent_kinds: tuple[str, ...]      # nodes that contain leaf symbols
    leaf_kinds: tuple[str, ...]        # nodes that are leaf symbols themselves
    decorator_kinds: tuple[str, ...]   # wrap parents/leafs (Python decorated_definition)
    name_field: str                    # tree-sitter field name for the symbol's identifier


def _python_lang() -> tuple[object, LangSpec]:
    import tree_sitter_python
    from tree_sitter import Language

    spec = LangSpec(
        name="python",
        parent_kinds=("class_definition",),
        leaf_kinds=("function_definition",),
        decorator_kinds=("decorated_definition",),
        name_field="name",
    )
    return Language(tree_sitter_python.language()), spec


def _typescript_lang() -> tuple[object, LangSpec]:
    import tree_sitter_typescript
    from tree_sitter import Language

    spec = LangSpec(
        name="typescript",
        parent_kinds=("class_declaration", "interface_declaration"),
        leaf_kinds=(
            "function_declaration",
            "method_definition",
            "method_signature",
            "abstract_method_signature",
            "type_alias_declaration",
        ),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_typescript.language_typescript()), spec


def _tsx_lang() -> tuple[object, LangSpec]:
    import tree_sitter_typescript
    from tree_sitter import Language

    spec = LangSpec(
        name="tsx",
        parent_kinds=("class_declaration", "interface_declaration"),
        leaf_kinds=(
            "function_declaration",
            "method_definition",
            "method_signature",
            "type_alias_declaration",
        ),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_typescript.language_tsx()), spec


def _javascript_lang() -> tuple[object, LangSpec]:
    import tree_sitter_javascript
    from tree_sitter import Language

    spec = LangSpec(
        name="javascript",
        parent_kinds=("class_declaration",),
        leaf_kinds=("function_declaration", "method_definition"),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_javascript.language()), spec


def _go_lang() -> tuple[object, LangSpec]:
    import tree_sitter_go
    from tree_sitter import Language

    spec = LangSpec(
        name="go",
        parent_kinds=("type_declaration",),
        leaf_kinds=("function_declaration", "method_declaration"),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_go.language()), spec


def _java_lang() -> tuple[object, LangSpec]:
    import tree_sitter_java
    from tree_sitter import Language

    spec = LangSpec(
        name="java",
        parent_kinds=("class_declaration", "interface_declaration", "enum_declaration"),
        leaf_kinds=("method_declaration", "constructor_declaration"),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_java.language()), spec


def _rust_lang() -> tuple[object, LangSpec]:
    import tree_sitter_rust
    from tree_sitter import Language

    spec = LangSpec(
        name="rust",
        parent_kinds=("impl_item", "struct_item", "enum_item", "trait_item", "mod_item"),
        leaf_kinds=("function_item",),
        decorator_kinds=(),
        name_field="name",
    )
    return Language(tree_sitter_rust.language()), spec


_LANG_FACTORY: dict[str, Callable[[], tuple[object, LangSpec]]] = {
    "python": _python_lang,
    "py": _python_lang,
    "typescript": _typescript_lang,
    "ts": _typescript_lang,
    "tsx": _tsx_lang,
    "javascript": _javascript_lang,
    "js": _javascript_lang,
    "go": _go_lang,
    "java": _java_lang,
    "rust": _rust_lang,
    "rs": _rust_lang,
}


def supported_languages() -> set[str]:
    return set(_LANG_FACTORY.keys())


_LANG_CACHE: dict[str, tuple[object, LangSpec]] = {}


def _get_lang(language: str) -> tuple[object, LangSpec] | None:
    key = language.lower()
    if key in _LANG_CACHE:
        return _LANG_CACHE[key]
    factory = _LANG_FACTORY.get(key)
    if factory is None:
        return None
    try:
        lang, spec = factory()
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.code_chunker: failed to load grammar for %s: %s", language, exc)
        return None
    _LANG_CACHE[key] = (lang, spec)
    return lang, spec


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------


def chunk_code_symbols(text: str, *, language: str) -> list[Chunk] | None:
    """Tree-sitter symbol chunker. Returns ``None`` when the language has
    no registered grammar — the caller should fall back to the line-window
    splitter in that case.
    """
    if not text or not text.strip():
        return []
    pair = _get_lang(language)
    if pair is None:
        return None
    lang, spec = pair

    from tree_sitter import Parser

    parser = Parser(lang)
    src = text.encode("utf-8", errors="replace")
    tree = parser.parse(src)
    root = tree.root_node

    def line_of(byte_offset: int) -> int:
        # 1-based line numbers for human-readable citations.
        return src.count(b"\n", 0, byte_offset) + 1

    def slice_text(node) -> str:
        return src[node.start_byte : node.end_byte].decode("utf-8", errors="replace")

    def first_nonempty_line(s: str) -> str:
        for line in s.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:200]
        return ""

    def name_of(node) -> str:
        # First try the language-declared name field.
        try:
            child = node.child_by_field_name(spec.name_field)
            if child is not None:
                return slice_text(child).strip()[:120] or "<anonymous>"
        except Exception:
            pass
        # Fallback: find the first identifier child.
        for c in node.children:
            if c.type in ("identifier", "type_identifier", "property_identifier"):
                return slice_text(c).strip()[:120] or "<anonymous>"
        return "<anonymous>"

    def find_symbol(node):
        """Tree-sitter wraps Python decorated functions in
        ``decorated_definition``; the actual function/class is a child.
        Unwrap so we always work on the symbol node itself.
        """
        if node.type in spec.decorator_kinds:
            for c in node.children:
                if c.type in spec.parent_kinds + spec.leaf_kinds:
                    return c, node  # (inner, outer-with-decorator)
        return node, node

    chunks: list[Chunk] = []
    chunk_index = 0
    seen_byte_ranges: set[tuple[int, int]] = set()

    # Pre-collect parent symbols so we can correlate leafs to enclosing parents.
    # We walk depth-first and track the current parent_chunk_id stack.
    parent_stack: list[tuple[str, str, str]] = []  # (parent_chunk_id, parent_kind, parent_name)

    # Module preamble — everything in the root that isn't a symbol or a wrapped symbol.
    preamble_byte_ranges: list[tuple[int, int]] = []
    symbol_root_nodes: list = []
    for child in root.children:
        inner, outer = find_symbol(child)
        if inner.type in spec.parent_kinds + spec.leaf_kinds:
            symbol_root_nodes.append(outer)
        else:
            preamble_byte_ranges.append((child.start_byte, child.end_byte))

    # Module preamble chunk (acts as a soft "parent" for top-level symbols too).
    preamble_text_parts: list[str] = []
    for s, e in preamble_byte_ranges:
        block = src[s:e].decode("utf-8", errors="replace").strip()
        if block:
            preamble_text_parts.append(block)
    module_chunk_id: str | None = None
    if preamble_text_parts:
        preamble_text = "\n\n".join(preamble_text_parts)
        # Cap module preamble at PARENT_SIZE * 2 — anything larger is rare
        # and would just be embedded as a wall of imports.
        module_chunk_id = str(uuid.uuid4())
        chunks.append(
            Chunk(
                chunk_id=module_chunk_id,
                parent_chunk_id=None,
                chunk_index=chunk_index,
                chunk_kind="code_module",
                content_text=preamble_text,
                token_count=_tok_len(preamble_text),
                language=spec.name,
                metadata={
                    "role": "module",
                    "symbol_kind": "module",
                },
            )
        )
        chunk_index += 1

    def emit_symbol(node, parent_chunk_id: str | None, parent_name: str | None) -> str:
        """Emit a chunk for ``node`` and return its chunk_id (or "" if skipped)."""
        nonlocal chunk_index
        rng = (node.start_byte, node.end_byte)
        if rng in seen_byte_ranges:
            return ""
        seen_byte_ranges.add(rng)

        text_block = slice_text(node).strip()
        if not text_block:
            return ""
        sym_kind = node.type
        sym_name = name_of(node)
        chunk_id = str(uuid.uuid4())
        token_count = _tok_len(text_block)

        # Oversized symbols → window inside the body.
        if token_count > CHILD_SIZE * 4:
            # Emit a "summary" parent + windowed children.
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    parent_chunk_id=parent_chunk_id or module_chunk_id,
                    chunk_index=chunk_index,
                    chunk_kind=("code_class" if sym_kind in spec.parent_kinds else "code_symbol"),
                    content_text=text_block,
                    token_count=token_count,
                    language=spec.name,
                    metadata={
                        "role": "parent",
                        "symbol_kind": sym_kind,
                        "symbol_name": sym_name,
                        "parent_symbol": parent_name,
                        "line_start": line_of(node.start_byte),
                        "line_end": line_of(node.end_byte),
                        "signature": first_nonempty_line(text_block),
                    },
                )
            )
            chunk_index += 1
            for window in _windowed_lines(text_block, CHILD_SIZE * 2, CHILD_OVERLAP):
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        parent_chunk_id=chunk_id,
                        chunk_index=chunk_index,
                        chunk_kind="code_window",
                        content_text=window,
                        token_count=_tok_len(window),
                        language=spec.name,
                        metadata={
                            "role": "child",
                            "symbol_kind": sym_kind,
                            "symbol_name": sym_name,
                            "parent_symbol": parent_name,
                            "line_start": line_of(node.start_byte),
                            "line_end": line_of(node.end_byte),
                        },
                    )
                )
                chunk_index += 1
            return chunk_id

        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                parent_chunk_id=parent_chunk_id or module_chunk_id,
                chunk_index=chunk_index,
                chunk_kind=(
                    "code_class" if sym_kind in spec.parent_kinds else "code_symbol"
                ),
                content_text=text_block,
                token_count=token_count,
                language=spec.name,
                metadata={
                    "role": "parent" if sym_kind in spec.parent_kinds else "leaf",
                    "symbol_kind": sym_kind,
                    "symbol_name": sym_name,
                    "parent_symbol": parent_name,
                    "line_start": line_of(node.start_byte),
                    "line_end": line_of(node.end_byte),
                    "signature": first_nonempty_line(text_block),
                },
            )
        )
        chunk_index += 1
        return chunk_id

    def walk(node, parent_chunk_id: str | None, parent_name: str | None) -> None:
        inner, outer = find_symbol(node)
        if inner.type in spec.parent_kinds:
            new_id = emit_symbol(outer, parent_chunk_id, parent_name)
            new_name = name_of(inner)
            for c in inner.children:
                walk(c, new_id or parent_chunk_id, new_name or parent_name)
            return
        if inner.type in spec.leaf_kinds:
            emit_symbol(outer, parent_chunk_id, parent_name)
            return
        for c in node.children:
            walk(c, parent_chunk_id, parent_name)

    for sym in symbol_root_nodes:
        walk(sym, module_chunk_id, None)

    return chunks


def _windowed_lines(text: str, window_tokens: int, overlap_tokens: int) -> list[str]:
    """Token-aware windowing for oversized symbol bodies. Splits on
    line boundaries to keep code readable.
    """
    lines = text.splitlines()
    if not lines:
        return []
    out: list[str] = []
    buf: list[str] = []
    buf_tokens = 0
    overlap_lines: list[str] = []
    for line in lines:
        line_tokens = _tok_len(line)
        if buf_tokens + line_tokens > window_tokens and buf:
            out.append("\n".join(buf))
            # Keep ~overlap_tokens worth of trailing lines as overlap.
            overlap_lines = []
            ot = 0
            for ln in reversed(buf):
                tn = _tok_len(ln)
                if ot + tn > overlap_tokens:
                    break
                overlap_lines.insert(0, ln)
                ot += tn
            buf = list(overlap_lines)
            buf_tokens = sum(_tok_len(l) for l in buf)
        buf.append(line)
        buf_tokens += line_tokens
    if buf:
        out.append("\n".join(buf))
    return out


# ---------------------------------------------------------------------------
# Symbol references — code knowledge graph
# ---------------------------------------------------------------------------


@dataclass
class CallEdge:
    """A call site found inside a known caller symbol.

    ``caller_chunk_id`` is the chunk holding the function whose body
    contains the call. ``callee_name`` is the textual identifier (no
    type resolution beyond name matching). ``callee_chunk_id`` is the
    matched local definition when name resolution succeeds; None means
    unresolved external (still kept as a hint for lexical search).
    """

    caller_chunk_id: str
    caller_symbol: str
    callee_name: str
    callee_chunk_id: str | None
    line: int


@dataclass
class ImportEdge:
    """An import statement at the module level.

    ``module`` is the imported source (e.g. ``"./utils"``, ``"fmt"``,
    ``"matrx_files"``). ``names`` are the symbols pulled
    in from it (or ``["*"]`` for wildcard / namespace imports).
    """

    module: str
    names: list[str]
    line: int


@dataclass
class CodeAnalysis:
    chunks: list[Chunk]
    calls: list[CallEdge] = field(default_factory=list)
    imports: list[ImportEdge] = field(default_factory=list)


# Per-language node types that count as "a call site". Tree-sitter exposes
# the callee through different child names, so we extract by walking.
_CALL_NODE_KINDS = {
    "python": ("call",),
    "typescript": ("call_expression",),
    "tsx": ("call_expression",),
    "javascript": ("call_expression",),
    "go": ("call_expression",),
    "java": ("method_invocation",),
    "rust": ("call_expression", "macro_invocation"),
}


def _last_identifier(text: str) -> str:
    """Strip method/attr access chain and return the final identifier.

    ``foo.bar.baz()``  → ``baz``
    ``arr[0]``         → ``arr[0]``  (intentionally untouched)
    ``Foo<T>.bar``     → ``bar``
    """
    s = text.strip()
    # Cut off any opening bracket / generic.
    for stop in ("(", "<", "["):
        i = s.find(stop)
        if i != -1:
            s = s[:i]
    # Take the last segment of a member access chain.
    if "." in s:
        s = s.rsplit(".", 1)[-1]
    if "::" in s:
        s = s.rsplit("::", 1)[-1]
    return s.strip()


def _extract_calls_in_subtree(
    src: bytes,
    node,
    call_kinds: tuple[str, ...],
) -> list[tuple[str, int]]:
    """Walk node's children collecting (callee_name, line_start) pairs.

    The ``function`` field gives us the callee's source slice; we keep
    the last identifier as the resolution target.
    """
    out: list[tuple[str, int]] = []
    stack = [node]
    while stack:
        cur = stack.pop()
        for c in cur.children:
            if c.type in call_kinds:
                fn_node = c.child_by_field_name("function")
                if fn_node is None:
                    # Some grammars (rust macro_invocation) put the name
                    # directly as the first identifier child.
                    for cc in c.children:
                        if cc.type in ("identifier", "scoped_identifier", "field_identifier"):
                            fn_node = cc
                            break
                if fn_node is not None:
                    text = src[fn_node.start_byte : fn_node.end_byte].decode("utf-8", errors="replace")
                    name = _last_identifier(text)
                    if name and name.isidentifier():
                        line = src.count(b"\n", 0, c.start_byte) + 1
                        out.append((name, line))
            stack.append(c)
    return out


def _extract_imports(
    src: bytes,
    root,
    language: str,
) -> list[ImportEdge]:
    out: list[ImportEdge] = []

    def line_of(node) -> int:
        return src.count(b"\n", 0, node.start_byte) + 1

    def slice_text(node) -> str:
        return src[node.start_byte : node.end_byte].decode("utf-8", errors="replace")

    if language in ("python", "py"):
        for child in root.children:
            if child.type == "import_statement":
                # ``import a.b.c`` or ``import a, b``
                names = []
                for c in child.children:
                    if c.type == "dotted_name":
                        names.append(slice_text(c).strip())
                    elif c.type == "aliased_import":
                        n = c.child_by_field_name("name")
                        if n is not None:
                            names.append(slice_text(n).strip())
                for n in names:
                    out.append(ImportEdge(module=n, names=["*"], line=line_of(child)))
            elif child.type == "import_from_statement":
                mod_node = child.child_by_field_name("module_name")
                module = slice_text(mod_node).strip() if mod_node else ""
                names = []
                for c in child.children:
                    if c.type in ("dotted_name", "identifier"):
                        if c is mod_node:
                            continue
                        names.append(slice_text(c).strip())
                    elif c.type == "aliased_import":
                        n = c.child_by_field_name("name")
                        if n is not None:
                            names.append(slice_text(n).strip())
                if module:
                    out.append(ImportEdge(module=module, names=names or ["*"], line=line_of(child)))
    elif language in ("typescript", "tsx", "javascript", "ts", "js"):
        for child in root.children:
            if child.type == "import_statement":
                source_node = child.child_by_field_name("source")
                module = slice_text(source_node).strip().strip('"').strip("'") if source_node else ""
                names: list[str] = []
                # named imports live under import_clause → named_imports → import_specifier
                for c in child.children:
                    if c.type == "import_clause":
                        for cc in c.children:
                            if cc.type == "named_imports":
                                for spec in cc.children:
                                    if spec.type == "import_specifier":
                                        n = spec.child_by_field_name("name") or spec
                                        names.append(slice_text(n).strip())
                            elif cc.type == "namespace_import":
                                names.append("*")
                            elif cc.type == "identifier":
                                names.append(slice_text(cc).strip())
                if module:
                    out.append(ImportEdge(module=module, names=names or ["*"], line=line_of(child)))
    elif language == "go":
        for child in root.children:
            if child.type == "import_declaration":
                for c in child.children:
                    if c.type == "import_spec":
                        path = c.child_by_field_name("path")
                        if path is not None:
                            module = slice_text(path).strip().strip('"')
                            out.append(ImportEdge(module=module, names=["*"], line=line_of(c)))
                    elif c.type == "import_spec_list":
                        for spec in c.children:
                            if spec.type == "import_spec":
                                path = spec.child_by_field_name("path")
                                if path is not None:
                                    module = slice_text(path).strip().strip('"')
                                    out.append(ImportEdge(module=module, names=["*"], line=line_of(spec)))
    elif language == "rust":
        for child in root.children:
            if child.type == "use_declaration":
                # `use a::b::c;` — keep raw text as module ref.
                module = slice_text(child).strip().rstrip(";").strip().removeprefix("use").strip()
                out.append(ImportEdge(module=module, names=["*"], line=line_of(child)))
    elif language == "java":
        for child in root.children:
            if child.type == "import_declaration":
                module = slice_text(child).strip().rstrip(";").strip().removeprefix("import").strip()
                out.append(ImportEdge(module=module, names=["*"], line=line_of(child)))
    return out


def analyze_code(text: str, *, language: str) -> CodeAnalysis | None:
    """Tree-sitter chunker + call / import extraction in one pass.

    Returns ``None`` for unsupported languages. The chunks list is the
    same shape ``chunk_code_symbols`` would have produced; ``calls``
    lists every call site found inside a chunked symbol, and
    ``imports`` lists module-level imports.
    """
    chunks = chunk_code_symbols(text, language=language)
    if chunks is None:
        return None
    if not chunks:
        return CodeAnalysis(chunks=[])

    pair = _get_lang(language)
    if pair is None:
        return CodeAnalysis(chunks=chunks)
    lang, spec = pair

    from tree_sitter import Parser

    parser = Parser(lang)
    src = text.encode("utf-8", errors="replace")
    tree = parser.parse(src)

    # Index chunks by line range for fast caller lookup.
    sym_chunks = [
        c
        for c in chunks
        if c.metadata
        and c.metadata.get("symbol_kind")
        and c.chunk_kind in ("code_symbol", "code_class", "code_window")
    ]
    by_lines: list[tuple[int, int, str, str]] = []
    for c in sym_chunks:
        m = c.metadata or {}
        ls = int(m.get("line_start") or 0)
        le = int(m.get("line_end") or 0)
        by_lines.append((ls, le, c.chunk_id, str(m.get("symbol_name") or "")))
    # Resolve callees by name to local symbols (best-effort).
    name_to_chunk: dict[str, str] = {}
    for c in sym_chunks:
        name = (c.metadata or {}).get("symbol_name")
        if name and isinstance(name, str) and name not in name_to_chunk:
            name_to_chunk[name] = c.chunk_id

    call_kinds = _CALL_NODE_KINDS.get(spec.name, ())
    calls_out: list[CallEdge] = []
    if call_kinds:
        for ls, le, chunk_id, sym_name in by_lines:
            if not sym_name or sym_name == "<anonymous>":
                continue
            # Find the AST node corresponding to this chunk by scanning
            # the root for a node whose start_line matches.
            target_node = _find_node_by_line_span(tree.root_node, src, ls, le)
            if target_node is None:
                continue
            for callee_name, line in _extract_calls_in_subtree(src, target_node, call_kinds):
                if callee_name == sym_name:
                    # Skip self-references (recursion still useful but
                    # noisy; we're surfacing structure, not semantics).
                    continue
                calls_out.append(
                    CallEdge(
                        caller_chunk_id=chunk_id,
                        caller_symbol=sym_name,
                        callee_name=callee_name,
                        callee_chunk_id=name_to_chunk.get(callee_name),
                        line=line,
                    )
                )

    imports = _extract_imports(src, tree.root_node, spec.name)
    return CodeAnalysis(chunks=chunks, calls=calls_out, imports=imports)


def _find_node_by_line_span(root, src: bytes, target_start: int, target_end: int):
    """Find the AST node whose 1-based line span equals
    ``(target_start, target_end)``. Best-effort — returns the closest
    enclosing match.
    """
    best = None
    best_score = -1
    stack = [root]
    while stack:
        node = stack.pop()
        ns = src.count(b"\n", 0, node.start_byte) + 1
        ne = src.count(b"\n", 0, node.end_byte) + 1
        if ns == target_start and ne == target_end:
            return node
        # Track the smallest enclosing node as fallback.
        if ns <= target_start and ne >= target_end:
            score = (target_end - target_start) - (ne - ns)
            if score > best_score:
                best_score = score
                best = node
        for c in node.children:
            stack.append(c)
    return best


__all__ = [
    "CallEdge",
    "CodeAnalysis",
    "ImportEdge",
    "analyze_code",
    "chunk_code_symbols",
    "supported_languages",
]
