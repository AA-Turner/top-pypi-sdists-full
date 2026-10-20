"""Scrapling needs cssselect>=1.5; readability-lxml 0.9 declares <1.4 out of caution (uv override in the
root pyproject). Prove readability still extracts with the installed cssselect."""

from __future__ import annotations

import pytest

readability = pytest.importorskip("readability")


def test_readability_extracts_with_installed_cssselect() -> None:
    html = "<html><head><title>T</title></head><body><article><p>" + ("Real sentence of content. " * 40) + "</p></article></body></html>"
    doc = readability.Document(html)
    assert "Real sentence of content." in doc.summary()
