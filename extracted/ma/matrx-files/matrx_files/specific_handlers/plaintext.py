"""Plain-text codec — .txt / .md / .rtf into the SAME converged portions shape
the Office and PDF codecs produce.

    from matrx_files.specific_handlers.plaintext import extract_plaintext

IN (``extract_plaintext``) — bytes -> ``PlainTextExtraction`` (portions of
roughly N words each, each already clean). A plain-text file has no pages, so
the portion is the page-equivalent: a run of whole paragraphs up to a word
budget, never a mid-sentence cut. That is what lets a .txt flow through the
identical pipeline a PDF does (portions -> clean/chunk/embed/ner) with zero
format-specific code downstream.

Why this exists (2026-09-12): every upload picker in the platform advertised
``.txt,.md,.rtf`` while the only registered readers were PDF and OpenXML
Office, so the simplest possible source — a text file of notes — was invited
and then refused. A codec is the honest fix; narrowing the picker would have
been the dishonest one.

Pure python: no host imports, no ORM, no network, no LibreOffice.
"""

from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, Field

from .knobs import extraction_knob

# --- MIME constants (the canonical strings every routing table imports) ------

TXT_MIME = "text/plain"
MD_MIME = "text/markdown"
RTF_MIME = "application/rtf"
CSV_MIME = "text/csv"


class PlainTextKind(str, Enum):
    """The text family a set of bytes belongs to."""

    txt = "txt"
    md = "md"
    rtf = "rtf"
    csv = "csv"
    #: A highlights export (Kindle "My Clippings.txt", a Kindle Notebook HTML
    #: export, or a Readwise CSV). Detected from the CONTENT, never the name.
    highlights = "highlights"


# mime (lowercased, no parameters) -> kind
PLAINTEXT_MIMES: dict[str, PlainTextKind] = {
    TXT_MIME: PlainTextKind.txt,
    "text/x-log": PlainTextKind.txt,
    MD_MIME: PlainTextKind.md,
    "text/x-markdown": PlainTextKind.md,
    RTF_MIME: PlainTextKind.rtf,
    "text/rtf": PlainTextKind.rtf,
    CSV_MIME: PlainTextKind.csv,
    "application/csv": PlainTextKind.csv,
}

# filename extension -> kind. The wire mime is routinely wrong or absent
# (TUS uploads carry application/octet-stream), so the extension decides too.
PLAINTEXT_EXTENSIONS: dict[str, PlainTextKind] = {
    ".txt": PlainTextKind.txt,
    ".text": PlainTextKind.txt,
    ".log": PlainTextKind.txt,
    ".md": PlainTextKind.md,
    ".markdown": PlainTextKind.md,
    ".mdown": PlainTextKind.md,
    ".rtf": PlainTextKind.rtf,
    ".csv": PlainTextKind.csv,
}

# Bounds. A text file can be a 40 MB log; portions and the whole document are
# hard-capped, and the extraction records what it trimmed rather than trimming
# silently.
# The three bounds are `platform.feature_knob` rows (feature media.file_service);
# each constant is the package's standalone default and the host binds the live
# row through configure_extraction_knobs (see ../knobs.py).
DEFAULT_WORDS_PER_PORTION = 700
#: KNOB MIRROR of platform.feature_knob "media.file_service" "plaintext_max_portions"
MAX_PORTIONS = 2_000
#: KNOB MIRROR of platform.feature_knob "media.file_service" "plaintext_max_portion_chars"
MAX_PORTION_CHARS = 200_000
#: KNOB MIRROR of platform.feature_knob "media.file_service" "plaintext_max_total_chars"
MAX_TOTAL_CHARS = 20_000_000


class PlainTextExtractionError(Exception):
    """Base for plain-text extraction failures."""


class EmptyTextError(PlainTextExtractionError):
    """The bytes decoded to nothing readable."""


class PlainTextPortion(BaseModel):
    """One converged unit — the plain-text analogue of a PDF page: whole
    paragraphs up to the word budget. ``markdown`` and ``text`` carry the same
    body (text IS the AI-facing form here)."""

    index: int  # 0-based
    number: int  # 1-based (page_number equivalent)
    text: str = ""
    markdown: str = ""
    word_count: int = 0
    #: The reader app's own anchor for this passage, verbatim, when the file
    #: carried one ("Location 1482-1484", "Page 73"). Empty for ordinary text.
    anchor: str = ""
    #: What this portion came out of, when one file holds several works (a
    #: Kindle clippings file is every book the person ever highlighted).
    source_label: str = ""

    @property
    def char_count(self) -> int:
        return len(self.text)


class PlainTextExtraction(BaseModel):
    kind: PlainTextKind
    mime_type: str
    portions: list[PlainTextPortion] = Field(default_factory=list)
    raw_chars: int = 0
    words: int = 0
    metadata: dict[str, str | int | bool] = Field(default_factory=dict)

    @property
    def markdown(self) -> str:
        return "\n\n".join(p.text for p in self.portions)


