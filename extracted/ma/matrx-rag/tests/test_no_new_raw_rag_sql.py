"""Structural guard — the 'never again' enforcement for raw ``rag.*`` SQL.

matrx-rag is migrating every ``rag.*`` persistence path off hand-rolled asyncpg
SQL and onto the host-injected ORM models (``matrx_rag.get_db_model(...)`` /
``try_get_db_model(...)``). The migration finished 2026-07-11; the standing
rule is ``packages/matrx-rag/CLAUDE.md`` hard rule 5 (zero raw-SQL
exceptions). Node truth:
``/Users/armanisadeghi/code/common-docs/systems/knowledge/rag/DECISIONS.md``.

This test makes the raw-SQL class of failure EXTINCT, not merely patched:

  * Every ``rag.<table>`` reference in the package's runtime ``.py`` files is
    counted and pinned to ``raw_rag_sql_baseline.json``.
  * Adding a NEW raw ``rag.*`` query (the regression we are eradicating) raises
    the count above the baseline → this test FAILS loudly with guidance.
  * REMOVING raw SQL (migrating it to the ORM) drops the count below the
    baseline → this test also fails, demanding you lower the baseline in the
    same change. That keeps the baseline an exact, ratcheting high-water-mark
    that can only ever shrink toward zero.

Schema-owning SQL is exempt: ``migrations/*.sql`` legitimately defines the
``rag.*`` tables and is NOT a candidate for ORM migration. Doc/comment mentions
of a table name are counted too (they're cheap to keep in the baseline and
trying to distinguish "comment" from "SQL string" is brittle) — the metric we
care about is monotonic, file-scoped, and trends to zero.

To refresh the baseline after an intentional change::

    REWRITE_RAW_RAG_SQL_BASELINE=1 uv run pytest \
        packages/matrx-rag/tests/test_no_new_raw_rag_sql.py
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

# Every table that lives in the ``rag`` Postgres schema (see
# matrx_rag/migrations/0003_rag_schema.sql and friends). A reference of the
# form ``rag.<one-of-these>`` in a runtime .py file is raw-SQL surface that
# should migrate to the ORM.
_RAG_TABLES = (
    "kg_chunks",
    "kg_entities",
    "kg_edges",
    "kg_chunk_entities",
    "kg_entity_aliases",
    "kg_clusters",
    "embeddings_oai_3_small_1536",
    "embeddings_voyage_code_3_1024",
    "data_stores",
    "data_store_members",
    "library_docs",
    "retrieval_audit",
    "embedding_cache",
)

_RAG_REF_RE = re.compile(r"\brag\.(?:" + "|".join(_RAG_TABLES) + r")\b")

_PKG_ROOT = Path(__file__).resolve().parent.parent / "matrx_rag"
_BASELINE_PATH = Path(__file__).resolve().parent / "raw_rag_sql_baseline.json"


def _scan() -> dict[str, int]:
    """Return {relative_posix_path: rag.* reference count} for every runtime
    ``.py`` file in the package (migrations/*.sql are schema-owning, excluded)."""
    counts: dict[str, int] = {}
    for path in sorted(_PKG_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        n = len(_RAG_REF_RE.findall(text))
        if n:
            counts[path.relative_to(_PKG_ROOT).as_posix()] = n
    return counts


def test_no_new_raw_rag_sql() -> None:
    current = _scan()

    if os.getenv("REWRITE_RAW_RAG_SQL_BASELINE"):
        _BASELINE_PATH.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        return

    assert _BASELINE_PATH.exists(), (
        f"Missing baseline {_BASELINE_PATH}. Generate it once with REWRITE_RAW_RAG_SQL_BASELINE=1."
    )
    baseline: dict[str, int] = json.loads(_BASELINE_PATH.read_text())

    regressions: list[str] = []
    improvements: list[str] = []
    for file, count in sorted(current.items()):
        base = baseline.get(file, 0)
        if count > base:
            regressions.append(
                f"  {file}: {count} raw rag.* refs (baseline {base}) — "
                f"+{count - base} NEW. Migrate to matrx_rag.get_db_model(...) "
                f"instead of hand-rolled SQL."
            )
        elif count < base:
            improvements.append(f"  {file}: {count} (baseline {base})")
    # A file that dropped entirely out of `current` but is still in baseline.
    for file, base in sorted(baseline.items()):
        if file not in current and base > 0:
            improvements.append(f"  {file}: 0 (baseline {base})")

    msg_parts: list[str] = []
    if regressions:
        msg_parts.append(
            "New raw rag.* SQL was added — this class of failure is being "
            "eradicated (see packages/matrx-rag/CLAUDE.md hard rule 5). "
            "Use the "
            "injected ORM models via matrx_rag.get_db_model(...) / "
            "try_get_db_model(...):\n" + "\n".join(regressions)
        )
    if improvements:
        msg_parts.append(
            "Raw rag.* SQL was REMOVED (good!) but the baseline is now stale. "
            "Lower it in this change:\n  REWRITE_RAW_RAG_SQL_BASELINE=1 uv run "
            "pytest packages/matrx-rag/tests/test_no_new_raw_rag_sql.py\n" + "\n".join(improvements)
        )
    assert not msg_parts, "\n\n".join(msg_parts)
