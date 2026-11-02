"""PDF compression with five quality tiers and an optional hard size cap.

The two knobs are independent:

- ``level`` (1-5) — the *quality* tier. Higher number = more aggressive
  reduction. Tiers 1-4 do in-place image recompression (preserves text,
  links, annotations); tier 5 falls back to **per-page rasterization**
  (re-renders each page as a JPEG image at low DPI, throwing away text
  and links). Rasterization is the "always-works" strategy — it shrinks
  scanned PDFs, JBIG2/JPX-encoded pages, and SMask-laden documents that
  in-place recompression silently skips.

- ``max_size_bytes`` (optional) — an *absolute* upper bound on the
  output. When the requested level produces a file larger than this
  cap, the caller's iteration loop bumps to the next level. Levels are
  walked sequentially so the smallest level that meets the cap wins;
  if even tier 5 can't satisfy the cap, the best attempt is returned
  with ``cap_satisfied=False``.

In-place strategy notes:
- Streams are written with ``compress=False`` because the bytes are
  already JPEG. Letting PyMuPDF deflate them and then overriding
  ``/Filter`` to ``/DCTDecode`` produces a Flate(JPEG) stream that
  declares itself as raw JPEG — Adobe rejects this with a "problem
  reading this document" dialog.
- ``/Width`` and ``/Height`` are always rewritten to match the new
  JPEG's dimensions; otherwise readers complain with "Insufficient
  data for an image."
- Image-mask, stencil-mask, soft-mask, and indexed-palette images are
  skipped (re-encoding any of these as DCTDecode RGB produces an
  invalid PDF object). On heavily-scanned PDFs this can mean *every*
  image gets skipped — that's why tier 5 rasterizes instead.

Rasterization strategy notes:
- Each source page is rendered to an RGB pixmap at ``raster_dpi``,
  JPEG-compressed at ``raster_quality``, and placed on a fresh page
  with the same MediaBox as the source.
- This drops the text layer, links, annotations, form fields, and
  bookmarks. Pages with a lot of small fonts may become slightly
  fuzzy at 100 DPI. Users opt into this by selecting tier 5
  (or by setting a tight ``max_size_bytes`` that forces escalation
  to tier 5).
"""

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Literal

from PIL import Image

from ..concurrency import run_in_cpu_executor
from ..internal import load_pymupdf

CompressStrategy = Literal["inplace", "raster"]


@dataclass(frozen=True)
class CompressTier:
    level: int
    strategy: CompressStrategy

    # In-place strategy parameters (ignored when strategy=="raster"):
    recompress_images: bool
    jpeg_quality: int
    scale: float            # multiplied against image width/height; 1.0 = no resize
    min_image_width: int    # only recompress images at least this wide (px)

    # Raster strategy parameters (ignored when strategy=="inplace"):
    raster_dpi: int
    raster_quality: int

    # Always applied:
    strip_metadata: bool
    garbage: int            # PDF garbage-collection level passed to doc.tobytes


# Five tiers with explicit strategy + parameter tables. Tweak with
# measurements, not vibes — see the smoke tests in this file's neighbour.
TIERS: dict[int, CompressTier] = {
    1: CompressTier(
        level=1, strategy="inplace",
        recompress_images=False, jpeg_quality=0,  scale=1.00, min_image_width=0,
        raster_dpi=0, raster_quality=0,
        strip_metadata=False, garbage=3,
    ),
    2: CompressTier(
        level=2, strategy="inplace",
        recompress_images=True, jpeg_quality=85, scale=1.00, min_image_width=1500,
        raster_dpi=0, raster_quality=0,
        strip_metadata=False, garbage=4,
    ),
    3: CompressTier(
        level=3, strategy="inplace",
        recompress_images=True, jpeg_quality=78, scale=0.66, min_image_width=500,
        raster_dpi=0, raster_quality=0,
        strip_metadata=False, garbage=4,
    ),
    4: CompressTier(
        level=4, strategy="inplace",
        recompress_images=True, jpeg_quality=60, scale=0.50, min_image_width=300,
        raster_dpi=0, raster_quality=0,
        strip_metadata=False, garbage=4,
    ),
    5: CompressTier(
        level=5, strategy="raster",
        recompress_images=False, jpeg_quality=0, scale=1.00, min_image_width=0,
        raster_dpi=110, raster_quality=55,
        strip_metadata=True, garbage=4,
    ),
}

MIN_LEVEL = min(TIERS)
MAX_LEVEL = max(TIERS)


