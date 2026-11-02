"""The optional extras: heavy dependencies a capability needs, installed only by the hosts that use it.

The base ``matrx-files`` install is the file service's core (storage, sharing, images through
Pillow, PDF rendering through pypdfium2, Office codecs). The heavy native stacks are extras, so a
slim host (Matrx 2's tools service, a scraper) does not carry hundreds of MB it never runs:

  matrx-files[pdf]    PyMuPDF: PDF manipulation (merge/split/redact/compress), page photos -> PDF
  matrx-files[ocr]    pytesseract: OCR of scanned pages (also needs the `tesseract` binary)
  matrx-files[media]  rembg + onnxruntime (background removal), OpenCV + NumPy (inpaint, document
                      detection, video frames/probes), imageio-ffmpeg (video composition),
                      pillow-heif / pillow-avif-plugin (HEIC and AVIF images)
  matrx-files[all]    every extra (the platform server installs this)

Every import of an extra's module goes through :func:`require` at the point of use, so a missing
extra fails loudly, naming the extra to install, and never at ``import matrx_files``.
"""

from __future__ import annotations

from types import ModuleType

from matrx_utils.module_loading import load_declared_module

EXTRAS: dict[str, tuple[str, ...]] = {
    "pdf": ("pymupdf",),
    "ocr": ("pytesseract",),
    "media": ("rembg", "onnxruntime", "cv2", "numpy", "imageio_ffmpeg", "pillow_heif", "pillow_avif"),
}


class MissingExtraError(ImportError):
    """A capability needs an optional extra that is not installed. Still an ``ImportError``, so every
    existing ``except ImportError`` availability check keeps working."""

    def __init__(self, extra: str, module: str, feature: str) -> None:
        self.extra = extra
        self.module_name = module
        super().__init__(
            f"{feature} needs the matrx-files[{extra}] extra (module `{module}` is not installed). "
            f"Install it with: pip install 'matrx-files[{extra}]'",
            name=module,
        )


def missing_extra_message(extra: str, module: str, feature: str) -> str:
    return str(MissingExtraError(extra, module, feature))


def require(module: str, extra: str, feature: str) -> ModuleType:
    """Import ``module`` (part of ``matrx-files[extra]``) or raise :class:`MissingExtraError`."""
    try:
        return load_declared_module(module)
    except ImportError as exc:
        raise MissingExtraError(extra, module, feature) from exc