def classify_plaintext(
    mime_type: str | None = None, file_name: str | None = None
) -> PlainTextKind | None:
    """The text kind for this file, or None when it isn't one we read."""
    if mime_type:
        mime = mime_type.lower().split(";", 1)[0].strip()
        kind = PLAINTEXT_MIMES.get(mime)
        if kind is not None:
            return kind
    name = (file_name or "").lower()
    for ext, kind in PLAINTEXT_EXTENSIONS.items():
        if name.endswith(ext):
            return kind
    return None


def canonical_mime(kind: PlainTextKind) -> str:
    return {
        PlainTextKind.txt: TXT_MIME,
        PlainTextKind.md: MD_MIME,
        PlainTextKind.rtf: RTF_MIME,
        PlainTextKind.csv: CSV_MIME,
        PlainTextKind.highlights: TXT_MIME,
    }[kind]


def decode_text(raw: bytes) -> str:
    """Bytes -> str without ever raising: BOM-aware, then utf-8, then a
    byte-preserving latin-1. A source file is never refused for its encoding."""
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig", errors="replace")
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")


# --- RTF ------------------------------------------------------------------- #
#
# A compact, dependency-free de-RTF: RTF is a group/control-word format, so
# plain text is what survives after the control words, the binary/metadata
# destinations, and the group braces are removed. This is the same approach the
# well-known `striprtf` recipe takes, written here so the codec carries no
# extra dependency.

# Destinations whose CONTENT is metadata/binary, never body text.
_RTF_SKIP_DESTINATIONS = {
    "fonttbl",
    "colortbl",
    "stylesheet",
    "info",
    "pict",
    "object",
    "objdata",
    "themedata",
    "colorschememapping",
    "datastore",
    "latentstyles",
    "listtable",
    "listoverridetable",
    "rsidtbl",
    "generator",
    "filetbl",
    "xmlnstbl",
}

# Control words that stand for a character.
_RTF_CHARACTERS = {
    "par": "\n",
    "line": "\n",
    "sect": "\n\n",
    "page": "\n\n",
    "tab": "\t",
    "emdash": "\u2014",
    "endash": "\u2013",
    "lquote": "\u2018",
    "rquote": "\u2019",
    "ldblquote": "\u201c",
    "rdblquote": "\u201d",
    "bullet": "\u2022",
    "~": "\u00a0",
    "_": "-",
    "-": "",
}

_RTF_TOKEN = re.compile(
    r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?"  # control word (+ optional numeric arg)
    r"|\\'([0-9a-f]{2})"  # hex-escaped byte
    r"|\\([^a-z])"  # control symbol
    r"|([{}])"  # group
    r"|[\r\n]+"  # literal newlines are not text in RTF
    r"|(.)",  # a plain character
    re.IGNORECASE,
)


def rtf_to_text(source: str) -> str:
    """Best-effort plain text out of an RTF document."""
    out: list[str] = []
    depth = 0
    # Depth at which we entered a skipped destination (None = not skipping).
    skip_from: int | None = None
    for match in _RTF_TOKEN.finditer(source):
        word, _arg, hexbyte, symbol, brace, char = match.groups()
        if brace == "{":
            depth += 1
            continue
        if brace == "}":
            if skip_from is not None and depth <= skip_from:
                skip_from = None
            depth -= 1
            continue
        if word is not None:
            lowered = word.lower()
            if lowered in _RTF_SKIP_DESTINATIONS:
                if skip_from is None:
                    skip_from = depth
                continue
            if skip_from is not None:
                continue
            replacement = _RTF_CHARACTERS.get(lowered)
            if replacement is not None:
                out.append(replacement)
            continue
        if skip_from is not None:
            continue
        if hexbyte is not None:
            try:
                out.append(bytes([int(hexbyte, 16)]).decode("cp1252", errors="replace"))
            except ValueError:  # pragma: no cover - the regex guarantees hex
                pass
            continue
        if symbol is not None:
            if symbol == "*":
                # \* marks an ignorable destination: skip the whole group.
                if skip_from is None:
                    skip_from = depth
                continue
            if symbol in ("\\", "{", "}"):
                out.append(symbol)
            continue
        if char is not None:
            out.append(char)
    text = "".join(out)
    # RTF writers emit a \par per line; collapse the runs they leave behind.
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# --- extraction ------------------------------------------------------------ #


def _paragraphs(text: str) -> list[str]:
    """Blank-line separated blocks, each with its internal line breaks kept."""
    blocks = [block.strip("\n") for block in re.split(r"\n[ \t]*\n", text)]
    return [block for block in blocks if block.strip()]


