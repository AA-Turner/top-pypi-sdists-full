"""Protect: password to open, owner password and permissions, and removal (PDF-PLAN U11).

AES-256 (security handler revision 6) through pikepdf's ``Encryption``. Two passwords:

- ``user_password``  — needed to OPEN the file. Empty means anyone can open it, but the owner
  restrictions below still apply in compliant readers.
- ``owner_password`` — lifts the restrictions. Defaults to the user password when not given.

Honest scope: permissions are enforced by the reader, not by cryptography; only the password to
open is a lock. The result says so in ``metadata["permissions_are_advisory"]``.
"""

from __future__ import annotations

import io
from typing import Any

from ..concurrency import run_in_cpu_executor
from ..models import PdfBinaryResult
from ._pike import is_signed, load_pikepdf, open_pdf, save_pdf

#: Permission name -> pikepdf.Permissions field. All default to allowed.
PERMISSION_FIELDS: dict[str, str] = {
    "print_lowres": "print_lowres",
    "print_highres": "print_highres",
    "modify": "modify_other",
    "extract": "extract",
    "annotate": "modify_annotation",
    "form": "modify_form",
    "assemble": "modify_assembly",
    "accessibility": "accessibility",
}


def protect_pdf_bytes(
    pdf_bytes: bytes,
    *,
    user_password: str = "",
    owner_password: str | None = None,
    allow: dict[str, bool] | None = None,
    source_password: str = "",
) -> PdfBinaryResult:
    """Encrypt with AES-256. ``allow`` maps a permission name to True/False; omitted names stay allowed."""
    pikepdf = load_pikepdf()
    allow = dict(allow or {})
    unknown = sorted(set(allow) - set(PERMISSION_FIELDS))
    if unknown:
        raise ValueError(f"Unknown permission: {', '.join(unknown)}. Use one of {', '.join(PERMISSION_FIELDS)}.")
    owner = owner_password if owner_password else user_password
    if not owner:
        raise ValueError("Give a password to open the file, an owner password, or both.")

    permissions = pikepdf.Permissions(
        **{PERMISSION_FIELDS[name]: bool(allow.get(name, True)) for name in PERMISSION_FIELDS}
    )
    with open_pdf(pdf_bytes, source_password) as pdf:
        signed = is_signed(pdf)
        page_count = len(pdf.pages)
        content = save_pdf(
            pdf,
            encryption=pikepdf.Encryption(owner=owner, user=user_password or "", R=6, allow=permissions),
            deterministic_id=False,  # qpdf cannot derive a stable id for an encrypted file
        )
    return PdfBinaryResult(
        content=content,
        page_count=page_count,
        operation="protect",
        metadata={
            "encryption": "AES-256",
            "needs_password_to_open": bool(user_password),
            "permissions": {name: bool(allow.get(name, True)) for name in PERMISSION_FIELDS},
            "permissions_are_advisory": True,
            "signed": signed,
        },
    )


def unprotect_pdf_bytes(pdf_bytes: bytes, *, password: str) -> PdfBinaryResult:
    """Remove the encryption. Needs the password (user or owner) that opens the file."""
    with open_pdf(pdf_bytes, password) as pdf:
        was_encrypted = bool(pdf.is_encrypted)
        page_count = len(pdf.pages)
        content = save_pdf(pdf, encryption=False)
    return PdfBinaryResult(
        content=content,
        page_count=page_count,
        operation="unprotect",
        metadata={"was_encrypted": was_encrypted},
    )


def encryption_summary(pdf_bytes: bytes, password: str = "") -> dict[str, Any]:
    """What a person needs to know before opening: encrypted or not, and whether this password opens it."""
    pikepdf = load_pikepdf()
    try:
        with pikepdf.open(io.BytesIO(pdf_bytes), password=password or "") as pdf:
            return {"encrypted": bool(pdf.is_encrypted), "opens": True}
    except pikepdf.PasswordError:
        return {"encrypted": True, "opens": False}


async def protect_pdf_bytes_async(pdf_bytes: bytes, **kwargs: Any) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: protect_pdf_bytes(pdf_bytes, **kwargs))


async def unprotect_pdf_bytes_async(pdf_bytes: bytes, *, password: str) -> PdfBinaryResult:
    return await run_in_cpu_executor(lambda: unprotect_pdf_bytes(pdf_bytes, password=password))


__all__ = [
    "PERMISSION_FIELDS",
    "protect_pdf_bytes",
    "protect_pdf_bytes_async",
    "unprotect_pdf_bytes",
    "unprotect_pdf_bytes_async",
    "encryption_summary",
]
