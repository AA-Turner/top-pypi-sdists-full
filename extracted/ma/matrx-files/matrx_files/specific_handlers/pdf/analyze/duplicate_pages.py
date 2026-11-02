"""Five-way duplicate-page detection.

Every method runs independently and emits its own DetectorResult. Consumers
pick whichever signal fits their use case:

- exact:        SHA-256 of the raw extracted text (rejects identical pages).
- normalized:   Whitespace + case + punctuation normalized, then hashed.
- shingle:      5-gram MinHash (Jaccard estimate). Tier-gated by similarity cutoff.
- structural:   Per-page block-layout fingerprint (geometry + block-count signature).
- visual:       64-bit pHash on rendered pages. Tier-gated by Hamming distance.
"""

from __future__ import annotations

import hashlib
import re
import time
from collections import defaultdict
from typing import Any

from ....analysis import (
    Detector,
    DetectorResult,
    DetectorSpec,
    PipelineContext,
    register_detector,
)
from ..internal import load_pymupdf

DETECTOR_VERSION = "v1"

EXACT_KIND = "duplicate_pages_exact"
NORM_KIND = "duplicate_pages_normalized"
SHINGLE_KIND = "duplicate_pages_shingle"
STRUCT_KIND = "duplicate_pages_structural"
VISUAL_KIND = "duplicate_pages_visual"


# ── helpers ──────────────────────────────────────────────────────────────────

_WHITESPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]")


def _open_doc(ctx: PipelineContext):
    doc = ctx.cache.get("pymupdf_doc")
    if doc is not None:
        return doc
    pymupdf = load_pymupdf()
    doc = pymupdf.open(stream=ctx.bytes_in_memory, filetype="pdf")
    ctx.cache["pymupdf_doc"] = doc
    return doc


def _get_page_text_map(ctx: PipelineContext) -> dict[int, str]:
    cached = ctx.cache.get("page_text_combined") or ctx.cache.get("page_text_native") or {}
    return {
        int(p): entry.get("text", "") or entry.get("text_ocr", "") for p, entry in cached.items()
    }


def _normalise(text: str) -> str:
    t = text.lower()
    t = _PUNCT_RE.sub(" ", t)
    t = _WHITESPACE_RE.sub(" ", t).strip()
    return t


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _group_by_hash(per_page: dict[int, str]) -> list[dict[str, Any]]:
    by_hash: dict[str, list[int]] = defaultdict(list)
    for page_no, h in per_page.items():
        by_hash[h].append(page_no)
    groups: list[dict[str, Any]] = []
    for h, pages in by_hash.items():
        if len(pages) > 1:
            groups.append({"hash": h, "pages": sorted(pages), "count": len(pages)})
    groups.sort(key=lambda g: (-g["count"], g["pages"][0]))
    return groups


# ── EXACT ────────────────────────────────────────────────────────────────────


class DuplicatePagesExactDetector(Detector):
    kind = EXACT_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound text hashing — runs off-loop via base Detector.run.
        started = time.monotonic()
        page_text = _get_page_text_map(ctx)
        hashes = {p: _hash_text(t) for p, t in page_text.items() if t.strip()}
        groups = _group_by_hash(hashes)
        ctx.cache.setdefault("duplicate_signals", {})[EXACT_KIND] = groups
        return DetectorResult(
            kind=EXACT_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={
                "groups_count": len(groups),
                "duplicate_pages": sum(g["count"] for g in groups),
            },
            payload={"groups": groups, "page_hashes": hashes},
            text_sources=["native", "ocr"],
        )


# ── NORMALIZED ───────────────────────────────────────────────────────────────


class DuplicatePagesNormalizedDetector(Detector):
    kind = NORM_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound normalize + hash — runs off-loop via base Detector.run.
        started = time.monotonic()
        page_text = _get_page_text_map(ctx)
        hashes = {p: _hash_text(_normalise(t)) for p, t in page_text.items() if t.strip()}
        groups = _group_by_hash(hashes)
        ctx.cache.setdefault("duplicate_signals", {})[NORM_KIND] = groups
        return DetectorResult(
            kind=NORM_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={
                "groups_count": len(groups),
                "duplicate_pages": sum(g["count"] for g in groups),
            },
            payload={"groups": groups, "page_hashes": hashes},
            text_sources=["native", "ocr"],
        )


# ── SHINGLE (k-shingle Jaccard via hash signature) ───────────────────────────

