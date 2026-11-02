"""NER engine eval — span-detection + canonicalization scoreboards (GLiNER2 vs Haiku).

Runs ONE NER engine over a gold set and scores the two jobs *separately* (they
must not be averaged — a model can be great at finding spans and poor at naming
them, and an aggregate hides that):

  1. SPAN DETECTION — entity-level precision/recall/F1 at two strictnesses:
       * strict   : (kind, start, end) exactly match a gold entity
       * type-match: same kind + span overlap (boundaries lenient)
     plus a SemEval-style breakdown (exact / partial / wrong-type / spurious / missing).
  2. CANONICALIZATION (on detected spans) — of the gold spans the engine *found*,
     the fraction whose canonical_name matches gold (case/space-normalized). This
     isolates naming quality from detection quality.

Plus latency per chunk. Run both engines and diff the JSON reports, or use --compare.

The engine is the REAL wired one: the host is booted (``--bootstrap``), then
get_ner_extractor() is pulled and, when the host installed a per-call dispatcher
(an extractor with ``engine_named(name)``), the ``--engine`` it names is run — so
this exercises the production engines end-to-end (no reimplementation of either).

Run::

    # GLiNER2
    uv run python -m matrx_rag.eval.ner_runner --engine gliner \
        --golden packages/matrx-rag/matrx_rag/eval/ner_golden_starter.json \
        --user-id <uuid> --report-out /tmp/ner_gliner.json

    # Haiku (current default)
    uv run python -m matrx_rag.eval.ner_runner --engine llm \
        --golden packages/matrx-rag/matrx_rag/eval/ner_golden_starter.json \
        --user-id <uuid> --report-out /tmp/ner_llm.json

    # Side-by-side
    uv run python -m matrx_rag.eval.ner_runner --compare /tmp/ner_llm.json /tmp/ner_gliner.json
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
from statistics import mean, median

from matrx_rag.eval._bootstrap import BOOTSTRAP_HELP, run_bootstrap
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Gold set
# ---------------------------------------------------------------------------


@dataclass
class GoldEntity:
    kind: str
    canonical_name: str
    # Author EITHER explicit offsets OR a surface ``text`` we resolve to offsets.
    text: str | None = None
    span_start: int | None = None
    span_end: int | None = None


@dataclass
class NerGoldItem:
    text: str
    entities: list[GoldEntity]
    tags: list[str] = field(default_factory=list)


def _resolve_offsets(item_text: str, entities: list[GoldEntity]) -> list[dict[str, Any]]:
    """Return gold entities as dicts with validated char offsets.

    Explicit span_start/span_end win; otherwise the surface ``text`` is located
    in document order (a left-to-right cursor handles repeated surfaces). Every
    resolved span is validated so a bad gold annotation fails loud, not silent.
    """
    resolved: list[dict[str, Any]] = []
    cursor = 0
    for e in entities:
        if e.span_start is not None and e.span_end is not None:
            s, en = e.span_start, e.span_end
        else:
            if not e.text:
                raise ValueError(f"gold entity {e!r} has neither offsets nor surface text")
            idx = item_text.find(e.text, cursor)
            if idx < 0:
                idx = item_text.find(e.text)  # fall back to first occurrence
            if idx < 0:
                raise ValueError(f"gold surface {e.text!r} not found in text")
            s, en = idx, idx + len(e.text)
            cursor = en
        surface = item_text[s:en]
        expected = e.text if e.text is not None else surface
        if surface != expected:
            raise ValueError(
                f"gold offset mismatch: text[{s}:{en}]={surface!r} != {expected!r}"
            )
        resolved.append(
            {"kind": e.kind, "canonical_name": e.canonical_name, "span_start": s, "span_end": en}
        )
    return resolved


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _norm(s: str) -> str:
    return " ".join((s or "").split()).casefold().strip()


def _overlaps(a: dict, b: dict) -> bool:
    return a["span_start"] < b["span_end"] and b["span_start"] < a["span_end"]


@dataclass
class ItemScore:
    text_len: int
    tags: list[str]
    n_gold: int
    n_pred: int
    exact: int           # COR: correct kind + exact boundary
    partial: int         # PAR: correct kind + overlap, boundary off
    wrong_type: int      # INC: overlap but wrong kind
    spurious: int        # SPU: predicted, no gold overlap
    missing: int         # MIS: gold, no predicted overlap
    canon_correct: int   # of detected (exact+partial) gold spans, canonical_name matched
    canon_total: int     # detected gold spans eligible for canonical scoring
    latency_ms: int
    error: str | None = None


def _score_item(gold: list[dict], pred: list[dict]) -> tuple[ItemScore, dict]:
    gold_used = [False] * len(gold)
    pred_used = [False] * len(pred)
    exact = partial = wrong_type = 0
    canon_correct = canon_total = 0

    # Pass 1 — exact (kind + boundary).
    for pi, p in enumerate(pred):
        for gi, g in enumerate(gold):
            if gold_used[gi]:
                continue
            if p["kind"] == g["kind"] and p["span_start"] == g["span_start"] and p["span_end"] == g["span_end"]:
                exact += 1
                pred_used[pi] = gold_used[gi] = True
                canon_total += 1
                if _norm(p.get("canonical_name", "")) == _norm(g["canonical_name"]):
                    canon_correct += 1
                break

    # Pass 2 — partial (same kind + overlap).
    for pi, p in enumerate(pred):
        if pred_used[pi]:
            continue
        for gi, g in enumerate(gold):
            if gold_used[gi] or p["kind"] != g["kind"]:
                continue
            if _overlaps(p, g):
                partial += 1
                pred_used[pi] = gold_used[gi] = True
                canon_total += 1
                if _norm(p.get("canonical_name", "")) == _norm(g["canonical_name"]):
                    canon_correct += 1
                break

    # Pass 3 — wrong type (overlap, any kind).
    for pi, p in enumerate(pred):
        if pred_used[pi]:
            continue
        for gi, g in enumerate(gold):
            if gold_used[gi]:
                continue
            if _overlaps(p, g):
                wrong_type += 1
                pred_used[pi] = gold_used[gi] = True
                break

    spurious = sum(1 for u in pred_used if not u)
    missing = sum(1 for u in gold_used if not u)
    score = ItemScore(
        text_len=0, tags=[], n_gold=len(gold), n_pred=len(pred),
        exact=exact, partial=partial, wrong_type=wrong_type,
        spurious=spurious, missing=missing,
        canon_correct=canon_correct, canon_total=canon_total, latency_ms=0,
    )
    return score, {}


def _prf(correct: float, n_pred: int, n_gold: int) -> dict[str, float]:
    p = correct / n_pred if n_pred else 0.0
    r = correct / n_gold if n_gold else 0.0
    f = (2 * p * r / (p + r)) if (p + r) else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4)}


def _summarize(engine: str, scores: list[ItemScore]) -> dict[str, Any]:
    tot_gold = sum(s.n_gold for s in scores)
    tot_pred = sum(s.n_pred for s in scores)
    exact = sum(s.exact for s in scores)
    partial = sum(s.partial for s in scores)
    wrong = sum(s.wrong_type for s in scores)
    spurious = sum(s.spurious for s in scores)
    missing = sum(s.missing for s in scores)
    canon_c = sum(s.canon_correct for s in scores)
    canon_t = sum(s.canon_total for s in scores)
    lats = [s.latency_ms for s in scores if s.error is None]
    return {
        "engine": engine,
        "n_items": len(scores),
        "n_errors": sum(1 for s in scores if s.error),
        "span_detection": {
            "strict": _prf(exact, tot_pred, tot_gold),
            "type_match": _prf(exact + partial, tot_pred, tot_gold),
            "breakdown": {
                "exact": exact, "partial": partial, "wrong_type": wrong,
                "spurious": spurious, "missing": missing,
                "gold_total": tot_gold, "pred_total": tot_pred,
            },
        },
        "canonicalization_on_detected": {
            "accuracy": round(canon_c / canon_t, 4) if canon_t else None,
            "correct": canon_c, "detected": canon_t,
        },
        "latency_ms": {
            "mean": round(mean(lats), 1) if lats else None,
            "median": round(median(lats), 1) if lats else None,
        },
    }


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


async def run_ner_eval(
    *, golden_path: str, engine: str, user_id: str, organization_id: str | None
) -> dict[str, Any]:
    raw = json.loads(Path(golden_path).read_text())
    items = [
        NerGoldItem(
            text=it["text"],
            entities=[GoldEntity(**e) for e in it["entities"]],
            tags=it.get("tags", []),
        )
        for it in raw["items"]
    ]

    # Pull the REAL wired extractor for the selected engine.
    from matrx_rag._ext import get_ner_extractor

    extractor = get_ner_extractor()
    if extractor is None:
        raise RuntimeError(
            "No NER extractor is wired. Boot the host with --bootstrap so it installs one."
        )
    # A host that chooses the engine per call exposes each engine by name; the
    # eval runs exactly the one asked for. A host with one plain extractor IS
    # that engine.
    engine_named = getattr(extractor, "engine_named", None)
    if callable(engine_named):
        extractor = engine_named(engine)

    scores: list[ItemScore] = []
    for item in items:
        gold = _resolve_offsets(item.text, item.entities)
        started = time.perf_counter()
        error: str | None = None
        pred: list[dict] = []
        try:
            pred = await extractor.extract(
                item.text,
                organization_id=organization_id,
                user_id=user_id,
                source_kind="eval",
                source_id="ner_eval",
            )
        except Exception as exc:  # noqa: BLE001 — record + continue
            error = f"{type(exc).__name__}: {exc}"
            logger.warning("extractor failed on item (%s): %s", item.tags, exc)
        latency_ms = int((time.perf_counter() - started) * 1000)

        score, _ = _score_item(gold, pred or [])
        score.text_len = len(item.text)
        score.tags = item.tags
        score.latency_ms = latency_ms
        score.error = error
        scores.append(score)

    summary = _summarize(engine, scores)
    return {
        "name": raw.get("name") or Path(golden_path).stem,
        "engine": engine,
        "ran_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "summary": summary,
        "items": [asdict(s) for s in scores],
    }


def _print_summary(report: dict[str, Any]) -> None:
    s = report["summary"]
    sd = s["span_detection"]
    print(f"\n=== NER eval: {report['name']} — engine={report['engine']} ===")
    print(f"  items={s['n_items']} errors={s['n_errors']}")
    print("  SPAN DETECTION")
    print(f"    strict     P={sd['strict']['precision']:.3f} R={sd['strict']['recall']:.3f} F1={sd['strict']['f1']:.3f}")
    print(f"    type-match P={sd['type_match']['precision']:.3f} R={sd['type_match']['recall']:.3f} F1={sd['type_match']['f1']:.3f}")
    b = sd["breakdown"]
    print(f"    breakdown  exact={b['exact']} partial={b['partial']} wrong_type={b['wrong_type']} spurious={b['spurious']} missing={b['missing']} (gold={b['gold_total']} pred={b['pred_total']})")
    c = s["canonicalization_on_detected"]
    print(f"  CANONICALIZATION (on detected spans): acc={c['accuracy']} ({c['correct']}/{c['detected']})")
    lm = s["latency_ms"]
    print(f"  LATENCY ms: mean={lm['mean']} median={lm['median']}")


def _print_compare(a: dict[str, Any], b: dict[str, Any]) -> None:
    def row(label: str, va: Any, vb: Any) -> None:
        print(f"  {label:<34} {str(va):>14}   {str(vb):>14}")

    sa, sb = a["summary"], b["summary"]
    print(f"\n=== A/B: {a['engine']} vs {b['engine']} ===")
    row("", a["engine"], b["engine"])
    row("span strict F1", sa["span_detection"]["strict"]["f1"], sb["span_detection"]["strict"]["f1"])
    row("span type-match F1", sa["span_detection"]["type_match"]["f1"], sb["span_detection"]["type_match"]["f1"])
    row("span strict recall", sa["span_detection"]["strict"]["recall"], sb["span_detection"]["strict"]["recall"])
    row("canonicalization acc", sa["canonicalization_on_detected"]["accuracy"], sb["canonicalization_on_detected"]["accuracy"])
    row("missing (gold not found)", sa["span_detection"]["breakdown"]["missing"], sb["span_detection"]["breakdown"]["missing"])
    row("spurious (false pos)", sa["span_detection"]["breakdown"]["spurious"], sb["span_detection"]["breakdown"]["spurious"])
    row("latency ms (median)", sa["latency_ms"]["median"], sb["latency_ms"]["median"])


def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="NER engine eval (span + canonicalization)")
    p.add_argument("--engine", choices=["llm", "gliner"], help="Which NER engine to run")
    p.add_argument("--golden", help="Path to NER gold JSON")
    p.add_argument("--user-id", help="A real user_id (the extractor requires one)")
    p.add_argument("--organization-id", default=None)
    p.add_argument("--span-model", default=None, help="Override RAG_NER_SPAN_MODEL (gliner engine)")
    p.add_argument("--threshold", default=None, help="Override RAG_NER_THRESHOLD (gliner engine)")
    p.add_argument("--report-out", default=None)
    p.add_argument("--bootstrap", default=None, help=BOOTSTRAP_HELP)
    p.add_argument("--compare", nargs=2, metavar=("A.json", "B.json"),
                   help="Print a side-by-side of two existing reports and exit")
    return p


async def _main_async(args: argparse.Namespace) -> int:
    if not (args.engine and args.golden and args.user_id):
        print("error: --engine, --golden and --user-id are required (unless --compare)", file=sys.stderr)
        return 2

    import os

    # GLiNER variants are chosen BEFORE the host wires the extractor; the
    # engine itself is picked from the host's dispatcher after boot.
    if args.span_model:
        os.environ["RAG_NER_SPAN_MODEL"] = args.span_model
    if args.threshold:
        os.environ["RAG_NER_THRESHOLD"] = str(args.threshold)

    # Boot the HOST (if one was named) so its DB models / seams are registered
    # before the eval runs. matrx-rag never imports a host — see _bootstrap.py.
    await run_bootstrap(args.bootstrap)

    report = await run_ner_eval(
        golden_path=args.golden,
        engine=args.engine,
        user_id=args.user_id,
        organization_id=args.organization_id,
    )
    _print_summary(report)
    if args.report_out:
        Path(args.report_out).write_text(json.dumps(report, indent=2))
        print(f"\nFull report → {args.report_out}")
    return 0


def main() -> None:
    import dotenv

    dotenv.load_dotenv()
    args = _build_argparser().parse_args()
    if args.compare:
        a = json.loads(Path(args.compare[0]).read_text())
        b = json.loads(Path(args.compare[1]).read_text())
        _print_compare(a, b)
        sys.exit(0)
    sys.exit(asyncio.run(_main_async(args)))


if __name__ == "__main__":
    main()


__all__ = ["run_ner_eval", "NerGoldItem", "GoldEntity", "ItemScore"]
