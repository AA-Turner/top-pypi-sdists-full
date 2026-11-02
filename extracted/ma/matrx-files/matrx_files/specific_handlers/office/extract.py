"""Office (OpenXML) -> markdown/portions extraction.

The whole point: turn a .docx / .pptx / .xlsx into the SAME converged shape a
PDF produces — a list of portions (page-equivalents) each carrying clean
markdown — so an AI model reads it and the RAG pipeline chunks it with zero
format-specific downstream code.

Pure python (python-docx / python-pptx / openpyxl). No LibreOffice, no network,
no host imports. Legacy binary formats (.doc/.ppt/.xls) are detected and raise
``LegacyBinaryOfficeError`` — the caller decides whether a LibreOffice
conversion is available.
"""

from __future__ import annotations

import io
import zipfile

from ..table_markdown import rows_to_markdown
from .mime import classify_office
from .models import (
    DOCX_MIME,
    PPTX_MIME,
    XLSX_MIME,
    OfficeExtraction,
    OfficeKind,
    OfficePortion,
)

# Bounds — an Office file can be enormous; a tool/RAG result that re-feeds the
# model on every loop must be bounded (the platform's tool-result-size lesson).
# These are generous but hard caps; extraction records a warning when it trims.
MAX_SHEET_ROWS = 500
MAX_SHEET_COLS = 50
MAX_CELL_CHARS = 500
#: KNOB MIRROR of platform.feature_knob "media.file_service" "plaintext_max_portion_chars" (same row as plaintext.py)
MAX_PORTION_CHARS = 200_000
# Cap the number of portions (slides/sheets) so a 10k-slide deck can't produce
# an unbounded result; the whole-document markdown is additionally bounded.
#: KNOB MIRROR of platform.feature_knob "media.file_service" "plaintext_max_portions" (same row as plaintext.py)
MAX_PORTIONS = 2_000

# Magic bytes. OLE/CFB (legacy .doc/.ppt/.xls) vs OpenXML (a zip: PK\x03\x04).
_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
_ZIP_MAGIC = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")


class OfficeExtractionError(Exception):
    """Base for Office extraction failures."""


class LegacyBinaryOfficeError(OfficeExtractionError):
    """The bytes are a legacy OLE/CFB format (.doc/.ppt/.xls) the pure-python
    codec cannot read. Requires a LibreOffice conversion step."""


class UnsupportedOfficeError(OfficeExtractionError):
    """The bytes are not a recognized Office document."""


def _looks_legacy_ole(raw: bytes) -> bool:
    """True when the bytes are an OLE/CFB container (legacy .doc/.ppt/.xls),
    regardless of filename/MIME. Bytes are truth."""
    return raw[:8] == _OLE_MAGIC


def _has_valid_ole_header(raw: bytes) -> bool:
    if len(raw) < 512 or not _looks_legacy_ole(raw):
        return False
    major_version = int.from_bytes(raw[26:28], "little")
    sector_shift = int.from_bytes(raw[30:32], "little")
    return (
        raw[28:30] == b"\xfe\xff"
        and major_version in {3, 4}
        and sector_shift == (9 if major_version == 3 else 12)
        and int.from_bytes(raw[32:34], "little") == 6
    )


def _sniff_openxml_kind(raw: bytes) -> OfficeKind | None:
    """Identify an OpenXML file from its bytes by inspecting the zip archive
    (``word/`` → docx, ``ppt/`` → pptx, ``xl/`` → xlsx). Returns None if the
    bytes aren't a readable OOXML package. This makes classification robust to a
    missing/wrong MIME and an extensionless filename."""
    if not raw[:4].startswith(_ZIP_MAGIC):
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            names = zf.namelist()
    except zipfile.BadZipFile:
        return None
    if "[Content_Types].xml" not in names and not any(
        n.startswith(("word/", "ppt/", "xl/")) for n in names
    ):
        return None
    if any(n.startswith("word/") for n in names):
        return OfficeKind.docx
    if any(n.startswith("ppt/") for n in names):
        return OfficeKind.pptx
    if any(n.startswith("xl/") for n in names):
        return OfficeKind.xlsx
    return None


def _cap_portion(text: str, warnings: list[str], label: str) -> str:
    if len(text) <= MAX_PORTION_CHARS:
        return text
    warnings.append(f"{label} trimmed to {MAX_PORTION_CHARS} chars")
    return text[:MAX_PORTION_CHARS]


def _trim(text: str, limit: int = MAX_CELL_CHARS) -> str:
    text = text or ""
    return text if len(text) <= limit else text[:limit] + "…"


