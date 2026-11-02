"""Highlights codec — the passages a reader already chose, out of the exports
every reading app gives its own user.

    from matrx_files.specific_handlers.highlights import extract_highlights

Handles, from bytes:

* **Kindle ``My Clippings.txt``** — the plain-text file every Kindle writes to
  its own ``documents/`` folder. Records separated by ``==========``, each with
  a title/author line, a location/page/date line, and the passage.
* **Kindle Notebook export** — the HTML file ``read.amazon.com/notebook``
  downloads ("Export notebook"), whose highlights carry section headings and
  page/location strings.
* **Readwise CSV export** — ``Highlight, Book Title, Book Author, …,
  Location``, the format Readwise gives for every book a person has read.

Why this exists (2026-09-17). The complete text of a copy-protected book is
not ours to take, and the platform will never strip protection to get it. But
the passages a reader *chose* are theirs, already exported, already DRM-free,
and they are the highest-signal part of the book — the expert already did the
distillation by hand. This codec is the lawful route the DRM refusal points at,
so that sentence is a real door rather than an apology.

Each highlight becomes its own portion carrying its book, its author, and its
location anchor, so a rule distilled from it cites *"Who, location 1,482"* —
the same provenance promise the ebook codec makes with chapter + position.

Pure python, stdlib only. No host imports, no ORM, no network.
"""

from __future__ import annotations

import csv
import io
import re
from collections.abc import Iterable, Iterator
from enum import Enum

from pydantic import BaseModel, Field

from .ebook import html_to_blocks
from .plaintext import decode_text

CLIPPINGS_SEPARATOR = "=========="

#: KNOB MIRROR of platform.feature_knob "media.file_service" "highlights_max_items"
MAX_HIGHLIGHTS = 50_000


class HighlightsKind(str, Enum):
    kindle_clippings = "kindle_clippings"
    kindle_notebook = "kindle_notebook"
    readwise_csv = "readwise_csv"


class HighlightsError(Exception):
    """Base for highlights extraction failures."""


class EmptyHighlightsError(HighlightsError):
    """The export parsed but held no passages."""


class Highlight(BaseModel):
    index: int
    number: int
    text: str
    book_title: str = ""
    book_author: str = ""
    #: The reader app's own anchor, verbatim ("Location 1482-1484", "Page 73").
    location: str = ""
    #: ``highlight`` | ``note`` | ``bookmark`` — a Kindle export mixes all three
    #: and a bookmark has no words, so it is dropped rather than kept as blank.
    kind: str = "highlight"
    added_at: str = ""
    #: The row exactly as the file carried it, for the columns this codec does
    #: not model. Readwise ships tags, a color, a location type and an Amazon
    #: book id that the Masterwork portion has no use for but the export index
    #: filters on. Carrying the row is what lets BOTH projections keep everything
    #: off ONE parser instead of a second reader growing beside this one to
    #: recover four columns. Empty for formats that are not row-shaped.
    raw: dict[str, str] = Field(default_factory=dict)

    def citation(self) -> str:
        book = self.book_title or "this book"
        return f"{book} — {self.location}" if self.location else book


class HighlightsExtraction(BaseModel):
    kind: HighlightsKind
    highlights: list[Highlight] = Field(default_factory=list)
    books: list[str] = Field(default_factory=list)
    words: int = 0
    raw_chars: int = 0
    truncated: bool = False
    dropped_empty: int = 0
    metadata: dict[str, str | int | bool] = Field(default_factory=dict)

    @property
    def markdown(self) -> str:
        out: list[str] = []
        last_book = None
        for h in self.highlights:
            if h.book_title != last_book:
                last_book = h.book_title
                out.append(f"## {h.book_title or 'Highlights'}")
            anchor = f" ({h.location})" if h.location else ""
            out.append(f"> {h.text}{anchor}")
        return "\n\n".join(out)


# --- sniffing -------------------------------------------------------------- #


def looks_like_kindle_clippings(text: str) -> bool:
    """True for a Kindle ``My Clippings.txt``. Content-based, because the file
    is a ``.txt`` like any other and its NAME is often changed by the person
    who copied it off the device."""
    head = text[:20_000]
    if CLIPPINGS_SEPARATOR not in head:
        return False
    return bool(
        re.search(r"(?im)^-\s*Your (Highlight|Note|Bookmark)\b", head)
        or re.search(r"(?im)^-\s*(Ihre Markierung|Votre surlignement|Su subrayado)", head)
    )


