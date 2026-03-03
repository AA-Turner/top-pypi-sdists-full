"""Segmentation response models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    import numpy as np
    from PIL import Image


def _decode_rle(counts: list[int]) -> Any:
    """Decode full-length RLE to a flat binary uint8 array.

    The server encodes masks as ``[bg, fg, bg, fg, ...]`` where
    ``sum(counts) == total_pixels``.  Odd-indexed counts are foreground.
    """
    import numpy as np

    total = sum(counts)
    flat = np.zeros(total, dtype=np.uint8)
    pos = 0
    for i, c in enumerate(counts):
        if i % 2 == 1:  # odd = foreground
            flat[pos : pos + c] = 1
        pos += c
    return flat


class MaskRLE(BaseModel):
    """Run-length encoded mask."""

    counts: list[int]
    size: list[int]

    def decode(self) -> np.ndarray:
        """Decode RLE to a flat binary uint8 array.

        The server encodes masks as full-length RLE: ``[bg, fg, bg, fg, ...]``
        where ``sum(counts) == total_pixels``.
        Use :meth:`Detection.mask` with the source image to obtain a
        full ``(H, W)`` mask at image resolution.
        """
        return _decode_rle(self.counts)

    def to_pil(self) -> Image.Image:
        """Decode to a PIL Image in mode 'L' (0/255)."""
        from PIL import Image

        arr = self.decode() * 255
        return Image.fromarray(arr, mode="L")


class Detection:
    """A single detection from a PredictionResult.

    Constructed lazily — not a wire model.
    """

    __slots__ = ("index", "mask_rle", "box", "score")

    def __init__(
        self,
        index: int,
        mask_rle: MaskRLE,
        box: list[float],
        score: float,
    ) -> None:
        self.index = index
        self.mask_rle = mask_rle
        self.box = box
        self.score = score

    def image_box(self) -> tuple[int, int, int, int]:
        """Bounding box in standard image coordinates ``(x0, y0, x1, y1)``."""
        x0, y0, x1, y1 = self.box
        return (int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))

    # -- Mask decode -------------------------------------------------------

    def mask(self, image: Image.Image | None = None) -> np.ndarray:
        """Decoded binary mask as ``(H, W)`` uint8 array.

        Parameters
        ----------
        image:
            Source image.  When provided the mask is placed at the correct
            position within a full ``(H, W)`` array matching the image
            dimensions.  Without it, only a flat compact decode is returned.
        """
        if image is None:
            return self.mask_rle.decode()
        return self._full_mask(image.size)

    def mask_pil(self, image: Image.Image | None = None) -> Image.Image:
        """Decoded mask as PIL Image (mode 'L')."""
        from PIL import Image as PILImage

        if image is not None:
            arr = self._full_mask(image.size) * 255
            return PILImage.fromarray(arr, mode="L")
        return self.mask_rle.to_pil()

    def _full_mask(self, image_size: tuple[int, int]) -> np.ndarray:
        """Decode full-length RLE into a ``(H, W)`` image-resolution mask."""
        import numpy as np

        W_img, H_img = image_size
        flat = _decode_rle(self.mask_rle.counts)
        expected = W_img * H_img
        if len(flat) != expected:
            if len(flat) > expected:
                flat = flat[:expected]
            else:
                padded = np.zeros(expected, dtype=np.uint8)
                padded[: len(flat)] = flat
                flat = padded
        return flat.reshape(H_img, W_img)

    # -- Crop / extract ----------------------------------------------------

    def crop(self, image: Image.Image) -> Image.Image:
        """Return the bounding-box crop of *image*."""
        return image.crop(self.image_box())

    def extract(self, image: Image.Image) -> Image.Image:
        """Return an RGBA image cropped to the bbox, transparent outside the mask."""
        import numpy as np
        from PIL import Image as PILImage

        W, H = image.size
        x0, y0, x1, y1 = self.image_box()
        # Clamp to image bounds (PIL.crop does this too)
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(W, x1), min(H, y1)
        cropped = image.crop((x0, y0, x1, y1)).convert("RGBA")
        mask_arr = self._full_mask(image.size)
        mask_crop = mask_arr[y0:y1, x0:x1]
        alpha = PILImage.fromarray((mask_crop * 255).astype(np.uint8), mode="L")
        cropped.putalpha(alpha)
        return cropped

    def __repr__(self) -> str:
        return f"Detection(index={self.index}, score={self.score:.3f}, box={[round(v, 1) for v in self.box]})"


class PredictionResult(BaseModel):
    """Result from a single segmentation prediction."""

    masks_rle: list[MaskRLE] = []
    boxes: list[list[float]] = []
    scores: list[float] = []
    num_detections: int = 0
    elapsed_ms: float = 0

    def __getitem__(self, idx: int) -> Detection:
        if idx < 0:
            idx += self.num_detections
        if idx < 0 or idx >= self.num_detections:
            raise IndexError(f"Detection index {idx} out of range [0, {self.num_detections})")
        return Detection(
            index=idx,
            mask_rle=self.masks_rle[idx],
            box=self.boxes[idx],
            score=self.scores[idx],
        )

    def __iter__(self):
        for i in range(self.num_detections):
            yield self[i]

    def __len__(self) -> int:
        return self.num_detections

    def detections(self) -> list[Detection]:
        """Return all detections as a list."""
        return list(self)

    def masks(self, image: Image.Image | None = None) -> list[np.ndarray]:
        """Return all decoded masks as a list of numpy arrays."""
        return [det.mask(image) for det in self]

    def __repr__(self) -> str:
        return f"PredictionResult(num_detections={self.num_detections}, scores={[round(s, 3) for s in self.scores]})"


class BatchResult(BaseModel):
    """Result from a batch segmentation prediction."""

    results: list[PredictionResult] = []
    elapsed_ms: float = 0
    batch_size: int = 0

    def __getitem__(self, idx: int) -> PredictionResult:
        return self.results[idx]

    def __iter__(self):
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __repr__(self) -> str:
        return f"BatchResult(batch_size={self.batch_size}, elapsed_ms={self.elapsed_ms})"


# ─── OmniParser UI element models ────────────────────────────────────


class UIElement(BaseModel):
    """A single UI element detected by OmniParser."""

    bbox: list[float]  # normalized [x0, y0, x1, y1] in 0..1
    bbox_pixels: list[int]  # absolute [x0, y0, x1, y1]
    element_type: str  # "icon" or "text"
    content: str  # caption for icons, OCR text for text regions
    confidence: float
    interactable: bool

    def image_box(self) -> tuple[int, int, int, int]:
        """Bounding box in pixel coordinates ``(x0, y0, x1, y1)``."""
        return (self.bbox_pixels[0], self.bbox_pixels[1], self.bbox_pixels[2], self.bbox_pixels[3])

    def crop(self, image: Image.Image) -> Image.Image:
        """Return the bounding-box crop of *image*."""
        return image.crop(self.image_box())

    def __repr__(self) -> str:
        return f"UIElement(type={self.element_type!r}, content={self.content!r}, confidence={self.confidence:.2f})"


class UIParseResult(BaseModel):
    """Result from OmniParser UI parsing."""

    elements: list[UIElement] = []
    image_width: int = 0
    image_height: int = 0
    num_icons: int = 0
    num_text_regions: int = 0
    elapsed_ms: float = 0

    @property
    def icons(self) -> list[UIElement]:
        return [e for e in self.elements if e.element_type == "icon"]

    @property
    def text_regions(self) -> list[UIElement]:
        return [e for e in self.elements if e.element_type == "text"]

    def __getitem__(self, idx: int) -> UIElement:
        return self.elements[idx]

    def __iter__(self):
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

    def __repr__(self) -> str:
        return f"UIParseResult(icons={self.num_icons}, text={self.num_text_regions}, elapsed_ms={self.elapsed_ms})"
