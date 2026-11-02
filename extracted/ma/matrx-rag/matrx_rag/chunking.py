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


__all__ = [
    "CHUNKER_VERSION",
    "Chunk",
    "chunk_code",
    "chunk_text",
]
