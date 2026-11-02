"""Eval runner — compute recall@k / MRR / mean faithfulness against a
golden set.

Run::

    uv run python -m aidream.services.rag.eval.runner \
        --golden aidream/services/rag/eval/golden_starter.json \
        --user-id <uuid>

Add ``--baseline`` to emit a name suitable for diffing against later
runs. Add ``--organization-id <uuid>`` to retrieve in the org scope
instead of personal scope.

Faithfulness sampling:
  - Items that have an ``"answer"`` field also get scored via
    ``aidream.services.rag.grounding.verify_grounded``. The retrieved
    chunks fed to the verifier are the same ones the search returned.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any

from matrx_rag.eval._bootstrap import BOOTSTRAP_HELP, run_bootstrap

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------


@dataclass
class GoldenItem:
    query: str
    expected_source_ids: list[str] = field(default_factory=list)
    expected_chunk_ids: list[str] = field(default_factory=list)
    source_kinds: list[str] | None = None
    answer: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class ItemResult:
    query: str
    tags: list[str]
    expected_source_ids: list[str]
    expected_chunk_ids: list[str]
    retrieved_chunk_ids: list[str]
    retrieved_source_ids: list[str]
    matched_at: int | None  # 1-based rank of the first matching hit (None = miss)
    hit_at_1: bool
    hit_at_3: bool
    hit_at_5: bool
    hit_at_10: bool
    rr: float                # reciprocal rank (0 if miss)
    latency_ms: int
    faithfulness: float | None
    error: str | None = None


@dataclass
class RunSummary:
    n_items: int
    recall_at_1: float
    recall_at_3: float
    recall_at_5: float
    recall_at_10: float
    mrr: float
    mean_faithfulness: float | None
    n_with_answer: int
    mean_latency_ms: float


# ---------------------------------------------------------------------------
# Single item evaluation
# ---------------------------------------------------------------------------


def _matches(retrieved_source_ids: list[str], retrieved_chunk_ids: list[str], item: GoldenItem) -> int | None:
    """Return the 1-based rank of the first matching retrieved item.

    Match logic:
      * If ``item.expected_chunk_ids`` is non-empty, exact match against
        ``retrieved_chunk_ids``.
      * Else if ``item.expected_source_ids`` is non-empty, source-level
        match against ``retrieved_source_ids``.
      * Else: no expectation, returns None (item ignored for hit metrics).
    """
    if item.expected_chunk_ids:
        targets = set(item.expected_chunk_ids)
        for i, cid in enumerate(retrieved_chunk_ids, start=1):
            if cid in targets:
                return i
        return None
    if item.expected_source_ids:
        targets = set(item.expected_source_ids)
        for i, sid in enumerate(retrieved_source_ids, start=1):
            if sid in targets:
                return i
        return None
    return None


async def _evaluate_item(
    item: GoldenItem,
    *,
    user_id: str,
    organization_id: str | None,
    embedding_models: list[str] | None,
    multi_query: int,
    use_hyde: bool,
    use_mmr: bool,
    rerank: bool,
    score_faithfulness: bool,
) -> ItemResult:
    from matrx_rag.search import search

    started = time.perf_counter()
    try:
        resp = await search(
            item.query,
            user_id=user_id,
            organization_id=organization_id,
            source_kinds=item.source_kinds,
            limit=10,
            embedding_models=embedding_models,
            rerank=rerank,
            use_mmr=use_mmr,
            multi_query=multi_query,
            use_hyde=use_hyde,
            only_children=True,
            record_audit=False,  # eval calls shouldn't pollute the audit table
        )
    except Exception as exc:  # noqa: BLE001
        return ItemResult(
            query=item.query,
            tags=item.tags,
            expected_source_ids=item.expected_source_ids,
            expected_chunk_ids=item.expected_chunk_ids,
            retrieved_chunk_ids=[],
            retrieved_source_ids=[],
            matched_at=None,
            hit_at_1=False,
            hit_at_3=False,
            hit_at_5=False,
            hit_at_10=False,
            rr=0.0,
            latency_ms=int((time.perf_counter() - started) * 1000),
            faithfulness=None,
            error=str(exc),
        )
    retrieved_chunks = [h.chunk_id for h in resp.hits]
    retrieved_sources = [h.source_id for h in resp.hits]
    rank = _matches(retrieved_sources, retrieved_chunks, item)
    rr = 1.0 / rank if rank else 0.0
    faithfulness: float | None = None
    if score_faithfulness and item.answer and resp.hits:
        from matrx_rag.grounding import verify_grounded

        try:
            report = await verify_grounded(
                answer=item.answer,
                retrieved=[
                    {"chunk_id": h.chunk_id, "content_text": h.content_text}
                    for h in resp.hits
                ],
            )
            faithfulness = report.overall_faithfulness
        except Exception as exc:  # noqa: BLE001
            logger.warning("faithfulness scoring failed for %r: %s", item.query, exc)

    return ItemResult(
        query=item.query,
        tags=item.tags,
        expected_source_ids=item.expected_source_ids,
        expected_chunk_ids=item.expected_chunk_ids,
        retrieved_chunk_ids=retrieved_chunks,
        retrieved_source_ids=retrieved_sources,
        matched_at=rank,
        hit_at_1=bool(rank and rank <= 1),
        hit_at_3=bool(rank and rank <= 3),
        hit_at_5=bool(rank and rank <= 5),
        hit_at_10=bool(rank and rank <= 10),
        rr=rr,
        latency_ms=int((time.perf_counter() - started) * 1000),
        faithfulness=faithfulness,
    )


# ---------------------------------------------------------------------------
# Run + summarize
# ---------------------------------------------------------------------------


async def run_eval(
    *,
    golden_path: str,
    user_id: str,
    organization_id: str | None = None,
    embedding_models: list[str] | None = None,
    multi_query: int = 1,
    use_hyde: bool = False,
    use_mmr: bool = True,
    rerank: bool = True,
    score_faithfulness: bool = True,
    concurrency: int = 4,
) -> dict[str, Any]:
    raw = json.loads(Path(golden_path).read_text())
    items = [GoldenItem(**it) for it in raw["items"]]
    name = raw.get("name") or Path(golden_path).stem

    sem = asyncio.Semaphore(concurrency)

    async def one(item: GoldenItem) -> ItemResult:
        async with sem:
            return await _evaluate_item(
                item,
                user_id=user_id,
                organization_id=organization_id,
                embedding_models=embedding_models,
                multi_query=multi_query,
                use_hyde=use_hyde,
                use_mmr=use_mmr,
                rerank=rerank,
                score_faithfulness=score_faithfulness,
            )

    results = await asyncio.gather(*(one(it) for it in items))
    n = len(results)
    n_judged = sum(1 for r in results if r.matched_at is not None or r.expected_chunk_ids or r.expected_source_ids)
    n_judged = max(1, n_judged)  # don't divide by zero
    summary = RunSummary(
        n_items=n,
        recall_at_1=sum(r.hit_at_1 for r in results) / n_judged,
        recall_at_3=sum(r.hit_at_3 for r in results) / n_judged,
        recall_at_5=sum(r.hit_at_5 for r in results) / n_judged,
        recall_at_10=sum(r.hit_at_10 for r in results) / n_judged,
        mrr=mean(r.rr for r in results) if results else 0.0,
        mean_faithfulness=(
            mean(r.faithfulness for r in results if r.faithfulness is not None)
            if any(r.faithfulness is not None for r in results)
            else None
        ),
        n_with_answer=sum(1 for r in results if r.faithfulness is not None),
        mean_latency_ms=mean(r.latency_ms for r in results) if results else 0.0,
    )

    return {
        "name": name,
        "ran_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "config": {
            "embedding_models": embedding_models,
            "multi_query": multi_query,
            "use_hyde": use_hyde,
            "use_mmr": use_mmr,
            "rerank": rerank,
            "score_faithfulness": score_faithfulness,
        },
        "summary": asdict(summary),
        "items": [asdict(r) for r in results],
    }


def _print_summary(report: dict[str, Any]) -> None:
    s = report["summary"]
    print(f"\n=== Eval: {report['name']} ===")
    cfg = report["config"]
    print(
        f"  config: rerank={cfg['rerank']} mmr={cfg['use_mmr']} "
        f"multi_query={cfg['multi_query']} hyde={cfg['use_hyde']}"
    )
    print(f"  n_items: {s['n_items']}  mean_latency={s['mean_latency_ms']:.0f}ms")
    print(f"  recall@1:  {s['recall_at_1']:.3f}")
    print(f"  recall@3:  {s['recall_at_3']:.3f}")
    print(f"  recall@5:  {s['recall_at_5']:.3f}")
    print(f"  recall@10: {s['recall_at_10']:.3f}")
    print(f"  MRR:       {s['mrr']:.3f}")
    if s["mean_faithfulness"] is not None:
        print(f"  faithfulness (n={s['n_with_answer']}): {s['mean_faithfulness']:.3f}")


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="RAG eval harness")
    p.add_argument("--golden", required=True, help="Path to golden JSON")
    p.add_argument("--user-id", required=True)
    p.add_argument("--organization-id", default=None)
    p.add_argument("--embedding-models", nargs="*", default=None,
                   help="Override embedding models, e.g. openai:text-embedding-3-small")
    p.add_argument("--multi-query", type=int, default=1)
    p.add_argument("--use-hyde", action="store_true")
    p.add_argument("--no-mmr", action="store_true")
    p.add_argument("--no-rerank", action="store_true")
    p.add_argument("--no-faithfulness", action="store_true")
    p.add_argument("--report-out", default=None,
                   help="Path to write the full JSON report; if omitted, just prints summary.")
    p.add_argument("--bootstrap", default=None, help=BOOTSTRAP_HELP)
    return p


async def _main_async() -> int:
    args = _build_argparser().parse_args()

    # Boot the HOST (if one was named) so its DB models / seams are registered
    # before the eval runs. matrx-rag never imports a host — see _bootstrap.py.
    await run_bootstrap(args.bootstrap)

    report = await run_eval(
        golden_path=args.golden,
        user_id=args.user_id,
        organization_id=args.organization_id,
        embedding_models=args.embedding_models,
        multi_query=args.multi_query,
        use_hyde=args.use_hyde,
        use_mmr=not args.no_mmr,
        rerank=not args.no_rerank,
        score_faithfulness=not args.no_faithfulness,
    )
    _print_summary(report)
    if args.report_out:
        Path(args.report_out).write_text(json.dumps(report, indent=2))
        print(f"\nFull report → {args.report_out}")
    return 0


def main() -> None:
    import dotenv
    dotenv.load_dotenv()
    sys.exit(asyncio.run(_main_async()))


if __name__ == "__main__":
    main()


__all__ = ["GoldenItem", "ItemResult", "RunSummary", "run_eval"]
