"""Image metadata (EXIF / GPS / container) reading — REPORT, never interpret.

``read_image_metadata(image_bytes)`` decodes an image's embedded metadata and
returns a flat, JSON-safe report: camera make/model, capture timestamps, GPS
coordinates in signed decimal degrees, the software tag, pixel dimensions, which
metadata containers are present, and the full raw tag table.

**Why this is a matrx-files primitive and not a caller's helper.** "What does
this image say about itself" is a file-handling fact, not one feature's need.
The verification desk asks it of a suspect photo, an intake pipeline asks it of
a phone upload, an asset library asks it to sort by capture date. One decoder,
one vocabulary, one place where the Pillow quirks below are already solved.

**The stripped signal is factual, never a verdict.** Every major social network
re-encodes uploads and drops EXIF, so "no EXIF on a JPEG" is a real, reportable
observation — and it is ONLY an observation. This module never says an image is
fake, edited, or laundered. ``metadata_stripped`` is ``True`` only when the
format normally carries EXIF and none survived, ``False`` when EXIF is present,
and ``None`` when the format does not normally carry EXIF at all (PNG, WebP,
GIF) — because there the absence means nothing and a ``False``/``True`` there
would be a lie dressed as data. ``stripped_note`` always says which of the three
happened, in words.

Earned traps:

* **Pillow's ``getexif()`` is not the whole table.** The maker/model/software
  tags live in IFD0, but the capture timestamps, lens and most of what a camera
  writes live in the **Exif IFD** (tag 0x8769) and GPS lives in the **GPS IFD**
  (0x8825). Reading only the top level silently returns an image with "no
  DateTimeOriginal" on a photo that plainly has one.
* **GPS is stored as unsigned DMS plus a hemisphere letter.** Converting
  without applying ``S``/``W`` as a negative sign puts every southern and
  western photo in the wrong hemisphere.
* **EXIF values are not JSON.** Rationals, bytes, undefined-type blobs and
  nested dicts all appear; everything is coerced through ``_jsonable`` so the
  table can cross a wire without a serializer exploding at the boundary.
* **EXIF datetimes are ``YYYY:MM:DD HH:MM:SS``**, not ISO-8601. Both the raw
  string and the parsed ISO form are returned; unparseable stays ``None``
  rather than becoming a guess.
"""

from __future__ import annotations

import io
from datetime import datetime
from fractions import Fraction
from typing import Any

from PIL import ExifTags, Image

try:  # pragma: no cover - environment-dependent
    from pillow_heif import register_heif_opener  # type: ignore

    register_heif_opener()
except ImportError:  # pragma: no cover
    pass

#: Formats that normally carry EXIF. Absence of EXIF in one of these is a real
#: observation; absence in anything else is simply how the format works.
EXIF_BEARING_FORMATS: frozenset[str] = frozenset(
    {"JPEG", "JPEG2000", "MPO", "TIFF", "HEIF", "HEIC", "AVIF", "DNG", "WEBP"}
)

#: Cap on how many raw tags ride back, so a pathological file cannot return a
#: multi-megabyte table into a workflow channel or an agent's context.
MAX_RAW_TAGS = 400

#: Cap on a single stringified tag value.
MAX_TAG_VALUE_CHARS = 512

_TAG_NAMES: dict[int, str] = dict(ExifTags.TAGS)
_GPS_TAG_NAMES: dict[int, str] = dict(ExifTags.GPSTAGS)


def _jsonable(value: Any, *, depth: int = 0) -> Any:
    """Coerce an EXIF value into something ``json.dumps`` accepts."""
    if value is None or isinstance(value, bool | int | float | str):
        if isinstance(value, str) and len(value) > MAX_TAG_VALUE_CHARS:
            return value[:MAX_TAG_VALUE_CHARS] + "…"
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            return None
        return value
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace").strip("\x00").strip()
        if len(text) > MAX_TAG_VALUE_CHARS:
            text = text[:MAX_TAG_VALUE_CHARS] + "…"
        return text or f"<{len(value)} bytes>"
    if isinstance(value, Fraction):
        return float(value) if value.denominator else None
    if hasattr(value, "numerator") and hasattr(value, "denominator"):  # IFDRational
        try:
            return float(value)
        except (ZeroDivisionError, ValueError):
            return None
    if depth >= 3:
        return str(value)[:MAX_TAG_VALUE_CHARS]
    if isinstance(value, tuple | list):
        return [_jsonable(v, depth=depth + 1) for v in value[:64]]
    if isinstance(value, dict):
        return {str(k): _jsonable(v, depth=depth + 1) for k, v in list(value.items())[:64]}
    return str(value)[:MAX_TAG_VALUE_CHARS]


