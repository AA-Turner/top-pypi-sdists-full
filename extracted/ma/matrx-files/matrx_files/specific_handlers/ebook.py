"""Ebook codec — EPUB / MOBI / AZW3 / FB2 / HTML / MHTML into the SAME
converged portions shape the PDF, Office and plain-text codecs produce, with
the one thing a book has that a page-stack does not: **chapters**.

    from matrx_files.specific_handlers.ebook import extract_ebook

IN (``extract_ebook``) — bytes -> ``EbookExtraction``. Every portion carries
the chapter it came from, its position inside that chapter, and how far through
the book it sits, so a rule distilled from a book can cite *"Chapter 4, part 3
of 9 — 41% in"* instead of a naked quote with no provenance.

Why this exists (2026-09-17). An expert tried to put a book he owns into a
Masterwork and was stopped in 11 seconds: the upload picker's ``accept`` list
had no ``.epub`` at all, so his own file could not even be selected. The
picker's own source comment said it plainly — *".doc / .epub are deliberately
absent: nothing reads them yet."* This is the reader that makes the list honest.

## Protection is detected and refused — never removed

A DRM-wrapped file (Adobe ADEPT, Amazon Mobipocket/KFX, Apple FairPlay, Barnes
& Noble) raises ``ProtectedEbookError``, which carries the scheme it found and
the lawful ways forward. **This codec contains no circumvention of any kind and
must never grow one** — that is the owner's decision, not a library's, and the
refusal sentence exists so a person is told the truth instead of watching an
upload fail for no stated reason.

IDPF font obfuscation (``http://www.idpf.org/2008/embedding``) is NOT DRM — it
is the standard, legal way an EPUB scrambles an embedded *font* file, and it
appears in ``META-INF/encryption.xml`` in perfectly ordinary DRM-free books
(Standard Ebooks ships it). Treating it as DRM would refuse thousands of free
books, so it is recognized and ignored.

Pure python, stdlib only: ``zipfile``, ``html.parser``, ``xml.etree``,
``email``, ``struct``. No host imports, no ORM, no network.
"""

from __future__ import annotations

import io
import re
import struct
import zipfile
from email import message_from_bytes
from email.policy import default as _email_default_policy
from enum import Enum
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from pydantic import BaseModel, Field

from .knobs import extraction_knob
from .plaintext import DEFAULT_WORDS_PER_PORTION, decode_text, paginate_text

# --- MIME constants (the canonical strings every routing table imports) ------

EPUB_MIME = "application/epub+zip"
MOBI_MIME = "application/x-mobipocket-ebook"
AZW3_MIME = "application/vnd.amazon.mobi8-ebook"
FB2_MIME = "application/x-fictionbook+xml"
HTML_MIME = "text/html"
MHTML_MIME = "message/rfc822"


class EbookKind(str, Enum):
    """The ebook family a set of bytes belongs to."""

    epub = "epub"
    mobi = "mobi"
    azw3 = "azw3"
    fb2 = "fb2"
    html = "html"
    mhtml = "mhtml"


#: mime (lowercased, no parameters) -> kind
EBOOK_MIMES: dict[str, EbookKind] = {
    EPUB_MIME: EbookKind.epub,
    "application/epub": EbookKind.epub,
    MOBI_MIME: EbookKind.mobi,
    "application/x-mobi8-ebook": EbookKind.azw3,
    AZW3_MIME: EbookKind.azw3,
    FB2_MIME: EbookKind.fb2,
    "text/fb2+xml": EbookKind.fb2,
    HTML_MIME: EbookKind.html,
    "application/xhtml+xml": EbookKind.html,
    # NOTE: `message/rfc822` and `multipart/related` are deliberately NOT here.
    # A saved web page and an ordinary email share those mimes, and routing
    # every uploaded email into the book reader would be a lie about what it
    # is. `.mhtml` / `.mht` by extension is how a saved page actually arrives.
    "application/x-mimearchive": EbookKind.mhtml,
}

#: filename extension -> kind. The wire mime is routinely wrong or absent (TUS
#: uploads carry application/octet-stream), so the extension decides too.
EBOOK_EXTENSIONS: dict[str, EbookKind] = {
    ".epub": EbookKind.epub,
    ".mobi": EbookKind.mobi,
    ".prc": EbookKind.mobi,
    ".azw": EbookKind.mobi,
    ".azw3": EbookKind.azw3,
    ".fb2": EbookKind.fb2,
    ".html": EbookKind.html,
    ".htm": EbookKind.html,
    ".xhtml": EbookKind.html,
    ".mhtml": EbookKind.mhtml,
    ".mht": EbookKind.mhtml,
}

# Bounds. A book is big by nature; these are the same shape as the plain-text
# codec's bounds — `platform.feature_knob` rows (feature media.file_service)
# mirrored here so the package stands alone, never a silent clip.
#: KNOB MIRROR of platform.feature_knob "media.file_service" "ebook_max_portions"
MAX_PORTIONS = 5_000
#: KNOB MIRROR of platform.feature_knob "media.file_service" "ebook_max_total_chars"
MAX_TOTAL_CHARS = 40_000_000
#: KNOB MIRROR of platform.feature_knob "media.file_service" "ebook_max_documents"
MAX_DOCUMENTS = 4_000