def looks_like_kindle_notebook(text: str) -> bool:
    """True for the HTML ``read.amazon.com/notebook`` exports. Structural, not
    filename-based: the person renames the download, and Amazon has changed the
    wrapper markup more than once while keeping these class names."""
    head = text[:400_000]
    if "<" not in head:
        return False
    has_notes = "noteText" in head and "noteHeading" in head
    return bool(has_notes or ("kp-notebook" in head.lower() and "bookTitle" in head))


def looks_like_readwise_csv(text: str) -> bool:
    first = text[:2000].splitlines()[0] if text.strip() else ""
    lowered = first.lower()
    return "highlight" in lowered and ("book title" in lowered or "title" in lowered)


def classify_highlights(
    raw: bytes | str, *, file_name: str | None = None
) -> HighlightsKind | None:
    """The highlights export kind for these bytes, or None."""
    text = decode_text(raw) if isinstance(raw, bytes) else raw
    name = (file_name or "").lower()
    if looks_like_kindle_clippings(text):
        return HighlightsKind.kindle_clippings
    if name.endswith(".csv") and looks_like_readwise_csv(text):
        return HighlightsKind.readwise_csv
    if looks_like_kindle_notebook(text):
        return HighlightsKind.kindle_notebook
    if looks_like_readwise_csv(text) and "," in text[:2000]:
        return HighlightsKind.readwise_csv
    return None


# --- Kindle "My Clippings.txt" --------------------------------------------- #

# "- Your Highlight on page 73 | Location 1482-1484 | Added on Monday, …"
# The kind word and the anchors are localized, so the parse is deliberately
# forgiving: anything on that line that is not the date is the location.
_CLIP_META = re.compile(
    r"(?im)^-\s*(?:Your|Ihre|Votre|Su)?\s*"
    r"(?P<kind>Highlight|Note|Bookmark|Markierung|Notiz|Lesezeichen|"
    r"surlignement|note|signet|subrayado|nota|marcador)"
    r"(?P<rest>.*)$"
)
_CLIP_ADDED = re.compile(r"(?i)\|\s*(?:Added on|Hinzugefügt am|Ajouté le|Añadido el)\s*(?P<when>.+)$")

_KIND_WORDS = {
    "highlight": "highlight",
    "markierung": "highlight",
    "surlignement": "highlight",
    "subrayado": "highlight",
    "note": "note",
    "notiz": "note",
    "nota": "note",
    "bookmark": "bookmark",
    "lesezeichen": "bookmark",
    "signet": "bookmark",
    "marcador": "bookmark",
}


def _split_title_author(line: str) -> tuple[str, str]:
    """``Who: The A Method for Hiring (Smart, Geoff)`` -> title, author."""
    line = line.strip().lstrip("﻿").strip()
    match = re.match(r"^(?P<title>.+?)\s*\((?P<author>[^()]+)\)\s*$", line)
    if not match:
        return line, ""
    author = match.group("author").strip()
    if "," in author and author.count(",") == 1:
        last, first = (p.strip() for p in author.split(","))
        if last and first:
            author = f"{first} {last}"
    return match.group("title").strip(), author


def iter_kindle_clippings(lines: Iterable[str]) -> Iterator[Highlight]:
    """Every clipping, one record held at a time.

    THE streaming reader for this format. ``parse_kindle_clippings`` is a thin
    ``list()`` over it, and aidream's export adapter projects its own row shape
    off the same generator - one parser, two projections, which is the whole
    point of BOARD row B9. A decade of reading is a large file and the export
    lane cannot hold it, so the streaming shape is the canonical one and the
    whole-string API is the convenience built on it, never the other way round.

    Takes lines rather than a file handle so that a caller with a string, a text
    handle, or a decoded archive member all feed it the same way.
    """
    record: list[str] = []
    index = 0

    def finish(record: list[str], index: int) -> Highlight | None:
        kept = [ln.rstrip() for ln in record if ln.strip()]
        if len(kept) < 2:
            return None
        return _clipping_from_lines(kept, index)

    for raw in lines:
        if raw.strip() == CLIPPINGS_SEPARATOR or raw.strip().startswith(
            CLIPPINGS_SEPARATOR
        ):
            made = finish(record, index)
            record = []
            if made is not None:
                index += 1
                yield made
            continue
        record.append(raw)

    made = finish(record, index)  # a file whose last record has no separator
    if made is not None:
        yield made


