"""The PDF stream bridge yields every item before it ends, and the text stream
refuses to end with missing pages.

The break this guards (2026-11-16): the end-of-stream marker was posted from
the event loop when the executor future resolved, while the pages were posted
from the worker thread through ``call_soon_threadsafe``. Those are two
channels; the completion could win, so the consumer read the end marker first
and the stream ended with ZERO pages and no error — a saved PDF finished
"done" with no text (about 1 run in 1,500 in the wild).

The seam: the real ``extract_text_pages_stream`` over a real PDF, with only
the executor replaced by one that runs the work on a REAL thread and returns
the moment that thread finishes, without letting the event loop run the
thread's posted callbacks first. That is exactly the losing interleaving,
made certain instead of 1-in-1,500.
"""

from __future__ import annotations

import os
import tempfile
import threading
from pathlib import Path
from typing import Any

import pytest

pymupdf = pytest.importorskip("pymupdf")

from matrx_files.specific_handlers.pdf.extract import search as search_mod  # noqa: E402
from matrx_files.specific_handlers.pdf.extract import text as text_mod  # noqa: E402
from matrx_files.specific_handlers.pdf.models import PdfExtractStart, PdfPageText  # noqa: E402
from matrx_files.specific_handlers.pdf.stream_bridge import iter_sync_stream  # noqa: E402


async def _completion_wins_executor(fn: Any, *args: Any) -> Any:
    """Run ``fn`` on a real worker thread and return as soon as it finishes,
    WITHOUT yielding to the event loop — so the executor's completion is seen
    before any callback the thread posted with ``call_soon_threadsafe``."""
    box: dict[str, Any] = {}

    def _target() -> None:
        try:
            box["value"] = fn(*args)
        except BaseException as exc:  # noqa: BLE001 — re-raised on the loop
            box["error"] = exc

    t = threading.Thread(target=_target)
    t.start()
    t.join()
    if "error" in box:
        raise box["error"]
    return box["value"]


def _pdf(lines: list[str]) -> str:
    doc = pymupdf.open()
    for line in lines:
        page = doc.new_page()
        page.insert_text((72, 72), line)
    path = os.path.join(tempfile.mkdtemp(), "intake.pdf")
    doc.save(path)
    return path


@pytest.mark.parametrize(
    "lines",
    [
        ["Harbor Dental new patient intake", "Insurance card front and back"],
        ["Pickup route Tuesday", "Bin count 42 commercial", "Driver signature on file"],
    ],
)
async def test_every_page_is_yielded_when_the_executor_completion_wins_the_race(
    monkeypatch: pytest.MonkeyPatch, lines: list[str]
) -> None:
    monkeypatch.setattr(text_mod, "run_in_cpu_executor", _completion_wins_executor)
    path = _pdf(lines)

    got = [item async for item in text_mod.extract_text_pages_stream(path)]

    assert isinstance(got[0], PdfExtractStart)
    assert got[0].total_pages == len(lines)
    pages = [g for g in got[1:] if isinstance(g, PdfPageText)]
    assert [p.page_number for p in pages] == list(range(1, len(lines) + 1))
    assert [p.text.strip() for p in pages] == lines


async def test_search_stream_yields_its_pages_when_the_executor_completion_wins_the_race(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(search_mod, "run_in_cpu_executor", _completion_wins_executor)
    path = _pdf(["Invoice 5 total due", "Invoice 6 paid in full", "Statement of account"])
    data = Path(path).read_bytes()  # noqa: ASYNC240 — a tiny local fixture file

    got = [item async for item in search_mod.search_text_stream(data, query="invoice")]

    assert got[0].total_pages == 3
    hits = [(p.page_number, len(p.hits)) for p in got[1:]]
    assert hits == [(1, 1), (2, 1), (3, 0)]


async def test_text_stream_raises_when_a_page_never_arrives(monkeypatch: pytest.MonkeyPatch) -> None:
    real = text_mod.extract_text_pages

    def _drops_page_two(*args: Any, **kwargs: Any) -> list[PdfPageText]:
        args = list(args)
        on_page = args[6]
        args[6] = lambda page: None if page.page_number == 2 else on_page(page)
        return real(*args, **kwargs)

    monkeypatch.setattr(text_mod, "extract_text_pages", _drops_page_two)
    path = _pdf(["Lease page one", "Lease page two", "Lease page three"])

    seen: list[int] = []
    with pytest.raises(text_mod.PdfPagesMissingError, match=r"returned 2 of 3 pages \(missing pages \[2\]\)"):
        async for item in text_mod.extract_text_pages_stream(path):
            if isinstance(item, PdfPageText):
                seen.append(item.page_number)
    assert seen == [1, 3]


async def test_bridge_ends_with_the_error_when_the_work_never_starts() -> None:
    async def _refusing_executor(fn: Any, *args: Any) -> Any:
        raise RuntimeError("cannot schedule new futures after shutdown")

    with pytest.raises(RuntimeError, match="after shutdown"):
        async for _ in iter_sync_stream(_refusing_executor, lambda emit: emit(1)):
            pass


async def test_bridge_yields_items_then_raises_the_work_failure() -> None:
    def _work(emit: Any) -> None:
        emit("page 1 read")
        emit("page 2 read")
        raise ValueError("page 3 is damaged")

    got: list[str] = []
    with pytest.raises(ValueError, match="page 3 is damaged"):
        async for item in iter_sync_stream(_completion_wins_executor, _work):
            got.append(item)
    assert got == ["page 1 read", "page 2 read"]