# ---------------------------------------------------------------------------
# In-place image recompression
# ---------------------------------------------------------------------------


def _has_key(doc, xref: int, key: str) -> bool:
    key_type, _ = doc.xref_get_key(xref, key)
    return key_type != "null"


def _bool_key_is_true(doc, xref: int, key: str) -> bool:
    key_type, key_val = doc.xref_get_key(xref, key)
    return key_type == "bool" and key_val.lower() == "true"


def _is_indexed_colorspace(doc, xref: int) -> bool:
    cs_type, cs_val = doc.xref_get_key(xref, "ColorSpace")
    if cs_type == "name" and cs_val == "/Indexed":
        return True
    if cs_type == "array" and "/Indexed" in cs_val:
        return True
    return False


def _recompress_image_xref(doc, xref: int, pymupdf, tier: CompressTier) -> bool:
    """Recompress one image stream in place. Returns True on success."""
    if _bool_key_is_true(doc, xref, "ImageMask"):
        return False
    if _has_key(doc, xref, "SMask") or _has_key(doc, xref, "Mask"):
        return False
    if _is_indexed_colorspace(doc, xref):
        return False

    try:
        pix = pymupdf.Pixmap(doc, xref)
    except Exception:
        return False

    try:
        if pix.width < tier.min_image_width:
            return False
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        if pix.colorspace is not None and pix.colorspace.n not in (1, 3):
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)

        mode = "L" if pix.n == 1 else "RGB"
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        if tier.scale < 1.0:
            new_size = (
                max(int(pix.width * tier.scale), 1),
                max(int(pix.height * tier.scale), 1),
            )
            img = img.resize(new_size, Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=tier.jpeg_quality, optimize=True)
        jpeg_bytes = buf.getvalue()

        doc.update_stream(xref, jpeg_bytes, new=False, compress=False)
        doc.xref_set_key(xref, "Filter", "/DCTDecode")
        doc.xref_set_key(xref, "Width", str(img.width))
        doc.xref_set_key(xref, "Height", str(img.height))
        doc.xref_set_key(
            xref,
            "ColorSpace",
            "/DeviceGray" if mode == "L" else "/DeviceRGB",
        )
        doc.xref_set_key(xref, "BitsPerComponent", "8")
        for stale_key in ("Decode", "DecodeParms", "Predictor"):
            doc.xref_set_key(xref, stale_key, "null")
        return True
    finally:
        pix = None


@dataclass(frozen=True)
class _InplaceStats:
    images_seen: int
    images_recompressed: int


def _compress_inplace(pdf_bytes: bytes, tier: CompressTier) -> tuple[bytes, _InplaceStats]:
    pymupdf = load_pymupdf()
    seen = 0
    recompressed = 0
    with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
        if tier.recompress_images:
            seen_xrefs: set[int] = set()
            for page in doc:
                for img_info in page.get_images(full=True):
                    xref = img_info[0]
                    if xref in seen_xrefs:
                        continue
                    seen_xrefs.add(xref)
                    seen += 1
                    if _recompress_image_xref(doc, xref, pymupdf, tier):
                        recompressed += 1

        if tier.strip_metadata:
            doc.set_metadata({})

        return (
            doc.tobytes(garbage=tier.garbage, deflate=True),
            _InplaceStats(images_seen=seen, images_recompressed=recompressed),
        )


# ---------------------------------------------------------------------------
# Page rasterization
# ---------------------------------------------------------------------------


def _compress_by_rasterization(pdf_bytes: bytes, tier: CompressTier) -> bytes:
    """Render every page to a JPEG and rebuild the PDF.

    Drops text layers, links, annotations, form fields. Use only when
    in-place strategies aren't shrinking enough (tier 5 by default).
    """
    pymupdf = load_pymupdf()
    src = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    out = pymupdf.open()
    try:
        for page in src:
            pix = page.get_pixmap(
                dpi=tier.raster_dpi,
                alpha=False,
                colorspace=pymupdf.csRGB,
            )
            jpeg = pix.tobytes("jpeg", jpg_quality=tier.raster_quality)
            new_page = out.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, stream=jpeg)
            pix = None

        if tier.strip_metadata:
            out.set_metadata({})

        return out.tobytes(garbage=tier.garbage, deflate=True)
    finally:
        out.close()
        src.close()


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CompressResult:
    """Outcome of a capped compression run.

    Fields:
        content:              the compressed PDF bytes.
        level_used:           tier that ultimately produced ``content``.
        cap_satisfied:        True when ``max_size_bytes`` was satisfied
                              (or no cap was specified). False when even
                              ``MAX_LEVEL`` exceeds the cap.
        strategy_used:        "inplace" or "raster" — which path produced
                              ``content`` (matches ``TIERS[level_used].strategy``).
        images_seen:          number of unique image xrefs visited during
                              the in-place pass. 0 for raster runs.
        images_recompressed:  number of images actually re-encoded
                              (skips: SMask/Mask/ImageMask/indexed/tiny).
                              0 for raster runs.
    """

    content: bytes
    level_used: int
    cap_satisfied: bool
    strategy_used: CompressStrategy
    images_seen: int = 0
    images_recompressed: int = 0