# --- errors ---------------------------------------------------------------- #


class EbookExtractionError(Exception):
    """Base for ebook extraction failures.

    🚨 ``person_refusal`` IS A CONTRACT, NOT A LABEL. Every sentence this
    family raises was written for the person holding the file — what stopped
    us and what they can do instead. A caller that runs this codec behind a
    pipeline whose contract is "capture everything, never raise" must re-raise
    anything carrying this attribute, or the sentence dies in a log and the
    person gets a shrug (board row B4f, 2026-09-18: the content-processing
    orchestrator captured ``ProtectedEbookError`` as an ordinary stage failure,
    so the DRM refusal never reached a screen and the reader's handler for it
    was dead code for as long as it existed).
    """

    #: See the class docstring — pipelines that swallow exceptions re-raise
    #: these.
    person_refusal: bool = True


class EmptyEbookError(EbookExtractionError):
    """The file parsed but produced no readable words."""


class UnreadableEbookError(EbookExtractionError):
    """A structurally valid file this codec cannot decode yet (e.g. HUFF/CDIC
    compressed Mobipocket). Distinct from protection: nothing is stopping us but
    missing code, and the sentence says so."""


class ProtectedEbookError(EbookExtractionError):
    """The file is wrapped in DRM.

    Raised and never worked around. ``scheme`` names what was found;
    ``sentence()`` is the honest message a person reads, which always names the
    lawful ways forward — it is the whole point of detecting this rather than
    letting the upload die silently."""

    #: The lawful routes, in the order a person is most likely to have one.
    LAWFUL_OPTIONS: tuple[str, ...] = (
        "a DRM-free copy of the same book (many publishers sell one directly)",
        "photos of the pages of your physical copy — we read those now",
        "your own highlights export (Kindle’s “My Clippings.txt” or your "
        "Notebook page, or a Readwise export)",
        "the audiobook you own — we transcribe it",
    )

    def __init__(self, scheme: str, file_name: str | None = None) -> None:
        self.scheme = scheme
        self.file_name = file_name
        super().__init__(self.sentence())

    def sentence(self) -> str:
        name = f"“{self.file_name}”" if self.file_name else "This file"
        options = "; ".join(self.LAWFUL_OPTIONS)
        return (
            f"{name} is copy-protected ({self.scheme}), so we cannot read it — "
            f"and we will never strip a publisher’s protection. What does work: "
            f"{options}."
        )


# --- shapes ---------------------------------------------------------------- #


class EbookChapter(BaseModel):
    """One chapter (or spine document) of the book."""

    index: int  # 0-based, spine order
    number: int  # 1-based
    title: str = ""
    href: str = ""  # the document inside the container, when there is one
    word_count: int = 0
    portion_count: int = 0
    first_portion_index: int = 0


class EbookPortion(BaseModel):
    """One converged unit — the book analogue of a PDF page: whole paragraphs
    up to a word budget, **stamped with where in the book it came from**."""

    index: int  # 0-based, across the whole book
    number: int  # 1-based
    text: str = ""
    markdown: str = ""
    word_count: int = 0
    chapter_index: int = 0
    chapter_number: int = 1
    chapter_title: str = ""
    chapter_href: str = ""
    position_in_chapter: int = 1  # 1-based
    chapter_portions: int = 1
    #: 0.0–1.0 through the whole book at the START of this portion — the
    #: location analogue for a format that has no page numbers.
    progress: float = 0.0

    @property
    def char_count(self) -> int:
        return len(self.text)

    def citation(self) -> str:
        """How a rule cites this passage, in a person's words."""
        where = self.chapter_title or f"Chapter {self.chapter_number}"
        return (
            f"{where} — part {self.position_in_chapter} of "
            f"{self.chapter_portions} ({round(self.progress * 100)}% in)"
        )


class EbookExtraction(BaseModel):
    kind: EbookKind
    mime_type: str
    title: str = ""
    authors: list[str] = Field(default_factory=list)
    language: str = ""
    publisher: str = ""
    identifier: str = ""
    chapters: list[EbookChapter] = Field(default_factory=list)
    portions: list[EbookPortion] = Field(default_factory=list)
    raw_chars: int = 0
    words: int = 0
    truncated: bool = False
    metadata: dict[str, str | int | bool] = Field(default_factory=dict)

    @property
    def markdown(self) -> str:
        out: list[str] = []
        last_chapter = -1
        for portion in self.portions:
            if portion.chapter_index != last_chapter:
                last_chapter = portion.chapter_index
                heading = portion.chapter_title or f"Chapter {portion.chapter_number}"
                out.append(f"## {heading}")
            out.append(portion.text)
        return "\n\n".join(out)


