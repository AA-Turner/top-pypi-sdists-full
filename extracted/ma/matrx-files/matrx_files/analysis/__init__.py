"""File-analysis platform — file-type-agnostic dispatcher + detector registry.

Public surface:
- ``analyze_file(...)`` — top-level entry point.
- ``register_detector(kind, factory)`` — detector module registration.
- ``DetectorSpec`` / ``DetectorResult`` / ``Detector`` / ``PipelineContext`` —
  the building blocks.

PDF detectors are registered when ``matrx_files.specific_handlers.pdf.analyze``
is imported.
"""

from __future__ import annotations

from .context import PipelineContext, ResolvedSettings
from .dispatcher import (
    ANALYZER_VERSION,
    AnalysisOutcome,
    AnalysisProgressCallback,
    AnalysisProgressEvent,
    analyze_file,
)
from .label_catalog import (
    LABEL_CATALOG,
    get_categories,
    get_label,
    get_label_catalog,
    normalize_value,
)
from .ocr_router import (
    DEFAULT_OCR_PROVIDER,
    OcrProviderProtocol,
    needs_ocr,
    select_pages_for_ocr,
)
from .persistence import PersistenceProtocol, persist_one_result
from .preferences import PrefsStoreProtocol, resolve_settings
from .protocol import (
    ConfidenceTier,
    CostClass,
    Detector,
    DetectorFactory,
    DetectorResult,
    DetectorSpec,
    DetectorStatus,
    PageInfo,
    TextSource,
)
from .registry import (
    ANALYZER_REGISTRY,
    DETECTOR_FACTORIES,
    get_factory,
    get_specs_for_mime,
    instantiate,
    register_detector,
    text_dependent_kinds,
)

__all__ = [
    # entry points
    "analyze_file",
    "AnalysisOutcome",
    "AnalysisProgressCallback",
    "AnalysisProgressEvent",
    "ANALYZER_VERSION",
    # registry
    "register_detector",
    "get_factory",
    "instantiate",
    "get_specs_for_mime",
    "text_dependent_kinds",
    "ANALYZER_REGISTRY",
    "DETECTOR_FACTORIES",
    # protocol
    "Detector",
    "DetectorSpec",
    "DetectorResult",
    "DetectorFactory",
    "DetectorStatus",
    "ConfidenceTier",
    "CostClass",
    "TextSource",
    "PageInfo",
    # context
    "PipelineContext",
    "ResolvedSettings",
    # persistence
    "PersistenceProtocol",
    "persist_one_result",
    # preferences
    "PrefsStoreProtocol",
    "resolve_settings",
    # ocr
    "OcrProviderProtocol",
    "DEFAULT_OCR_PROVIDER",
    "needs_ocr",
    "select_pages_for_ocr",
    # label catalog
    "LABEL_CATALOG",
    "get_label_catalog",
    "get_categories",
    "get_label",
    "normalize_value",
]
