"""The synthetic PDF corpus (PDF-PLAN U1): small PDFs GENERATED inside the test, never stored.

Why generated: a golden corpus that exists on one machine is not a forcing test. Every file here is
rebuilt from this module by any developer, in a bare venv, from ``pikepdf`` + ``Pillow`` only -
and, on purpose, NEVER from PyMuPDF (the AGPL guard ``scripts/check_no_new_pymupdf_imports.py``
fails a new importer).

Each :class:`CorpusPdf` carries its own EXPECTED output (the golden): the native text per page, or,
for a scanned page, the words the OCR must find. The runner
(``test_pdf_corpus_extraction.py``) holds today's extractor to it, so a planted change in
``extract_text_pages`` turns it red. The 500-page case is a parameter (``long_document(pages=500)``),
not a stored file.

Kinds covered (the plan's list): digital, scanned image, mixed digital+scanned, rotated, encrypted,
tables, accented/non-ASCII text, AcroForm, multi-page. Shapes are built from raw PDF objects so the
corpus has no engine of its own to disagree with.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field

#: Page size in points (US Letter).
PAGE_W, PAGE_H = 612, 792

#: Words a scanned page must yield after OCR. Large, high-contrast, so tesseract is stable across
#: versions; the runner asserts these as a CONTAINS check, never an exact string.
SCAN_WORDS = ("invoice", "total", "balance")


@dataclass(frozen=True)
class CorpusPdf:
    name: str
    data: bytes
    page_count: int
    #: Expected native text per page ("" for a scanned page). Compared after whitespace collapse.
    native_text: tuple[str, ...]
    #: Pages that carry no text layer (scanned image) and must go to OCR.
    scanned_pages: tuple[int, ...] = ()
    #: Per-page /Rotate values (degrees) when not all zero.
    rotations: tuple[int, ...] = ()
    #: Words OCR must find on a scanned page (page index -> words). A scanned page absent here is a
    #: KNOWN LIMIT of today's OCR (see ``scanned_rotated``) and is only held to "went to OCR".
    ocr_words: dict[int, tuple[str, ...]] = field(default_factory=dict)
    password: str | None = None
    tags: frozenset[str] = field(default_factory=frozenset)


#: Native-text pages carry at least this much text, like real documents: the extractor's default
#: ``use_ocr_threshold=100`` sends a SHORTER page to OCR (a named behaviour, tested separately).
FILLER = " The quick brown fox jumps over the lazy dog near the quiet river bank."


def _pikepdf():
    import pytest

    return pytest.importorskip("pikepdf")


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(lines: list[tuple[int, int, str]], width: int = 62) -> list[tuple[int, int, str]]:
    """Break any line longer than ``width`` characters at word boundaries (one text line per row)."""
    out: list[tuple[int, int, str]] = []
    for x, y, text in lines:
        words, row, offset = text.split(), "", 0
        for word in words:
            if row and len(row) + 1 + len(word) > width:
                out.append((x, y - offset, row))
                row, offset = word, offset + 16
            else:
                row = f"{row} {word}".strip()
        out.append((x, y - offset, row))
    return out


def _text_stream(lines: list[tuple[int, int, str]], size: int = 12) -> bytes:
    """One content stream placing each ``(x, y, text)`` with Helvetica. Latin-1 encoded."""
    ops = [f"BT /F1 {size} Tf".encode()]
    last_x = last_y = 0
    for x, y, text in _wrap(lines):
        ops.append(f"{x - last_x} {y - last_y} Td ".encode() + b"(" + _escape(text).encode("latin-1") + b") Tj")
        last_x, last_y = x, y
    ops.append(b"ET")
    return b"\n".join(ops)


def _new_pdf():
    pikepdf = _pikepdf()
    pdf = pikepdf.new()
    font = pdf.make_indirect(
        pikepdf.Dictionary(
            Type=pikepdf.Name.Font,
            Subtype=pikepdf.Name.Type1,
            BaseFont=pikepdf.Name.Helvetica,
            Encoding=pikepdf.Name.WinAnsiEncoding,
        )
    )
    return pdf, font


def _add_text_page(pdf, font, lines: list[tuple[int, int, str]], rotate: int = 0):
    pikepdf = _pikepdf()
    page = pdf.add_blank_page(page_size=(PAGE_W, PAGE_H))
    page.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
    page.Contents = pdf.make_stream(_text_stream(lines))
    if rotate:
        page.Rotate = rotate
    return page


def _scan_jpeg(words: tuple[str, ...]) -> tuple[bytes, int, int]:
    """A page-sized grayscale JPEG of big black words on white - what a scanner hands us."""
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1275, 1650  # 150 dpi US Letter
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=90)
    y = 200
    for word in words:
        draw.text((150, y), word.upper(), fill=0, font=font)
        y += 220
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=92)
    return buffer.getvalue(), width, height


def _add_scanned_page(pdf, words: tuple[str, ...] = SCAN_WORDS, rotate: int = 0):
    pikepdf = _pikepdf()
    jpeg, width, height = _scan_jpeg(words)
    image = pdf.make_stream(jpeg)
    image.Type = pikepdf.Name.XObject
    image.Subtype = pikepdf.Name.Image
    image.Width, image.Height = width, height
    image.ColorSpace = pikepdf.Name.DeviceGray
    image.BitsPerComponent = 8
    image.Filter = pikepdf.Name.DCTDecode
    page = pdf.add_blank_page(page_size=(PAGE_W, PAGE_H))
    page.Resources = pikepdf.Dictionary(XObject=pikepdf.Dictionary(Im0=image))
    page.Contents = pdf.make_stream(f"q {PAGE_W} 0 0 {PAGE_H} 0 0 cm /Im0 Do Q".encode())
    if rotate:
        page.Rotate = rotate
    return page


def _save(pdf, **kwargs) -> bytes:
    buffer = io.BytesIO()
    # qpdf refuses a deterministic id for an encrypted file; everything else is byte-stable.
    pdf.save(buffer, deterministic_id="encryption" not in kwargs, **kwargs)
    return buffer.getvalue()


def _collapse(text: str) -> str:
    return " ".join(text.split())


def digital() -> CorpusPdf:
    pdf, font = _new_pdf()
    pages = [  # noqa: E501
        [(72, 720, "Lease agreement clause marker-1"), (72, 700, "The tenant shall pay rent monthly on the first day." + FILLER)],
        [(72, 720, "Lease agreement clause marker-2"), (72, 700, "The landlord shall maintain the common areas of the building." + FILLER)],
    ]
    for lines in pages:
        _add_text_page(pdf, font, lines)
    expected = tuple(_collapse(" ".join(t for _, _, t in lines)) for lines in pages)
    return CorpusPdf("digital", _save(pdf), 2, expected, tags=frozenset({"digital"}))


def scanned() -> CorpusPdf:
    pdf, _ = _new_pdf()
    _add_scanned_page(pdf)
    return CorpusPdf(
        "scanned", _save(pdf), 1, ("",), scanned_pages=(0,), ocr_words={0: SCAN_WORDS}, tags=frozenset({"scanned"})
    )


def mixed() -> CorpusPdf:
    """Digital, scanned, digital: the case a per-page OCR fallback exists for."""
    pdf, font = _new_pdf()
    first = [(72, 720, "Cover page marker-first with enough native text to skip OCR entirely." + FILLER)]
    last = [(72, 720, "Closing page marker-last with enough native text to skip OCR entirely." + FILLER)]
    _add_text_page(pdf, font, first)
    _add_scanned_page(pdf)
    _add_text_page(pdf, font, last)
    expected = (_collapse(first[0][2]), "", _collapse(last[0][2]))
    return CorpusPdf(
        "mixed",
        _save(pdf),
        3,
        expected,
        scanned_pages=(1,),
        ocr_words={1: SCAN_WORDS},
        tags=frozenset({"mixed", "scanned"}),
    )


def rotated() -> CorpusPdf:
    pdf, font = _new_pdf()
    rotations = (0, 90, 180, 270)
    expected = []
    for degrees in rotations:
        text = f"Rotated page marker-{degrees} read the same text regardless of the rotate flag." + FILLER
        _add_text_page(pdf, font, [(72, 720, text)], rotate=degrees)
        expected.append(_collapse(text))
    return CorpusPdf(
        "rotated", _save(pdf), 4, tuple(expected), rotations=rotations, tags=frozenset({"rotated", "digital"})
    )


def encrypted(password: str = "open-sesame") -> CorpusPdf:
    pikepdf = _pikepdf()
    pdf, font = _new_pdf()
    text = "Confidential board minutes marker-secret protected by an open password." + FILLER
    _add_text_page(pdf, font, [(72, 720, text)])
    data = _save(pdf, encryption=pikepdf.Encryption(user=password, owner=password + "-owner", R=6))
    return CorpusPdf(
        "encrypted", data, 1, (_collapse(text),), password=password, tags=frozenset({"encrypted", "digital"})
    )


def tables() -> CorpusPdf:
    """A ruled-less 3x3 table laid out by position - the shape table detectors read."""
    pdf, font = _new_pdf()
    rows = [("Item", "Qty", "Price"), ("Widget", "4", "10.00"), ("Gadget", "2", "25.50")]
    lines = [(72 + col * 150, 720 - row * 24, cell) for row, cells in enumerate(rows) for col, cell in enumerate(cells)]
    lines.append((72, 600, "Order summary table with three columns and two data rows." + FILLER))
    _add_text_page(pdf, font, lines)
    expected = (_collapse(" ".join(text for _, _, text in lines)),)
    return CorpusPdf("tables", _save(pdf), 1, expected, tags=frozenset({"tables", "digital"}))


def accented() -> CorpusPdf:
    """Non-ASCII Latin text (WinAnsi). CJK/Cyrillic need an embedded font and are NOT covered here."""
    pdf, font = _new_pdf()
    text = "Café crème brûlée über naïve façade señor" + FILLER
    _add_text_page(pdf, font, [(72, 720, text)])
    return CorpusPdf("accented", _save(pdf), 1, (_collapse(text),), tags=frozenset({"accented", "digital"}))


def scanned_multi() -> CorpusPdf:
    """Three scanned pages with different words: per-page OCR must not bleed between pages."""
    pdf, _ = _new_pdf()
    sets = (("alpha", "bravo", "charlie"), ("delta", "echo", "foxtrot"), ("golf", "hotel", "india"))
    for words in sets:
        _add_scanned_page(pdf, words)
    return CorpusPdf(
        "scanned_multi",
        _save(pdf),
        3,
        ("", "", ""),
        scanned_pages=(0, 1, 2),
        ocr_words=dict(enumerate(sets)),
        tags=frozenset({"scanned"}),
    )


def scanned_rotated() -> CorpusPdf:
    """A scan whose page carries /Rotate 90 (the sideways-feed case). TODAY'S OCR READS IT AS GARBAGE
    (it rasterises the page as displayed and runs tesseract without orientation detection); the
    corpus records that as a known limit instead of hiding it. OCRmyPDF (U14) rotates and deskews."""
    pdf, _ = _new_pdf()
    _add_scanned_page(pdf, rotate=90)
    return CorpusPdf(
        "scanned_rotated", _save(pdf), 1, ("",), scanned_pages=(0,), rotations=(90,), tags=frozenset({"scanned", "rotated"})
    )


def blank() -> CorpusPdf:
    """A page with no content at all: extraction returns an empty page, not an error."""
    pdf, _ = _new_pdf()
    pdf.add_blank_page(page_size=(PAGE_W, PAGE_H))
    return CorpusPdf("blank", _save(pdf), 1, ("",), tags=frozenset({"blank"}))


def acroform() -> CorpusPdf:
    """Two text fields and a checkbox - a fillable form (the PyPDFForm path reads this)."""
    pikepdf = _pikepdf()
    pdf, font = _new_pdf()
    page = _add_text_page(pdf, font, [(72, 720, "Application form marker-form" + FILLER), (72, 690, "Full name"), (72, 650, "City")])
    fields = []
    annots = []
    for name, y, kind in (("full_name", 686, "Tx"), ("city", 646, "Tx"), ("agree", 606, "Btn")):
        widget = pdf.make_indirect(
            pikepdf.Dictionary(
                Type=pikepdf.Name.Annot,
                Subtype=pikepdf.Name.Widget,
                FT=pikepdf.Name(f"/{kind}"),
                T=pikepdf.String(name),
                Rect=[200, y, 400, y + 20],
                F=4,
                P=page.obj,
            )
        )
        fields.append(widget)
        annots.append(widget)
    page.Annots = pdf.make_indirect(pikepdf.Array(annots))
    pdf.Root.AcroForm = pikepdf.Dictionary(Fields=pikepdf.Array(fields), DA=pikepdf.String("/F1 0 Tf 0 g"))
    expected = (_collapse("Application form marker-form" + FILLER + " Full name City"),)
    return CorpusPdf(
        "acroform", _save(pdf), 1, expected, tags=frozenset({"forms", "digital"})
    )


def long_document(pages: int = 30) -> CorpusPdf:
    """Multi-page; ``pages=500`` is the scale case (a parameter, never a stored file)."""
    pdf, font = _new_pdf()
    expected = []
    for number in range(1, pages + 1):
        text = f"Chapter page marker-{number:04d} of the long document." + FILLER
        _add_text_page(pdf, font, [(72, 720, text)])
        expected.append(_collapse(text))
    return CorpusPdf(f"long_{pages}", _save(pdf), pages, tuple(expected), tags=frozenset({"long", "digital"}))


def build_corpus() -> dict[str, CorpusPdf]:
    """The standard corpus (about a dozen shapes counting variants); cheap enough for every run."""
    items = [
        digital(),
        scanned(),
        mixed(),
        rotated(),
        encrypted(),
        tables(),
        accented(),
        acroform(),
        scanned_multi(),
        scanned_rotated(),
        blank(),
        long_document(30),
    ]
    return {item.name: item for item in items}


def decrypted_bytes(item: CorpusPdf) -> bytes:
    """An encrypted corpus file with its password removed (what a caller does before extraction)."""
    pikepdf = _pikepdf()
    with pikepdf.open(io.BytesIO(item.data), password=item.password or "") as pdf:
        return _save(pdf)


def collapse(text: str) -> str:
    """Whitespace-collapsed text: the comparison form for native extraction."""
    return _collapse(text)


def check_extraction(extract, corpus: dict[str, CorpusPdf] | None = None, *, ocr: bool = True) -> list[str]:
    """Hold an extractor to the corpus. ``extract(path) -> list[PdfPageText]``. Returns mismatches.

    Native pages must equal the declared text (whitespace-collapsed) and stay on the native path;
    scanned pages must go to OCR and (when ``ocr``) yield their declared words. An empty list is a
    pass. A planted change to the extractor makes this non-empty - that is the forcing test.
    """
    import tempfile
    from pathlib import Path

    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, item in (corpus or build_corpus()).items():
            path = Path(tmp) / f"{name}.pdf"
            path.write_bytes(decrypted_bytes(item) if item.password else item.data)
            pages = extract(str(path))
            if len(pages) != item.page_count:
                problems.append(f"{name}: {len(pages)} pages, expected {item.page_count}")
                continue
            for index, page in enumerate(pages):
                where = f"{name} p{index + 1}"
                if index in item.scanned_pages:
                    if page.extraction_method != "ocr":
                        problems.append(f"{where}: scanned page not sent to OCR ({page.extraction_method})")
                    elif ocr and index in item.ocr_words:
                        text = page.text.lower()
                        missing = [w for w in item.ocr_words[index] if w.lower() not in text]
                        if missing:
                            problems.append(f"{where}: OCR lost {missing}")
                elif item.native_text[index]:
                    if collapse(page.text) != item.native_text[index]:
                        problems.append(f"{where}: text differs: {collapse(page.text)[:60]!r}")
                    if page.extraction_method != "native":
                        problems.append(f"{where}: native text went to {page.extraction_method}")
                elif page.text.strip():
                    problems.append(f"{where}: blank page produced text {page.text.strip()[:40]!r}")
                if item.rotations and page.rotation != item.rotations[index]:
                    problems.append(f"{where}: rotation {page.rotation}, expected {item.rotations[index]}")
    return problems