def _clipping_from_lines(lines: list[str], index: int) -> Highlight | None:
    """One record's lines -> one Highlight, or None for a bookmark with no words."""
    title, author = _split_title_author(lines[0])
    meta_match = _CLIP_META.search(lines[1])
    kind = "highlight"
    location = ""
    added = ""
    if meta_match:
        kind = _KIND_WORDS.get(meta_match.group("kind").strip().lower(), "highlight")
        rest = meta_match.group("rest") or ""
        added_match = _CLIP_ADDED.search(rest)
        if added_match:
            added = added_match.group("when").strip()
            rest = rest[: added_match.start()]
        location = re.sub(r"\s+", " ", rest.strip(" |")).strip()
        # "on page 73 | Location 1482" -> "page 73 | Location 1482": the
        # leading preposition belongs to the sentence, not the anchor.
        location = re.sub(r"(?i)^(on|at|auf|sur|en)\s+", "", location).strip(" |")
    body = " ".join(ln.strip() for ln in lines[2:]).strip()
    if not body:
        return None  # a bookmark has no words — dropped, and counted
    return Highlight(
        index=index,
        number=index + 1,
        text=body,
        book_title=title,
        book_author=author,
        location=location,
        kind=kind,
        added_at=added,
    )


def parse_kindle_clippings(text: str) -> list[Highlight]:
    """Every clipping, in memory. A ``list()`` over the streaming reader above."""
    return list(iter_kindle_clippings(text.splitlines()))


# --- Kindle Notebook export (HTML) ----------------------------------------- #


def parse_kindle_notebook(source: str) -> list[Highlight]:
    """The HTML ``read.amazon.com/notebook`` downloads.

    Amazon's markup uses class names (``bookTitle``, ``authors``,
    ``noteHeading``, ``noteText``) that have been stable for years; the parse
    falls back to structural order when they change, rather than returning
    nothing."""
    def _class_texts(name: str) -> list[str]:
        return [
            re.sub(r"\s+", " ", html_to_blocks(chunk)[1][0] if html_to_blocks(chunk)[1] else "").strip()
            for chunk in re.findall(
                rf'(?is)<[^>]*class="[^"]*\b{name}\b[^"]*"[^>]*>(.*?)</(?:div|h\d|span|p)>',
                source,
            )
        ]

    titles = _class_texts("bookTitle")
    authors = _class_texts("authors")
    headings = re.findall(
        r'(?is)<[^>]*class="[^"]*\bnoteHeading\b[^"]*"[^>]*>(.*?)</(?:div|h\d|span|p)>',
        source,
    )
    bodies = re.findall(
        r'(?is)<[^>]*class="[^"]*\bnoteText\b[^"]*"[^>]*>(.*?)</(?:div|h\d|span|p)>',
        source,
    )
    title = titles[0] if titles else ""
    author = authors[0] if authors else ""
    out: list[Highlight] = []
    for i, body_html in enumerate(bodies):
        blocks = html_to_blocks(body_html)[1]
        body = " ".join(blocks).strip()
        if not body:
            continue
        heading = ""
        if i < len(headings):
            heading_blocks = html_to_blocks(headings[i])[1]
            heading = " ".join(heading_blocks).strip()
        kind = "note" if re.search(r"(?i)\bnote\b", heading) else "highlight"
        location = ""
        loc_match = re.search(r"(?i)((?:page|location)\s*[\d,\-–]+)", heading)
        if loc_match:
            location = loc_match.group(1).strip()
        out.append(
            Highlight(
                index=len(out),
                number=len(out) + 1,
                text=body,
                book_title=title,
                book_author=author,
                location=location,
                kind=kind,
            )
        )
    return out


# --- Readwise CSV ---------------------------------------------------------- #

_READWISE_COLUMNS = {
    "text": ("highlight", "text", "highlight text"),
    "title": ("book title", "title", "document title"),
    "author": ("book author", "author"),
    "location": ("location", "page", "location number"),
    "note": ("note", "highlight note"),
    "date": ("highlighted at", "date", "created at"),
}