_SHINGLE_K = 5
_SHINGLE_NUM_HASHES = 64


def _shingles(text: str, k: int = _SHINGLE_K) -> set[str]:
    norm = _normalise(text)
    tokens = norm.split()
    if len(tokens) < k:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}


def _minhash_signature(shingles: set[str], num_hashes: int = _SHINGLE_NUM_HASHES) -> list[int]:
    if not shingles:
        return [0] * num_hashes
    sig: list[int] = []
    for seed in range(num_hashes):
        best = None
        for s in shingles:
            h = int.from_bytes(
                hashlib.blake2b(f"{seed}:{s}".encode(), digest_size=8).digest(),
                "big",
                signed=False,
            )
            if best is None or h < best:
                best = h
        sig.append(best or 0)
    return sig


def _signature_jaccard(a: list[int], b: list[int]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    matches = sum(1 for x, y in zip(a, b) if x == y)
    return matches / len(a)


_SHINGLE_TIER_THRESHOLD = {"high": 0.92, "medium": 0.80, "low": 0.65}


class DuplicatePagesShingleDetector(Detector):
    kind = SHINGLE_KIND
    version = DETECTOR_VERSION
    cost_class = "medium"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound MinHash + O(n²) pairwise — runs off-loop via base run().
        started = time.monotonic()
        page_text = _get_page_text_map(ctx)
        threshold = _SHINGLE_TIER_THRESHOLD.get(tier, _SHINGLE_TIER_THRESHOLD["medium"])

        sigs = ctx.cache.get("shingle_signatures")
        if sigs is None:
            sigs = {}
            for p, t in page_text.items():
                sigs[p] = _minhash_signature(_shingles(t))
            ctx.cache["shingle_signatures"] = sigs

        # Pairwise — small page counts only; for huge docs we'd LSH. v1 is O(n²).
        groups: list[dict[str, Any]] = []
        seen: set[int] = set()
        for p1 in sorted(sigs.keys()):
            if p1 in seen:
                continue
            cluster = [p1]
            for p2 in sorted(sigs.keys()):
                if p2 <= p1 or p2 in seen:
                    continue
                sim = _signature_jaccard(sigs[p1], sigs[p2])
                if sim >= threshold:
                    cluster.append(p2)
            if len(cluster) > 1:
                for p in cluster:
                    seen.add(p)
                groups.append(
                    {"pages": sorted(cluster), "count": len(cluster), "threshold": threshold}
                )

        ctx.cache.setdefault("duplicate_signals", {})[f"{SHINGLE_KIND}:{tier}"] = groups

        return DetectorResult(
            kind=SHINGLE_KIND,
            confidence_tier=tier,
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={"groups_count": len(groups), "threshold": threshold},
            payload={"groups": groups},
            text_sources=["native", "ocr"],
        )


# ── STRUCTURAL (block-layout fingerprint) ────────────────────────────────────


class DuplicatePagesStructuralDetector(Detector):
    kind = STRUCT_KIND
    version = DETECTOR_VERSION
    cost_class = "fast"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound PyMuPDF block layout fingerprint — runs off-loop.
        started = time.monotonic()
        doc = _open_doc(ctx)
        fingerprints: dict[int, str] = {}
        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            try:
                blocks = page.get_text("blocks", sort=False) or []
            except Exception:
                blocks = []
            sig_parts: list[str] = [f"w={int(rect.width)}", f"h={int(rect.height)}"]
            for blk in blocks:
                x0, y0, x1, y1, _text, _bnum, btype = blk[:7]
                # Quantize bboxes to 16-pt grid so minor jitter doesn't break the hash.
                sig_parts.append(
                    f"b{int(btype)}:{int(x0) // 16}:{int(y0) // 16}:{int(x1) // 16}:{int(y1) // 16}"
                )
            fp = _hash_text("|".join(sig_parts))
            fingerprints[i + 1] = fp
        groups = _group_by_hash(fingerprints)
        ctx.cache.setdefault("duplicate_signals", {})[STRUCT_KIND] = groups
        return DetectorResult(
            kind=STRUCT_KIND,
            confidence_tier="n/a",
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={
                "groups_count": len(groups),
                "duplicate_pages": sum(g["count"] for g in groups),
            },
            payload={"groups": groups, "fingerprints": fingerprints},
        )


# ── VISUAL (perceptual hash) ─────────────────────────────────────────────────


def _phash_64(page) -> int:
    """64-bit dHash of a low-res render — simple and deterministic."""
    pix = page.get_pixmap(dpi=36, alpha=False, colorspace="GRAY")
    # Resize-equivalent — use 9x8 grayscale samples for dHash.
    target_w, target_h = 9, 8
    if pix.width <= 0 or pix.height <= 0:
        return 0
    samples = bytearray(target_w * target_h)
    samples_raw = pix.samples  # row-major grayscale
    stride = pix.stride
    for ty in range(target_h):
        src_y = int(ty * pix.height / target_h)
        for tx in range(target_w):
            src_x = int(tx * pix.width / target_w)
            samples[ty * target_w + tx] = samples_raw[src_y * stride + src_x]
    bits = 0
    for ty in range(target_h):
        for tx in range(target_w - 1):
            left = samples[ty * target_w + tx]
            right = samples[ty * target_w + tx + 1]
            if right > left:
                bits = (bits << 1) | 1
            else:
                bits = bits << 1
    return bits & ((1 << 64) - 1)


def _hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


_VISUAL_TIER_MAX_DIST = {"high": 2, "medium": 6, "low": 10}


class DuplicatePagesVisualDetector(Detector):
    kind = VISUAL_KIND
    version = DETECTOR_VERSION
    cost_class = "slow"

    def analyze(self, ctx: PipelineContext, tier: str) -> DetectorResult:
        # CPU-bound pixmap render + pHash (the 'duplicate_pages_visual' from the
        # 2026-06-04 incident) — runs off-loop via base Detector.run.
        started = time.monotonic()
        doc = _open_doc(ctx)
        max_dist = _VISUAL_TIER_MAX_DIST.get(tier, _VISUAL_TIER_MAX_DIST["medium"])

        phashes = ctx.cache.get("phashes")
        if phashes is None:
            phashes = {}
            for i in range(doc.page_count):
                phashes[i + 1] = _phash_64(doc[i])
            ctx.cache["phashes"] = phashes

        groups: list[dict[str, Any]] = []
        seen: set[int] = set()
        sorted_pages = sorted(phashes.keys())
        for p1 in sorted_pages:
            if p1 in seen:
                continue
            cluster = [p1]
            for p2 in sorted_pages:
                if p2 <= p1 or p2 in seen:
                    continue
                if _hamming(phashes[p1], phashes[p2]) <= max_dist:
                    cluster.append(p2)
            if len(cluster) > 1:
                for p in cluster:
                    seen.add(p)
                groups.append(
                    {"pages": sorted(cluster), "count": len(cluster), "max_hamming": max_dist}
                )

        ctx.cache.setdefault("duplicate_signals", {})[f"{VISUAL_KIND}:{tier}"] = groups
        # store readable hex hashes for the FE
        phash_hex = {p: f"{h:016x}" for p, h in phashes.items()}
        return DetectorResult(
            kind=VISUAL_KIND,
            confidence_tier=tier,
            detector_version=DETECTOR_VERSION,
            elapsed_ms=int((time.monotonic() - started) * 1000),
            summary={"groups_count": len(groups), "max_hamming": max_dist},
            payload={"groups": groups, "page_phash": phash_hex},
        )


def _f_exact(spec: DetectorSpec) -> Detector:
    return DuplicatePagesExactDetector()


def _f_norm(spec: DetectorSpec) -> Detector:
    return DuplicatePagesNormalizedDetector()


def _f_shingle(spec: DetectorSpec) -> Detector:
    return DuplicatePagesShingleDetector()


def _f_struct(spec: DetectorSpec) -> Detector:
    return DuplicatePagesStructuralDetector()


def _f_visual(spec: DetectorSpec) -> Detector:
    return DuplicatePagesVisualDetector()


register_detector(EXACT_KIND, _f_exact)
register_detector(NORM_KIND, _f_norm)
register_detector(SHINGLE_KIND, _f_shingle)
register_detector(STRUCT_KIND, _f_struct)
register_detector(VISUAL_KIND, _f_visual)


__all__ = [
    "EXACT_KIND",
    "NORM_KIND",
    "SHINGLE_KIND",
    "STRUCT_KIND",
    "VISUAL_KIND",
    "DETECTOR_VERSION",
    "DuplicatePagesExactDetector",
    "DuplicatePagesNormalizedDetector",
    "DuplicatePagesShingleDetector",
    "DuplicatePagesStructuralDetector",
    "DuplicatePagesVisualDetector",
]
