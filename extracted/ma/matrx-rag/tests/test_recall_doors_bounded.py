"""The recall doors stay bounded for a heavy owner (kg_046, 2026-11-14).

Every "search my knowledge" for owners of ~120k passages timed out (57014). The live bodies of
``rag.recall_vector`` / ``rag.recall_lexical`` are recorded in this package's migrations; the
NEWEST file defining each is what a standalone install runs, so these checks read that file.

* vector: the exact-scan candidate count must stream and stop at the cap (``UNION ALL`` under the
  LIMIT - a ``UNION`` hashes every arm first: 119k own passages read to learn "over 20,000"), and
  the HNSW fallback walk must carry an explicit ``hnsw.max_scan_tuples`` bound;
* lexical: words capped (rarest first by the column's statistics), every-word pass first, then the
  selective-word pass, with kg_041's any-word match kept as the last pass (the recall floor); since
  wf_292 / kg_047 each pass ranks a bounded candidate set and the floor matches the rarest words
  that fit a budget;
* neither door may lose the read-access predicate.
"""

from __future__ import annotations

import re
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parents[1] / "matrx_rag" / "migrations"


def _latest_body(function: str) -> tuple[str, str]:
    pattern = re.compile(
        rf"create or replace function rag\.{function}\(.*?\n\$function\$;", re.IGNORECASE | re.DOTALL
    )
    found: list[tuple[str, str]] = []
    for path in sorted(MIGRATIONS.glob("kg_*.sql")):
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            found.append((path.name, match.group(0)))
    assert found, f"no migration defines rag.{function}"
    return found[-1]


def _code(body: str) -> str:
    """The body without SQL comments, so a comment cannot satisfy a check."""
    return "\n".join(line.split("--", 1)[0] for line in body.splitlines())


def test_vector_candidate_count_streams_and_stops_at_the_cap() -> None:
    name, body = _latest_body("recall_vector")
    code = _code(body).lower()
    head, sep, _ = code.partition("limit v_exact_max + 1")
    assert sep, f"{name}: the candidate count lost its cap"
    arms = head[head.index("into v_raw from ("):]
    assert re.search(r"\bunion\s+all\b", arms), f"{name}: candidate arms must be UNION ALL"
    assert not re.search(r"\bunion\b(?!\s+all)", arms), f"{name}: a bare UNION hashes every arm before the LIMIT"
    assert "select distinct u from unnest(v_raw)" in code, f"{name}: the exact path must de-duplicate candidates"


def test_vector_hnsw_walk_is_bounded() -> None:
    name, body = _latest_body("recall_vector")
    code = _code(body)
    assert "set_config('hnsw.max_scan_tuples'" in code, f"{name}: the HNSW walk needs an explicit max_scan_tuples"
    assert "'max_scan_tuples'" in code and "10000" in code, f"{name}: max_scan_tuples is a caller knob, default 10000"
    assert "set_config('hnsw.ef_search'" in code and "set_config('hnsw.iterative_scan'" in code


def test_lexical_matches_narrowest_first_with_the_any_word_floor() -> None:
    name, body = _latest_body("recall_lexical")
    code = _code(body)
    assert "lexical_max_terms" in code and "v_term_text[1:v_max_terms]" in code, f"{name}: words must be capped"
    assert "most_common_elems" in code and "pg_stats" in code, f"{name}: rarity comes from the column statistics"
    assert "') & ('" in code, f"{name}: the every-word pass is missing"
    assert "lexical_common_term_freq" in code, f"{name}: the selective-word pass is missing"
    assert "array_remove(array[v_and, v_rare, coalesce(v_match, v_any)], null)" in code, (
        f"{name}: passes must run every-word, selective-word, then any-word (the floor) last"
    )
    # Matching and ranking are separate parameters: a narrow pass still ranks by every kept word.
    assert "ts_rank_cd(cand.tsv, $20, 32)" in code and "c.content_tsv @@ $16" in code


def test_lexical_passes_rank_a_bounded_candidate_set() -> None:
    """wf_292 / kg_047 (2026-11-18): a broad question of common words ranked 46k-121k passages and
    timed out cold. Each pass ranks at most ``lexical_candidate_cap`` readable passages (the LIMIT sits
    AFTER the read predicate, so a sparse reader still gets every match), and the floor matches on the
    rarest words that fit ``lexical_any_match_budget``."""
    name, body = _latest_body("recall_lexical")
    code = _code(body)
    assert "'lexical_candidate_cap'" in code and "3000" in code, f"{name}: the candidate cap is a caller knob"
    assert "'lexical_any_match_budget'" in code and "20000" in code, f"{name}: the floor budget is a caller knob"
    assert re.search(r"where c\.content_tsv @@ \$16 and %s limit %s\) cand", code), (
        f"{name}: the cap must bound the matched, read-checked rows before ts_rank_cd"
    )
    assert "rag._recall_predicate_sql(f), v_cap)" in code
    assert "exit when v_est > 0 and v_est + v_term_fr[j] * v_rows > v_budget;" in code, (
        f"{name}: the floor must take the rarest words that fit the budget, at least one"
    )


def test_lexical_drops_stop_words() -> None:
    name, body = _latest_body("recall_lexical")
    assert "to_tsvector('english', w) <> ''::tsvector" in _code(body), f"{name}: stop words must be dropped"


def test_both_doors_keep_the_read_predicate() -> None:
    for function in ("recall_vector", "recall_lexical"):
        name, body = _latest_body(function)
        code = _code(body)
        assert "rag._recall_predicate_sql(f)" in code, f"{name}: rag.{function} lost its read-access predicate"
        assert "if p_user is null and not v_bypass then return; end if;" in code