def _clean_str(value: Any) -> str | None:
    text = _jsonable(value)
    if not isinstance(text, str):
        return None
    text = text.strip().strip("\x00").strip()
    return text or None


def _parse_exif_datetime(raw: Any, offset: Any = None) -> str | None:
    """``'2026:09:10 14:03:22'`` → ISO-8601. Never guesses."""
    text = _clean_str(raw)
    if not text:
        return None
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            parsed = datetime.strptime(text.split(".")[0], fmt)
        except ValueError:
            continue
        iso = parsed.isoformat()
        tz = _clean_str(offset)
        if tz and (tz.startswith("+") or tz.startswith("-")) and len(tz) >= 5:
            iso = f"{iso}{tz}"
        return iso
    return None


def _dms_to_degrees(dms: Any, ref: Any) -> float | None:
    """Unsigned degrees/minutes/seconds + hemisphere letter → signed decimal."""
    if not isinstance(dms, tuple | list) or len(dms) != 3:
        return None
    try:
        degrees, minutes, seconds = (float(part) for part in dms)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    value = degrees + minutes / 60.0 + seconds / 3600.0
    hemisphere = (_clean_str(ref) or "").upper()[:1]
    if hemisphere in ("S", "W"):
        value = -value
    if hemisphere in ("N", "S") and not -90.0 <= value <= 90.0:
        return None
    if hemisphere in ("E", "W") and not -180.0 <= value <= 180.0:
        return None
    return round(value, 7)


