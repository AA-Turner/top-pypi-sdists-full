"""flowtask.interfaces.scoring — SweetSpot spatial scoring interface (FEAT-190).

Framework-agnostic contract for site-selection / spatial suitability scoring.
No dependency on agents, LLM clients, dataset managers, or the flowtask DAG
runtime (spec G2, AC9).

Contract types (``models.py``) are re-exported eagerly here since they only
depend on ``pydantic``, ``numpy`` and ``pandas``. Heavier symbols
(``SweetSpotScorer``, ``ScoringEngine``, extractor ABC/registry) are
lazy-loaded via ``__getattr__`` so that ``import flowtask.interfaces.scoring``
never pulls in ``scipy`` or ``h3`` at import time (spec AC11). This mirrors
the parent ``flowtask/interfaces/__init__.py`` lazy-loading pattern.
"""
from .models import (
    CandidateGrid,
    Criterion,
    Direction,
    ExtractorParams,
    HardFilter,
    POILayer,
    ScoreResult,
    ScoringPolicy,
    ValueFunction,
)

# Lazy-loaded modules and their import paths.
_LAZY_IMPORTS = {
    "ScoringEngine": (".engine", "ScoringEngine"),
    "SweetSpotScorer": (".service", "SweetSpotScorer"),
    "AbstractFeatureExtractor": (".abstract", "AbstractFeatureExtractor"),
    "ExtractorRegistry": (".abstract", "ExtractorRegistry"),
    "extractor_registry": (".abstract", "extractor_registry"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        import importlib
        module_path, attr_name = _LAZY_IMPORTS[name]
        module = importlib.import_module(module_path, package=__name__)
        value = getattr(module, attr_name)
        # Cache in module namespace so __getattr__ is not called again.
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    # Eager (contract types — pydantic/numpy/pandas only):
    "Direction",
    "ValueFunction",
    "ExtractorParams",
    "Criterion",
    "HardFilter",
    "ScoringPolicy",
    "POILayer",
    "CandidateGrid",
    "ScoreResult",
    # Lazy (heavy — scipy/sklearn/h3 pulled in only on first access):
    "ScoringEngine",
    "SweetSpotScorer",
    "AbstractFeatureExtractor",
    "ExtractorRegistry",
    "extractor_registry",
)