def classify_ebook(
    mime_type: str | None = None, file_name: str | None = None
) -> EbookKind | None:
    """The ebook kind for this file, or None when it isn't one we read."""
    name = (file_name or "").lower()
    # Extension wins over mime here (unlike plaintext): an .epub routinely
    # arrives as application/zip and an .azw3 as application/octet-stream, and
    # `.mhtml` legitimately carries `message/rfc822` which is also plain email.
    for ext, kind in EBOOK_EXTENSIONS.items():
        if name.endswith(ext):
            return kind
    if mime_type:
        mime = mime_type.lower().split(";", 1)[0].strip()
        kind = EBOOK_MIMES.get(mime)
        if kind is not None:
            return kind
    return None


def canonical_mime(kind: EbookKind) -> str:
    return {
        EbookKind.epub: EPUB_MIME,
        EbookKind.mobi: MOBI_MIME,
        EbookKind.azw3: AZW3_MIME,
        EbookKind.fb2: FB2_MIME,
        EbookKind.html: HTML_MIME,
        EbookKind.mhtml: MHTML_MIME,
    }[kind]


# --- HTML -> blocks (stdlib only) ------------------------------------------ #

_BLOCK_TAGS = {
    "p", "div", "section", "article", "blockquote", "li", "tr", "pre",
    "h1", "h2", "h3", "h4", "h5", "h6", "figcaption", "dd", "dt", "td", "th",
}
_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_DROP_TAGS = {"script", "style", "head", "nav", "svg", "noscript", "template"}