def paginate_text(
    text: str, *, words_per_portion: int = DEFAULT_WORDS_PER_PORTION
) -> list[str]:
    """Whole paragraphs accumulated up to a word budget — the page-equivalent.

    A paragraph longer than the budget on its own is hard-split on word
    boundaries (never mid-word, never mid-character), so one 50k-word wall of
    text still becomes readable portions instead of one unusable page."""
    budget = max(50, int(words_per_portion))
    pages: list[str] = []
    current: list[str] = []
    current_words = 0

    def flush() -> None:
        nonlocal current, current_words
        if current:
            pages.append("\n\n".join(current).strip())
            current = []
            current_words = 0

    for block in _paragraphs(text):
        words = block.split()
        if len(words) > budget:
            flush()
            for start in range(0, len(words), budget):
                pages.append(" ".join(words[start : start + budget]))
            continue
        if current_words and current_words + len(words) > budget:
            flush()
        current.append(block)
        current_words += len(words)
    flush()
    return [page for page in pages if page.strip()]


def _highlights_as_plaintext(
    text: str, file_name: str | None, max_portions: int
) -> PlainTextExtraction:
    """A highlights export -> ONE portion per passage, each keeping the book it
    came from and the anchor the reading app gave it."""
    from .highlights import extract_highlights

    extraction = extract_highlights(text, file_name=file_name)
    truncated = extraction.truncated
    items = extraction.highlights
    if len(items) > max_portions:
        items = items[:max_portions]
        truncated = True
    portions = [
        PlainTextPortion(
            index=i,
            number=i + 1,
            text=h.text,
            markdown=h.text,
            word_count=len(h.text.split()),
            anchor=h.location,
            source_label=h.book_title,
        )
        for i, h in enumerate(items)
    ]
    return PlainTextExtraction(
        kind=PlainTextKind.highlights,
        mime_type=TXT_MIME,
        portions=portions,
        raw_chars=extraction.raw_chars,
        words=sum(p.word_count for p in portions),
        metadata={
            "highlights_kind": extraction.kind.value,
            "highlights": len(portions),
            "books": len(extraction.books),
            "truncated": truncated,
        },
    )


def extract_plaintext(
    raw: bytes | str,
    *,
    mime_type: str | None = None,
    file_name: str | None = None,
    words_per_portion: int = DEFAULT_WORDS_PER_PORTION,
) -> PlainTextExtraction:
    """bytes -> portions. Raises ``EmptyTextError`` when there is no readable
    text, so a caller never persists an empty document that looks successful."""
    kind = classify_plaintext(mime_type, file_name) or PlainTextKind.txt
    text = decode_text(raw) if isinstance(raw, bytes) else raw
    raw_chars = len(text)
    truncated = False
    max_total_chars = int(extraction_knob("plaintext_max_total_chars", MAX_TOTAL_CHARS))
    max_portions = int(extraction_knob("plaintext_max_portions", MAX_PORTIONS))
    max_portion_chars = int(extraction_knob("plaintext_max_portion_chars", MAX_PORTION_CHARS))
    if raw_chars > max_total_chars:
        text = text[:max_total_chars]
        truncated = True
    # A highlights export is a text file by extension and a *book* by content:
    # sniffed here so a person's "My Clippings.txt" or Readwise CSV keeps its
    # per-passage book and location anchor instead of becoming a wall of text.
    # (Imported inside the function: the highlights codec reads this module.)
    if kind in (PlainTextKind.txt, PlainTextKind.csv):
        from .highlights import HighlightsError, classify_highlights

        if classify_highlights(text, file_name=file_name) is not None:
            try:
                return _highlights_as_plaintext(text, file_name, max_portions)
            except HighlightsError:
                # Looked like an export, parsed as nothing — fall through and
                # read it as the plain text it also is, never refuse it.
                pass

    if kind is PlainTextKind.rtf:
        text = rtf_to_text(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        raise EmptyTextError(
            f"no readable text in {file_name or 'the file'} ({kind.value})"
        )

    pages = paginate_text(text, words_per_portion=words_per_portion)
    if len(pages) > max_portions:
        pages = pages[:max_portions]
        truncated = True
    portions = [
        PlainTextPortion(
            index=i,
            number=i + 1,
            text=page[:max_portion_chars],
            markdown=page[:max_portion_chars],
            word_count=len(page.split()),
        )
        for i, page in enumerate(pages)
    ]
    return PlainTextExtraction(
        kind=kind,
        mime_type=canonical_mime(kind),
        portions=portions,
        raw_chars=raw_chars,
        words=sum(p.word_count for p in portions),
        metadata={
            "words_per_portion": int(words_per_portion),
            "truncated": truncated,
        },
    )


__all__ = [
    "DEFAULT_WORDS_PER_PORTION",
    "EmptyTextError",
    "MD_MIME",
    "PLAINTEXT_EXTENSIONS",
    "PLAINTEXT_MIMES",
    "PlainTextExtraction",
    "PlainTextExtractionError",
    "PlainTextKind",
    "PlainTextPortion",
    "CSV_MIME",
    "RTF_MIME",
    "TXT_MIME",
    "canonical_mime",
    "classify_plaintext",
    "decode_text",
    "extract_plaintext",
    "paginate_text",
    "rtf_to_text",
]
