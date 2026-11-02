"""Page photos — a stack of phone photographs becomes ONE ordered document.

    from matrx_files.specific_handlers.page_photos import photos_to_pdf

The most natural way a non-technical person digitises paper is to pull out
their phone and photograph each page. Until 2026-09-17 they could not: the
upload picker had no image type at all, so the file could not even be selected,
and there was no notion of "these 40 files are one thing, in this order."

This module is the missing primitive. It takes the photos, **decides their
order and says how it decided**, fixes what a phone gets wrong (HEIC, EXIF
rotation, two-page spreads), and assembles one PDF — which then flows through
the platform's existing PDF page reader and its existing OCR, with no new
pipeline and no prompt tuning anywhere.

    photos ──order──▶ normalize ──▶ one PDF ──▶ the SAME extract_pages_full /
                                                  Tesseract path a scanned PDF
                                                  has always taken

Ordering, in the order it is trusted:

1. **An explicit order the person gave** (they dragged the thumbnails) — always
   wins; nothing guesses over a human.
2. **Natural filename order** — ``IMG_4002`` before ``IMG_4010`` (a plain
   string sort puts ``IMG_40010`` before ``IMG_4002``, which is how page 100
   ends up after page 2 and nobody notices).
3. **EXIF ``DateTimeOriginal``**, then file mtime, when filenames do not sort.

When filename order and capture-time order **disagree**, that is announced in
``PagePhotoSet.order_warning`` rather than silently picked — a 400-page book in
the wrong order is worse than one that refuses.

Pure python: PIL (+ pillow-heif, already a dependency) and PyMuPDF. No host
imports, no ORM, no network.
"""

from __future__ import annotations

import io
import re
from enum import Enum

from PIL import Image, ImageOps
from pydantic import BaseModel, Field

from .knobs import extraction_knob

try:  # HEIC is what an iPhone actually produces
    from pillow_heif import register_heif_opener  # type: ignore

    register_heif_opener()
    HEIC_AVAILABLE = True
except ImportError:  # pragma: no cover - dependency is declared; this is belt+braces
    HEIC_AVAILABLE = False

# --- MIME constants -------------------------------------------------------- #

#: image mime -> canonical extension. These are the formats a phone or a
#: scanner actually emits; anything else is refused by name, never silently.
PAGE_PHOTO_MIMES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/heic": ".heic",
    "image/heif": ".heic",
    "image/webp": ".webp",
    "image/tiff": ".tiff",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/avif": ".avif",
}

PAGE_PHOTO_EXTENSIONS: tuple[str, ...] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".heif",
    ".webp",
    ".tiff",
    ".tif",
    ".bmp",
    ".avif",
)

# Bounds — `platform.feature_knob` rows (feature media.file_service) mirrored
# here so the package stands alone. A 400-page book photographed by hand is a
# real, ordinary case; the ceiling exists to stop a runaway, not to stop a book.
#: KNOB MIRROR of platform.feature_knob "media.file_service" "page_photos_max_photos"
MAX_PHOTOS = 1_200
#: KNOB MIRROR of platform.feature_knob "media.file_service" "page_photos_max_edge_px"
MAX_EDGE_PX = 3_200
#: KNOB MIRROR of platform.feature_knob "media.file_service" "page_photos_jpeg_quality"
JPEG_QUALITY = 82
#: A landscape photo at least this much wider than tall is treated as an open
#: book — two pages in one shot — and split down the middle.
SPREAD_ASPECT_RATIO = 1.35


class PhotoOrderBasis(str, Enum):
    explicit = "explicit"  # the person arranged them
    filename = "filename"  # natural filename order
    captured_at = "captured_at"  # EXIF DateTimeOriginal / mtime


class PagePhotosError(Exception):
    """Base for page-photo failures.

    Carries ``person_refusal`` for the same reason the ebook codec's errors do
    (see ``ebook.EbookExtractionError``): the sentence is written for the
    person holding the photo, so a pipeline that captures exceptions instead
    of raising them must re-raise this one.
    """

    person_refusal: bool = True


class UnreadablePhotoError(PagePhotosError):
    """One photo could not be opened. Named, never skipped in silence."""


class PagePhoto(BaseModel):
    """One photo on the way in."""

    file_name: str
    #: 0-based order the caller wants, when the person arranged them.
    explicit_order: int | None = None
    #: ISO-8601 capture time, when the caller already knows it.
    captured_at: str | None = None

    model_config = {"arbitrary_types_allowed": True}


