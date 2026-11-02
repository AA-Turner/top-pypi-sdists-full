"""Pattern-candidate detector — find PII/regex spans WITHOUT modifying the file.

Returns spans with page + bbox + masked preview + full salted hash, organized
by tier. Each tier is a separate detector run so consumers can choose strictness.

This is the "discover-only" counterpart to ``redact_pattern`` — it never
emits the original matched text, only:
  - The pattern_id that matched.
  - The page number and bbox.
  - A masked preview ("S******** (9)") for FE display.
  - A salted SHA-256 of the actual match so a future "show all files that
    mention THIS exact SSN" query is possible without storing the PII.
"""

from __future__ import annotations

import hashlib
import os
import re
import time
from collections.abc import Callable
from typing import Any

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ..internal import load_pymupdf
from ..redact.patterns import BUILTIN_PATTERNS

DETECTOR_KIND = "redaction_candidates"
DETECTOR_VERSION = "v1"


def _resolve_catalog(ctx: PipelineContext) -> list[dict[str, Any]]:
    """Use ctx.settings.pattern_catalog if populated; else fall back to BUILTIN_PATTERNS."""
    cat = getattr(ctx.settings, "pattern_catalog", None) or []
    if cat:
        return cat
    out: list[dict[str, Any]] = []
    for pid, value in BUILTIN_PATTERNS.items():
        if isinstance(value, tuple):
            regex, desc = value
            out.append(
                {
                    "id": pid,
                    "label": desc,
                    "category": "pii",
                    "regex": regex,
                    "tiers": ("n/a", "low", "medium", "high"),
                }
            )
        elif isinstance(value, dict):
            out.append({"id": pid, **value})
    return out


def _validator_callable(spec: Any) -> Callable[[str], bool] | None:
    """Look up a validator function on the catalog entry.

    Catalog entries may pass either a callable (in-process patterns) or a
    string identifier (DB-loaded patterns). String form is matched against
    a small known-validators table.
    """
    if spec is None:
        return None
    if callable(spec):
        return spec
    from ..redact.validators import VALIDATORS  # local to avoid circular import

    if isinstance(spec, str):
        return VALIDATORS.get(spec)
    return None


def _mask_preview(text: str) -> str:
    if not text:
        return ""
    head = text[0]
    return f"{head}{'*' * max(0, len(text) - 1)} ({len(text)})"


def _hash_match(text: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}|{text}".encode()).hexdigest()


def _get_page_spans(doc) -> list[tuple[int, list, str]]:
    """For each page, return (page_index, words_list, joined_text)."""
    out: list[tuple[int, list, str]] = []
    for i in range(doc.page_count):
        page = doc[i]
        words = page.get_text("words", sort=True) or []
        spans: list[tuple[int, int, tuple[float, float, float, float]]] = []
        parts: list[str] = []
        cursor = 0
        for w in words:
            x0, y0, x1, y1, word, *_rest = w
            if not word:
                continue
            parts.append(word)
            parts.append(" ")
            spans.append((cursor, cursor + len(word), (float(x0), float(y0), float(x1), float(y1))))
            cursor += len(word) + 1
        out.append((i, spans, "".join(parts)))
    return out


