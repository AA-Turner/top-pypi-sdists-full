"""Tests for ``resolve_general_doc_path``."""

from __future__ import annotations

import importlib.resources
from pathlib import Path

import pytest

from agentic_devtools.cli.setup import expectations_specializer
from agentic_devtools.cli.setup.expectations_specializer import resolve_general_doc_path

_CANONICAL_DOC = Path(__file__).parents[5] / "docs" / "setup-expectations" / "agdt-setup.md"


class TestResolveGeneralDocPath:
    """FR-004 canonical-checkout-first resolution order."""

    def test_prefers_checkout_doc(self) -> None:
        """The canonical checkout doc is preferred when it exists."""
        resolved = resolve_general_doc_path()
        assert resolved is not None
        assert "docs/setup-expectations" in resolved.as_posix()
        assert resolved.exists()

    def test_falls_back_to_packaged_resource(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When the checkout doc is absent, the packaged resource is used."""

        def fake_exists(self: Path) -> bool:
            return "resources/setup-expectations" in self.as_posix()

        monkeypatch.setattr(expectations_specializer.Path, "exists", fake_exists)
        resolved = resolve_general_doc_path()
        assert resolved is not None
        assert "resources/setup-expectations" in resolved.as_posix()

    def test_returns_none_when_neither_exists(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When neither path exists, ``None`` is returned."""
        monkeypatch.setattr(expectations_specializer.Path, "exists", lambda self: False)
        assert resolve_general_doc_path() is None

    def test_packaged_resource_matches_canonical_doc(self) -> None:
        """Byte-for-byte parity: packaged resource must not drift from the canonical doc.

        The packaged resource is the installed-wheel fallback when the source checkout is
        absent.  If the two files diverge, wheels will produce a specialized document that
        misstates current setup behaviour.  This test fails immediately when the files
        diverge, preventing silent drift.

        Only applicable in a source-checkout environment where the canonical doc exists.
        """
        if not _CANONICAL_DOC.exists():
            pytest.skip("Canonical doc not present — source-checkout only test")
        pkg = importlib.resources.files("agentic_devtools") / "resources" / "setup-expectations" / "agdt-setup.md"
        packaged_bytes = pkg.read_bytes()
        canonical_bytes = _CANONICAL_DOC.read_bytes()
        assert packaged_bytes == canonical_bytes, (
            "agentic_devtools/resources/setup-expectations/agdt-setup.md has drifted from "
            "docs/setup-expectations/agdt-setup.md. "
            "Copy the canonical document over the packaged resource to restore parity."
        )