# --------------------------------------------------------------------------- #
# DOCX
# --------------------------------------------------------------------------- #


def _para_is_list_item(paragraph) -> bool:  # noqa: ANN001
    """True when the paragraph carries real list numbering (``w:numPr``).

    Word's ``List Paragraph`` STYLE is applied to genuine bullet/number lists
    AND to plain indented body text alike — the actual list-ness lives in the
    paragraph's numbering properties, not the style name. Checking ``numPr``
    stops plain indented paragraphs from being rendered as bullets."""
    try:
        from docx.oxml.ns import qn

        pPr = paragraph._p.pPr
        if pPr is None:
            return False
        return pPr.find(qn("w:numPr")) is not None
    except Exception:  # noqa: BLE001 — any XML shape we don't recognize → not a list
        return False


def _iter_docx_blocks(document):  # noqa: ANN001, ANN201 — python-docx types
    """Yield paragraphs and tables in document order (python-docx exposes them
    as separate flat lists, losing interleaving)."""
    from docx.oxml.ns import qn
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    parent = document.element.body
    for child in parent.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def _docx_table_md(table) -> str:  # noqa: ANN001
    # Cells pre-trimmed only; rows_to_markdown owns escaping + table shape.
    rows = [[_trim(c.text) for c in row.cells] for row in table.rows]
    return rows_to_markdown(rows, header=True)


def _extract_docx(raw: bytes) -> OfficeExtraction:
    import docx
    from docx.table import Table

    document = docx.Document(io.BytesIO(raw))
    lines: list[str] = []
    warnings: list[str] = []

    for block in _iter_docx_blocks(document):
        if isinstance(block, Table):
            md = _docx_table_md(block)
            if md:
                lines.append(md)
                lines.append("")
            continue
        # Paragraph
        text = (block.text or "").strip()
        if not text:
            continue
        style = (getattr(block.style, "name", "") or "").lower()
        if style.startswith("heading") or style == "title":
            try:
                level = int(style.replace("heading", "").strip() or "1") if "heading" in style else 1
            except ValueError:
                level = 1
            level = max(1, min(level, 6))
            lines.append(f"{'#' * level} {text}")
        elif "list number" in style:
            lines.append(f"1. {text}")
        elif "list bullet" in style:
            lines.append(f"- {text}")
        elif _para_is_list_item(block):
            # Generic "List Paragraph" (or any style) that is actually a
            # numbered/bulleted item per its numPr — render as a list item.
            lines.append(f"- {text}")
        elif "quote" in style:
            lines.append(f"> {text}")
        else:
            lines.append(text)
        lines.append("")

    markdown = "\n".join(lines).strip()
    if len(markdown) > MAX_PORTION_CHARS:
        markdown = markdown[:MAX_PORTION_CHARS]
        warnings.append(f"document trimmed to {MAX_PORTION_CHARS} chars")

    core = document.core_properties
    metadata = {
        "paragraphs": len(document.paragraphs),
        "tables": len(document.tables),
    }
    if core.title:
        metadata["title"] = core.title
    if core.author:
        metadata["author"] = core.author

    # A .docx has no reliable page boundaries via python-docx — the whole body
    # is one portion; the chunk stage splits it downstream.
    portion = OfficePortion(
        index=0,
        number=1,
        kind="section",
        title=(core.title or None),
        markdown=markdown,
        text=markdown,
        meta={"tables": len(document.tables)},
    )
    return OfficeExtraction(
        office_kind=OfficeKind.docx,
        mime_type=DOCX_MIME,
        markdown=markdown,
        portions=[portion],
        metadata=metadata,
        warnings=warnings,
    )


# --------------------------------------------------------------------------- #
# PPTX
# --------------------------------------------------------------------------- #


def _shape_text(shape) -> list[str]:  # noqa: ANN001
    out: list[str] = []
    if getattr(shape, "has_text_frame", False):
        for para in shape.text_frame.paragraphs:
            line = "".join(run.text for run in para.runs).strip()
            if not line and para.text:
                line = para.text.strip()
            if line:
                bullet = "  " * max(getattr(para, "level", 0) or 0, 0)
                out.append(f"{bullet}- {line}")
    return out


def _table_from_shape(shape) -> str:  # noqa: ANN001
    tbl = shape.table
    rows = [[_trim(c.text) for c in r.cells] for r in tbl.rows]
    return rows_to_markdown(rows, header=True)