class PatternCandidatesDetector(Detector):
    kind = DETECTOR_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF text extraction + regex sweep — runs off-loop.
        started = time.monotonic()
        catalog = _resolve_catalog(ctx)
        if not catalog:
            return DetectorResult(
                kind=DETECTOR_KIND,
                confidence_tier=tier,
                detector_version=DETECTOR_VERSION,
                elapsed_ms=int((time.monotonic() - started) * 1000),
                status="skipped",
                summary={"reason": "empty pattern catalog"},
                payload={"spans": []},
                text_sources=["native", "ocr"],
            )

        pymupdf = load_pymupdf()
        doc = ctx.cache.get("pymupdf_doc")
        if doc is None:
            doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
            ctx.cache["pymupdf_doc"] = doc

        restrict_pages = ctx.cache.get("restrict_pages")
        salt = os.environ.get("MATRX_REDACTION_HASH_SALT", "matrx-utils-default-salt")
        spans_data = _get_page_spans(doc)
        all_spans: list[dict[str, Any]] = []
        per_pattern_counts: dict[str, int] = {}

        # Compile patterns for the requested tier.
        compiled: list[tuple[dict[str, Any], re.Pattern, str | None]] = []
        for entry in catalog:
            pid = entry.get("id") or ""
            tiers_supported = tuple(entry.get("tiers") or ("n/a",))
            # If the entry supports tier "n/a", it runs at every tier.
            if tier not in tiers_supported and "n/a" not in tiers_supported:
                continue
            regex_str = entry.get("regex")
            # Newer entries may carry a dict {low,medium,high} for per-tier regex
            tier_regex = entry.get("tier_regex") or {}
            picked = tier_regex.get(tier) if isinstance(tier_regex, dict) else None
            if picked:
                regex_str = picked
            if not regex_str:
                continue
            flags = int(entry.get("flags") or 0)
            try:
                pat = re.compile(regex_str, flags=flags)
            except re.error:
                continue
            validator_id = entry.get("validator")
            compiled.append((entry, pat, validator_id))

        for page_index, page_spans, page_text in spans_data:
            page_no = page_index + 1
            if restrict_pages is not None and page_no not in restrict_pages:
                continue
            if not page_text:
                continue
            for entry, pattern, validator_id in compiled:
                pid = entry.get("id") or ""
                category = entry.get("category", "pii")
                for match in pattern.finditer(page_text):
                    matched_text = match.group(0)
                    mstart, mend = match.start(), match.end()
                    hit_bboxes = [
                        bbox
                        for (sstart, send, bbox) in page_spans
                        if not (send <= mstart or sstart >= mend)
                    ]
                    if not hit_bboxes:
                        continue
                    validator = _validator_callable(validator_id)
                    valid = True
                    if validator is not None:
                        try:
                            valid = bool(validator(matched_text))
                        except Exception:
                            valid = False
                    # High-tier hits that fail validator are demoted, not dropped.
                    effective_tier = tier
                    if not valid and tier == "high":
                        effective_tier = "medium"
                    if not valid and tier == "medium":
                        effective_tier = "low"
                    if not valid and tier == "low":
                        # Drop only if low-tier still fails — i.e. cannot meet any bar.
                        continue
                    x0 = min(b[0] for b in hit_bboxes)
                    y0 = min(b[1] for b in hit_bboxes)
                    x1 = max(b[2] for b in hit_bboxes)
                    y1 = max(b[3] for b in hit_bboxes)
                    all_spans.append(
                        {
                            "pattern_id": pid,
                            "category": category,
                            "page_number": page_no,
                            "bbox": {"x0": x0, "y0": y0, "x1": x1, "y1": y1},
                            "char_start": mstart,
                            "char_end": mend,
                            "masked_preview": _mask_preview(matched_text),
                            "match_hash": _hash_match(matched_text, salt),
                            "validator_passed": valid,
                            "confidence_tier": effective_tier,
                        }
                    )
                    per_pattern_counts[pid] = per_pattern_counts.get(pid, 0) + 1

        # Roll up summary counts for the dispatcher to merge into file_analysis.summary_counts.
        counts = ctx.cache.setdefault("summary_counts", {})
        pii_bucket = counts.setdefault("pii", {})
        for pid, c in per_pattern_counts.items():
            pii_bucket[pid] = pii_bucket.get(pid, 0) + c

        return DetectorResult(
            kind=DETECTOR_KIND,
            confidence_tier=tier,
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={
                "spans_count": len(all_spans),
                "per_pattern_counts": per_pattern_counts,
                "tier": tier,
            },
            payload={"spans": all_spans},
            text_sources=["native", "ocr"],
        )


def _factory(spec: DetectorSpec) -> Detector:
    return PatternCandidatesDetector()


register_detector(DETECTOR_KIND, _factory)


__all__ = [
    "DETECTOR_KIND",
    "DETECTOR_VERSION",
    "PatternCandidatesDetector",
]