class PagePhotoPage(BaseModel):
    """One page of the assembled document, back-linked to the photo it came
    from — so a rule quoted from page 37 can name the photograph."""

    number: int  # 1-based page number in the assembled document
    file_name: str
    #: For a two-page spread: ``left`` / ``right``; otherwise ``""``.
    half: str = ""
    width: int = 0
    height: int = 0
    rotated: bool = False


class PagePhotoSet(BaseModel):
    """The assembled document plus everything a person must be told about it."""

    pages: list[PagePhotoPage] = Field(default_factory=list)
    order_basis: PhotoOrderBasis = PhotoOrderBasis.filename
    #: Present when filename order and capture-time order disagree, or when
    #: anything else about the ordering deserves a sentence on screen.
    order_warning: str = ""
    spreads_split: int = 0
    heic_converted: int = 0
    truncated: bool = False
    skipped: list[str] = Field(default_factory=list)

    @property
    def page_count(self) -> int:
        return len(self.pages)


# --- ordering -------------------------------------------------------------- #

_NUMBERS = re.compile(r"(\d+)")


def natural_key(name: str) -> tuple[object, ...]:
    """``IMG_4002.jpg`` sorts before ``IMG_4010.jpg`` and page 2 before page 100."""
    parts = _NUMBERS.split(name.lower())
    return tuple(int(p) if p.isdigit() else p for p in parts)


def order_page_photos(
    photos: list[PagePhoto],
) -> tuple[list[PagePhoto], PhotoOrderBasis, str]:
    """(ordered photos, how we decided, what to tell the person)."""
    if not photos:
        return [], PhotoOrderBasis.filename, ""

    if all(p.explicit_order is not None for p in photos):
        return (
            sorted(photos, key=lambda p: p.explicit_order or 0),
            PhotoOrderBasis.explicit,
            "",
        )

    by_name = sorted(photos, key=lambda p: natural_key(p.file_name))
    timed = [p for p in photos if p.captured_at]
    if len(timed) < len(photos):
        missing = len(photos) - len(timed)
        warning = (
            f"{missing} of {len(photos)} photos have no capture time, so we put "
            "them in filename order. If that is not the page order, drag them "
            "into the right order before you upload."
            if missing and len(photos) > 1
            else ""
        )
        return by_name, PhotoOrderBasis.filename, warning

    by_time = sorted(photos, key=lambda p: (p.captured_at or "", natural_key(p.file_name)))
    if [p.file_name for p in by_time] == [p.file_name for p in by_name]:
        return by_name, PhotoOrderBasis.filename, ""

    # They disagree. Capture time is the better witness to the order a person
    # actually photographed pages in — but they are told, never overruled quietly.
    return (
        by_time,
        PhotoOrderBasis.captured_at,
        "The filenames and the times these photos were taken disagree about the "
        "page order, so we used the order you took them in. Check the first few "
        "pages, and drag them into order if that is wrong.",
    )


# --- normalization --------------------------------------------------------- #


def _open_normalised(raw: bytes, file_name: str) -> Image.Image:
    """Bytes -> an upright RGB image, with the phone's EXIF rotation applied."""
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except Exception as exc:  # noqa: BLE001 — a bad photo is named, not swallowed
        raise UnreadablePhotoError(
            f"“{file_name}” could not be opened as an image ({exc.__class__.__name__}). "
            "If it came from a phone, try sharing it as JPEG instead of HEIC."
        ) from exc
    # A phone stores the sensor's orientation in EXIF rather than rotating the
    # pixels; without this every portrait page is sideways and OCR reads nothing.
    image = ImageOps.exif_transpose(image) or image
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    max_edge = int(extraction_knob("page_photos_max_edge_px", MAX_EDGE_PX))
    if max(image.size) > max_edge:
        image.thumbnail((max_edge, max_edge), Image.LANCZOS)
    return image


def _exif_captured_at(raw: bytes) -> str | None:
    """EXIF ``DateTimeOriginal`` as ``YYYY-MM-DDTHH:MM:SS``, or None."""
    try:
        with Image.open(io.BytesIO(raw)) as image:
            exif = image.getexif()
            if not exif:
                return None
            # 36867 DateTimeOriginal, 36868 DateTimeDigitized, 306 DateTime
            for tag in (36867, 36868, 306):
                value = exif.get(tag) or exif.get_ifd(0x8769).get(tag)
                if value:
                    text = str(value).strip()
                    match = re.match(
                        r"^(\d{4})[:\-](\d{2})[:\-](\d{2})[ T](\d{2}:\d{2}:\d{2})", text
                    )
                    if match:
                        y, m, d, t = match.groups()
                        return f"{y}-{m}-{d}T{t}"
    except Exception:  # noqa: BLE001 — EXIF is optional, never fatal
        return None
    return None