def _clamp_level(level: int) -> int:
    if level < MIN_LEVEL:
        return MIN_LEVEL
    if level > MAX_LEVEL:
        return MAX_LEVEL
    return level


def _run_tier(pdf_bytes: bytes, tier: CompressTier) -> tuple[bytes, _InplaceStats]:
    if tier.strategy == "raster":
        return _compress_by_rasterization(pdf_bytes, tier), _InplaceStats(0, 0)
    return _compress_inplace(pdf_bytes, tier)


def compress_pdf_bytes(pdf_bytes: bytes, level: int = 2) -> bytes:
    """Compress at exactly the requested ``level`` (1..5).

    Use ``compress_pdf_bytes_capped`` when you also have an absolute
    size ceiling and want the smallest level that fits.
    """
    tier = TIERS[_clamp_level(level)]
    content, _ = _run_tier(pdf_bytes, tier)
    return content


def compress_pdf_bytes_capped(
    pdf_bytes: bytes,
    *,
    level: int = 2,
    max_size_bytes: int | None = None,
) -> CompressResult:
    """Compress starting at ``level`` and escalate one tier at a time
    until either the output fits in ``max_size_bytes`` or ``MAX_LEVEL``
    is reached.

    ``max_size_bytes=None`` honors the requested level exactly. The
    level is a *minimum* — we never go below it even if the source
    file is already under the cap, because the caller explicitly asked
    for that quality tier.
    """
    start = _clamp_level(level)
    best_level = start
    best_tier = TIERS[start]
    best_content, best_stats = _run_tier(pdf_bytes, best_tier)

    # Iteration only kicks in when the starting tier missed the cap.
    # We escalate one tier at a time but ALWAYS keep the smallest output
    # we've seen so far — this matters because tier 5 (raster) is not
    # guaranteed to be smaller than tier 4 (inplace) on every PDF (a
    # clean image-bearing PDF can compress better with inplace+downscale
    # than with raster). Without this, jumping from a satisfying tier to
    # the next would risk returning a larger file.
    if max_size_bytes is not None and max_size_bytes > 0:
        cur_level = start
        while len(best_content) > max_size_bytes and cur_level < MAX_LEVEL:
            cur_level += 1
            cur_tier = TIERS[cur_level]
            cur_content, cur_stats = _run_tier(pdf_bytes, cur_tier)
            if len(cur_content) < len(best_content):
                best_content = cur_content
                best_stats = cur_stats
                best_tier = cur_tier
                best_level = cur_level

    cap_satisfied = max_size_bytes is None or len(best_content) <= max_size_bytes
    return CompressResult(
        content=best_content,
        level_used=best_level,
        cap_satisfied=cap_satisfied,
        strategy_used=best_tier.strategy,
        images_seen=best_stats.images_seen,
        images_recompressed=best_stats.images_recompressed,
    )


async def compress_pdf_bytes_async(pdf_bytes: bytes, level: int = 2) -> bytes:
    return await run_in_cpu_executor(compress_pdf_bytes, pdf_bytes, level)


async def compress_pdf_bytes_capped_async(
    pdf_bytes: bytes,
    *,
    level: int = 2,
    max_size_bytes: int | None = None,
) -> CompressResult:
    return await run_in_cpu_executor(
        lambda pb: compress_pdf_bytes_capped(pb, level=level, max_size_bytes=max_size_bytes),
        pdf_bytes,
    )


__all__ = [
    "CompressTier",
    "CompressResult",
    "CompressStrategy",
    "TIERS",
    "MIN_LEVEL",
    "MAX_LEVEL",
    "compress_pdf_bytes",
    "compress_pdf_bytes_async",
    "compress_pdf_bytes_capped",
    "compress_pdf_bytes_capped_async",
]
