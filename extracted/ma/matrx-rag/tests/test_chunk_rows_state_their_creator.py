"""Every rag.kg_chunks row the ingest builds states ``created_by`` — and ONLY ``created_by``.

1153 (2026-09-26) gave rag.kg_chunks the canonical base contract; the owner-column retirement
(migrations 1192-1194, 2026-09-26) makes ``created_by`` the one owner column and retires the legacy
``owner_id``. The ingest writes as the service role with no ``app.user_id``, so
``platform._stamp_actor`` has nobody to stamp — the writer must state ``created_by`` itself (the
Source's owner). Until the legacy column drops, the DB trigger ``_0_owner_mirror`` fills
``owner_id`` from ``created_by``; after the drop, a writer still naming ``owner_id`` would fail every
insert. So a chunk row states ``created_by`` and never ``owner_id``.

The guard is structural on purpose: it finds every dict literal in the package that builds a chunk
row (it carries ``source_kind``, ``source_id``, ``chunk_index`` and ``content_text``) — so a fifth
writer added tomorrow is caught without anyone remembering to list it here.

Proven red, then green (2026-09-26): against the writers that stated both keys this failed naming
ingestion.py, derivation.py, stages.py and extraction_indexing.py; green after they stated only
created_by.
"""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "matrx_rag"
CHUNK_KEYS = {"source_kind", "source_id", "chunk_index", "content_text"}


def _chunk_row_dicts() -> list[tuple[str, int, dict[str, ast.expr]]]:
    found = []
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            keys = {
                k.value: v
                for k, v in zip(node.keys, node.values, strict=True)
                if isinstance(k, ast.Constant) and isinstance(k.value, str)
            }
            if CHUNK_KEYS <= keys.keys():
                found.append((str(path.relative_to(PACKAGE)), node.lineno, keys))
    return found


def test_the_guard_sees_the_known_writers() -> None:
    files = {f for f, _, _ in _chunk_row_dicts()}
    assert {"ingestion.py", "derivation.py", "stages.py", "extraction_indexing.py"} <= files, files


def test_every_chunk_row_states_created_by_and_never_owner_id() -> None:
    wrong = []
    for file, line, keys in _chunk_row_dicts():
        if "created_by" not in keys:
            wrong.append(f"{file}:{line} (no created_by)")
        if "owner_id" in keys:
            wrong.append(f"{file}:{line} (still writes the retired owner_id)")
    assert not wrong, (
        "chunk rows must state created_by (the ingest has no auth.uid(), so _stamp_actor leaves it "
        "NULL) and must not write owner_id (retired; dropped after Stage A): " + ", ".join(wrong)
    )