def _collect_tags(image: Image.Image) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return (flat named tag table, exif-ifd-by-id, gps-ifd-by-id).

    The flat table merges IFD0 and the Exif IFD under human tag names; the
    by-id dicts are what the field extractors below read, because a name
    lookup can miss on a tag Pillow's table does not carry.
    """
    exif = image.getexif()
    flat: dict[str, Any] = {}
    exif_ifd: dict[int, Any] = {}
    gps_ifd: dict[int, Any] = {}
    if not exif:
        return flat, exif_ifd, gps_ifd

    for tag_id, value in exif.items():
        if tag_id in (0x8769, 0x8825, 0xA005):  # sub-IFD pointers, expanded below
            continue
        flat[_TAG_NAMES.get(tag_id, f"Tag{tag_id:#06x}")] = _jsonable(value)

    try:
        exif_ifd = dict(exif.get_ifd(0x8769))
    except Exception:  # noqa: BLE001 — a mangled Exif IFD must not kill the read
        exif_ifd = {}
    for tag_id, value in exif_ifd.items():
        flat.setdefault(_TAG_NAMES.get(tag_id, f"Tag{tag_id:#06x}"), _jsonable(value))

    try:
        gps_ifd = dict(exif.get_ifd(0x8825))
    except Exception:  # noqa: BLE001
        gps_ifd = {}
    for tag_id, value in gps_ifd.items():
        # GPSTAGS names already start with "GPS" (GPSLatitude, ...); only the
        # unnamed fallback needs the prefix, or the table reads "GPSGPSLatitude".
        name = _GPS_TAG_NAMES.get(tag_id)
        flat.setdefault(name or f"GPSTag{tag_id:#06x}", _jsonable(value))

    return flat, {int(k): v for k, v in exif_ifd.items()}, {int(k): v for k, v in gps_ifd.items()}


def read_image_metadata(image_bytes: bytes) -> dict[str, Any]:
    """Decode an image's embedded metadata. Reports facts; draws no conclusions.

    Raises ``ValueError`` when the bytes are not a decodable image — an
    undecodable file is a failure, never a report full of ``None`` that reads
    like "this image has no metadata".
    """
    if not image_bytes:
        raise ValueError("read_image_metadata: empty byte string — nothing to decode.")
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
    except Exception as exc:  # noqa: BLE001 — re-raised as one actionable error
        raise ValueError(
            f"read_image_metadata: could not decode these bytes as an image "
            f"({type(exc).__name__}: {exc})."
        ) from exc

    fmt = (image.format or "").upper() or None
    flat, exif_ifd, gps_ifd = _collect_tags(image)
    info = image.info or {}

    containers = {
        "exif": bool(flat),
        "xmp": bool(info.get("xmp") or info.get("XML:com.adobe.xmp")),
        "iptc": bool(info.get("photoshop") or info.get("iptc")),
        "icc_profile": bool(info.get("icc_profile")),
        "png_text": bool(
            [k for k, v in info.items() if isinstance(v, str) and k not in ("xmp", "comment")]
        )
        if fmt == "PNG"
        else False,
        "comment": bool(info.get("comment")),
    }

    if flat:
        stripped: bool | None = False
        note = f"EXIF metadata is present ({len(flat)} tags)."
    elif fmt in EXIF_BEARING_FORMATS:
        stripped = True
        note = (
            f"No EXIF metadata at all, in a {fmt} file — a format that normally carries it. "
            "Re-encoding by a social network, a screenshot, a messaging app, or a "
            "deliberate strip all produce this. It is an observation, not a verdict."
        )
    else:
        stripped = None
        note = (
            f"{fmt or 'This format'} does not normally carry EXIF, so its absence here "
            "says nothing either way."
        )

    def exif_str(*tag_ids: int) -> str | None:
        for tag_id in tag_ids:
            found = _clean_str(exif_ifd.get(tag_id))
            if found:
                return found
        name_lookup = {tid: _TAG_NAMES.get(tid) for tid in tag_ids}
        for name in name_lookup.values():
            if name and (found := _clean_str(flat.get(name))):
                return found
        return None

    datetime_original = _parse_exif_datetime(
        exif_ifd.get(0x9003) or flat.get("DateTimeOriginal"),
        exif_ifd.get(0x9011) or flat.get("OffsetTimeOriginal"),
    )
    datetime_digitized = _parse_exif_datetime(exif_ifd.get(0x9004) or flat.get("DateTimeDigitized"))
    datetime_modified = _parse_exif_datetime(flat.get("DateTime"))

    latitude = _dms_to_degrees(gps_ifd.get(2), gps_ifd.get(1))
    longitude = _dms_to_degrees(gps_ifd.get(4), gps_ifd.get(3))
    altitude = None
    if gps_ifd.get(6) is not None:
        raw_alt = _jsonable(gps_ifd.get(6))
        if isinstance(raw_alt, int | float):
            altitude = round(float(raw_alt) * (-1.0 if _jsonable(gps_ifd.get(5)) == 1 else 1.0), 3)

    orientation_raw = _jsonable(flat.get("Orientation"))

    raw_tags = dict(list(flat.items())[:MAX_RAW_TAGS])

    return {
        "format": fmt,
        "mime_type": Image.MIME.get(image.format or "", None),
        "width": int(image.width),
        "height": int(image.height),
        "color_mode": image.mode,
        "frame_count": int(getattr(image, "n_frames", 1) or 1),
        "camera_make": _clean_str(flat.get("Make")),
        "camera_model": _clean_str(flat.get("Model")),
        "lens_model": exif_str(0xA434),
        "software": _clean_str(flat.get("Software")),
        "artist": _clean_str(flat.get("Artist")),
        "copyright": _clean_str(flat.get("Copyright")),
        "image_description": _clean_str(flat.get("ImageDescription")),
        "datetime_original": datetime_original,
        "datetime_original_text": _clean_str(exif_ifd.get(0x9003) or flat.get("DateTimeOriginal")),
        "datetime_digitized": datetime_digitized,
        "datetime_modified": datetime_modified,
        "orientation": orientation_raw if isinstance(orientation_raw, int) else None,
        "gps_latitude": latitude,
        "gps_longitude": longitude,
        "gps_altitude_m": altitude,
        "gps_timestamp": _clean_str(gps_ifd.get(29)),
        "has_exif": bool(flat),
        "metadata_stripped": stripped,
        "stripped_note": note,
        "containers": containers,
        "tag_count": len(flat),
        "raw_tags": raw_tags,
        "raw_tags_truncated": len(flat) > MAX_RAW_TAGS,
    }


__all__ = [
    "EXIF_BEARING_FORMATS",
    "MAX_RAW_TAGS",
    "read_image_metadata",
]
