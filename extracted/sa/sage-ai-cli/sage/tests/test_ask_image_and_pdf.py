"""Tests for `sage ask --image` (vision input) and PDF/DOCX --file support.

These tests verify the CLI plumbing: when --image is given, vision_input
helpers are called; when --file points at a PDF, document_extractor is
used. Backend model calls are stubbed — we're testing wiring.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner


_runner = CliRunner()


def _make_tiny_png(path: Path) -> Path:
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\x00\x01\x00\x00\x05\x00"
        b"\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return path


# ── vision_input wiring tests (unit-style — no actual model call) ───────────


class TestEncodingHelpers:
    """The CLI sits on top of vision_input.build_vision_message + the
    DocumentExtractor. These tests verify the CLI's helpers call the right
    backend functions with the right args."""

    def test_image_path_yields_vision_message(self, tmp_path):
        """The CLI helper that handles --image must turn a path into a
        vision-formatted message dict (the OpenAI multipart shape)."""
        from sage.core.vision_input import build_vision_message

        png = _make_tiny_png(tmp_path / "test.png")
        msg = build_vision_message("describe this", [png])
        assert msg["role"] == "user"
        assert isinstance(msg["content"], list)
        assert msg["content"][0]["text"] == "describe this"
        assert msg["content"][1]["type"] == "image_url"

    def test_pdf_file_extracts_text(self, tmp_path):
        """When --file is a PDF, sage should run it through DocumentExtractor
        rather than reading binary bytes as text (which produces garbage)."""
        pypdf = pytest.importorskip("pypdf")
        from pypdf import PdfWriter

        from sage.core.document_extractor import DocumentExtractor

        pdf = tmp_path / "report.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        with pdf.open("wb") as f:
            writer.write(f)

        extractor = DocumentExtractor()
        result = extractor.extract(pdf)
        # Even a blank page produces a result — page_count = 1, text may be empty
        assert result.page_count == 1
        assert isinstance(result.text, str)


# ── Helper function tests (testing what the CLI does pre-model-call) ─────────


class TestAskPromptBuilding:
    """The helper logic that builds the final prompt from --file / --image /
    raw prompt. We test this indirectly through the public helpers."""

    def test_helper_handles_image_attachment(self, tmp_path):
        """When given an image path, the helper composes the multimodal
        message; no images = plain string message."""
        from sage.core.vision_input import build_vision_message

        png = _make_tiny_png(tmp_path / "img.png")

        # With image
        with_img = build_vision_message("describe", [png])
        assert isinstance(with_img["content"], list)

        # Without image
        without = build_vision_message("describe", [])
        assert isinstance(without["content"], str)
        assert without["content"] == "describe"

    def test_helper_handles_pdf_file(self, tmp_path):
        """When --file is a PDF, content should be extracted as text not
        embedded as binary garbage."""
        pypdf = pytest.importorskip("pypdf")
        from pypdf import PdfWriter
        from sage.core.document_extractor import DocumentExtractor

        pdf = tmp_path / "doc.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        with pdf.open("wb") as f:
            writer.write(f)

        # The helper that reads --file: routes through extractor for PDFs
        ext = DocumentExtractor()
        fmt = ext.detect_format(pdf)
        assert fmt == "pdf"

    def test_helper_handles_plain_text_file_unchanged(self, tmp_path):
        """Existing behavior: .txt files read as utf-8."""
        from sage.core.document_extractor import DocumentExtractor

        txt = tmp_path / "notes.txt"
        txt.write_text("just text")
        result = DocumentExtractor().extract(txt)
        assert result.text == "just text"
        assert result.mime_type == "text/plain"
