"""LibreOffice conversion — the ONE bridge for the two things pure-python can't do:

  1. Read legacy binary formats (.doc/.ppt/.xls) by converting them to OpenXML.
  2. Render any Office document to PDF (so the thumbnail engine can rasterize
     page 1, and callers can get a faithful print view).

LibreOffice (``soffice``) is a SYSTEM binary, an optional-at-runtime capability
like tesseract: present on the standalone files image, usually absent in a bare
in-process host. Every entry point degrades loudly — ``libreoffice_available()``
gates callers, and a conversion attempt without it raises ``LibreOfficeUnavailable``
rather than silently returning nothing.

Concurrency: each ``soffice`` invocation gets its own throwaway ``-env:UserInstallation``
profile dir, so parallel conversions don't collide on the shared default profile
(the classic LibreOffice-in-a-server failure).
"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import tempfile
import uuid
from functools import lru_cache
from pathlib import Path

from .models import OfficeKind

# Per-invocation wall clock. A hung soffice must not wedge a worker forever.
CONVERT_TIMEOUT_SECONDS = 120


class OfficeConversionError(Exception):
    """LibreOffice ran but the conversion failed or produced no output."""


class LibreOfficeUnavailable(OfficeConversionError):
    """The ``soffice`` binary isn't installed on this host."""


