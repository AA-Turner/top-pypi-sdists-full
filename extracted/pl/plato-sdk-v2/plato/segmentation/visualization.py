"""Segmentation visualization utilities (PIL/numpy only — no OpenCV or matplotlib)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
    from plato.segmentation.models import PredictionResult, UIParseResult

# 30-colour static palette (RGB)
_PALETTE: list[tuple[int, int, int]] = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (128, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (255, 128, 0),
    (255, 0, 128),
    (128, 255, 0),
    (0, 255, 128),
    (128, 0, 255),
    (0, 128, 255),
    (200, 100, 50),
    (50, 200, 100),
    (100, 50, 200),
    (200, 200, 50),
    (50, 200, 200),
    (200, 50, 200),
    (150, 75, 0),
    (0, 150, 75),
    (75, 0, 150),
    (255, 200, 150),
    (150, 255, 200),
    (200, 150, 255),
]


def render_overlay(
    image: Image.Image,
    result: PredictionResult,
    alpha: float = 0.5,
    draw_boxes: bool = True,
    draw_labels: bool = True,
) -> Image.Image:
    """Render coloured mask overlay with optional bounding boxes and score labels.

    Args:
        image: Source RGB image.
        result: A PredictionResult from the segmentation SDK.
        alpha: Blending factor for the colour overlay (0 = invisible, 1 = opaque).
        draw_boxes: Whether to draw bounding-box rectangles.
        draw_labels: Whether to draw score labels near boxes.

    Returns:
        A new RGB PIL Image with the overlay composited.
    """
    base = image.convert("RGB").copy()
    overlay = np.array(base, dtype=np.float64)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    for det in result:
        colour = _PALETTE[det.index % len(_PALETTE)]
        mask_arr = det.mask(image)  # full (H, W) mask at image resolution

        # Alpha-blend colour through the mask
        fg = mask_arr.astype(bool)
        overlay[fg] = (1 - alpha) * overlay[fg] + alpha * np.array(colour, dtype=np.float64)

    out = Image.fromarray(overlay.astype(np.uint8))
    draw = ImageDraw.Draw(out)

    for det in result:
        colour = _PALETTE[det.index % len(_PALETTE)]
        x0, y0, x1, y1 = det.image_box()

        if draw_boxes:
            draw.rectangle([x0, y0, x1, y1], outline=colour, width=2)

        if draw_labels:
            label = f"{det.score:.2f}"
            bbox = draw.textbbox((x0, y0), label, font=font)
            draw.rectangle([bbox[0] - 1, bbox[1] - 1, bbox[2] + 1, bbox[3] + 1], fill=colour)
            draw.text((x0, y0), label, fill=(255, 255, 255), font=font)

    return out


def save_extractions(
    image: Image.Image,
    result: PredictionResult,
    output_dir: str | Path,
    prefix: str = "segment",
) -> list[Path]:
    """Extract each detection as an RGBA PNG (transparent outside mask).

    Args:
        image: Source RGB image.
        result: A PredictionResult from the segmentation SDK.
        output_dir: Directory to write PNGs into (created if needed).
        prefix: Filename prefix; files are named ``{prefix}_{i:03d}.png``.

    Returns:
        List of written file paths.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for det in result:
        p = out / f"{prefix}_{det.index:03d}.png"
        det.extract(image).save(p)
        paths.append(p)
    return paths


# ─── OmniParser UI visualization ─────────────────────────────────────

_ICON_COLOR = (0, 120, 255)  # blue
_TEXT_COLOR = (0, 200, 80)  # green


def render_ui_overlay(
    image: Image.Image,
    result: UIParseResult,
    alpha: float = 0.25,
) -> Image.Image:
    """Draw bounding boxes and labels for UI elements on the image.

    Icons are drawn in blue, text regions in green.
    """
    base = image.convert("RGB").copy()
    draw = ImageDraw.Draw(base, "RGBA")

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    for el in result:
        colour = _ICON_COLOR if el.element_type == "icon" else _TEXT_COLOR
        x0, y0, x1, y1 = el.bbox_pixels
        fill = colour + (int(alpha * 255),)
        draw.rectangle([x0, y0, x1, y1], outline=colour, fill=fill, width=2)

        label = el.content[:40]
        bbox = draw.textbbox((x0, y0 - 16), label, font=font)
        draw.rectangle([bbox[0] - 1, bbox[1] - 1, bbox[2] + 1, bbox[3] + 1], fill=colour)
        draw.text((x0, y0 - 16), label, fill=(255, 255, 255), font=font)

    return base


def save_ui_crops(
    image: Image.Image,
    result: UIParseResult,
    output_dir: str | Path,
) -> list[Path]:
    """Save each UI element as a cropped PNG.

    Files are named by type and index, e.g. ``icon_003.png``, ``text_012.png``.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, el in enumerate(result):
        p = out / f"{el.element_type}_{i:03d}.png"
        el.crop(image).save(p)
        paths.append(p)
    return paths
