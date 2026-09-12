"""Regression guards for the public PEP 562 lazy-export surface."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

import matrx_scraper
from matrx_mandate_scan.adapters.python import scan_source


PACKAGE_INIT = Path(matrx_scraper.__file__).resolve()


def test_lazy_export_targets_are_literal_and_scannable() -> None:
    """The safety scan must audit every deferred public module import."""
    result = scan_source(PACKAGE_INIT.read_text(encoding="utf-8"), str(PACKAGE_INIT))

    assert "UNRESOLVED_IMPORT" not in {finding.code for finding in result.findings}
    assert set(matrx_scraper._LAZY_IMPORTS.values()) == set(matrx_scraper._MODULE_LOADERS)


def test_lazy_export_keeps_cache_identity_and_unknown_attributes_are_loud() -> None:
    """A resolved export is cached; an absent public name remains an AttributeError."""
    name = "ScrapeOptions"
    original = matrx_scraper.__dict__.pop(name, None)
    sys.modules.pop("matrx_scraper.scrape_options", None)
    try:
        first = getattr(matrx_scraper, name)
        assert getattr(matrx_scraper, name) is first
        assert matrx_scraper.__dict__[name] is first
        with pytest.raises(AttributeError, match="has no attribute 'not_a_scraper_export'"):
            getattr(matrx_scraper, "not_a_scraper_export")
    finally:
        if original is not None:
            matrx_scraper.__dict__[name] = original
        else:
            matrx_scraper.__dict__.pop(name, None)


def test_known_export_preserves_loud_missing_module_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Known names do not turn an unavailable optional module into a fake export."""
    original = matrx_scraper.__dict__.pop("ScrapeOptions", None)
    monkeypatch.setitem(
        matrx_scraper._MODULE_LOADERS,
        "matrx_scraper.scrape_options",
        lambda: (_ for _ in ()).throw(ModuleNotFoundError("optional module unavailable")),
    )
    try:
        with pytest.raises(ModuleNotFoundError, match="optional module unavailable"):
            getattr(matrx_scraper, "ScrapeOptions")
    finally:
        if original is not None:
            matrx_scraper.__dict__["ScrapeOptions"] = original


@pytest.mark.parametrize(
    ("alias", "module_path", "source_name"),
    [
        ("CustomExtractor", "matrx_scraper.custom_extractors", "Extractor"),
        ("find_extractors_for_url", "matrx_scraper.custom_extractors", "find_for_url"),
        ("run_custom_extractors", "matrx_scraper.custom_extractors", "run_all"),
        ("run_custom_extractor", "matrx_scraper.custom_extractors", "run_extractor"),
        ("PageRankEdge", "matrx_scraper.pagerank", "Edge"),
    ],
)
def test_public_lazy_aliases_resolve_to_their_canonical_source(
    alias: str, module_path: str, source_name: str
) -> None:
    """Public compatibility aliases remain deferred and keep source identity."""
    original = matrx_scraper.__dict__.pop(alias, None)
    try:
        expected = getattr(importlib.import_module(module_path), source_name)
        assert getattr(matrx_scraper, alias) is expected
        assert getattr(matrx_scraper, alias) is expected
    finally:
        if original is not None:
            matrx_scraper.__dict__[alias] = original
        else:
            matrx_scraper.__dict__.pop(alias, None)
