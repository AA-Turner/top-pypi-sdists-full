"""CLI PDF @file routing regressions."""

from __future__ import annotations

import sys
from unittest.mock import patch

from anteroom.cli.repl import _expand_file_references
from anteroom.services.document_extractor import ExtractionResult


def test_pdf_file_reference_inlines_extracted_text(tmp_path):
    pdf = tmp_path / "report.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")

    with patch(
        "anteroom.services.document_extractor.extract_text",
        return_value=ExtractionResult(text="Quarterly report content"),
    ):
        result = _expand_file_references("summarize @report.pdf", str(tmp_path))

    assert "Quarterly report content" in result
    assert 'name="report.pdf"' in result
    assert 'source="inline_pdf_extraction"' in result
    assert "Use the appropriate tool" not in result
    assert "use tools to read this file" not in result


def test_pdf_file_reference_missing_pypdf_reports_failure_without_tool_routing(tmp_path):
    pdf = tmp_path / "scan.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")

    with patch.dict(sys.modules, {"pypdf": None}):
        result = _expand_file_references("read @scan.pdf", str(tmp_path))

    assert "PDF text could not be extracted automatically" in result
    assert "pypdf not installed" in result
    assert "anteroom[docs]" not in result
    assert 'name="scan.pdf"' in result
    assert str(pdf) not in result
    assert "Use the appropriate tool" not in result
    assert "use tools to read this file" not in result


def test_bare_pdf_path_inlines_extracted_text_before_tool_routing(tmp_path):
    pdf = tmp_path / "ID Card.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake pdf")

    with patch(
        "anteroom.services.document_extractor.extract_text",
        return_value=ExtractionResult(text="Name: Example Person"),
    ):
        result = _expand_file_references(f"{pdf} what's in this pdf", str(tmp_path))

    assert "Name: Example Person" in result
    assert "what's in this pdf" in result
    assert 'name="ID Card.pdf"' in result
    assert str(pdf) not in result
    assert 'source="inline_pdf_extraction"' in result
    assert "Use the appropriate tool" not in result
    assert "use tools to read this file" not in result
    assert "docx" not in result.lower()