@lru_cache(maxsize=1)
def _soffice_path() -> str | None:
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    # Common absolute locations (slim images / macOS) when PATH is sparse.
    for candidate in (
        "/usr/bin/soffice",
        "/usr/lib/libreoffice/program/soffice",
        "/opt/libreoffice/program/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ):
        if os.path.exists(candidate):
            return candidate
    return None


def libreoffice_available() -> bool:
    """True when this host can do LibreOffice conversions."""
    return _soffice_path() is not None


_SUFFIX = {
    OfficeKind.docx: ".docx",
    OfficeKind.pptx: ".pptx",
    OfficeKind.xlsx: ".xlsx",
    OfficeKind.doc: ".doc",
    OfficeKind.ppt: ".ppt",
    OfficeKind.xls: ".xls",
}


def _run_soffice(raw: bytes, *, input_suffix: str, convert_to: str) -> bytes:
    soffice = _soffice_path()
    if soffice is None:
        raise LibreOfficeUnavailable(
            "LibreOffice (soffice) is not installed on this host — legacy-format "
            "reading and Office→PDF rendering require it (present on the files image)."
        )

    with tempfile.TemporaryDirectory(prefix="office_convert_") as work:
        work_path = Path(work)
        profile = work_path / f"profile_{uuid.uuid4().hex}"
        in_path = work_path / f"in{input_suffix}"
        in_path.write_bytes(raw)

        # ``convert_to`` may carry an export filter, e.g. "pdf:impress_pdf_Export".
        target_ext = convert_to.split(":", 1)[0]
        cmd = [
            soffice,
            "--headless",
            "--norestore",
            "--nolockcheck",
            f"-env:UserInstallation=file://{profile}",
            "--convert-to",
            convert_to,
            "--outdir",
            str(work_path),
            str(in_path),
        ]
        # Run soffice in its OWN process group so a timeout can kill the whole
        # tree — LibreOffice routinely spawns a detached ``soffice.bin`` grandchild
        # that outlives the parent and would otherwise leak CPU/RAM.
        new_session = os.name == "posix"
        proc = subprocess.Popen(  # noqa: S603 — fixed argv, no shell
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=new_session,
        )
        try:
            _out, err = proc.communicate(timeout=CONVERT_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as exc:
            if new_session:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    proc.kill()
            else:
                proc.kill()
            proc.communicate()
            raise OfficeConversionError(
                f"soffice timed out after {CONVERT_TIMEOUT_SECONDS}s converting to {target_ext}"
            ) from exc

        out_path = work_path / f"in.{target_ext}"
        if not out_path.exists():
            # LibreOffice reports success on stdout even when it wrote nothing;
            # the missing output file is the real signal. Surface stderr.
            stderr = (err or b"").decode("utf-8", "replace")[:500]
            raise OfficeConversionError(
                f"soffice produced no {target_ext} output (rc={proc.returncode}): {stderr}"
            )
        return out_path.read_bytes()


def convert_to_pdf(raw: bytes, *, source_kind: OfficeKind | None = None, input_suffix: str | None = None) -> bytes:
    """Render any Office document to PDF bytes (for thumbnails / print view)."""
    suffix = input_suffix or (_SUFFIX.get(source_kind) if source_kind else None) or ".docx"
    # Kind-specific export filters give better fidelity than the bare "pdf".
    export_filter = {
        OfficeKind.pptx: "pdf:impress_pdf_Export",
        OfficeKind.ppt: "pdf:impress_pdf_Export",
        OfficeKind.xlsx: "pdf:calc_pdf_Export",
        OfficeKind.xls: "pdf:calc_pdf_Export",
    }.get(source_kind or OfficeKind.docx, "pdf")
    return _run_soffice(raw, input_suffix=suffix, convert_to=export_filter)


def convert_legacy_to_openxml(raw: bytes, legacy_kind: OfficeKind) -> tuple[bytes, OfficeKind]:
    """Convert a legacy binary (.doc/.ppt/.xls) to its OpenXML equivalent and
    return (bytes, new_kind) so the pure-python codec can read it."""
    mapping = {
        OfficeKind.doc: (".doc", "docx", OfficeKind.docx),
        OfficeKind.ppt: (".ppt", "pptx", OfficeKind.pptx),
        OfficeKind.xls: (".xls", "xlsx", OfficeKind.xlsx),
    }
    if legacy_kind not in mapping:
        raise OfficeConversionError(f"{legacy_kind.value!r} is not a legacy binary format")
    in_suffix, target, new_kind = mapping[legacy_kind]
    out = _run_soffice(raw, input_suffix=in_suffix, convert_to=target)
    return out, new_kind


# Open formats a person downloads from the three editors: the editor's own OpenXML export is the
# input, LibreOffice writes the target. key = target extension, value = (source suffixes allowed, mime).
EXPORT_TARGETS: dict[str, tuple[frozenset[str], str]] = {
    "odt": (frozenset({".docx"}), "application/vnd.oasis.opendocument.text"),
    "rtf": (frozenset({".docx"}), "application/rtf"),
    "ods": (frozenset({".xlsx"}), "application/vnd.oasis.opendocument.spreadsheet"),
    "odp": (frozenset({".pptx"}), "application/vnd.oasis.opendocument.presentation"),
}


def convert_openxml_to_open_format(raw: bytes, *, input_suffix: str, target: str) -> tuple[bytes, str]:
    """OpenXML bytes (.docx/.xlsx/.pptx) → an open format (.odt/.rtf/.ods/.odp). Returns (bytes, mime).

    Raises ``OfficeConversionError`` for a target/source pair we do not offer — loudly, never a
    silent pass-through of the input."""
    key = target.strip().lower().lstrip(".")
    suffix = input_suffix.strip().lower()
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    if key not in EXPORT_TARGETS:
        raise OfficeConversionError(f"unsupported export target {target!r}; offered: {sorted(EXPORT_TARGETS)}")
    sources, mime = EXPORT_TARGETS[key]
    if suffix not in sources:
        raise OfficeConversionError(f"{key!r} is exported from {sorted(sources)}, not {suffix!r}")
    return _run_soffice(raw, input_suffix=suffix, convert_to=key), mime


__all__ = [
    "EXPORT_TARGETS",
    "convert_openxml_to_open_format",
    "libreoffice_available",
    "convert_to_pdf",
    "convert_legacy_to_openxml",
    "OfficeConversionError",
    "LibreOfficeUnavailable",
    "CONVERT_TIMEOUT_SECONDS",
]
