"""Shared pikepdf helpers for the U11 write operations (protect, stamp, outline, properties).

PDF-PLAN decision 1: every NEW PDF write uses the permissive stack (pikepdf here), never PyMuPDF; the
guard ``scripts/check_no_new_pymupdf_imports.py`` fails a new importer. pikepdf is imported lazily so
``import matrx_files`` stays light; a host without it gets one clear error naming the package.
"""

from __future__ import annotations

import io
from typing import Any


def load_pikepdf() -> Any:
    try:
        import pikepdf

        return pikepdf
    except ImportError as exc:  # pragma: no cover - the platform image installs it
        raise ImportError(
            "This PDF operation needs the `pikepdf` package (the permissive PDF write stack). "
            "Install it with: pip install 'pikepdf>=10'",
            name="pikepdf",
        ) from exc


def open_pdf(pdf_bytes: bytes, password: str = "") -> Any:
    """Open PDF bytes. A wrong or missing password is a ValueError in plain words, never a stack."""
    pikepdf = load_pikepdf()
    try:
        return pikepdf.open(io.BytesIO(pdf_bytes), password=password or "")
    except pikepdf.PasswordError as exc:
        if password:
            raise ValueError("That password does not open this PDF.") from exc
        raise ValueError("This PDF is password protected. Give its password to continue.") from exc
    except pikepdf.PdfError as exc:
        raise ValueError(f"This file could not be read as a PDF: {exc}") from exc


def save_pdf(pdf: Any, **kwargs: Any) -> bytes:
    """Serialize deterministically (same input, same bytes) with object streams."""
    out = io.BytesIO()
    kwargs.setdefault("deterministic_id", True)
    pdf.save(out, **kwargs)
    return out.getvalue()


def inherited(page_obj: Any, key: str) -> Any:
    """A page attribute that is inheritable through /Parent (/Resources, /MediaBox, /CropBox, /Rotate)."""
    node = page_obj
    for _ in range(64):
        if key in node:
            return node[key]
        parent = node.get("/Parent")
        if parent is None:
            return None
        node = parent
    return None


def is_signed(pdf: Any) -> bool:
    """True when the file carries a digital signature (editing it invalidates the seal)."""
    try:
        acro = pdf.Root.get("/AcroForm")
        if acro is None:
            return False
        if int(acro.get("/SigFlags", 0)) & 1:
            return True
        for field in acro.get("/Fields", []):
            if field.get("/FT") == "/Sig" and field.get("/V") is not None:
                return True
    except Exception:  # an odd form tree must not break the edit
        return False
    return False