def _extract_pptx(raw: bytes) -> OfficeExtraction:
    from pptx import Presentation

    prs = Presentation(io.BytesIO(raw))
    portions: list[OfficePortion] = []
    doc_lines: list[str] = []
    warnings: list[str] = []

    total_slides = len(prs.slides)
    for idx, slide in enumerate(prs.slides):
        if idx >= MAX_PORTIONS:
            warnings.append(f"deck truncated to {MAX_PORTIONS} of {total_slides} slides")
            break
        number = idx + 1
        title = None
        body_lines: list[str] = []
        note_text = ""

        for shape in slide.shapes:
            if shape == slide.shapes.title or (
                getattr(shape, "is_placeholder", False)
                and getattr(shape.placeholder_format, "idx", None) == 0
            ):
                if getattr(shape, "has_text_frame", False) and shape.text_frame.text.strip():
                    title = shape.text_frame.text.strip()
                    continue
            if getattr(shape, "has_table", False):
                md = _table_from_shape(shape)
                if md:
                    body_lines.append(md)
                continue
            body_lines.extend(_shape_text(shape))

        if slide.has_notes_slide:
            nf = slide.notes_slide.notes_text_frame
            if nf is not None and nf.text.strip():
                note_text = nf.text.strip()

        header = f"## Slide {number}" + (f": {title}" if title else "")
        parts = [header]
        parts.extend(body_lines)
        if note_text:
            parts.append("")
            parts.append(f"**Speaker notes:** {note_text}")
        slide_md = _cap_portion("\n".join(parts).strip(), warnings, f"slide {number}")

        plain = "\n".join([title or f"Slide {number}", *(l.lstrip("- ") for l in body_lines), note_text]).strip()
        portions.append(
            OfficePortion(
                index=idx,
                number=number,
                kind="slide",
                title=title,
                markdown=slide_md,
                text=plain,
                meta={"has_notes": bool(note_text)},
            )
        )
        doc_lines.append(slide_md)
        doc_lines.append("")

    metadata = {"slides": total_slides}
    return OfficeExtraction(
        office_kind=OfficeKind.pptx,
        mime_type=PPTX_MIME,
        markdown="\n".join(doc_lines).strip(),
        portions=portions,
        metadata=metadata,
        warnings=warnings,
    )


# --------------------------------------------------------------------------- #
# XLSX
# --------------------------------------------------------------------------- #


def _cell_str(value) -> str:  # noqa: ANN001
    if value is None:
        return ""
    return _trim(str(value))


def _extract_xlsx(raw: bytes) -> OfficeExtraction:
    import openpyxl

    wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    portions: list[OfficePortion] = []
    doc_lines: list[str] = []
    warnings: list[str] = []

    for idx, ws in enumerate(wb.worksheets):
        if len(portions) >= MAX_PORTIONS:
            warnings.append(f"workbook truncated to {MAX_PORTIONS} sheets")
            break
        number = idx + 1
        rows_iter = ws.iter_rows(values_only=True)
        cell_rows: list[list[str]] = []  # trimmed, unescaped — rows_to_markdown escapes
        plain_rows: list[str] = []
        ncols = 0
        row_count = 0
        truncated_rows = False
        truncated_cols = False

        for r_i, row in enumerate(rows_iter):
            if r_i >= MAX_SHEET_ROWS:
                truncated_rows = True
                break
            row_count += 1
            cells = list(row)
            if len(cells) > MAX_SHEET_COLS:
                cells = cells[:MAX_SHEET_COLS]
                truncated_cols = True
            ncols = max(ncols, len(cells))
            str_cells = [_cell_str(c) for c in cells]
            cell_rows.append(str_cells)
            plain_rows.append("\t".join(str_cells))

        # Skip fully-empty sheets.
        if not any(cell.strip() for r in cell_rows for cell in r):
            continue

        table_md = rows_to_markdown(cell_rows, header=True)
        sheet_md = _cap_portion(f"## Sheet: {ws.title}\n\n{table_md}".strip(), warnings, f"sheet '{ws.title}'")
        if truncated_rows:
            note = f"\n\n_(sheet truncated to {MAX_SHEET_ROWS} rows)_"
            sheet_md += note
            warnings.append(f"sheet '{ws.title}' truncated to {MAX_SHEET_ROWS} rows")
        if truncated_cols:
            warnings.append(f"sheet '{ws.title}' truncated to {MAX_SHEET_COLS} cols")

        portions.append(
            OfficePortion(
                index=idx,
                number=number,
                kind="sheet",
                title=ws.title,
                markdown=sheet_md,
                text="\n".join(plain_rows),
                meta={"rows": row_count, "cols": ncols},
            )
        )
        doc_lines.append(sheet_md)
        doc_lines.append("")

    wb.close()
    metadata = {"sheets": len(portions)}
    return OfficeExtraction(
        office_kind=OfficeKind.xlsx,
        mime_type=XLSX_MIME,
        markdown="\n".join(doc_lines).strip(),
        portions=portions,
        metadata=metadata,
        warnings=warnings,
    )


