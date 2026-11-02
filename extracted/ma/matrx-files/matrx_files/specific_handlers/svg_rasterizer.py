"""SVG-as-master rasterization.

Lets ``preset='logo'`` (and any future preset that wants vector inputs)
accept SVG uploads. The SVG is persisted as the master without modification;
when variants are rendered, the SVG is rasterized to a single high-resolution
PNG, then handed to the normal Pillow pipeline so every existing resize /
normalize / save code path applies unchanged.

Backend: librsvg's ``rsvg-convert`` binary. Faster + better SVG spec coverage
than the pure-Python alternatives, and it ships in every major Linux distro
(``apt install librsvg2-bin``) and Homebrew (``brew install librsvg``).

Graceful degrade: if the binary is missing the rasterizer raises
:class:`SvgRasterizerUnavailable` and callers should skip variant rendering
for SVG masters (the SVG itself still persists as the master).
"""

from __future__ import annotations

import shutil
import subprocess


class SvgRasterizerUnavailable(RuntimeError):
    """Raised when rsvg-convert is not installed in PATH."""


_RSVG_BIN: str | None = None
_RSVG_CHECKED: bool = False


def _rsvg_path() -> str | None:
    """One-time PATH lookup; cached for the lifetime of the process."""
    global _RSVG_BIN, _RSVG_CHECKED
    if not _RSVG_CHECKED:
        _RSVG_BIN = shutil.which("rsvg-convert")
        _RSVG_CHECKED = True
    return _RSVG_BIN


# Magic-number signatures for the common raster formats. If the bytes open
# with any of these, the payload is definitively NOT an SVG — even if a
# ``<svg`` substring appears later (e.g. inside a PNG tEXt chunk, JPEG EXIF,
# or embedded thumbnail). Checking these first kills the false-positive that
# routed raster images into rsvg-convert and produced exit-status-1 failures.
_RASTER_MAGIC: tuple[bytes, ...] = (
    b"\x89PNG\r\n\x1a\n",  # PNG
    b"\xff\xd8\xff",  # JPEG
    b"GIF87a",  # GIF
    b"GIF89a",  # GIF
    b"BM",  # BMP
    b"II*\x00",  # TIFF (little-endian)
    b"MM\x00*",  # TIFF (big-endian)
)


def is_svg(image_bytes: bytes, *, mime_hint: str | None = None) -> bool:
    """Best-effort SVG detection.

    Sniffs the first ~512 bytes for an ``<svg`` tag. The mime_hint
    (typically ``image/svg+xml`` from media_sniff) is consulted first;
    when missing we fall back to content sniffing because PIL will
    happily try to open SVG as PNG and explode three frames deeper.

    Raster magic numbers are checked BEFORE the ``<svg`` substring scan so a
    binary image carrying ``<svg`` in its metadata is never misclassified.
    A raster mime_hint is likewise authoritative.
    """
    if mime_hint:
        hint = mime_hint.lower()
        if "svg" in hint:
            return True
        if hint.startswith("image/") and hint not in ("image/svg+xml",):
            return False
    if image_bytes[:16].startswith(_RASTER_MAGIC):
        return False
    # RIFF....WEBP (WebP) — 4-byte RIFF, 4-byte size, then WEBP.
    if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return False
    head = image_bytes[:512].lstrip()
    # Skip XML prolog / BOM / DOCTYPE if present.
    lower = head.lower()
    return b"<svg" in lower[:512]


def is_available() -> bool:
    """True iff rsvg-convert is on PATH and callable."""
    return _rsvg_path() is not None


_SUPPORTS_BG_COLOR: bool | None = None


def _supports_background_color(binary: str) -> bool:
    """One-time probe: does this rsvg-convert accept ``--background-color``?

    The flag was added in librsvg ~2.54. Older builds (e.g. Debian's
    ``librsvg2-bin`` on bullseye/2.50) reject it and exit non-zero with no
    PNG output — which surfaced in production as a generic exit-status-1
    failure on every SVG upload. We probe ``--help`` once and cache the
    answer so the common path stays a single subprocess call.
    """
    global _SUPPORTS_BG_COLOR
    if _SUPPORTS_BG_COLOR is None:
        try:
            help_proc = subprocess.run(
                [binary, "--help"],
                capture_output=True,
                timeout=5.0,
                check=False,
            )
            help_text = (help_proc.stdout or b"") + (help_proc.stderr or b"")
            _SUPPORTS_BG_COLOR = b"--background-color" in help_text
        except Exception:
            # If the probe itself fails, assume unsupported — the flag is a
            # nicety (transparent flatten), not required for a valid render.
            _SUPPORTS_BG_COLOR = False
    return _SUPPORTS_BG_COLOR


def rasterize_svg_to_png(
    svg_bytes: bytes,
    *,
    width: int,
    height: int,
    timeout_seconds: float = 10.0,
) -> bytes:
    """Rasterize ``svg_bytes`` to a PNG of the requested dimensions.

    Raises :class:`SvgRasterizerUnavailable` when rsvg-convert is missing,
    and :class:`subprocess.CalledProcessError` when the binary errors out
    (e.g. malformed SVG). On a ``CalledProcessError`` the captured stderr is
    re-attached to the raised exception so callers/logs see the real reason.

    Resilient to older librsvg builds: ``--background-color`` (librsvg ~2.54+)
    is only passed when the installed binary advertises support for it.
    """
    binary = _rsvg_path()
    if binary is None:
        raise SvgRasterizerUnavailable(
            "rsvg-convert not found on PATH. Install librsvg "
            "(apt install librsvg2-bin / brew install librsvg) "
            "to enable SVG-as-master support."
        )
    args = [
        binary,
        "--format=png",
        f"--width={int(width)}",
        f"--height={int(height)}",
        "--keep-aspect-ratio",
    ]
    if _supports_background_color(binary):
        args.append("--background-color=transparent")

    proc = subprocess.run(
        args,
        input=svg_bytes,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    if proc.returncode != 0:
        stderr_txt = (proc.stderr or b"").decode("utf-8", "replace").strip()
        raise subprocess.CalledProcessError(
            proc.returncode, args, output=proc.stdout, stderr=proc.stderr or stderr_txt.encode()
        )
    return proc.stdout


__all__ = [
    "SvgRasterizerUnavailable",
    "is_svg",
    "is_available",
    "rasterize_svg_to_png",
]
