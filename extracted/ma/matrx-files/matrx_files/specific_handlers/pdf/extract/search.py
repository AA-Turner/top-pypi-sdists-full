"""Text search across a PDF — returns hits with bbox + snippet.

Driven by the studio's Cmd+F UX. Uses PyMuPDF's per-page `search_for` (exact
literals — fastest) by default, with a regex fallback that scans the text
layer + maps matches back to word-level bboxes.

Returns a list of `SearchHit` ordered by (page_number, y0, x0). Doesn't open
a document twice — callers can pass an already-open `doc` via the `doc=`
keyword, or pass bytes for a one-shot.
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import AsyncIterator, Callable
from typing import Any

from pydantic import BaseModel, Field

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf


class SearchBbox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class SearchStart(BaseModel):
    """First item yielded by ``search_text_stream`` — the page count, the
    moment the document opens."""

    total_pages: int = Field(ge=0)


class SearchPageHits(BaseModel):
    """One page finished scanning — the hits found on it (possibly none)."""

    page_number: int = Field(ge=1)
    total_pages: int = Field(ge=0)
    hits: list[SearchHit] = Field(default_factory=list)


class SearchHit(BaseModel):
    page_number: int = Field(ge=1)
    bbox: SearchBbox
    snippet: str
    """A few words before + the match + a few words after. For UX display."""
    matched_text: str
    char_start: int | None = None
    """Offset into the page's words joined by single spaces (the text the
    snippet is cut from), for literal and regex hits alike."""
    char_end: int | None = None


def _snippet_around(text: str, start: int, end: int, window: int = 60) -> str:
    """The match with up to ``window`` characters each side, cut at whole words."""
    s = max(0, start - window)
    e = min(len(text), end + window)
    if s > 0:
        cut = text.find(" ", s, start)
        s = cut + 1 if cut != -1 else s
    if e < len(text):
        cut = text.rfind(" ", end, e)
        e = cut if cut != -1 else e
    return text[s:e].replace("\n", " ").strip()


def search_text(
    pdf_bytes: bytes,
    *,
    query: str,
    regex: bool = False,
    case_sensitive: bool = False,
    max_hits: int = 500,
    doc: Any = None,
    on_open: Callable[[int], None] | None = None,
    on_page: Callable[[SearchPageHits], None] | None = None,
) -> list[SearchHit]:
    """Search for `query` across every page. Returns up to `max_hits` results.

    ``on_open`` / ``on_page`` are optional sync progress hooks called from the
    scan loop (``on_open`` with the page count the moment the document opens,
    ``on_page`` with each page's hits as the page finishes — including pages
    with zero hits). They exist so callers can stream progress in real time —
    see ``search_text_stream``.
    """
    if not query:
        return []

    pymupdf = load_pymupdf()
    own_doc = doc is None
    if doc is None:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    try:
        if on_open is not None:
            on_open(doc.page_count)
        # ONE matcher for both modes, over ONE text: the page's words joined by single spaces, which is
        # also where every hit's char offsets and snippet come from. A literal query is the escaped text
        # with any run of whitespace matching any run (a phrase may cross a line break). The old literal
        # path took boxes from PyMuPDF's search_for but cut the snippet from a DIFFERENT text with a
        # wrong end offset (0), so every hit on a page showed the same garbled slice ("mple."), and
        # search_for ignored case_sensitive. Guard: tests/test_pdf_search_hits.py.
        flags = 0 if case_sensitive else re.IGNORECASE
        if regex:
            try:
                compiled = re.compile(query, flags)
            except re.error as exc:
                raise ValueError(f"invalid regex: {exc}") from exc
        else:
            compiled = re.compile(r"\s+".join(re.escape(part) for part in query.split()) or re.escape(query), flags)

        out: list[SearchHit] = []

        for page_index in range(doc.page_count):
            if len(out) >= max_hits:
                break
            page = doc[page_index]
            page_number = page_index + 1
            page_start = len(out)

            def _emit_page() -> None:
                if on_page is not None:
                    on_page(SearchPageHits(
                        page_number=page_number,
                        total_pages=doc.page_count,
                        hits=list(out[page_start:]),
                    ))

            # A literal hit inside a word (e.g. "fox" in "foxes") gets PyMuPDF's exact glyph box when one
            # lies inside the matched words' box; otherwise the words' box stands.
            exact_rects: list[Any] = []
            if not regex:
                try:
                    exact_rects = list(page.search_for(query))
                except Exception:
                    exact_rects = []

            # Match against the linear page text + map back via words.
            page_text = page.get_text("text") or ""
            if not page_text:
                _emit_page()
                continue

            try:
                words = page.get_text("words", sort=True) or []
            except Exception:
                words = []

            # Build (start, end, bbox) spans for words via the same reconstruction
            # used in pattern_candidates.
            spans: list[tuple[int, int, tuple[float, float, float, float]]] = []
            parts: list[str] = []
            cursor = 0
            for w in words:
                x0, y0, x1, y1, word, *_ = w
                if not word:
                    continue
                parts.append(word)
                parts.append(" ")
                spans.append((cursor, cursor + len(word), (
                    float(x0), float(y0), float(x1), float(y1),
                )))
                cursor += len(word) + 1
            linear = "".join(parts) or page_text

            for m in compiled.finditer(linear):
                if len(out) >= max_hits:
                    break
                ms, me = m.start(), m.end()
                hit_boxes = [b for (s, e, b) in spans if not (e <= ms or s >= me)]
                if not hit_boxes:
                    # Fall back to page-level bbox so the hit still shows on the page.
                    rect = page.rect
                    bbox = SearchBbox(x0=0.0, y0=0.0, x1=float(rect.width), y1=20.0)
                else:
                    bbox = SearchBbox(
                        x0=min(b[0] for b in hit_boxes),
                        y0=min(b[1] for b in hit_boxes),
                        x1=max(b[2] for b in hit_boxes),
                        y1=max(b[3] for b in hit_boxes),
                    )
                    for i, r in enumerate(exact_rects):
                        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
                        if bbox.x0 - 1 <= cx <= bbox.x1 + 1 and bbox.y0 - 1 <= cy <= bbox.y1 + 1:
                            bbox = SearchBbox(x0=float(r.x0), y0=float(r.y0), x1=float(r.x1), y1=float(r.y1))
                            del exact_rects[i]
                            break
                out.append(SearchHit(
                    page_number=page_number,
                    bbox=bbox,
                    matched_text=m.group(0),
                    snippet=_snippet_around(linear, ms, me),
                    char_start=ms,
                    char_end=me,
                ))
            _emit_page()

        # Stable ordering.
        out.sort(key=lambda h: (h.page_number, h.bbox.y0, h.bbox.x0))
        return out[:max_hits]
    finally:
        if own_doc:
            doc.close()


async def search_text_async(
    pdf_bytes: bytes,
    *,
    query: str,
    regex: bool = False,
    case_sensitive: bool = False,
    max_hits: int = 500,
) -> list[SearchHit]:
    return await run_in_cpu_executor(
        lambda: search_text(
            pdf_bytes,
            query=query,
            regex=regex,
            case_sensitive=case_sensitive,
            max_hits=max_hits,
        )
    )


async def search_text_stream(
    pdf_bytes: bytes,
    *,
    query: str,
    regex: bool = False,
    case_sensitive: bool = False,
    max_hits: int = 500,
) -> AsyncIterator[SearchStart | SearchPageHits]:
    """Stream the search as it happens: yields one ``SearchStart`` (page
    count) the moment the document opens, then a ``SearchPageHits`` per page
    as it finishes scanning (zero-hit pages included).

    Same pattern as ``extract_text_pages_stream``: the whole sync scan runs
    on ONE CPU-executor worker (PyMuPDF thread-safety — the Document never
    leaves its thread); page results cross back to the event loop via a
    queue. A scan error is re-raised here after every already-scanned page
    has been yielded. The scan stops early once ``max_hits`` is reached.
    """
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[SearchStart | SearchPageHits | None] = asyncio.Queue()

    def _on_open(total_pages: int) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, SearchStart(total_pages=total_pages))

    def _on_page(page_hits: SearchPageHits) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, page_hits)

    async def _run() -> None:
        try:
            await run_in_cpu_executor(
                lambda: search_text(
                    pdf_bytes,
                    query=query,
                    regex=regex,
                    case_sensitive=case_sensitive,
                    max_hits=max_hits,
                    on_open=_on_open,
                    on_page=_on_page,
                )
            )
        finally:
            queue.put_nowait(None)  # sentinel — runs on the event loop already

    worker = asyncio.ensure_future(_run())
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        # Propagate a scan failure (worker is guaranteed settled once the
        # sentinel arrived; on generator abandonment this awaits the tail).
        await worker


__all__ = [
    "SearchBbox",
    "SearchHit",
    "SearchPageHits",
    "SearchStart",
    "search_text",
    "search_text_async",
    "search_text_stream",
]