def read_captured_at(raw: bytes) -> str | None:
    """Public: the capture time of these photo bytes, or None."""
    return _exif_captured_at(raw)


def _split_spread(image: Image.Image) -> list[tuple[Image.Image, str]]:
    """An open book photographed in one landscape shot is two pages."""
    width, height = image.size
    if height and width / height >= SPREAD_ASPECT_RATIO:
        middle = width // 2
        return [
            (image.crop((0, 0, middle, height)), "left"),
            (image.crop((middle, 0, width, height)), "right"),
        ]
    return [(image, "")]


# --- assembly -------------------------------------------------------------- #


def photos_to_pdf(
    photos: list[tuple[PagePhoto, bytes]],
    *,
    split_spreads: bool = True,
) -> tuple[bytes, PagePhotoSet]:
    """Ordered photos -> (one PDF's bytes, what we did and what to say).

    The PDF is the platform's existing page/OCR contract: from here the stack
    of photos is read by exactly the same reader a scanned PDF has always used.
    An unreadable photo is named in ``skipped`` and the rest of the book still
    goes in — one bad shot never costs 399 good pages."""
    from matrx_files._extras import require

    pymupdf = require("pymupdf", "pdf", "Page photos to PDF")  # here, so the codec imports without it

    max_photos = int(extraction_knob("page_photos_max_photos", MAX_PHOTOS))
    quality = int(extraction_knob("page_photos_jpeg_quality", JPEG_QUALITY))

    # Fill in capture times we can read ourselves, so ordering has a witness.
    enriched: list[tuple[PagePhoto, bytes]] = []
    for photo, raw in photos:
        if photo.captured_at is None:
            photo = photo.model_copy(update={"captured_at": _exif_captured_at(raw)})
        enriched.append((photo, raw))

    ordered_meta, basis, warning = order_page_photos([p for p, _ in enriched])
    by_name = {p.file_name: raw for p, raw in enriched}

    truncated = False
    if len(ordered_meta) > max_photos:
        ordered_meta = ordered_meta[:max_photos]
        truncated = True

    document = pymupdf.open()
    result = PagePhotoSet(order_basis=basis, order_warning=warning, truncated=truncated)
    if truncated:
        extra = (
            f" Only the first {max_photos} photos were used; the rest are not in "
            "this document."
        )
        result.order_warning = (result.order_warning + extra).strip()

    for photo in ordered_meta:
        raw = by_name.get(photo.file_name)
        if raw is None:
            continue
        lowered = photo.file_name.lower()
        try:
            image = _open_normalised(raw, photo.file_name)
        except UnreadablePhotoError as exc:
            result.skipped.append(str(exc))
            continue
        if lowered.endswith((".heic", ".heif")):
            result.heic_converted += 1

        halves = _split_spread(image) if split_spreads else [(image, "")]
        if len(halves) > 1:
            result.spreads_split += 1
        for half_image, half in halves:
            buffer = io.BytesIO()
            half_image.convert("RGB").save(
                buffer, format="JPEG", quality=quality, optimize=True
            )
            data = buffer.getvalue()
            width, height = half_image.size
            page = document.new_page(width=width, height=height)
            page.insert_image(pymupdf.Rect(0, 0, width, height), stream=data)
            result.pages.append(
                PagePhotoPage(
                    number=len(result.pages) + 1,
                    file_name=photo.file_name,
                    half=half,
                    width=width,
                    height=height,
                    rotated=False,
                )
            )

    if not result.pages:
        document.close()
        raise UnreadablePhotoError(
            "None of these photos could be read. "
            + (" ".join(result.skipped) if result.skipped else "")
        )

    out = document.tobytes()
    document.close()
    return out, result


def is_page_photo(mime_type: str | None, file_name: str | None) -> bool:
    """True when this file is a photograph/scan we turn into pages."""
    if mime_type:
        mime = mime_type.lower().split(";", 1)[0].strip()
        if mime in PAGE_PHOTO_MIMES:
            return True
    name = (file_name or "").lower()
    return name.endswith(PAGE_PHOTO_EXTENSIONS)


__all__ = [
    "HEIC_AVAILABLE",
    "JPEG_QUALITY",
    "MAX_EDGE_PX",
    "MAX_PHOTOS",
    "PAGE_PHOTO_EXTENSIONS",
    "PAGE_PHOTO_MIMES",
    "SPREAD_ASPECT_RATIO",
    "PagePhoto",
    "PagePhotoPage",
    "PagePhotoSet",
    "PagePhotosError",
    "PhotoOrderBasis",
    "UnreadablePhotoError",
    "is_page_photo",
    "natural_key",
    "order_page_photos",
    "photos_to_pdf",
    "read_captured_at",
]
