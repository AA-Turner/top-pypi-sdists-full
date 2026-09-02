from __future__ import annotations

import asyncio
import threading

import pytest

from matrx_scraper import extractors


@pytest.mark.asyncio
async def test_pdf_extraction_async_keeps_event_loop_responsive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered = threading.Event()
    release = threading.Event()
    loop_thread_id = threading.get_ident()
    worker_thread_ids: list[int] = []

    def blocking_extract(_pdf_bytes: bytes) -> str:
        worker_thread_ids.append(threading.get_ident())
        entered.set()
        release.wait(timeout=2)
        return "extracted"

    monkeypatch.setattr(extractors, "extract_text_from_pdf_bytes", blocking_extract)

    task = asyncio.create_task(extractors.extract_text_from_pdf_bytes_async(b"%PDF"))
    assert await asyncio.to_thread(entered.wait, 1)
    await asyncio.sleep(0)
    assert not task.done()
    assert worker_thread_ids == [worker_thread_ids[0]]
    assert worker_thread_ids[0] != loop_thread_id

    release.set()
    assert await task == "extracted"
