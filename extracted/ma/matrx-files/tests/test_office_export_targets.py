"""Download → OpenDocument / Rich Text: the converter refuses pairs we don't offer, and (where
LibreOffice is installed) produces real .odt / .rtf bytes from a real .docx."""

import io
import zipfile

import pytest

from matrx_files.specific_handlers.office.convert import (
    OfficeConversionError,
    convert_openxml_to_open_format,
    libreoffice_available,
)


def _minimal_docx(text: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>',
        )
        z.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
        )
        z.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>",
        )
    return buf.getvalue()


def test_unknown_target_is_refused_not_passed_through():
    with pytest.raises(OfficeConversionError):
        convert_openxml_to_open_format(b"x", input_suffix=".docx", target="exe")


def test_wrong_source_for_target_is_refused():
    with pytest.raises(OfficeConversionError):
        convert_openxml_to_open_format(b"x", input_suffix=".xlsx", target="odt")


@pytest.mark.skipif(not libreoffice_available(), reason="LibreOffice not installed on this host")
def test_docx_becomes_real_odt_and_rtf():
    docx = _minimal_docx("hello open formats")
    odt, odt_mime = convert_openxml_to_open_format(docx, input_suffix=".docx", target="odt")
    assert odt[:2] == b"PK" and odt_mime == "application/vnd.oasis.opendocument.text"
    with zipfile.ZipFile(io.BytesIO(odt)) as z:
        assert b"hello open formats" in z.read("content.xml")
    rtf, rtf_mime = convert_openxml_to_open_format(docx, input_suffix=".docx", target="rtf")
    assert rtf.startswith(b"{\\rtf") and b"hello open formats" in rtf and rtf_mime == "application/rtf"
