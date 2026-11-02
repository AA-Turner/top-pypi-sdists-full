"""Detector registry — declarative dispatch keyed by mime type.

Two registries:

1. ``ANALYZER_REGISTRY`` — mime → list[DetectorSpec]. Built-in defaults.
   Adding a new file type is an entry here + a detector module.

2. ``DETECTOR_FACTORIES`` — kind → factory. Each detector module registers
   itself at import time. The dispatcher resolves kind → factory → run.

PDF detectors are imported and registered by
``matrx_files.specific_handlers.pdf.analyze``.
"""

from __future__ import annotations

from typing import Any

from .protocol import Detector, DetectorFactory, DetectorSpec


# ── kind → factory registry ───────────────────────────────────────────────────

DETECTOR_FACTORIES: dict[str, DetectorFactory] = {}


def register_detector(kind: str, factory: DetectorFactory) -> None:
    """Register a detector factory. Called at module import time."""
    DETECTOR_FACTORIES[kind] = factory


def get_factory(kind: str) -> DetectorFactory | None:
    return DETECTOR_FACTORIES.get(kind)


def instantiate(spec: DetectorSpec) -> Detector | None:
    factory = DETECTOR_FACTORIES.get(spec.kind)
    if factory is None:
        return None
    return factory(spec)


# ── mime → list[DetectorSpec] registry ────────────────────────────────────────

ANALYZER_REGISTRY: dict[str, list[DetectorSpec]] = {
    "application/pdf": [
        # Tier 1 — instant
        DetectorSpec(kind="metadata", cost_class="fast"),
        DetectorSpec(kind="page_classification", cost_class="fast"),
        DetectorSpec(kind="page_outline", cost_class="fast"),
        DetectorSpec(kind="text_extraction_native", cost_class="fast"),
        # Tier 2 — fast
        DetectorSpec(
            kind="redaction_candidates",
            cost_class="fast",
            tiers=("low", "medium", "high"),
            depends_on=("text_extraction_native",),
            requires_text=True,
        ),
        DetectorSpec(
            kind="repeated_regions",
            cost_class="fast",
            tiers=("low", "medium", "high"),
        ),
        DetectorSpec(kind="tables", cost_class="fast"),
        DetectorSpec(
            kind="duplicate_pages_exact",
            cost_class="fast",
            depends_on=("text_extraction_native",),
            requires_text=True,
        ),
        DetectorSpec(
            kind="duplicate_pages_normalized",
            cost_class="fast",
            depends_on=("text_extraction_native",),
            requires_text=True,
        ),
        DetectorSpec(kind="duplicate_pages_structural", cost_class="fast"),
        # Tier 3 — medium
        DetectorSpec(
            kind="duplicate_pages_shingle",
            cost_class="medium",
            tiers=("low", "medium", "high"),
            depends_on=("text_extraction_native",),
            requires_text=True,
        ),
        DetectorSpec(kind="embedded_images", cost_class="medium"),
        # Tier 4 — slow
        DetectorSpec(
            kind="text_extraction_ocr",
            cost_class="slow",
            depends_on=("text_extraction_native",),
        ),
        DetectorSpec(
            kind="duplicate_pages_visual",
            cost_class="slow",
            tiers=("low", "medium", "high"),
        ),
    ],
}


def get_specs_for_mime(mime_type: str) -> list[DetectorSpec]:
    """Resolve registered specs for a mime type. Wildcards supported (image/*)."""
    if mime_type in ANALYZER_REGISTRY:
        return list(ANALYZER_REGISTRY[mime_type])
    prefix = mime_type.split("/", 1)[0] + "/*"
    return list(ANALYZER_REGISTRY.get(prefix, []))


def text_dependent_kinds() -> set[str]:
    """The detector kinds that need to be re-emitted when OCR adds new text."""
    out: set[str] = set()
    for specs in ANALYZER_REGISTRY.values():
        for spec in specs:
            if spec.requires_text:
                out.add(spec.kind)
    return out


__all__ = [
    "ANALYZER_REGISTRY",
    "DETECTOR_FACTORIES",
    "register_detector",
    "get_factory",
    "instantiate",
    "get_specs_for_mime",
    "text_dependent_kinds",
]
