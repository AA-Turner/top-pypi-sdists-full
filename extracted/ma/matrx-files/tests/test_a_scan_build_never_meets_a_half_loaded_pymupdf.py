"""The scan build's first PyMuPDF use never meets a half-loaded PyMuPDF (2026-11-19).

Live, every scan save that raced another thread's first ``require("pymupdf")`` (page photos to
PDF) failed with ``module 'pymupdf' has no attribute 'open'`` and wrote no file: the declared-module
seam loaded PyMuPDF without the import lock, so the scan build's plain ``import pymupdf`` took the
module as finished while its body (~0.5 s in PyMuPDF 2.0) was still running.

This runs the exact pair on the installed (locked) PyMuPDF in a FRESH interpreter, because the race
only exists on a process's first load: thread A loads PyMuPDF through ``require``; thread B runs the
real ``build_scan_pdf`` while A's load is mid-body. Red before the seam fix (B raised the live error),
green after.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap

import pytest

pytest.importorskip("pymupdf")

_SCRIPT = textwrap.dedent(
    """
    import io, json, sys, threading, time
    from PIL import Image
    from matrx_files._extras import require
    from matrx_files.specific_handlers.pdf.images_to_pdf import ScanPdfInputItem, build_scan_pdf

    assert "pymupdf" not in sys.modules, "the race needs a process that has not loaded PyMuPDF yet"
    buf = io.BytesIO()
    Image.new("RGB", (640, 480), "white").save(buf, "JPEG")
    photo = buf.getvalue()
    results = {}
    started = threading.Event()

    def page_photos_load():
        started.set()
        try:
            require("pymupdf", "pdf", "Page photos to PDF")
            results["require"] = "ok"
        except BaseException as exc:
            results["require"] = f"{type(exc).__name__}: {exc}"

    def scan_build():
        started.wait()
        time.sleep(DELAY)  # the require() load is mid-body now
        try:
            pdf, pages = build_scan_pdf([ScanPdfInputItem(raw_bytes=photo, kind="image")])
            results["scan"] = f"ok {pages} page(s), {len(pdf)} bytes" if pdf[:5] == b"%PDF-" else "not a PDF"
        except BaseException as exc:
            results["scan"] = f"{type(exc).__name__}: {exc}"

    threads = [threading.Thread(target=page_photos_load), threading.Thread(target=scan_build)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    print(json.dumps(results))
    """
)


@pytest.mark.parametrize("delay", [0.0, 0.05, 0.2])
def test_a_scan_build_racing_a_first_pymupdf_load_still_builds(delay: float) -> None:
    proc = subprocess.run(
        [sys.executable, "-c", f"DELAY = {delay}\n" + _SCRIPT],
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    results = json.loads(proc.stdout.strip().splitlines()[-1])
    assert results["require"] == "ok", results
    assert results["scan"].startswith("ok 1 page(s)"), results
