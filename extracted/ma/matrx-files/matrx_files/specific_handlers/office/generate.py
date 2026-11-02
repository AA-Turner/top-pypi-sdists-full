"""Structured spec -> Office bytes.

The inverse of ``extract``: an agent authors a ``DocumentSpec`` /
``PresentationSpec`` / ``SpreadsheetSpec`` (the canonical "what we want a Word
doc / deck / sheet to be"), and this renders real .docx / .pptx / .xlsx bytes.

Because the input is structured, generation is deterministic and cheap — the AI
only has to fill the structure, never emit raw OpenXML. Pure python; no
LibreOffice. The result is base64 so it round-trips through JSON/persistence;
the host decodes and writes it to /assets.
"""

from __future__ import annotations

import base64
import io

from .models import (
    DOCX_MIME,
    PPTX_MIME,
    XLSX_MIME,
    DocumentSpec,
    OfficeGenerationResult,
    OfficeKind,
    PresentationSpec,
    SheetSpec,
    SpreadsheetSpec,
)


def _wrap(kind: OfficeKind, mime: str, ext: str, data: bytes) -> OfficeGenerationResult:
    return OfficeGenerationResult(
        office_kind=kind,
        mime_type=mime,
        extension=ext,
        base64_data=base64.b64encode(data).decode("ascii"),
        byte_size=len(data),
    )


# --------------------------------------------------------------------------- #
# DOCX
# --------------------------------------------------------------------------- #


def generate_docx(spec: DocumentSpec) -> OfficeGenerationResult:
    import docx

    document = docx.Document()
    if spec.title:
        document.add_heading(spec.title, level=0)

    for block in spec.blocks:
        if block.type == "heading":
            document.add_heading(block.text, level=max(1, min(block.level, 6)))
        elif block.type == "paragraph":
            document.add_paragraph(block.text)
        elif block.type == "bullet":
            document.add_paragraph(block.text, style="List Bullet")
        elif block.type == "numbered":
            document.add_paragraph(block.text, style="List Number")
        elif block.type == "quote":
            document.add_paragraph(block.text, style="Intense Quote")
        elif block.type == "page_break":
            document.add_page_break()
        elif block.type == "table" and block.rows:
            ncols = max(len(r) for r in block.rows)
            table = document.add_table(rows=0, cols=ncols)
            table.style = "Light Grid Accent 1"
            for r_i, row in enumerate(block.rows):
                cells = table.add_row().cells
                for c_i in range(ncols):
                    cells[c_i].text = str(row[c_i]) if c_i < len(row) else ""
                if r_i == 0 and block.header:
                    for cell in cells:
                        for para in cell.paragraphs:
                            for run in para.runs:
                                run.bold = True

    buf = io.BytesIO()
    document.save(buf)
    return _wrap(OfficeKind.docx, DOCX_MIME, ".docx", buf.getvalue())


# --------------------------------------------------------------------------- #
# PPTX
# --------------------------------------------------------------------------- #


def _find_body_placeholder(slide):  # noqa: ANN001, ANN201 — python-pptx types
    """The slide's content/body placeholder (never the subtitle or title).

    Subtitle placeholders also carry idx 1 on a title layout, so matching idx
    alone routes bullets into the subtitle. Match by placeholder TYPE instead."""
    from pptx.enum.shapes import PP_PLACEHOLDER

    body_types = {PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT}
    for ph in slide.placeholders:
        try:
            if ph.placeholder_format.type in body_types:
                return ph
        except Exception:  # noqa: BLE001
            continue
    return None


def generate_pptx(spec: PresentationSpec) -> OfficeGenerationResult:
    from pptx import Presentation
    from pptx.util import Inches, Pt

    prs = Presentation()
    blank = prs.slide_layouts[6]
    title_slide = prs.slide_layouts[0]
    title_content = prs.slide_layouts[1]
    section_layout = prs.slide_layouts[2] if len(prs.slide_layouts) > 2 else title_slide

    # Optional cover slide.
    if spec.title:
        s = prs.slides.add_slide(title_slide)
        s.shapes.title.text = spec.title
        if spec.subtitle and len(s.placeholders) > 1:
            s.placeholders[1].text = spec.subtitle

    for slide_spec in spec.slides:
        layout = {
            "title": title_slide,
            "title_content": title_content,
            "section": section_layout,
            "blank": blank,
        }.get(slide_spec.layout, title_content)
        s = prs.slides.add_slide(layout)

        # Title: use the layout's title placeholder if it has one, else a
        # textbox so a titled slide on a title-less layout (e.g. "blank") still
        # shows its title instead of silently dropping it.
        if slide_spec.title:
            if s.shapes.title is not None:
                s.shapes.title.text = slide_spec.title
            else:
                box = s.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
                box.text_frame.text = slide_spec.title

        # Body: bullets take priority; fall back to `body`. Find a real body
        # placeholder (idx 1), but NEVER a subtitle (idx 1 on a title layout is
        # the subtitle) — only BODY/CONTENT/OBJECT placeholders hold bullets.
        lines = slide_spec.bullets or ([slide_spec.body] if slide_spec.body else [])
        if lines:
            body_ph = _find_body_placeholder(s)
            tf = body_ph.text_frame if body_ph is not None else (
                # No content placeholder on this layout → drop in a textbox so
                # the content is never silently lost.
                s.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5)).text_frame
            )
            tf.clear()
            for i, line in enumerate(lines):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                para.text = line
                para.font.size = Pt(18)

        if slide_spec.notes:
            s.notes_slide.notes_text_frame.text = slide_spec.notes

    buf = io.BytesIO()
    prs.save(buf)
    return _wrap(OfficeKind.pptx, PPTX_MIME, ".pptx", buf.getvalue())


# --------------------------------------------------------------------------- #
# XLSX
# --------------------------------------------------------------------------- #


def generate_xlsx(spec: SpreadsheetSpec) -> OfficeGenerationResult:
    import openpyxl
    from openpyxl.styles import Font

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # drop the default sheet; we add our own

    sheets = spec.sheets or [SheetSpec()]
    for sheet_spec in sheets:
        ws = wb.create_sheet(title=(sheet_spec.name or "Sheet")[:31])
        if sheet_spec.columns:
            ws.append(list(sheet_spec.columns))
            for cell in ws[1]:
                cell.font = Font(bold=True)
            if sheet_spec.freeze_header:
                ws.freeze_panes = "A2"
        for row in sheet_spec.rows:
            ws.append(list(row))

    if not wb.sheetnames:
        wb.create_sheet(title="Sheet1")

    buf = io.BytesIO()
    wb.save(buf)
    return _wrap(OfficeKind.xlsx, XLSX_MIME, ".xlsx", buf.getvalue())


def generate_office(spec: DocumentSpec | PresentationSpec | SpreadsheetSpec) -> OfficeGenerationResult:
    """Render a spec to Office bytes, dispatching on the spec type."""
    if isinstance(spec, DocumentSpec):
        return generate_docx(spec)
    if isinstance(spec, PresentationSpec):
        return generate_pptx(spec)
    if isinstance(spec, SpreadsheetSpec):
        return generate_xlsx(spec)
    raise TypeError(f"unsupported office spec type: {type(spec).__name__}")


__all__ = [
    "generate_office",
    "generate_docx",
    "generate_pptx",
    "generate_xlsx",
]