class _HtmlBlocks(HTMLParser):
    """HTML -> (heading, blocks). Block-level tags become paragraph breaks; the
    first heading becomes the document's title. No dependency, no DOM."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[str] = []
        self.headings: list[str] = []
        self._buf: list[str] = []
        self._drop_depth = 0
        self._heading_depth = 0

    # -- helpers
    def _flush(self) -> None:
        text = "".join(self._buf)
        self._buf = []
        collapsed = re.sub(r"[ \t ]+", " ", text).strip()
        if collapsed:
            self.blocks.append(collapsed)
            if self._heading_depth > 0:
                self.headings.append(collapsed)

    # -- parser hooks
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _DROP_TAGS:
            self._drop_depth += 1
            return
        if self._drop_depth:
            return
        if tag == "br":
            self._buf.append(" ")
            return
        if tag in _BLOCK_TAGS:
            self._flush()
            if tag in _HEADING_TAGS:
                self._heading_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in _DROP_TAGS:
            self._drop_depth = max(0, self._drop_depth - 1)
            return
        if self._drop_depth:
            return
        if tag in _BLOCK_TAGS:
            self._flush()
            if tag in _HEADING_TAGS:
                self._heading_depth = max(0, self._heading_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._drop_depth:
            return
        self._buf.append(data)

    def close(self) -> None:  # type: ignore[override]
        super().close()
        self._flush()


def html_to_blocks(source: str) -> tuple[str, list[str]]:
    """(first heading, paragraph blocks) out of an HTML/XHTML document."""
    parser = _HtmlBlocks()
    try:
        parser.feed(source)
        parser.close()
    except Exception:  # noqa: BLE001 — a malformed book is still a book
        parser._flush()
    heading = parser.headings[0] if parser.headings else ""
    return heading, [b for b in parser.blocks if b]


# --- container readers ----------------------------------------------------- #


class _Document(BaseModel):
    """One spine document before pagination."""

    title: str = ""
    href: str = ""
    blocks: list[str] = Field(default_factory=list)


_NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "cnt": "urn:oasis:names:tc:opendocument:xmlns:container",
    "enc": "http://www.w3.org/2001/04/xmlenc#",
    "ncx": "http://www.daisy.org/z3986/2005/ntoc-not-used",
}

#: Encryption algorithms that MAY be font obfuscation — the IDPF scheme and
#: Adobe's font-mangling scheme, which every ordinary EPUB with an embedded
#: font uses. 🚨 An algorithm alone NEVER settles the question (see
#: `_epub_protection`): the same two URIs appear in real Adobe ADEPT
#: `encryption.xml` manifests, so what they COVER is what decides.
_FONT_OBFUSCATION = {
    "http://www.idpf.org/2008/embedding",
    "http://ns.adobe.com/pdf/enc#RC",
}

#: Adobe's DRM namespace. Any element from it inside `encryption.xml` (the
#: `<adept:resource>` that names the licensed resource) is ADEPT and nothing
#: else — font obfuscation never carries one.
_ADEPT_NS = "http://ns.adobe.com/adept"

#: Readium LCP's license file. Most European store and library EPUBs today are
#: LCP, and we detected none of them before 2026-09-18.
_LCP_LICENCE = "META-INF/license.lcpl"

#: What font obfuscation is ALLOWED to cover. Anything else under an
#: obfuscation algorithm is content encryption wearing a font's URI.
_FONT_SUFFIXES = (".otf", ".ttf", ".ttc", ".woff", ".woff2", ".eot", ".dfont")


def _name_scheme(algorithms: set[str]) -> str:
    """What to CALL the protection, for a person. A raw algorithm URI in the
    refusal sentence is a URL read aloud at someone who wants their own book —
    the scheme goes in the log and the block row, a plain phrase goes to them.
    """
    if any("adobe" in a.lower() for a in algorithms):
        return "Adobe ADEPT"
    if any("lcp" in a.lower() or "readium" in a.lower() for a in algorithms):
        return "Readium LCP"
    return "a copy-protection scheme we do not recognize"


def _epub_protection(zf: zipfile.ZipFile) -> str | None:
    """The DRM scheme in this EPUB, or None. Font obfuscation is not DRM.

    🚨 THE ALGORITHM URI IS NOT THE ANSWER. Until 2026-09-18 this decided
    purely on `EncryptionMethod/@Algorithm`, with
    `http://ns.adobe.com/pdf/enc#RC` permanently allow-listed as "font
    obfuscation". That URI is ALSO what a real Adobe ADEPT manifest carries, so
    an ADEPT-wrapped book whose `encryption.xml` named it — and carried an
    `<adept:resource>` and a `CipherReference` at a stylesheet, neither of
    which font obfuscation ever has — was read as DRM-free. It was then parsed
    as an ordinary book, and the person got a generic ten-minute timeout
    instead of the refusal sentence naming the lawful routes (board row B4f).

    Three signals now decide, in order of how certain they are:
      1. a scheme's own file or namespace (`rights.xml`, `license.lcpl`,
         `sinf`, the ADEPT namespace) — unambiguous;
      2. what an obfuscation-shaped algorithm actually COVERS — obfuscation
         only ever covers font files;
      3. any other algorithm — content encryption by definition.

    Font obfuscation stays free: a manifest whose obfuscation algorithms cover
    only fonts (or name no resource at all) still returns None, so the
    thousands of Standard Ebooks-style books that ship it are never refused.
    """
    names = set(zf.namelist())
    if "META-INF/rights.xml" in names:
        return "Adobe ADEPT"
    if _LCP_LICENCE in names:
        return "Readium LCP"
    for name in names:
        lowered = name.lower()
        if lowered.endswith(".xml") and "sinf" in lowered:
            return "Apple FairPlay"
        if lowered.endswith("/rights.xml") or lowered.endswith("kindle.dat"):
            return "vendor DRM"
    if "META-INF/encryption.xml" not in names:
        return None
    try:
        root = ET.fromstring(zf.read("META-INF/encryption.xml"))
    except ET.ParseError:
        # An encryption declaration we cannot even parse is not something to
        # guess about — say so honestly rather than reading half a book.
        return "an unreadable encryption declaration"

    # (1) The licensing namespaces speak for themselves.
    for el in root.iter():
        tag = str(el.tag)
        if tag.startswith(f"{{{_ADEPT_NS}"):
            return "Adobe ADEPT"
    if any(
        "license.lcpl" in (el.get("URI") or "")
        for el in root.iter()
        if el.tag.endswith("RetrievalMethod")
    ):
        return "Readium LCP"

    # (2)/(3) Per EncryptedData block: the algorithm it declares against the
    # resources it names. An obfuscation URI over a stylesheet, a chapter or
    # an image is content encryption.
    for block in [el for el in root.iter() if el.tag.endswith("EncryptedData")] or [root]:
        algorithms = {
            (el.get("Algorithm") or "").strip()
            for el in block.iter()
            if el.tag.endswith("EncryptionMethod")
        }
        algorithms = {a for a in algorithms if a}
        if not algorithms:
            continue
        targets = [
            (el.get("URI") or "").strip()
            for el in block.iter()
            if el.tag.endswith("CipherReference")
        ]
        targets = [t for t in targets if t]
        real = {a for a in algorithms if a not in _FONT_OBFUSCATION}
        if not real and targets:
            # Obfuscation-shaped, so it is only honest while every resource it
            # covers is a font.
            non_fonts = [
                t for t in targets if not t.lower().split("?")[0].endswith(_FONT_SUFFIXES)
            ]
            if non_fonts:
                return _name_scheme(algorithms)
            continue
        if not real:
            continue
        return _name_scheme(real)
    return None


def _read_epub(raw: bytes, file_name: str | None) -> tuple[list[_Document], dict[str, str]]:
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile as exc:
        raise UnreadableEbookError(
            f"{file_name or 'this file'} is not a readable EPUB container: {exc}"
        ) from exc

    with zf:
        scheme = _epub_protection(zf)
        if scheme:
            raise ProtectedEbookError(scheme, file_name)

        # container.xml -> the OPF package document
        try:
            container = ET.fromstring(zf.read("META-INF/container.xml"))
        except (KeyError, ET.ParseError) as exc:
            raise UnreadableEbookError(
                f"{file_name or 'this EPUB'} has no readable META-INF/container.xml"
            ) from exc
        rootfile = container.find(".//cnt:rootfile", _NS)
        opf_path = (rootfile.get("full-path") if rootfile is not None else None) or ""
        if not opf_path:
            raise UnreadableEbookError(
                f"{file_name or 'this EPUB'} names no package document"
            )
        base = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""

        try:
            opf = ET.fromstring(zf.read(opf_path))
        except (KeyError, ET.ParseError) as exc:
            raise UnreadableEbookError(
                f"{file_name or 'this EPUB'} has an unreadable package document "
                f"({opf_path})"
            ) from exc

        meta: dict[str, str] = {}
        for tag, key in (
            ("title", "title"),
            ("creator", "author"),
            ("language", "language"),
            ("publisher", "publisher"),
            ("identifier", "identifier"),
        ):
            el = opf.find(f".//dc:{tag}", _NS)
            if el is not None and (el.text or "").strip():
                meta.setdefault(key, (el.text or "").strip())
        authors = [
            (el.text or "").strip()
            for el in opf.findall(".//dc:creator", _NS)
            if (el.text or "").strip()
        ]
        if authors:
            meta["authors"] = "".join(authors)

        manifest: dict[str, str] = {}
        for item in opf.findall(".//opf:manifest/opf:item", _NS):
            iid = item.get("id")
            href = item.get("href")
            if iid and href:
                manifest[iid] = href

        spine_hrefs: list[str] = []
        for ref in opf.findall(".//opf:spine/opf:itemref", _NS):
            idref = ref.get("idref")
            if not idref:
                continue
            href = manifest.get(idref)
            if href and not href.lower().endswith((".css", ".jpg", ".png", ".otf", ".ttf")):
                spine_hrefs.append(href)
        if not spine_hrefs:
            # No usable spine — fall back to every XHTML in the zip, in name
            # order, and say so in metadata rather than returning nothing.
            spine_hrefs = sorted(
                n for n in zf.namelist() if n.lower().endswith((".xhtml", ".html", ".htm"))
            )
            meta["spine_fallback"] = "1"
            base = ""

        titles = _epub_toc_titles(zf, opf, base, manifest)

        max_documents = int(extraction_knob("ebook_max_documents", MAX_DOCUMENTS))
        documents: list[_Document] = []
        for href in spine_hrefs[:max_documents]:
            path = f"{base}/{href}" if base else href
            path = _normalize_zip_path(path)
            try:
                body = zf.read(path)
            except KeyError:
                continue
            heading, blocks = html_to_blocks(decode_text(body))
            if not blocks:
                continue
            documents.append(
                _Document(
                    title=titles.get(href.split("#", 1)[0], "") or heading,
                    href=href,
                    blocks=blocks,
                )
            )
        if len(spine_hrefs) > max_documents:
            meta["documents_truncated"] = str(len(spine_hrefs) - max_documents)
        return documents, meta


def _normalize_zip_path(path: str) -> str:
    """Resolve ``a/../b`` inside a zip name without touching the filesystem."""
    parts: list[str] = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _epub_toc_titles(
    zf: zipfile.ZipFile,
    opf: ET.Element,
    base: str,
    manifest: dict[str, str],
) -> dict[str, str]:
    """href -> chapter title, from the EPUB 3 nav document or the EPUB 2 NCX.

    A chapter title from the book's own table of contents is the one a reader
    would use to cite it, so it beats the first heading in the file."""
    titles: dict[str, str] = {}

    # EPUB 3 nav
    nav_href = None
    for item in opf.findall(".//opf:manifest/opf:item", _NS):
        if "nav" in (item.get("properties") or "").split():
            nav_href = item.get("href")
            break
    if nav_href:
        try:
            nav_raw = zf.read(_normalize_zip_path(f"{base}/{nav_href}" if base else nav_href))
        except KeyError:
            nav_raw = b""
        if nav_raw:
            nav_dir = nav_href.rsplit("/", 1)[0] if "/" in nav_href else ""
            for href, label in _links_from_html(decode_text(nav_raw)):
                target = _normalize_zip_path(f"{nav_dir}/{href}" if nav_dir else href)
                titles.setdefault(target.split("#", 1)[0], label)

    # EPUB 2 NCX (also present in most EPUB 3s for back-compat)
    ncx_href = None
    for iid, href in manifest.items():
        if href.lower().endswith(".ncx") or iid.lower() in ("ncx", "toc"):
            ncx_href = href
            break
    if ncx_href:
        try:
            ncx_raw = zf.read(_normalize_zip_path(f"{base}/{ncx_href}" if base else ncx_href))
        except KeyError:
            ncx_raw = b""
        if ncx_raw:
            try:
                ncx = ET.fromstring(ncx_raw)
            except ET.ParseError:
                ncx = None
            if ncx is not None:
                ncx_dir = ncx_href.rsplit("/", 1)[0] if "/" in ncx_href else ""
                for point in ncx.iter():
                    if not point.tag.endswith("navPoint"):
                        continue
                    label = ""
                    href = ""
                    for child in point.iter():
                        if child.tag.endswith("text") and not label:
                            label = (child.text or "").strip()
                        if child.tag.endswith("content") and not href:
                            href = child.get("src") or ""
                    if label and href:
                        target = _normalize_zip_path(
                            f"{ncx_dir}/{href}" if ncx_dir else href
                        )
                        titles.setdefault(target.split("#", 1)[0], label)
    return titles


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href") or None
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            label = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if label:
                self.links.append((self._href, label))
            self._href = None
            self._buf = []


def _links_from_html(source: str) -> list[tuple[str, str]]:
    parser = _Links()
    try:
        parser.feed(source)
        parser.close()
    except Exception:  # noqa: BLE001
        pass
    return parser.links


# --- FB2 ------------------------------------------------------------------- #


def _read_fb2(raw: bytes, file_name: str | None) -> tuple[list[_Document], dict[str, str]]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise UnreadableEbookError(
            f"{file_name or 'this FB2 file'} is not readable XML: {exc}"
        ) from exc

    def local(el: ET.Element) -> str:
        return el.tag.rsplit("}", 1)[-1]

    meta: dict[str, str] = {}
    for el in root.iter():
        name = local(el)
        if name == "book-title" and (el.text or "").strip():
            meta.setdefault("title", (el.text or "").strip())
        elif name == "lang" and (el.text or "").strip():
            meta.setdefault("language", (el.text or "").strip())
        elif name == "author":
            parts = [
                (child.text or "").strip()
                for child in el
                if local(child) in ("first-name", "middle-name", "last-name")
            ]
            full = " ".join(p for p in parts if p)
            if full:
                meta["authors"] = (
                    f"{meta['authors']}{full}" if "authors" in meta else full
                )

    def text_of(el: ET.Element) -> str:
        return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

    documents: list[_Document] = []
    for body in (el for el in root if local(el) == "body"):
        if (body.get("name") or "") == "notes":
            continue
        sections = [el for el in body if local(el) == "section"] or [body]
        for i, section in enumerate(sections):
            title = ""
            blocks: list[str] = []
            for child in section:
                if local(child) == "title" and not title:
                    title = text_of(child)
                    continue
                block = text_of(child)
                if block:
                    blocks.append(block)
            if blocks:
                documents.append(
                    _Document(title=title, href=f"section-{i + 1}", blocks=blocks)
                )
    return documents, meta


# --- HTML / MHTML ---------------------------------------------------------- #


def _split_html_by_headings(source: str) -> list[_Document]:
    """One long HTML page becomes chapters at its own h1/h2 boundaries — the
    structure the author already wrote, not one invented by us."""
    parts = re.split(r"(?i)(<h[12][^>]*>.*?</h[12]>)", source, flags=re.S)
    if len(parts) <= 1:
        heading, blocks = html_to_blocks(source)
        return [_Document(title=heading, href="", blocks=blocks)] if blocks else []

    documents: list[_Document] = []
    preface_heading, preface_blocks = html_to_blocks(parts[0])
    if preface_blocks:
        documents.append(
            _Document(title=preface_heading, href="", blocks=preface_blocks)
        )
    for i in range(1, len(parts) - 1, 2):
        title, _ = html_to_blocks(parts[i])
        _, blocks = html_to_blocks(parts[i + 1])
        if blocks:
            documents.append(_Document(title=title, href=f"h-{len(documents) + 1}", blocks=blocks))
    return documents


def _read_html(raw: bytes, file_name: str | None) -> tuple[list[_Document], dict[str, str]]:
    source = decode_text(raw)
    meta: dict[str, str] = {}
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", source)
    if title_match:
        meta["title"] = re.sub(r"\s+", " ", title_match.group(1)).strip()
    documents = _split_html_by_headings(source)
    if not documents:
        raise EmptyEbookError(f"no readable text in {file_name or 'this HTML file'}")
    return documents, meta


def _read_mhtml(raw: bytes, file_name: str | None) -> tuple[list[_Document], dict[str, str]]:
    """A saved web page (Chrome/Edge 'Webpage, Single File') is a MIME archive:
    stdlib `email` already parses it; the HTML part is the page."""
    message = message_from_bytes(raw, policy=_email_default_policy)
    html_parts: list[str] = []
    for part in message.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes) and payload.strip():
                html_parts.append(decode_text(payload))
    if not html_parts:
        raise UnreadableEbookError(
            f"{file_name or 'this saved page'} contains no HTML part — it may be "
            "a mail archive rather than a saved web page."
        )
    meta: dict[str, str] = {}
    subject = message.get("Subject")
    if subject:
        meta["title"] = str(subject).strip()
    location = message.get("Content-Location") or message.get("Snapshot-Content-Location")
    if location:
        meta["source_url"] = str(location).strip()
    documents: list[_Document] = []
    for source in html_parts:
        documents.extend(_split_html_by_headings(source))
    if not documents:
        raise EmptyEbookError(f"no readable text in {file_name or 'this saved page'}")
    return documents, meta


# --- MOBI / AZW3 (PalmDB) -------------------------------------------------- #

_PALMDOC_NO_COMPRESSION = 1
_PALMDOC_LZ77 = 2
_PALMDOC_HUFF_CDIC = 17480


def _palm_records(raw: bytes) -> list[bytes]:
    """The record payloads of a PalmDB (.mobi/.azw/.azw3/.prc) file."""
    if len(raw) < 78:
        raise UnreadableEbookError("file is too short to be a Mobipocket container")
    (count,) = struct.unpack_from(">H", raw, 76)
    offsets: list[int] = []
    for i in range(count):
        base = 78 + i * 8
        if base + 4 > len(raw):
            break
        (offset,) = struct.unpack_from(">I", raw, base)
        offsets.append(offset)
    records: list[bytes] = []
    for i, offset in enumerate(offsets):
        end = offsets[i + 1] if i + 1 < len(offsets) else len(raw)
        if 0 <= offset <= end <= len(raw):
            records.append(raw[offset:end])
    if not records:
        raise UnreadableEbookError("Mobipocket container has no records")
    return records


def _palmdoc_decompress(data: bytes) -> bytes:
    """PalmDOC LZ77 — the compression MOBI6 and KF8 text records use."""
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        byte = data[i]
        i += 1
        if byte == 0:
            out.append(0)
        elif byte <= 8:
            out.extend(data[i : i + byte])
            i += byte
        elif byte <= 0x7F:
            out.append(byte)
        elif byte <= 0xBF:
            if i >= n:
                break
            pair = (byte << 8) | data[i]
            i += 1
            distance = (pair >> 3) & 0x07FF
            length = (pair & 0x0007) + 3
            if distance == 0 or distance > len(out):
                break
            for _ in range(length):
                out.append(out[-distance])
        else:
            out.append(32)
            out.append(byte ^ 0x80)
    return bytes(out)


def _read_mobi(
    raw: bytes, kind: EbookKind, file_name: str | None
) -> tuple[list[_Document], dict[str, str]]:
    records = _palm_records(raw)
    header = records[0]
    if len(header) < 16:
        raise UnreadableEbookError("Mobipocket header record is truncated")
    compression, _unused, text_length, record_count = struct.unpack_from(">HHIH", header, 0)
    (encryption,) = struct.unpack_from(">H", header, 12)

    # Protection first, always — before a single byte of text is decoded.
    if encryption != 0:
        scheme = {
            1: "Mobipocket legacy DRM",
            2: "Amazon Mobipocket DRM",
        }.get(encryption, f"Amazon DRM (type {encryption})")
        raise ProtectedEbookError(scheme, file_name)
    if raw[:8] in (b"TPZ3TPZ3", b"TPZ0TPZ0") or raw[60:68] == b"TPZ3TPZ3":
        raise ProtectedEbookError("Amazon Topaz", file_name)

    if compression == _PALMDOC_HUFF_CDIC:
        raise UnreadableEbookError(
            f"{file_name or 'This Mobipocket file'} uses HUFF/CDIC compression, "
            "which we do not decode yet. An EPUB of the same book reads "
            "perfectly today, and so do photos of the pages."
        )
    if compression not in (_PALMDOC_NO_COMPRESSION, _PALMDOC_LZ77):
        raise UnreadableEbookError(
            f"{file_name or 'This Mobipocket file'} uses an unknown compression "
            f"({compression}); we only read uncompressed and PalmDOC files."
        )

    meta: dict[str, str] = {}
    # MOBI header (inside record 0, after the 16-byte PalmDOC header)
    if len(header) > 24 and header[16:20] == b"MOBI":
        (full_name_offset,) = struct.unpack_from(">I", header, 84)
        (full_name_length,) = struct.unpack_from(">I", header, 88)
        if 0 < full_name_length < 1024 and full_name_offset + full_name_length <= len(header):
            title = header[full_name_offset : full_name_offset + full_name_length]
            if title.strip():
                meta["title"] = decode_text(title).strip()

    body = bytearray()
    for record in records[1 : 1 + max(0, record_count)]:
        if compression == _PALMDOC_LZ77:
            body.extend(_palmdoc_decompress(record))
        else:
            body.extend(record)
    text = decode_text(bytes(body[:text_length] if text_length else body))
    if not text.strip():
        raise EmptyEbookError(
            f"no readable text in {file_name or 'this Mobipocket file'}"
        )
    meta["mobi_compression"] = "palmdoc" if compression == _PALMDOC_LZ77 else "none"
    meta["mobi_flavour"] = "kf8" if kind is EbookKind.azw3 else "mobi6"
    documents = _split_html_by_headings(text)
    if not documents:
        heading, blocks = html_to_blocks(text)
        documents = [_Document(title=heading, href="", blocks=blocks)] if blocks else []
    if not documents:
        raise EmptyEbookError(
            f"no readable text in {file_name or 'this Mobipocket file'}"
        )
    return documents, meta


# --- protection probe (cheap, no full parse) ------------------------------- #


def detect_protection(
    raw: bytes, *, mime_type: str | None = None, file_name: str | None = None
) -> str | None:
    """The DRM scheme guarding these bytes, or None.

    Callable on its own so a gate can refuse a protected file with the honest
    sentence WITHOUT paying for a full extraction. Never removes anything."""
    kind = classify_ebook(mime_type, file_name)
    try:
        if kind is EbookKind.epub or raw[:2] == b"PK":
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                return _epub_protection(zf)
        if kind in (EbookKind.mobi, EbookKind.azw3):
            records = _palm_records(raw)
            if len(records[0]) >= 14:
                (encryption,) = struct.unpack_from(">H", records[0], 12)
                if encryption != 0:
                    return {
                        1: "Mobipocket legacy DRM",
                        2: "Amazon Mobipocket DRM",
                    }.get(encryption, f"Amazon DRM (type {encryption})")
    except (EbookExtractionError, zipfile.BadZipFile, struct.error):
        return None
    return None


# --- extraction ------------------------------------------------------------ #


def extract_ebook(
    raw: bytes,
    *,
    mime_type: str | None = None,
    file_name: str | None = None,
    words_per_portion: int = DEFAULT_WORDS_PER_PORTION,
) -> EbookExtraction:
    """bytes -> chaptered portions.

    Raises ``ProtectedEbookError`` for DRM (with the lawful options in the
    message), ``UnreadableEbookError`` for a format we cannot decode yet, and
    ``EmptyEbookError`` when a file parses to nothing — so a caller never
    persists an empty document that looks like a success."""
    kind = classify_ebook(mime_type, file_name)
    if kind is None:
        raise UnreadableEbookError(
            f"{file_name or 'this file'} is not an ebook format we read"
        )

    if kind is EbookKind.epub:
        documents, meta = _read_epub(raw, file_name)
    elif kind in (EbookKind.mobi, EbookKind.azw3):
        documents, meta = _read_mobi(raw, kind, file_name)
    elif kind is EbookKind.fb2:
        documents, meta = _read_fb2(raw, file_name)
    elif kind is EbookKind.mhtml:
        documents, meta = _read_mhtml(raw, file_name)
    else:
        documents, meta = _read_html(raw, file_name)

    if not documents:
        raise EmptyEbookError(f"no readable text in {file_name or 'this file'}")

    max_total_chars = int(extraction_knob("ebook_max_total_chars", MAX_TOTAL_CHARS))
    max_portions = int(extraction_knob("ebook_max_portions", MAX_PORTIONS))
    truncated = bool(meta.pop("documents_truncated", ""))

    raw_chars = sum(len(b) + 2 for doc in documents for b in doc.blocks)

    # Paginate each chapter INDEPENDENTLY: a portion never spans two chapters,
    # which is what makes "chapter + position" an exact citation rather than an
    # approximation.
    chapters: list[EbookChapter] = []
    portions: list[EbookPortion] = []
    consumed_chars = 0
    for chapter_index, doc in enumerate(documents):
        if consumed_chars >= max_total_chars or len(portions) >= max_portions:
            truncated = True
            break
        body = "\n\n".join(doc.blocks)
        if consumed_chars + len(body) > max_total_chars:
            body = body[: max(0, max_total_chars - consumed_chars)]
            truncated = True
        consumed_chars += len(body)
        pages = paginate_text(body, words_per_portion=words_per_portion)
        if not pages:
            continue
        if len(portions) + len(pages) > max_portions:
            pages = pages[: max_portions - len(portions)]
            truncated = True
        first_index = len(portions)
        for position, page in enumerate(pages, start=1):
            portions.append(
                EbookPortion(
                    index=len(portions),
                    number=len(portions) + 1,
                    text=page,
                    markdown=page,
                    word_count=len(page.split()),
                    chapter_index=chapter_index,
                    chapter_number=chapter_index + 1,
                    chapter_title=doc.title,
                    chapter_href=doc.href,
                    position_in_chapter=position,
                    chapter_portions=len(pages),
                )
            )
        chapters.append(
            EbookChapter(
                index=chapter_index,
                number=chapter_index + 1,
                title=doc.title,
                href=doc.href,
                word_count=sum(len(p.split()) for p in pages),
                portion_count=len(pages),
                first_portion_index=first_index,
            )
        )

    if not portions:
        raise EmptyEbookError(f"no readable text in {file_name or 'this file'}")

    total = len(portions)
    for portion in portions:
        portion.progress = round(portion.index / total, 4)

    authors_blob = meta.pop("authors", "")
    return EbookExtraction(
        kind=kind,
        mime_type=canonical_mime(kind),
        title=meta.pop("title", ""),
        authors=[a for a in authors_blob.split("") if a],
        language=meta.pop("language", ""),
        publisher=meta.pop("publisher", ""),
        identifier=meta.pop("identifier", ""),
        chapters=chapters,
        portions=portions,
        raw_chars=raw_chars,
        words=sum(p.word_count for p in portions),
        truncated=truncated,
        metadata={
            "words_per_portion": int(words_per_portion),
            "chapters": len(chapters),
            "truncated": truncated,
            **meta,
        },
    )


__all__ = [
    "AZW3_MIME",
    "EBOOK_EXTENSIONS",
    "EBOOK_MIMES",
    "EPUB_MIME",
    "FB2_MIME",
    "HTML_MIME",
    "MHTML_MIME",
    "MOBI_MIME",
    "EbookChapter",
    "EbookExtraction",
    "EbookExtractionError",
    "EbookKind",
    "EbookPortion",
    "EmptyEbookError",
    "ProtectedEbookError",
    "UnreadableEbookError",
    "canonical_mime",
    "classify_ebook",
    "detect_protection",
    "extract_ebook",
    "html_to_blocks",
]
