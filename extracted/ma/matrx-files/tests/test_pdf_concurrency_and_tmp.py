"""Tests for the new Phase 0 PDF utilities: concurrency executors and temp management.

These cover code paths the original monolith didn't have. Together with the
existing test_pdf_handler_operations.py they pin the Phase 0 refactor's behavior.
"""

from __future__ import annotations

import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from matrx_utils.source_guard import stable_source

from matrx_files.specific_handlers.pdf import (
    cleanup_tmp_older_than,
    pdf_temp_dir,
    pdf_temp_file,
    write_pdf_bytes_to_temp,
)
from matrx_files.specific_handlers.pdf.concurrency import (
    configure_worker_counts,
    get_cpu_executor,
    get_ocr_executor,
    run_in_cpu_executor,
    run_in_ocr_executor,
    shutdown_executors,
)


# ---------------------------------------------------------------------------
# Concurrency executor tests
# ---------------------------------------------------------------------------


def test_cpu_executor_singleton() -> None:
    a = get_cpu_executor()
    b = get_cpu_executor()
    assert a is b
    assert isinstance(a, ThreadPoolExecutor)


def test_ocr_executor_singleton_and_distinct() -> None:
    cpu = get_cpu_executor()
    ocr = get_ocr_executor()
    ocr2 = get_ocr_executor()
    assert ocr is ocr2
    assert ocr is not cpu


def test_run_in_cpu_executor_returns_value() -> None:
    async def go() -> int:
        return await run_in_cpu_executor(lambda: 7)

    assert asyncio.run(go()) == 7


def test_run_in_cpu_executor_propagates_exception() -> None:
    async def go() -> None:
        await run_in_cpu_executor(lambda: 1 / 0)

    with pytest.raises(ZeroDivisionError):
        asyncio.run(go())


def test_run_in_ocr_executor_accepts_args_kwargs() -> None:
    def add(a: int, b: int = 0) -> int:
        return a + b

    async def go() -> int:
        return await run_in_ocr_executor(add, 3, b=4)

    assert asyncio.run(go()) == 7


def test_cpu_worker_count_comes_from_the_host(monkeypatch: pytest.MonkeyPatch) -> None:
    # Tear down the existing executor so the next access reads the host count.
    shutdown_executors()
    configure_worker_counts(cpu=lambda: 2)
    try:
        executor = get_cpu_executor()
        assert executor._max_workers == 2
    finally:
        shutdown_executors()
        configure_worker_counts(cpu=lambda: 0)


def test_ocr_worker_count_comes_from_the_host(monkeypatch: pytest.MonkeyPatch) -> None:
    shutdown_executors()
    configure_worker_counts(ocr=lambda: 1)
    try:
        executor = get_ocr_executor()
        assert executor._max_workers == 1
    finally:
        shutdown_executors()
        configure_worker_counts(ocr=lambda: 0)


def test_retired_env_vars_do_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forcing function (env-vars-are-values-not-toggles §4): the retired
    MATRX_PDF_*_WORKERS names must be inert, and the module must not read
    the environment for sizing at all."""
    from matrx_files.specific_handlers.pdf import concurrency

    shutdown_executors()
    configure_worker_counts(cpu=lambda: 3, ocr=lambda: 0)
    monkeypatch.setenv("MATRX_PDF_CPU_WORKERS", "1")
    monkeypatch.setenv("MATRX_PDF_OCR_WORKERS", "1")
    try:
        assert get_cpu_executor()._max_workers == 3
        assert get_ocr_executor()._max_workers == max(1, min(4, os.cpu_count() or 2))
    finally:
        shutdown_executors()
        configure_worker_counts(cpu=lambda: 0, ocr=lambda: 0)
    source = stable_source(concurrency)
    assert "os.environ" not in source and "os.getenv" not in source


def test_unreadable_host_count_announces_and_uses_package_posture(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def boom() -> int:
        raise RuntimeError("settings not loaded")

    shutdown_executors()
    configure_worker_counts(cpu=boom)
    try:
        assert get_cpu_executor()._max_workers == max(1, os.cpu_count() or 2)
        assert "could not be read" in capsys.readouterr().err
    finally:
        shutdown_executors()
        configure_worker_counts(cpu=lambda: 0)


def test_default_tesseract_provider_runs_ocr_off_the_event_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: the in-process Tesseract provider once ran ocr_image_bytes
    (~1.4s/page, CPU-bound) synchronously ON the event loop, freezing the whole
    server per page. It must offload via the bounded OCR executor — not the
    loop thread, and not an unbounded pool like asyncio.to_thread."""
    import threading

    import matrx_files.specific_handlers.pdf.extract.ocr as ocr_mod
    from matrx_files.analysis.ocr_router import DEFAULT_OCR_PROVIDER

    seen: dict[str, str] = {}

    def fake_ocr(image_bytes: bytes, config: str | None = None) -> str:
        seen["thread"] = threading.current_thread().name
        return "ocr text"

    monkeypatch.setattr(ocr_mod, "ocr_image_bytes", fake_ocr)

    async def go() -> str:
        seen["loop_thread"] = threading.current_thread().name
        return await DEFAULT_OCR_PROVIDER.ocr_page_image(b"png-bytes")

    assert asyncio.run(go()) == "ocr text"
    assert seen["thread"] != seen["loop_thread"]
    assert seen["thread"].startswith("matrx-pdf-ocr")


# ---------------------------------------------------------------------------
# Temp file management tests
# ---------------------------------------------------------------------------


def test_pdf_temp_dir_is_namespaced_and_persists() -> None:
    base = pdf_temp_dir()
    assert base.exists()
    assert base.is_dir()
    assert "matrx_pdf" in str(base)


def test_write_pdf_bytes_to_temp_writes_file() -> None:
    path = write_pdf_bytes_to_temp(b"%PDF-1.4 fake")
    try:
        assert path.exists()
        assert path.read_bytes() == b"%PDF-1.4 fake"
        assert path.parent == pdf_temp_dir()
        assert path.suffix == ".pdf"
    finally:
        path.unlink(missing_ok=True)


def test_pdf_temp_file_context_unlinks_on_exit() -> None:
    captured: list = []
    with pdf_temp_file(b"hello") as path:
        captured.append(path)
        assert path.exists()
    assert not captured[0].exists()


def test_pdf_temp_file_unlinks_even_on_exception() -> None:
    captured: list = []
    try:
        with pdf_temp_file(b"hello") as path:
            captured.append(path)
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert not captured[0].exists()


def test_cleanup_tmp_older_than_age_threshold() -> None:
    new_path = write_pdf_bytes_to_temp(b"recent")
    old_path = write_pdf_bytes_to_temp(b"stale")
    try:
        # Backdate the "old" file to ~2 hours ago.
        old_time = time.time() - 7200
        os.utime(old_path, (old_time, old_time))

        removed = cleanup_tmp_older_than(seconds=3600)
        assert removed >= 1
        assert not old_path.exists()
        assert new_path.exists()
    finally:
        new_path.unlink(missing_ok=True)
        old_path.unlink(missing_ok=True)


def test_cleanup_tmp_older_than_returns_zero_when_dir_clean() -> None:
    # Sweep with a huge age threshold so nothing qualifies.
    removed = cleanup_tmp_older_than(seconds=10_000_000)
    assert removed == 0