# --------------------------------------------------------------------------- #
# Dispatch
# --------------------------------------------------------------------------- #

_EXTRACTORS = {
    OfficeKind.docx: _extract_docx,
    OfficeKind.pptx: _extract_pptx,
    OfficeKind.xlsx: _extract_xlsx,
}


def _extract_legacy(
    raw: bytes,
    mime_type: str | None,
    file_name: str | None,
    allow_libreoffice: bool,
) -> OfficeExtraction:
    """Handle OLE/CFB legacy bytes: convert to OpenXML via LibreOffice when
    available, else raise ``LegacyBinaryOfficeError``."""
    from .convert import (
        LibreOfficeUnavailable,
        OfficeConversionError,
        convert_legacy_to_openxml,
        libreoffice_available,
    )

    if not _has_valid_ole_header(raw):
        raise LegacyBinaryOfficeError(
            f"malformed or truncated legacy Office container (name={file_name!r})"
        )

    if not (allow_libreoffice and libreoffice_available()):
        raise LegacyBinaryOfficeError(
            f"legacy binary Office format (OLE/CFB, name={file_name!r}) requires "
            f"LibreOffice conversion, which is unavailable on this host"
        )
    # Name/MIME only hints WHICH legacy format; default to .doc if unknown.
    legacy_kind = classify_office(mime_type, file_name)
    if legacy_kind is None or not legacy_kind.is_legacy_binary:
        legacy_kind = OfficeKind.doc
    try:
        converted, new_kind = convert_legacy_to_openxml(raw, legacy_kind)
    except (LibreOfficeUnavailable, OfficeConversionError) as exc:
        raise LegacyBinaryOfficeError(f"legacy conversion failed: {exc}") from exc
    try:
        extraction = _EXTRACTORS[new_kind](converted)
    except (zipfile.BadZipFile, KeyError, ValueError) as exc:
        raise UnsupportedOfficeError(
            f"converted legacy document was unreadable (name={file_name!r}): "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    extraction.warnings.append(f"converted from legacy {legacy_kind.value} via LibreOffice")
    return extraction


def extract_office(
    raw: bytes,
    *,
    mime_type: str | None = None,
    file_name: str | None = None,
    allow_libreoffice: bool = True,
) -> OfficeExtraction:
    """Extract Office bytes to the converged markdown/portions representation.

    Classification is **bytes-first**: an OLE/CFB container is a legacy binary
    regardless of what its name/MIME claim, and an OpenXML package is identified
    by inspecting the zip — so a legacy .doc renamed .docx, or a real .docx with
    no extension, is handled correctly. Name/MIME are only the fallback when the
    bytes are inconclusive.

    Legacy binary (.doc/.ppt/.xls): if LibreOffice is available on this host
    (``allow_libreoffice`` and ``soffice`` installed) the bytes are converted to
    OpenXML and extracted; otherwise ``LegacyBinaryOfficeError`` is raised. Any
    non-readable bytes raise ``UnsupportedOfficeError`` — the error contract
    callers rely on; underlying zip/parse errors never leak."""
    # Bytes win. OLE magic → legacy binary, no matter the name/MIME.
    if _looks_legacy_ole(raw):
        return _extract_legacy(raw, mime_type, file_name, allow_libreoffice)

    kind = _sniff_openxml_kind(raw) or classify_office(mime_type, file_name)
    if kind is None:
        raise UnsupportedOfficeError(
            f"not a readable Office document (mime={mime_type!r}, name={file_name!r})"
        )
    if kind.is_legacy_binary:
        # Name/MIME said legacy but the bytes weren't OLE (corrupt/misnamed).
        raise LegacyBinaryOfficeError(
            f"legacy binary Office format {kind.value!r} requires LibreOffice conversion"
        )

    try:
        return _EXTRACTORS[kind](raw)
    except (zipfile.BadZipFile, KeyError, ValueError) as exc:
        # A parser blew up on malformed/encrypted/mislabeled bytes — convert to
        # the documented error type so `except OfficeExtractionError` catches it.
        raise UnsupportedOfficeError(
            f"failed to read Office document (kind={kind.value}, "
            f"name={file_name!r}): {type(exc).__name__}: {exc}"
        ) from exc


__all__ = [
    "extract_office",
    "OfficeExtractionError",
    "LegacyBinaryOfficeError",
    "UnsupportedOfficeError",
    "MAX_SHEET_ROWS",
    "MAX_SHEET_COLS",
]
