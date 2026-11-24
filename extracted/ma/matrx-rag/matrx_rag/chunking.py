"""Hierarchical text chunking — Phase 1.

Produces the parent/child chunk structure described in the architecture doc:

* **Parent chunks** (~1500 tokens): the unit the LLM reads at generation
  time. Big enough to be semantically self-contained.
* **Child chunks**  (~300 tokens, 50-token overlap): the unit retrieval
  matches against. Small enough that a hit is a tight match.

Each child chunk carries ``parent_chunk_id`` pointing to the parent that
contains its content. The hybrid search returns child hits; generation
expands them to their parents for context.

Phase 1 covers two chunkers:

* ``recursive_text`` — langchain RecursiveCharacterTextSplitter on prose
  (md / txt / notes / cloud-files plain text).
* ``code_lines``     — line-based split on code, ~250-line parents and
  ~50-line children. Tree-sitter (Phase 1.5) will replace this.

Output shape is plain Python dicts — Pydantic shaping happens upstream in
``rag_actions``.
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache

import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

from matrx_rag.secret_guard import guard_text
from matrx_utils.splitting import count_tokens

CHUNKER_VERSION = "v1"

# Use cl100k_base — used by OpenAI's text-embedding-3-* and gpt-4 family.
# Voyage uses its own tokenizer; for chunking we just need a stable token
# proxy, not exact counts per provider.
#
# Resolved LAZILY and cached: `tiktoken.get_encoding` performs a live HTTPS
# fetch of the BPE asset on a cold host. At module scope that made importing
# this module — and therefore booting anything that imports it — depend on a
# third-party CDN, and it broke offline/air-gapped installs and the slot
# census. Never move this call back to import time.
@lru_cache(maxsize=1)
def _encoding() -> tiktoken.Encoding:
    return tiktoken.get_encoding("cl100k_base")


def _tok_len(text: str) -> int:
    # THE platform token count (matrx_utils.splitting.count_tokens — same encoding),
    # so a RAG parent and a data.batch part measure a page identically.
    return count_tokens(text or "")


@dataclass
class Chunk:
    """A single chunk record bound for ``rag.kg_chunks``.

    chunk_id is allocated client-side so that the embed step and the
    upsert step can co-reference rows without round-tripping the DB.
    """

    chunk_id: str
    parent_chunk_id: str | None
    chunk_index: int
    chunk_kind: str
    content_text: str
    token_count: int
    language: str | None = None
    metadata: dict[str, object] | None = None


# ---------------------------------------------------------------------------
# recursive_text — prose
# ---------------------------------------------------------------------------

PARENT_SIZE = 1500
PARENT_OVERLAP = 0
CHILD_SIZE = 300
CHILD_OVERLAP = 50


def chunk_text(text: str, *, language: str | None = None) -> list[Chunk]:
    """Hierarchical chunking for prose. Returns a flat list with parents
    first, then children, each child carrying ``parent_chunk_id``.
    """
    text = (text or "").strip()
    if not text:
        return []
    # LAST SEAM before a value can become a stored row. sources.resolve()
    # already guarded everything that came through it, and redaction is
    # idempotent — so this pass normally finds nothing and costs one regex
    # sweep. It earns its keep for the callers that build their own
    # ResolvedSource and never touch resolve(): the PDF and image pipelines,
    # and the rag.* workflow actions that are handed raw text.
    text, _count, _names = guard_text(text, where="chunking.chunk_text")

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_SIZE,
        chunk_overlap=PARENT_OVERLAP,
        length_function=_tok_len,
        is_separator_regex=False,
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_SIZE,
        chunk_overlap=CHILD_OVERLAP,
        length_function=_tok_len,
        is_separator_regex=False,
    )

    out: list[Chunk] = []
    idx = 0
    parent_blocks = parent_splitter.split_text(text)
    for parent_idx, parent_block in enumerate(parent_blocks):
        parent_id = str(uuid.uuid4())
        out.append(
            Chunk(
                chunk_id=parent_id,
                parent_chunk_id=None,
                chunk_index=idx,
                chunk_kind="text",
                content_text=parent_block,
                token_count=_tok_len(parent_block),
                language=language,
                metadata={"role": "parent", "parent_index": parent_idx},
            )
        )
        idx += 1
        for child_block in child_splitter.split_text(parent_block):
            if _same_text(child_block, parent_block):
                # A parent too small to split would get ONE child with its exact
                # text: a duplicate row, a second embedding, and the same passage
                # twice in search. The parent stays a leaf and is its own context.
                continue
            out.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    parent_chunk_id=parent_id,
                    chunk_index=idx,
                    chunk_kind="text",
                    content_text=child_block,
                    token_count=_tok_len(child_block),
                    language=language,
                    metadata={"role": "child", "parent_index": parent_idx},
                )
            )
            idx += 1
    return out


# ---------------------------------------------------------------------------
# sections — workbook sheets, document sections, deck slides
# ---------------------------------------------------------------------------

#: Source kinds whose resolved text is a sequence of titled sections (workbook sheets,
#: document headings, deck slides): chunked one section at a time, never across a boundary.
SECTIONED_KINDS: frozenset[str] = frozenset({"workbook", "udt_document", "deck"})

_SECTION_HEADING = re.compile(r"^(#{1,6})\s+(\S.*)$")


def split_sections(text: str, *, kind: str) -> list[tuple[str, str]]:
    """Split rendered text into ``(heading_trail, body)`` sections.

    ``workbook`` / ``deck``: every ``## `` line opens a sheet / slide (``#`` is the record's own title
    and prefixes every section's trail). ``udt_document``: every heading of any level opens a section;
    the trail is the heading path (``Title > H1 > H2``). Text before the first heading is its own
    section under the title. Fenced code is not special: renderers never emit fences.
    """
    lines = (text or "").strip().splitlines()
    title = ""
    trail: list[tuple[int, str]] = []
    sections: list[tuple[str, list[str]]] = []
    current: list[str] = []
    current_trail = ""

    def flush() -> None:
        nonlocal current
        body = "\n".join(current).strip()
        if body:
            sections.append((current_trail, [body]))
        current = []

    for line in lines:
        m = _SECTION_HEADING.match(line)
        if m is None:
            current.append(line)
            continue
        level, name = len(m.group(1)), m.group(2).strip()
        if level == 1 and not title and not sections and not "".join(current).strip():
            title = name
            current_trail = title
            continue
        if kind in ("workbook", "deck") and level != 2:
            current.append(line)
            continue
        if level == 1 and name == title and not trail:
            flush()  # the document body repeats its own title as the first heading
            continue
        flush()
        trail = [(lv, nm) for lv, nm in trail if lv < level] + [(level, name)]
        current_trail = " > ".join(([title] if title else []) + [nm for _lv, nm in trail])
    flush()
    return [(t, b[0]) for t, b in sections]


def chunk_sections(text: str, *, kind: str, language: str | None = None) -> list[Chunk]:
    """Hierarchical chunking per section (:func:`split_sections`), reusing :func:`chunk_text`.

    Each section is chunked on its own, so a chunk never straddles two sheets, sections or slides, and
    every chunk's text opens with its section trail (``Title > Sheet``) — that line is what lets a hit
    name where it came from. ``metadata['section']`` carries the trail. Falls back to plain
    :func:`chunk_text` when the text has no sections.
    """
    sections = split_sections(text, kind=kind)
    if not sections:
        return chunk_text(text, language=language)
    out: list[Chunk] = []
    for trail, body in sections:
        section_text = f"[{trail}]\n{body}" if trail else body
        for ch in chunk_text(section_text, language=language):
            ch.chunk_index = len(out)
            ch.metadata = {**(ch.metadata or {}), "section": trail}
            if trail and not ch.content_text.startswith(f"[{trail}]"):
                # A later child of a long section: carry the trail so the hit still names its sheet / slide.
                ch.content_text = f"[{trail}]\n{ch.content_text}"
                ch.token_count = _tok_len(ch.content_text)
            out.append(ch)
    return out


# ---------------------------------------------------------------------------
# code_lines — naive line-based code chunking until tree-sitter lands
# ---------------------------------------------------------------------------

CODE_PARENT_LINES = 250
CODE_CHILD_LINES = 50
CODE_CHILD_OVERLAP_LINES = 5


def chunk_code(text: str, *, language: str | None = None) -> list[Chunk]:
    """Line-window chunker for code. Phase 1.5 replaces this with a
    tree-sitter symbol chunker that splits on function/class boundaries.
    """
    text = text or ""
    if not text.strip():
        return []
    # Same last-seam guard as chunk_text — code files are where .env dumps,
    # config blobs and pasted tokens live.
    text, _count, _names = guard_text(text, where="chunking.chunk_code")
    lines = text.splitlines()
    if not lines:
        return []

    out: list[Chunk] = []
    idx = 0
    for parent_start, parent_text in _windows(lines, CODE_PARENT_LINES, 0):
        parent_id = str(uuid.uuid4())
        out.append(
            Chunk(
                chunk_id=parent_id,
                parent_chunk_id=None,
                chunk_index=idx,
                chunk_kind="code_window",
                content_text=parent_text,
                token_count=_tok_len(parent_text),
                language=language,
                metadata={
                    "role": "parent",
                    "line_start": parent_start,
                    "line_end": parent_start + len(parent_text.splitlines()),
                },
            )
        )
        idx += 1
        for child_start, child_text in _windows(
            parent_text.splitlines(),
            CODE_CHILD_LINES,
            CODE_CHILD_OVERLAP_LINES,
        ):
            if _same_text(child_text, parent_text):
                continue  # a short window's single child IS the window (see chunk_text)
            out.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    parent_chunk_id=parent_id,
                    chunk_index=idx,
                    chunk_kind="code_window",
                    content_text=child_text,
                    token_count=_tok_len(child_text),
                    language=language,
                    metadata={
                        "role": "child",
                        "line_start": parent_start + child_start,
                        "line_end": parent_start + child_start + len(child_text.splitlines()),
                    },
                )
            )
            idx += 1
    return out


def _same_text(a: str, b: str) -> bool:
    """Equal up to whitespace — the test for a child that would duplicate its parent."""
    return " ".join((a or "").split()) == " ".join((b or "").split())


def _windows(lines: list[str], window: int, overlap: int) -> Iterator[tuple[int, str]]:
    if window <= 0:
        return
    step = max(1, window - overlap)
    for i in range(0, len(lines), step):
        block = lines[i : i + window]
        if not block:
            continue
        yield i, "\n".join(block)
        if i + window >= len(lines):
            return


# ---------------------------------------------------------------------------
# Bounded chunk-row writes
# ---------------------------------------------------------------------------

# One kg_chunks INSERT statement carries at most this many rows and this
# many bytes of content_text. Every inserted row runs five row triggers and
# feeds two GIN indexes over its text (trigram + tsvector), so the cost of one
# statement grows with the TEXT it carries, not the row count: a single
# 1,400-page note sent as ONE multi-row INSERT ran past the pool's 10 s
# statement timeout (ops.system_error 57014 on kg_chunks, 2026-11-02..13)
# and the note never became searchable. Code-reviewed constants, not env vars.
CHUNK_WRITE_BATCH_ROWS = 100
CHUNK_WRITE_BATCH_BYTES = 200_000


def chunk_row_write_batches(
    rows: list[dict],
    *,
    max_rows: int | None = None,
    max_bytes: int | None = None,
) -> list[list[dict]]:
    """Split kg_chunks rows into insert batches bounded by row count AND text size.

    Every writer of the chunk table (``KgChunks``) sends its rows through this, one INSERT
    per batch, inside its own transaction (atomicity is unchanged: the batches
    share the caller's transaction). Parents are ordered before their children
    (``parent_chunk_id`` is a self-referencing foreign key checked at the end
    of each statement, so a child may never land in an earlier batch than its
    parent). A single row larger than ``max_bytes`` gets a batch of its own.
    """
    max_rows = CHUNK_WRITE_BATCH_ROWS if max_rows is None else max_rows
    max_bytes = CHUNK_WRITE_BATCH_BYTES if max_bytes is None else max_bytes
    if max_rows < 1 or max_bytes < 1:
        raise ValueError("chunk_row_write_batches: max_rows and max_bytes must be positive")

    # Parent-first order, stable otherwise: a row is emitted once the parent
    # it names is either outside this set (already stored) or emitted.
    ids_in_set = {str(r.get("id")) for r in rows if r.get("id") is not None}
    ordered: list[dict] = []
    emitted: set[str] = set()
    pending = list(rows)
    while pending:
        remaining: list[dict] = []
        for row in pending:
            parent = row.get("parent_chunk_id")
            parent_key = str(parent) if parent is not None else None
            if parent_key is None or parent_key not in ids_in_set or parent_key in emitted:
                ordered.append(row)
                if row.get("id") is not None:
                    emitted.add(str(row["id"]))
            else:
                remaining.append(row)
        if len(remaining) == len(pending):
            # A parent cycle inside one write cannot be satisfied by any order;
            # keep the caller's order and let the database name the defect.
            ordered.extend(remaining)
            break
        pending = remaining

    batches: list[list[dict]] = []
    current: list[dict] = []
    current_bytes = 0
    for row in ordered:
        size = len((row.get("content_text") or "").encode("utf-8"))
        if current and (len(current) >= max_rows or current_bytes + size > max_bytes):
            batches.append(current)
            current, current_bytes = [], 0
        current.append(row)
        current_bytes += size
    if current:
        batches.append(current)
    return batches


__all__ = [
    "CHUNKER_VERSION",
    "CHUNK_WRITE_BATCH_BYTES",
    "CHUNK_WRITE_BATCH_ROWS",
    "Chunk",
    "chunk_code",
    "chunk_row_write_batches",
    "chunk_text",
]
