"""
In-memory seed files for integration tests: PDFs, raster/SVG images, Word, Excel.

Sizes are approximate; PDFs vary by ``repeat`` payload. No third-party deps.
"""

from __future__ import annotations

import base64
import io
import random
import zipfile
import zlib
from dataclasses import dataclass


@dataclass(frozen=True)
class SeedFile:
    filename: str
    content: bytes
    content_type: str


def _png_1x1_orange() -> bytes:
    """Minimal valid 1x1 PNG (orange pixel)."""
    return (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb4"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def _jpeg_1x1() -> bytes:
    """Tiny valid baseline JPEG (1x1)."""
    return base64.b64decode(
        "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsL"
        "DBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/"
        "2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
        "MjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAFQAB"
        "AQAAAAAAAAAAAAAAAAAAAAr/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEB"
        "AQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMB"
        "AAIRAxEAPwCwAA8="
    )


def _svg_simple(label: str) -> bytes:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="80">
  <rect width="120" height="80" fill="#336699"/>
  <text x="10" y="45" fill="white" font-size="14">{label}</text>
</svg>
""".encode()


def _pdf_with_zlib_payload(payload: bytes) -> bytes:
    """Single-page PDF with one Flate-compressed content stream."""
    comp = zlib.compress(payload)
    stream_hdr = (
        f"<< /Length {len(comp)} /Filter /FlateDecode >>\nstream\n".encode("ascii")
    )
    objects = [
        b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        b"4 0 obj"
        + stream_hdr
        + comp
        + b"\nendstream\nendobj\n",
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]
    out = bytearray(b"%PDF-1.4\n")
    positions: list[int] = [0, len(out)]
    for obj in objects:
        out.extend(obj)
        positions.append(len(out))
    xref_pos = len(out)
    out.extend(b"xref\n0 6\n0000000000 65535 f \n")
    for i in range(1, 6):
        out.extend(f"{positions[i]:010d} 00000 n \n".encode("ascii"))
    out.extend(
        b"trailer<< /Size 6 /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode("ascii")
        + b"\n%%EOF\n"
    )
    return bytes(out)


def build_pdf_variants() -> tuple[SeedFile, SeedFile, SeedFile]:
    """Three PDFs with different on-wire sizes (high-entropy payload scales larger)."""
    small = _pdf_with_zlib_payload(b"SDK seed small PDF. " * 50)
    rnd = random.Random(42)
    med = _pdf_with_zlib_payload(rnd.randbytes(48_000))
    large = _pdf_with_zlib_payload(rnd.randbytes(220_000))
    return (
        SeedFile("seed_small.pdf", small, "application/pdf"),
        SeedFile("seed_medium.pdf", med, "application/pdf"),
        SeedFile("seed_large.pdf", large, "application/pdf"),
    )


def build_image_variants() -> tuple[SeedFile, SeedFile, SeedFile]:
    return (
        SeedFile("seed_icon.png", _png_1x1_orange(), "image/png"),
        SeedFile("seed_photo.jpeg", _jpeg_1x1(), "image/jpeg"),
        SeedFile("seed_vector.svg", _svg_simple("SDK"), "image/svg+xml"),
    )


def _docx_bytes(body_text: str) -> bytes:
    """Minimal OOXML .docx (Word)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/>'
            "</Relationships>",
        )
        esc = (
            body_text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        zf.writestr(
            "word/document.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body><w:p><w:r><w:t>{esc}</w:t></w:r></w:p></w:body></w:document>',
        )
    return buf.getvalue()


def _excel_col_letter(col_index: int) -> str:
    """1-based column index to Excel letter(s) (1 -> A, 27 -> AA)."""
    n = col_index
    letters = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _xlsx_bytes(sheet_values: list[list[str]]) -> bytes:
    """Minimal .xlsx with one sheet."""
    buf = io.BytesIO()
    shared: list[str] = []
    for row in sheet_values:
        for cell in row:
            if cell not in shared:
                shared.append(cell)
    shared_xml = "".join(
        f"<si><t>{s.replace('&', '&amp;').replace('<', '&lt;')}</t></si>" for s in shared
    )
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/sharedStrings.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
            "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="s1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            'Target="worksheets/sheet1.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Sheet1" sheetId="1" r:id="s1"/></sheets></workbook>',
        )
        rows_xml = []
        for r, row in enumerate(sheet_values, start=1):
            cells = []
            for c, val in enumerate(row, start=1):
                idx = shared.index(val)
                col = _excel_col_letter(c)
                cells.append(f'<c r="{col}{r}" t="s"><v>{idx}</v></c>')
            rows_xml.append(f"<row r=\"{r}\">{''.join(cells)}</row>")
        zf.writestr(
            "xl/worksheets/sheet1.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f"<sheetData>{''.join(rows_xml)}</sheetData></worksheet>",
        )
        cell_count = sum(len(r) for r in sheet_values)
        zf.writestr(
            "xl/sharedStrings.xml",
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'count="{cell_count}" uniqueCount="{len(shared)}">'
            f"{shared_xml}</sst>",
        )
    return buf.getvalue()


def build_word_variants() -> tuple[SeedFile, SeedFile, SeedFile]:
    return (
        SeedFile(
            "seed_notes_a.docx",
            _docx_bytes("Python SDK seed document A — short."),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        SeedFile(
            "seed_notes_b.docx",
            _docx_bytes("Python SDK seed document B — " + ("paragraph " * 80)),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        SeedFile(
            "seed_notes_c.docx",
            _docx_bytes(
                "Python SDK seed document C — tables of text.\n"
                + "\n".join(f"Line {i}" for i in range(120)),
            ),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
    )


def build_excel_variants() -> tuple[SeedFile, SeedFile, SeedFile]:
    return (
        SeedFile(
            "seed_sheet_1.xlsx",
            _xlsx_bytes([["ColA", "ColB"], ["1", "2"]]),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
        SeedFile(
            "seed_sheet_2.xlsx",
            _xlsx_bytes([[f"R{r}C{c}" for c in range(8)] for r in range(25)]),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
        SeedFile(
            "seed_sheet_3.xlsx",
            _xlsx_bytes([["SKU", "Qty", "Price"]] + [[str(i), str(i * 2), str(i * 10.5)] for i in range(1, 200)]),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
    )


def all_seed_files() -> list[SeedFile]:
    """All 12 seed files (3 PDF + 3 images + 3 Word + 3 Excel)."""
    out: list[SeedFile] = []
    out.extend(build_pdf_variants())
    out.extend(build_image_variants())
    out.extend(build_word_variants())
    out.extend(build_excel_variants())
    return out
