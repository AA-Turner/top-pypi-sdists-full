"""A valid hand-made PDF (unembedded standard-14 font, ``Td`` then ``TL``) must still show its text after our ops.

Live walk 3: a generated PDF went blank after crop plus a saved rotation. The fonts were never dropped: MuPDF's
``clean=True`` rewrote ``72 760 Td 24 TL`` into ``72 760 TD`` so every ``T*`` line fell 760 pt off the page. The
page operations and compress no longer ask for that rewrite. Proven by rendering and counting dark pixels.
"""

from __future__ import annotations

import io

import pytest

pikepdf = pytest.importorskip("pikepdf")
pdfium = pytest.importorskip("pypdfium2")

from matrx_files.specific_handlers.pdf.ops.compress import compress_pdf_bytes  # noqa: E402
from matrx_files.specific_handlers.pdf.ops.pages import (  # noqa: E402
    crop_pages_in_bytes,
    delete_pages_from_bytes,
    rotate_pages_in_bytes,
)


def _hand_made(pages: int = 3) -> bytes:
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            f"<< /Type /Pages /Kids [{' '.join(f'{4 + 2 * i} 0 R' for i in range(pages))}] /Count {pages} >>",
            "<< /Type /Font /Subtype /Font /BaseFont /Helvetica >>"]  # standard-14, no descriptor, not embedded
    for i in range(pages):
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>")
        s = f"BT /F1 18 Tf 72 760 Td 24 TL\n(Page {i + 1} heading) '\n(Zebra marker alpha) '\nET"
        objs.append(f"<< /Length {len(s)} >>\nstream\n{s}\nendstream")
    out = b"%PDF-1.4\n"
    offs = []
    for i, o in enumerate(objs):
        offs.append(len(out))
        out += f"{i + 1} 0 obj\n{o}\nendobj\n".encode()
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    return out + f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF".encode()


def _ink(pdf: bytes) -> int:
    img = pdfium.PdfDocument(pdf)[0].render(scale=1).to_pil().convert("L")
    return sum(1 for p in img.getdata() if p < 128)


def test_the_source_itself_has_text_to_lose() -> None:
    assert _ink(_hand_made()) > 500


@pytest.mark.parametrize("op", ["crop", "rotate", "crop_then_rotate", "delete", "compress"])
def test_text_survives_the_op(op: str) -> None:
    src = _hand_made()
    if op == "crop":
        out = crop_pages_in_bytes(src, {"x0": 20, "y0": 20, "x1": 500, "y1": 800}).content
    elif op == "rotate":
        out = rotate_pages_in_bytes(src, 90).content
    elif op == "crop_then_rotate":
        out = rotate_pages_in_bytes(crop_pages_in_bytes(src, {"x0": 20, "y0": 20, "x1": 500, "y1": 800}).content, 90).content
    elif op == "delete":
        out = delete_pages_from_bytes(src, pages=[3]).content
    else:
        out = compress_pdf_bytes(src, level=2)
    assert _ink(out) > 500, f"{op} left the page blank"
    with pikepdf.open(io.BytesIO(out)) as pdf:  # the font resource is kept, still unembedded
        fonts = pdf.pages[0].obj.Resources.Font
        assert str(next(iter(fonts.values())).BaseFont) == "/Helvetica"


def test_a_password_protected_pdf_is_refused_in_a_sentence_not_in_mupdf_words() -> None:
    """Live walk 3: tools on a protected file must explain why they cannot run (and the viewer asks for the password)."""
    protected = io.BytesIO()
    plain = pikepdf.new()
    plain.add_blank_page()
    plain.save(protected, encryption=pikepdf.Encryption(user="s3cret", owner="own", R=6))
    for run in (lambda: rotate_pages_in_bytes(protected.getvalue(), 90), lambda: crop_pages_in_bytes(protected.getvalue(), {"x0": 0, "y0": 0, "x1": 100, "y1": 100}), lambda: delete_pages_from_bytes(protected.getvalue(), pages=[1])):
        with pytest.raises(ValueError, match="password protected"):
            run()