def iter_readwise_csv(handle: "io.TextIOBase | Iterable[str]") -> Iterator[Highlight]:
    """Every Readwise row, streamed.

    THE streaming reader for this format, for the same reason as the Kindle one
    above: aidream's export adapter projects ExportItem off this generator rather
    than keeping a second copy of the column-name guessing, which is the drift
    BOARD row B9 named. ``csv.DictReader`` already reads a row at a time, so this
    holds one row whatever the file's size.
    """
    reader = csv.DictReader(handle)
    if not reader.fieldnames:
        return
    lookup = {(name or "").strip().lower(): name for name in reader.fieldnames}

    def column(key: str) -> str | None:
        for candidate in _READWISE_COLUMNS[key]:
            if candidate in lookup:
                return lookup[candidate]
        return None

    col_text = column("text")
    if not col_text:
        return
    col_title, col_author = column("title"), column("author")
    col_location, col_note, col_date = column("location"), column("note"), column("date")

    index = 0
    for row in reader:
        body = (row.get(col_text) or "").strip()
        if not body:
            continue
        location = (row.get(col_location) or "").strip() if col_location else ""
        if location and location.isdigit():
            location = f"Location {location}"
        note = (row.get(col_note) or "").strip() if col_note else ""
        yield Highlight(
            index=index,
            number=index + 1,
            text=f"{body}\n\nMy note: {note}" if note else body,
            book_title=(row.get(col_title) or "").strip() if col_title else "",
            book_author=(row.get(col_author) or "").strip() if col_author else "",
            location=location,
            kind="highlight",
            added_at=(row.get(col_date) or "").strip() if col_date else "",
            raw={k: v for k, v in row.items() if isinstance(k, str) and isinstance(v, str)},
        )
        index += 1


def parse_readwise_csv(text: str) -> list[Highlight]:
    """Every Readwise row, in memory. A ``list()`` over the streaming reader."""
    return list(iter_readwise_csv(io.StringIO(text)))


# --- extraction ------------------------------------------------------------ #


def extract_highlights(
    raw: bytes | str,
    *,
    file_name: str | None = None,
    kind: HighlightsKind | None = None,
) -> HighlightsExtraction:
    """bytes -> one portion per highlight, each with its book and anchor."""
    text = decode_text(raw) if isinstance(raw, bytes) else raw
    resolved = kind or classify_highlights(text, file_name=file_name)
    if resolved is None:
        raise HighlightsError(
            f"{file_name or 'this file'} is not a highlights export we recognize "
            "(Kindle “My Clippings.txt”, a Kindle Notebook export, or a Readwise CSV)."
        )

    if resolved is HighlightsKind.kindle_clippings:
        items = parse_kindle_clippings(text)
    elif resolved is HighlightsKind.kindle_notebook:
        items = parse_kindle_notebook(text)
    else:
        items = parse_readwise_csv(text)

    if not items:
        raise EmptyHighlightsError(
            f"{file_name or 'this export'} parsed as a "
            f"{resolved.value.replace('_', ' ')} but held no passages."
        )

    truncated = False
    if len(items) > MAX_HIGHLIGHTS:
        items = items[:MAX_HIGHLIGHTS]
        truncated = True
        for i, item in enumerate(items):
            item.index, item.number = i, i + 1

    books: list[str] = []
    for item in items:
        if item.book_title and item.book_title not in books:
            books.append(item.book_title)

    return HighlightsExtraction(
        kind=resolved,
        highlights=items,
        books=books,
        words=sum(len(h.text.split()) for h in items),
        raw_chars=len(text),
        truncated=truncated,
        metadata={
            "highlights": len(items),
            "books": len(books),
            "notes": sum(1 for h in items if h.kind == "note"),
            "truncated": truncated,
        },
    )


__all__ = [
    "CLIPPINGS_SEPARATOR",
    "iter_kindle_clippings",
    "iter_readwise_csv",
    "EmptyHighlightsError",
    "Highlight",
    "HighlightsError",
    "HighlightsExtraction",
    "HighlightsKind",
    "classify_highlights",
    "extract_highlights",
    "looks_like_kindle_clippings",
    "looks_like_kindle_notebook",
    "looks_like_readwise_csv",
    "parse_kindle_clippings",
    "parse_kindle_notebook",
    "parse_readwise_csv",
]
