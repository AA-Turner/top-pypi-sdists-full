"""Text documents (markdown, plaintext, csv, json, …) must NOT be shipped to
Anthropic/OpenAI as a PDF-oriented base64 document block — that 400s the whole
request (live incident 2026-06-29: ``media_type: Input should be
'application/pdf'``). They must be decoded and delivered as text. PDFs are
unaffected. Binary non-PDFs drop rather than emit a malformed payload.
"""

from __future__ import annotations

import base64

from matrx_ai.config.media_config import (
    DocumentContent,
    decode_document_text,
    is_pdf_mime,
    is_text_document_mime,
)

_MD = "# Title\n\nSome **markdown** body.\n"
_MD_B64 = base64.b64encode(_MD.encode("utf-8")).decode("ascii")


def test_markdown_anthropic_is_text_source_not_base64():
    doc = DocumentContent(base64_data=_MD_B64, mime_type="text/markdown")
    out = doc.to_anthropic()
    assert out["type"] == "document"
    assert out["source"]["type"] == "text"
    assert out["source"]["media_type"] == "text/plain"
    assert out["source"]["data"] == _MD
    # The pre-fix bug: base64 source with a non-pdf media_type.
    assert out["source"].get("media_type") != "text/markdown"


def test_markdown_openai_is_input_text_not_input_file():
    doc = DocumentContent(base64_data=_MD_B64, mime_type="text/markdown")
    out = doc.to_openai()
    assert out["type"] == "input_text"
    assert out["text"] == _MD


def test_plaintext_and_json_route_to_text():
    for mime in ("text/plain", "application/json", "text/csv"):
        doc = DocumentContent(base64_data=_MD_B64, mime_type=mime)
        assert doc.to_anthropic()["source"]["type"] == "text"
        assert doc.to_openai()["type"] == "input_text"


def test_pdf_still_uses_base64_source():
    pdf_b64 = base64.b64encode(b"%PDF-1.4 fake").decode("ascii")
    doc = DocumentContent(base64_data=pdf_b64, mime_type="application/pdf")
    anthropic = doc.to_anthropic()
    assert anthropic["source"]["type"] == "base64"
    assert anthropic["source"]["media_type"] == "application/pdf"
    openai = doc.to_openai()
    assert openai["type"] == "input_file"


def test_binary_nonpdf_drops_rather_than_malform():
    # 0xFF 0xFE is not valid UTF-8 — a binary file mislabeled as a document.
    binary_b64 = base64.b64encode(b"\xff\xfe\x00\x01").decode("ascii")
    doc = DocumentContent(base64_data=binary_b64, mime_type="application/octet-stream")
    assert doc.to_anthropic() is None
    assert doc.to_openai() is None


def test_mime_classifiers():
    assert is_pdf_mime("application/pdf")
    assert is_pdf_mime("application/pdf; charset=binary")
    assert not is_pdf_mime("text/markdown")
    assert is_text_document_mime("text/markdown")
    assert is_text_document_mime("application/json")
    assert not is_text_document_mime("application/pdf")
    assert not is_text_document_mime("image/png")


def test_decode_document_text_rejects_binary():
    assert decode_document_text(_MD_B64) == _MD
    assert decode_document_text(base64.b64encode(b"\xff\xfe").decode("ascii")) is None
